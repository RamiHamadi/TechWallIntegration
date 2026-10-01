"""Tech Wall ep.6 — iPhone keyboard trackpad (hold the spacebar) — Blueprint stop-motion"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw
import screens as S
from screens import F, TXT, GRAY, BLUE, SW, SH
import movie as m
import movie_blue as mb
import themes as th
from lib import rotate_sprite, rng_for, FPS, ease

OUT = __import__('lib').out('frames_trackpad')
mb.OUT = OUT
NAVY, MID, YEL, PAPER = mb.NAVY, mb.MID, mb.YEL, mb.PAPER

TINT = (222, 166, 0)            # Notes accent (cursor, buttons)
SELC = (255, 236, 160)          # selection highlight
KB_BG, KEY, KEY_SH, KEY_DK = (208, 211, 218), (255, 255, 255), (138, 140, 146), (171, 176, 188)
TP_KEY = (222, 224, 229)        # keys while the keyboard is a trackpad
BODY = F(400, 34)
X0, Y_BODY, LH = 30, 300, 54
LINES = ['Meet Sam at teh cafe', 'at 10:30 on Saturday.', 'Email: sam@exmple.com', 'Bring the charger!']
KB_TOP = 700


# ======================================================================= Notes screen + keyboard
def key_layout():
    """{id: (x0, y0, x1, y1, label, dark)} in screen coords"""
    keys = {}
    gap, kw, kh = 8, 47.2, 84
    rows = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM']
    y = KB_TOP + 14
    for r, row in enumerate(rows):
        n = len(row)
        x = (SW - (n * kw + (n - 1) * gap)) / 2
        for ch in row:
            keys['k_' + ch.lower()] = (x, y, x + kw, y + kh, ch.lower(), False)
            x += kw + gap
        if r == 2:
            keys['shift'] = (5, y, 5 + 66, y + kh, 'shift', True)
            keys['bksp'] = (SW - 5 - 66, y, SW - 5, y + kh, 'bksp', True)
        y += kh + 22
    keys['k123'] = (5, y, 105, y + kh, '123', True)
    keys['emoji'] = (113, y, 173, y + kh, 'emoji', True)
    keys['space'] = (181, y, SW - 113, y + kh, 'space', False)
    keys['ret'] = (SW - 105, y, SW - 5, y + kh, 'return', True)
    return keys


KEYS = key_layout()


def text_x(line, idx):
    """x of a (possibly fractional) cursor index in line"""
    i = int(idx); fr = idx - i
    x = X0 + BODY.getlength(line[:i])
    if fr and i < len(line):
        x += fr * BODY.getlength(line[i])
    return x


def draw_keyboard(d, tp, hl):
    d.rectangle((0, KB_TOP, SW, SH), fill=KB_BG)
    for kid, (x0, y0, x1, y1, lab, dark) in KEYS.items():
        if tp:
            d.rounded_rectangle((x0, y0, x1, y1), 10, fill=TP_KEY)
            continue
        col = KEY_DK if dark else KEY
        if kid == hl:
            col = KEY_DK if not dark else KEY
        d.rounded_rectangle((x0, y0 + 2, x1, y1 + 2), 10, fill=KEY_SH)
        d.rounded_rectangle((x0, y0, x1, y1), 10, fill=col)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if lab == 'shift':
            d.polygon([(cx, cy - 18), (cx - 17, cy), (cx - 8, cy), (cx - 8, cy + 15), (cx + 8, cy + 15), (cx + 8, cy), (cx + 17, cy)],
                      outline=TXT, width=3)
        elif lab == 'bksp':
            d.polygon([(cx - 24, cy), (cx - 10, cy - 14), (cx + 20, cy - 14), (cx + 20, cy + 14), (cx - 10, cy + 14)], outline=TXT, width=3)
            d.line([(cx - 3, cy - 6), (cx + 9, cy + 6)], fill=TXT, width=3); d.line([(cx - 3, cy + 6), (cx + 9, cy - 6)], fill=TXT, width=3)
        elif lab == 'emoji':
            d.ellipse((cx - 17, cy - 17, cx + 17, cy + 17), outline=TXT, width=3)
            d.ellipse((cx - 8, cy - 7, cx - 3, cy - 2), fill=TXT); d.ellipse((cx + 3, cy - 7, cx + 8, cy - 2), fill=TXT)
            d.arc((cx - 10, cy - 8, cx + 10, cy + 10), 30, 150, fill=TXT, width=3)
        elif lab in ('space', '123', 'return'):
            d.text((cx, cy), lab, font=F(400, 28), fill=TXT, anchor='mm')
        else:
            d.text((cx, cy - 2), lab, font=F(400, 40), fill=TXT, anchor='mm')
    if tp:
        return
    # globe + mic strip under the keys
    gy = SH - 50
    d.ellipse((44, gy - 18, 80, gy + 18), outline=(90, 92, 98), width=3)
    d.line([(44, gy), (80, gy)], fill=(90, 92, 98), width=2); d.ellipse((54, gy - 18, 70, gy + 18), outline=(90, 92, 98), width=2)
    d.rounded_rectangle((SW - 70, gy - 20, SW - 56, gy + 4), 7, outline=(90, 92, 98), width=3)
    d.arc((SW - 77, gy - 12, SW - 49, gy + 12), 0, 180, fill=(90, 92, 98), width=3)
    d.line([(SW - 63, gy + 12), (SW - 63, gy + 20)], fill=(90, 92, 98), width=3)


def notes_content(ov, hl):
    img = Image.new('RGB', (SW, SH), (255, 255, 255))
    d = ImageDraw.Draw(img)
    y = 112
    S.chevron(d, 24, y + 24, TINT, w=5, s=11, left=True)
    d.text((50, y + 24), 'Notes', font=F(500, 32), fill=TINT, anchor='lm')
    d.text((SW - 30, y + 24), 'Done', font=F(600, 32), fill=TINT, anchor='rm')
    d.text((SW / 2, 196), '1 October 2026 at 9:41', font=F(400, 22), fill=GRAY, anchor='mm')
    d.text((X0, 222), 'Weekend plans', font=F(600, 44), fill=TXT, anchor='lt')
    lines = list(ov.get('lines', LINES))
    sel = ov.get('sel')
    if sel:
        ln, a, b = sel
        ly = Y_BODY + ln * LH
        xa, xb = text_x(lines[ln], a), text_x(lines[ln], b)
        d.rectangle((xa, ly - 4, xb, ly + 44), fill=SELC)
        for xx, top in ((xa, True), (xb, False)):
            d.line([(xx, ly - 4), (xx, ly + 44)], fill=TINT, width=4)
            cy = ly - 10 if top else ly + 50
            d.ellipse((xx - 8, cy - 8, xx + 8, cy + 8), fill=TINT)
    for i, ln in enumerate(lines):
        d.text((X0, Y_BODY + i * LH), ln, font=BODY, fill=TXT, anchor='lt')
    cur = ov.get('cur')
    if cur and not sel:
        ln, idx = cur
        cx = text_x(lines[ln], idx); cy = Y_BODY + ln * LH
        if ov.get('tp'):
            # floating cursor while the keyboard is a trackpad
            d.rounded_rectangle((cx - 4, cy - 10, cx + 4, cy + 50), 4, fill=(120, 120, 128))
            d.rounded_rectangle((cx - 2, cy - 4, cx + 3, cy + 44), 2, fill=TINT)
        else:
            d.rounded_rectangle((cx - 2, cy - 4, cx + 2, cy + 44), 2, fill=TINT)
    draw_keyboard(d, ov.get('tp'), hl)
    rows = {k: v[:4] for k, v in KEYS.items()}
    for i, ln in enumerate(lines):
        rows[f'line{i}'] = (X0, Y_BODY + i * LH, X0 + BODY.getlength(ln), Y_BODY + i * LH + 40)
    return img, rows


_orig = S.screen_content
_cache = {}


def screen_content(name, ov=None, hl=None):
    ov = ov or {}
    if name != 'notes':
        return _orig(name, ov, hl)
    key = (name, tuple(sorted(ov.items())), hl)
    if key not in _cache:
        if len(_cache) > 24:
            _cache.clear()
        _cache[key] = notes_content(ov, hl)
    return _cache[key]


S.screen_content = screen_content
_view = S.view


def view(spec):
    if spec['name'] != 'notes':
        return _view(spec)
    v = screen_content('notes', spec.get('ov'), spec.get('hl'))[0].copy()
    S.status_bar(v, dark_text=True, bg=(255, 255, 255))
    return v


m.view = view


def row_point(spec, rid, fx=0.5):
    _, rows = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    return x0 + (x1 - x0) * fx, (y0 + y1) / 2 - spec.get('scroll', 0)


m.row_point = row_point


# ======================================================================= timeline helpers
def spec(name, **kw):
    d = dict(name=name, scroll=0, hl=None, ov={})
    d.update(kw)
    return d


def key_tap(t, kid, change, n_move=3):
    """quick keyboard tap: move, press (ring + highlight), apply ov change, release"""
    sp = t.ph['spec']
    tx, ty = t.s2c(*row_point(sp, kid))
    t.move_hand(tx, ty, n_move)
    t.press(tx, ty)
    sp['hl'] = kid
    sp['ov'].update(change)
    t.snap()
    t.hand['press'] = False
    sp['hl'] = None
    t.hold(2)


def hold_space(t):
    """touch & hold the spacebar until the keyboard turns into a trackpad"""
    sp = t.ph['spec']
    tx, ty = t.s2c(*row_point(sp, 'space'))
    t.move_hand(tx, ty, 6); t.hold(2)
    t.press(tx, ty)
    t.hold(5)
    sp['ov']['tp'] = True
    t.sound('pop')
    t.hold(4)


def slide(t, to, n, ov_key='cur', sel_from=None):
    """drag on the keyboard while the cursor (or selection end) glides to `to` = (line, idx)"""
    sp = t.ph['spec']
    ov = sp['ov']
    l0, i0 = ov['cur'] if sel_from is None else (sel_from[0], ov['sel'][2])
    l1, i1 = to
    lines = ov.get('lines', LINES)
    x0, y0 = text_x(lines[l0], i0), Y_BODY + l0 * LH
    x1, y1 = text_x(lines[l1], i1), Y_BODY + l1 * LH
    hx, hy = t.hand['x'], t.hand['y']
    t.sound('swish')
    for k in range(1, n + 1):
        e = ease(k / n)
        cx, cy = x0 + (x1 - x0) * e, y0 + (y1 - y0) * e
        if sel_from is None:
            # snap the line to the nearest row, the index follows the x position
            ln = l0 if e < 0.5 else l1
            idx = i0 + (i1 - i0) * e if l0 == l1 else idx_at(lines[ln], cx)
            ov['cur'] = (ln, round(idx * 4) / 4)
        else:
            ov['sel'] = (sel_from[0], sel_from[1], round((i0 + (i1 - i0) * e) * 4) / 4)
        t.hand.update(x=hx + (cx - x0) * 0.7, y=hy + (cy - y0) * 0.7, press=True)
        t.snap()


def idx_at(line, x):
    best, bi = 1e9, 0
    for i in range(len(line) + 1):
        dx = abs(text_x(line, i) - x)
        if dx < best:
            best, bi = dx, i
    return bi


def release(t):
    t.hand['press'] = False
    t.ph['spec']['ov']['tp'] = False
    t.sound('tap')
    t.hold(2)


# ======================================================================= timeline
def build():
    t = m.TL()
    t.ph['spec'] = spec('notes', ov={'lines': tuple(LINES), 'cur': (3, 18)})
    t.fx.append(('title', 0, 86)); t.hold(92)
    t.phone_to(m.PHY, 6, keys=-40); t.hold(2)
    sp = t.ph['spec']
    # ---- the problem: tapping on a typo lands in the wrong place
    t.cap('P', 'Tapping on a typo to fix it? Missed again', m.PINK); t.hold(4)
    tx, ty = t.s2c(text_x(LINES[0], 13.5), Y_BODY + 20)
    t.move_hand(tx, ty, 6); t.hold(2); t.press(tx, ty)
    sp['ov']['cur'] = (0, 20); t.hold(2); t.hand['press'] = False
    t.fx.append(('burst', t.f, 830, 760, 0)); t.sound('knock'); t.hold(12)
    t.hand_out(4)
    t.cap('Q', 'Your spacebar is a hidden trackpad', m.YELLOW); t.hold(24)
    # ---- step 1: hold the spacebar
    t.cap('1', 'Touch & hold the spacebar', m.YELLOW); t.hold(6)
    hold_space(t); t.hold(4)
    # ---- step 2: slide to move the cursor
    t.cap('2', 'Slide your finger to move the cursor', m.PINK); t.hold(4)
    slide(t, (0, 16), 6)
    slide(t, (0, 15), 3)
    t.hold(4)
    release(t)
    # ---- fix the typo: teh -> the
    lines = list(LINES)
    for ch_line, cur in (('Meet Sam at te cafe', 14), ('Meet Sam at t cafe', 13)):
        key_tap(t, 'bksp', {'lines': (ch_line,) + tuple(lines[1:]), 'cur': (0, cur)})
    for kid, ch_line, cur in (('k_h', 'Meet Sam at th cafe', 14), ('k_e', 'Meet Sam at the cafe', 15)):
        key_tap(t, kid, {'lines': (ch_line,) + tuple(lines[1:]), 'cur': (0, cur)})
    lines[0] = 'Meet Sam at the cafe'
    t.sound('ding')
    t.hand_out(4)
    t.cap('check', 'Typo fixed, exactly where you wanted', m.MINT)
    t.fx.append(('burst', t.f, 800, 760, 1)); t.hold(24)
    # ---- field test: fix one letter inside an email address
    t.cap('T', 'Fix one letter in an email address', m.PEACH); t.hold(6)
    hold_space(t)
    slide(t, (2, 13), 8)
    t.hold(4)
    release(t)
    lines[2] = 'Email: sam@example.com'
    key_tap(t, 'k_a', {'lines': tuple(lines), 'cur': (2, 14)}, n_move=4)
    t.sound('ding')
    t.fx.append(('burst', t.f, 800, 860, 1)); t.hold(8)
    t.hand_out(4); t.hold(10)
    # ---- bonus: second finger selects text
    t.cap('+', 'Bonus: add a 2nd finger to select text', m.SKY); t.hold(6)
    hold_space(t)
    slide(t, (1, 12), 6)
    t.hold(3)
    fx2, fy2 = t.s2c(*row_point(sp, 'k_d'))
    t.fx.append(('ring', t.f, fx2, fy2)); t.sound('tap')
    t.fx.append(('burst', t.f, 300, 1500, 2))
    sp['ov']['sel'] = (1, 12, 12); t.hold(4)
    slide(t, (1, 20), 8, sel_from=(1, 12))
    t.hold(14)
    release(t)
    t.hand_out(4); t.hold(10)
    t.cap_off()
    t.phone_to(2700, 5)
    t.fx.append(('end', t.f)); t.hold(72)
    return t


# ======================================================================= props / title / end
def fig_head(badge):
    if badge.isdigit():
        return f'FIG. 0{badge}  /  STEP {badge} OF 2'
    return {'P': 'FIG. 00  /  THE PROBLEM', 'Q': 'FIG. 00  /  THE FIX', 'T': 'FIG. 03  /  FIELD TEST',
            'check': 'RESULT  /  OK', '+': 'APPENDIX  /  BONUS'}[badge]


mb.fig_head = fig_head


def vellum_keyboard():
    w, h = 300, 560
    im = Image.new('RGBA', (w, h), (230, 240, 255, 70))
    d = ImageDraw.Draw(im)
    C = th.CHALK + (255,)
    d.rounded_rectangle((20, 20, w - 20, h - 20), 46, outline=C, width=5)
    d.rounded_rectangle((w / 2 - 50, 36, w / 2 + 50, 60), 12, fill=C)
    for k, ln in enumerate((170, 120, 190)):
        d.line([(50, 110 + 34 * k), (50 + ln, 110 + 34 * k)], fill=C, width=6)
    d.line([(152, 92), (152, 124)], fill=mb.YEL + (255,), width=6)
    for r in range(3):
        for c in range(6):
            x = 46 + c * 36 + (r % 2) * 10
            d.rounded_rectangle((x, 290 + r * 46, x + 26, 322 + r * 46), 6, outline=C, width=3)
    d.rounded_rectangle((80, 432, 220, 470), 10, fill=mb.YEL + (255,))
    th.dashed_circle(d, 150, 451, 52, C, 4)
    for s in (-1, 1):
        x = 150 + s * 80
        d.line([(150 + s * 60, 510), (x, 510)], fill=C, width=4)
        d.polygon([(x + s * 12, 510), (x, 500), (x, 520)], fill=C)
    sp = th.sprite(im, border=0, off=(6, 9), blur=6, op=.3, tex=False)
    return rotate_sprite(sp, 8)


def init_props():
    mb.init_props()
    P = m.P
    tiles = []
    for i, ch in enumerate('SPACE'):
        tiles.append(rotate_sprite(th.stencil_letter(ch, PAPER), rng_for('s', i).uniform(-4, 4)))
    for i, ch in enumerate('TRACKPAD'):
        sp = th.stencil_letter(ch, YEL)
        sp = tuple(s_.resize((int(s_.width * .58), int(s_.height * .58)), Image.LANCZOS) for s_ in sp)
        tiles.append(rotate_sprite(sp, rng_for('k', i).uniform(-5, 5)))
    P['tiles'] = tiles
    P['t_label'] = mb.label('SPEC // iPhone tip', th.JB(700, 34), fg=MID, rot=-2, padx=30, pady=16)
    P['t_s1'] = mb.center_label('STOP TAPPING TO FIX TYPOS', th.JB(800, 44), rot=1.5)
    P['t_s1b'] = mb.center_label('YOUR SPACEBAR HIDES A TRACKPAD', th.JB(800, 44), rot=-1)
    P['t_s2'] = mb.center_label('keyboard trackpad', th.JB(700, 40), bg=YEL, rot=-2)
    P['t_phone'] = vellum_keyboard()
    P['t_burst'] = mb.label(['iOS 12', '& LATER'], th.JB(800, 38), rot=6, padx=26, pady=16)
    P['bursts'] = [mb.label('MISSED!', th.JB(800, 64), tape=True, rot=-8, padx=30, pady=12),
                   mb.label('FIXED!', th.JB(800, 64), bg=YEL, tape=True, rot=7, padx=30, pady=12),
                   mb.label('+ 2ND FINGER', th.JB(800, 52), bg=YEL, tape=True, rot=-6, padx=26, pady=12)]
    P['e_chips'] = [rotate_sprite(mb.path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('Tap any text', TINT, 'dot', -2), ('Hold SPACE', BLUE, 'touch', 1.5), ('Slide finger', BLUE, 'touch', -1.5),
        ('Let go', NAVY, 'touch', 2)])]
    P['e_s1'] = mb.center_label('2ND FINGER = SELECT TEXT', th.JB(800, 46), bg=YEL, rot=-1.5)
    P['e_s2'] = mb.center_label('WORKS ANYWHERE YOU TYPE', th.JB(800, 46), rot=1.5)
    P['e_s3'] = mb.center_label('iPhone & iPad with iOS 12 or later', th.JB(600, 34), fg=MID, rot=-1, pady=18)


def draw_title(cv, f, a, ex):
    P = m.P
    els = [('t_label', 540, 380, a + 1, 0)]
    for i in range(5):
        els.append((i, 540 + (i - 2) * 160, 590, a + 4 + 2 * i, i % 3))
    for i in range(8):
        els.append((5 + i, 540 + (i - 3.5) * 112, 790, a + 12 + i, i % 3))
    els += [('t_s1', 540, 960, a + 22, 0), ('t_s1b', 540, 1060, a + 25, 1), ('t_s2', 520, 1180, a + 28, 2),
            ('t_phone', 540, 1560, a + 31, 0), ('t_burst', 820, 1420, a + 34, 1)]
    for key, x, y, ap, stg in els:
        yy = m.drop_y(f, ap, y, ex, stg)
        if yy is None:
            continue
        sp = P['tiles'][key] if isinstance(key, int) else P[key]
        m.put(cv, sp, x, yy, f, ('t', key))


m.draw_title = draw_title


def add_sounds(t):
    for e in t.fx:
        if e[0] == 'title':
            a = e[1]
            for ap in [a + 1] + [a + 4 + 2 * i for i in range(5)] + [a + 12 + i for i in range(0, 8, 2)] + [a + 22, a + 25, a + 28, a + 31, a + 34]:
                t.snd.append((ap, 'pop'))
            t.snd.append((e[2] + 1, 'whoosh'))
        if e[0] == 'end':
            a = e[1]
            for ap in [a + 2] + [a + 6 + 4 * i for i in range(4)] + [a + 24, a + 28, a + 32]:
                t.snd.append((ap, 'pop'))
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))


if __name__ == '__main__':
    t = build()
    add_sounds(t)
    m.TLD = dict(frames=t.frames, fx=t.fx, caps=t.caps, snd=t.snd)
    n = len(t.frames)
    print('frames', n, 'seconds', n / FPS, flush=True)
    for c in t.caps:
        print(c['inn'], c['out'], c['text'])
    os.makedirs(OUT, exist_ok=True)
    init_props()
    only = [int(a) for a in sys.argv[1:]]
    if only:
        for f in only:
            if f < n:
                mb.render(f)
    else:
        with Pool(2) as pool:
            for i, _ in enumerate(pool.imap(mb.render, range(n), chunksize=8)):
                if i % 100 == 0:
                    print('rendered', i, flush=True)
        m.make_audio(m.TLD, n, __import__('lib').out('audio_trackpad.wav'))

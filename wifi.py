"""Tech Wall ep.3 — See your saved Wi-Fi password on iPhone — Blueprint stop-motion"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw
import screens as S
from screens import F, BG_UI, CARD, SEP, TXT, GRAY, BLUE, GREEN, HL, ROW, CX0, CX1, SW, SH, chevron, checkmark, glyph
import movie as m
import movie_blue as mb
import themes as th
from lib import rotate_sprite, rng_for, FPS

OUT = __import__('lib').out('frames_wifi')
mb.OUT = OUT
NAVY, MID, YEL, PAPER = mb.NAVY, mb.MID, mb.YEL, mb.PAPER
PASSWORD = 'SunnyDays2024'


# ======================================================================= custom iOS screens
def wifi_glyph(d, cx, cy, col, s=1.0):
    for r_ in (18 * s, 11 * s):
        d.arc((cx - r_, cy - r_ + 6 * s, cx + r_, cy + r_ + 6 * s), 225, 315, fill=col, width=max(2, int(3 * s)))
    d.ellipse((cx - 3 * s, cy + 3 * s, cx + 3 * s, cy + 9 * s), fill=col)


def lock_glyph(d, cx, cy, col):
    d.rounded_rectangle((cx - 8, cy - 2, cx + 8, cy + 11), 3, fill=col)
    d.arc((cx - 6, cy - 12, cx + 6, cy + 4), 180, 360, fill=col, width=3)


def info_glyph(d, cx, cy, col=BLUE):
    d.ellipse((cx - 17, cy - 17, cx + 17, cy + 17), outline=col, width=3)
    d.text((cx, cy + 1), 'i', font=F(600, 24), fill=col, anchor='mm')


def net_card(nets, hl):
    """nets: list of (id, name, connected)"""
    n = len(nets)
    img = Image.new('RGB', (CX1 - CX0, ROW * n), CARD)
    d = ImageDraw.Draw(img)
    rows = {}
    w = img.width
    for i, (rid, name, conn) in enumerate(nets):
        y0 = i * ROW; cy = y0 + ROW / 2
        if hl in (rid, rid + '_i'):
            d.rectangle((0, y0, w, y0 + ROW), fill=HL)
        if conn:
            checkmark(d, 20, cy, BLUE, s=16, w=4)
        d.text((58, cy), name, font=F(500, 30), fill=TXT, anchor='lm')
        lock_glyph(d, w - 132, cy, TXT)
        wifi_glyph(d, w - 92, cy - 6, TXT)
        info_glyph(d, w - 40, cy)
        if i < n - 1:
            d.line([(58, y0 + ROW - 1), (w, y0 + ROW - 1)], fill=SEP, width=2)
        rows[rid] = (0, y0, w, y0 + ROW)
        rows[rid + '_i'] = (w - 70, y0 + 10, w - 10, y0 + ROW - 10)
    mk = Image.new('L', img.size, 0)
    ImageDraw.Draw(mk).rounded_rectangle((0, 0, img.width - 1, img.height - 1), 24, fill=255)
    return img, mk, rows


def faceid(img, cx, cy):
    d = ImageDraw.Draw(img)
    s = 230
    d.rounded_rectangle((cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2), 44, fill=(228, 228, 234))
    g = 46; L = 22; c = (40, 40, 46)
    x0, y0, x1, y1 = cx - g, cy - g - 14, cx + g, cy + g - 14
    for (ax, ay, dx, dy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        d.line([(ax, ay + dy * L), (ax, ay), (ax + dx * L, ay)], fill=c, width=5, joint='curve')
    d.line([(cx - 16, cy - 30), (cx - 16, cy - 20)], fill=c, width=5)
    d.line([(cx + 16, cy - 30), (cx + 16, cy - 20)], fill=c, width=5)
    d.line([(cx + 2, cy - 30), (cx + 2, cy - 6), (cx - 6, cy - 6)], fill=c, width=4)
    d.arc((cx - 18, cy - 20, cx + 18, cy + 4), 30, 150, fill=c, width=4)
    d.text((cx, cy + 82), 'Face ID', font=F(600, 28), fill=c, anchor='mm')


def detail_content(ov, hl):
    img = Image.new('RGB', (SW, 1800), BG_UI)
    d = ImageDraw.Draw(img)
    rows = {}
    y = 112
    chevron(d, 24, y + 24, BLUE, w=5, s=11, left=True)
    d.text((50, y + 24), 'Wi-Fi', font=F(500, 32), fill=BLUE, anchor='lm')
    rows['back'] = (10, y - 6, 250, y + 56); y += 62
    d.text((30, y), 'Home', font=F(600, 62), fill=TXT, anchor='lt'); y += 98

    def card(rowspec):
        nonlocal y
        cimg, mk, ids = S.render_card(rowspec, {}, hl)
        img.paste(cimg, (CX0, y), mk)
        for k, (a0, a1) in ids.items():
            rows[k] = (CX0, y + a0, CX1, y + a1)
        y0 = y
        y += cimg.height + 34
        return y0

    yf = y
    cimg = Image.new('RGB', (CX1 - CX0, ROW), CARD)
    ImageDraw.Draw(cimg).text((22, ROW / 2), 'Forget This Network', font=F(500, 30), fill=BLUE, anchor='lm')
    mk = Image.new('L', cimg.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, cimg.width - 1, cimg.height - 1), 24, fill=255)
    img.paste(cimg, (CX0, y), mk); y += ROW + 34
    ypw = card([('autojoin', 'Auto-Join', None, None, 'toggle_on', None),
                ('password', 'Password', None, None, 'none', None)])
    # password value
    pcy = ypw + ROW + ROW / 2
    state = ov.get('pw', 'dots')
    if state == 'shown':
        d.text((CX1 - 22, pcy), PASSWORD, font=F(500, 30), fill=TXT, anchor='rm')
    else:
        for k in range(10):
            x = CX1 - 30 - k * 20
            d.ellipse((x - 6, pcy - 6, x + 6, pcy + 6), fill=GRAY)
    card([('lowdata', 'Low Data Mode', None, None, 'toggle_off', None),
          ('private', 'Private Wi-Fi Address', None, None, 'toggle_on', None)])
    d.text((44, y + 26), 'IPV4 ADDRESS', font=F(500, 23), fill=GRAY, anchor='lm'); y += 50
    card([('cfg', 'Configure IP', None, 'Automatic', 'chev', None),
          ('ip', 'IP Address', None, '192.168.1.24', 'none', None)])
    if ov.get('copy'):
        bx = CX1 - 110; by = pcy - ROW / 2 - 40
        d.rounded_rectangle((bx - 66, by - 34, bx + 66, by + 30), 16, fill=(44, 44, 48))
        d.polygon([(bx - 14, by + 29), (bx + 14, by + 29), (bx, by + 44)], fill=(44, 44, 48))
        d.text((bx, by - 2), 'Copy', font=F(500, 30), fill=(255, 255, 255), anchor='mm')
        rows['copybtn'] = (bx - 66, by - 34, bx + 66, by + 30)
    if state == 'faceid':
        faceid(img, SW / 2, 560)
    return img.crop((0, 0, SW, max(SH, y + 40))), rows


def wifi_content(ov, hl):
    img = Image.new('RGB', (SW, 1800), BG_UI)
    d = ImageDraw.Draw(img)
    rows = {}
    y = 112
    chevron(d, 24, y + 24, BLUE, w=5, s=11, left=True)
    d.text((50, y + 24), 'Settings', font=F(500, 32), fill=BLUE, anchor='lm')
    rows['back'] = (10, y - 6, 250, y + 56)
    if not ov.get('edit'):
        d.text((SW - 30, y + 24), 'Edit', font=F(500, 32), fill=BLUE, anchor='rm')
        rows['edit'] = (SW - 120, y - 6, SW - 10, y + 56)
    else:
        d.text((SW - 30, y + 24), 'Done', font=F(600, 32), fill=BLUE, anchor='rm')
    y += 62
    d.text((30, y), 'Wi-Fi', font=F(600, 62), fill=TXT, anchor='lt'); y += 98
    if not ov.get('edit'):
        cimg, _, ids = S.render_card([('wifitog', 'Wi-Fi', None, None, 'toggle_on', None)], {}, hl)
        nimg, _, nrows = net_card([('home', 'Home', True)], hl)
        comb = Image.new('RGB', (cimg.width, cimg.height + nimg.height), CARD)
        comb.paste(cimg, (0, 0)); comb.paste(nimg, (0, cimg.height))
        ImageDraw.Draw(comb).line([(22, cimg.height - 1), (comb.width, cimg.height - 1)], fill=SEP, width=2)
        mk = Image.new('L', comb.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, comb.width - 1, comb.height - 1), 24, fill=255)
        img.paste(comb, (CX0, y), mk)
        for k, b in nrows.items():
            rows[k] = (CX0 + b[0], y + cimg.height + b[1], CX0 + b[2], y + cimg.height + b[3])
        y += comb.height + 34
        d.text((44, y + 26), 'OTHER NETWORKS', font=F(500, 23), fill=GRAY, anchor='lm'); y += 50
        nimg, mk2, nrows = net_card([('n1', 'Neighbor_2G', False), ('n2', 'CoffeeShop', False), ('n3', 'Office_5G', False)], hl)
        img.paste(nimg, (CX0, y), mk2); y += nimg.height + 34
    else:
        d.text((44, y + 26), 'KNOWN NETWORKS', font=F(500, 23), fill=GRAY, anchor='lm'); y += 50
        nimg, mk2, nrows = net_card([('k1', 'Home', True), ('k2', 'Office_5G', False), ("k3", "Mom's House", False),
                                     ('k4', 'Hotel Lobby', False), ('k5', 'Gym WiFi', False)], hl)
        img.paste(nimg, (CX0, y), mk2)
        for k, b in nrows.items():
            rows[k] = (CX0 + b[0], y + b[1], CX0 + b[2], y + b[3])
        y += nimg.height + 34
        for ln in ['Tap the info button next to any saved network to', 'see its password.']:
            d.text((44, y - 18), ln, font=F(400, 24), fill=GRAY, anchor='lt'); y += 31
    if ov.get('faceid'):
        faceid(img, SW / 2, 560)
    return img.crop((0, 0, SW, max(SH, y + 40))), rows


_orig = S.screen_content
_cache = {}


def screen_content(name, ov=None, hl=None):
    ov = ov or {}
    if name not in ('wifi', 'wifidetail'):
        return _orig(name, ov, hl)
    key = (name, tuple(sorted(ov.items())), hl)
    if key not in _cache:
        _cache[key] = (wifi_content if name == 'wifi' else detail_content)(ov, hl)
    return _cache[key]


S.screen_content = screen_content


def row_point(spec, rid, fx=0.62):
    _, rows = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    if spec['name'] == 'home':
        return (x0 + x1) / 2 + 8, (y0 + y1) / 2 + 10
    return x0 + (x1 - x0) * fx, (y0 + y1) / 2 - spec.get('scroll', 0)


m.row_point = row_point


# ======================================================================= timeline
def spec(name, **kw):
    d = dict(name=name, scroll=0, hl=None, ov={})
    d.update(kw)
    return d


def build():
    t = m.TL()
    t.fx.append(('title', 0, 50)); t.hold(56)
    t.phone_to(m.PHY, 6, keys=-40); t.hold(2)
    t.cap('1', 'Open Settings', m.YELLOW); t.hold(8)
    t.tap('app_settings', nav=spec('settings'), n_move=7)
    t.cap('2', 'Tap Wi-Fi', m.PINK); t.hold(10)
    t.tap('wifi', nav=spec('wifi'))
    t.cap('3', 'Tap the (i) next to your network', m.MINT); t.hold(10)
    t.tap('home_i', nav=spec('wifidetail', ov={'pw': 'dots'}), fx=0.5)
    t.cap('4', 'Tap Password, unlock with Face ID', m.SKY); t.hold(10)
    t.tap('password', fx=0.5)
    t.move_hand(t.hand['x'] + 170, t.hand['y'] + 330, 3)
    t.ph['spec']['ov'] = {'pw': 'faceid'}; t.sound('pop'); t.hold(10)
    t.ph['spec']['ov'] = {'pw': 'shown', 'copy': True}; t.sound('ding'); t.hold(4)
    t.cap('check', "There's your Wi-Fi password!", m.MINT)
    tx, ty = t.s2c(*row_point(t.ph['spec'], 'password', 0.72))
    t.move_hand(tx, ty + 40, 5); t.hold(24)
    t.cap('5', 'Tap Copy to share it', m.PEACH); t.hold(8)
    t.tap('copybtn', fx=0.5, ov={'copy': False})
    t.fx.append(('burst', t.f, 790, 760, 2)); t.hold(14)
    t.hand_out(4)
    # bonus
    t.cap('+', 'Bonus: tap Edit to see old networks too', m.SKY); t.hold(8)
    t.tap('back', nav=spec('wifi'), back=True, fx=0.2)
    t.tap('edit', fx=0.5)
    t.move_hand(t.hand['x'] + 120, t.hand['y'] + 520, 3)
    t.ph['spec']['ov'] = {'faceid': True}; t.sound('pop'); t.hold(9)
    t.ph['spec']['ov'] = {'edit': True}; t.sound('ding'); t.hold(4)
    t.move_hand(*t.s2c(*row_point(t.ph['spec'], 'k3', 0.5)), 6); t.hold(22)
    t.hand_out(4)
    t.cap_off()
    t.phone_to(2700, 5)
    t.fx.append(('end', t.f)); t.hold(72)
    return t


# ======================================================================= props / title / end
def fig_head(badge):
    if badge.isdigit():
        return f'FIG. 0{badge}  /  STEP {badge} OF 5'
    return {'check': 'RESULT  /  OK', '!': 'FIG. 06  /  FIELD TEST', '+': 'APPENDIX  /  BONUS'}[badge]


mb.fig_head = fig_head


def vellum_wifi():
    w, h = 300, 560
    im = Image.new('RGBA', (w, h), (230, 240, 255, 70))
    d = ImageDraw.Draw(im)
    C = th.CHALK + (255,)
    d.rounded_rectangle((20, 20, w - 20, h - 20), 46, outline=C, width=5)
    d.rounded_rectangle((w / 2 - 50, 36, w / 2 + 50, 60), 12, fill=C)
    cx, cy = w / 2, 250
    for r_ in (100, 68, 36):
        d.arc((cx - r_, cy - r_, cx + r_, cy + r_), 220, 320, fill=C, width=8)
    d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=mb.YEL + (255,))
    d.rounded_rectangle((50, 330, w - 50, 400), 14, outline=C, width=4)
    for k in range(6):
        x = 82 + k * 28
        d.ellipse((x - 8, 357, x + 8, 373), fill=C)
    d.text((w / 2, 450), 'PASSWORD', font=th.JB(800, 30), fill=C, anchor='mm')
    sp = th.sprite(im, border=0, off=(6, 9), blur=6, op=.3, tex=False)
    return rotate_sprite(sp, 8)


def init_props():
    mb.init_props()
    P = m.P
    tiles = []
    for i, ch in enumerate('WI-FI'):
        tiles.append(rotate_sprite(th.stencil_letter(ch, PAPER), rng_for('w', i).uniform(-4, 4)))
    for i, ch in enumerate('PASSWORD'):
        sp = th.stencil_letter(ch, YEL)
        sp = tuple(s_.resize((int(s_.width * .58), int(s_.height * .58)), Image.LANCZOS) for s_ in sp)
        tiles.append(rotate_sprite(sp, rng_for('p', i).uniform(-5, 5)))
    P['tiles'] = tiles
    P['t_label'] = mb.label('SPEC // iPhone tip', th.JB(700, 34), fg=MID, rot=-2, padx=30, pady=16)
    P['t_s1'] = mb.center_label('FORGOT YOUR WI-FI PASSWORD?', th.JB(800, 44), rot=1.5)
    P['t_s1b'] = mb.center_label('YOUR iPHONE KNOWS IT', th.JB(800, 44), rot=-1)
    P['t_s2'] = mb.center_label('no router needed', th.JB(700, 40), bg=YEL, rot=-2)
    P['t_phone'] = vellum_wifi()
    P['t_burst'] = mb.label(['iOS 16', '& LATER'], th.JB(800, 38), rot=6, padx=26, pady=16)
    P['bursts'] = P['bursts'][:2] + [mb.label('COPIED!', th.JB(800, 64), bg=YEL, tape=True, rot=-8, padx=30, pady=12)]
    P['e_chips'] = [rotate_sprite(mb.path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('Settings', S.GRAYI, 'gear', -2), ('Wi-Fi', BLUE, 'wifi', 1.5), ('(i) your network', BLUE, 'dot', -1.5),
        ('Password', NAVY, 'touch', 2)])]
    P['e_s1'] = mb.center_label('TAP COPY TO SHARE IT', th.JB(800, 46), bg=YEL, rot=-1.5)
    P['e_s2'] = mb.center_label('OLD NETWORKS: TAP EDIT', th.JB(800, 46), rot=1.5)
    P['e_s3'] = mb.center_label('iPhone with iOS 16 or later', th.JB(600, 34), fg=MID, rot=-1, pady=18)


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
        m.make_audio(m.TLD, n, __import__('lib').out('audio_wifi.wav'))

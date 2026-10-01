"""Tech Wall ep.2 — Windows clipboard history (Win + V) — Blueprint stop-motion"""
import sys, os, copy, math
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter
import movie as m
import themes as th
from movie_blue import label, center_label, path_label, chalk_arrow, dashed_ring, NAVY, MID, YEL, PAPER
from lib import rotate_sprite, rng_for, FPS, ease, jit, draw_sprite, blit, apply_tex, paper_tex, wrap
from screens import glyph

OUT = __import__('lib').out('frames_winv')
W, H = 1080, 1920
BLUEW = (0, 103, 192)

# ------------------------------------------------------------------ geometry
MON_W, BEZ_H = 900, 590
SW, SH = 852, 532
MONX, MONY = 540, 930               # monitor sprite centre (raw 900 x 734)
MON_RAW_H = 734
KBX, KBY = 540, 1565
KB_W, KB_H = 1000, 380
HIDE = (1350, 2350)


def scr_origin(dy=0):
    return MONX - MON_W / 2 + 24, MONY - MON_RAW_H / 2 + 24 + dy


# keyboard layout: name -> (x, y, w) in keyboard coords, key height 74
KEYS = {}
for i, ch in enumerate('QWERTYUIOP'):
    KEYS[ch] = (62 + i * 88, 34, 78)
for i, ch in enumerate('ASDFGHJKL'):
    KEYS[ch] = (88 + i * 88, 122, 78)
for i, ch in enumerate('ZXCVBNM'):
    KEYS[ch] = (130 + i * 88, 210, 78)
KEYS.update({'CTRL': (40, 298, 120), 'WIN': (170, 298, 104), 'ALT': (284, 298, 104), 'SPACE': (398, 298, 330),
             'ALT2': (738, 298, 104), 'CTRL2': (852, 298, 108)})
ACTIVE = ['CTRL', 'WIN', 'C', 'V']
KLAB = {'CTRL': 'Ctrl', 'CTRL2': 'Ctrl', 'WIN': 'WIN', 'ALT': 'Alt', 'ALT2': 'Alt', 'SPACE': ''}


def key_center(k):
    x, y, w = KEYS[k]
    return KBX - KB_W / 2 + x + w / 2, KBY - KB_H / 2 + y + 37


# ------------------------------------------------------------------ props
def monitor_raw():
    im = Image.new('RGBA', (MON_W, MON_RAW_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((MON_W / 2 - 64, BEZ_H - 10, MON_W / 2 + 64, BEZ_H + 112), 10, fill=(60, 62, 72))
    d.rounded_rectangle((MON_W / 2 - 200, BEZ_H + 100, MON_W / 2 + 200, MON_RAW_H - 2), 16, fill=(70, 72, 84))
    d.rounded_rectangle((0, 0, MON_W, BEZ_H), 26, fill=(34, 34, 40))
    d.rounded_rectangle((6, 6, MON_W - 6, BEZ_H - 6), 22, outline=(70, 70, 80), width=3)
    d.ellipse((MON_W / 2 - 5, BEZ_H - 16, MON_W / 2 + 5, BEZ_H - 6), fill=(90, 220, 140))
    return im


def keyboard_raw():
    im = Image.new('RGBA', (KB_W, KB_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, KB_W, KB_H), 34, fill=(214, 218, 228))
    d.rounded_rectangle((8, 8, KB_W - 8, KB_H - 8), 28, outline=(190, 196, 210), width=3)
    for k, (x, y, w) in KEYS.items():
        if k in ACTIVE:
            continue
        draw_key(d, x, y, w, KLAB.get(k, k), False)
    return im


def draw_key(d, x, y, w, lab, pressed, hl=False):
    h = 74
    top = YEL if hl else (250, 250, 252)
    side = (200, 150, 40) if hl else (176, 180, 192)
    if pressed:
        d.rounded_rectangle((x, y + 6, x + w, y + h), 14, fill=side)
        d.rounded_rectangle((x + 4, y + 8, x + w - 4, y + h - 4), 12, fill=top)
        cy = y + 6 + (h - 10) / 2
    else:
        d.rounded_rectangle((x, y, x + w, y + h), 14, fill=side)
        d.rounded_rectangle((x + 4, y + 2, x + w - 4, y + h - 12), 12, fill=top)
        cy = y + (h - 12) / 2
    if lab:
        d.text((x + w / 2, cy), lab, font=th.JB(800, 26 if len(lab) > 1 else 30), fill=NAVY, anchor='mm')


def key_sprite(k, pressed, hl):
    x, y, w = KEYS[k]
    im = Image.new('RGBA', (w + 4, 80), (0, 0, 0, 0))
    draw_key(ImageDraw.Draw(im), 2, 2, w, KLAB.get(k, k), pressed, hl)
    return th.sprite(im, border=0, off=(2, 3) if pressed else (4, 6), blur=2 if pressed else 4, op=.35, tex=True, tex_strength=.5)


def cursor_sprite():
    im = Image.new('RGBA', (60, 84), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(4, 4), (4, 64), (18, 51), (29, 76), (40, 71), (29, 47), (48, 47)]
    d.polygon(pts, fill=(255, 255, 255), outline=(20, 20, 26))
    d.line(pts + [pts[0]], fill=(20, 20, 26), width=4, joint='curve')
    return th.sprite(im, border=5, off=(5, 8), blur=4, op=.4), (4 + 11 + 5, 4 + 11 + 5)


# ------------------------------------------------------------------ screen
DOC = [('A', 'Meeting at 5 PM'), ('B', 'example.com/back-tap')]
ITEM_TXT = {'A': 'Meeting at 5 PM', 'B': 'example.com/back-tap', 'I': None}
LINE_Y = {'A': 132, 'B': 186}
IMG_BOX = (60, 218, 250, 330)
PASTE_Y = 382
PANEL = (470, 70, 834, 474)


def photo(w, h):
    im = Image.new('RGB', (w, h), (130, 190, 235))
    d = ImageDraw.Draw(im)
    d.ellipse((w * .68, h * .14, w * .86, h * .38), fill=(255, 226, 120))
    d.polygon([(0, h), (w * .3, h * .38), (w * .55, h), ], fill=(70, 120, 150))
    d.polygon([(w * .3, h), (w * .65, h * .3), (w, h * .9), (w, h)], fill=(44, 90, 120))
    d.polygon([(w * .58, h * .4), (w * .65, h * .3), (w * .72, h * .4)], fill=(250, 250, 255))
    return im


PHOTO = None


def wallpaper():
    im = Image.new('RGB', (SW, SH))
    d = ImageDraw.Draw(im)
    for y in range(SH):
        t = y / SH
        d.line([(0, y), (SW, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip((120, 170, 230), (40, 70, 150))))
    for i, (cx, cy, r_, c) in enumerate([(700, 420, 260, (90, 140, 230)), (180, 520, 300, (70, 110, 210))]):
        g = Image.new('L', (SW, SH), 0)
        ImageDraw.Draw(g).ellipse((cx - r_, cy - r_, cx + r_, cy + r_), fill=120)
        im.paste(Image.new('RGB', (SW, SH), c), (0, 0), g.filter(ImageFilter.GaussianBlur(60)))
    return im


_wp = None
_scache = {}


def render_screen(s):
    global _wp, PHOTO
    key = repr(sorted((k, v) for k, v in s.items() if k not in ('fall',)))
    if key in _scache and not s.get('fall'):
        return _scache[key].copy()
    if _wp is None:
        _wp = wallpaper(); PHOTO = photo(190, 112)
    im = _wp.copy()
    d = ImageDraw.Draw(im)
    # window
    d.rounded_rectangle((30, 28, 600, 454), 14, fill=(250, 250, 252), outline=(200, 205, 215), width=2)
    d.rounded_rectangle((30, 28, 600, 74), 14, fill=(236, 238, 244))
    d.rectangle((30, 58, 600, 74), fill=(236, 238, 244))
    d.text((52, 51), 'notes.txt', font=th.JB(600, 20), fill=(60, 64, 80), anchor='lm')
    for i, x in enumerate((508, 540, 572)):
        if i == 0:
            d.line([(x - 7, 51), (x + 7, 51)], fill=(80, 80, 90), width=2)
        elif i == 1:
            d.rectangle((x - 7, 44, x + 7, 58), outline=(80, 80, 90), width=2)
        else:
            d.line([(x - 7, 44), (x + 7, 58)], fill=(80, 80, 90), width=2); d.line([(x - 7, 58), (x + 7, 44)], fill=(80, 80, 90), width=2)
    sel = s.get('sel')
    for lid, txt in DOC:
        y = LINE_Y[lid]
        f = th.JB(600, 26)
        if sel == lid:
            d.rectangle((56, y - 18, 64 + f.getlength(txt), y + 18), fill=(160, 205, 255))
        d.text((60, y), txt, font=f, fill=(20, 90, 200) if lid == 'B' else (30, 32, 44), anchor='lm')
        if lid == 'B':
            d.line([(60, y + 16), (60 + f.getlength(txt), y + 16)], fill=(20, 90, 200), width=2)
    im.paste(PHOTO, (IMG_BOX[0], IMG_BOX[1]))
    if sel == 'I':
        d.rectangle((IMG_BOX[0] - 5, IMG_BOX[1] - 5, IMG_BOX[2] + 5, IMG_BOX[3] + 5), outline=(60, 140, 255), width=5)
    if s.get('pasted'):
        f = th.JB(600, 26)
        d.rectangle((56, PASTE_Y - 18, 64 + f.getlength('Meeting at 5 PM'), PASTE_Y + 18), fill=YEL)
        d.text((60, PASTE_Y), 'Meeting at 5 PM', font=f, fill=(30, 32, 44), anchor='lm')
    elif s.get('caret', True):
        d.line([(60, PASTE_Y - 16), (60, PASTE_Y + 16)], fill=(30, 32, 44), width=3)
    # taskbar
    d.rectangle((0, SH - 46, SW, SH), fill=(232, 236, 244))
    for i in range(5):
        x = SW / 2 - 110 + i * 48
        d.rounded_rectangle((x, SH - 37, x + 30, SH - 9), 7, fill=[(0, 103, 192), (255, 185, 0), (90, 90, 100), (16, 160, 110), (220, 70, 70)][i])
    d.text((SW - 20, SH - 23), '9:41', font=th.JB(600, 18), fill=(40, 40, 50), anchor='rm')
    # clipboard stickies (desktop)
    stack = s.get('stack', ())
    for i, it in enumerate(stack):
        sticky(im, 640, 96 + i * 82, it, rot=[-3, 2, -1][i % 3])
    if s.get('fall'):
        it, age = s['fall']
        sticky(im, 640 + age * 14, 96 + age * age * 22, it, rot=-3 + age * 14, gone=True)
    # panel
    if s.get('panel'):
        draw_panel(im, s)
    if not s.get('fall'):
        _scache[key] = im.copy()
    return im


def sticky(im, x, y, it, rot=0, gone=False):
    w, h = 190, 70
    st = Image.new('RGBA', (w, h + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(st)
    d.rectangle((0, 12, w, h + 12), fill=(255, 236, 140))
    d.rectangle((w / 2 - 34, 0, w / 2 + 34, 22), fill=(230, 215, 170))
    d.text((12, 30), 'COPIED', font=th.JB(800, 14), fill=(150, 110, 20), anchor='lm')
    if ITEM_TXT[it]:
        t = ITEM_TXT[it]
        d.text((12, 58), t if len(t) < 15 else t[:13] + '..', font=th.JB(700, 19), fill=(40, 34, 20), anchor='lm')
    else:
        st.paste(PHOTO.resize((70, 40)), (12, 40))
        d.text((92, 60), 'photo', font=th.JB(700, 19), fill=(40, 34, 20), anchor='lm')
    if gone:
        d.text((w - 10, 30), 'GONE', font=th.JB(800, 16), fill=(220, 50, 50), anchor='rm')
    st = st.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', st.size, (0, 0, 0, 0))
    sh.putalpha(st.split()[3].point(lambda v: int(v * .3)).filter(ImageFilter.GaussianBlur(4)))
    base = im.convert('RGBA')
    base.alpha_composite(sh, (int(x + 4), int(y + 6)))
    base.alpha_composite(st, (int(x), int(y)))
    im.paste(base.convert('RGB'))


def draw_panel(im, s):
    x0, y0, x1, y1 = PANEL
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 6, y0 + 10, x1 + 6, y1 + 10), 16, fill=(0, 0, 0, 90))
    base = im.convert('RGBA'); base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); im.paste(base.convert('RGB'))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, y0, x1, y1), 16, fill=(246, 247, 251), outline=(205, 210, 222), width=2)
    # tab row (generic icons)
    for i in range(5):
        cx = x0 + 34 + i * 44
        c = (0, 103, 192) if i == 4 else (150, 155, 170)
        d.rounded_rectangle((cx - 13, y0 + 18, cx + 13, y0 + 44), 6, outline=c, width=3)
    d.line([(x0 + 34 + 4 * 44 - 16, y0 + 52), (x0 + 34 + 4 * 44 + 16, y0 + 52)], fill=(0, 103, 192), width=4)
    d.text((x0 + 20, y0 + 80), 'Clipboard', font=th.JB(800, 24), fill=(30, 32, 44), anchor='lm')
    if s['panel'] == 'off':
        d.text((x0 + 20, y0 + 150), 'Clipboard history', font=th.JB(600, 21), fill=(60, 64, 80), anchor='lm')
        d.text((x0 + 20, y0 + 178), 'is turned off.', font=th.JB(600, 21), fill=(60, 64, 80), anchor='lm')
        hov = s.get('btn_hl')
        d.rounded_rectangle((x0 + 20, y0 + 222, x0 + 180, y0 + 270), 10, fill=(0, 84, 160) if hov else BLUEW)
        d.text((x0 + 100, y0 + 246), 'Turn on', font=th.JB(800, 22), fill=(255, 255, 255), anchor='mm')
        return
    d.text((x1 - 20, y0 + 80), 'Clear all', font=th.JB(600, 18), fill=(0, 103, 192), anchor='rm')
    items = s.get('items', ())
    if not items:
        d.text((x0 + 20, y0 + 150), 'Copy something to', font=th.JB(600, 21), fill=(110, 114, 130), anchor='lm')
        d.text((x0 + 20, y0 + 178), 'see it here.', font=th.JB(600, 21), fill=(110, 114, 130), anchor='lm')
    for i, it in enumerate(items):
        cy0 = y0 + 106 + i * 94
        hl = s.get('card_hl') == it
        d.rounded_rectangle((x0 + 14, cy0, x1 - 14, cy0 + 84), 10, fill=(255, 255, 255), outline=(0, 103, 192) if hl else (220, 224, 234), width=3 if hl else 2)
        if ITEM_TXT[it]:
            d.text((x0 + 30, cy0 + 42), ITEM_TXT[it], font=th.JB(600, 21), fill=(30, 32, 44), anchor='lm')
        else:
            im.paste(PHOTO.resize((100, 59)), (x0 + 30, cy0 + 12))
        # "..." button
        mx = x1 - 40
        for k in range(3):
            d.ellipse((mx - 12 + k * 10, cy0 + 18, mx - 7 + k * 10, cy0 + 23), fill=(90, 94, 110))
        if it in s.get('pinned', ()):
            pin_icon(d, x1 - 44, cy0 + 56, (0, 103, 192), True)
        if s.get('more') == it:
            d.rounded_rectangle((x1 - 120, cy0 + 34, x1 - 22, cy0 + 78), 8, fill=(236, 240, 250), outline=(200, 206, 220))
            pin_icon(d, x1 - 96, cy0 + 56, (0, 103, 192) if s.get('pin_hl') else (60, 64, 80), it in s.get('pinned', ()))
            # trash
            d.rectangle((x1 - 56, cy0 + 48, x1 - 40, cy0 + 68), outline=(60, 64, 80), width=2)
            d.line([(x1 - 60, cy0 + 47), (x1 - 36, cy0 + 47)], fill=(60, 64, 80), width=2)


def pin_icon(d, cx, cy, col, filled):
    pts = [(cx - 8, cy - 12), (cx + 8, cy - 12), (cx + 6, cy - 2), (cx + 11, cy + 3), (cx - 11, cy + 3), (cx - 6, cy - 2)]
    if filled:
        d.polygon(pts, fill=col)
    else:
        d.polygon(pts, outline=col, width=2)
    d.line([(cx, cy + 3), (cx, cy + 14)], fill=col, width=3)


def card_point(i, more=False):
    x0, y0, x1, y1 = PANEL
    cy0 = y0 + 106 + i * 94
    if more:
        return x1 - 30, cy0 + 21
    return x0 + 120, cy0 + 42


# ================================================================== timeline
class TL:
    def __init__(s):
        s.frames = []
        s.cur = dict(mon_dy=-1500, kb_dy=900, scr=dict(caret=True), cursor=None, hand=None, keys=[], combo=None)
        s.caps, s.fx, s.snd = [], [], []

    @property
    def f(s):
        return len(s.frames)

    def snap(s):
        s.frames.append(copy.deepcopy(s.cur))

    def hold(s, n):
        for _ in range(n):
            s.snap()

    def sound(s, k, df=0):
        s.snd.append((s.f + df, k))

    def cap(s, head, text, badge='n'):
        if s.caps and s.caps[-1]['out'] is None:
            s.caps[-1]['out'] = s.f
        s.caps.append(dict(head=head, text=text, inn=s.f + 1, out=None, rot=rng_for(text).uniform(-1.3, 1.3)))
        s.sound('paper', 1)

    def cap_off(s):
        if s.caps and s.caps[-1]['out'] is None:
            s.caps[-1]['out'] = s.f; s.sound('paper')

    def tween(s, key, to, n):
        v0 = s.cur[key]
        for i in range(1, n + 1):
            s.cur[key] = v0 + (to - v0) * ease(i / n); s.snap()

    def cursor_to(s, x, y, n=5):
        if s.cur['cursor'] is None:
            s.cur['cursor'] = dict(x=SW + 60, y=SH - 60, p=False)
        c = s.cur['cursor']; x0, y0 = c['x'], c['y']
        for i in range(1, n + 1):
            t = ease(i / n); c['x'] = x0 + (x - x0) * t; c['y'] = y0 + (y - y0) * t; s.snap()

    def click(s, after=None):
        c = s.cur['cursor']; c['p'] = True
        ox, oy = scr_origin(s.cur['mon_dy'])
        s.fx.append(('ring', s.f, ox + c['x'], oy + c['y'])); s.sound('tap')
        s.hold(2); c['p'] = False
        if after:
            after()
        s.hold(1)

    def hand_to(s, x, y, n=5):
        if s.cur['hand'] is None:
            s.cur['hand'] = dict(x=HIDE[0], y=HIDE[1], p=False)
        h = s.cur['hand']; x0, y0 = h['x'], h['y']
        for i in range(1, n + 1):
            t = ease(i / n); h['x'] = x0 + (x - x0) * t; h['y'] = y0 + (y - y0) * t; s.snap()

    def hand_out(s, n=4):
        s.hand_to(*HIDE, n); s.cur['hand'] = None

    def combo(s, hold_key, key, label_txt, after=None, n=6):
        s.cur['keys'] = [hold_key]; s.cur['combo'] = dict(t=label_txt, f=s.f); s.sound('tap')
        s.hold(2)
        s.hand_to(*key_center(key), n)
        s.hold(1)
        s.cur['hand']['p'] = True; s.cur['keys'] = [hold_key, key]; s.sound('tap')
        s.fx.append(('ring', s.f, *key_center(key)))
        s.hold(2)
        if after:
            after()
        s.hold(3)
        s.cur['hand']['p'] = False; s.cur['keys'] = []
        s.hand_to(key_center(key)[0] + 60, key_center(key)[1] + 120, 3)

    def scr(s, **kw):
        s.cur['scr'].update(kw)


def build():
    t = TL()
    t.fx.append(('title', 0, 52)); t.hold(58)
    # props in
    t.sound('whoosh')
    for i in range(1, 8):
        e = ease(i / 7)
        t.cur['mon_dy'] = -1500 * (1 - e) + (24 if i == 6 else 0)
        t.cur['kb_dy'] = 900 * (1 - ease(max(0, i - 1) / 6)) + (-20 if i == 7 else 0)
        t.snap()
    t.cur['kb_dy'] = 0; t.cur['mon_dy'] = 0; t.hold(3)
    # ---- problem
    t.cap('FIG. 01  /  THE PROBLEM', 'Copy something new... the old copy is gone')
    t.hold(12)
    ax, ay = 140, LINE_Y['A']
    t.cursor_to(ax, ay, 6); t.click(lambda: t.scr(sel='A'))
    t.combo('CTRL', 'C', 'CTRL + C', after=lambda: (t.scr(stack=('A',)), t.sound('pop')))
    t.hold(6)
    t.cursor_to(160, LINE_Y['B'], 5); t.click(lambda: t.scr(sel='B'))
    t.combo('CTRL', 'C', 'CTRL + C', after=lambda: (t.scr(stack=('B',)), t.sound('whoosh')))
    # fall of A
    for age in range(0, 8):
        t.scr(fall=('A', age)); t.snap()
    t.scr(fall=None); t.hand_out(3)
    t.hold(8)
    # ---- step 1
    t.cap('FIG. 02  /  STEP 1 OF 3', 'Press WIN + V, then click Turn on')
    t.scr(sel=None, stack=())
    t.hold(12)
    t.combo('WIN', 'V', 'WIN + V', after=lambda: (t.scr(panel='off'), t.sound('pop')))
    t.hand_out(3)
    t.cursor_to(PANEL[0] + 100, PANEL[1] + 246, 6)
    t.scr(btn_hl=True); t.hold(2)
    t.click(lambda: (t.scr(panel='list', items=(), btn_hl=False), t.sound('ding')))
    t.hold(12)
    t.scr(panel=None); t.hold(4)
    # ---- step 2
    t.cap('FIG. 03  /  STEP 2 OF 3', 'Copy a few things, as usual')
    t.hold(12)
    for it, (px, py) in [('A', (140, LINE_Y['A'])), ('B', (160, LINE_Y['B'])), ('I', (150, 270))]:
        t.cursor_to(px, py, 4); t.click(lambda it=it: t.scr(sel=it))
        stack = tuple(list(t.cur['scr'].get('stack', ())) + [it])
        t.combo('CTRL', 'C', 'CTRL + C', after=lambda st=stack: (t.scr(stack=st), t.sound('pop')), n=4)
    t.hand_out(3)
    t.scr(sel=None)
    t.cap('FIG. 03  /  RESULT', 'All 3 copies are saved, nothing lost!', )
    t.hold(30)
    # ---- step 3
    t.cap('FIG. 04  /  STEP 3 OF 3', 'Press WIN + V and pick any copy to paste')
    t.scr(stack=())
    t.hold(12)
    t.cursor_to(70, PASTE_Y, 4); t.click()
    t.combo('WIN', 'V', 'WIN + V', after=lambda: (t.scr(panel='list', items=('I', 'B', 'A')), t.sound('pop')))
    t.hand_out(3)
    t.cursor_to(*card_point(2), 6)
    t.scr(card_hl='A'); t.hold(3)
    t.click(lambda: (t.scr(panel=None, card_hl=None, pasted=True, caret=False), t.sound('ding')))
    t.cap('RESULT  /  OK', 'Pasted, even an older copy!')
    t.hold(30)
    # ---- bonus pin
    t.cap('APPENDIX  /  BONUS', 'Pin a copy to keep it after a restart')
    t.hold(10)
    t.combo('WIN', 'V', 'WIN + V', after=lambda: (t.scr(panel='list', items=('I', 'B', 'A')), t.sound('pop')), n=5)
    t.hand_out(3)
    t.cursor_to(*card_point(2, more=True), 6); t.click(lambda: t.scr(more='A'))
    x1 = PANEL[2]; cy0 = PANEL[1] + 106 + 2 * 94
    t.cursor_to(x1 - 96, cy0 + 56, 4); t.scr(pin_hl=True); t.hold(2)
    t.click(lambda: (t.scr(pinned=('A',), more=None, pin_hl=False), t.sound('ding')))
    t.hold(26)
    # ---- end
    t.cap_off()
    t.cur['cursor'] = None
    t.sound('whoosh')
    for i in range(1, 6):
        e = ease(i / 5); t.cur['mon_dy'] = -1600 * e; t.cur['kb_dy'] = 1000 * e; t.snap()
    t.fx.append(('end', t.f)); t.hold(72)
    return t


# ================================================================== render
P = {}
TLD = None


def init_props():
    P['bg'] = th.bg_blue(with_dims=False)
    P['mon'] = th.sprite(monitor_raw(), border=8, off=(16, 22), blur=14, op=.42)
    P['kb'] = th.sprite(keyboard_raw(), border=8, off=(12, 18), blur=12, op=.42)
    P['keys'] = {(k, p): key_sprite(k, p, p) for k in ACTIVE for p in (False, True)}
    P['hand'] = {'hover': th.hand_sprite('blue', press=False), 'press': th.hand_sprite('blue', press=True)}
    P['cursor'], P['ctip'] = cursor_sprite()
    P['rings'] = [dashed_ring(r, YEL, w) for r, w in [(30, 8), (50, 7), (70, 5)]]
    P['hold'] = label('HOLD', th.JB(800, 26), bg=YEL, rot=-6, padx=14, pady=6)
    P['notes'] = {}
    P['combo'] = {}
    # title
    P['tiles'] = [rotate_sprite(th.stencil_letter(ch, PAPER if ch in 'WIN' else YEL), rng_for('wt', i).uniform(-4, 4)) for i, ch in enumerate('WIN+V')]
    P['t_label'] = label('SPEC // PC tip', th.JB(700, 34), fg=MID, rot=-2, padx=30, pady=16)
    P['t_s1'] = center_label('YOUR PC CAN REMEMBER', th.JB(800, 46), rot=1.5)
    P['t_s1b'] = center_label('EVERYTHING YOU COPY', th.JB(800, 46), rot=-1)
    P['t_s2'] = center_label('clipboard history', th.JB(700, 40), bg=YEL, rot=-2)
    P['t_kw'] = key_sprite('WIN', False, True); P['t_kv'] = key_sprite('V', False, True)
    P['t_plus'] = center_label('+', th.JB(800, 60), bg=PAPER, padx=24, pady=6)
    P['t_burst'] = label(['WINDOWS', '10 & 11'], th.JB(800, 36), rot=6, padx=26, pady=16)
    # end
    P['e_head'] = center_label('SAVE THIS TIP', th.JB(800, 92), rot=-2.5, padx=56, pady=30)
    P['e_chips'] = [rotate_sprite(path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('WIN + V', (0, 103, 192), 'grid', -2), ('Turn on', (16, 160, 110), 'touch', 1.5), ('Copy as usual', (90, 90, 100), 'dot', -1.5),
        ('WIN + V & paste', NAVY, 'grid', 2)])]
    P['e_arrows'] = [chalk_arrow(r) for r in (14, -14, 14)]
    P['e_s1'] = center_label('PIN = KEEPS AFTER RESTART', th.JB(800, 44), bg=YEL, rot=-1.5)
    P['e_s2'] = center_label('SAVES UP TO 25 COPIES', th.JB(800, 44), rot=1.5)
    P['e_s3'] = center_label('works on Windows 10 & 11', th.JB(600, 34), fg=MID, rot=-1, pady=18)


def put(cv, sp, x, y, f, key, amp=1.6):
    jx, jy = jit(f, key, amp)
    draw_sprite(cv, sp, x + jx, y + jy)


def draw_title(cv, f, a, ex):
    els = [('t_label', 540, 400, a + 1, 0)]
    xs = [210, 375, 540, 705, 870]
    for i in range(5):
        els.append((('tile', i), xs[i], 640, a + 4 + 2 * i, i % 3))
    els += [('t_s1', 540, 880, a + 16, 0), ('t_s1b', 540, 990, a + 19, 1), ('t_s2', 520, 1120, a + 23, 2),
            ('t_kw', 420, 1430, a + 27, 0), ('t_plus', 540, 1430, a + 28, 1), ('t_kv', 650, 1430, a + 29, 2),
            ('t_burst', 820, 1640, a + 32, 0)]
    for key, x, y, ap, stg in els:
        yy = m.drop_y(f, ap, y, ex, stg)
        if yy is None:
            continue
        sp = P['tiles'][key[1]] if isinstance(key, tuple) else P[key]
        if key in ('t_kw', 't_kv'):
            sp = tuple(s_.resize((int(s_.width * 2), int(s_.height * 2)), Image.BICUBIC) for s_ in sp)
        put(cv, sp, x, yy, f, key)


def draw_end(cv, f, a):
    els = [('e_head', 540, 300, a + 2)]
    xs = [470, 600, 470, 600]
    for i in range(4):
        els.append((('chip', i), xs[i], 560 + 185 * i, a + 6 + 4 * i))
        if i < 3:
            els.append((('arrow', i), (190, 950, 190)[i], 652 + 185 * i, a + 9 + 4 * i))
    els += [('e_s1', 540, 1340, a + 24), ('e_s2', 540, 1470, a + 28), ('e_s3', 540, 1640, a + 32)]
    for key, x, y, ap in els:
        yy = m.drop_y(f, ap, y)
        if yy is None:
            continue
        if isinstance(key, tuple):
            sp = P['e_chips'][key[1]] if key[0] == 'chip' else P['e_arrows'][key[1]]
        else:
            sp = P[key]
        put(cv, sp, x, yy, f, key)


def draw_caps(cv, f, caps):
    for c in caps:
        k = f - c['inn']
        if k < 0:
            continue
        y = {0: -260, 1: 380, 2: 268, 3: 312}.get(k, 300)
        if c['out'] is not None and f >= c['out']:
            e = f - c['out']
            if e > 2:
                continue
            y = (230, -10, -400)[e]
        key = (c['head'], c['text'])
        if key not in P['notes']:
            P['notes'][key] = rotate_sprite(th.cap_blue(c['head'], c['text']), c['rot'])
        put(cv, P['notes'][key], 540, y, f, ('cap', c['text']), amp=1.8)


_stex = None


def render(f):
    global _stex
    tl = TLD
    st = tl['frames'][f]
    cv = P['bg'].copy()
    for e in tl['fx']:
        if e[0] == 'title' and f < e[2] + 8:
            draw_title(cv, f, e[1], e[2])
        if e[0] == 'end' and f >= e[1]:
            draw_end(cv, f, e[1])
    # keyboard
    if st['kb_dy'] < 850:
        kx, ky = KBX, KBY + st['kb_dy']
        jx, jy = jit(f, 'kb', 1.2)
        draw_sprite(cv, P['kb'], kx + jx, ky + jy)
        for k in ACTIVE:
            pressed = k in st['keys']
            sp = P['keys'][(k, pressed)]
            cx, cy = key_center(k)
            draw_sprite(cv, sp, cx + jx, cy + st['kb_dy'] + jy + (3 if pressed else 0))
            if pressed and k in ('CTRL', 'WIN') and len(st['keys']) >= 1:
                draw_sprite(cv, P['hold'], cx + jx, cy + st['kb_dy'] - 66 + jy)
        if st['combo'] and f - st['combo']['f'] < 40:
            t_ = st['combo']['t']
            if t_ not in P['combo']:
                P['combo'][t_] = label(t_, th.JB(800, 48), bg=YEL, tape=True, rot=-3, padx=28, pady=12)
            age = f - st['combo']['f']
            yy = {0: 1180, 1: 1340, 2: 1312}.get(age, 1320)
            put(cv, P['combo'][t_], 905, yy - 30 + st['kb_dy'], f, 'combo')
    # monitor
    if st['mon_dy'] > -1450:
        mx, my = MONX, MONY + st['mon_dy']
        jx, jy = jit(f, 'mon', 1.2)
        sh, body = P['mon']
        body = body.copy()
        scr = render_screen(st['scr'])
        if _stex is None:
            _stex = paper_tex(SW, SH, seed=77, strength=.7)
        scr = apply_tex(scr, _stex)
        ox = (body.width - MON_W) // 2 + 24; oy = (body.height - MON_RAW_H) // 2 + 24
        mask = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, SW - 1, SH - 1), 10, fill=255)
        body.paste(scr, (ox, oy), mask)
        draw_sprite(cv, (sh, body), mx + jx, my + jy)
        # cursor
        c = st['cursor']
        if c:
            sx0, sy0 = scr_origin(st['mon_dy'])
            csh, cbody = P['cursor']
            tx, ty = P['ctip']
            pad_ = (cbody.width - 60) // 2
            x = sx0 + c['x'] + jx - (pad_ + 4) + (2 if c['p'] else 0)
            y = sy0 + c['y'] + jy - ((cbody.height - 84) // 2 + 4) + (2 if c['p'] else 0)
            blit(cv, csh, x, y); blit(cv, cbody, x, y)
    # fx rings
    for e in tl['fx']:
        if e[0] == 'ring':
            k = f - e[1]
            if 0 <= k < 3:
                put(cv, P['rings'][k], e[2], e[3], f, 'ring', .5)
    # hand
    hd = st['hand']
    if hd:
        sh_, body_, tip = P['hand']['press' if hd['p'] else 'hover']
        jx, jy = jit(f, 'hand', 1.4)
        blit(cv, sh_, hd['x'] - tip[0] + jx, hd['y'] - tip[1] + jy); blit(cv, body_, hd['x'] - tip[0] + jx, hd['y'] - tip[1] + jy)
    draw_caps(cv, f, tl['caps'])
    k = 1 + rng_for(f, 'flicker').uniform(-0.016, 0.016)
    out = cv.convert('RGB').point(lambda v: min(255, int(v * k)))
    out.save(f'{OUT}/{f:05d}.png', compress_level=1)
    return f


def add_title_end_sounds(t):
    for e in t.fx:
        if e[0] == 'title':
            a = e[1]
            for ap in [a + 1] + [a + 4 + 2 * i for i in range(5)] + [a + 16, a + 19, a + 23, a + 27, a + 28, a + 29, a + 32]:
                t.snd.append((ap, 'pop'))
            t.snd.append((e[2] + 1, 'whoosh'))
        if e[0] == 'end':
            a = e[1]
            for ap in [a + 2] + [a + 6 + 4 * i for i in range(4)] + [a + 24, a + 28, a + 32]:
                t.snd.append((ap, 'pop'))


if __name__ == '__main__':
    t = build()
    add_title_end_sounds(t)
    TLD = dict(frames=t.frames, fx=t.fx, caps=t.caps, snd=t.snd)
    n = len(t.frames)
    print('frames', n, 'seconds', n / FPS, flush=True)
    for c in t.caps:
        print(c['inn'], c['out'], c['text'])
    os.makedirs(OUT, exist_ok=True)
    init_props()
    only = [int(a) for a in sys.argv[1:]]
    if only:
        for f in only:
            render(f)
    else:
        with Pool(2) as pool:
            for i, _ in enumerate(pool.imap(render, range(n), chunksize=8)):
                if i % 100 == 0:
                    print('rendered', i, flush=True)
        m.make_audio(TLD, n, __import__('lib').out('audio_winv.wav'))

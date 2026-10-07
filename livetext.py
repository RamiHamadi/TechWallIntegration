"""Tech Wall — iPhone Live Text: copy text from the camera or any photo. Short-form structure (~16 s, loops):
Hook (frame 0: a Wi-Fi card's password already selected in the camera, Copy -> COPIED!) -> 3 quick tips
(Camera: Detect Text / Photos: Live Text button / tap a number to call) -> specific CTA on the opening screen,
so the replay flows back into the hook. No end card. Screens are generic look-alikes, fictional data only.
Verified 2026-10-07: support.apple.com (Use Live Text with your iPhone camera; Copy and translate text from photos).
Build:  ./build.sh livetext
"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import screens as S
from screens import F, SW, SH, TXT, GRAY, BLUE
import movie as m
import movie_blue as mb
import themes as th

EP = 'livetext'
OUT = __import__('lib').out(f'frames_{EP}')
mb.OUT = OUT
YEL = mb.YEL
SEL = (178, 210, 255)
WHITE = (255, 255, 255)


# ======================================================================= screens
def viewfinder(d):
    for y in range(110, 900):
        t = (y - 110) / 790
        d.line([(0, y), (SW, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip((112, 96, 80), (70, 58, 48))))


def cam_chrome(d, rows, ov, hl):
    d.rectangle((0, 0, SW, 110), fill=(0, 0, 0))
    d.rectangle((0, 900, SW, SH), fill=(0, 0, 0))
    for i, lab in enumerate(['VIDEO', 'PHOTO', 'PORTRAIT']):
        d.text((150 + i * 130, 940), lab, font=F(600, 22), fill=YEL if lab == 'PHOTO' else (220, 220, 225), anchor='mm')
    d.ellipse((SW / 2 - 52, 990, SW / 2 + 52, 1094), outline=WHITE, width=6)
    d.ellipse((SW / 2 - 40, 1002, SW / 2 + 40, 1082), fill=WHITE)
    # Detect Text button (bottom-right of the viewfinder)
    on = ov.get('dt')
    x0, y0 = SW - 104, 800
    d.rounded_rectangle((x0, y0, x0 + 72, y0 + 72), 18, fill=YEL if on else (40, 40, 44), outline=YEL if hl == 'dt' else None, width=3)
    col = (20, 20, 24) if on else WHITE
    for k, w in enumerate((40, 30, 36)):
        d.line([(x0 + 16, y0 + 22 + k * 14), (x0 + 16 + w, y0 + 22 + k * 14)], fill=col, width=5)
    d.rounded_rectangle((x0 + 6, y0 + 6, x0 + 66, y0 + 66), 12, outline=col, width=2)
    rows['dt'] = (x0, y0, x0 + 72, y0 + 72)


def copy_menu(d, rows, x, y, hl, items=('Copy', 'Select All', 'Look Up')):
    f = F(500, 25)
    w = sum(f.getlength(t) + 36 for t in items)
    x0 = max(14, min(x - w / 2, SW - 14 - w))
    d.rounded_rectangle((x0, y - 32, x0 + w, y + 30), 14, fill=(46, 46, 50))
    d.polygon([(x - 12, y - 31), (x + 12, y - 31), (x, y - 46)], fill=(46, 46, 50))   # arrow up to the selection
    cx = x0
    for i, t in enumerate(items):
        tw = f.getlength(t) + 36
        if hl == 'copy' and i == 0:
            d.rounded_rectangle((cx + 2, y - 30, cx + tw - 2, y + 28), 12, fill=(90, 90, 96))
        d.text((cx + tw / 2, y), t, font=f, fill=WHITE, anchor='mm')
        if i == 0:
            rows['copy'] = (cx, y - 32, cx + tw, y + 30)
        if i < len(items) - 1:
            d.line([(cx + tw, y - 22), (cx + tw, y + 22)], fill=(110, 110, 116), width=2)
        cx += tw


def cam_content(ov, hl):
    im = Image.new('RGB', (SW, SH)); d = ImageDraw.Draw(im); rows = {}
    viewfinder(d)
    # paper Wi-Fi card
    d.rectangle((84, 330, 490, 650), fill=(30, 24, 20))
    d.rectangle((70, 312, 476, 632), fill=(250, 248, 240))
    d.text((100, 362), 'Guest Wi-Fi', font=F(600, 38), fill=TXT, anchor='lm')
    d.line([(100, 398), (446, 398)], fill=(210, 205, 190), width=2)
    lines = [('net', 'Network: Home', 450), ('pw', 'Password:', 520), ('pw2', 'SunnyDays2024', 570)]
    if ov.get('dt'):
        for rid, t, y in lines:
            d.rounded_rectangle((96, y - 26, 104 + F(600, 31).getlength(t), y + 24), 6, fill=(232, 238, 252))
    if ov.get('sel'):
        w = F(600, 31).getlength('SunnyDays2024')
        d.rectangle((96, 546, 104 + w, 596), fill=SEL)
        for xx in (96, 104 + w):
            d.line([(xx, 544), (xx, 598)], fill=BLUE, width=4)
        d.ellipse((90, 536, 102, 548), fill=BLUE); d.ellipse((98 + w, 592, 110 + w, 604), fill=BLUE)
    for rid, t, y in lines:
        d.text((100, y), t, font=F(600 if rid == 'pw2' else 500, 31), fill=TXT, anchor='lm')
        rows[rid] = (100, y - 26, 100 + F(600, 31).getlength(t), y + 24)
    if ov.get('frame'):
        for (cx, cy, sx, sy) in [(56, 298, 1, 1), (490, 298, -1, 1), (56, 646, 1, -1), (490, 646, -1, -1)]:
            d.line([(cx, cy), (cx + 40 * sx, cy)], fill=YEL, width=6); d.line([(cx, cy), (cx, cy + 40 * sy)], fill=YEL, width=6)
    if ov.get('sel') and not ov.get('copied'):
        copy_menu(d, rows, 200, 664, hl)
    if ov.get('copied'):
        d.rounded_rectangle((SW / 2 - 90, 690, SW / 2 + 90, 744), 27, fill=(46, 46, 50))
        d.text((SW / 2, 717), 'Copied', font=F(600, 25), fill=WHITE, anchor='mm')
    cam_chrome(d, rows, ov, hl)
    return im, rows


def photo_content(ov, hl):
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im); rows = {}
    d.text((30, 140), '< Photos', font=F(500, 28), fill=BLUE, anchor='lm')
    d.rectangle((0, 190, SW, 900), fill=(214, 206, 190))
    d.rectangle((60, 250, 500, 840), fill=(252, 250, 244))
    items = [('Banana Bread', F(600, 38)), ('3 ripe bananas', F(500, 28)), ('2 cups flour', F(500, 28)),
             ('1 tsp baking soda', F(500, 28)), ('Bake 60 min at 175 °C', F(500, 28))]
    for i, (t, f) in enumerate(items):
        y = 310 + i * 90
        if ov.get('lt'):
            d.rounded_rectangle((84, y - 30, 96 + f.getlength(t), y + 30), 6, fill=SEL if ov.get('all') else (232, 238, 252))
        d.text((90, y), t, font=f, fill=TXT, anchor='lm')
    # Live Text button, lower-right of the photo
    x0, y0 = SW - 100, 820
    on = ov.get('lt')
    d.rounded_rectangle((x0, y0, x0 + 68, y0 + 68), 16, fill=BLUE if on else (240, 240, 245), outline=YEL if hl == 'lt' else None, width=3)
    col = WHITE if on else (30, 30, 34)
    for k, w in enumerate((36, 26, 32)):
        d.line([(x0 + 16, y0 + 20 + k * 14), (x0 + 16 + w, y0 + 20 + k * 14)], fill=col, width=5)
    rows['lt'] = (x0, y0, x0 + 68, y0 + 68)
    if on:
        hlc = (90, 90, 96) if hl == 'copyall' else (46, 46, 50)
        d.rounded_rectangle((40, 826, 220, 882), 28, fill=hlc)
        d.text((130, 854), 'Copy All', font=F(600, 25), fill=WHITE, anchor='mm')
        rows['copyall'] = (40, 826, 220, 882)
    if ov.get('copied'):
        d.rounded_rectangle((SW / 2 - 90, 940, SW / 2 + 90, 994), 27, fill=(60, 60, 66))
        d.text((SW / 2, 967), 'Copied', font=F(600, 25), fill=WHITE, anchor='mm')
    return im, rows


def flyer_content(ov, hl):
    im = Image.new('RGB', (SW, SH), (0, 0, 0)); d = ImageDraw.Draw(im); rows = {}
    d.text((30, 140), '< Photos', font=F(500, 28), fill=BLUE, anchor='lm')
    d.rectangle((0, 190, SW, 900), fill=(120, 150, 170))
    d.rectangle((70, 240, 490, 860), fill=(255, 214, 90))
    d.text((SW / 2, 330), 'GUITAR', font=F(600, 62), fill=TXT, anchor='mm')
    d.text((SW / 2, 400), 'LESSONS', font=F(600, 62), fill=TXT, anchor='mm')
    d.text((SW / 2, 500), 'Beginners welcome', font=F(500, 30), fill=TXT, anchor='mm')
    num = '555-0100'; f = F(600, 46)
    w = f.getlength(num)
    d.text((SW / 2, 620), num, font=f, fill=BLUE if ov.get('lt') else TXT, anchor='mm')
    if ov.get('lt'):
        d.line([(SW / 2 - w / 2, 648), (SW / 2 + w / 2, 648)], fill=BLUE, width=4)
    rows['num'] = (SW / 2 - w / 2, 590, SW / 2 + w / 2, 650)
    if ov.get('sheet'):
        d.rounded_rectangle((20, 860, SW - 20, SH - 30), 26, fill=(248, 248, 250))
        for i, (t, c) in enumerate([('Call 555-0100', BLUE), ('Send Message', BLUE), ('Add to Contacts', BLUE)]):
            y = 920 + i * 80
            if hl == 'call' and i == 0:
                d.rounded_rectangle((30, y - 36, SW - 30, y + 36), 16, fill=(226, 230, 240))
            d.text((SW / 2, y), t, font=F(600 if i == 0 else 500, 30), fill=c, anchor='mm')
            if i < 2:
                d.line([(40, y + 40), (SW - 40, y + 40)], fill=(220, 220, 226), width=2)
        rows['call'] = (30, 884, SW - 30, 956)
    return im, rows


BUILD = {'cam': cam_content, 'photo': photo_content, 'flyer': flyer_content}
_orig = S.screen_content
_cache = {}


def screen_content(name, ov=None, hl=None):
    ov = ov or {}
    if name not in BUILD:
        return _orig(name, ov, hl)
    key = (name, tuple(sorted(ov.items())), hl)
    if key not in _cache:
        if len(_cache) > 30:
            _cache.clear()
        _cache[key] = BUILD[name](ov, hl)
    return _cache[key]


S.screen_content = screen_content
_view = S.view


def view(spec):
    if spec['name'] not in BUILD:
        return _view(spec)
    v = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))[0].copy()
    S.status_bar(v, dark_text=False)
    return v


m.view = view


def row_point(spec, rid, fx=0.5):
    _, rows = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    return x0 + (x1 - x0) * fx, (y0 + y1) / 2


m.row_point = row_point


# ======================================================================= timeline
def fig_head(badge):
    if badge.isdigit():
        return f'TIP {badge} OF 3'
    return {'H': 'TECH WALL  /  iPHONE TIP', 'cta': 'SAVE THIS  /  FOR LATER'}[badge]


mb.fig_head = fig_head
spec = m.spec
HOOK = {'frame': True, 'dt': True, 'sel': True}


def build():
    t = m.TL()
    # HOOK — frame 0: the password is already selected in the camera; Copy -> COPIED!
    mb.result_first(t, spec('cam', ov=dict(HOOK)), 'H', 'YOUR iPHONE CAMERA CAN COPY TEXT')
    t.hold(6)
    t.tap('copy', ov={'copied': True}, n_move=4)
    t.fx.append(('burst', t.f, 800, 760, 0)); t.sound('pop')
    t.hand_out(3); t.hold(10)
    # TIP 1 — Camera: Detect Text
    t.cap('1', 'Camera: tap Detect Text', m.MINT)
    t.ph['spec'] = spec('cam', ov={'frame': True}); t.sound('swish'); t.hold(5)
    t.tap('dt', ov={'frame': True, 'dt': True}, n_move=4, fx=0.5)
    t.hold(3)
    t.tap('pw2', ov={'frame': True, 'dt': True, 'sel': True}, n_move=3, fx=0.3)
    t.hand_out(3); t.hold(11)
    # TIP 2 — Photos: Live Text button, Copy All
    t.cap('2', 'Photos: tap Live Text', m.SKY)
    t.navigate(spec('photo'))
    t.hold(4)
    t.tap('lt', ov={'lt': True}, n_move=4, fx=0.5)
    t.hold(2)
    t.tap('copyall', ov={'lt': True, 'all': True, 'copied': True}, n_move=4, fx=0.5)
    t.hand_out(3); t.hold(11)
    # TIP 3 — tap a number to call it
    t.cap('3', 'Tap a number to call it', m.PEACH)
    t.navigate(spec('flyer', ov={'lt': True}))
    t.hold(4)
    t.tap('num', ov={'lt': True, 'sheet': True}, n_move=4, fx=0.5)
    t.hand_out(3); t.hold(12)
    # CTA — back on the opening screen so the replay flows into the hook
    t.cap('cta', 'Save this. What would you copy first?', m.YELLOW)
    t.navigate(spec('cam', ov=dict(HOOK)), back=True)
    t.hold(42)
    return t


def init_props():
    mb.init_props()
    m.P['bursts'] = [mb.label('COPIED!', th.JB(800, 64), bg=YEL, tape=True, rot=-7, padx=30, pady=12)]


if __name__ == '__main__':
    t = build()
    for e in t.fx:
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))
    mb.finish(t, EP, init_props)

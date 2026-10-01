import math
from PIL import Image, ImageDraw, ImageFilter
from lib import *

SW, SH = 560, 1184
BG_UI = (242, 242, 247); CARD = (255, 255, 255); SEP = (224, 224, 230)
TXT = (28, 28, 30); GRAY = (142, 142, 147); BLUE = (10, 122, 255); GREEN = (52, 199, 89)
HL = (206, 206, 212)
ROW = 86
CX0, CX1 = 24, 536

ORANGE = (255, 149, 0); GRAYI = (142, 142, 147); INDIGO = (88, 86, 214); RED = (255, 69, 58)

SCREENS = {
    'settings': [
        ('title', 'Settings'), ('search',),
        ('card', [('airplane', 'Airplane Mode', ORANGE, None, 'toggle_off', 'plane'),
                  ('wifi', 'Wi-Fi', BLUE, 'Home', 'chev', 'wifi'),
                  ('bt', 'Bluetooth', BLUE, 'On', 'chev', 'dot'),
                  ('cell', 'Cellular', GREEN, None, 'chev', 'bars'),
                  ('battery', 'Battery', GREEN, None, 'chev', 'batt')]),
        ('card', [('general', 'General', GRAYI, None, 'chev', 'gear'),
                  ('accessibility', 'Accessibility', BLUE, None, 'chev', 'person'),
                  ('camera', 'Camera', GRAYI, None, 'chev', 'cam'),
                  ('cc', 'Control Center', GRAYI, None, 'chev', 'grid'),
                  ('display', 'Display & Brightness', BLUE, None, 'chev', 'sun'),
                  ('homescreen', 'Home Screen', INDIGO, None, 'chev', 'grid'),
                  ('siri', 'Siri', (40, 40, 45), None, 'chev', 'dot')]),
    ],
    'accessibility': [
        ('back', 'Settings'), ('title', 'Accessibility'),
        ('header', 'VISION'),
        ('card', [('voiceover', 'VoiceOver', (40, 40, 45), 'Off', 'chev', 'person'),
                  ('zoom', 'Zoom', (40, 40, 45), 'Off', 'chev', 'zoom'),
                  ('text', 'Display & Text Size', BLUE, None, 'chev', 'sun'),
                  ('motion', 'Motion', GREEN, None, 'chev', 'dot'),
                  ('spoken', 'Spoken Content', (40, 40, 45), None, 'chev', 'dot')]),
        ('header', 'PHYSICAL AND MOTOR'),
        ('card', [('touch', 'Touch', BLUE, None, 'chev', 'touch'),
                  ('faceid', 'Face ID & Attention', GREEN, None, 'chev', 'dot'),
                  ('switch', 'Switch Control', (40, 40, 45), 'Off', 'chev', 'grid'),
                  ('voicectl', 'Voice Control', BLUE, 'Off', 'chev', 'dot'),
                  ('side', 'Side Button', BLUE, None, 'chev', 'dot')]),
    ],
    'touch': [
        ('back', 'Accessibility'), ('title', 'Touch'),
        ('card', [('assistive', 'AssistiveTouch', None, 'Off', 'chev', None)]),
        ('footer', 'AssistiveTouch allows you to use your iPhone if you have difficulty touching the screen or if you require an adaptive accessory.'),
        ('card', [('reach', 'Reachability', None, None, 'toggle_off', None)]),
        ('footer', 'Swipe down on the bottom edge of the screen to bring the top into reach.'),
        ('card', [('haptic', 'Haptic Touch', None, None, 'chev', None),
                  ('accom', 'Touch Accommodations', None, 'Off', 'chev', None)]),
        ('card', [('wake', 'Tap or Swipe to Wake', None, None, 'toggle_on', None),
                  ('shake', 'Shake to Undo', None, None, 'toggle_on', None),
                  ('vib', 'Vibration', None, None, 'toggle_on', None),
                  ('endcall', 'Prevent Lock to End Call', None, None, 'toggle_off', None)]),
        ('card', [('audio', 'Call Audio Routing', None, 'Automatic', 'chev', None)]),
        ('card', [('backtap', 'Back Tap', None, '@bt', 'chev', None)]),
        ('footer', 'Double or triple tap on the back of your iPhone to perform actions quickly.'),
    ],
    'backtap': [
        ('back', 'Touch'), ('title', 'Back Tap'),
        ('card', [('double', 'Double Tap', None, '@dt', 'chev', None),
                  ('triple', 'Triple Tap', None, '@tt', 'chev', None)]),
        ('footer', 'Double or triple tap on the back of your iPhone to perform actions quickly.'),
    ],
    'doubletap': [
        ('back', 'Back Tap'), ('title', 'Double Tap'),
        ('card', [('none', 'None', None, None, 'sel', None)]),
        ('header', 'SYSTEM'),
        ('card', [(k.lower().replace(' ', ''), k, None, None, 'sel', None) for k in
                  ['App Switcher', 'Camera', 'Control Center', 'Flashlight', 'Home', 'Lock Rotation',
                   'Lock Screen', 'Mute', 'Notification Center', 'Reachability', 'Screenshot', 'Shake']]),
    ],
}

DEFAULT_OV = {'bt': 'Off', 'dt': 'None', 'tt': 'None', 'sel': 'none'}


def glyph(d, kind, x, y, s):
    """white glyph in icon square at (x,y) size s"""
    c = (x + s / 2, y + s / 2)
    w = (255, 255, 255)
    if kind == 'gear':
        pts = []
        for i in range(32):
            a = i * math.pi / 16
            r = s * (0.36 if (i // 2) % 2 == 0 else 0.27)
            pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
        d.polygon(pts, fill=w)
        d.ellipse((c[0] - s * .13, c[1] - s * .13, c[0] + s * .13, c[1] + s * .13), fill=(142, 142, 147))
    elif kind == 'person':
        d.ellipse((c[0] - s * .09, y + s * .16, c[0] + s * .09, y + s * .34), fill=w)
        d.line([(x + s * .22, y + s * .44), (x + s * .78, y + s * .44)], fill=w, width=max(3, int(s * .08)))
        d.line([(c[0], y + s * .40), (c[0], y + s * .62)], fill=w, width=max(3, int(s * .1)))
        d.line([(c[0], y + s * .60), (x + s * .34, y + s * .84)], fill=w, width=max(3, int(s * .08)))
        d.line([(c[0], y + s * .60), (x + s * .66, y + s * .84)], fill=w, width=max(3, int(s * .08)))
    elif kind == 'touch':
        d.ellipse((c[0] - s * .3, c[1] - s * .3, c[0] + s * .3, c[1] + s * .3), outline=w, width=max(2, int(s * .07)))
        d.ellipse((c[0] - s * .12, c[1] - s * .12, c[0] + s * .12, c[1] + s * .12), fill=w)
    elif kind == 'wifi':
        for i, r in enumerate((.34, .22)):
            d.arc((c[0] - s * r, c[1] - s * r + s * .12, c[0] + s * r, c[1] + s * r + s * .12), 220, 320, fill=w, width=max(2, int(s * .08)))
        d.ellipse((c[0] - s * .06, c[1] + s * .12, c[0] + s * .06, c[1] + s * .24), fill=w)
    elif kind == 'bars':
        for i in range(4):
            hh = s * (.15 + .12 * i)
            d.rounded_rectangle((x + s * (.2 + .16 * i), y + s * .75 - hh, x + s * (.3 + .16 * i), y + s * .75), 2, fill=w)
    elif kind == 'batt':
        d.rounded_rectangle((x + s * .18, y + s * .34, x + s * .76, y + s * .66), 4, outline=w, width=max(2, int(s * .06)))
        d.rectangle((x + s * .24, y + s * .4, x + s * .6, y + s * .6), fill=w)
        d.rectangle((x + s * .78, y + s * .44, x + s * .83, y + s * .56), fill=w)
    elif kind == 'cam':
        d.rounded_rectangle((x + s * .18, y + s * .32, x + s * .82, y + s * .74), 5, fill=w)
        d.ellipse((c[0] - s * .12, c[1] - s * .07, c[0] + s * .12, c[1] + s * .17), fill=(142, 142, 147))
    elif kind == 'sun':
        d.ellipse((c[0] - s * .16, c[1] - s * .16, c[0] + s * .16, c[1] + s * .16), fill=w)
        for i in range(8):
            a = i * math.pi / 4
            d.line([(c[0] + s * .24 * math.cos(a), c[1] + s * .24 * math.sin(a)),
                    (c[0] + s * .34 * math.cos(a), c[1] + s * .34 * math.sin(a))], fill=w, width=max(2, int(s * .06)))
    elif kind == 'grid':
        for i in range(2):
            for j in range(2):
                d.rounded_rectangle((x + s * (.24 + .28 * i), y + s * (.24 + .28 * j), x + s * (.46 + .28 * i), y + s * (.46 + .28 * j)), 3, fill=w)
    elif kind == 'zoom':
        d.ellipse((x + s * .2, y + s * .2, x + s * .62, y + s * .62), outline=w, width=max(2, int(s * .08)))
        d.line([(x + s * .58, y + s * .58), (x + s * .8, y + s * .8)], fill=w, width=max(3, int(s * .1)))
    elif kind == 'plane':
        d.polygon([(c[0], y + s * .15), (c[0] + s * .07, y + s * .4), (x + s * .85, y + s * .55), (c[0] + s * .07, y + s * .58),
                   (c[0] + s * .05, y + s * .78), (c[0] + s * .16, y + s * .86), (c[0] - s * .16, y + s * .86), (c[0] - s * .05, y + s * .78),
                   (c[0] - s * .07, y + s * .58), (x + s * .15, y + s * .55), (c[0] - s * .07, y + s * .4)], fill=w)
    else:
        d.ellipse((c[0] - s * .18, c[1] - s * .18, c[0] + s * .18, c[1] + s * .18), fill=w)


def chevron(d, x, cy, col, w=4, s=10, left=False):
    if left:
        d.line([(x + s, cy - s * 1.6), (x, cy), (x + s, cy + s * 1.6)], fill=col, width=w, joint='curve')
    else:
        d.line([(x, cy - s), (x + s, cy), (x, cy + s)], fill=col, width=w, joint='curve')


def checkmark(d, x, cy, col, s=14, w=5):
    d.line([(x, cy), (x + s * .4, cy + s * .45), (x + s * 1.1, cy - s * .55)], fill=col, width=w, joint='curve')


def render_card(rows, ov, hl):
    n = len(rows)
    img = Image.new('RGB', (CX1 - CX0, ROW * n), CARD)
    d = ImageDraw.Draw(img)
    ids = {}
    for i, (rid, label, icol, val, kind, gl) in enumerate(rows):
        y0 = i * ROW; cy = y0 + ROW / 2
        if rid == hl:
            d.rectangle((0, y0, img.width, y0 + ROW), fill=HL)
        lx = 22
        if icol:
            d.rounded_rectangle((20, y0 + 18, 70, y0 + 68), 12, fill=icol)
            glyph(d, gl, 20, y0 + 18, 50)
            lx = 88
        d.text((lx, cy), label, font=F(500, 30), fill=TXT, anchor='lm')
        if isinstance(val, str) and val.startswith('@'):
            val = ov.get(val[1:], DEFAULT_OV[val[1:]])
        right = img.width - 22
        if kind == 'chev':
            chevron(d, right - 10, cy, (196, 196, 200))
            right -= 30
        if val:
            d.text((right, cy), val, font=F(400, 30), fill=GRAY, anchor='rm')
        if kind in ('toggle_on', 'toggle_off'):
            on = kind == 'toggle_on'
            d.rounded_rectangle((img.width - 108, cy - 25, img.width - 22, cy + 25), 25, fill=GREEN if on else (229, 229, 234))
            kx = img.width - 49 if on else img.width - 81
            d.ellipse((kx - 21, cy - 21, kx + 21, cy + 21), fill=(255, 255, 255), outline=(215, 215, 220))
        if kind == 'sel' and ov.get('sel', 'none') == rid:
            checkmark(d, img.width - 48, cy, BLUE)
        if i < n - 1:
            d.line([(lx, y0 + ROW - 1), (img.width, y0 + ROW - 1)], fill=SEP, width=2)
        ids[rid] = (y0, y0 + ROW)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), 24, fill=255)
    return img, m, ids


_content_cache = {}


def screen_content(name, ov=None, hl=None):
    """tall content image + rows {id: (x0,y0,x1,y1)} in content coords"""
    ov = ov or {}
    key = (name, tuple(sorted(ov.items())), hl)
    if key in _content_cache:
        return _content_cache[key]
    if name == 'home':
        res = home_content(hl)
        _content_cache[key] = res
        return res
    blocks = SCREENS[name]
    img = Image.new('RGB', (SW, 2400), BG_UI)
    d = ImageDraw.Draw(img)
    y = 112
    rows = {}
    for b in blocks:
        t = b[0]
        if t == 'back':
            chevron(d, 24, y + 24, BLUE, w=5, s=11, left=True)
            d.text((50, y + 24), b[1], font=F(500, 32), fill=BLUE, anchor='lm')
            rows['back'] = (10, y - 6, 250, y + 56)
            y += 62
        elif t == 'title':
            d.text((30, y), b[1], font=F(600, 62), fill=TXT, anchor='lt')
            y += 98
        elif t == 'search':
            d.rounded_rectangle((CX0, y, CX1, y + 62), 18, fill=(227, 227, 232))
            d.ellipse((46, y + 18, 66, y + 38), outline=GRAY, width=3)
            d.line([(63, y + 36), (72, y + 45)], fill=GRAY, width=3)
            d.text((84, y + 31), 'Search', font=F(400, 30), fill=GRAY, anchor='lm')
            y += 92
        elif t == 'header':
            d.text((44, y + 26), b[1], font=F(500, 23), fill=GRAY, anchor='lm')
            y += 50
        elif t == 'card':
            cimg, m, ids = render_card(b[1], ov, hl)
            img.paste(cimg, (CX0, y), m)
            for k, (a0, a1) in ids.items():
                rows[k] = (CX0, y + a0, CX1, y + a1)
            y += cimg.height + 34
        elif t == 'footer':
            y -= 22
            for ln in wrap(b[1], F(400, 24), 460):
                d.text((44, y), ln, font=F(400, 24), fill=GRAY, anchor='lt')
                y += 31
            y += 30
    h = max(SH, y + 40)
    img = img.crop((0, 0, SW, h))
    _content_cache[key] = (img, rows)
    return img, rows


HOME_APPS = [
    ('Calendar', (255, 255, 255), 'cal'), ('Photos', (255, 255, 255), 'flower'), ('Camera', (142, 142, 147), 'cam'), ('Mail', (10, 122, 255), 'mail'),
    ('Notes', (255, 214, 10), 'notes'), ('Clock', (30, 30, 32), 'clock'), ('Maps', (120, 200, 120), 'pin'), ('Settings', (142, 142, 147), 'gear'),
    ('Weather', (60, 150, 240), 'sun'), ('Music', (250, 60, 90), 'note'), ('Books', (255, 149, 0), 'book'), ('Wallet', (30, 30, 32), 'grid'),
    ('Health', (255, 255, 255), 'heart'), ('Files', (10, 122, 255), 'grid'), ('Podcasts', (150, 80, 220), 'touch'), ('Fitness', (30, 30, 32), 'dot'),
]
DOCK = [((52, 199, 89), 'phone'), ((52, 199, 89), 'bubble'), ((10, 122, 255), 'compass'), ((250, 60, 90), 'note')]


def home_icon(d, kind, x, y, s, bg):
    w = (255, 255, 255)
    c = (x + s / 2, y + s / 2)
    if kind == 'cal':
        d.text((c[0], y + s * .22), 'THU', font=F(600, int(s * .17)), fill=(255, 59, 48), anchor='mm')
        d.text((c[0], y + s * .6), '1', font=F(500, int(s * .5)), fill=TXT, anchor='mm')
    elif kind == 'flower':
        cols = [(255, 149, 0), (255, 204, 0), (52, 199, 89), (10, 180, 220), (88, 86, 214), (175, 82, 222), (255, 45, 85), (255, 59, 48)]
        for i, col in enumerate(cols):
            a = i * math.pi / 4
            px, py = c[0] + s * .17 * math.cos(a), c[1] + s * .17 * math.sin(a)
            d.ellipse((px - s * .13, py - s * .13, px + s * .13, py + s * .13), fill=col)
    elif kind == 'mail':
        d.rounded_rectangle((x + s * .18, y + s * .3, x + s * .82, y + s * .7), 4, fill=w)
        d.line([(x + s * .2, y + s * .32), (c[0], c[1] + s * .04), (x + s * .8, y + s * .32)], fill=(10, 122, 255), width=3)
    elif kind == 'notes':
        d.rectangle((x, y, x + s, y + s * .28), fill=(255, 204, 0))
        d.rectangle((x, y + s * .28, x + s, y + s), fill=w)
        for i in range(3):
            d.line([(x + s * .15, y + s * (.45 + .15 * i)), (x + s * .85, y + s * (.45 + .15 * i))], fill=(220, 220, 220), width=2)
    elif kind == 'clock':
        d.ellipse((x + s * .12, y + s * .12, x + s * .88, y + s * .88), fill=w)
        d.line([c, (c[0], y + s * .26)], fill=TXT, width=3)
        d.line([c, (x + s * .7, c[1] + s * .1)], fill=TXT, width=3)
        d.ellipse((c[0] - 4, c[1] - 4, c[0] + 4, c[1] + 4), fill=(255, 149, 0))
    elif kind == 'pin':
        d.polygon([(x, y + s * .6), (x + s, y + s * .3), (x + s, y + s * .45), (x, y + s * .75)], fill=(250, 250, 240))
        d.ellipse((c[0] - s * .12, y + s * .2, c[0] + s * .12, y + s * .44), fill=(255, 59, 48))
    elif kind == 'note':
        d.ellipse((x + s * .26, y + s * .58, x + s * .44, y + s * .74), fill=w)
        d.line([(x + s * .42, y + s * .66), (x + s * .42, y + s * .26), (x + s * .72, y + s * .2), (x + s * .72, y + s * .58)], fill=w, width=5)
        d.ellipse((x + s * .56, y + s * .52, x + s * .74, y + s * .68), fill=w)
    elif kind == 'book':
        d.polygon([(c[0], y + s * .3), (x + s * .2, y + s * .25), (x + s * .2, y + s * .72), (c[0], y + s * .77)], fill=w)
        d.polygon([(c[0], y + s * .3), (x + s * .8, y + s * .25), (x + s * .8, y + s * .72), (c[0], y + s * .77)], fill=(255, 235, 210))
    elif kind == 'heart':
        r = s * .14
        d.ellipse((c[0] - 2 * r, c[1] - r * 1.4, c[0], c[1] + r * .6), fill=(255, 45, 85))
        d.ellipse((c[0], c[1] - r * 1.4, c[0] + 2 * r, c[1] + r * .6), fill=(255, 45, 85))
        d.polygon([(c[0] - 2 * r + 2, c[1] - r * .2), (c[0] + 2 * r - 2, c[1] - r * .2), (c[0], c[1] + r * 1.9)], fill=(255, 45, 85))
    elif kind == 'phone':
        d.rounded_rectangle((x + s * .3, y + s * .22, x + s * .7, y + s * .78), 10, outline=w, width=6)
    elif kind == 'bubble':
        d.ellipse((x + s * .18, y + s * .22, x + s * .82, y + s * .72), fill=w)
        d.polygon([(x + s * .28, y + s * .6), (x + s * .22, y + s * .82), (x + s * .45, y + s * .68)], fill=w)
    elif kind == 'compass':
        d.ellipse((x + s * .14, y + s * .14, x + s * .86, y + s * .86), fill=w)
        d.polygon([(x + s * .68, y + s * .32), (c[0] + 5, c[1] + 5), (c[0] - 5, c[1] - 5)], fill=(255, 59, 48))
        d.polygon([(x + s * .32, y + s * .68), (c[0] + 5, c[1] + 5), (c[0] - 5, c[1] - 5)], fill=(200, 200, 205))
    else:
        glyph(d, kind, x, y, s)


def wallpaper():
    img = Image.new('RGB', (SW, SH))
    d = ImageDraw.Draw(img)
    for yy in range(SH):
        t = yy / SH
        col = tuple(int(a + (b - a) * t) for a, b in zip((255, 205, 160), (250, 150, 150)))
        d.line([(0, yy), (SW, yy)], fill=col)
    d.ellipse((330, 120, 470, 260), fill=(255, 238, 200))
    layers = [((245, 130, 120), 640, 50, 0.010, 0.4), ((120, 190, 175), 760, 60, 0.008, 1.7),
              ((64, 150, 160), 880, 45, 0.012, 3.1), ((40, 105, 135), 1000, 55, 0.009, 0.9)]
    for col, base, amp, fr, ph in layers:
        pts = [(x, base + amp * math.sin(x * fr + ph) + amp * .4 * math.sin(x * fr * 2.7 + ph)) for x in range(0, SW + 10, 10)]
        d.polygon(pts + [(SW, SH), (0, SH)], fill=col)
    return img


def home_content(hl=None):
    img = wallpaper()
    over = Image.new('RGBA', img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(over)
    od.rounded_rectangle((18, 1020, SW - 18, 1158), 52, fill=(255, 255, 255, 95))
    img = Image.alpha_composite(img.convert('RGBA'), over).convert('RGB')
    d = ImageDraw.Draw(img)
    rows = {}
    s = 104
    for i, (label, bg, kind) in enumerate(HOME_APPS):
        r, c = divmod(i, 4)
        cx = 72 + 139 * c; cy = 200 + 186 * r
        x, y = cx - s / 2, cy - s / 2
        icon = Image.new('RGB', (s, s), bg)
        idr = ImageDraw.Draw(icon)
        home_icon(idr, kind, 0, 0, s, bg)
        if label == 'Settings' and hl == 'app_settings':
            icon = Image.blend(icon, Image.new('RGB', (s, s), (0, 0, 0)), 0.3)
        m = Image.new('L', (s, s), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, s - 1, s - 1), 26, fill=255)
        img.paste(icon, (int(x), int(y)), m)
        d.text((cx + 1, cy + 72), label, font=F(500, 22), fill=(60, 40, 40), anchor='mm')
        d.text((cx, cy + 71), label, font=F(500, 22), fill=(255, 255, 255), anchor='mm')
        rows['app_' + label.lower()] = (x, y, x + s, y + s)
    for i, (bg, kind) in enumerate(DOCK):
        cx = 72 + 139 * i; cy = 1089
        icon = Image.new('RGB', (s, s), bg)
        home_icon(ImageDraw.Draw(icon), kind, 0, 0, s, bg)
        m = Image.new('L', (s, s), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, s - 1, s - 1), 26, fill=255)
        img.paste(icon, (int(cx - s / 2), int(cy - s / 2)), m)
    return img, rows


def status_bar(img, dark_text=True, bg=None):
    d = ImageDraw.Draw(img)
    if bg:
        d.rectangle((0, 0, SW, 100), fill=bg)
    col = TXT if dark_text else (255, 255, 255)
    d.text((92, 52), '9:41', font=F(600, 32), fill=col, anchor='mm')
    for i in range(4):
        hh = 8 + 5 * i
        d.rounded_rectangle((404 + 9 * i, 62 - hh, 410 + 9 * i, 62), 2, fill=col)
    d.rounded_rectangle((452, 40, 500, 64), 7, outline=col, width=3)
    d.rounded_rectangle((457, 45, 488, 59), 3, fill=col)
    d.rectangle((502, 48, 505, 56), fill=col)


_tex = None


def screen_tex():
    global _tex
    if _tex is None:
        _tex = paper_tex(SW, SH, seed=21, strength=0.8)
    return _tex


def view(spec):
    """spec: dict(name, scroll, hl, ov) -> SWxSH RGB"""
    content, rows = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))
    sc = int(spec.get('scroll', 0))
    v = content.crop((0, sc, SW, sc + SH)).copy()
    if spec['name'] == 'home':
        status_bar(v, dark_text=True)
    else:
        status_bar(v, dark_text=True, bg=BG_UI)
    return v


def row_point(spec, rid, fx=0.62):
    _, rows = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    if spec['name'] == 'home':
        return (x0 + x1) / 2 + 8, (y0 + y1) / 2 + 10
    return x0 + (x1 - x0) * fx, (y0 + y1) / 2 - spec.get('scroll', 0)


def max_scroll(spec):
    content, _ = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))
    return max(0, content.height - SH)

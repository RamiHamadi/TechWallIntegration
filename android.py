"""Tech Wall ep.4 — Android Notification history — Blueprint stop-motion"""
import sys, os, math
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter
import screens as S
from screens import SW, SH, glyph
from lib import F, rotate_sprite, rng_for, FPS, ease, apply_tex
import movie as m
import movie_blue as mb
import themes as th

OUT = __import__('lib').out('frames_android')
mb.OUT = OUT
NAVY, MID, YEL, PAPER = mb.NAVY, mb.MID, mb.YEL, mb.PAPER

BG = (250, 248, 253)
SURF = (243, 237, 247)
TXT = (28, 27, 31)
SUB = (88, 84, 96)
ACC = (11, 87, 208)
ACC_L = (216, 228, 255)
HLC = (226, 222, 232)
ROWH = 112


# ======================================================================= android phone hardware
def android_phone_raw():
    PW, PH = 600, 1224
    img = Image.new('RGBA', (PW + 16, PH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for a, b in [(300, 380), (430, 600)]:
        d.rounded_rectangle((PW, a, PW + 16, b), 5, fill=(70, 74, 86))
    d.rounded_rectangle((8, 0, PW + 8, PH - 1), 70, fill=(30, 32, 38))
    d.rounded_rectangle((14, 6, PW + 2, PH - 7), 64, outline=(84, 88, 100), width=4)
    return img


# ======================================================================= android screens
def arrow_back(d, x, cy, col=TXT):
    d.line([(x, cy), (x + 30, cy)], fill=col, width=4)
    d.line([(x, cy), (x + 13, cy - 13)], fill=col, width=4)
    d.line([(x, cy), (x + 13, cy + 13)], fill=col, width=4)


def mswitch(d, x, cy, on):
    w, h = 92, 52
    if on:
        d.rounded_rectangle((x, cy - h / 2, x + w, cy + h / 2), h / 2, fill=ACC)
        kx = x + w - 28
        d.ellipse((kx - 20, cy - 20, kx + 20, cy + 20), fill=(255, 255, 255))
        d.line([(kx - 9, cy), (kx - 2, cy + 7), (kx + 10, cy - 7)], fill=ACC, width=4)
    else:
        d.rounded_rectangle((x, cy - h / 2, x + w, cy + h / 2), h / 2, fill=(226, 224, 232), outline=(120, 116, 128), width=3)
        kx = x + 26
        d.ellipse((kx - 13, cy - 13, kx + 13, cy + 13), fill=(120, 116, 128))


def bell(d, cx, cy, col, s=1.0, slash=False):
    d.pieslice((cx - 34 * s, cy - 40 * s, cx + 34 * s, cy + 28 * s), 180, 360, fill=col)
    d.rectangle((cx - 34 * s, cy - 6 * s, cx + 34 * s, cy + 22 * s), fill=col)
    d.rounded_rectangle((cx - 44 * s, cy + 18 * s, cx + 44 * s, cy + 30 * s), 6, fill=col)
    d.ellipse((cx - 10 * s, cy + 30 * s, cx + 10 * s, cy + 46 * s), fill=col)
    if slash:
        d.line([(cx - 52 * s, cy - 48 * s), (cx + 52 * s, cy + 52 * s)], fill=BG, width=int(14 * s))
        d.line([(cx - 52 * s, cy - 48 * s), (cx + 52 * s, cy + 52 * s)], fill=col, width=int(6 * s))


def app_icon(d, cx, cy, r, col, gl):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
    if gl == 'msg':
        d.rounded_rectangle((cx - r * .5, cy - r * .4, cx + r * .5, cy + r * .3), 6, fill=(255, 255, 255))
        d.polygon([(cx - r * .3, cy + r * .25), (cx - r * .45, cy + r * .55), (cx, cy + r * .28)], fill=(255, 255, 255))
    elif gl == 'cal':
        d.rounded_rectangle((cx - r * .45, cy - r * .4, cx + r * .45, cy + r * .45), 4, fill=(255, 255, 255))
        d.rectangle((cx - r * .45, cy - r * .4, cx + r * .45, cy - r * .18), fill=(30, 30, 40))
    elif gl == 'box':
        d.polygon([(cx, cy - r * .5), (cx + r * .45, cy - r * .25), (cx + r * .45, cy + r * .3), (cx, cy + r * .55), (cx - r * .45, cy + r * .3), (cx - r * .45, cy - r * .25)], fill=(255, 255, 255))
    elif gl == 'bell':
        bell(d, cx, cy - r * .12, (255, 255, 255), s=r / 75)
    else:
        glyph(d, gl, cx - r * .8, cy - r * .8, r * 1.6)


NOTIFS = {
    'mom': ('Messages', (30, 160, 90), 'msg', 'Mom', "Don't forget the keys!"),
    'cal': ('Calendar', (66, 133, 244), 'cal', 'Dentist', 'Today at 4:00 PM'),
    'pkg': ('Delivery', (230, 120, 30), 'box', 'Your package', 'Arriving today by 6 PM'),
}


def notif_card(d, x0, y0, w, key, when='now', hl=False, bg=(255, 255, 255)):
    app, col, gl, title, body = NOTIFS[key]
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 132), 28, fill=HLC if hl else bg)
    app_icon(d, x0 + 46, y0 + 48, 24, col, gl)
    d.text((x0 + 86, y0 + 34), f'{app}  ·  {when}', font=F(500, 21), fill=SUB, anchor='lm')
    d.text((x0 + 86, y0 + 66), title, font=F(600, 27), fill=TXT, anchor='lm')
    d.text((x0 + 86, y0 + 100), body, font=F(400, 24), fill=SUB, anchor='lm')


def wallpaper():
    im = Image.new('RGB', (SW, SH))
    d = ImageDraw.Draw(im)
    for y in range(SH):
        t = y / SH
        d.line([(0, y), (SW, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip((120, 100, 200), (40, 140, 160))))
    for cx, cy, r_, c in [(460, 300, 220, (170, 130, 230)), (120, 800, 260, (60, 180, 170))]:
        g = Image.new('L', (SW, SH), 0); ImageDraw.Draw(g).ellipse((cx - r_, cy - r_, cx + r_, cy + r_), fill=150)
        im.paste(Image.new('RGB', (SW, SH), c), (0, 0), g.filter(ImageFilter.GaussianBlur(70)))
    return im


_wp = None


def home_content(ov, hl):
    global _wp
    if _wp is None:
        _wp = wallpaper()
    im = _wp.copy()
    d = ImageDraw.Draw(im)
    rows = {}
    d.text((40, 190), '9:41', font=F(500, 110), fill=(255, 255, 255), anchor='ls')
    d.text((44, 236), 'Thu, Oct 1', font=F(500, 30), fill=(240, 240, 250), anchor='ls')
    apps = [('Phone', (30, 160, 90), 'dot'), ('Messages', (30, 160, 90), 'msg'), ('Camera', (90, 90, 100), 'cam'), ('Settings', (100, 104, 116), 'gear'),
            ('Calendar', (66, 133, 244), 'cal'), ('Photos', (240, 170, 40), 'sun'), ('Maps', (52, 168, 83), 'dot'), ('Clock', (60, 60, 70), 'dot')]
    for i, (nm, col, gl) in enumerate(apps):
        r, c = divmod(i, 4)
        cx = 76 + c * 136; cy = 760 + r * 160
        rr = 46
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col)
        if gl == 'msg' or gl == 'cal':
            app_icon(d, cx, cy, rr, col, gl)
        else:
            glyph(d, gl, cx - rr * .75, cy - rr * .75, rr * 1.5)
        if nm == 'Settings' and hl == 'app_settings':
            d.ellipse((cx - rr - 6, cy - rr - 6, cx + rr + 6, cy + rr + 6), outline=(255, 255, 255), width=5)
        d.text((cx, cy + 66), nm, font=F(500, 21), fill=(255, 255, 255), anchor='mm')
        rows['app_' + nm.lower()] = (cx - rr, cy - rr - 10, cx + rr, cy + rr - 10)
    d.rounded_rectangle((36, 1066, SW - 36, 1130), 32, fill=(240, 236, 248))
    d.ellipse((66, 1084, 92, 1110), outline=SUB, width=4); d.line([(88, 1106), (98, 1116)], fill=SUB, width=4)
    d.text((116, 1098), 'Search', font=F(500, 26), fill=SUB, anchor='lm')
    d.rounded_rectangle((SW / 2 - 70, SH - 22, SW / 2 + 70, SH - 14), 4, fill=(255, 255, 255))
    if ov.get('banner') is not None and ov['banner'] < 600:
        bx = 20 + ov['banner']
        sh = Image.new('L', im.size, 0)
        ImageDraw.Draw(sh).rounded_rectangle((bx + 6, 70, bx + 526, 214), 28, fill=110)
        im.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(10)))
        d = ImageDraw.Draw(im)
        notif_card(d, bx, 64, 520, ov.get('bkey', 'mom'))
        rows['banner'] = (bx, 64, bx + 520, 196)
    return im, rows


def list_rows(d, y, items, hl, rows, icons=True):
    for rid, title, sub, col, gl in items:
        if hl == rid:
            d.rounded_rectangle((12, y, SW - 12, y + ROWH), 22, fill=HLC)
        x = 40
        if icons:
            app_icon(d, 64, y + ROWH / 2, 30, col, gl); x = 118
        d.text((x, y + 42), title, font=F(500, 30), fill=TXT, anchor='lm')
        if sub:
            d.text((x, y + 78), sub, font=F(400, 23), fill=SUB, anchor='lm')
        rows[rid] = (12, y, SW - 12, y + ROWH)
        y += ROWH
    return y


def settings_content(ov, hl):
    im = Image.new('RGB', (SW, 1500), BG)
    d = ImageDraw.Draw(im); rows = {}
    d.text((32, 170), 'Settings', font=F(600, 60), fill=TXT, anchor='ls')
    d.rounded_rectangle((24, 200, SW - 24, 270), 35, fill=SURF)
    d.ellipse((50, 222, 74, 246), outline=SUB, width=4); d.line([(70, 242), (80, 252)], fill=SUB, width=4)
    d.text((98, 235), 'Search Settings', font=F(400, 26), fill=SUB, anchor='lm')
    y = 300
    y = list_rows(d, y, [
        ('net', 'Network & internet', 'Wi-Fi, mobile, hotspot', (66, 133, 244), 'wifi'),
        ('dev', 'Connected devices', 'Bluetooth, pairing', (52, 168, 83), 'dot'),
        ('apps', 'Apps', 'Recent apps, default apps', (230, 120, 30), 'grid'),
        ('notifications', 'Notifications', 'Notification history, conversations', (150, 90, 210), 'bell'),
        ('battery', 'Battery', '82%', (52, 168, 83), 'batt'),
        ('storage', 'Storage', '46% used', (90, 90, 160), 'dot'),
        ('sound', 'Sound & vibration', 'Volume, haptics', (0, 150, 160), 'dot'),
        ('display', 'Display', 'Dark theme, font size', (240, 170, 40), 'sun')], hl, rows)
    return im.crop((0, 0, SW, max(SH, y + 40))), rows


def notif_content(ov, hl):
    im = Image.new('RGB', (SW, 1500), BG)
    d = ImageDraw.Draw(im); rows = {}
    arrow_back(d, 34, 132); rows['back'] = (20, 100, 100, 164)
    d.text((32, 250), 'Notifications', font=F(600, 54), fill=TXT, anchor='ls')
    y = 290
    d.text((40, y + 20), 'Manage', font=F(600, 24), fill=ACC, anchor='lm'); y += 46
    y = list_rows(d, y, [
        ('appn', 'App notifications', 'Control notifications from apps', None, None),
        ('history', 'Notification history', 'Show recent and snoozed notifications', None, None),
        ('conv', 'Conversations', 'No priority conversations', None, None),
        ('bubbles', 'Bubbles', 'On / Conversations can float', None, None)], hl, rows, icons=False)
    y += 16
    d.text((40, y + 20), 'Privacy', font=F(600, 24), fill=ACC, anchor='lm'); y += 46
    y = list_rows(d, y, [
        ('lock', 'Notifications on lock screen', 'Show all notifications', None, None),
        ('sens', 'Sensitive notifications', 'Hide on lock screen', None, None)], hl, rows, icons=False)
    return im.crop((0, 0, SW, max(SH, y + 40))), rows


def hist_content(ov, hl):
    im = Image.new('RGB', (SW, 1500), BG)
    d = ImageDraw.Draw(im); rows = {}
    arrow_back(d, 34, 132); rows['back'] = (20, 100, 100, 164)
    d.text((32, 250), 'Notification history', font=F(600, 46), fill=TXT, anchor='ls')
    on = ov.get('on', False)
    y = 290
    d.rounded_rectangle((24, y, SW - 24, y + 100), 50, fill=ACC_L if on else SURF)
    if hl == 'switch':
        d.rounded_rectangle((24, y, SW - 24, y + 100), 50, fill=HLC)
    d.text((56, y + 50), 'Use notification history', font=F(600, 28), fill=TXT, anchor='lm')
    mswitch(d, SW - 140, y + 50, on)
    rows['switch'] = (24, y, SW - 24, y + 100)
    y += 140
    items = ov.get('items')
    if not on:
        bell(d, SW / 2, 600, (150, 146, 158), 1.3, slash=True)
        for i, ln in enumerate(['Turn on notification history', 'to see recent and snoozed', 'notifications']):
            d.text((SW / 2, 720 + i * 36), ln, font=F(400, 26), fill=SUB, anchor='mm')
    elif not items:
        bell(d, SW / 2, 600, (150, 146, 158), 1.3)
        d.text((SW / 2, 720), 'No recent notifications', font=F(400, 26), fill=SUB, anchor='mm')
    else:
        d.text((40, y + 10), 'Recently dismissed', font=F(600, 24), fill=ACC, anchor='lm'); y += 34
        notif_card(d, 24, y, SW - 48, 'mom', when='1m', hl=(hl == 'n_mom'), bg=SURF)
        rows['n_mom'] = (24, y, SW - 24, y + 132)
        if ov.get('glow'):
            d.rounded_rectangle((20, y - 4, SW - 20, y + 136), 30, outline=YEL, width=6)
        y += 160
        d.text((40, y + 10), 'Last 24 hours', font=F(600, 24), fill=ACC, anchor='lm'); y += 34
        for k, w in [('cal', '2h'), ('pkg', '5h')]:
            notif_card(d, 24, y, SW - 48, k, when=w, bg=SURF); y += 146
    return im.crop((0, 0, SW, max(SH, y + 40))), rows


def shade_content(ov, hl):
    global _wp
    if _wp is None:
        _wp = wallpaper()
    im = Image.blend(_wp, Image.new('RGB', (SW, SH), (20, 18, 30)), 0.82)
    d = ImageDraw.Draw(im); rows = {}
    d.text((32, 150), '9:41', font=F(500, 48), fill=(255, 255, 255), anchor='ls')
    d.text((32, 186), 'Thu, Oct 1', font=F(400, 24), fill=(200, 200, 215), anchor='ls')
    tiles = [('Internet', True), ('Bluetooth', False), ('Flashlight', False), ('Do Not Disturb', False)]
    for i, (nm, on) in enumerate(tiles):
        r_, c_ = divmod(i, 2)
        x0 = 24 + c_ * 262; y0 = 220 + r_ * 96
        d.rounded_rectangle((x0, y0, x0 + 250, y0 + 82), 41, fill=(190, 210, 255) if on else (60, 58, 74))
        d.text((x0 + 36, y0 + 41), nm if len(nm) < 11 else 'DND', font=F(500, 24), fill=(20, 20, 30) if on else (230, 230, 240), anchor='lm')
    notif_card(d, 24, 440, SW - 48, 'cal', when='2h', bg=(48, 46, 60))
    # recolor text for dark card
    d.rounded_rectangle((24, 440, SW - 24, 572), 28, fill=(48, 46, 60))
    app_icon(d, 70, 488, 24, (66, 133, 244), 'cal')
    d.text((110, 474), 'Calendar  ·  2h', font=F(500, 21), fill=(190, 190, 205), anchor='lm')
    d.text((110, 506), 'Dentist', font=F(600, 27), fill=(250, 250, 255), anchor='lm')
    d.text((110, 540), 'Today at 4:00 PM', font=F(400, 24), fill=(200, 200, 215), anchor='lm')
    for lab, x0, rid in [('Manage', 24, 'manage'), ('History', 196, 'hist_btn'), ('Clear all', 380, 'clear')]:
        hlb = hl == rid
        d.rounded_rectangle((x0, 600, x0 + 156, 660), 30, fill=(110, 100, 150) if hlb else (60, 58, 74))
        d.text((x0 + 78, 630), lab, font=F(600, 24), fill=(240, 240, 250), anchor='mm')
        rows[rid] = (x0, 600, x0 + 156, 660)
    if ov.get('pulse'):
        d.rounded_rectangle((190, 594, 358, 666), 34, outline=YEL, width=5)
    d.rounded_rectangle((SW / 2 - 70, SH - 22, SW / 2 + 70, SH - 14), 4, fill=(220, 220, 230))
    return im, rows


BUILDERS = {'a_home': home_content, 'a_settings': settings_content, 'a_notif': notif_content, 'a_hist': hist_content, 'a_shade': shade_content}
_cache = {}


def screen_content(name, ov=None, hl=None):
    ov = ov or {}
    key = (name, tuple(sorted(ov.items())), hl)
    if key not in _cache:
        _cache[key] = BUILDERS[name](ov, hl)
    return _cache[key]


def status_bar(img, light):
    d = ImageDraw.Draw(img)
    col = (255, 255, 255) if light else TXT
    d.text((40, 46), '9:41', font=F(600, 28), fill=col, anchor='lm')
    x = SW - 40
    d.rounded_rectangle((x - 22, 34, x, 58), 4, outline=col, width=3); d.rectangle((x - 18, 38, x - 6, 54), fill=col)
    d.polygon([(x - 64, 58), (x - 36, 58), (x - 36, 32)], fill=col)
    for r_ in (14, 8):
        d.arc((x - 90 - r_, 52 - r_, x - 90 + r_, 52 + r_), 225, 315, fill=col, width=3)


def aview(spec):
    content, rows = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))
    sc = int(spec.get('scroll', 0))
    v = content.crop((0, sc, SW, sc + SH)).copy()
    light = spec['name'] in ('a_home', 'a_shade')
    if not light:
        ImageDraw.Draw(v).rectangle((0, 0, SW, 84), fill=BG)
    status_bar(v, light)
    return v


def row_point(spec, rid, fx=0.62):
    _, rows = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    if rid.startswith('app_') or rid in ('hist_btn',):
        return (x0 + x1) / 2 + 6, (y0 + y1) / 2 + 8
    return x0 + (x1 - x0) * fx, (y0 + y1) / 2 - spec.get('scroll', 0)


m.row_point = row_point
_tex = None


def compose_screen(ph):
    global _tex
    sp = ph['spec']; tr = ph['trans']
    if tr:
        new, old, p = aview(sp), aview(tr['old']), tr['p']
        img = Image.new('RGB', (SW, SH), (0, 0, 0))
        if not tr['back']:
            img.paste(Image.blend(old, Image.new('RGB', old.size, (0, 0, 0)), 0.15 * p), (int(-p * SW * 0.3), 0))
            img.paste(new, (int((1 - p) * SW), 0))
        else:
            img.paste(Image.blend(new, Image.new('RGB', new.size, (0, 0, 0)), 0.15 * (1 - p)), (int(-(1 - p) * SW * 0.3), 0))
            img.paste(old, (int(p * SW), 0))
    else:
        img = aview(sp)
    d = ImageDraw.Draw(img)
    d.ellipse((SW / 2 - 15, 30, SW / 2 + 15, 60), fill=(8, 8, 10))
    if _tex is None:
        _tex = th.paper_tex(SW, SH, seed=91, strength=.7)
    return apply_tex(img, _tex)


m.compose_screen = compose_screen


# ======================================================================= timeline
def spec(name, **kw):
    d = dict(name=name, scroll=0, hl=None, ov={})
    d.update(kw)
    return d


def banner_swipe(t, label_fx=True):
    sp = t.ph['spec']
    for b in (-700, -300, -60, 0):          # banner drops in (slides from top via x? use y) -> slide in from left
        sp['ov'] = dict(sp['ov'], banner=b); t.snap()
    t.sound('pop'); t.hold(10)
    bx, by = t.s2c(*row_point(sp, 'banner', 0.35))
    t.move_hand(bx, by, 6); t.hold(1)
    t.press(bx, by, 'tap'); t.snap()
    for i, b in enumerate((60, 180, 360, 620)):
        sp['ov'] = dict(sp['ov'], banner=b); t.hand['x'] += [50, 110, 160, 180][i]; t.snap()
    t.sound('whoosh')
    t.hand['press'] = False
    sp['ov'] = {k: v for k, v in sp['ov'].items() if k != 'banner'}
    if label_fx:
        t.fx.append(('burst', t.f, 800, 820, 2)); t.sound('pop', 0)
    t.hold(3)
    t.hand_out(4)


def build():
    t = m.TL()
    t.ph['spec'] = spec('a_home')
    t.fx.append(('title', 0, 50)); t.hold(56)
    t.phone_to(m.PHY, 6, keys=-40); t.hold(2)
    # problem
    t.cap('P', 'Oops! You swiped a message away', m.PINK); t.hold(4)
    banner_swipe(t)
    t.cap('Q', 'Gone forever? Not on Android!', m.YELLOW); t.hold(20)
    # steps
    t.cap('1', 'Open Settings', m.YELLOW); t.hold(8)
    t.tap('app_settings', nav=spec('a_settings'), n_move=7)
    t.cap('2', 'Tap Notifications', m.PINK); t.hold(10)
    t.tap('notifications', nav=spec('a_notif'))
    t.cap('3', 'Tap Notification history', m.MINT); t.hold(10)
    t.tap('history', nav=spec('a_hist', ov={'on': False}))
    t.cap('4', 'Turn on "Use notification history"', m.SKY); t.hold(10)
    t.tap('switch', fx=0.85, ov={'on': True})
    t.hold(6)
    t.cap('check', 'Done! It now keeps the last 24 hours', m.MINT); t.hold(16)
    t.hand_out(4)
    # field test
    t.cap('T', 'Test it: swipe a notification away...', m.PEACH)
    t.navigate(spec('a_home')); t.hold(6)
    banner_swipe(t, label_fx=False)
    t.navigate(spec('a_hist', ov={'on': True, 'items': True}))
    t.ph['spec']['ov'] = {'on': True, 'items': True, 'glow': True}; t.sound('ding')
    t.cap('check', "...it's still here in your history!", m.MINT)
    tx, ty = t.s2c(*row_point(t.ph['spec'], 'n_mom', 0.5))
    t.move_hand(tx + 40, ty + 110, 6); t.hold(26)
    t.hand_out(4)
    # bonus
    t.cap('+', 'Shortcut: tap History in your notification panel', m.SKY)
    t.navigate(spec('a_shade', ov={'pulse': True})); t.hold(10)
    t.tap('hist_btn', nav=spec('a_hist', ov={'on': True, 'items': True}))
    t.hold(20)
    t.hand_out(4)
    t.cap_off()
    t.phone_to(2700, 5)
    t.fx.append(('end', t.f)); t.hold(72)
    return t


# ======================================================================= props / title / end
def fig_head(badge):
    if badge.isdigit():
        return f'FIG. 0{badge}  /  STEP {badge} OF 4'
    return {'P': 'FIG. 00  /  THE PROBLEM', 'Q': 'FIG. 00  /  THE GOOD NEWS', 'T': 'FIG. 05  /  FIELD TEST',
            'check': 'RESULT  /  OK', '+': 'APPENDIX  /  BONUS'}[badge]


mb.fig_head = fig_head


def vellum_bell():
    w, h = 300, 560
    im = Image.new('RGBA', (w, h), (230, 240, 255, 70))
    d = ImageDraw.Draw(im)
    C = th.CHALK + (255,)
    d.rounded_rectangle((20, 20, w - 20, h - 20), 40, outline=C, width=5)
    d.ellipse((w / 2 - 10, 38, w / 2 + 10, 58), outline=C, width=3)
    cx, cy = w / 2, 230
    d.arc((cx - 60, cy - 70, cx + 60, cy + 50), 180, 360, fill=C, width=6)
    d.line([(cx - 60, cy - 10), (cx - 60, cy + 40)], fill=C, width=6); d.line([(cx + 60, cy - 10), (cx + 60, cy + 40)], fill=C, width=6)
    d.line([(cx - 80, cy + 44), (cx + 80, cy + 44)], fill=C, width=6)
    d.ellipse((cx - 14, cy + 52, cx + 14, cy + 80), outline=C, width=5)
    # clock-rewind arrow
    d.arc((cx - 90, 330, cx + 90, 510), 200, 500, fill=mb.YEL + (255,), width=6)
    d.polygon([(cx - 92, 400), (cx - 110, 372), (cx - 70, 376)], fill=mb.YEL + (255,))
    d.text((cx, 420), '24h', font=th.JB(800, 44), fill=C, anchor='mm')
    sp = th.sprite(im, border=0, off=(6, 9), blur=6, op=.3, tex=False)
    return rotate_sprite(sp, 8)


def init_props():
    mb.init_props()
    P = m.P
    P['front'] = th.sprite(android_phone_raw(), border=8, off=(16, 22), blur=14, op=.4)
    P['tiles'] = [rotate_sprite(th.stencil_letter(ch, PAPER if i < 4 else YEL), rng_for('o', i).uniform(-6, 6)) for i, ch in enumerate('OOPS!')]
    P['t_label'] = mb.label('SPEC // Android tip', th.JB(700, 34), fg=MID, rot=-2, padx=30, pady=16)
    P['t_s1'] = mb.center_label('SWIPED A NOTIFICATION AWAY?', th.JB(800, 42), rot=1.5)
    P['t_s1b'] = mb.center_label('ANDROID CAN BRING IT BACK', th.JB(800, 42), rot=-1)
    P['t_s2'] = mb.center_label('notification history', th.JB(700, 40), bg=YEL, rot=-2)
    P['t_phone'] = vellum_bell()
    P['t_burst'] = mb.label(['ANDROID', '11 & LATER'], th.JB(800, 36), rot=6, padx=26, pady=16)
    P['bursts'] = P['bursts'][:2] + [mb.label('OOPS!', th.JB(800, 70), bg=YEL, tape=True, rot=-8, padx=30, pady=12)]
    P['e_chips'] = [rotate_sprite(mb.path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('Settings', (100, 104, 116), 'gear', -2), ('Notifications', (150, 90, 210), 'bell', 1.5),
        ('Notification history', ACC, 'dot', -1.5), ('Turn it on', NAVY, 'touch', 2)])]
    P['e_s1'] = mb.center_label('SAMSUNG: NOTIFICATIONS > ADVANCED SETTINGS', th.JB(800, 32), bg=YEL, rot=-1.5)
    P['e_s2'] = mb.center_label('KEEPS THE LAST 24 HOURS', th.JB(800, 46), rot=1.5)
    P['e_s3'] = mb.center_label('Android 11 or later', th.JB(600, 34), fg=MID, rot=-1, pady=18)


def draw_title(cv, f, a, ex):
    P = m.P
    els = [('t_label', 540, 380, a + 1, 0)]
    for i in range(5):
        els.append((i, 540 + (i - 2) * 175, 620, a + 4 + 2 * i, i % 3))
    els += [('t_s1', 540, 870, a + 16, 0), ('t_s1b', 540, 975, a + 19, 1), ('t_s2', 520, 1095, a + 23, 2),
            ('t_phone', 540, 1500, a + 27, 0), ('t_burst', 820, 1380, a + 31, 1)]
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
            for ap in [a + 1] + [a + 4 + 2 * i for i in range(5)] + [a + 16, a + 19, a + 23, a + 27, a + 31]:
                t.snd.append((ap, 'pop'))
            t.snd.append((e[2] + 1, 'whoosh'))
        if e[0] == 'end':
            a = e[1]
            for ap in [a + 2] + [a + 6 + 4 * i for i in range(4)] + [a + 24, a + 28, a + 32]:
                t.snd.append((ap, 'pop'))


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
        m.make_audio(m.TLD, n, __import__('lib').out('audio_android.wav'))

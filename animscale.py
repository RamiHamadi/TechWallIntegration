"""Tech Wall — Android: animation scale 0.5x ("make your Android *feel* 2x faster"), result-first (~30 s).
Frame 0 shows the payoff (Developer options, all 3 animation scales at 0.5x) with the hook, a snappy app open
proves it, then "here's how": Build number x7 -> System > Developer options -> 3 pickers -> 0.5x.
Screens/props from android.py (Android phone + Material-style screens); timeline from rf_demo.py.
Build:  ./build.sh animscale
"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import android as A
from android import BG, SURF, TXT, SUB, ACC, ACC_L, HLC, ROWH, arrow_back, mswitch, list_rows, android_phone_raw, spec
from screens import SW, SH
from lib import F, rotate_sprite, rng_for, ease
import movie as m
import movie_blue as mb
import themes as th

EP = 'animscale'
OUT = __import__('lib').out(f'frames_{EP}')
mb.OUT = OUT
NAVY, MID, YEL, PAPER = mb.NAVY, mb.MID, mb.YEL, mb.PAPER
SCALES = [('win', 'Window animation scale'), ('trans', 'Transition animation scale'), ('anim', 'Animator duration scale')]
PICK = ['Animation off', 'Animation scale .5x', 'Animation scale 1x', 'Animation scale 1.5x', 'Animation scale 2x',
        'Animation scale 5x', 'Animation scale 10x']


# ======================================================================= screens
def header(d, title, rows, size=54):
    arrow_back(d, 34, 132); rows['back'] = (20, 100, 100, 164)
    d.text((32, 250), title, font=F(600, size), fill=TXT, anchor='ls')


def settings_content(ov, hl):
    im = Image.new('RGB', (SW, 1700), BG)
    d = ImageDraw.Draw(im); rows = {}
    d.text((32, 170), 'Settings', font=F(600, 60), fill=TXT, anchor='ls')
    d.rounded_rectangle((24, 200, SW - 24, 270), 35, fill=SURF)
    d.ellipse((50, 222, 74, 246), outline=SUB, width=4); d.line([(70, 242), (80, 252)], fill=SUB, width=4)
    d.text((98, 235), 'Search Settings', font=F(400, 26), fill=SUB, anchor='lm')
    y = list_rows(d, 300, [
        ('net', 'Network & internet', 'Wi-Fi, mobile, hotspot', (66, 133, 244), 'wifi'),
        ('cdev', 'Connected devices', 'Bluetooth, pairing', (52, 168, 83), 'dot'),
        ('apps', 'Apps', 'Recent apps, default apps', (230, 120, 30), 'grid'),
        ('notifications', 'Notifications', 'Notification history', (150, 90, 210), 'bell'),
        ('battery', 'Battery', '82%', (52, 168, 83), 'batt'),
        ('display', 'Display', 'Dark theme, font size', (240, 170, 40), 'sun'),
        ('wall', 'Wallpaper & style', 'Colors, themed icons', (200, 90, 140), 'grid'),
        ('a11y', 'Accessibility', 'Display, interaction, audio', (52, 120, 200), 'person'),
        ('sec', 'Security & privacy', 'App security, device lock', (52, 168, 83), 'dot'),
        ('loc', 'Location', 'On', (66, 133, 244), 'dot'),
        ('system', 'System', 'Languages, gestures, backup', (100, 104, 116), 'gear'),
        ('about', 'About phone', 'My Phone', (66, 133, 244), 'person')], hl, rows)
    return im.crop((0, 0, SW, max(SH, y + 40))), rows


def about_content(ov, hl):
    im = Image.new('RGB', (SW, SH), BG)
    d = ImageDraw.Draw(im); rows = {}
    header(d, 'About phone', rows)
    y = list_rows(d, 290, [
        ('name', 'Device name', 'My Phone', None, None),
        ('num', 'Phone number', '+1 555 0100', None, None),
        ('legal', 'Legal information', None, None, None),
        ('ver', 'Android version', '15', None, None),
        ('build', 'Build number', 'TW1A.251005.007', None, None)], hl, rows, icons=False)
    if ov.get('glow'):
        x0, y0, x1, y1 = rows['build']
        d.rounded_rectangle((x0 - 4, y0 - 4, x1 + 4, y1 + 4), 26, outline=YEL, width=6)
    toast = ov.get('toast')
    if toast:
        f = F(500, 25)
        w = f.getlength(toast) + 60
        d.rounded_rectangle((SW / 2 - w / 2, 1010, SW / 2 + w / 2, 1076), 33, fill=(48, 46, 56))
        d.text((SW / 2, 1043), toast, font=f, fill=(245, 245, 250), anchor='mm')
    return im, rows


def system_content(ov, hl):
    im = Image.new('RGB', (SW, SH), BG)
    d = ImageDraw.Draw(im); rows = {}
    header(d, 'System', rows)
    list_rows(d, 290, [
        ('lang', 'Languages', 'System languages, app languages', None, None),
        ('gest', 'Gestures', None, None, None),
        ('date', 'Date & time', 'GMT+03:00', None, None),
        ('backup', 'Backup', 'On', None, None),
        ('devopt', 'Developer options', None, None, None),
        ('reset', 'Reset options', None, None, None)], hl, rows, icons=False)
    return im, rows


def dev_content(ov, hl):
    im = Image.new('RGB', (SW, SH), BG)
    d = ImageDraw.Draw(im); rows = {}
    header(d, 'Developer options', rows, size=50)
    y = 284
    d.rounded_rectangle((24, y, SW - 24, y + 96), 48, fill=ACC_L)
    d.text((56, y + 48), 'Use developer options', font=F(600, 27), fill=TXT, anchor='lm')
    mswitch(d, SW - 140, y + 48, True)
    y += 120
    y = list_rows(d, y, [('stay', 'Stay awake', 'Screen never sleeps while charging', None, None),
                         ('usb', 'USB debugging', 'Debug mode when USB is connected', None, None)], hl, rows, icons=False)
    d.text((40, y + 26), 'Drawing', font=F(600, 25), fill=ACC, anchor='lm'); y += 54
    for rid, title in SCALES:
        val = ov.get(rid, '1x')
        if hl == rid:
            d.rounded_rectangle((12, y, SW - 12, y + ROWH), 22, fill=HLC)
        d.text((40, y + 40), title, font=F(500, 29), fill=TXT, anchor='lm')
        d.text((40, y + 78), f'Animation scale {val}', font=F(600 if val == '.5x' else 400, 24),
               fill=ACC if val == '.5x' else SUB, anchor='lm')
        if ov.get('glow') and val == '.5x':
            d.rounded_rectangle((16, y + 4, SW - 16, y + ROWH - 4), 22, outline=YEL, width=5)
        rows[rid] = (12, y, SW - 12, y + ROWH)
        y += ROWH
    pick = ov.get('pick')
    if pick:
        im = Image.blend(im, Image.new('RGB', im.size, (20, 18, 28)), .45)
        d = ImageDraw.Draw(im)
        x0, y0, x1 = 34, 250, SW - 34
        y1 = y0 + 110 + len(PICK) * 84
        d.rounded_rectangle((x0, y0, x1, y1), 34, fill=(243, 238, 248))
        d.text((x0 + 36, y0 + 60), dict(SCALES)[pick], font=F(600, 30), fill=TXT, anchor='lm')
        cur = ov.get(pick, '1x')
        for i, lab in enumerate(PICK):
            yy = y0 + 130 + i * 84
            on = lab.endswith(' ' + cur)
            if hl == f'p{i}':
                d.rounded_rectangle((x0 + 12, yy - 38, x1 - 12, yy + 38), 18, fill=HLC)
            d.ellipse((x0 + 34, yy - 16, x0 + 66, yy + 16), outline=ACC if on else SUB, width=4)
            if on:
                d.ellipse((x0 + 42, yy - 8, x0 + 58, yy + 8), fill=ACC)
            d.text((x0 + 90, yy), lab, font=F(500, 27), fill=TXT, anchor='lm')
            rows[f'p{i}'] = (x0 + 12, yy - 38, x1 - 12, yy + 38)
    return im, rows


def zoom_content(ov, hl):
    """home screen with the Messages app zooming open (p 0..1)"""
    base, rows = A.home_content({}, None)
    im = base.copy()
    p = ov.get('p', 0)
    if p > 0:
        cx, cy = 76 + 136, 760
        x0 = cx - 46 + (0 - (cx - 46)) * p; y0 = cy - 46 + (0 - (cy - 46)) * p
        x1 = cx + 46 + (SW - (cx + 46)) * p; y1 = cy + 46 + (SH - (cy + 46)) * p
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((x0, y0, x1, y1), int(46 * (1 - p) + 20), fill=BG if p > .6 else (30, 160, 90))
        if p >= 1:
            d.text((32, 200), 'Messages', font=F(600, 52), fill=TXT, anchor='ls')
            for i, (who, txt) in enumerate([('Sam', 'Lunch at 1?'), ('Mom', "Don't forget the keys!")]):
                yy = 260 + i * 130
                A.app_icon(d, 70, yy + 50, 32, (30, 160, 90), 'msg')
                d.text((122, yy + 34), who, font=F(600, 28), fill=TXT, anchor='lm')
                d.text((122, yy + 70), txt, font=F(400, 24), fill=SUB, anchor='lm')
    return im, rows


A.BUILDERS.update({'x_settings': settings_content, 'x_about': about_content, 'x_system': system_content,
                   'x_dev': dev_content, 'x_zoom': zoom_content})
_light = A.aview


def aview(sp):
    if sp['name'] == 'x_zoom' and sp.get('ov', {}).get('p', 0) < 1:
        content, _ = A.screen_content(sp['name'], sp.get('ov'), sp.get('hl'))
        v = content.copy(); A.status_bar(v, True); return v
    return _light(sp)


A.aview = aview


def row_point(sp, rid, fx=0.62):
    _, rows = A.screen_content(sp['name'], sp.get('ov'), sp.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    if rid.startswith('app_'):
        return (x0 + x1) / 2 + 6, (y0 + y1) / 2 + 8
    return x0 + (x1 - x0) * fx, (y0 + y1) / 2 - sp.get('scroll', 0)


m.row_point = row_point


# ======================================================================= timeline
def fig_head(badge):
    if badge.isdigit():
        return f"HERE'S HOW  /  STEP {badge} OF 3"
    return {'H': 'TECH WALL  /  ANDROID TIP', 'ok': 'RESULT  /  OK', '+': 'BONUS'}[badge]


mb.fig_head = fig_head
HALF = {'win': '.5x', 'trans': '.5x', 'anim': '.5x'}


def build():
    t = m.TL()
    # 0:00 — result first: all three scales at 0.5x
    mb.result_first(t, spec('x_dev', ov=dict(HALF, glow=True)), 'H', 'MAKE YOUR ANDROID FEEL 2X FASTER')
    t.hold(10)
    # proof: an app snaps open at half the animation time
    t.navigate(spec('a_home'))
    t.hold(2)
    t.tap('app_messages', n_move=4)
    t.ph['spec'] = spec('x_zoom', ov={'p': .5}); t.sound('swish'); t.snap()
    t.ph['spec'] = spec('x_zoom', ov={'p': 1}); t.snap()
    t.fx.append(('burst', t.f, 800, 760, 0)); t.sound('pop')
    t.hand_out(3); t.hold(10)
    # 0:03 — here's how
    t.cap('1', "Here's how: About phone, tap Build number 7x", m.MINT)
    t.navigate(spec('x_settings'), back=True)
    t.hold(4)
    t.swipe(500, y=950)
    t.tap('about', nav=spec('x_about'), n_move=4)
    t.hold(3)
    bx, by = t.s2c(*row_point(t.ph['spec'], 'build', 0.4))
    t.move_hand(bx, by, 4)
    sp = t.ph['spec']
    for k in range(1, 8):
        t.press(bx, by)
        left = 7 - k
        sp['ov'] = {'toast': (f'{left} steps away from being a developer' if 0 < left < 5
                              else ('You are now a developer!' if left == 0 else None))}
        if sp['ov']['toast'] is None:
            sp['ov'] = {}
        t.snap(); t.hand['press'] = False; t.snap()
    sp['ov'] = {'toast': 'You are now a developer!', 'glow': True}
    t.fx.append(('burst', t.f, 790, 1030, 1)); t.sound('ding')
    t.hand_out(3); t.hold(10)
    t.cap('2', 'Back, then System > Developer options', m.SKY)
    t.navigate(spec('x_settings', scroll=500), back=True)
    t.hold(3)
    t.tap('system', nav=spec('x_system'), n_move=4)
    t.hold(3)
    t.tap('devopt', nav=spec('x_dev'), n_move=4)
    t.hold(4)
    t.cap('3', 'Set all 3 animation scales to .5x', m.PEACH)
    t.hold(3)
    vals = {}
    for rid, _ in SCALES:
        t.tap(rid, n_move=4, fx=0.88)
        t.ph['spec']['ov'] = dict(vals, pick=rid); t.sound('pop'); t.hold(3)
        t.tap('p1', n_move=3, fx=0.1)
        vals[rid] = '.5x'
        t.ph['spec']['ov'] = dict(vals, pick=rid); t.sound('ding'); t.hold(2)
        t.ph['spec']['ov'] = dict(vals); t.hold(2)
    t.hand_out(3)
    t.cap('ok', 'Done! Every animation takes half the time', m.MINT)
    t.ph['spec']['ov'] = dict(vals, glow=True)
    t.hold(20)
    # bonus: Samsung path
    t.cap('+', 'Samsung: About phone > Software info', m.SKY)
    t.navigate(spec('x_about', ov={'glow': True}), back=True)
    t.hold(20)
    mb.end_card(t)
    return t


# ======================================================================= props
def init_props():
    mb.init_props()
    P = m.P
    P['front'] = th.sprite(android_phone_raw(), border=8, off=(16, 22), blur=14, op=.4)
    P['bursts'] = [mb.label('HALF THE WAIT!', th.JB(800, 56), bg=YEL, tape=True, rot=-7, padx=28, pady=12),
                   mb.label('7 TAPS!', th.JB(800, 64), tape=True, rot=6, padx=30, pady=12)]
    P['e_chips'] = [rotate_sprite(mb.path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('Build number x7', (66, 133, 244), 'touch', -2), ('Developer options', (100, 104, 116), 'gear', 1.5),
        ('Drawing', (240, 170, 40), 'sun', -1.5), ('All 3 at .5x', NAVY, 'dot', 2)])]
    P['e_s1'] = mb.center_label('ONLY CHANGE THESE 3 SETTINGS', th.JB(800, 44), bg=YEL, rot=-1.5)
    P['e_s2'] = mb.center_label('SAMSUNG: SOFTWARE INFORMATION', th.JB(800, 42), rot=1.5)
    P['e_s3'] = mb.center_label('apps run the same, they just feel snappier', th.JB(600, 32), fg=MID, rot=-1, pady=18)


if __name__ == '__main__':
    t = build()
    for e in t.fx:
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))
    mb.finish(t, EP, init_props)

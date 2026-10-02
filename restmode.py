"""Tech Wall ep.8 — PS5: charge controllers in Rest Mode — Blueprint stop-motion (TV + console + controller rig)"""
import sys, os, math
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter
import movie as m
import themes as th
from movie_blue import label, center_label, path_label, chalk_arrow, dashed_ring, NAVY, MID, YEL, PAPER
from lib import rotate_sprite, rng_for, FPS, ease, jit, draw_sprite, blit, apply_tex, paper_tex, F
import winv as wv
from winv import MON_W, MON_RAW_H, SW, SH, MONX, MONY, HIDE, scr_origin, monitor_raw

OUT = __import__('lib').out('frames_restmode')
UI_BG = (14, 22, 44)
UI_TXT = (236, 240, 248)
UI_DIM = (140, 150, 172)
ORANGE = (255, 150, 40)
LBLUE = (70, 150, 255)

# ------------------------------------------------------------------ rig geometry (canvas coords)
CON_X, CON_Y = 250, 1590          # console
CTL_X, CTL_Y = 735, 1600          # controller
GAUGE = (930, 1390)               # battery gauge label
BTN = {'dpad_r': (CTL_X - 98, CTL_Y - 34), 'dpad_d': (CTL_X - 122, CTL_Y - 10), 'dpad_u': (CTL_X - 122, CTL_Y - 58),
       'ok': (CTL_X + 122, CTL_Y + 8), 'home': (CTL_X, CTL_Y + 58)}


# ------------------------------------------------------------------ props
def console_raw(light):
    w, h = 360, 170
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 18, w, h), 26, fill=(244, 245, 249), outline=(200, 205, 216), width=3)
    d.rounded_rectangle((18, 0, w - 18, 40), 18, fill=(250, 250, 252), outline=(200, 205, 216), width=3)
    d.rectangle((0, 84, w, 112), fill=(38, 40, 50))
    col = {'white': (235, 245, 255), 'orange': ORANGE, 'orange_lo': (190, 110, 40), 'off': (70, 72, 82)}[light]
    d.rounded_rectangle((24, 94, w - 24, 102), 4, fill=col)
    d.rounded_rectangle((30, 128, 62, 144), 3, fill=(60, 62, 72))          # USB port
    d.rounded_rectangle((76, 128, 108, 144), 3, fill=(60, 62, 72))
    d.ellipse((w - 52, 124, w - 30, 146), outline=(160, 166, 178), width=3)  # power button
    return im


def controller_raw(light, pressed):
    w, h = 470, 300
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    body, edge = (246, 247, 250), (196, 200, 212)
    d.ellipse((0, 70, 190, 300), fill=body, outline=edge, width=3)            # left grip
    d.ellipse((w - 190, 70, w, 300), fill=body, outline=edge, width=3)        # right grip
    d.rounded_rectangle((40, 20, w - 40, 200), 70, fill=body, outline=edge, width=3)
    d.rectangle((60, 120, w - 60, 200), fill=body)
    # touchpad + light bar
    lc = {'blue': LBLUE, 'orange': ORANGE, 'orange_lo': (200, 120, 50), 'off': (200, 204, 214)}[light]
    d.rounded_rectangle((165, 22, w - 165, 98), 14, fill=(228, 231, 238), outline=edge, width=2)
    d.rounded_rectangle((150, 18, 172, 102), 8, fill=lc); d.rounded_rectangle((w - 172, 18, w - 150, 102), 8, fill=lc)
    cx, cy = w / 2, h / 2
    # d-pad
    dx, dy = 113, cy - 34
    for (ax, ay, bx, by), name in [((dx - 12, dy - 44, dx + 12, dy - 12), 'dpad_u'), ((dx - 12, dy + 12, dx + 12, dy + 44), 'dpad_d'),
                                   ((dx - 44, dy - 12, dx - 12, dy + 12), 'dpad_l'), ((dx + 12, dy - 12, dx + 44, dy + 12), 'dpad_r')]:
        d.rounded_rectangle((ax, ay, bx, by), 5, fill=YEL if pressed == name else (70, 74, 88))
    d.rectangle((dx - 12, dy - 12, dx + 12, dy + 12), fill=(70, 74, 88))
    # four plain face buttons (no symbols)
    fx, fy = w - 113, cy - 34
    for k, (ox, oy) in enumerate([(0, -40), (-40, 0), (40, 0), (0, 40)]):
        name = 'ok' if k == 3 else f'f{k}'
        d.ellipse((fx + ox - 17, fy + oy - 17, fx + ox + 17, fy + oy + 17), fill=YEL if pressed == name else (70, 74, 88))
    # sticks + home button
    for sx in (cx - 70, cx + 70):
        d.ellipse((sx - 30, cy + 26, sx + 30, cy + 86), fill=(52, 56, 68)); d.ellipse((sx - 20, cy + 36, sx + 20, cy + 76), fill=(84, 88, 102))
    d.ellipse((cx - 15, cy + 43, cx + 15, cy + 73), fill=YEL if pressed == 'home' else (60, 64, 78))
    return im


def gauge_raw(level, charging):
    w, h = 250, 96
    im = Image.new('RGBA', (w, h), PAPER + (255,))
    d = ImageDraw.Draw(im)
    col = (220, 60, 50) if level < .25 else (60, 170, 90)
    d.rounded_rectangle((18, 24, 128, 72), 8, outline=NAVY, width=5)
    d.rectangle((128, 38, 138, 58), fill=NAVY)
    d.rectangle((26, 32, 26 + int(94 * level), 64), fill=col)
    if charging:
        d.polygon([(78, 26), (60, 52), (74, 52), (66, 72), (90, 44), (76, 44), (84, 26)], fill=YEL, outline=NAVY)
    d.text((150, h / 2), f'{int(round(level * 100))}%', font=th.JB(800, 40), fill=NAVY, anchor='lm')
    return th.sprite(im, border=0, off=(6, 9), blur=6, op=.4)


# ------------------------------------------------------------------ TV screens
SETTINGS = ['Accessibility', 'Network', 'Users and Accounts', 'Family and Parental Controls', 'System', 'Accessories', 'Sound',
            'Screen and Video']
SYS_LEFT = ['System Software', 'Power Saving', 'Beeps', 'Language', 'Date and Time', 'Console Information']
POWER_RIGHT = ['Set Time Until Console Enters Rest Mode', 'Features Available in Rest Mode', 'Set Time Until Controllers Turn Off']
PICK = ['Off', '3 Hours', 'Always', 'Adaptive']
POWER_MENU = ['Enter Rest Mode', 'Turn Off Console', 'Restart Console']


def ui_bg():
    im = Image.new('RGB', (SW, SH))
    d = ImageDraw.Draw(im)
    for y in range(SH):
        t = y / SH
        d.line([(0, y), (SW, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip((22, 36, 74), (10, 14, 30))))
    return im


def sel_box(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0, y0, x1, y1), 10, fill=(44, 62, 108), outline=(245, 248, 255), width=3)


def game_screen(s):
    im = Image.new('RGB', (SW, SH))
    d = ImageDraw.Draw(im)
    for y in range(SH):
        t = y / SH
        d.line([(0, y), (SW, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip((120, 190, 250), (255, 210, 160))))
    d.ellipse((620, 50, 720, 150), fill=(255, 236, 160))
    d.polygon([(0, 380), (160, 250), (330, 380)], fill=(110, 170, 130)); d.polygon([(250, 380), (470, 220), (700, 380)], fill=(90, 150, 120))
    d.rectangle((0, 380, SW, SH), fill=(90, 160, 90))
    for i in range(6):
        d.rectangle((i * 160 - 20, 380, i * 160 + 70, 410), fill=(150, 110, 70))
    d.ellipse((330, 300, 380, 350), fill=(255, 200, 40), outline=(200, 140, 20), width=4)
    d.rounded_rectangle((200, 300, 250, 380), 12, fill=(230, 80, 80)); d.ellipse((205, 268, 245, 308), fill=(250, 220, 190))
    d.text((24, 28), 'SCORE 01250', font=th.JB(800, 24), fill=(255, 255, 255), anchor='lm')
    if s.get('notif'):
        x0, y0 = SW - 420, 20
        d.rounded_rectangle((x0, y0, SW - 20, y0 + 84), 14, fill=(26, 30, 44))
        d.rounded_rectangle((x0 + 18, y0 + 24, x0 + 66, y0 + 50), 5, outline=(255, 90, 80), width=3)
        d.rectangle((x0 + 66, y0 + 31, x0 + 71, y0 + 43), fill=(255, 90, 80)); d.rectangle((x0 + 22, y0 + 28, x0 + 30, y0 + 46), fill=(255, 90, 80))
        d.text((x0 + 86, y0 + 28), 'Controller battery low', font=F(600, 26), fill=UI_TXT, anchor='lm')
        d.text((x0 + 86, y0 + 58), 'Charge your controller', font=F(400, 21), fill=UI_DIM, anchor='lm')
    return im


def home_screen(s):
    im = ui_bg(); d = ImageDraw.Draw(im)
    d.text((34, 40), 'Games', font=F(600, 26), fill=UI_TXT, anchor='lm')
    d.text((130, 40), 'Media', font=F(500, 26), fill=UI_DIM, anchor='lm')
    icons = [('search', SW - 150), ('gear', SW - 100), ('user', SW - 50)]
    for name, x in icons:
        if s.get('sel') == name:
            d.ellipse((x - 24, 16, x + 24, 64), outline=(245, 248, 255), width=3, fill=(44, 62, 108))
        if name == 'gear':
            pts = [(x + (12 if k % 2 == 0 else 9) * math.cos(k * math.pi / 8), 40 + (12 if k % 2 == 0 else 9) * math.sin(k * math.pi / 8)) for k in range(16)]
            d.polygon(pts, fill=UI_TXT); d.ellipse((x - 4, 36, x + 4, 44), fill=UI_BG)
        elif name == 'search':
            d.ellipse((x - 10, 30, x + 6, 46), outline=UI_TXT, width=3); d.line([(x + 4, 44), (x + 11, 51)], fill=UI_TXT, width=3)
        else:
            d.ellipse((x - 14, 26, x + 14, 54), fill=(120, 160, 230))
    cols = [(230, 90, 80), (90, 170, 230), (250, 190, 60), (120, 200, 130), (170, 120, 220)]
    for i, c in enumerate(cols):
        sz = 150 if i == 0 else 104
        x = 40 + (0 if i == 0 else 170 + (i - 1) * 120); y = 110
        d.rounded_rectangle((x, y, x + sz, y + sz), 18, fill=c)
    d.text((40, 300), 'Play', font=F(600, 24), fill=UI_TXT, anchor='lm')
    return im


def list_rows(d, items, x0, x1, y0, rh, sel, size=22, dim=None):
    for i, it in enumerate(items):
        y = y0 + i * rh
        if sel == i:
            sel_box(d, (x0 - 10, y - rh / 2 + 4, x1, y + rh / 2 - 4))
        elif dim == i:
            d.rounded_rectangle((x0 - 10, y - rh / 2 + 4, x1, y + rh / 2 - 4), 10, fill=(34, 46, 80))
        d.text((x0 + 6, y), it, font=F(500, size), fill=UI_TXT, anchor='lm')


def settings_screen(s):
    im = ui_bg(); d = ImageDraw.Draw(im)
    d.text((40, 44), 'Settings', font=F(600, 36), fill=UI_TXT, anchor='lm')
    list_rows(d, SETTINGS, 60, 620, 104, 54, s.get('sel'), size=28)
    return im


def system_screen(s):
    im = ui_bg(); d = ImageDraw.Draw(im)
    d.text((40, 44), 'System', font=F(600, 36), fill=UI_TXT, anchor='lm')
    left = s.get('left', 0)
    list_rows(d, SYS_LEFT, 40, 300, 108, 60, left if s.get('pane') == 'left' else None, size=25,
              dim=left if s.get('pane') == 'right' else None)
    d.line([(316, 80), (316, SH - 30)], fill=(54, 66, 100), width=2)
    right = POWER_RIGHT if left == 1 else ['System Software Update and Settings', 'Console Information']
    list_rows(d, right, 336, 836, 108, 70, s.get('right') if s.get('pane') == 'right' else None, size=22)
    return im


def restfeat_screen(s):
    im = ui_bg(); d = ImageDraw.Draw(im)
    d.text((40, 44), 'Features Available in Rest Mode', font=F(600, 34), fill=UI_TXT, anchor='lm')
    rows = [('Supply Power to USB Ports', s.get('usb', 'Off')), ('Stay Connected to the Internet', 'on'),
            ('Enable Turning On Console from Network', 'on')]
    for i, (lab, val) in enumerate(rows):
        y = 124 + i * 74
        if s.get('sel') == i and not s.get('picker') is not None:
            sel_box(d, (36, y - 30, 816, y + 30))
        elif s.get('sel') == i:
            d.rounded_rectangle((36, y - 30, 816, y + 30), 10, fill=(34, 46, 80))
        d.text((56, y), lab, font=F(500, 27), fill=UI_TXT, anchor='lm')
        if val == 'on':
            d.rounded_rectangle((738, y - 14, 790, y + 14), 14, fill=LBLUE); d.ellipse((764, y - 11, 786, y + 11), fill=(255, 255, 255))
        else:
            d.text((796, y), val, font=F(600, 27), fill=(255, 210, 120) if val != 'Off' else UI_DIM, anchor='rm')
    if s.get('picker') is not None:
        x0, y0, x1, y1 = 480, 96, 840, 96 + 96 * 4 + 20
        d.rounded_rectangle((x0 + 6, y0 + 8, x1 + 6, y1 + 8), 16, fill=(4, 6, 14))
        d.rounded_rectangle((x0, y0, x1, y1), 16, fill=(28, 38, 70), outline=(70, 90, 140), width=2)
        for i, it in enumerate(PICK):
            y = y0 + 58 + i * 96
            if s['picker'] == i:
                sel_box(d, (x0 + 14, y - 40, x1 - 14, y + 40))
            on = s.get('usb', 'Off') == it
            d.ellipse((x0 + 32, y - 15, x0 + 62, y + 15), outline=UI_TXT, width=3)
            if on:
                d.ellipse((x0 + 39, y - 8, x0 + 55, y + 8), fill=LBLUE)
            d.text((x0 + 80, y - (10 if it == 'Adaptive' else 0)), it, font=F(600, 30), fill=UI_TXT, anchor='lm')
            if it == 'Adaptive':
                d.text((x0 + 80, y + 20), 'newer models', font=F(400, 20), fill=UI_DIM, anchor='lm')
    return im


def power_menu(im, sel):
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 230, 200, 640, 200 + 66 * 3 + 76
    d.rounded_rectangle((x0 + 6, y0 + 8, x1 + 6, y1 + 8), 16, fill=(4, 6, 14))
    d.rounded_rectangle((x0, y0, x1, y1), 16, fill=(28, 38, 70), outline=(70, 90, 140), width=2)
    d.text((x0 + 24, y0 + 36), 'Power', font=F(600, 30), fill=UI_TXT, anchor='lm')
    list_rows(d, POWER_MENU, x0 + 30, x1 - 16, y0 + 100, 66, sel, size=27)


_scache = {}


def render_screen(s):
    key = repr(sorted(s.items()))
    if key in _scache:
        return _scache[key].copy()
    if len(_scache) > 30:
        _scache.clear()
    v = s['view']
    if v == 'off':
        im = Image.new('RGB', (SW, SH), (8, 10, 16))
        ImageDraw.Draw(im).polygon([(SW * .55, 0), (SW * .75, 0), (SW * .35, SH), (SW * .15, SH)], fill=(16, 19, 28))
    else:
        im = {'game': game_screen, 'home': home_screen, 'settings': settings_screen, 'system': system_screen,
              'restfeat': restfeat_screen}[v](s)
    if s.get('power') is not None:
        power_menu(im, s['power'])
    _scache[key] = im.copy()
    return im


# ================================================================== timeline
class TL(wv.TL):
    def __init__(s):
        super().__init__()
        s.cur['scr'] = dict(view='game', notif=False)
        s.cur['rig'] = dict(light='white', ctl='blue', batt=.62, chg=False, cable=False, btn=None, gauge=False)

    def rig(s, **kw):
        s.cur['rig'].update(kw)

    def press(s, name, after=None, n=4):
        x, y = BTN[name]
        s.hand_to(x, y, n)
        s.cur['hand']['p'] = True; s.rig(btn=name); s.sound('tap')
        s.fx.append(('ring', s.f, x, y))
        if after:
            after()
        s.hold(2)
        s.cur['hand']['p'] = False; s.rig(btn=None)
        s.snap()


def build():
    t = TL()
    t.fx.append(('title', 0, 86)); t.hold(92)
    # props in (TV from the top, console + controller from the bottom)
    t.sound('whoosh')
    for i in range(1, 8):
        e = ease(i / 7)
        t.cur['mon_dy'] = -1500 * (1 - e) + (24 if i == 6 else 0)
        t.cur['kb_dy'] = 900 * (1 - ease(max(0, i - 1) / 6)) + (-20 if i == 7 else 0)
        t.snap()
    t.cur['kb_dy'] = 0; t.cur['mon_dy'] = 0; t.hold(3)
    # ---- problem: low battery mid-game
    t.cap('FIG. 00  /  THE PROBLEM', 'Controller dead again, mid-game?'); t.hold(6)
    t.rig(gauge=True)
    for lv in (.5, .35, .2, .1):
        t.rig(batt=lv); t.hold(3)
    t.scr(notif=True); t.sound('pop')
    t.fx.append(('burst', t.f, 860, 640, 0)); t.sound('knock')
    for k in range(4):
        t.rig(ctl='off' if k % 2 == 0 else 'blue'); t.hold(3)
    t.rig(ctl='blue'); t.hold(6)
    t.cap('FIG. 00  /  THE FIX', 'Let the PS5 charge it while it sleeps'); t.hold(30)
    # ---- step 1: Settings > System
    t.cap('FIG. 01  /  STEP 1 OF 3', 'Go to Settings > System'); t.hold(8)
    t.scr(view='home', notif=False, sel='user'); t.sound('swish'); t.hold(4)
    t.press('dpad_u', after=lambda: t.scr(sel='gear'))
    t.hold(3)
    t.press('ok', after=lambda: (t.scr(view='settings', sel=0), t.sound('swish')))
    for i in range(1, 5):
        t.press('dpad_d', after=lambda i=i: t.scr(sel=i), n=3)
    t.hold(3)
    t.press('ok', after=lambda: (t.scr(view='system', sel=None, pane='left', left=0, right=0), t.sound('swish')))
    t.hold(6)
    # ---- step 2: Power Saving > Features Available in Rest Mode
    t.cap('FIG. 02  /  STEP 2 OF 3', 'Power Saving > Features Available in Rest Mode'); t.hold(8)
    t.press('dpad_d', after=lambda: t.scr(left=1))
    t.hold(3)
    t.press('dpad_r', after=lambda: t.scr(pane='right', right=0))
    t.press('dpad_d', after=lambda: t.scr(right=1), n=3)
    t.hold(3)
    t.press('ok', after=lambda: (t.scr(view='restfeat', pane=None, left=None, right=None, sel=0, usb='Off'), t.sound('swish')))
    t.hold(6)
    # ---- step 3: Supply Power to USB Ports > 3 Hours
    t.cap('FIG. 03  /  STEP 3 OF 3', 'Supply Power to USB Ports: 3 Hours'); t.hold(8)
    t.press('ok', after=lambda: (t.scr(picker=0), t.sound('pop')))
    t.hold(3)
    t.press('dpad_d', after=lambda: t.scr(picker=1))
    t.hold(3)
    t.press('ok', after=lambda: (t.scr(usb='3 Hours', picker=None), t.sound('ding')))
    t.hand_out(3)
    t.cap('RESULT  /  OK', 'USB ports now stay powered in Rest Mode'); t.hold(30)
    # ---- field test: plug in, enter rest mode, watch it charge
    t.cap('FIG. 04  /  FIELD TEST', 'Plug it in, then enter Rest Mode'); t.hold(6)
    t.rig(cable=True); t.sound('paper'); t.hold(8)
    t.press('home', after=lambda: (t.scr(power=0), t.sound('pop')))
    t.hold(6)
    t.press('ok', after=lambda: (t.scr(view='off', power=None), t.rig(light='orange', ctl='orange', chg=True), t.sound('whoosh')))
    t.hand_out(3)
    lv = .1
    for k in range(18):
        lv = min(1.0, .1 + .9 * ease((k + 1) / 18))
        pulse = 'orange' if k % 4 < 2 else 'orange_lo'
        t.rig(batt=lv, light=pulse, ctl=pulse); t.snap()
    t.rig(chg=False, light='orange', ctl='off'); t.sound('ding')
    t.fx.append(('burst', t.f, 840, 1300, 1)); t.hold(16)
    # ---- bonus: Adaptive on newer models
    t.cap('APPENDIX  /  BONUS', 'Newer PS5? Choose Adaptive to save power'); t.hold(4)
    t.rig(light='white', ctl='blue')
    t.scr(view='restfeat', sel=0, usb='3 Hours', picker=1); t.sound('swish'); t.hold(6)
    t.press('dpad_d', after=lambda: t.scr(picker=2), n=5)
    t.press('dpad_d', after=lambda: t.scr(picker=3), n=3)
    t.hold(3)
    t.press('ok', after=lambda: (t.scr(usb='Adaptive', picker=None), t.sound('ding')))
    t.fx.append(('burst', t.f, 300, 640, 2)); t.hand_out(3); t.hold(20)
    # ---- end
    t.cap_off()
    t.rig(gauge=False)
    t.sound('whoosh')
    for i in range(1, 6):
        e = ease(i / 5); t.cur['mon_dy'] = -1600 * e; t.cur['kb_dy'] = 1000 * e; t.snap()
    t.fx.append(('end', t.f)); t.hold(72)
    return t


# ================================================================== render
P = {}
TLD = None


def vellum_controller():
    w, h = 420, 330
    im = Image.new('RGBA', (w, h), (230, 240, 255, 70))
    d = ImageDraw.Draw(im)
    C = th.CHALK + (255,)
    d.ellipse((30, 110, 170, 290), outline=C, width=5); d.ellipse((250, 110, 390, 290), outline=C, width=5)
    d.rounded_rectangle((60, 70, 360, 220), 60, outline=C, width=5)
    d.rounded_rectangle((160, 80, 260, 130), 10, outline=C, width=4)
    d.line([(210, 70), (210, 40), (330, 20)], fill=C, width=5)
    d.rounded_rectangle((320, 6, 360, 34), 6, fill=C)
    d.polygon([(214, 150), (190, 196), (208, 196), (198, 236), (236, 180), (216, 180), (230, 150)], fill=YEL + (255,))
    for k, (ox, oy) in enumerate([(0, -20), (-20, 0), (20, 0), (0, 20)]):
        d.ellipse((300 + ox - 9, 150 + oy - 9, 300 + ox + 9, 150 + oy + 9), outline=C, width=3)
    d.line([(100, 150), (140, 150)], fill=C, width=5); d.line([(120, 130), (120, 170)], fill=C, width=5)
    sp = th.sprite(im, border=0, off=(6, 9), blur=6, op=.3, tex=False)
    return rotate_sprite(sp, -6)


def init_props():
    P['bg'] = th.bg_blue(with_dims=False)
    P['mon'] = th.sprite(monitor_raw(), border=8, off=(16, 22), blur=14, op=.42)
    P['hand'] = {'hover': th.hand_sprite('blue', press=False), 'press': th.hand_sprite('blue', press=True)}
    P['rings'] = [dashed_ring(r, YEL, w) for r, w in [(30, 8), (50, 7), (70, 5)]]
    P['notes'] = {}
    P['console'] = {}
    P['ctl'] = {}
    P['gauge'] = {}
    P['bursts'] = [label('LOW BATTERY!', th.JB(800, 56), tape=True, rot=-8, padx=28, pady=12),
                   label('CHARGED!', th.JB(800, 64), bg=YEL, tape=True, rot=7, padx=30, pady=12),
                   label('SAVES POWER', th.JB(800, 52), bg=YEL, tape=True, rot=-6, padx=26, pady=12)]
    # title
    P['tiles'] = [rotate_sprite(th.stencil_letter(ch, PAPER if i < 4 else YEL), rng_for('rm', i).uniform(-4, 4))
                  for i, ch in enumerate('RESTMODE')]
    P['t_label'] = label('SPEC // console tip', th.JB(700, 34), fg=MID, rot=-2, padx=30, pady=16)
    P['t_s1'] = center_label('CONTROLLER DEAD AGAIN?', th.JB(800, 44), rot=1.5)
    P['t_s1b'] = center_label('CHARGE IT WHILE THE PS5 SLEEPS', th.JB(800, 40), rot=-1)
    P['t_s2'] = center_label('USB power in rest mode', th.JB(700, 40), bg=YEL, rot=-2)
    P['t_phone'] = vellum_controller()
    P['t_burst'] = label(['PS5', 'ALL MODELS'], th.JB(800, 36), rot=6, padx=26, pady=16)
    # end
    P['e_head'] = center_label('SAVE THIS TIP', th.JB(800, 92), rot=-2.5, padx=56, pady=30)
    P['e_chips'] = [rotate_sprite(path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('Settings', (90, 90, 100), 'gear', -2), ('System', (40, 70, 140), 'grid', 1.5), ('Power Saving', (16, 140, 100), 'batt', -1.5),
        ('USB: 3 Hours', NAVY, 'dot', 2)])]
    P['e_arrows'] = [chalk_arrow(r) for r in (14, -14, 14)]
    P['e_s1'] = center_label('PLUG IN, THEN REST MODE', th.JB(800, 44), bg=YEL, rot=-1.5)
    P['e_s2'] = center_label('ADAPTIVE ON NEWER MODELS', th.JB(800, 44), rot=1.5)
    P['e_s3'] = center_label('works on every PS5 console', th.JB(600, 34), fg=MID, rot=-1, pady=18)
    P['e_follow'] = center_label('FOLLOW  TECH WALL', th.JB(800, 40), bg=YEL, rot=1, pady=18)


wv.P = P
put = wv.put
draw_caps = wv.draw_caps


def draw_title(cv, f, a, ex):
    els = [('t_label', 540, 370, a + 1, 0)]
    for i in range(4):
        els.append((i, 540 + (i - 1.5) * 170, 560, a + 4 + 2 * i, i % 3))
    for i in range(4):
        els.append((4 + i, 540 + (i - 1.5) * 170, 770, a + 12 + 2 * i, i % 3))
    els += [('t_s1', 540, 950, a + 22, 0), ('t_s1b', 540, 1050, a + 25, 1), ('t_s2', 520, 1170, a + 28, 2),
            ('t_phone', 520, 1450, a + 31, 0), ('t_burst', 840, 1660, a + 34, 1)]
    for key, x, y, ap, stg in els:
        yy = m.drop_y(f, ap, y, ex, stg)
        if yy is None:
            continue
        sp = P['tiles'][key] if isinstance(key, int) else P[key]
        put(cv, sp, x, yy, f, ('t', key))


def draw_end(cv, f, a):
    wv.draw_end(cv, f, a)
    yy = m.drop_y(f, a + 36, 1770)
    if yy is not None:
        put(cv, P['e_follow'], 600, yy, f, 'e_follow')


def cable(cv, dy, f):
    d = ImageDraw.Draw(cv)
    jx, jy = jit(f, 'cable', 1.0)
    pts = []
    x0, y0 = CON_X - 160 + 46 + jx, CON_Y - 85 + 136 + dy + jy          # console USB port
    x1, y1 = CTL_X + jx, CTL_Y - 150 + dy + jy                          # top of controller
    for k in range(21):
        t = k / 20
        x = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * (x0 + 40) + 3 * (1 - t) * t * t * (x1 - 120) + t ** 3 * x1
        y = (1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * (y0 + 190) + 3 * (1 - t) * t * t * (y1 - 160) + t ** 3 * y1
        pts.append((x, y))
    d.line(pts, fill=(18, 20, 28), width=11, joint='curve')
    d.line(pts, fill=(60, 64, 78), width=7, joint='curve')


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
    rg = st['rig']
    dy = st['kb_dy']
    if dy < 850:
        k = rg['light']
        if k not in P['console']:
            P['console'][k] = th.sprite(console_raw(k), border=8, off=(12, 18), blur=12, op=.42)
        jx, jy = jit(f, 'console', 1.2)
        draw_sprite(cv, P['console'][k], CON_X + jx, CON_Y + dy + jy)
        if rg['cable']:
            cable(cv, dy, f)
        k = (rg['ctl'], rg['btn'])
        if k not in P['ctl']:
            P['ctl'][k] = th.sprite(controller_raw(*k), border=8, off=(12, 18), blur=12, op=.42)
        jx, jy = jit(f, 'ctl', 1.2)
        draw_sprite(cv, P['ctl'][k], CTL_X + jx, CTL_Y + dy + jy)
        if rg['gauge']:
            k = (round(rg['batt'], 2), rg['chg'])
            if k not in P['gauge']:
                P['gauge'][k] = gauge_raw(*k)
            put(cv, P['gauge'][k], GAUGE[0], GAUGE[1] + dy, f, 'gauge')
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
    for e in tl['fx']:
        k = f - e[1]
        if e[0] == 'ring' and 0 <= k < 3:
            put(cv, P['rings'][k], e[2], e[3], f, 'ring', .5)
        elif e[0] == 'burst' and 0 <= k < 12:
            sc = {0: 0.5, 1: 1.08}.get(k, 1.0)
            sp = P['bursts'][e[4]]
            if sc != 1.0:
                sp = tuple(s_.resize((int(s_.width * sc), int(s_.height * sc)), Image.BILINEAR) for s_ in sp)
            put(cv, sp, e[2], e[3], f, ('burst', e[1]))
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
            for ap in [a + 1] + [a + 4 + 2 * i for i in range(4)] + [a + 12 + 2 * i for i in range(4)] + [a + 22, a + 25, a + 28, a + 31, a + 34]:
                t.snd.append((ap, 'pop'))
            t.snd.append((e[2] + 1, 'whoosh'))
        if e[0] == 'end':
            a = e[1]
            for ap in [a + 2] + [a + 6 + 4 * i for i in range(4)] + [a + 24, a + 28, a + 32, a + 36]:
                t.snd.append((ap, 'pop'))
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))


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
            if f < n:
                render(f)
    else:
        with Pool(2) as pool:
            for i, _ in enumerate(pool.imap(render, range(n), chunksize=8)):
                if i % 100 == 0:
                    print('rendered', i, flush=True)
        m.make_audio(TLD, n, __import__('lib').out('audio_restmode.wav'))

"""Tech Wall — AI tip: translate anything with your camera (Google Lens), result-first (~25 s).
Frame 0 shows the payoff (a Spanish menu already shown in English through the camera) with the hook, then
"here's how": Google app -> Lens icon -> Translate -> point at text, and a gallery-photo bonus.
Screens are generic look-alikes (no logos); the phone and screen helpers come from android.py, timeline from rf_demo.py.
Build:  ./build.sh lens
"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import android as A
from android import BG, SURF, TXT, SUB, ACC, android_phone_raw, spec
from screens import SW, SH
from lib import F, rotate_sprite
import movie as m
import movie_blue as mb
import themes as th

EP = 'lens'
OUT = __import__('lib').out(f'frames_{EP}')
mb.OUT = OUT
NAVY, MID, YEL, PAPER = mb.NAVY, mb.MID, mb.YEL, mb.PAPER
MENU = [('MENÚ', 'MENU', None), ('Sopa del día', 'Soup of the day', '6 €'), ('Pollo asado', 'Roast chicken', '12 €'),
        ('Tarta de queso', 'Cheesecake', '5 €'), ('Agua con gas', 'Sparkling water', '2 €')]
SIGN = [('SALIDA', 'EXIT'), ('Cuidado: piso mojado', 'Caution: wet floor')]
WHITE, DIM = (245, 245, 250), (150, 150, 160)


# ======================================================================= screens
def arrow(d, x0, x1, y, col, w=3):
    d.line([(x0, y), (x1, y)], fill=col, width=w)
    d.polygon([(x1 + 2, y), (x1 - 9, y - 7), (x1 - 9, y + 7)], fill=col)


def lens_icon(d, cx, cy, col, s=1.0):
    r = 16 * s
    d.rounded_rectangle((cx - r, cy - r, cx + r, cy + r), int(7 * s), outline=col, width=max(2, int(3 * s)))
    d.ellipse((cx - 6 * s, cy - 6 * s, cx + 6 * s, cy + 6 * s), outline=col, width=max(2, int(3 * s)))
    d.ellipse((cx + 7 * s, cy + 7 * s, cx + 12 * s, cy + 12 * s), fill=col)


def overlay_text(d, box, text, font, align='l'):
    """Lens-style: paint over the original words with the paper colour, write the translation on top"""
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 6, fill=(250, 246, 236))
    tx = x0 + 6 if align == 'l' else (x0 + x1) / 2
    d.text((tx, (y0 + y1) / 2), text, font=font, fill=(20, 24, 40), anchor='lm' if align == 'l' else 'mm')


def lens_content(ov, hl):
    im = Image.new('RGB', (SW, SH))
    d = ImageDraw.Draw(im)
    for y in range(SH):
        t = y / SH
        d.line([(0, y), (SW, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip((92, 78, 66), (52, 44, 38))))
    rows = {}
    n = ov.get('n', 0)
    if ov.get('photo'):
        # bonus: a photo of a sign picked from the gallery
        d.rectangle((40, 250, SW - 40, 880), fill=(205, 210, 214))
        d.rounded_rectangle((90, 330, SW - 90, 520), 18, fill=(30, 140, 80))
        d.rounded_rectangle((110, 520, SW - 110, 720), 14, fill=(250, 214, 60))
        big, small = F(600, 64), F(500, 30)
        if n >= 1:
            overlay_text(d, (130, 380, SW - 130, 470), SIGN[0][1], big, 'c')
        else:
            d.text((SW / 2, 425), SIGN[0][0], font=big, fill=(255, 255, 255), anchor='mm')
        if n >= 2:
            overlay_text(d, (130, 590, SW - 130, 650), SIGN[1][1], small, 'c')
        else:
            d.text((SW / 2, 620), SIGN[1][0], font=small, fill=(30, 30, 30), anchor='mm')
    else:
        sh = Image.new('L', im.size, 0)
        ImageDraw.Draw(sh).rectangle((70, 248, 512, 880), fill=140)
        im.paste((20, 16, 12), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
        d = ImageDraw.Draw(im)
        d.rectangle((56, 230, 500, 862), fill=(246, 240, 226))
        d.line([(86, 330), (470, 330)], fill=(190, 170, 140), width=2)
        for i, (es, en, price) in enumerate(MENU):
            y = 284 if i == 0 else 330 + i * 110 - 50
            font = F(600, 46) if i == 0 else F(500, 31)
            if i == 0:
                if n > 0:
                    overlay_text(d, (SW / 2 - 90, y - 32, SW / 2 + 90, y + 32), en, font, 'c')
                else:
                    d.text((SW / 2 - 4, y), es, font=font, fill=(70, 40, 30), anchor='mm')
                continue
            if n > i:
                overlay_text(d, (82, y - 26, 82 + font.getlength(en) + 16, y + 26), en, font)
            else:
                d.text((88, y), es, font=font, fill=(70, 40, 30), anchor='lm')
            d.text((472, y), price, font=F(500, 29), fill=(70, 40, 30), anchor='rm')
        if ov.get('glow'):
            d.rectangle((50, 224, 506, 868), outline=YEL, width=6)
    # top bar
    d.line([(34, 108), (58, 132)], fill=WHITE, width=4); d.line([(34, 132), (58, 108)], fill=WHITE, width=4)
    d.text((SW / 2, 120), 'Lens', font=F(600, 32), fill=WHITE, anchor='mm')
    if ov.get('tab') == 'translate':
        d.rounded_rectangle((110, 160, SW - 110, 212), 26, fill=(250, 250, 252))
        d.text((175, 186), 'Spanish', font=F(600, 24), fill=TXT, anchor='lm')
        arrow(d, 285, 315, 186, ACC)
        d.text((330, 186), 'English', font=F(600, 24), fill=ACC, anchor='lm')
    # bottom panel: modes, shutter, gallery
    d.rectangle((0, 930, SW, SH), fill=(24, 24, 28))
    for name, label, x in (('translate', 'Translate', 120), ('search', 'Search', 280), ('homework', 'Homework', 440)):
        on = ov.get('tab', 'search') == name
        if on:
            d.rounded_rectangle((x - 78, 948, x + 78, 994), 23, fill=(64, 66, 76))
        if hl == f'tab_{name}':
            d.rounded_rectangle((x - 78, 948, x + 78, 994), 23, outline=YEL, width=3)
        d.text((x, 971), label, font=F(600 if on else 500, 25), fill=WHITE if on else DIM, anchor='mm')
        rows[f'tab_{name}'] = (x - 78, 948, x + 78, 994)
    d.ellipse((SW / 2 - 46, 1030, SW / 2 + 46, 1122), outline=WHITE, width=6)
    d.ellipse((SW / 2 - 34, 1042, SW / 2 + 34, 1110), fill=(235, 235, 240))
    d.rounded_rectangle((60, 1046, 120, 1106), 12, fill=(120, 140, 160) if hl != 'gallery' else YEL)
    d.polygon([(66, 1100), (86, 1074), (100, 1090), (108, 1080), (116, 1100)], fill=(70, 150, 90))
    rows['gallery'] = (60, 1046, 120, 1106)
    return im, rows


def google_content(ov, hl):
    im = Image.new('RGB', (SW, SH), (255, 255, 255))
    d = ImageDraw.Draw(im); rows = {}
    d.ellipse((SW - 84, 100, SW - 40, 144), fill=(66, 133, 244))
    d.text((SW - 62, 122), 'R', font=F(600, 24), fill=(255, 255, 255), anchor='mm')
    d.text((SW / 2, 330), 'Search', font=F(600, 64), fill=(60, 64, 72), anchor='mm')
    y = 420
    d.rounded_rectangle((30, y, SW - 30, y + 84), 42, fill=SURF, outline=(220, 220, 228), width=2)
    d.ellipse((58, y + 28, 84, y + 54), outline=SUB, width=4); d.line([(80, y + 50), (90, y + 60)], fill=SUB, width=4)
    d.text((108, y + 42), 'Search', font=F(400, 28), fill=SUB, anchor='lm')
    d.rounded_rectangle((SW - 150, y + 24, SW - 136, y + 52), 7, outline=SUB, width=3)
    d.arc((SW - 156, y + 36, SW - 130, y + 62), 0, 180, fill=SUB, width=3)
    if hl == 'lens':
        d.ellipse((SW - 104, y + 10, SW - 40, y + 74), fill=HLY)
    lens_icon(d, SW - 72, y + 42, ACC, 1.0)
    rows['lens'] = (SW - 104, y + 10, SW - 40, y + 74)
    for i, (lab, col) in enumerate([('Translate', (66, 133, 244)), ('Song', (234, 67, 53)), ('Weather', (251, 188, 5))]):
        x = 40 + i * 170
        d.rounded_rectangle((x, 560, x + 150, 620), 30, fill=SURF)
        d.ellipse((x + 16, 576, x + 44, 604), fill=col)
        d.text((x + 56, 590), lab, font=F(500, 23), fill=TXT, anchor='lm')
    return im, rows


HLY = (255, 236, 160)
A.BUILDERS.update({'x_lens': lens_content, 'x_google': google_content})
_aview = A.aview


def aview(sp):
    if sp['name'] == 'x_lens':
        content, _ = A.screen_content(sp['name'], sp.get('ov'), sp.get('hl'))
        v = content.copy(); A.status_bar(v, True); return v
    if sp['name'] == 'x_google':
        content, _ = A.screen_content(sp['name'], sp.get('ov'), sp.get('hl'))
        v = content.copy(); A.status_bar(v, False); return v
    return _aview(sp)


A.aview = aview


def row_point(sp, rid, fx=0.5):
    _, rows = A.screen_content(sp['name'], sp.get('ov'), sp.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    return x0 + (x1 - x0) * fx, (y0 + y1) / 2 - sp.get('scroll', 0)


m.row_point = row_point


# ======================================================================= timeline
def fig_head(badge):
    if badge.isdigit():
        return f"HERE'S HOW  /  STEP {badge} OF 3"
    return {'H': 'TECH WALL  /  AI TIP', 'ok': 'RESULT  /  OK', '+': 'BONUS'}[badge]


mb.fig_head = fig_head
ALL = len(MENU)


def build():
    t = m.TL()
    # 0:00 — result first: the menu is already in English
    mb.result_first(t, spec('x_lens', ov={'tab': 'translate', 'n': ALL, 'glow': True}), 'H', 'READ ANY MENU IN ANY LANGUAGE')
    t.hold(16)
    # proof: move the phone, the Spanish shows for a moment, English snaps back
    sp = t.ph['spec']
    for dx, n in ((-14, 0), (10, 0), (0, 2), (0, ALL)):
        t.ph['x'] = 540 + dx; sp['ov'] = {'tab': 'translate', 'n': n}; t.snap(); t.snap()
    t.ph['x'] = 540
    t.fx.append(('burst', t.f, 820, 700, 0)); t.sound('ding')
    t.hold(16)
    # 0:02 — here's how
    t.cap('1', "Here's how: Google app, tap the Lens icon", m.MINT)
    t.navigate(spec('x_google'), back=True)
    t.hold(10)
    t.tap('lens', nav=spec('x_lens', ov={'tab': 'search', 'n': 0}), n_move=4)
    t.hand_out(3)
    t.hold(5)
    t.cap('2', 'Swipe to Translate', m.SKY)
    t.hold(10)
    t.tap('tab_translate', ov={'tab': 'translate', 'n': 0}, n_move=4)
    t.hand_out(3)
    t.cap('3', 'Point your camera at text', m.PEACH)
    t.hold(8)
    for n in range(1, ALL + 1):
        t.ph['spec']['ov'] = {'tab': 'translate', 'n': n}; t.sound('pop'); t.hold(5)
    t.cap('ok', 'Signs and labels work too', m.MINT)
    t.ph['spec']['ov'] = {'tab': 'translate', 'n': ALL, 'glow': True}
    t.hold(26)
    # bonus: translate a photo you already took
    t.cap('+', 'Old photo? Tap the gallery and translate it', m.SKY)
    t.ph['spec']['ov'] = {'tab': 'translate', 'n': ALL}
    t.hold(10)
    t.tap('gallery', ov={'tab': 'translate', 'n': 0, 'photo': True}, n_move=4)
    t.hand_out(3)
    for n in (1, 2):
        t.ph['spec']['ov'] = {'tab': 'translate', 'n': n, 'photo': True}; t.sound('pop'); t.hold(6)
    t.fx.append(('burst', t.f, 800, 760, 1))
    t.hold(22)
    mb.end_card(t)
    return t


# ======================================================================= props
def init_props():
    mb.init_props()
    P = m.P
    P['front'] = th.sprite(android_phone_raw(), border=8, off=(16, 22), blur=14, op=.4)
    P['bursts'] = [mb.label('TRANSLATED!', th.JB(800, 58), bg=YEL, tape=True, rot=-7, padx=28, pady=12),
                   mb.label('EVEN PHOTOS!', th.JB(800, 56), tape=True, rot=6, padx=28, pady=12)]
    P['e_chips'] = [rotate_sprite(mb.path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('Google app', (66, 133, 244), 'zoom', -2), ('Lens icon', (90, 90, 100), 'cam', 1.5),
        ('Translate', (52, 168, 83), 'dot', -1.5), ('Point at text', NAVY, 'touch', 2)])]
    P['e_s1'] = mb.center_label('WORKS ON PHOTOS TOO', th.JB(800, 46), bg=YEL, rot=-1.5)
    P['e_s2'] = mb.center_label('ANDROID & iPHONE', th.JB(800, 46), rot=1.5)
    P['e_s3'] = mb.center_label('100+ languages · Google app or Translate app', th.JB(600, 31), fg=MID, rot=-1, pady=18)


if __name__ == '__main__':
    t = build()
    for e in t.fx:
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))
    mb.finish(t, EP, init_props)

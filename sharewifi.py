"""Tech Wall ep.5 — Share Wi-Fi with a QR code on Android — Blueprint stop-motion"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter
import qrcode
import android as A
from android import (BG, SURF, TXT, SUB, ACC, ACC_L, HLC, ROWH, arrow_back, mswitch, app_icon, list_rows, notif_card,
                     android_phone_raw, spec)
from screens import SW, SH, glyph
from lib import F, rotate_sprite, rng_for, FPS, ease, apply_tex, draw_sprite, jit
import movie as m
import movie_blue as mb
import themes as th

OUT = __import__('lib').out('frames_sharewifi')
mb.OUT = OUT
NAVY, MID, YEL, PAPER = mb.NAVY, mb.MID, mb.YEL, mb.PAPER
PASSWORD = 'SunnyDays2024'
A.NOTIFS['guest'] = ('Messages', (30, 160, 90), 'msg', 'Sam', "What's the Wi-Fi password??")


def qr_img(size):
    q = qrcode.QRCode(border=0, box_size=1, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(f'WIFI:T:WPA;S:Home;P:{PASSWORD};;'); q.make()
    mtx = q.get_matrix(); n = len(mtx)
    im = Image.new('RGB', (n, n), (255, 255, 255))
    px = im.load()
    for y in range(n):
        for x in range(n):
            if mtx[y][x]:
                px[x, y] = (20, 20, 26)
    return im.resize((size, size), Image.NEAREST)


QR = None


def wifi_icon(d, cx, cy, col, s=1.0):
    for r_ in (26 * s, 17 * s, 8 * s):
        d.arc((cx - r_, cy - r_ + 8 * s, cx + r_, cy + r_ + 8 * s), 225, 315, fill=col, width=max(2, int(4 * s)))
    d.ellipse((cx - 4 * s, cy + 5 * s, cx + 4 * s, cy + 13 * s), fill=col)


def gear(d, cx, cy, r_, col):
    import math
    pts = []
    for i in range(32):
        a = i * math.pi / 16
        rr = r_ if (i // 2) % 2 == 0 else r_ * .74
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)
    d.ellipse((cx - r_ * .36, cy - r_ * .36, cx + r_ * .36, cy + r_ * .36), fill=BG)


def header(d, title, rows):
    arrow_back(d, 34, 132); rows['back'] = (20, 100, 100, 164)
    d.text((32, 250), title, font=F(600, 50), fill=TXT, anchor='ls')


def net_content(ov, hl):
    im = Image.new('RGB', (SW, 1500), BG); d = ImageDraw.Draw(im); rows = {}
    header(d, 'Network & internet', rows)
    y = list_rows(d, 290, [
        ('internet', 'Internet', 'Home', (66, 133, 244), 'wifi'),
        ('calls', 'Calls & SMS', 'Default SIM', (52, 168, 83), 'dot'),
        ('sims', 'SIMs', 'Mobile network', (90, 90, 160), 'dot'),
        ('hotspot', 'Hotspot & tethering', 'Off', (230, 120, 30), 'dot'),
        ('saver', 'Data Saver', 'Off', (0, 150, 160), 'dot'),
        ('vpn', 'VPN', 'None', (150, 90, 210), 'dot'),
        ('dns', 'Private DNS', 'Automatic', (100, 104, 116), 'dot')], hl, rows)
    return im.crop((0, 0, SW, max(SH, y + 40))), rows


def inet_content(ov, hl):
    im = Image.new('RGB', (SW, 1500), BG); d = ImageDraw.Draw(im); rows = {}
    header(d, 'Internet', rows)
    y = 290
    d.rounded_rectangle((24, y, SW - 24, y + 100), 50, fill=ACC_L)
    d.text((56, y + 50), 'Wi-Fi', font=F(600, 30), fill=TXT, anchor='lm')
    mswitch(d, SW - 140, y + 50, True); y += 130
    # connected network
    if hl in ('home', 'home_gear'):
        d.rounded_rectangle((12, y, SW - 12, y + ROWH), 22, fill=HLC)
    wifi_icon(d, 60, y + ROWH / 2 - 6, ACC, 1.1)
    d.text((112, y + 40), 'Home', font=F(600, 30), fill=TXT, anchor='lm')
    d.text((112, y + 76), 'Connected', font=F(400, 23), fill=SUB, anchor='lm')
    d.line([(SW - 100, y + 24), (SW - 100, y + ROWH - 24)], fill=(210, 206, 216), width=2)
    gear(d, SW - 56, y + ROWH / 2, 22, SUB)
    rows['home'] = (12, y, SW - 12, y + ROWH); rows['home_gear'] = (SW - 96, y + 10, SW - 16, y + ROWH - 10)
    if ov.get('gearpulse'):
        d.ellipse((SW - 96, y + 16, SW - 16, y + ROWH - 16), outline=YEL, width=5)
    y += ROWH + 10
    for nm in ['Neighbor_2G', 'CoffeeShop', 'Office_5G']:
        wifi_icon(d, 60, y + ROWH / 2 - 6, SUB, 1.1)
        d.rounded_rectangle((70, y + ROWH / 2 + 2, 84, y + ROWH / 2 + 14), 3, fill=SUB)
        d.text((112, y + ROWH / 2), nm, font=F(500, 30), fill=TXT, anchor='lm')
        y += ROWH
    d.text((40, y + 30), '+  Add network', font=F(500, 28), fill=ACC, anchor='lm')
    return im.crop((0, 0, SW, max(SH, y + 80))), rows


def detail_content(ov, hl):
    im = Image.new('RGB', (SW, 1500), BG); d = ImageDraw.Draw(im); rows = {}
    arrow_back(d, 34, 132); rows['back'] = (20, 100, 100, 164)
    cx = SW / 2
    d.ellipse((cx - 56, 190, cx + 56, 302), fill=ACC_L)
    wifi_icon(d, cx, 238, ACC, 1.6)
    d.text((cx, 350), 'Home', font=F(600, 48), fill=TXT, anchor='mm')
    d.text((cx, 396), 'Connected', font=F(400, 26), fill=SUB, anchor='mm')
    btns = [('forget', 'Forget', 'trash'), ('disc', 'Disconnect', 'x'), ('share', 'Share', 'qr')]
    for i, (rid, lab, ic) in enumerate(btns):
        bx = 100 + i * 180; by = 470
        hlb = hl == rid
        d.rounded_rectangle((bx - 70, by - 40, bx + 70, by + 70), 26, fill=HLC if hlb else SURF)
        if ic == 'qr':
            for qx, qy in [(-16, -18), (8, -18), (-16, 6)]:
                d.rectangle((bx + qx, by + qy, bx + qx + 12, by + qy + 12), outline=ACC, width=3)
            d.rectangle((bx + 10, by + 8, bx + 18, by + 16), fill=ACC)
        elif ic == 'trash':
            d.rectangle((bx - 12, by - 12, bx + 12, by + 16), outline=ACC, width=3); d.line([(bx - 18, by - 14), (bx + 18, by - 14)], fill=ACC, width=3)
        else:
            d.line([(bx - 12, by - 12), (bx + 12, by + 12)], fill=ACC, width=4); d.line([(bx - 12, by + 12), (bx + 12, by - 12)], fill=ACC, width=4)
        d.text((bx, by + 44), lab, font=F(500, 22), fill=TXT, anchor='mm')
        rows[rid] = (bx - 70, by - 40, bx + 70, by + 70)
    if ov.get('sharepulse'):
        d.rounded_rectangle((460 - 76, 470 - 46, 460 + 76, 470 + 76), 30, outline=YEL, width=5)
    y = 590
    for t1, t2 in [('Signal strength', 'Excellent'), ('Frequency', '5 GHz'), ('Security', 'WPA2/WPA3-Personal'), ('Auto-connect', 'On')]:
        d.text((40, y + 36), t1, font=F(500, 29), fill=TXT, anchor='lm')
        d.text((40, y + 72), t2, font=F(400, 23), fill=SUB, anchor='lm'); y += ROWH
    if ov.get('verify'):
        sh = Image.new('L', im.size, 0); ImageDraw.Draw(sh).rectangle((0, 0, SW, im.height), fill=110)
        im.paste((0, 0, 0), (0, 0), sh)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 760, SW, 1220), 40, fill=(252, 250, 255))
        d.text((SW / 2, 830), "Confirm it's you", font=F(600, 34), fill=TXT, anchor='mm')
        d.text((SW / 2, 874), 'to share Wi-Fi', font=F(400, 24), fill=SUB, anchor='mm')
        fx, fy = SW / 2, 990
        ok = ov['verify'] == 'ok'
        col = (52, 168, 83) if ok else ACC
        d.ellipse((fx - 64, fy - 64, fx + 64, fy + 64), fill=(230, 244, 234) if ok else ACC_L)
        if ok:
            d.line([(fx - 26, fy + 2), (fx - 6, fy + 22), (fx + 30, fy - 20)], fill=col, width=8, joint='curve')
        else:
            for k, r_ in enumerate((14, 26, 38)):
                d.arc((fx - r_, fy - r_, fx + r_, fy + r_), 200 + k * 10, 520 - k * 10, fill=col, width=4)
        d.text((SW / 2, 1100), 'Touch the fingerprint sensor', font=F(400, 24), fill=SUB, anchor='mm')
    return im.crop((0, 0, SW, max(SH, 1240))), rows


def qr_content(ov, hl):
    global QR
    if QR is None:
        QR = qr_img(348)
    im = Image.new('RGB', (SW, 1500), BG); d = ImageDraw.Draw(im); rows = {}
    arrow_back(d, 34, 132); rows['back'] = (20, 100, 100, 164)
    d.text((SW / 2, 230), 'Share Wi-Fi', font=F(600, 46), fill=TXT, anchor='mm')
    d.text((SW / 2, 284), 'Scan this QR code to connect', font=F(400, 24), fill=SUB, anchor='mm')
    d.text((SW / 2, 316), 'to "Home"', font=F(400, 24), fill=SUB, anchor='mm')
    d.rounded_rectangle((SW / 2 - 200, 360, SW / 2 + 200, 760), 30, fill=(255, 255, 255), outline=(220, 216, 226), width=2)
    im.paste(QR, (int(SW / 2 - 174), 386))
    d.text((SW / 2, 812), 'Wi-Fi password: ' + PASSWORD, font=F(500, 26), fill=TXT, anchor='mm')
    rows['qr'] = (SW / 2 - 200, 360, SW / 2 + 200, 760)
    hlb = hl == 'quick'
    d.rounded_rectangle((SW / 2 - 150, 880, SW / 2 + 150, 950), 35, fill=(170, 190, 240) if hlb else ACC)
    d.text((SW / 2, 915), 'Quick Share', font=F(600, 28), fill=(255, 255, 255), anchor='mm')
    rows['quick'] = (SW / 2 - 150, 880, SW / 2 + 150, 950)
    if ov.get('qrglow'):
        d.rounded_rectangle((SW / 2 - 206, 354, SW / 2 + 206, 766), 34, outline=YEL, width=7)
    return im.crop((0, 0, SW, max(SH, 1000))), rows


A.BUILDERS.update({'a_net': net_content, 'a_inet': inet_content, 'a_ndetail': detail_content, 'a_qr': qr_content})


def row_point(spec_, rid, fx=0.62):
    _, rows = A.screen_content(spec_['name'], spec_.get('ov'), spec_.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    if rid.startswith('app_'):
        return (x0 + x1) / 2 + 6, (y0 + y1) / 2 + 8
    if rid in ('home_gear', 'share', 'quick', 'qr'):
        return (x0 + x1) / 2, (y0 + y1) / 2 - spec_.get('scroll', 0)
    return x0 + (x1 - x0) * fx, (y0 + y1) / 2 - spec_.get('scroll', 0)


m.row_point = row_point


# ======================================================================= friend phone (demo)
FRIEND = {}


def friend_screen(state):
    global QR
    if QR is None:
        QR = qr_img(348)
    im = Image.new('RGB', (SW, SH))
    d = ImageDraw.Draw(im)
    for y in range(SH):
        t = y / SH
        d.line([(0, y), (SW, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip((70, 66, 60), (30, 28, 26))))
    # the shown QR (on our phone) seen through camera
    q = QR.resize((250, 250)).rotate(-6, expand=True, fillcolor=(60, 58, 54))
    d.rounded_rectangle((130, 380, 430, 680), 20, fill=(240, 240, 244))
    im.paste(q, (int(SW / 2 - q.width / 2), int(530 - q.height / 2)))
    d = ImageDraw.Draw(im)
    c = YEL
    for (ax, ay, dx, dy) in [(110, 360, 1, 1), (450, 360, -1, 1), (110, 700, 1, -1), (450, 700, -1, -1)]:
        d.line([(ax, ay + dy * 50), (ax, ay), (ax + dx * 50, ay)], fill=c, width=10)
    d.ellipse((SW / 2 - 40, SH - 150, SW / 2 + 40, SH - 70), outline=(255, 255, 255), width=8)
    if state in ('join', 'ok'):
        ok = state == 'ok'
        d.rounded_rectangle((40, 780, SW - 40, 900), 40, fill=(52, 168, 83) if ok else (255, 255, 255))
        if ok:
            d.line([(90, 840), (108, 858), (140, 822)], fill=(255, 255, 255), width=7)
            d.text((170, 840), 'Connected to Home', font=F(600, 30), fill=(255, 255, 255), anchor='lm')
        else:
            wifi_icon(d, 96, 834, ACC, 1.2)
            d.text((140, 840), 'Join "Home" network', font=F(600, 30), fill=TXT, anchor='lm')
    A.status_bar(im, True)
    d = ImageDraw.Draw(im)
    d.ellipse((SW / 2 - 15, 30, SW / 2 + 15, 60), fill=(8, 8, 10))
    return im


def draw_friend(cv, f, fr):
    if not FRIEND:
        sh, body = th.sprite(android_phone_raw(), border=8, off=(16, 22), blur=14, op=.4)
        FRIEND['sp'] = (sh, body)
        FRIEND['off'] = ((body.width - 616) // 2 + 28, (body.height - 1224) // 2 + 20)
        FRIEND['mask'] = Image.new('L', (SW, SH), 0)
        ImageDraw.Draw(FRIEND['mask']).rounded_rectangle((0, 0, SW - 1, SH - 1), 62, fill=255)
        FRIEND['cache'] = {}
    st = fr['state']
    if st not in FRIEND['cache']:
        sh, body = FRIEND['sp']
        body = body.copy()
        body.paste(apply_tex(friend_screen(st), th.paper_tex(SW, SH, seed=5, strength=.7)), FRIEND['off'], FRIEND['mask'])
        sc = .56
        sp = (sh.resize((int(sh.width * sc), int(sh.height * sc)), Image.LANCZOS), body.resize((int(body.width * sc), int(body.height * sc)), Image.LANCZOS))
        FRIEND['cache'][st] = rotate_sprite(sp, -8)
    jx, jy = jit(f, 'friend', 1.4)
    draw_sprite(cv, FRIEND['cache'][st], fr['x'] + jx, fr['y'] + jy)
    if st == 'ok':
        pass


_orig_draw_phone = m.draw_phone


def draw_phone(cv, f, ph):
    _orig_draw_phone(cv, f, ph)
    if ph.get('friend'):
        draw_friend(cv, f, ph['friend'])


m.draw_phone = draw_phone


# ======================================================================= timeline
def build():
    t = m.TL()
    t.ph['spec'] = spec('a_home')
    t.fx.append(('title', 0, 50)); t.hold(56)
    t.phone_to(m.PHY, 6, keys=-40); t.hold(2)
    # problem
    t.cap('P', 'Guests asking for your Wi-Fi password... again?', m.PINK); t.hold(4)
    sp = t.ph['spec']
    for b in (-700, -300, -60, 0):
        sp['ov'] = {'banner': b, 'bkey': 'guest'}; t.snap()
    t.sound('pop'); t.hold(20)
    t.cap('Q', 'Show them a QR code instead!', m.YELLOW)
    for b in (60, 220, 700):
        sp['ov'] = {'banner': b, 'bkey': 'guest'}; t.snap()
    sp['ov'] = {}; t.hold(14)
    # steps
    t.cap('1', 'Open Settings', m.YELLOW); t.hold(8)
    t.tap('app_settings', nav=spec('a_settings'), n_move=7)
    t.cap('2', 'Tap Network & internet', m.PINK); t.hold(10)
    t.tap('net', nav=spec('a_net'))
    t.cap('3', 'Tap Internet', m.MINT); t.hold(10)
    t.tap('internet', nav=spec('a_inet', ov={'gearpulse': True}))
    t.cap('4', 'Tap the gear next to your network', m.SKY); t.hold(10)
    t.tap('home_gear', nav=spec('a_ndetail', ov={'sharepulse': True}))
    t.cap('5', "Tap Share, then confirm it's you", m.PEACH); t.hold(10)
    t.tap('share')
    t.ph['spec']['ov'] = {'verify': 'scan'}; t.sound('pop')
    t.move_hand(t.hand['x'] + 150, t.hand['y'] + 520, 3); t.hold(8)
    t.ph['spec']['ov'] = {'verify': 'ok'}; t.sound('ding'); t.hold(6)
    t.navigate(spec('a_qr', ov={'qrglow': True}))
    t.cap('check', 'Your Wi-Fi QR code is ready!', m.MINT)
    t.hand_out(4); t.hold(18)
    # demo: friend scans
    t.cap('T', 'Your friend just points their camera at it', m.PEACH)
    t.sound('whoosh')
    for i in range(1, 7):
        e = ease(i / 6)
        t.ph['x'] = 540 - 200 * e
        t.ph['friend'] = dict(x=1500 - (1500 - 830) * e, y=1330, state='scan')
        t.snap()
    t.hold(14)
    t.ph['friend']['state'] = 'join'; t.sound('pop'); t.hold(14)
    t.ph['friend']['state'] = 'ok'; t.sound('ding')
    t.cap('check', 'Connected, no typing needed!', m.MINT); t.hold(28)
    t.sound('whoosh')
    for i in range(1, 6):
        e = ease(i / 5)
        t.ph['x'] = 340 + 200 * e
        t.ph['friend']['x'] = 830 + 700 * e
        t.snap()
    t.ph['friend'] = None
    # bonus
    t.cap('+', 'Bonus: Quick Share sends it to nearby phones', m.SKY); t.hold(8)
    tx, ty = t.s2c(*row_point(t.ph['spec'], 'quick'))
    t.move_hand(tx, ty, 6); t.hold(2); t.press(tx, ty); t.ph['spec']['hl'] = 'quick'; t.hold(2)
    t.hand['press'] = False; t.ph['spec']['hl'] = None; t.hold(18)
    t.hand_out(4)
    t.cap_off()
    t.phone_to(2700, 5)
    t.fx.append(('end', t.f)); t.hold(72)
    return t


def render(f):
    tl = m.TLD
    st = tl['frames'][f]
    P = m.P
    ph = st['ph']
    P['bg'] = P['bg_dims'] if (abs(ph['y'] - m.PHY) < 60 and abs(ph['x'] - 540) < 5) else P['bg_plain']
    cv = P['bg'].copy()
    for e in tl['fx']:
        if e[0] == 'title' and f < e[2] + 8:
            m.draw_title(cv, f, e[1], e[2])
        if e[0] == 'end' and f >= e[1]:
            m.draw_end(cv, f, e[1])
    m.draw_phone(cv, f, ph)
    m.draw_fx(cv, f, tl['fx'])
    m.draw_hand(cv, f, st['hand'])
    m.draw_caps(cv, f, tl['caps'])
    k = 1 + rng_for(f, 'flicker').uniform(-0.016, 0.016)
    out = cv.convert('RGB').point(lambda v: min(255, int(v * k)))
    out.save(f'{OUT}/{f:05d}.png', compress_level=1)
    return f


# ======================================================================= props / title / end
def fig_head(badge):
    if badge.isdigit():
        return f'FIG. 0{badge}  /  STEP {badge} OF 5'
    return {'P': 'FIG. 00  /  THE PROBLEM', 'Q': 'FIG. 00  /  THE FIX', 'T': 'FIG. 06  /  FIELD TEST',
            'check': 'RESULT  /  OK', '+': 'APPENDIX  /  BONUS'}[badge]


mb.fig_head = fig_head


def vellum_qr():
    w, h = 300, 560
    im = Image.new('RGBA', (w, h), (230, 240, 255, 70))
    d = ImageDraw.Draw(im)
    C = th.CHALK + (255,)
    d.rounded_rectangle((20, 20, w - 20, h - 20), 40, outline=C, width=5)
    d.ellipse((w / 2 - 10, 38, w / 2 + 10, 58), outline=C, width=3)
    x0, y0, s = 60, 150, 180
    d.rectangle((x0, y0, x0 + s, y0 + s), outline=C, width=5)
    for qx, qy in [(0, 0), (s - 54, 0), (0, s - 54)]:
        d.rectangle((x0 + qx + 10, y0 + qy + 10, x0 + qx + 44, y0 + qy + 44), outline=C, width=5)
        d.rectangle((x0 + qx + 20, y0 + qy + 20, x0 + qx + 34, y0 + qy + 34), fill=C)
    r = rng_for('vq')
    for i in range(16):
        for j in range(16):
            if r.random() < .35 and not ((i < 6 and j < 6) or (i > 9 and j < 6) or (i < 6 and j > 9)):
                d.rectangle((x0 + 10 + i * 10, y0 + 10 + j * 10, x0 + 17 + i * 10, y0 + 17 + j * 10), fill=C)
    for (ax, ay, dx, dy) in [(48, 138, 1, 1), (252, 138, -1, 1), (48, 342, 1, -1), (252, 342, -1, -1)]:
        d.line([(ax, ay + dy * 30), (ax, ay), (ax + dx * 30, ay)], fill=mb.YEL + (255,), width=6)
    d.text((w / 2, 420), 'SCAN', font=th.JB(800, 44), fill=C, anchor='mm')
    d.text((w / 2, 470), '= CONNECTED', font=th.JB(700, 26), fill=C, anchor='mm')
    sp = th.sprite(im, border=0, off=(6, 9), blur=6, op=.3, tex=False)
    return rotate_sprite(sp, 8)


def init_props():
    mb.init_props()
    P = m.P
    P['front'] = th.sprite(android_phone_raw(), border=8, off=(16, 22), blur=14, op=.4)
    P['tiles'] = [rotate_sprite(th.stencil_letter(ch, PAPER if i < 5 else YEL), rng_for('sw', i).uniform(-5, 5)) for i, ch in enumerate('SHAREWI-FI')]
    P['t_label'] = mb.label('SPEC // Android tip', th.JB(700, 34), fg=MID, rot=-2, padx=30, pady=16)
    P['t_s1'] = mb.center_label('NO NEED TO SAY THE PASSWORD', th.JB(800, 42), rot=1.5)
    P['t_s1b'] = mb.center_label('JUST SHOW A QR CODE', th.JB(800, 42), rot=-1)
    P['t_s2'] = mb.center_label('android wi-fi sharing', th.JB(700, 40), bg=YEL, rot=-2)
    P['t_phone'] = vellum_qr()
    P['t_burst'] = mb.label(['ANDROID', '10 & LATER'], th.JB(800, 36), rot=6, padx=26, pady=16)
    P['e_chips'] = [rotate_sprite(mb.path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('Settings', (100, 104, 116), 'gear', -2), ('Network & internet', (66, 133, 244), 'wifi', 1.5),
        ('Internet > gear', ACC, 'gear', -1.5), ('Share', NAVY, 'grid', 2)])]
    P['e_s1'] = mb.center_label('SAMSUNG: WI-FI > GEAR > QR CODE', th.JB(800, 38), bg=YEL, rot=-1.5)
    P['e_s2'] = mb.center_label('FRIEND: SCAN WITH CAMERA', th.JB(800, 44), rot=1.5)
    P['e_s3'] = mb.center_label('Android 10 or later', th.JB(600, 34), fg=MID, rot=-1, pady=18)


def draw_title(cv, f, a, ex):
    P = m.P
    els = [('t_label', 540, 360, a + 1, 0)]
    for i in range(5):
        els.append((i, 540 + (i - 2) * 172, 560, a + 4 + 2 * i, i % 3))
    for i in range(5):
        els.append((5 + i, 540 + (i - 2) * 172, 760, a + 12 + 2 * i, i % 3))
    els += [('t_s1', 540, 950, a + 22, 0), ('t_s1b', 540, 1055, a + 25, 1), ('t_s2', 520, 1170, a + 28, 2),
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
            for ap in [a + 1] + [a + 4 + 2 * i for i in range(5)] + [a + 12 + 2 * i for i in range(5)] + [a + 22, a + 25, a + 28, a + 31, a + 34]:
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
                render(f)
    else:
        with Pool(2) as pool:
            for i, _ in enumerate(pool.imap(render, range(n), chunksize=8)):
                if i % 100 == 0:
                    print('rendered', i, flush=True)
        m.make_audio(m.TLD, n, __import__('lib').out('audio_sharewifi.wav'))

"""Tech Wall — "Your battery drains because of this…"  (iPhone, MOTION GRAPHICS, 30 fps)

Background App Refresh: find the drain in Settings › Battery (Background Activity),
then Settings › General › Background App Refresh: turn it off per app or limit to Wi-Fi.
Bonus: Low Power Mode pauses Background App Refresh automatically (Apple Support 120745 / 118408).
Build:  ./build.sh battery
"""
import sys, math
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import mgfx as G
from mgfx import MG, spec, EASE, seg, sprite_at, P, YEL, CHALK, NAVY, MID, PAPER
import screens as S
from screens import F, BG_UI, CARD, SEP, TXT, GRAY, BLUE, GREEN, HL, CX0, CX1, SW, SH, chevron, checkmark, glyph
import themes as th
import movie_blue as mb
from lib import rotate_sprite, blit, rng_for

RED, ORANGE = (240, 80, 70), (255, 150, 60)
CUT_APPS = ('stream', 'photo')          # the two apps switched off in step 3

# fictional apps (no real app names / logos)
APPS = [  # id, name, colour, icon, battery %, usage type
    ('stream', 'StreamTV', (230, 60, 60), 'play', '31%', 'Background Activity'),
    ('photo', 'PhotoFeed', (175, 82, 222), 'cam', '22%', 'Background Activity'),
    ('maps', 'Maps', (52, 168, 83), 'pin', '12%', 'On Screen'),
    ('mail', 'Mail', (10, 122, 255), 'mail', '8%', 'On Screen'),
    ('weather', 'Weather', (60, 150, 240), 'sun', '', ''),
    ('notes', 'Notes', (240, 190, 20), 'notes', '', ''),
]
APP = {a[0]: a for a in APPS}


def app_icon(d, key, x, y, s):
    """rounded app tile with a white glyph"""
    _, _, col, gl, _, _ = APP[key]
    d.rounded_rectangle((x, y, x + s, y + s), int(s * .24), fill=col)
    cx, cy, w = x + s / 2, y + s / 2, (255, 255, 255)
    if gl == 'play':
        d.polygon([(cx - s * .16, cy - s * .22), (cx - s * .16, cy + s * .22), (cx + s * .24, cy)], fill=w)
    elif gl == 'mail':
        d.rounded_rectangle((cx - s * .3, cy - s * .2, cx + s * .3, cy + s * .2), 4, fill=w)
        d.line([(cx - s * .28, cy - s * .18), (cx, cy + s * .04), (cx + s * .28, cy - s * .18)], fill=col, width=max(2, int(s * .06)))
    elif gl == 'pin':
        d.ellipse((cx - s * .2, cy - s * .3, cx + s * .2, cy + s * .1), fill=w)
        d.polygon([(cx - s * .17, cy - s * .02), (cx + s * .17, cy - s * .02), (cx, cy + s * .3)], fill=w)
        d.ellipse((cx - s * .07, cy - s * .17, cx + s * .07, cy - s * .03), fill=col)
    elif gl == 'notes':
        d.rounded_rectangle((cx - s * .26, cy - s * .3, cx + s * .26, cy + s * .3), 5, fill=w)
        for k in range(3):
            d.line([(cx - s * .16, cy - s * .12 + k * s * .13), (cx + s * .16, cy - s * .12 + k * s * .13)], fill=col, width=max(2, int(s * .05)))
    else:
        glyph(d, gl, x, y, s)


# ======================================================================= iOS-style screens
def toggle(d, xr, cy, on):
    d.rounded_rectangle((xr - 86, cy - 25, xr, cy + 25), 25, fill=GREEN if on else (229, 229, 234))
    kx = xr - 27 if on else xr - 59
    d.ellipse((kx - 21, cy - 21, kx + 21, cy + 21), fill=(255, 255, 255), outline=(215, 215, 220))


def card(img, y, items, hl, rows, rowh=86):
    """items: (rid, label, icon_key|None, right, sub) ; right = ('chev', val) | ('toggle', on) | ('check', on) | ('text', s) | None"""
    w = CX1 - CX0
    c = Image.new('RGB', (w, rowh * len(items)), CARD)
    d = ImageDraw.Draw(c)
    for i, (rid, lab, ic, right, sub) in enumerate(items):
        y0 = i * rowh; cy = y0 + rowh / 2
        if hl == rid:
            d.rectangle((0, y0, w, y0 + rowh), fill=HL)
        lx = 22
        if ic:
            app_icon(d, ic, 20, int(cy - 27), 54); lx = 92
        if sub:
            d.text((lx, cy - 15), lab, font=F(500, 30), fill=TXT, anchor='lm')
            d.text((lx, cy + 20), sub, font=F(400, 23), fill=GRAY, anchor='lm')
        else:
            d.text((lx, cy), lab, font=F(500, 30), fill=TXT, anchor='lm')
        xr = w - 22
        if right:
            kind, v = right
            if kind == 'chev':
                chevron(d, xr - 10, cy, (196, 196, 200)); xr -= 30
                if v:
                    d.text((xr, cy), v, font=F(400, 28), fill=GRAY, anchor='rm')
            elif kind == 'toggle':
                toggle(d, xr, cy, v)
            elif kind == 'check' and v:
                checkmark(d, w - 48, cy, BLUE)
            elif kind == 'text':
                d.text((xr, cy), v, font=F(500, 29), fill=TXT, anchor='rm')
        if i < len(items) - 1:
            d.line([(lx, y0 + rowh - 1), (w, y0 + rowh - 1)], fill=SEP, width=2)
        rows[rid] = (CX0, y + y0, CX1, y + y0 + rowh)
    mk = Image.new('L', c.size, 0)
    ImageDraw.Draw(mk).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 24, fill=255)
    img.paste(c, (CX0, y), mk)
    return y + c.height + 34


def nav(d, rows, back, title, size=62):
    y = 112
    chevron(d, 24, y + 24, BLUE, w=5, s=11, left=True)
    d.text((50, y + 24), back, font=F(500, 32), fill=BLUE, anchor='lm')
    rows['back'] = (10, y - 6, 250, y + 56)
    while F(600, size).getlength(title) > SW - 60:
        size -= 2
    d.text((30, y + 62), title, font=F(600, size), fill=TXT, anchor='lt')
    return y + 62 + int(size * 1.55)


def header(d, y, txt):
    d.text((44, y + 26), txt, font=F(500, 23), fill=GRAY, anchor='lm')
    return y + 50


def footer(d, y, txt):
    y -= 22
    for ln in S.wrap(txt, F(400, 24), 460):
        d.text((44, y), ln, font=F(400, 24), fill=GRAY, anchor='lt'); y += 31
    return y + 30


BARS = [3, 4, 2, 2, 1, 1, 2, 5, 8, 7, 9, 10, 8, 7, 9, 11, 10, 8, 9, 12, 10, 7, 5, 3]


def battery_screen(ov, hl):
    img = Image.new('RGB', (SW, 1500), BG_UI); d = ImageDraw.Draw(img); rows = {}
    y = nav(d, rows, 'Settings', 'Battery')
    y = card(img, y, [('lpm', 'Low Power Mode', None, ('toggle', bool(ov.get('lpm'))), None)], hl, rows)
    y = header(d, y, 'LAST 24 HOURS')
    # usage chart card
    ch = 200
    c = Image.new('RGB', (CX1 - CX0, ch), CARD); cd = ImageDraw.Draw(c)
    for k in range(4):
        gy = 30 + k * 40
        for gx in range(20, c.width - 20, 14):
            cd.line([(gx, gy), (gx + 6, gy)], fill=(214, 214, 222), width=2)
    p = ov.get('bars', 10) / 10
    bw = (c.width - 60) / len(BARS)
    for i, v in enumerate(BARS):
        hh = v / 12 * 140 * EASE['o'](min(1, max(0, p * 1.6 - i / len(BARS) * .6)))
        x0 = 30 + i * bw
        cd.rounded_rectangle((x0 + 3, 170 - hh, x0 + bw - 3, 170), 3, fill=GREEN)
    for i, lab in enumerate(['12 A', '6', '12 P', '6']):
        cd.text((30 + i * (c.width - 60) / 4, 186), lab, font=F(400, 18), fill=GRAY, anchor='lm')
    mk = Image.new('L', c.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, c.width - 1, ch - 1), 24, fill=255)
    img.paste(c, (CX0, y), mk); y += ch + 34
    y = header(d, y, 'BATTERY USAGE BY APP')
    y0 = y
    y = card(img, y, [(a[0], a[1], a[0], ('text', a[4]), a[5]) for a in APPS[:4]], hl, rows, rowh=96)
    if ov.get('glow'):
        for i in range(2):                     # highlight the two "Background Activity" lines
            gy = y0 + i * 96 + 48 + 20
            d.rounded_rectangle((CX0 + 84, gy - 18, CX0 + 340, gy + 18), 12, outline=YEL, width=5)
    return img.crop((0, 0, SW, max(SH, y + 40))), rows


def general_screen(ov, hl):
    img = Image.new('RGB', (SW, 1500), BG_UI); d = ImageDraw.Draw(img); rows = {}
    y = nav(d, rows, 'Settings', 'General')
    ch = lambda rid, lab: (rid, lab, None, ('chev', None), None)
    y = card(img, y, [ch('about', 'About'), ch('update', 'Software Update')], hl, rows)
    y = card(img, y, [ch('airdrop', 'AirDrop'), ch('airplay', 'AirPlay & Continuity'), ch('pip', 'Picture in Picture')], hl, rows)
    y = card(img, y, [ch('storage', 'iPhone Storage'), ch('bar', 'Background App Refresh')], hl, rows)
    y = card(img, y, [ch('date', 'Date & Time'), ch('kbd', 'Keyboard'), ch('fonts', 'Fonts')], hl, rows)
    if ov.get('glow'):
        x0, y0, x1, y1 = rows['bar']
        d.rounded_rectangle((x0 - 5, y0 - 5, x1 + 5, y1 + 5), 20, outline=YEL, width=6)
    return img.crop((0, 0, SW, max(SH, y + 40))), rows


MODES = {'off': 'Off', 'wifi': 'Wi-Fi', 'cell': 'Wi-Fi & Cellular Data'}


def bar_screen(ov, hl):
    img = Image.new('RGB', (SW, 1500), BG_UI); d = ImageDraw.Draw(img); rows = {}
    y = nav(d, rows, 'General', 'Background App Refresh')
    y = card(img, y, [('mode', 'Background App Refresh', None, ('chev', None), MODES[ov.get('mode', 'cell')])], hl, rows, rowh=104)
    y = footer(d, y, 'Allow apps to refresh their content when on Wi-Fi or cellular in the background. '
                     'Turning off apps may help preserve battery life.')
    y = card(img, y, [(a[0], a[1], a[0], ('toggle', not ov.get('off_' + a[0])), None) for a in APPS], hl, rows)
    return img.crop((0, 0, SW, max(SH, y + 40))), rows


def mode_screen(ov, hl):
    img = Image.new('RGB', (SW, 1500), BG_UI); d = ImageDraw.Draw(img); rows = {}
    y = nav(d, rows, 'Back', 'Background App Refresh')
    y = card(img, y, [(k, v, None, ('check', ov.get('mode', 'cell') == k), None) for k, v in MODES.items()], hl, rows)
    return img.crop((0, 0, SW, max(SH, y + 40))), rows


G.SCREEN_FN.update({'b_battery': battery_screen, 'b_general': general_screen, 'b_bar': bar_screen, 'b_mode': mode_screen})


# ======================================================================= hook / result graphics
BX, BY, BW, BH = 520, 1040, 540, 260          # battery centre + size
TILES = [('stream', 190, 640), ('photo', 540, 600), ('maps', 890, 640),
         ('mail', 190, 1500), ('weather', 540, 1560), ('notes', 890, 1500)]
TS = 130


def tile_sprite(key):
    im = Image.new('RGBA', (TS, TS), (0, 0, 0, 0))
    app_icon(ImageDraw.Draw(im), key, 0, 0, TS)
    return th.sprite(im, border=6, off=(7, 10), blur=7, op=.42)


class Hook:
    """battery + app tiles drain scene; reused (with 'cut' lines) for the result and Low Power bonus"""
    def __init__(s):
        s.vis = G.Track(1.0)       # 0..1 whole group in/out (on screen at frame 0)
        s.level = G.Track(1.0)     # battery level 0..1
        s.lines = G.Track(0.0)     # drain lines on (0..1 draw-on)
        s.cut = G.Track(0.0)       # 0..1 lines retract for the apps switched off (CUT_APPS)
        s.talpha = G.Track(1.0)    # tiles + lines fade (bonus)
        s.lpm = G.Track(0.0)       # low power mode switch 0..1
        s.tiles_in = []            # per-tile pop-in start times
        s.flow = 1.0               # dash speed factor


HK = Hook()


def battery_color(lv, lpm):
    if lpm > .5:
        return YEL
    if lv > .5:
        return (110, 210, 120)
    return ORANGE if lv > .25 else RED


def draw_hook(cv, t, mg):
    v = HK.vis.at(t)
    if v <= .001:
        return
    d = ImageDraw.Draw(cv)
    lv = HK.level.at(t)
    ln = HK.lines.at(t)
    cut = HK.cut.at(t)
    lpm = HK.lpm.at(t)
    ta = HK.talpha.at(t)
    # group motion: rises in, drops out
    dy = (1 - EASE['o5'](v)) * 700
    bx, by = BX, BY + dy
    # --- drain lines (battery -> app tiles), dashes flowing out of the battery
    for i, (key, tx, ty) in enumerate(TILES):
        ty += dy
        t0 = HK.tiles_in[i] if i < len(HK.tiles_in) else 0
        if t < t0 + .2:
            continue
        sx = bx + (BW / 2 if tx > bx + 80 else -BW / 2 if tx < bx - 80 else 0)
        sy = by + (-BH / 2 if ty < by else BH / 2)
        if abs(tx - bx) <= 80:
            sx = tx
        ex, ey = tx, ty + (TS / 2 + 10 if ty < by else -TS / 2 - 10)
        L = math.hypot(ex - sx, ey - sy)
        ux, uy = (ex - sx) / L, (ey - sy) / L
        c_ = cut if key in CUT_APPS else 0.0
        a0, a1 = L * c_, L * min(1, ln) * ta     # visible span (cut retracts from battery side)
        speed = 1.0 - .6 * cut if key not in CUT_APPS else 1.0   # others: Wi-Fi only -> slower
        ph = (t * 140 * speed) % 40
        s_ = a0 - (a0 % 40) + ph - 40
        while s_ < a1:
            p0, p1 = max(s_, a0), min(s_ + 22, a1)
            if p1 > p0:
                d.line([(sx + ux * p0, sy + uy * p0), (sx + ux * p1, sy + uy * p1)], fill=CHALK, width=7)
            s_ += 40
        if c_ > .02 and ta > .5:                    # yellow "cut" marker near the tile
            k = min(1, c_ * 1.4)
            mx, my = sx + ux * L * .55, sy + uy * L * .55
            r = 22 * EASE['back'](k)
            d.line([(mx - r, my - r), (mx + r, my + r)], fill=YEL, width=9)
            d.line([(mx - r, my + r), (mx + r, my - r)], fill=YEL, width=9)
    # --- app tiles (pop in) + spinning refresh arrows
    for i, (key, tx, ty) in enumerate(TILES):
        t0 = HK.tiles_in[i] if i < len(HK.tiles_in) else 0
        sc = EASE['back'](seg(t, t0, t0 + .35))
        if sc <= 0:
            continue
        ty += dy
        if ta <= .01:
            continue
        sprite_at(cv, P['tiles'][key], tx, ty, sc, ta)
        c_ = cut if key in CUT_APPS else 0.0
        if ta < .95:
            continue
        if c_ < .5 and sc > .9:                  # refresh arrow spinning on the tile corner
            cx, cy, r = tx + TS / 2 - 6, ty - TS / 2 + 6, 24
            d.ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), fill=NAVY)
            a = (t * 300) % 360
            d.arc((cx - r, cy - r, cx + r, cy + r), a, a + 280, fill=YEL, width=7)
            ex_, ey_ = cx + r * math.cos(math.radians(a + 280)), cy + r * math.sin(math.radians(a + 280))
            ang = math.radians(a + 280 + 90)
            d.polygon([(ex_ + 12 * math.cos(ang), ey_ + 12 * math.sin(ang)),
                       (ex_ + 12 * math.cos(ang + 2.4), ey_ + 12 * math.sin(ang + 2.4)),
                       (ex_ + 12 * math.cos(ang - 2.4), ey_ + 12 * math.sin(ang - 2.4))], fill=YEL)
        elif c_ >= .5 and sc > .9:                # "OFF" chip on the tile
            cx, cy = tx + TS / 2 - 4, ty - TS / 2 + 4
            d.rounded_rectangle((cx - 40, cy - 20, cx + 40, cy + 20), 10, fill=YEL)
            d.text((cx, cy), 'OFF', font=th.JB(800, 24), fill=NAVY, anchor='mm')
    # --- the battery (chalk outline, filled level)
    x0, y0, x1, y1 = bx - BW / 2, by - BH / 2, bx + BW / 2, by + BH / 2
    d.rounded_rectangle((x0 - 4, y0 - 4, x1 + 4, y1 + 4), 46, fill=NAVY)
    fw = (BW - 44) * max(.03, lv)
    d.rounded_rectangle((x0 + 22, y0 + 22, x0 + 22 + fw, y1 - 22), 26, fill=battery_color(lv, lpm))
    d.rounded_rectangle((x0, y0, x1, y1), 44, outline=CHALK, width=12)
    d.rounded_rectangle((x1 + 10, by - 52, x1 + 38, by + 52), 12, fill=CHALK)
    pct = f'{int(round(lv * 100))}%'
    d.text((bx + 3, by + 5), pct, font=th.JB(800, 128), fill=NAVY, anchor='mm')
    d.text((bx, by), pct, font=th.JB(800, 128), fill=PAPER, anchor='mm')
    # --- chalk annotation under the battery
    lab_a = min(1, ln * 2.5) * (1 - cut) * ta
    if lab_a > .05 and lpm < .05:
        sprite_at(cv, P['bg_label'], bx, by + BH / 2 + 80, 1, lab_a)
    # --- Low Power Mode switch (bonus) — tiles have faded out, so it sits centred under the battery
    if lpm > .001:
        k = EASE['back'](seg(lpm, 0, .45))
        sw_y = by + BH / 2 + 170
        if k > .05:
            d.text((bx - 120, sw_y), 'LOW POWER MODE', font=th.JB(800, 46), fill=CHALK, anchor='mm')
        on = EASE['io'](seg(lpm, .45, 1))
        sx = bx + 250
        if k > .9:
            d.rounded_rectangle((sx - 90, sw_y - 46, sx + 90, sw_y + 46), 46,
                                fill=tuple(int(a + (b - a) * on) for a, b in zip((90, 110, 150), YEL)), outline=CHALK, width=6)
            kx = sx - 44 + 88 * on
            d.ellipse((kx - 36, sw_y - 36, kx + 36, sw_y + 36), fill=PAPER)
        sprite_at(cv, P['lpm_label'], bx, sw_y + 120, k)


# ======================================================================= end card (smooth)
END = []


def draw_end(cv, t, mg):
    if mg.end_at is None or t < mg.end_at:
        return
    for key, x, y, dt in END:
        k = seg(t, mg.end_at + dt, mg.end_at + dt + .4)
        if k <= 0:
            continue
        yy = y - 260 * (1 - EASE['back'](k))
        sprite_at(cv, P[key], x, yy, 1, min(1, k * 3))


# ======================================================================= timeline
def build():
    mg = MG()
    mg.layers.append(draw_hook)
    mg.top_layers.append(draw_end)
    # ---- 0:00 HOOK — battery draining into background apps
    mg.cap('TECH WALL  /  iPHONE TIP', 'YOUR BATTERY DRAINS BECAUSE OF THIS...', rot=-1)
    mg.caps[-1]['t_in'] = -1                        # caption already on screen at frame 0
    HK.tiles_in = [-.6 + i * .05 for i in range(6)]     # all tiles already in at frame 0
    for i in range(6):
        if HK.tiles_in[i] >= 0:
            mg.snd.append((HK.tiles_in[i], 'pop'))
    HK.lines.k = [(-1e9, .35, 'lin')]           # lines already part-drawn at frame 0
    HK.lines.to(0, .7, 1.0, 'o')
    HK.level.to(.15, 3.4, .19, 'io')
    mg.t = 2.4
    mg.cap('FIG. 01  /  THE CULPRIT', 'Apps refreshing in the background')
    mg.t = 4.6
    # ---- phone in
    HK.vis.to(mg.t, .5, 0.0, 'i')
    mg.t += .25
    mg.set_spec(spec('settings'))
    mg.phone_to(y=G.PHY, dur=.7, dims=1.0)
    mg.wait(.5)
    mg.cap('STEP 1 OF 3', 'Settings > Battery: find what drains it')
    mg.wait(.55)
    mg.tap('battery', nav=spec('b_battery', ov={'bars': 0}))
    for b in range(1, 11):                        # usage bars grow
        sp = spec('b_battery', ov={'bars': b}); mg.spec.set(mg.t + b * .05, sp)
    mg.wait(.6)
    mg.spec.set(mg.t, spec('b_battery', ov={'bars': 10, 'glow': True}))
    mg.sound('ding')
    mg.cap('STEP 1 OF 3', 'Look for "Background Activity"')
    tx, ty = mg.s2c(380, 860)
    mg.hand_to(tx + 120, ty + 260, .4)
    mg.wait(1.6)
    # ---- step 2: General > Background App Refresh
    mg.cap('STEP 2 OF 3', 'General > Background App Refresh')
    mg.tap('back', nav=spec('settings'), back=True, fx=.3)
    mg.wait(.25)
    mg.tap('general', nav=spec('b_general'))
    mg.spec.set(mg.t + .05, spec('b_general', ov={'glow': True}))
    mg.wait(.45)
    mg.tap('bar', nav=spec('b_bar'))
    # ---- step 3: switch off heavy apps
    mg.cap('STEP 3 OF 3', "Turn it OFF for apps you don't need")
    mg.wait(.35)
    mg.tap('stream', ov={'off_stream': True}, fx=.86)
    mg.wait(.15)
    mg.tap('photo', ov={'off_stream': True, 'off_photo': True}, fx=.86, move=.3)
    mg.wait(.55)
    mg.cap('STEP 3 OF 3', 'Or limit it to Wi-Fi only')
    mg.wait(.3)
    mg.tap('mode', nav=spec('b_mode'), fx=.8, move=.35)
    mg.wait(.2)
    mg.tap('wifi', ov={'mode': 'wifi'}, fx=.8, move=.3)
    mg.wait(.4)
    mg.tap('back', nav=spec('b_bar', ov={'off_stream': True, 'off_photo': True, 'mode': 'wifi'}), back=True, fx=.25, move=.35)
    mg.wait(.9)
    mg.hand_out()
    # ---- result: lines cut, drain stops
    mg.phone_to(y=2700, dur=.55, e='i', dims=0.0)
    mg.wait(.3)
    HK.level.set(mg.t, .19)
    HK.vis.to(mg.t, .6, 1.0, 'o5')
    mg.cap('RESULT  /  OK', 'The biggest drains: cut off')
    mg.wait(.7)
    HK.cut.to(mg.t, .8, 1.0, 'io')
    for i in range(2):
        mg.snd.append((mg.t + .15 + i * .15, 'tap'))
    mg.wait(2.0)
    # ---- bonus: Low Power Mode
    mg.cap('BONUS', 'Low Power Mode pauses it automatically')
    HK.talpha.to(mg.t, .45, 0.0, 'io')
    mg.wait(.4)
    HK.lpm.to(mg.t, 1.2, 1.0, 'lin')
    mg.snd.append((mg.t + .6, 'ding'))
    mg.wait(2.6)
    # ---- end card
    mg.cap_off()
    HK.vis.to(mg.t, .45, 0.0, 'i')
    mg.sound('whoosh')
    mg.wait(.35)
    mg.end_at = mg.t
    for key, x, y, dt in END:
        if not key.startswith('e_arrow'):
            mg.snd.append((mg.end_at + dt, 'pop'))
    mg.wait(4.6)
    mg.duration = mg.t
    return mg


def init_props():
    P['tiles'] = {a[0]: tile_sprite(a[0]) for a in APPS}
    P['bg_label'] = mb.center_label('RUNNING IN THE BACKGROUND', th.JB(800, 34), bg=YEL, rot=-1.5, padx=28, pady=12)
    P['lpm_label'] = mb.center_label('SETTINGS > BATTERY > LOW POWER MODE', th.JB(800, 30), rot=1.5, padx=24, pady=10)
    P['e_head'] = mb.center_label('SAVE THIS TIP', th.JB(800, 92), rot=-2.5, padx=56, pady=30)
    chips = [('Settings', S.GRAYI, 'gear'), ('General', S.GRAYI, 'gear'),
             ('Background App Refresh', BLUE, 'touch'), ('Off for heavy apps', NAVY, 'batt')]
    for i, (tx, c, g) in enumerate(chips):
        P[f'e_chip{i}'] = rotate_sprite(mb.path_label(tx, c, g, i + 1, hot=(i == 3)), (-2, 1.5, -1.5, 2)[i])
    for i in range(3):
        P[f'e_arrow{i}'] = mb.chalk_arrow((14, -14, 14)[i])
    P['e_s1'] = mb.center_label('FIND IT: SETTINGS > BATTERY', th.JB(800, 42), bg=YEL, rot=-1.5)
    P['e_s2'] = mb.center_label('LOW POWER MODE PAUSES IT', th.JB(800, 42), rot=1.5)
    P['e_s3'] = mb.center_label('any recent iPhone · iOS', th.JB(600, 34), fg=MID, rot=-1, pady=18)
    P['e_follow'] = mb.center_label('FOLLOW  TECH WALL', th.JB(800, 40), bg=YEL, rot=1, pady=18)


END[:] = [('e_head', 540, 300, 0)] + \
    [(f'e_chip{i}', (500, 580, 540, 580)[i], 560 + 175 * i, .15 + .12 * i) for i in range(4)] + \
    [(f'e_arrow{i}', (120, 960, 120)[i], 648 + 175 * i, .25 + .12 * i) for i in range(3)] + \
    [('e_s1', 540, 1330, .75), ('e_s2', 540, 1455, .87), ('e_s3', 540, 1580, .99), ('e_follow', 600, 1730, 1.2)]

if __name__ == '__main__':
    G.run(build(), 'battery', cover_t=2.8, init=init_props)

"""Tech-themed stop-motion style frames: A) Circuit Board  B) Blueprint  C) Neon Paper"""
import sys, math, random
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
from lib import (W, H, noise_L, paper_tex, apply_tex, cutout, pad, blit, draw_sprite, rotate_sprite, wrap, rng_for, M)
from screens import view, row_point, SW, SH, screen_tex
from props import phone_raw, PW, PH, screen_mask

FD = __import__('lib').FD
_f = {}


def font(name, s):
    k = (name, s)
    if k not in _f:
        _f[k] = ImageFont.truetype(FD + name, s)
    return _f[k]


JB = lambda w, s: font(f'jetbrains-mono-latin-{w}-normal.woff', s)
PX = lambda s: font('press-start-2p-latin-400-normal.woff', s)
STN = lambda s: font('allerta-stencil-latin-400-normal.woff', s)
ORB = lambda w, s: font(f'orbitron-latin-{w}-normal.woff', s)


# ------------------------------------------------------------------ sprite with colored shadow / glow
def sprite(img, border=8, off=(10, 14), blur=10, op=0.38, col=(20, 12, 6), paper=(252, 249, 242), tex=True,
           glow=None, tex_strength=0.7):
    cut = cutout(img, border, paper)
    if tex:
        cut = apply_tex(cut, paper_tex(cut.width, cut.height, seed=cut.width * 3 + cut.height, strength=tex_strength))
    gb = glow[2] if glow else 0
    p = int(max(blur, gb) * 2.6 + max(abs(off[0]), abs(off[1])))
    body = pad(cut, p)
    a = cut.split()[3]
    under = Image.new('RGBA', body.size, (0, 0, 0, 0))
    if glow:
        gc, gop, gblur = glow
        al = Image.new('L', body.size, 0); al.paste(a.point(lambda v: int(v * gop)), (p, p))
        g = Image.new('RGBA', body.size, gc + (0,)); g.putalpha(al.filter(ImageFilter.GaussianBlur(gblur)))
        under.alpha_composite(g)
    al = Image.new('L', body.size, 0); al.paste(a.point(lambda v: int(v * op)), (p + off[0], p + off[1]))
    sh = Image.new('RGBA', body.size, col + (0,)); sh.putalpha(al.filter(ImageFilter.GaussianBlur(blur)))
    under.alpha_composite(sh)
    return under, body


def put(cv, sp, x, y, rot=0):
    if rot:
        sp = rotate_sprite(sp, rot)
    draw_sprite(cv, sp, x, y)


def base_noise(col, seed, mott=0.16, fine=0.10, vig=0.32):
    b = np.zeros((H, W, 3), np.float32); b[:] = col
    m = np.asarray(noise_L(W // 10, H // 10, seed, 70, 2).resize((W, H), Image.BICUBIC), np.float32)[..., None] - 128
    f = np.asarray(noise_L(W, H, seed + 1, 40, 0.6), np.float32)[..., None] - 128
    b += m * mott + f * fine
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dd = np.sqrt(((xx - W / 2) / (W * .75)) ** 2 + ((yy - H / 2) / (H * .7)) ** 2)
    b *= np.clip(1 - vig * dd ** 2.2, .5, 1)[..., None]
    return Image.fromarray(np.clip(b, 0, 255).astype(np.uint8)).convert('RGBA')


# ------------------------------------------------------------------ hand (themed sleeve)
def hand_img(sleeve, sleeve_line, stripe=None):
    w, h = 430, 800
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    skin, line = (243, 196, 158), (196, 132, 92)
    d.ellipse((0, 430, 130, 650), fill=skin, outline=line, width=5)
    d.rounded_rectangle((30, 360, 410, 760), 150, fill=skin, outline=line, width=5)
    for x0, y0 in [(160, 330), (240, 352), (318, 384)]:
        d.rounded_rectangle((x0, y0, x0 + 92, y0 + 140), 46, fill=skin, outline=line, width=5)
    d.rounded_rectangle((62, 0, 160, 470), 49, fill=skin, outline=line, width=5)
    d.rounded_rectangle((82, 16, 140, 96), 27, fill=(252, 224, 210), outline=(214, 156, 124), width=4)
    for yy in (215, 305):
        d.arc((86, yy - 12, 136, yy + 12), 200, 340, fill=line, width=4)
    d.rounded_rectangle((18, 650, 422, 800), 20, fill=sleeve, outline=sleeve_line, width=5)
    if stripe:
        d.rectangle((22, 690, 418, 708), fill=stripe)
    return img, (111, 4)


def hand_sprite(theme, press=False):
    sleeve = {'pcb': ((34, 36, 42), (20, 20, 24), (255, 140, 60)), 'blue': ((28, 50, 96), (16, 30, 64), (240, 244, 250)),
              'neon': ((22, 22, 30), (10, 10, 14), (0, 230, 255))}[theme]
    raw, tip = hand_img(*sleeve)
    S = 1900
    big = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    big.paste(raw, (S // 2 - tip[0], S // 2 - tip[1]))
    big = big.rotate(24, resample=Image.BICUBIC)
    bb = big.getbbox(); big = big.crop(bb)
    tipl = (S // 2 - bb[0], S // 2 - bb[1])
    off, blur, op = ((8, 11), 5, .42) if press else ((34, 46), 16, .30)
    glow = ((255, 46, 160), .35, 26) if theme == 'neon' else None
    paper = (20, 20, 26) if theme == 'neon' else (252, 249, 242)
    sh, body = sprite(big, border=9, off=off, blur=blur, op=op, glow=glow, paper=paper)
    p = (body.width - big.width) // 2
    return sh, body, (tipl[0] + p, tipl[1] + p)


def draw_hand(cv, hs, x, y):
    sh, body, tip = hs
    blit(cv, sh, x - tip[0], y - tip[1]); blit(cv, body, x - tip[0], y - tip[1])


# ------------------------------------------------------------------ phone
def phone_sprite(theme, side, spec=None):
    raw = phone_raw(side)
    if theme == 'neon':
        sp = sprite(raw, border=8, off=(10, 16), blur=14, op=.5, glow=((0, 230, 255), .55, 30), paper=(30, 30, 40))
    else:
        sp = sprite(raw, border=8, off=(16, 22), blur=14, op=.4)
    sh, body = sp
    if side == 'front':
        body = body.copy()
        scr = view(spec)
        d = ImageDraw.Draw(scr)
        d.rounded_rectangle((SW / 2 - 86, 22, SW / 2 + 86, 72), 25, fill=(10, 10, 12))
        scr = apply_tex(scr, screen_tex())
        ox = (body.width - (PW + 16)) // 2 + 28; oy = (body.height - PH) // 2 + 20
        body.paste(scr, (ox, oy), screen_mask())
    return sh, body


PHX, PHY = 540, 1205


def s2c(x, y):
    return PHX - PW / 2 + 20 + x, PHY - PH / 2 + 20 + y


# ================================================================== THEME A — CIRCUIT BOARD
COPPER = (214, 162, 82)


def bg_pcb():
    cv = base_noise((20, 96, 70), 31, vig=.38)
    silk = ImageDraw.Draw(cv)
    r = random.Random(5)
    # traces (raised copper foil)
    tr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tr)
    for i in range(46):
        x, y = r.uniform(0, W), r.uniform(0, H)
        pts = [(x, y)]
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dx, dy = r.choice(dirs)
        for s in range(r.randint(2, 4)):
            L = r.uniform(80, 340)
            x += dx * L; y += dy * L; pts.append((x, y))
            # 45° jog
            j = r.uniform(30, 90); sgn = r.choice([-1, 1])
            if dx:
                x += dx * j; y += sgn * j
            else:
                x += sgn * j; y += dy * j
            pts.append((x, y))
            dx, dy = r.choice([d_ for d_ in dirs if d_ != (-dx, -dy)])
        wdt = r.choice([8, 10, 14])
        td.line(pts, fill=COPPER + (255,), width=wdt, joint='curve')
        for px, py in (pts[0], pts[-1]):
            td.ellipse((px - 15, py - 15, px + 15, py + 15), fill=COPPER + (255,))
    trs = sprite(tr, border=0, off=(2, 3), blur=2, op=.5, tex=True, tex_strength=1.2)
    blit(cv, trs[0], (W - trs[0].width) / 2, (H - trs[0].height) / 2)
    blit(cv, trs[1], (W - trs[1].width) / 2, (H - trs[1].height) / 2)
    # drill holes on pads
    d = ImageDraw.Draw(cv)
    rr = random.Random(5)
    # silkscreen labels
    for txt, x, y in [('U7', 70, 520), ('R12', 960, 1350), ('C3', 60, 1080), ('+3V3', 940, 560), ('GND', 70, 1880),
                      ('BACK_TAP_v1.0', 640, 1880), ('J1', 980, 1080), ('SW2', 50, 1390)]:
        d.text((x, y), txt, font=JB(700, 26), fill=(226, 240, 230), anchor='lm')
    # chips
    for i, (x, y, rot, lab) in enumerate([(120, 640, 0, 'BT-2X'), (980, 830, 90, 'A17'), (110, 1560, 0, 'TAP'), (960, 1600, 90, 'IO'),
                                            (930, 150, 0, 'SoC')]):
        cw, ch = 210, 130
        im = Image.new('RGBA', (cw + 60, ch), (0, 0, 0, 0)); cd = ImageDraw.Draw(im)
        for k in range(5):
            cd.rectangle((0, 14 + k * 24, 34, 26 + k * 24), fill=(200, 200, 206))
            cd.rectangle((cw + 26, 14 + k * 24, cw + 60, 26 + k * 24), fill=(200, 200, 206))
        cd.rounded_rectangle((26, 0, cw + 34, ch), 10, fill=(30, 30, 34))
        cd.ellipse((40, 12, 56, 28), fill=(70, 70, 78))
        cd.text((30 + cw / 2, ch / 2), lab, font=JB(700, 34), fill=(150, 150, 160), anchor='mm')
        sp = sprite(im, border=0, off=(7, 10), blur=6, op=.45)
        put(cv, sp, x, y, rot)
    # LEDs
    for x, y, c in [(240, 470, (255, 70, 60)), (860, 1000, (60, 255, 140)), (250, 1760, (60, 255, 140)), (820, 1780, (255, 190, 40))]:
        g = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse((30, 30, 90, 90), fill=c + (150,)); g = g.filter(ImageFilter.GaussianBlur(14))
        blit(cv, g, x - 60, y - 60)
        led = Image.new('RGBA', (40, 40), (0, 0, 0, 0)); ImageDraw.Draw(led).ellipse((4, 4, 36, 36), fill=c)
        put(cv, sprite(led, border=0, off=(3, 4), blur=3, op=.4), x, y)
    return cv


def cap_pcb(step, text):
    w, h = 900, 236
    img = Image.new('RGBA', (w, h + 44), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for x in range(70, w - 50, 66):
        d.rectangle((x, 0, x + 30, 24), fill=(205, 205, 210)); d.rectangle((x, h + 20, x + 30, h + 44), fill=(205, 205, 210))
    d.rounded_rectangle((0, 22, w, h + 22), 20, fill=(28, 28, 33))
    d.ellipse((24, 42, 44, 62), fill=(62, 62, 70))
    led = Image.new('RGBA', (140, 140), (0, 0, 0, 0)); ImageDraw.Draw(led).ellipse((40, 40, 100, 100), fill=(60, 255, 140, 200))
    img.alpha_composite(led.filter(ImageFilter.GaussianBlur(16)), (12, 22 + h // 2 - 70))
    d.ellipse((60, 22 + h / 2 - 18, 96, 22 + h / 2 + 18), fill=(90, 255, 160))
    d.text((134, 70), step, font=JB(700, 30), fill=(90, 255, 160), anchor='lm')
    lines = wrap(text, JB(700, 54), 720)
    for i, ln in enumerate(lines[:2]):
        d.text((134, 132 + i * 64), ln, font=JB(700, 54), fill=(245, 245, 248), anchor='lm')
    d.text((w - 30, 60), 'U4', font=JB(500, 24), fill=(120, 120, 130), anchor='rm')
    return sprite(img, border=0, off=(9, 13), blur=9, op=.45)


def keycap(ch, base, top, fg):
    s = 172
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s, s), 28, fill=base)
    d.rounded_rectangle((16, 8, s - 16, s - 30), 22, fill=top)
    d.text((s / 2, (s - 22) / 2), ch, font=JB(800, 92), fill=fg, anchor='mm')
    return sprite(im, border=0, off=(8, 12), blur=8, op=.45)


def title_pcb(cv):
    tag = Image.new('RGBA', (420, 76), (28, 28, 33, 255)); td = ImageDraw.Draw(tag)
    td.text((210, 38), '// iPhone tip', font=JB(700, 36), fill=(90, 255, 160), anchor='mm')
    put(cv, sprite(tag, border=0, off=(6, 9), blur=6, op=.45), 540, 400, -3)
    for i, ch in enumerate('BACK'):
        put(cv, keycap(ch, (196, 198, 206), (246, 246, 250), (40, 40, 48)), 540 + (i - 1.5) * 186, 600, [-4, 3, -2, 5][i])
    for i, ch in enumerate('TAP'):
        put(cv, keycap(ch, (214, 120, 40), (255, 160, 70), (40, 24, 10)), 540 + (i - 1) * 186, 796, [3, -3, 4][i])
    lcd = Image.new('RGBA', (860, 150), (0, 0, 0, 0)); ld = ImageDraw.Draw(lcd)
    ld.rounded_rectangle((0, 0, 860, 150), 18, fill=(40, 42, 46))
    ld.rectangle((24, 22, 836, 128), fill=(164, 196, 120))
    ld.text((430, 58), 'THE HIDDEN iPHONE', font=JB(800, 46), fill=(30, 50, 22), anchor='mm')
    ld.text((430, 104), 'SHORTCUT_', font=JB(800, 46), fill=(30, 50, 22), anchor='mm')
    put(cv, sprite(lcd, border=0, off=(8, 12), blur=8, op=.45), 540, 1010, 1.5)
    sub = Image.new('RGBA', (840, 86), (0, 0, 0, 0)); sd = ImageDraw.Draw(sub)
    sd.rounded_rectangle((0, 0, 840, 86), 43, fill=COPPER)
    sd.text((420, 43), 'double-tap back => screenshot', font=JB(700, 38), fill=(40, 26, 8), anchor='mm')
    put(cv, sprite(sub, border=0, off=(6, 9), blur=6, op=.45), 540, 1180, -1.5)
    mini = phone_raw('back').resize((190, 377), Image.LANCZOS)
    put(cv, sprite(mini, border=6, off=(8, 12), blur=8, op=.4), 560, 1530, 10)
    arcs(cv, 650, 1500, COPPER, 'r')


def arcs(cv, x, y, col, side='r', n=3, gap=46, start=60):
    for k in range(n):
        r_ = start + k * gap
        im = Image.new('RGBA', (2 * r_ + 40, 2 * r_ + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        a0, a1 = (-40, 40) if side == 'r' else (140, 220)
        d.arc((20, 20, 20 + 2 * r_, 20 + 2 * r_), a0, a1, fill=col + (255,), width=16)
        put(cv, sprite(im, border=0, off=(4, 6), blur=4, op=.4), x, y)


# ================================================================== THEME B — BLUEPRINT
CHALK = (226, 236, 252)


def bg_blue(with_dims=True):
    cv = base_noise((26, 62, 128), 41, mott=.12, fine=.08, vig=.30)
    d = ImageDraw.Draw(cv)
    for x in range(0, W, 30):
        d.line([(x, 0), (x, H)], fill=(52, 92, 162) if x % 150 else (82, 126, 196), width=1 if x % 150 else 2)
    for y in range(0, H, 30):
        d.line([(0, y), (W, y)], fill=(52, 92, 162) if y % 150 else (82, 126, 196), width=1 if y % 150 else 2)
    # title block bottom-left
    bx, by = 24, 1700
    d.rectangle((bx, by, bx + 190, by + 196), outline=CHALK, width=3)
    for i, t in enumerate(['DWG BT-01', 'REV  A', 'SCALE 1:1', 'SHEET 4/6']):
        d.line([(bx, by + 49 * (i + 1)), (bx + 190, by + 49 * (i + 1))], fill=CHALK, width=2)
        d.text((bx + 12, by + 25 + 49 * i), t, font=JB(600, 21), fill=CHALK, anchor='lm')
    # registration marks
    for cx, cy in [(70, 70), (1010, 70), (1010, 1850)]:
        d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), outline=CHALK, width=3)
        d.line([(cx - 40, cy), (cx + 40, cy)], fill=CHALK, width=2); d.line([(cx, cy - 40), (cx, cy + 40)], fill=CHALK, width=2)
    if with_dims:
        # vertical dimension along phone right
        x = 910
        d.line([(x, 600), (x, 1820)], fill=CHALK, width=3)
        for yy, s in [(600, 1), (1820, -1)]:
            d.polygon([(x, yy), (x - 12, yy + 30 * s), (x + 12, yy + 30 * s)], fill=CHALK)
            d.line([(860, yy), (940, yy)], fill=CHALK, width=2)
        t = Image.new('RGBA', (220, 50), (0, 0, 0, 0))
        ImageDraw.Draw(t).text((110, 25), 'H 146.6', font=JB(700, 30), fill=CHALK, anchor='mm')
        t = t.rotate(90, expand=True)
        blit(cv, t, x + 8, 1210 - 110)
        # horizontal dim above phone
        y = 560
        d.line([(240, y), (840, y)], fill=CHALK, width=3)
        for xx, s in [(240, 1), (840, -1)]:
            d.polygon([(xx, y), (xx + 30 * s, y - 12), (xx + 30 * s, y + 12)], fill=CHALK)
            d.line([(xx, 530), (xx, 600)], fill=CHALK, width=2)
        d.rectangle((470, y - 22, 610, y + 22), fill=(26, 62, 128))
        d.text((540, y), 'W 71.5', font=JB(700, 30), fill=CHALK, anchor='mm')
    return cv


def cap_blue(fig, text):
    w, h = 900, 236
    img = Image.new('RGBA', (w, h), (250, 250, 246, 255)); d = ImageDraw.Draw(img)
    d.text((40, 46), fig, font=JB(700, 28), fill=(30, 74, 160), anchor='lm')
    d.line([(40, 74), (w - 40, 74)], fill=(160, 180, 215), width=2)
    for i, ln in enumerate(wrap(text, JB(800, 54), 820)[:2]):
        d.text((40, 124 + i * 62), ln, font=JB(800, 54), fill=(20, 40, 92), anchor='lm')
    sp = sprite(img, border=0, off=(8, 12), blur=8, op=.42)
    sh, body = sp
    body = body.copy()
    tape = Image.new('RGBA', (220, 56), (232, 216, 168, 205)).rotate(-4, expand=True, resample=Image.BICUBIC)
    body.alpha_composite(tape, (body.width // 2 - tape.width // 2 + 120, (body.height - h) // 2 - 30))
    return sh, body


def stencil_letter(ch, col=(250, 250, 246)):
    f = STN(210)
    bb = f.getbbox(ch)
    im = Image.new('RGBA', (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - bb[0], 10 - bb[1]), ch, font=f, fill=col)
    return sprite(im, border=0, off=(7, 11), blur=6, op=.45)


def title_blue(cv):
    d = ImageDraw.Draw(cv)
    lab = Image.new('RGBA', (420, 70), (250, 250, 246, 255))
    ImageDraw.Draw(lab).text((210, 35), 'SPEC // iPhone tip', font=JB(700, 32), fill=(30, 74, 160), anchor='mm')
    put(cv, sprite(lab, border=0, off=(6, 9), blur=6, op=.4), 540, 380, -2)
    for i, ch in enumerate('BACK'):
        put(cv, stencil_letter(ch), 540 + (i - 1.5) * 180, 600, [-3, 2, -1, 3][i])
    for i, ch in enumerate('TAP'):
        put(cv, stencil_letter(ch, (255, 196, 70)), 540 + (i - 1) * 180, 820, [2, -2, 3][i])
    # chalk schematic of phone back with target
    px, py, pw, ph_ = 380, 1060, 320, 640
    d.rounded_rectangle((px, py, px + pw, py + ph_), 50, outline=CHALK, width=5)
    d.rounded_rectangle((px + 22, py + 22, px + 132, py + 132), 30, outline=CHALK, width=4)
    for cy in (py + 52, py + 102):
        d.ellipse((px + 40, cy - 18, px + 76, cy + 18), outline=CHALK, width=3)
    cx, cy = px + pw / 2, py + ph_ / 2 + 20
    for r_ in (30, 62, 94):
        dashed_circle(d, cx, cy, r_, (255, 196, 70) if r_ == 30 else CHALK, 4)
    d.line([(cx - 120, cy), (cx + 120, cy)], fill=CHALK, width=2); d.line([(cx, cy - 120), (cx, cy + 120)], fill=CHALK, width=2)
    d.line([(cx + 70, cy - 70), (850, 1120)], fill=CHALK, width=3)
    lbl = Image.new('RGBA', (300, 120), (250, 250, 246, 255)); ld = ImageDraw.Draw(lbl)
    ld.text((150, 40), 'TAP x2', font=JB(800, 46), fill=(20, 40, 92), anchor='mm')
    ld.text((150, 88), '= SCREENSHOT', font=JB(700, 28), fill=(30, 74, 160), anchor='mm')
    put(cv, sprite(lbl, border=0, off=(6, 9), blur=6, op=.4), 880, 1080, 3)


def dashed_circle(d, cx, cy, r_, col, wdt, seg=14):
    for k in range(0, 360, seg * 2):
        d.arc((cx - r_, cy - r_, cx + r_, cy + r_), k, k + seg, fill=col, width=wdt)


# ================================================================== THEME C — NEON PAPER
CYAN, MAG, LIME = (0, 230, 255), (255, 46, 170), (170, 255, 60)


def bg_neon():
    cv = base_noise((14, 14, 22), 51, mott=.06, fine=.05, vig=.4)
    d = ImageDraw.Draw(cv)
    for y in range(20, H, 40):
        for x in range(20 + (20 if (y // 40) % 2 else 0), W, 40):
            d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(44, 44, 66))
    # neon tube strips at edges
    for (x0, y0, x1, y1, c) in [(40, 150, 40, 760, MAG), (1040, 1100, 1040, 1780, CYAN), (90, 1860, 520, 1860, CYAN), (640, 60, 1000, 60, MAG)]:
        g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.line([(x0, y0), (x1, y1)], fill=c + (230,), width=30)
        g = g.filter(ImageFilter.GaussianBlur(28))
        cv.alpha_composite(g)
        d.line([(x0, y0), (x1, y1)], fill=tuple(min(255, v + 120) for v in c), width=8)
    return cv


def neon_sprite(img, c, border=0):
    return sprite(img, border=border, off=(6, 9), blur=7, op=.6, glow=(c, .7, 26), paper=(20, 20, 26), tex=True, tex_strength=.5)


def cap_neon(step, text, c=CYAN):
    w, h = 900, 240
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w, h), 22, fill=c)
    d.rounded_rectangle((8, 8, w - 8, h - 8), 16, fill=(16, 16, 24))
    d.text((40, 52), '> ' + step, font=PX(26), fill=MAG, anchor='lm')
    lines = wrap(text, JB(800, 54), 800)
    for i, ln in enumerate(lines[:2]):
        y = 128 + i * 62
        d.text((40, y), ln, font=JB(800, 54), fill=(225, 252, 255), anchor='lm')
    ex = 40 + JB(800, 54).getlength(lines[-1]) + 14
    d.rectangle((ex, 128 + (len(lines) - 1) * 62 - 26, ex + 28, 128 + (len(lines) - 1) * 62 + 24), fill=c)
    return neon_sprite(img, c)


def title_neon(cv):
    tag = Image.new('RGBA', (440, 70), (0, 0, 0, 0)); td = ImageDraw.Draw(tag)
    td.rounded_rectangle((0, 0, 440, 70), 35, fill=LIME)
    td.text((220, 37), 'iPHONE TIP', font=PX(28), fill=(14, 14, 22), anchor='mm')
    put(cv, neon_sprite(tag, LIME), 540, 380, -3)
    for word, y, col, sz, sp_ in [('BACK', 590, MAG, 150, 190), ('TAP', 800, CYAN, 150, 200)]:
        for i, ch in enumerate(word):
            im = Image.new('RGBA', (sz + 40, sz + 40), (0, 0, 0, 0))
            ImageDraw.Draw(im).text(((sz + 40) / 2, (sz + 40) / 2), ch, font=PX(sz), fill=col, anchor='mm')
            im = im.crop(im.getbbox())
            n = len(word)
            put(cv, neon_sprite(im, col), 540 + (i - (n - 1) / 2) * sp_, y, rng_for(word, i).uniform(-5, 5))
    card = Image.new('RGBA', (880, 200), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, 880, 200), 20, fill=MAG); cd.rounded_rectangle((7, 7, 873, 193), 15, fill=(16, 16, 24))
    cd.text((440, 66), '[ hidden iPhone shortcut ]', font=JB(800, 44), fill=(255, 220, 240), anchor='mm')
    cd.text((440, 136), 'tap the back = screenshot', font=JB(600, 36), fill=CYAN, anchor='mm')
    put(cv, neon_sprite(card, MAG), 540, 1040, 1.5)
    mini = phone_raw('back').resize((190, 377), Image.LANCZOS)
    put(cv, sprite(mini, border=6, off=(8, 12), blur=8, op=.5, glow=(CYAN, .6, 26), paper=(30, 30, 40)), 560, 1480, 10)
    neon_rings(cv, 560, 1470)


def neon_rings(cv, x, y, n=3):
    for k in range(n):
        r_ = 70 + 52 * k
        im = Image.new('RGBA', (2 * r_ + 40, 2 * r_ + 40), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((20, 20, 20 + 2 * r_, 20 + 2 * r_), outline=CYAN + (255,), width=12 - 3 * k)
        put(cv, sprite(im, border=0, off=(3, 4), blur=3, op=.4, glow=(CYAN, .8, 18), tex=False), x, y)


def neon_word(cv, txt, x, y, c, rot):
    f = PX(64)
    w = int(f.getlength(txt)) + 60
    im = Image.new('RGBA', (w, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w, 110), 18, fill=c)
    d.text((w / 2, 58), txt, font=f, fill=(14, 14, 22), anchor='mm')
    put(cv, neon_sprite(im, c), x, y, rot)


# ================================================================== frames
def step_spec():
    return dict(name='touch', scroll=430, hl='backtap', ov={})


def frame(theme, kind):
    if theme == 'pcb':
        cv = bg_pcb()
    elif theme == 'blue':
        cv = bg_blue(with_dims=(kind != 'title'))
    else:
        cv = bg_neon()
    if kind == 'title':
        {'pcb': title_pcb, 'blue': title_blue, 'neon': title_neon}[theme](cv)
        return cv
    if kind == 'step':
        sp = step_spec()
        put(cv, phone_sprite(theme, 'front', sp), PHX, PHY)
        tx, ty = s2c(*row_point(sp, 'backtap'))
        if theme == 'neon':
            neon_rings(cv, tx, ty, 1)
        elif theme == 'blue':
            d = ImageDraw.Draw(cv); dashed_circle(d, tx, ty, 56, (255, 196, 70), 6)
        else:
            arcs(cv, tx + 30, ty - 10, COPPER, 'r', n=2, start=70, gap=40)
        draw_hand(cv, hand_sprite(theme, press=True), tx, ty)
        cap = {'pcb': lambda: cap_pcb('STEP_04/06', 'Scroll down, tap Back Tap'),
               'blue': lambda: cap_blue('FIG. 04  /  STEP 4 OF 6', 'Scroll down, tap Back Tap'),
               'neon': lambda: cap_neon('STEP 04/06', 'Scroll down, tap Back Tap')}[theme]()
        put(cv, cap, 540, 300, -1.2)
        return cv
    if kind == 'demo':
        put(cv, phone_sprite(theme, 'back'), PHX, PHY)
        bx, by = s2c(300, 640)
        if theme == 'pcb':
            arcs(cv, bx - 40, by, COPPER, 'l', start=110, gap=50)
            arcs(cv, bx + 40, by, COPPER, 'r', start=110, gap=50)
            tag = Image.new('RGBA', (300, 110), (28, 28, 33, 255)); td = ImageDraw.Draw(tag)
            td.text((150, 56), 'TAP x2', font=JB(800, 58), fill=(90, 255, 160), anchor='mm')
            put(cv, sprite(tag, border=0, off=(7, 10), blur=6, op=.45), 300, 1430, -8)
            put(cv, cap_pcb('RUN', 'Double-tap the back of your iPhone'), 540, 300, 1)
        elif theme == 'blue':
            d = ImageDraw.Draw(cv)
            for r_ in (60, 105, 150):
                dashed_circle(d, bx, by, r_, CHALK if r_ > 60 else (255, 196, 70), 5)
            d.line([(bx - 110, by - 110), (250, 1360)], fill=CHALK, width=3)
            lbl = Image.new('RGBA', (300, 120), (250, 250, 246, 255)); ld = ImageDraw.Draw(lbl)
            ld.text((150, 40), 'TAP x2', font=JB(800, 46), fill=(20, 40, 92), anchor='mm')
            ld.text((150, 88), 'anywhere on back', font=JB(600, 24), fill=(30, 74, 160), anchor='mm')
            put(cv, sprite(lbl, border=0, off=(6, 9), blur=6, op=.4), 240, 1310, -3)
            put(cv, cap_blue('FIG. 07  /  TEST', 'Double-tap the back of your iPhone'), 540, 300, 1)
        else:
            neon_rings(cv, bx, by, 3)
            neon_word(cv, 'TAP', 250, 1330, CYAN, -10)
            neon_word(cv, 'TAP', 830, 1250, MAG, 8)
            put(cv, cap_neon('RUN', 'Double-tap the back of your iPhone', MAG), 540, 300, 1)
        draw_hand(cv, hand_sprite(theme, press=True), bx, by)
        return cv


def board(theme, title, sub, accent):
    frames = [frame(theme, k).convert('RGB') for k in ('title', 'step', 'demo')]
    fw, fh = 560, 996
    gap = 24
    bw = 3 * fw + 4 * gap
    bh = fh + 170
    b = Image.new('RGB', (bw, bh), (18, 18, 22))
    d = ImageDraw.Draw(b)
    d.text((gap, 56), title, font=JB(800, 46), fill=accent, anchor='lm')
    d.text((gap, 108), sub, font=JB(500, 26), fill=(190, 190, 200), anchor='lm')
    for i, (f, lab) in enumerate(zip(frames, ['01  Title', '02  Step', '03  Demo'])):
        x = gap + i * (fw + gap)
        b.paste(f.resize((fw, fh), Image.LANCZOS), (x, 150))
        d.rounded_rectangle((x + 14, 164, x + 160, 204), 10, fill=(18, 18, 22))
        d.text((x + 26, 184), lab, font=JB(700, 22), fill=(230, 230, 236), anchor='lm')
    return b, frames


if __name__ == '__main__':
    out = __import__('lib').out('styleframes')
    import os
    os.makedirs(out, exist_ok=True)
    for th, t, s, a in [('pcb', 'A · CIRCUIT BOARD', 'Paper-cut copper traces, chips & LEDs on a green PCB · keycap title · chip-shaped captions', (90, 255, 160)),
                        ('blue', 'B · BLUEPRINT', 'Engineering drawing: grid paper, chalk dimensions, stencil title · taped spec labels', (255, 196, 70)),
                        ('neon', 'C · NEON PAPER', 'Back-lit cut paper on black · glowing edges, pixel title · terminal-style captions', (0, 230, 255))]:
        if len(sys.argv) > 1 and th not in sys.argv[1:]:
            continue
        b, frames = board(th, t, s, a)
        b.save(f'{out}/{th}_board.png')
        for k, f in zip(('title', 'step', 'demo'), frames):
            f.save(f'{out}/{th}_{k}.png')
        print('done', th)

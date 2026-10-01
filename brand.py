"""Tech Wall — Facebook profile picture + cover photo (Blueprint style)"""
import sys, math, random
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import themes as th
from lib import noise_L, rotate_sprite, blit, draw_sprite

OUT = __import__('lib').out('brand')
NAVY, MID, YEL, PAPER, CHALK = (20, 40, 92), (30, 74, 160), (255, 196, 70), (250, 250, 246), th.CHALK


def wall(w, h, seed=3):
    """dark painted plaster wall"""
    b = np.zeros((h, w, 3), np.float32); b[:] = (34, 40, 54)
    m = np.asarray(noise_L(w // 6, h // 6, seed, 70, 2).resize((w, h), Image.BICUBIC), np.float32)[..., None] - 128
    f = np.asarray(noise_L(w, h, seed + 1, 40, .7), np.float32)[..., None] - 128
    b += m * .10 + f * .07
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dd = np.sqrt(((xx - w / 2) / (w * .7)) ** 2 + ((yy - h / 2) / (h * .8)) ** 2)
    b *= np.clip(1 - .35 * dd ** 2, .5, 1)[..., None]
    # soft spotlight from top
    b += (np.exp(-(((xx - w / 2) / (w * .45)) ** 2 + ((yy + h * .15) / (h * .9)) ** 2)) * 26)[..., None]
    return Image.fromarray(np.clip(b, 0, 255).astype(np.uint8)).convert('RGBA')


def grid_paper(w, h, seed=1, minor=24):
    b = np.zeros((h, w, 3), np.float32); b[:] = (28, 66, 134)
    f = np.asarray(noise_L(w, h, seed, 40, .6), np.float32)[..., None] - 128
    m = np.asarray(noise_L(max(2, w // 8), max(2, h // 8), seed + 2, 60, 2).resize((w, h), Image.BICUBIC), np.float32)[..., None] - 128
    b += f * .08 + m * .10
    img = Image.fromarray(np.clip(b, 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(img)
    for x in range(0, w, minor):
        maj = (x // minor) % 5 == 0
        d.line([(x, 0), (x, h)], fill=(84, 128, 198) if maj else (54, 94, 164), width=2 if maj else 1)
    for y in range(0, h, minor):
        maj = (y // minor) % 5 == 0
        d.line([(0, y), (w, y)], fill=(84, 128, 198) if maj else (54, 94, 164), width=2 if maj else 1)
    return img


def chalk(d, kind, x, y, s):
    """chalk schematic inside box (x,y,s,s)"""
    C = CHALK
    cx, cy = x + s / 2, y + s / 2
    if kind == 'phone':
        pw, ph = s * .42, s * .82
        d.rounded_rectangle((cx - pw / 2, cy - ph / 2, cx + pw / 2, cy + ph / 2), int(s * .07), outline=C, width=4)
        d.rounded_rectangle((cx - pw / 2 + 10, cy - ph / 2 + 10, cx - pw / 2 + s * .17, cy - ph / 2 + s * .17), 12, outline=C, width=3)
        for r_ in (s * .05, s * .1, s * .15):
            th.dashed_circle(d, cx, cy + s * .08, r_, YEL if r_ < s * .06 else C, 3, seg=16)
        d.line([(cx - s * .22, cy + s * .08), (cx + s * .22, cy + s * .08)], fill=C, width=2)
        d.line([(cx, cy - s * .14), (cx, cy + s * .3)], fill=C, width=2)
    elif kind == 'gear':
        pts = []
        for i in range(48):
            a = i * math.pi / 24
            r_ = s * (.3 if (i // 3) % 2 == 0 else .24)
            pts.append((cx + r_ * math.cos(a), cy + r_ * math.sin(a)))
        d.polygon(pts, outline=C, width=4)
        d.ellipse((cx - s * .1, cy - s * .1, cx + s * .1, cy + s * .1), outline=C, width=4)
        d.line([(cx - s * .42, cy), (cx + s * .42, cy)], fill=C, width=2)
        d.line([(cx, cy - s * .42), (cx, cy + s * .42)], fill=C, width=2)
        th.dashed_circle(d, cx, cy, s * .38, C, 2, seg=10)
    elif kind == 'wifi':
        for k, r_ in enumerate((s * .36, s * .25, s * .14)):
            d.arc((cx - r_, cy - r_ + s * .12, cx + r_, cy + r_ + s * .12), 220, 320, fill=C, width=6)
        d.ellipse((cx - 10, cy + s * .1, cx + 10, cy + s * .1 + 20), fill=YEL)
        d.line([(cx - s * .4, cy + s * .34), (cx + s * .4, cy + s * .34)], fill=C, width=2)
    elif kind == 'battery':
        bw, bh = s * .6, s * .32
        d.rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), 14, outline=C, width=5)
        d.rectangle((cx + bw / 2, cy - bh * .2, cx + bw / 2 + 12, cy + bh * .2), fill=C)
        for i in range(4):
            x0 = cx - bw / 2 + 14 + i * (bw - 28) / 4
            d.rectangle((x0 + 4, cy - bh / 2 + 14, x0 + (bw - 28) / 4 - 4, cy + bh / 2 - 14), fill=YEL if i < 3 else None, outline=C, width=2)
        d.line([(cx - bw / 2, cy + bh / 2 + 30), (cx + bw / 2, cy + bh / 2 + 30)], fill=C, width=2)
        for xx in (cx - bw / 2, cx + bw / 2):
            d.line([(xx, cy + bh / 2 + 18), (xx, cy + bh / 2 + 42)], fill=C, width=2)
    elif kind == 'gamepad':
        bw, bh = s * .9, s * .5
        x0, y0 = cx - bw / 2, cy - bh / 2
        u = s / 100
        d.rounded_rectangle((x0 + bw * .1, y0, x0 + bw * .9, y0 + bh * .62), int(bh * .28), outline=C, width=4)
        d.ellipse((x0, y0 + bh * .18, x0 + bw * .34, y0 + bh), outline=C, width=4)
        d.ellipse((x0 + bw * .66, y0 + bh * .18, x0 + bw, y0 + bh), outline=C, width=4)
        dx, dy = x0 + bw * .2, y0 + bh * .4
        d.rectangle((dx - 8 * u, dy - 2.6 * u, dx + 8 * u, dy + 2.6 * u), fill=C); d.rectangle((dx - 2.6 * u, dy - 8 * u, dx + 2.6 * u, dy + 8 * u), fill=C)
        bx, by = x0 + bw * .8, y0 + bh * .4
        for ox, oy, col in [(0, -7, C), (7, 0, YEL), (0, 7, C), (-7, 0, C)]:
            d.ellipse((bx + (ox - 3) * u, by + (oy - 3) * u, bx + (ox + 3) * u, by + (oy + 3) * u), outline=col, width=3)
        for sx_ in (x0 + bw * .37, x0 + bw * .63):
            d.ellipse((sx_ - 6 * u, y0 + bh * .66 - 6 * u, sx_ + 6 * u, y0 + bh * .66 + 6 * u), outline=C, width=3)
        d.line([(x0 + bw * .1, y0 + bh + 10 * u), (x0 + bw * .9, y0 + bh + 10 * u)], fill=C, width=2)
    elif kind == 'laptop':
        sw_, sh_ = s * .66, s * .42
        d.rounded_rectangle((cx - sw_ / 2, cy - sh_ * .75, cx + sw_ / 2, cy + sh_ * .25), 12, outline=C, width=4)
        d.rectangle((cx - sw_ / 2 + 16, cy - sh_ * .75 + 16, cx + sw_ / 2 - 16, cy + sh_ * .25 - 16), outline=C, width=2)
        d.polygon([(cx - sw_ / 2 - 20, cy + sh_ * .3), (cx + sw_ / 2 + 20, cy + sh_ * .3), (cx + sw_ / 2 + 44, cy + sh_ * .48), (cx - sw_ / 2 - 44, cy + sh_ * .48)], outline=C, width=4)
        for i in range(3):
            yy = cy - sh_ * .55 + i * 30
            d.line([(cx - sw_ / 2 + 30, yy), (cx - sw_ / 2 + 30 + sw_ * [.4, .58, .3][i], yy)], fill=YEL if i == 1 else C, width=4)
        d.text((cx + sw_ / 2 - 40, cy - sh_ * .52), '>_', font=th.JB(800, 26), fill=C, anchor='rm')
    elif kind == 'tablet':
        pw, ph = s * .62, s * .8
        d.rounded_rectangle((cx - pw / 2, cy - ph / 2, cx + pw / 2, cy + ph / 2), int(s * .06), outline=C, width=4)
        d.rounded_rectangle((cx - pw / 2 + 14, cy - ph / 2 + 14, cx + pw / 2 - 14, cy + ph / 2 - 14), int(s * .04), outline=C, width=2)
        for i in range(3):
            for j in range(4):
                gx = cx - pw / 2 + 34 + i * (pw - 68) / 2.6
                gy = cy - ph / 2 + 36 + j * (ph - 90) / 4.2
                d.rounded_rectangle((gx, gy, gx + 30, gy + 30), 8, outline=YEL if (i, j) == (1, 2) else C, width=2)
        d.line([(cx - 40, cy + ph / 2 - 26), (cx + 40, cy + ph / 2 - 26)], fill=C, width=4)
    elif kind == 'headset':
        r_ = s * .3
        d.arc((cx - r_, cy - r_ - s * .05, cx + r_, cy + r_ - s * .05), 180, 360, fill=C, width=6)
        for sx_ in (cx - r_, cx + r_):
            d.rounded_rectangle((sx_ - 26, cy - s * .08, sx_ + 26, cy + s * .2), 20, outline=C, width=4)
        d.line([(cx - r_ + 10, cy + s * .14), (cx - s * .05, cy + s * .3)], fill=C, width=3)
        d.ellipse((cx - s * .05 - 10, cy + s * .3 - 10, cx - s * .05 + 10, cy + s * .3 + 10), fill=YEL)
    elif kind == 'screen':
        pw, ph = s * .44, s * .82
        d.rounded_rectangle((cx - pw / 2, cy - ph / 2, cx + pw / 2, cy + ph / 2), int(s * .07), outline=C, width=4)
        d.rounded_rectangle((cx - s * .06, cy - ph / 2 + 12, cx + s * .06, cy - ph / 2 + 30), 9, fill=C)
        for i in range(6):
            yy = cy - ph / 2 + s * .14 + i * s * .1
            d.rounded_rectangle((cx - pw / 2 + 14, yy, cx - pw / 2 + 36, yy + 22), 6, outline=C, width=2)
            d.line([(cx - pw / 2 + 46, yy + 11), (cx + pw / 2 - 30 - (i % 3) * 20, yy + 11)], fill=YEL if i == 3 else C, width=4)


def sheet(w, h, kind, code, title, seed, rot):
    img = grid_paper(w, h, seed)
    d = ImageDraw.Draw(img)
    d.rectangle((10, 10, w - 10, h - 10), outline=CHALK, width=3)
    s = min(w, h - 70) * .9
    chalk(d, kind, (w - s) / 2, 18 + (h - 70 - s) / 2, s)
    d.line([(10, h - 56), (w - 10, h - 56)], fill=CHALK, width=2)
    d.text((24, h - 32), code, font=th.JB(700, 22), fill=CHALK, anchor='lm')
    d.text((w - 24, h - 32), title, font=th.JB(800, 24), fill=YEL, anchor='rm')
    sp = th.sprite(img, border=0, off=(10, 16), blur=12, op=.55, tex=True, tex_strength=.6)
    return rotate_sprite(sp, rot)


def tape(body_img, x, y, ang, w=150):
    tp = Image.new('RGBA', (w, 44), (232, 216, 168, 205)).rotate(ang, expand=True, resample=Image.BICUBIC)
    body_img.alpha_composite(tp, (int(x - tp.width / 2), int(y - tp.height / 2)))


def pin(cv, x, y, col=YEL):
    g = Image.new('RGBA', (60, 60), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((14, 18, 46, 50), fill=(0, 0, 0, 120)); g = g.filter(ImageFilter.GaussianBlur(4))
    blit(cv, g, x - 26, y - 26)
    d = ImageDraw.Draw(cv)
    d.ellipse((x - 15, y - 15, x + 15, y + 15), fill=col)
    d.ellipse((x - 8, y - 10, x + 0, y - 2), fill=tuple(min(255, v + 50) for v in col))


def stencil(ch, size, col):
    f = th.STN(size)
    bb = f.getbbox(ch)
    im = Image.new('RGBA', (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - bb[0], 10 - bb[1]), ch, font=f, fill=col)
    return th.sprite(im, border=0, off=(7, 11), blur=7, op=.55)


def strip(text, font, bg, fg, rot, padx=36, pady=20):
    w = int(font.getlength(text) + 2 * padx); h = int(font.size * 1.25 + 2 * pady)
    im = Image.new('RGBA', (w, h), bg + (255,))
    ImageDraw.Draw(im).text((w / 2, h / 2), text, font=font, fill=fg, anchor='mm')
    return rotate_sprite(th.sprite(im, border=0, off=(7, 11), blur=7, op=.5), rot)


def place(cv, sp, x, y):
    draw_sprite(cv, sp, x, y)


# ======================================================================= COVER 1640x624
def cover():
    W, H = 1640, 624
    cv = wall(W, H)
    # sheets — left & right clusters (mobile crop keeps centre ~1110px)
    sheets = [
        ('tablet', 'TW-02', 'TABLET', 270, 320, 300, 470, 6, 2),
        ('phone', 'TW-01', 'PHONE', 300, 400, 125, 215, -6, 1),
        ('headset', 'TW-05', 'GEAR', 240, 290, 1570, 480, -8, 4),
        ('gamepad', 'TW-03', 'GAMES', 340, 300, 1465, 175, 5, 3),
        ('laptop', 'TW-04', 'PC', 320, 280, 1345, 480, -4, 5),
    ]
    for kind, code, title, w, h, x, y, rot, seed in sheets:
        sp = sheet(w, h, kind, code, title, seed, rot)
        sh, body = sp
        body = body.copy()
        if seed % 2:
            tape(body, body.width / 2, (body.height - h) / 2 + 22, rot * .5 - 3)
        place(cv, (sh, body), x, y)
        if seed % 2 == 0:
            pin(cv, int(x + math.sin(math.radians(rot)) * h * .42), int(y - h * .42), YEL)
    # title
    letters = 'TECH WALL'
    size = 150
    sps = [None if c == ' ' else stencil(c, size, PAPER if i < 4 else YEL) for i, c in enumerate(letters)]
    adv = [size * .32 if c == ' ' else th.STN(size).getlength(c) + 10 for c in letters]
    total = sum(adv)
    x = W / 2 - total / 2
    r = random.Random(4)
    for c, sp, a in zip(letters, sps, adv):
        if sp:
            place(cv, rotate_sprite(sp, r.uniform(-3, 3)), x + a / 2, 250 + r.uniform(-6, 6))
        x += a
    place(cv, strip('Everything tech, pinned to one wall', th.JB(800, 38), PAPER, NAVY, -1.5), W / 2, 412)
    place(cv, strip('PHONES · TABLETS · PCs · CONSOLES · GAMES', th.JB(800, 26), YEL, NAVY, 1.5, padx=24, pady=12), W / 2 + 60, 500)
    # chalk scribble arrow from tagline toward phone sheet
    return cv


# ======================================================================= PROFILE 720x720
def profile():
    S = 720
    cv = grid_paper(S, S, seed=9, minor=36)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    dd = np.sqrt(((xx - S / 2) / (S * .6)) ** 2 + ((yy - S / 2) / (S * .6)) ** 2)
    arr = np.asarray(cv.convert('RGB'), np.float32) * np.clip(1 - .45 * dd ** 2, .5, 1)[..., None]
    cv = Image.fromarray(arr.astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(cv)
    c = S / 2
    th.dashed_circle(d, c, c - 20, 270, CHALK, 5, seg=10)
    for a in range(0, 360, 90):
        ra = math.radians(a)
        d.line([(c + 250 * math.cos(ra), c - 20 + 250 * math.sin(ra)), (c + 300 * math.cos(ra), c - 20 + 300 * math.sin(ra))], fill=CHALK, width=5)
    sT = stencil('T', 330, PAPER); sW = stencil('W', 330, YEL)
    place(cv, rotate_sprite(sT, -4), c - 112, c - 40)
    place(cv, rotate_sprite(sW, 3), c + 96, c - 26)
    place(cv, strip('TECH WALL', th.JB(800, 50), PAPER, NAVY, -2, padx=30, pady=12), c, c + 190)
    return cv


def profile_alt():
    S = 720
    cv = grid_paper(S, S, seed=11, minor=36)
    d = ImageDraw.Draw(cv)
    c = S / 2
    pw, ph = 250, 470
    d.rounded_rectangle((c - pw / 2, c - ph / 2 - 30, c + pw / 2, c + ph / 2 - 30), 46, outline=CHALK, width=9)
    d.rounded_rectangle((c - pw / 2 + 22, c - ph / 2 - 8, c - pw / 2 + 112, c - ph / 2 + 82), 24, outline=CHALK, width=6)
    for r_ in (30, 62, 94):
        th.dashed_circle(d, c, c + 30, r_, YEL if r_ == 30 else CHALK, 7, seg=16)
    d.ellipse((c - 12, c + 18, c + 12, c + 42), fill=YEL)
    place(cv, strip('TECH WALL', th.JB(800, 50), PAPER, NAVY, -2, padx=30, pady=12), c, c + 250)
    return cv


def mock(cov, prof):
    """page preview: cover with circular avatar overlap (generic, no platform UI)"""
    W = 1640
    m = Image.new('RGB', (W, 624 + 260), (24, 25, 28))
    m.paste(cov.convert('RGB'), (0, 0))
    size = 300
    av = prof.convert('RGB').resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0); ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    ring = Image.new('L', (size + 16, size + 16), 0); ImageDraw.Draw(ring).ellipse((0, 0, size + 15, size + 15), fill=255)
    m.paste((24, 25, 28), (60, 624 - 150, 60 + size + 16, 624 - 150 + size + 16), ring)
    m.paste(av, (68, 624 - 142), mask)
    d = ImageDraw.Draw(m)
    d.text((400, 680), 'Tech Wall', font=th.JB(800, 64), fill=(240, 240, 245), anchor='lm')
    d.text((402, 750), 'Everything tech, pinned to one wall', font=th.JB(500, 30), fill=(170, 172, 180), anchor='lm')
    # mobile safe-zone guide
    sx = (W - 1110) // 2
    for x in (sx, W - sx):
        for y in range(0, 624, 24):
            d.line([(x, y), (x, y + 12)], fill=(255, 196, 70), width=2)
    d.text((W - sx - 10, 22), 'mobile crop', font=th.JB(600, 20), fill=(255, 196, 70), anchor='rm')
    return m


if __name__ == '__main__':
    import os
    os.makedirs(OUT, exist_ok=True)
    cov = cover(); cov.convert('RGB').save(f'{OUT}/TechWall_cover_1640x624.png')
    pr = profile(); pr.convert('RGB').save(f'{OUT}/TechWall_profile_720.png')
    pa = profile_alt(); pa.convert('RGB').save(f'{OUT}/TechWall_profile_alt_720.png')
    mock(cov, pr).save(f'{OUT}/TechWall_page_preview.png')
    print('ok')

import math
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from screens import SW, SH, glyph, BLUE, GRAYI

PW, PH = 600, 1224
INK = (52, 38, 28)


# ---------------------------------------------------------------- phone
def phone_raw(side):
    img = Image.new('RGBA', (PW + 16, PH), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if side == 'front':
        body, rim, btn = (38, 38, 44), (78, 78, 88), (60, 60, 68)
        left = [(250, 312), (390, 492), (520, 622)]; right = [(420, 580)]
    else:
        body, rim, btn = (162, 198, 228), (130, 166, 200), (140, 176, 208)
        left = [(420, 580)]; right = [(250, 312), (390, 492), (520, 622)]
    for a, b in left:
        d.rounded_rectangle((0, a, 16, b), 5, fill=btn)
    for a, b in right:
        d.rounded_rectangle((PW, a, PW + 16, b), 5, fill=btn)
    d.rounded_rectangle((8, 0, PW + 8, PH - 1), 92, fill=body)
    d.rounded_rectangle((14, 6, PW + 2, PH - 7), 86, outline=rim, width=4)
    if side == 'back':
        bx, by = 40, 40
        d.rounded_rectangle((bx, by, bx + 236, by + 236), 64, fill=(148, 184, 216), outline=(120, 156, 190), width=4)
        for cx, cy in [(bx + 70, by + 70), (bx + 70, by + 168)]:
            d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=(120, 150, 180))
            d.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), fill=(28, 30, 36))
            d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=(52, 60, 82))
            d.ellipse((cx - 12, cy - 22, cx, cy - 10), fill=(140, 160, 200))
        d.ellipse((bx + 168, by + 52, bx + 204, by + 88), fill=(250, 240, 205))
        d.ellipse((bx + 176, by + 158, bx + 196, by + 178), fill=(40, 44, 52))
    return img


SCREEN_MASK = None


def screen_mask():
    global SCREEN_MASK
    if SCREEN_MASK is None:
        m = Image.new('L', (SW, SH), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), 74, fill=255)
        SCREEN_MASK = m
    return SCREEN_MASK


# ---------------------------------------------------------------- hand
def hand_raw():
    w, h = 430, 800
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    skin, line = (243, 196, 158), (196, 132, 92)
    d.ellipse((0, 430, 130, 650), fill=skin, outline=line, width=5)                     # thumb
    d.rounded_rectangle((30, 360, 410, 760), 150, fill=skin, outline=line, width=5)     # palm
    for x0, y0 in [(160, 330), (240, 352), (318, 384)]:                                 # curled fingers
        d.rounded_rectangle((x0, y0, x0 + 92, y0 + 140), 46, fill=skin, outline=line, width=5)
    d.rounded_rectangle((62, 0, 160, 470), 49, fill=skin, outline=line, width=5)         # index finger
    d.rounded_rectangle((82, 16, 140, 96), 27, fill=(252, 224, 210), outline=(214, 156, 124), width=4)
    for yy in (215, 305):
        d.arc((86, yy - 12, 136, yy + 12), 200, 340, fill=line, width=4)
    d.rounded_rectangle((18, 650, 422, 800), 20, fill=(64, 170, 160), outline=(40, 120, 115), width=5)  # sleeve
    for i in range(6):
        d.line([(40 + 66 * i, 668), (40 + 66 * i, 790)], fill=(54, 150, 142), width=4)
    return img, (111, 4)


def hand_sprites():
    raw, tip = hand_raw()
    S = 1900
    big = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    big.paste(raw, (S // 2 - tip[0], S // 2 - tip[1]))
    big = big.rotate(24, resample=Image.BICUBIC)
    bb = big.getbbox()
    big = big.crop(bb)
    tip_local = (S // 2 - bb[0], S // 2 - bb[1])
    out = {}
    for name, off, blur, op in [('hover', (34, 46), 16, 0.30), ('press', (8, 11), 5, 0.42)]:
        sh, body = make_sprite(big, border=9, off=off, blur=blur, op=op)
        p = (body.width - big.width) // 2
        bb2 = Image.alpha_composite(sh, body).getbbox()
        sh, body = sh.crop(bb2), body.crop(bb2)
        out[name] = (sh, body, (tip_local[0] + p - bb2[0], tip_local[1] + p - bb2[1]))
    return out


# ---------------------------------------------------------------- paper notes / strips
def note_sprite(badge, text, col, rot):
    w, h = 900, 260
    img = Image.new('RGBA', (w, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 30, w, h + 30), fill=col)
    # badge
    d.ellipse((40, 30 + h / 2 - 66, 172, 30 + h / 2 + 66), fill=INK)
    bc = (106, 30 + h / 2)
    if badge == 'check':
        d.line([(bc[0] - 30, bc[1] + 2), (bc[0] - 8, bc[1] + 26), (bc[0] + 34, bc[1] - 28)], fill=(255, 255, 255), width=14, joint='curve')
    else:
        d.text(bc, badge, font=F(700, 80), fill=(255, 255, 255), anchor='mm')
    size = 60
    lines = wrap(text, F(600, size), 660)
    if len(lines) > 2:
        size = 50; lines = wrap(text, F(600, size), 660)
    lh = size * 1.12
    y0 = 30 + h / 2 - lh * len(lines) / 2 + lh / 2
    for i, ln in enumerate(lines):
        d.text((210, y0 + i * lh), ln, font=F(600, size), fill=INK, anchor='lm')
    # tape
    tape = Image.new('RGBA', (220, 64), (250, 246, 232, 175))
    tape = tape.rotate(-4, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(tape, (w // 2 - tape.width // 2, 0))
    sp = make_sprite(img, border=0, off=(9, 13), blur=9, op=0.36)
    return rotate_sprite(sp, rot)


def strip_sprite(text, font, bg, fg, rot, padx=40, pady=26, border=0):
    tw = font.getlength(text)
    bb = font.getbbox(text)
    th = bb[3] - bb[1]
    w, h = int(tw + 2 * padx), int(th + 2 * pady)
    img = Image.new('RGBA', (w, h), bg + (255,))
    d = ImageDraw.Draw(img)
    d.text((w / 2, h / 2), text, font=font, fill=fg, anchor='mm')
    # torn-ish edges: notch the ends
    r = rng_for('strip', text)
    m = Image.new('L', (w, h), 255)
    md = ImageDraw.Draw(m)
    for x in (0, w):
        pts = []
        for i in range(9):
            yy = h * i / 8
            pts.append((x + (r.uniform(0, 9) if x == 0 else -r.uniform(0, 9)), yy))
        poly = [(x, 0)] + pts + [(x, h)]
        md.polygon(poly, fill=0)
    img.putalpha(m)
    sp = make_sprite(img, border=border, off=(7, 10), blur=7, op=0.36)
    return rotate_sprite(sp, rot)


def tile_sprite(ch, col, rot):
    s = 150
    img = Image.new('RGBA', (s, s), col + (255,))
    d = ImageDraw.Draw(img)
    d.text((s / 2 + 3, s / 2 + 5), ch, font=F(700, 112), fill=(0, 0, 0, 60), anchor='mm')
    d.text((s / 2, s / 2), ch, font=F(700, 112), fill=(255, 255, 255), anchor='mm')
    sp = make_sprite(img, border=0, off=(8, 12), blur=8, op=0.38)
    return rotate_sprite(sp, rot)


def ring_sprites():
    out = []
    for r_, wdt in [(30, 12), (50, 10), (70, 7)]:
        s = 2 * r_ + 20
        img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
        ImageDraw.Draw(img).ellipse((10, 10, s - 10, s - 10), outline=(255, 255, 255, 255), width=wdt)
        out.append(make_sprite(img, border=0, off=(4, 6), blur=4, op=0.35, tex=False))
    return out


def burst_sprite(text, rot, col=(245, 183, 64)):
    s = 330
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = []
    for i in range(24):
        a = i * math.pi / 12
        rr = 150 if i % 2 == 0 else 108
        pts.append((s / 2 + rr * math.cos(a), s / 2 + rr * math.sin(a) * 0.82))
    d.polygon(pts, fill=col + (255,))
    d.text((s / 2, s / 2), text, font=M(78), fill=INK, anchor='mm')
    sp = make_sprite(img, border=7, off=(7, 10), blur=6, op=0.36)
    return rotate_sprite(sp, rot)


def chip_sprite(label, icol, gl, rot, hot=False):
    font = F(600, 60)
    tw = font.getlength(label)
    w, h = int(tw + 200), 132
    bg = (240, 98, 85) if hot else (255, 253, 248)
    fg = (255, 255, 255) if hot else INK
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=bg)
    d.rounded_rectangle((30, 26, 110, 106), 20, fill=icol)
    glyph(d, gl, 30, 26, 80)
    d.text((140, h / 2), label, font=font, fill=fg, anchor='lm')
    sp = make_sprite(img, border=6, off=(8, 12), blur=8, op=0.36)
    return rotate_sprite(sp, rot)


def arrow_sprite(rot):
    img = Image.new('RGBA', (90, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.line([(45, 6), (40, 40), (46, 96)], fill=INK, width=12, joint='curve')
    d.polygon([(18, 76), (74, 74), (46, 114)], fill=INK)
    sp = make_sprite(img, border=6, off=(5, 7), blur=5, op=0.3)
    return rotate_sprite(sp, rot)

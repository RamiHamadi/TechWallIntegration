import math, random, zlib, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 1080, 1920
FPS = 12
KIT = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(KIT, 'fonts') + '/'


def out(name):
    """path inside <kit>/out"""
    os.makedirs(os.path.join(KIT, 'out'), exist_ok=True)
    return os.path.join(KIT, 'out', name)
_fc = {}


def F(w, s):
    k = ('f', w, s)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(f'{FD}fredoka-latin-{w}-normal.woff', s)
    return _fc[k]


def M(s):
    k = ('m', s)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(f'{FD}marker.woff', s)
    return _fc[k]


def rng_for(*keys):
    return random.Random(zlib.crc32(repr(keys).encode()))


# ---------------------------------------------------------------- textures
def noise_L(w, h, seed, amp, blur):
    r = np.random.default_rng(seed)
    n = r.normal(0, 1, (h, w)).astype(np.float32)
    img = Image.fromarray(np.clip(128 + n * amp, 0, 255).astype(np.uint8), 'L')
    return img.filter(ImageFilter.GaussianBlur(blur)) if blur else img


def paper_tex(w, h, seed=1, strength=1.0):
    """multiply texture, values near 255"""
    fine = np.asarray(noise_L(w, h, seed, 40, 0.7), np.float32) - 128
    mott = np.asarray(noise_L(w // 8 + 1, h // 8 + 1, seed + 1, 60, 2).resize((w, h), Image.BICUBIC), np.float32) - 128
    v = 250 + (fine * 0.18 + mott * 0.12) * strength
    return Image.fromarray(np.clip(v, 0, 255).astype(np.uint8), 'L')


def apply_tex(img, tex):
    """multiply RGB of RGBA img by L texture"""
    rgb = img.convert('RGB')
    t = Image.merge('RGB', (tex, tex, tex))
    out = ImageChops.multiply(rgb, t)
    if img.mode == 'RGBA':
        out.putalpha(img.split()[3])
    return out


def make_background():
    base = np.zeros((H, W, 3), np.float32)
    base[:] = (214, 184, 143)
    mott = np.asarray(noise_L(W // 10, H // 10, 7, 70, 2).resize((W, H), Image.BICUBIC), np.float32)[..., None] - 128
    fine = np.asarray(noise_L(W, H, 8, 40, 0.6), np.float32)[..., None] - 128
    base += mott * 0.16 + fine * 0.10
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGB')
    d = ImageDraw.Draw(img)
    r = random.Random(3)
    for _ in range(900):  # paper fibres
        x, y = r.uniform(0, W), r.uniform(0, H)
        a = r.uniform(0, math.pi)
        L = r.uniform(6, 22)
        c = r.choice([(188, 156, 116), (230, 204, 166), (196, 165, 125)])
        d.line([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], fill=c, width=1)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dd = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
    vig = np.clip(1.0 - 0.32 * dd ** 2.2, 0.55, 1)[..., None]
    arr = np.asarray(img, np.float32) * vig
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    # a few confetti paper dots in corners (static set dressing)
    for i in range(14):
        rr = random.Random(100 + i)
        cx = rr.choice([rr.uniform(20, 160), rr.uniform(920, 1060)])
        cy = rr.uniform(60, 1860)
        rad = rr.uniform(10, 22)
        col = rr.choice(PALETTE)
        dot = Image.new('RGBA', (int(rad * 2 + 4),) * 2, (0, 0, 0, 0))
        ImageDraw.Draw(dot).ellipse((2, 2, rad * 2 + 2, rad * 2 + 2), fill=col + (255,))
        sh, body = make_sprite(dot, border=0, off=(3, 4), blur=3, op=0.35)
        blit(img, sh, cx - sh.width / 2, cy - sh.height / 2)
        blit(img, body, cx - sh.width / 2, cy - sh.height / 2)
    return img


PALETTE = [(240, 98, 85), (245, 183, 64), (64, 170, 160), (80, 130, 220),
           (235, 120, 170), (120, 190, 90), (150, 110, 210)]


# ---------------------------------------------------------------- sprites
def pad(img, p):
    n = Image.new('RGBA', (img.width + 2 * p, img.height + 2 * p), (0, 0, 0, 0))
    n.paste(img, (p, p))
    return n


def cutout(img, border=8, paper=(252, 249, 242)):
    img = pad(img, border + 6)
    if border <= 0:
        return img
    a = img.split()[3]
    ea = a.filter(ImageFilter.GaussianBlur(border * 0.55)).point(lambda v: 255 if v > 6 else 0)
    ea = ea.filter(ImageFilter.GaussianBlur(0.9))
    base = Image.new('RGBA', img.size, paper + (255,))
    base.putalpha(ea)
    base.alpha_composite(img)
    return base


def make_sprite(img, border=8, off=(10, 14), blur=10, op=0.38, tex=True):
    """returns (shadow, body) — same size, same centre"""
    cut = cutout(img, border)
    if tex:
        cut = apply_tex(cut, paper_tex(cut.width, cut.height, seed=cut.width * 7 + cut.height, strength=0.7))
    p = int(blur * 2.5 + max(abs(off[0]), abs(off[1])))
    body = pad(cut, p)
    a = cut.split()[3].point(lambda v: int(v * op))
    sh = Image.new('RGBA', body.size, (45, 28, 12, 0))
    al = Image.new('L', body.size, 0)
    al.paste(a, (p + off[0], p + off[1]))
    if blur:
        al = al.filter(ImageFilter.GaussianBlur(blur))
    sh.putalpha(al)
    return sh, body


def blit(canvas, sp, x, y):
    x = int(round(x)); y = int(round(y))
    sx = max(0, -x); sy = max(0, -y)
    ex = min(sp.width, canvas.width - x); ey = min(sp.height, canvas.height - y)
    if ex <= sx or ey <= sy:
        return
    canvas.alpha_composite(sp, (x + sx, y + sy), (sx, sy, ex, ey))


def draw_sprite(canvas, sprite, cx, cy, sx=1.0):
    sh, body = sprite
    if sx != 1.0:
        nw = max(2, int(body.width * sx))
        sh = sh.resize((nw, sh.height), Image.BILINEAR)
        body = body.resize((nw, body.height), Image.BILINEAR)
    blit(canvas, sh, cx - sh.width / 2, cy - sh.height / 2)
    blit(canvas, body, cx - body.width / 2, cy - body.height / 2)


def rotate_sprite(sprite, ang):
    return tuple(s.rotate(ang, resample=Image.BICUBIC, expand=True) for s in sprite)


def jit(f, key, amp=1.6):
    r = rng_for(f, key)
    return r.uniform(-amp, amp), r.uniform(-amp, amp)


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    return lines

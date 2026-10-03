"""Tech Wall MOTION-GRAPHICS engine (30 fps, smooth easing, no stop-motion jitter).

Same Blueprint look as the stop-motion episodes (navy grid, chalk dims, paper cut-outs,
taped spec captions, paper hand, yellow dashed tap rings, FOLLOW TECH WALL end strip),
but every element moves on eased keyframe tracks instead of 12 fps held poses.

An episode builds a timeline with `MG` (times in SECONDS), registers custom draw layers,
then calls `run(mg, episode_id)`. See battery.py for a complete example.
"""
import os, sys, math, copy
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw
import lib
from lib import W, H, blit, apply_tex, rotate_sprite, draw_sprite
import themes as th
import screens as S
from props import PW, PH, screen_mask
import movie as m
import movie_blue as mb

FPS = 30
NAVY, MID, YEL, PAPER, CHALK = mb.NAVY, mb.MID, mb.YEL, mb.PAPER, th.CHALK
PHX, PHY = 540, 1205
HIDE = (1350, 2350)


# ------------------------------------------------------------------ easing + tracks
def _c(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


EASE = {
    'lin': lambda x: x,
    'io': lambda x: 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2,
    'o': lambda x: 1 - (1 - x) ** 3,
    'o5': lambda x: 1 - (1 - x) ** 5,
    'i': lambda x: x ** 3,
    'back': lambda x: 1 + 2.7 * (x - 1) ** 3 + 1.7 * (x - 1) ** 2,
}


def seg(t, a, b):
    return _c((t - a) / (b - a)) if b > a else float(t >= a)


class Track:
    """numeric keyframe track: to(t0, dur, value, ease)"""

    def __init__(s, v):
        s.k = [(-1e9, v, 'lin')]

    @property
    def last(s):
        return s.k[-1][1]

    def to(s, t0, dur, v, e='io'):
        s.k.append((t0, s.last, 'lin'))
        s.k.append((t0 + dur, v, e))
        return s

    def set(s, t0, v):
        s.k.append((t0, s.last, 'lin')); s.k.append((t0 + 1e-6, v, 'lin'))

    def at(s, t):
        k = s.k
        for i in range(1, len(k)):
            if t < k[i][0]:
                a, b = k[i - 1], k[i]
                p = 1.0 if b[0] == a[0] else (t - a[0]) / (b[0] - a[0])
                return a[1] + (b[1] - a[1]) * EASE[b[2]](_c(p))
        return k[-1][1]


class Step:
    """discrete value track"""

    def __init__(s, v):
        s.k = [(-1e9, v)]

    def set(s, t, v):
        s.k.append((t, v))

    @property
    def last(s):
        return s.k[-1][1]

    def at(s, t):
        v = s.k[0][1]
        for a, b in s.k:
            if t >= a:
                v = b
            else:
                break
        return v


# ------------------------------------------------------------------ screens
SCREEN_FN = {}          # name -> fn(ov, hl) -> (img 560xH, rows)  (custom screens)
_scache = {}


def screen_content(name, ov=None, hl=None):
    ov = ov or {}
    if name not in SCREEN_FN:
        return S.screen_content(name, ov, hl)
    key = (name, tuple(sorted(ov.items())), hl)
    if key not in _scache:
        _scache[key] = SCREEN_FN[name](ov, hl)
    return _scache[key]


def view(sp):
    content, _ = screen_content(sp['name'], sp.get('ov'), sp.get('hl'))
    sc = int(sp.get('scroll', 0))
    v = content.crop((0, sc, S.SW, sc + S.SH)).copy()
    S.status_bar(v, dark_text=True, bg=S.BG_UI)
    return v


def row_box(sp, rid):
    _, rows = screen_content(sp['name'], sp.get('ov'), sp.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    sc = sp.get('scroll', 0)
    return x0, y0 - sc, x1, y1 - sc


def spec(name, **kw):
    d = dict(name=name, scroll=0, hl=None, ov={})
    d.update(kw)
    return d


# ------------------------------------------------------------------ timeline
class MG:
    def __init__(s):
        s.t = 0.0
        s.px, s.py, s.ps = Track(PHX), Track(2700), Track(1.0)
        s.dims = Track(0.0)
        s.spec = Step(spec('settings'))
        s.trans = []                       # (t0, dur, old, new, back)
        s.hx, s.hy = Track(HIDE[0]), Track(HIDE[1])
        s.hpress = Step(False)
        s.rings = []                       # (t, x, y)
        s.caps = []                        # dict(t_in, t_out, head, text, rot)
        s.snd = []                         # (t_sec, kind)
        s.layers = []                      # fn(cv, t, mg) drawn BELOW the phone
        s.top_layers = []                  # fn(cv, t, mg) drawn ABOVE the phone / hand
        s.end_at = None
        s.duration = 0

    # -- helpers
    def wait(s, d):
        s.t += d

    def sound(s, kind, dt=0):
        s.snd.append((s.t + dt, kind))

    def cap(s, head, text, rot=None):
        if s.caps and s.caps[-1]['t_out'] is None:
            s.caps[-1]['t_out'] = s.t
        r = rot if rot is not None else lib.rng_for(text).uniform(-1.4, 1.4)
        s.caps.append(dict(t_in=s.t, t_out=None, head=head, text=text, rot=r))
        s.sound('paper')

    def cap_off(s):
        if s.caps and s.caps[-1]['t_out'] is None:
            s.caps[-1]['t_out'] = s.t
            s.sound('paper')

    def phone_to(s, x=None, y=None, scale=None, dur=.6, e='o5', dims=None):
        if x is not None:
            s.px.to(s.t, dur, x, e)
        if y is not None:
            s.py.to(s.t, dur, y, e)
        if scale is not None:
            s.ps.to(s.t, dur, scale, e)
        if dims is not None:
            s.dims.to(s.t, dur, dims, 'io')
        s.sound('whoosh')

    def cur_spec(s):
        return copy.deepcopy(s.spec.last)

    def set_spec(s, sp):
        s.spec.set(s.t, copy.deepcopy(sp))

    def navigate(s, new, back=False, dur=.38):
        old = s.cur_spec()
        s.trans.append((s.t, dur, old, copy.deepcopy(new), back))
        s.set_spec(new)
        s.sound('swish')
        s.t += dur

    def s2c(s, x, y):
        """screen coords -> canvas coords (phone at rest, scale 1)"""
        return s.px.last - PW / 2 + 20 + x, s.py.last - PH / 2 + 20 + y

    def hand_to(s, x, y, dur=.42):
        s.hx.to(s.t, dur, x, 'io'); s.hy.to(s.t, dur, y, 'io')
        s.t += dur

    def hand_out(s, dur=.35):
        s.hx.to(s.t, dur, HIDE[0], 'i'); s.hy.to(s.t, dur, HIDE[1], 'i')
        s.t += dur

    def press(s, x, y, kind='tap'):
        s.hpress.set(s.t, True)
        s.rings.append((s.t, x, y))
        s.sound(kind)
        s.t += .16
        s.hpress.set(s.t, False)

    def tap(s, rid, nav=None, back=False, ov=None, fx=.62, fy=.5, move=.42, settle=.06):
        sp = s.cur_spec()
        x0, y0, x1, y1 = row_box(sp, rid)
        tx, ty = s.s2c(x0 + (x1 - x0) * fx, y0 + (y1 - y0) * fy)
        s.hand_to(tx, ty, move)
        s.t += settle
        hl = copy.deepcopy(sp); hl['hl'] = rid
        s.set_spec(hl)
        s.press(tx, ty)
        s.t += .05
        if ov is not None:
            sp2 = copy.deepcopy(sp); sp2['ov'] = dict(sp['ov'], **ov)
            s.set_spec(sp2)
            s.sound('ding')
        else:
            s.set_spec(sp)
        if nav is not None:
            s.t += .04
            s.navigate(nav, back)


# ------------------------------------------------------------------ rendering
P = {}
MGT = None
OUT = None


def init_base():
    P['bg_plain'] = th.bg_blue(with_dims=False)
    P['bg_dims'] = th.bg_blue(with_dims=True)
    P['front'] = th.sprite(th.phone_raw('front'), border=8, off=(16, 22), blur=14, op=.4)
    P['hand'] = {False: th.hand_sprite('blue', press=False), True: th.hand_sprite('blue', press=True)}
    P['caps'] = {}
    P['stex'] = lib.paper_tex(S.SW, S.SH, seed=31, strength=.7)


def sprite_at(cv, sp, x, y, scale=1.0, alpha=1.0):
    """draw an (shadow, body) sprite centred at x,y with scale + alpha"""
    if scale <= 0.01 or alpha <= 0.01:
        return
    sh, body = sp
    if abs(scale - 1) > 1e-3:
        sh = sh.resize((max(1, int(sh.width * scale)), max(1, int(sh.height * scale))), Image.BILINEAR)
        body = body.resize((max(1, int(body.width * scale)), max(1, int(body.height * scale))), Image.BILINEAR)
    if alpha < .999:
        sh = sh.copy(); body = body.copy()
        sh.putalpha(sh.split()[3].point(lambda v: int(v * alpha)))
        body.putalpha(body.split()[3].point(lambda v: int(v * alpha)))
    blit(cv, sh, x - sh.width / 2, y - sh.height / 2)
    blit(cv, body, x - body.width / 2, y - body.height / 2)


def compose_screen(mg, t):
    tr = None
    for t0, d, old, new, back in mg.trans:
        if t0 <= t < t0 + d:
            tr = (seg(t, t0, t0 + d), old, new, back)
    if tr:
        p, old, new, back = tr
        p = EASE['io'](p)
        a, b = view(old), view(new)
        img = Image.new('RGB', (S.SW, S.SH), (0, 0, 0))
        dark = lambda im, k: Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), k)
        if not back:
            img.paste(dark(a, .15 * p), (int(-p * S.SW * .3), 0))
            img.paste(b, (int((1 - p) * S.SW), 0))
        else:
            img.paste(dark(b, .15 * (1 - p)), (int(-(1 - p) * S.SW * .3), 0))
            img.paste(a, (int(p * S.SW), 0))
    else:
        img = view(mg.spec.at(t))
    ImageDraw.Draw(img).rounded_rectangle((S.SW / 2 - 86, 22, S.SW / 2 + 86, 72), 25, fill=(10, 10, 12))
    return apply_tex(img, P['stex'])


def draw_phone(cv, mg, t):
    y = mg.py.at(t)
    if y > 2650:
        return
    sh, body = P['front']
    body = body.copy()
    ox = (body.width - (PW + 16)) // 2 + 28
    oy = (body.height - PH) // 2 + 20
    body.paste(compose_screen(mg, t), (ox, oy), screen_mask())
    sprite_at(cv, (sh, body), mg.px.at(t), y, mg.ps.at(t))


def draw_rings(cv, mg, t):
    for t0, x, y in mg.rings:
        k = (t - t0) / .5
        if 0 <= k < 1:
            r = 26 + 60 * EASE['o'](k)
            a = int(255 * (1 - k))
            s = int(2 * r + 30)
            im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
            th.dashed_circle(ImageDraw.Draw(im), s / 2, s / 2, r, YEL + (a,), max(2, int(8 - 5 * k)), seg=16)
            blit(cv, im, x - s / 2, y - s / 2)


def draw_hand(cv, mg, t):
    x, y = mg.hx.at(t), mg.hy.at(t)
    if y > 2300:
        return
    sh, body, tip = P['hand'][mg.hpress.at(t)]
    blit(cv, sh, x - tip[0], y - tip[1]); blit(cv, body, x - tip[0], y - tip[1])


def cap_y(c, t):
    k = t - c['t_in']
    if k < 0:
        return None
    y = -300 + 600 * EASE['back'](seg(k, 0, .45))
    if c['t_out'] is not None and t >= c['t_out']:
        e = seg(t, c['t_out'], c['t_out'] + .32)
        if e >= 1:
            return None
        y = 300 - 720 * EASE['i'](e)
    return y


def draw_caps(cv, mg, t):
    for c in mg.caps:
        y = cap_y(c, t)
        if y is None:
            continue
        key = (c['head'], c['text'])
        if key not in P['caps']:
            P['caps'][key] = rotate_sprite(th.cap_blue(c['head'], c['text']), c['rot'])
        sprite_at(cv, P['caps'][key], 540, y)


def render(fi):
    mg = MGT
    t = fi / FPS
    dv = mg.dims.at(t)
    if dv <= .001:
        cv = P['bg_plain'].copy()
    elif dv >= .999:
        cv = P['bg_dims'].copy()
    else:
        cv = Image.blend(P['bg_plain'], P['bg_dims'], dv)
    for fn in mg.layers:
        fn(cv, t, mg)
    draw_phone(cv, mg, t)
    draw_rings(cv, mg, t)
    draw_hand(cv, mg, t)
    for fn in mg.top_layers:
        fn(cv, t, mg)
    draw_caps(cv, mg, t)
    cv.convert('RGB').save(f'{OUT}/{fi:05d}.png', compress_level=1)
    return fi


def run(mg, ep, cover_t=2.6, init=None):
    """render frames (or only the frame numbers given on the command line) + soundtrack"""
    global MGT, OUT
    MGT = mg
    OUT = lib.out(f'frames_{ep}')
    os.makedirs(OUT, exist_ok=True)
    n = int(round(mg.duration * FPS))
    with open(lib.out(f'meta_{ep}'), 'w') as fh:
        fh.write(f'FR={FPS}\nCF={int(cover_t * FPS)}\n')
    print('frames', n, 'seconds', round(n / FPS, 2), flush=True)
    for c in mg.caps:
        print(f"{c['t_in']:5.1f}s  {c['head']:<26} {c['text']}")
    init_base()
    if init:
        init()
    only = [int(a) for a in sys.argv[1:]]
    if only:
        for fi in only:
            if fi < n:
                render(fi)
        return
    with Pool(2) as pool:
        for i, _ in enumerate(pool.imap(render, range(n), chunksize=10)):
            if i % 150 == 0:
                print('rendered', i, flush=True)
    # soundtrack: movie.make_audio works in 12 fps frame units
    m.make_audio(dict(snd=[(ts * lib.FPS, k) for ts, k in mg.snd]), n / FPS * lib.FPS, lib.out(f'audio_{ep}.wav'))

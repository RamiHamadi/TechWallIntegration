import copy, os, sys, math, wave
import numpy as np
from multiprocessing import Pool
from PIL import Image, ImageDraw
from lib import *
from screens import view, row_point, SW, SH, BLUE, GRAYI, screen_tex
from props import *

OUT = __import__('lib').out('frames_movie')
PHY = 1205
YELLOW, PINK, MINT, SKY, PEACH = (255, 222, 105), (255, 182, 200), (170, 230, 200), (170, 210, 250), (255, 200, 150)

HIDE = (1300, 2350)


# =============================================================== timeline
class TL:
    def __init__(s):
        s.frames = []
        s.ph = dict(x=540, y=2700, spec=dict(name='home', scroll=0, hl=None, ov={}), trans=None,
                    sx=1.0, side='front', flash=0.0, thumb=None)
        s.hand = None
        s.caps, s.fx, s.snd = [], [], []

    @property
    def f(s):
        return len(s.frames)

    def snap(s):
        s.frames.append(dict(ph=copy.deepcopy(s.ph), hand=copy.deepcopy(s.hand)))

    def hold(s, n):
        for _ in range(n):
            s.snap()

    def sound(s, kind, df=0):
        s.snd.append((s.f + df, kind))

    def s2c(s, x, y):
        return s.ph['x'] - PW / 2 + 20 + x, s.ph['y'] - PH / 2 + 20 + y

    def cap(s, badge, text, col):
        if s.caps and s.caps[-1]['out'] is None:
            s.caps[-1]['out'] = s.f
        s.caps.append(dict(badge=badge, text=text, col=col, inn=s.f + 1, out=None, rot=rng_for(text).uniform(-2.2, 2.2)))
        s.sound('paper', 1)

    def cap_off(s):
        if s.caps and s.caps[-1]['out'] is None:
            s.caps[-1]['out'] = s.f
            s.sound('paper')

    def phone_to(s, y, n, keys=None):
        y0 = s.ph['y']
        s.sound('whoosh')
        for i in range(1, n + 1):
            t = ease(i / n)
            ov = 0
            if keys and i == n - 1:
                ov = keys
            s.ph['y'] = y0 + (y - y0) * t + ov
            s.snap()

    def move_hand(s, tx, ty, n, press=False):
        if s.hand is None:
            s.hand = dict(x=HIDE[0], y=HIDE[1], press=False)
        x0, y0 = s.hand['x'], s.hand['y']
        for i in range(1, n + 1):
            t = ease(i / n)
            s.hand.update(x=x0 + (tx - x0) * t, y=y0 + (ty - y0) * t, press=press)
            s.snap()

    def hand_out(s, n=4):
        s.move_hand(*HIDE, n)
        s.hand = None

    def press(s, tx, ty, kind='tap'):
        s.hand['press'] = True
        s.fx.append(('ring', s.f, tx, ty))
        s.sound(kind)

    def tap(s, rid, nav=None, back=False, ov=None, n_move=6, fx=0.62, after=None):
        spec = s.ph['spec']
        tx, ty = s.s2c(*row_point(spec, rid, fx))
        s.move_hand(tx, ty, n_move)
        s.hold(2)
        s.press(tx, ty)
        spec['hl'] = rid
        s.hold(2)
        s.hand['press'] = False
        if ov:
            spec['ov'].update(ov)
            spec['hl'] = None
            s.sound('ding')
        s.hold(1)
        spec['hl'] = None
        if nav:
            s.navigate(nav, back)

    def navigate(s, newspec, back=False):
        old = copy.deepcopy(s.ph['spec'])
        s.ph['spec'] = newspec
        s.sound('swish')
        for p in (0.4, 0.78):
            s.ph['trans'] = dict(old=old, p=p, back=back)
            if s.hand:
                s.hand['x'] += 14; s.hand['y'] += 18
            s.snap()
        s.ph['trans'] = None
        s.snap()

    def swipe(s, dist, n=6, x=300, y=900):
        spec = s.ph['spec']
        tx, ty = s.s2c(x, y)
        s.move_hand(tx, ty, 6)
        s.hold(1)
        s.press(tx, ty, 'tap')
        s.snap()
        sc0 = spec['scroll']
        for i in range(1, n + 1):
            t = ease(i / n)
            spec['scroll'] = sc0 + dist * t
            s.hand['y'] = ty - dist * t
            s.snap()
        s.hand['press'] = False
        s.hold(2)

    def flip(s, to):
        s.sound('whoosh')
        for sx in (0.72, 0.36, 0.06):
            s.ph['sx'] = sx; s.snap()
        s.ph['side'] = to
        for sx in (0.06, 0.4, 0.78, 1.0):
            s.ph['sx'] = sx; s.snap()


def spec(name, **kw):
    d = dict(name=name, scroll=0, hl=None, ov={})
    d.update(kw)
    return d


def build():
    t = TL()
    # ---- 1. title
    t.fx.append(('title', 0, 50))
    t.hold(56)
    # ---- 2. phone in
    t.phone_to(PHY, 6, keys=-40)
    t.hold(2)
    t.cap('1', 'Open Settings', YELLOW)
    t.hold(14)
    ov = {}
    t.tap('app_settings', nav=spec('settings', ov=ov), n_move=7)
    t.cap('2', 'Tap Accessibility', PINK)
    t.hold(12)
    t.hold(0)
    t.tap('accessibility', nav=spec('accessibility', ov=ov))
    t.cap('3', 'Tap Touch', MINT)
    t.hold(12)
    t.hold(0)
    t.tap('touch', nav=spec('touch', ov=ov))
    t.cap('4', 'Scroll down, tap Back Tap', SKY)
    t.hold(12)
    t.swipe(420)
    t.tap('backtap', nav=spec('backtap', ov=ov))
    t.cap('5', 'Tap Double Tap', PEACH)
    t.hold(12)
    dts = spec('doubletap', ov={'sel': 'none'})
    t.tap('double', nav=dts)
    t.cap('6', 'Choose Screenshot', YELLOW)
    t.hold(10)
    t.swipe(300, y=950)
    t.tap('screenshot', ov={'sel': 'screenshot'})
    t.hold(8)
    t.tap('back', nav=spec('backtap', ov={'dt': 'Screenshot'}), back=True, fx=0.3)
    t.cap('check', 'Done! Double Tap is set', MINT)
    t.hold(4)
    t.move_hand(*t.s2c(*row_point(t.ph['spec'], 'double', 0.82)), 5)
    t.hold(20)
    t.hand_out(4)
    # ---- 3. demo
    t.cap('!', 'Now double-tap the back of your iPhone', PINK)
    t.navigate(spec('home'))
    t.hold(14)
    t.flip('back')
    t.hold(3)
    bx, by = t.s2c(300, 640)
    t.move_hand(bx, by, 6)
    t.hold(2)
    for k in range(2):
        t.press(bx, by, 'knock')
        t.fx.append(('burst', t.f, bx + (-210 if k == 0 else 190), by - 260 + 60 * k, k))
        t.hold(2)
        t.hand['press'] = False
        t.hand['y'] -= 22
        t.hold(2)
        t.hand['y'] += 22
    t.hold(5)
    t.hand_out(4)
    t.flip('front')
    t.sound('shutter')
    for fl in (1.0, 0.55):
        t.ph['flash'] = fl; t.snap()
    t.ph['flash'] = 0.0
    t.ph['thumb'] = 0.0
    t.cap('check', 'Screenshot saved!', YELLOW)
    for p in (0.0, 0.35, 0.7, 0.9, 1.0):
        t.ph['thumb'] = p; t.snap()
    t.hold(22)
    # ---- 4. bonus
    t.cap('+', 'Bonus: set Triple Tap to Flashlight', SKY)
    t.ph['thumb'] = None
    t.navigate(spec('backtap', ov={'dt': 'Screenshot', 'tt': 'Flashlight'}))
    t.hold(36)
    # ---- 5. end
    t.cap_off()
    t.phone_to(2700, 5)
    t.fx.append(('end', t.f))
    t.hold(70)
    return t


# =============================================================== render
P = {}
TLD = None


def init_props():
    P['bg'] = make_background()
    P['front'] = make_sprite(phone_raw('front'), border=8, off=(16, 22), blur=14, op=0.40)
    P['back'] = make_sprite(phone_raw('back'), border=8, off=(16, 22), blur=14, op=0.40)
    P['hand'] = hand_sprites()
    P['rings'] = ring_sprites()
    P['notes'] = {}
    # title
    cols = PALETTE
    P['tiles'] = [tile_sprite(ch, cols[i % len(cols)], rng_for('tile', i).uniform(-7, 7)) for i, ch in enumerate('BACKTAP')]
    P['t_label'] = strip_sprite('iPhone tip', M(64), (255, 255, 255), (240, 98, 85), -4)
    P['t_s1'] = strip_sprite('The hidden iPhone shortcut', F(600, 56), (255, 253, 248), INK, 2)
    P['t_s2'] = strip_sprite('Tap the back = screenshot', M(56), (64, 170, 160), (255, 255, 255), -2)
    mini = phone_raw('back').resize((190, 377), Image.LANCZOS)
    P['t_phone'] = rotate_sprite(make_sprite(mini, border=6, off=(8, 12), blur=8, op=0.38), 10)
    P['t_burst'] = burst_sprite('tap tap!', -10)
    # end
    P['e_head'] = strip_sprite('Save this tip!', M(104), (245, 183, 64), INK, -3, padx=50, pady=30)
    P['e_chips'] = [chip_sprite('Settings', GRAYI, 'gear', -2), chip_sprite('Accessibility', BLUE, 'person', 1.5),
                    chip_sprite('Touch', BLUE, 'touch', -1.5), chip_sprite('Back Tap', INK, 'touch', 2, hot=True)]
    P['e_arrows'] = [arrow_sprite(r) for r in (14, -14, 14)]
    P['e_s1'] = strip_sprite('Double Tap = Screenshot', F(600, 54), (64, 170, 160), (255, 255, 255), -1.5)
    P['e_s2'] = strip_sprite('Triple Tap = Flashlight', F(600, 54), (150, 110, 210), (255, 255, 255), 1.5)
    P['e_s3'] = strip_sprite('Works on iPhone 8 or later with iOS 14+', F(500, 38), (255, 253, 248), INK, -1)
    P['bursts'] = [burst_sprite('TAP!', -12), burst_sprite('TAP!', 10, col=(235, 120, 170))]


def drop_y(f, a, y, f_exit=None, stagger=0):
    """stop-motion drop-in and fly-out. returns None if hidden."""
    k = f - a
    if k < 0:
        return None
    dy = {0: -300, 1: 28, 2: -10}.get(k, 0)
    if f_exit is not None:
        e = f - f_exit - stagger
        if e >= 0:
            if e >= 3:
                return None
            dy += (-80, -500, -1400)[e]
    return y + dy


def put(cv, sprite, x, y, f, key, amp=1.6, sx=1.0):
    jx, jy = jit(f, key, amp)
    draw_sprite(cv, sprite, x + jx, y + jy, sx)


def compose_screen(ph):
    sp = ph['spec']
    tr = ph['trans']
    if tr:
        new, old, p = view(sp), view(tr['old']), tr['p']
        img = Image.new('RGB', (SW, SH), (0, 0, 0))
        if not tr['back']:
            img.paste(Image.blend(old, Image.new('RGB', old.size, (0, 0, 0)), 0.15 * p), (int(-p * SW * 0.3), 0))
            img.paste(new, (int((1 - p) * SW), 0))
        else:
            img.paste(Image.blend(new, Image.new('RGB', new.size, (0, 0, 0)), 0.15 * (1 - p)), (int(-(1 - p) * SW * 0.3), 0))
            img.paste(old, (int(p * SW), 0))
    else:
        img = view(sp)
    if ph['thumb'] is not None:
        p = ease(ph['thumb'])
        snap = view(spec('home'))
        sc = 1 - 0.68 * p
        tw, th = int(SW * sc), int(SH * sc)
        if p > 0:
            img = Image.blend(img, Image.new('RGB', img.size, (255, 255, 255)), 0.0)
        th_img = snap.resize((tw, th), Image.BILINEAR)
        bw = int(2 + 6 * p)
        fr = Image.new('RGB', (tw + 2 * bw, th + 2 * bw), (255, 255, 255))
        fr.paste(th_img, (bw, bw))
        x = int(28 * p); y = int((SH - 40 - fr.height) * p)
        if p > 0:
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((x + 4, y + 6, x + fr.width + 4, y + fr.height + 6), 10, fill=(90, 90, 100))
        img.paste(fr, (x, y))
    if ph['flash'] > 0:
        img = Image.blend(img, Image.new('RGB', img.size, (255, 255, 255)), ph['flash'])
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((SW / 2 - 86, 22, SW / 2 + 86, 72), 25, fill=(10, 10, 12))
    img = apply_tex(img, screen_tex())
    return img


def draw_phone(cv, f, ph):
    if ph['y'] > 2600:
        return
    sh, body = P[ph['side']]
    if ph['side'] == 'front':
        body = body.copy()
        ox = (body.width - (PW + 16)) // 2 + 28
        oy = (body.height - PH) // 2 + 20
        body.paste(compose_screen(ph), (ox, oy), screen_mask())
    put(cv, (sh, body), ph['x'], ph['y'], f, 'phone', amp=1.2, sx=ph['sx'])


def draw_hand(cv, f, hd):
    if not hd:
        return
    sh, body, tip = P['hand']['press' if hd['press'] else 'hover']
    jx, jy = jit(f, 'hand', 1.4)
    x, y = hd['x'] - tip[0] + jx, hd['y'] - tip[1] + jy
    blit(cv, sh, x, y)
    blit(cv, body, x, y)


def draw_caps(cv, f, caps):
    for c in caps:
        k = f - c['inn']
        if k < 0:
            continue
        ys = {0: -260, 1: 380, 2: 268, 3: 312}
        y = ys.get(k, 300)
        if c['out'] is not None and f >= c['out']:
            e = f - c['out']
            if e > 2:
                continue
            y = (230, -10, -400)[e]
        key = (c['badge'], c['text'], c['col'])
        if key not in P['notes']:
            P['notes'][key] = note_sprite(c['badge'], c['text'], c['col'], c['rot'])
        put(cv, P['notes'][key], 540, y, f, ('cap', c['text']), amp=1.8)


def draw_title(cv, f, a, ex):
    els = [('t_label', 540, 420, a + 1, 0)]
    for i in range(4):
        els.append((('tile', i), 540 + (i - 1.5) * 168, 640, a + 4 + 2 * i, i))
    for i in range(3):
        els.append((('tile', 4 + i), 540 + (i - 1) * 168, 820, a + 12 + 2 * i, i + 1))
    els += [('t_s1', 540, 1040, a + 20, 0), ('t_s2', 520, 1170, a + 24, 1),
            ('t_phone', 560, 1530, a + 28, 2), ('t_burst', 790, 1380, a + 31, 0)]
    for key, x, y, ap, st in els:
        yy = drop_y(f, ap, y, ex, st)
        if yy is None:
            continue
        sp = P['tiles'][key[1]] if isinstance(key, tuple) else P[key]
        put(cv, sp, x, yy, f, key)


def draw_end(cv, f, a):
    els = [('e_head', 540, 300, a + 2)]
    xs = [470, 600, 470, 600]
    for i in range(4):
        els.append((('chip', i), xs[i], 560 + 185 * i, a + 6 + 4 * i))
        if i < 3:
            els.append((('arrow', i), (190, 950, 190)[i], 652 + 185 * i, a + 9 + 4 * i))
    els += [('e_s1', 540, 1340, a + 24), ('e_s2', 540, 1470, a + 28), ('e_s3', 540, 1640, a + 32)]
    for key, x, y, ap in els:
        yy = drop_y(f, ap, y)
        if yy is None:
            continue
        if isinstance(key, tuple):
            sp = P['e_chips'][key[1]] if key[0] == 'chip' else P['e_arrows'][key[1]]
        else:
            sp = P[key]
        put(cv, sp, x, yy, f, key)


def draw_fx(cv, f, fxs):
    for e in fxs:
        if e[0] == 'ring':
            k = f - e[1]
            if 0 <= k < 3:
                put(cv, P['rings'][k], e[2], e[3], f, 'ring', 0.5)
        elif e[0] == 'burst':
            k = f - e[1]
            if 0 <= k < 7:
                sc = {0: 0.5, 1: 1.08}.get(k, 1.0)
                sp = P['bursts'][e[4]]
                if sc != 1.0:
                    sp = tuple(s.resize((int(s.width * sc), int(s.height * sc)), Image.BILINEAR) for s in sp)
                put(cv, sp, e[2], e[3], f, ('burst', e[1]))


def render(f):
    tl = TLD
    st = tl['frames'][f]
    cv = P['bg'].copy()
    for e in tl['fx']:
        if e[0] == 'title' and f < e[2] + 8:
            draw_title(cv, f, e[1], e[2])
        if e[0] == 'end' and f >= e[1]:
            draw_end(cv, f, e[1])
    draw_phone(cv, f, st['ph'])
    draw_fx(cv, f, tl['fx'])
    draw_hand(cv, f, st['hand'])
    draw_caps(cv, f, tl['caps'])
    # exposure flicker
    k = 1 + rng_for(f, 'flicker').uniform(-0.018, 0.018)
    out = cv.convert('RGB').point(lambda v: min(255, int(v * k)))
    out.save(f'{OUT}/{f:05d}.png', compress_level=1)
    return f


# =============================================================== audio
SR = 44100


def env_noise(n, seed):
    return np.random.default_rng(seed).normal(0, 1, n)


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode='same')


def sfx(kind, seed=0):
    def T(d):
        return np.arange(int(d * SR)) / SR
    if kind == 'tap':
        t = T(0.08)
        return 0.35 * env_noise(len(t), seed) * np.exp(-t * 260) + 0.35 * np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 90)
    if kind == 'pop':
        t = T(0.12)
        fr = 720 - 2600 * t
        return 0.45 * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 30)
    if kind in ('whoosh', 'paper', 'swish'):
        d = {'whoosh': 0.32, 'paper': 0.2, 'swish': 0.16}[kind]
        a = {'whoosh': 0.5, 'paper': 0.32, 'swish': 0.22}[kind]
        t = T(d)
        n = env_noise(len(t), seed)
        n = n - lp(n, 6) if kind == 'paper' else lp(n, 3)
        return a * n * np.sin(np.pi * t / d) ** 2
    if kind == 'knock':
        t = T(0.25)
        return (0.9 * np.sin(2 * np.pi * 130 * t) * np.exp(-t * 28) + 0.5 * np.sin(2 * np.pi * 85 * t) * np.exp(-t * 18)
                + 0.3 * lp(env_noise(len(t), seed), 4) * np.exp(-t * 160))
    if kind == 'shutter':
        t = T(0.2)
        n = env_noise(len(t), seed)
        n = n - lp(n, 4)
        e = np.exp(-t * 90) + np.where(t > 0.07, np.exp(-(t - 0.07) * 90), 0)
        return 0.6 * n * e
    if kind == 'ding':
        t = T(0.9)
        return 0.22 * (np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 1975.5 * t)) * np.exp(-t * 5)
    return np.zeros(1)


def pluck(midi, dur, amp):
    t = np.arange(int(dur * SR)) / SR
    fr = 440 * 2 ** ((midi - 69) / 12)
    s = sum(a * np.sin(2 * np.pi * fr * h * t) * np.exp(-t * (3.2 + 2.2 * h)) for h, a in [(1, 1), (2, .45), (3, .22), (4, .1)])
    return amp * s * (1 - np.exp(-t * 600))


def music(total):
    out = np.zeros(int(total * SR) + SR * 2)
    bpm = 104
    e8 = 60 / bpm / 2
    chords = [(48, [60, 64, 67, 72]), (43, [59, 62, 67, 71]), (45, [60, 64, 69, 72]), (41, [60, 65, 69, 72])]
    pat = [0, 1, 2, 3, 2, 1, 2, 1]
    t = 0.0; bar = 0
    while t < total:
        bass, notes = chords[bar % 4]
        b = pluck(bass, 1.6, 0.55)
        i0 = int(t * SR); out[i0:i0 + len(b)] += b[:len(out) - i0]
        for j, p in enumerate(pat):
            tt = t + j * e8
            n = pluck(notes[p], 0.7, 0.28 if j % 2 == 0 else 0.2)
            i0 = int(tt * SR)
            if i0 < len(out):
                out[i0:i0 + len(n)] += n[:len(out) - i0]
        t += 8 * e8; bar += 1
    out = out[:int(total * SR)]
    fade = int(2.0 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    out[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    return out


def make_audio(tl, nframes, path):
    total = nframes / FPS
    mix = music(total) * 0.16
    for i, (f, kind) in enumerate(tl['snd']):
        s = sfx(kind, i)
        i0 = int(f / FPS * SR)
        if i0 >= len(mix):
            continue
        mix[i0:i0 + len(s)] += s[:len(mix) - i0]
    mix /= max(1e-6, np.abs(mix).max() / 0.89)
    pcm = (mix * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def add_title_end_sounds(t):
    for e in t.fx:
        if e[0] == 'title':
            a = e[1]
            for ap in [a + 1] + [a + 4 + 2 * i for i in range(4)] + [a + 12 + 2 * i for i in range(3)] + [a + 20, a + 24, a + 28, a + 31]:
                t.snd.append((ap, 'pop'))
            t.snd.append((e[2] + 1, 'whoosh'))
        if e[0] == 'end':
            a = e[1]
            for ap in [a + 2] + [a + 6 + 4 * i for i in range(4)] + [a + 24, a + 28, a + 32]:
                t.snd.append((ap, 'pop'))


if __name__ == '__main__':
    t = build()
    add_title_end_sounds(t)
    TLD = dict(frames=t.frames, fx=t.fx, caps=t.caps, snd=t.snd)
    n = len(t.frames)
    print('frames', n, 'seconds', n / FPS)
    os.makedirs(OUT, exist_ok=True)
    only = [int(a) for a in sys.argv[1:]]
    init_props()
    if only:
        for f in only:
            render(f)
    else:
        with Pool(2) as pool:
            for i, _ in enumerate(pool.imap(render, range(n), chunksize=8)):
                if i % 60 == 0:
                    print('rendered', i, flush=True)
        make_audio(TLD, n, __import__('lib').out('audio_movie.wav'))

"""Tech Wall — iPhone 18 Pro variable aperture (HTML-canvas motion graphics, 30 fps).

The animation lives in camera18/scene.html (a deterministic render(t) on a 1080x1920 canvas).
This script captures it frame by frame with headless Chromium (Playwright), writes a cinematic
synthesized soundtrack from the scene's event list, and the out/meta file for build.sh.

    ./build.sh camera18                 # full render + encode -> out/camera18.mp4
    python3 camera18.py 0 300 600       # preview single frames -> out/frames_camera18/
Needs: pip install playwright  (Chromium is preinstalled in the cloud env; else `playwright install chromium`)
"""
import os, sys, json, wave, asyncio
import numpy as np
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import lib

EP = 'camera18'
FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
SCENE = 'file://' + os.path.join(HERE, 'camera18', 'scene.html')
OUT = lib.out(f'frames_{EP}')
WORKERS = 3


async def capture(frames):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch(args=['--allow-file-access-from-files'])

        async def page():
            pg = await br.new_page(viewport={'width': 1080, 'height': 1920})
            await pg.goto(SCENE)
            await pg.wait_for_function('window.READY===true', timeout=30000)
            return pg
        p0 = await page()
        meta = await p0.evaluate('window.META')
        if frames is None:
            frames = list(range(int(round(meta['END'] * FPS))))
        pages = [p0] + [await page() for _ in range(WORKERS - 1)]
        q = list(frames)
        done = [0]

        async def work(pg):
            while q:
                fi = q.pop(0)
                path = f'{OUT}/{fi:05d}.png'
                if os.path.exists(path) and os.path.getsize(path) > 1000:
                    continue
                await pg.evaluate(f'render({fi / FPS})')
                await pg.locator('canvas').screenshot(path=path)
                done[0] += 1
                if done[0] % 150 == 0:
                    print('frame', fi, flush=True)
        await asyncio.gather(*[work(pg) for pg in pages])
        await br.close()
        return meta


# ------------------------------------------------------------------ cinematic soundtrack
SR = 44100
rng = np.random.default_rng(18)


def T(d):
    return np.arange(int(d * SR)) / SR


def lp(v, k):
    return np.convolve(v, np.ones(k) / k, mode='same')


def hz(mn):
    return 440 * 2 ** ((mn - 69) / 12)


def add(buf, t, s, g=1.0):
    i = int(t * SR)
    if 0 <= i < len(buf):
        s = s[:len(buf) - i]
        buf[i:i + len(s)] += s * g


def pad(notes, d, a=.05):
    t = T(d); s = np.zeros(len(t))
    for n in notes:
        for det in (-.08, .0, .08):
            s += np.sin(2 * np.pi * hz(n + det) * t) + .3 * np.sin(2 * np.pi * hz(n + 12 + det) * t)
    env = np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.2)
    return lp(s, 6) * env * a


def kick():
    t = T(.5)
    return np.sin(2 * np.pi * np.cumsum(42 + 90 * np.exp(-t * 30)) / SR) * np.exp(-t * 7) * .8


def tick(t0=0):
    t = T(.06)
    n = rng.normal(0, 1, len(t)); n = n - lp(n, 3)
    return n * np.exp(-t * 160) * .18


def sfx(k):
    if k == 'iris':           # mechanical blade sweep: fast ticks + soft servo whir
        out = np.zeros(int(.5 * SR))
        for i in range(7):
            add(out, i * .045, tick(), .9 - i * .08)
        t = T(.45); wh = np.sin(2 * np.pi * np.cumsum(900 + 500 * t) / SR) * np.sin(np.pi * t / .45) * .05
        add(out, 0, wh)
        return out
    if k == 'click':
        t = T(.09)
        s = np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * .25
        tk = tick(); s[:len(tk)] += tk
        return s
    if k == 'pop':
        t = T(.14)
        return np.sin(2 * np.pi * np.cumsum(420 + 700 * np.exp(-t * 35)) / SR) * np.exp(-t * 24) * .28
    if k == 'whoosh':
        t = T(.7); n = rng.normal(0, 1, len(t))
        out = np.zeros(len(t))
        for j, kk in enumerate([3, 6, 12, 24]):
            w = np.sin(np.pi * np.clip(t / .7 - j * .1 + .15, 0, 1)) ** 2
            out += (lp(n, kk) - lp(n, kk * 3)) * w
        return out * np.sin(np.pi * t / .7) ** 2 * .45
    if k == 'hit':
        t = T(2.2)
        return (np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t * 14)) / SR) * np.exp(-t * 2.2) * .9
                + lp(rng.normal(0, 1, len(t)), 2) * np.exp(-t * 5) * .18)
    if k == 'ding':
        t = T(1.4); s = np.zeros(len(t))
        for i, n in enumerate([84, 88, 91]):
            tt = np.maximum(t - i * .06, 0)
            s += np.sin(2 * np.pi * hz(n) * tt) * np.exp(-tt * 4) * (t >= i * .06)
        return s * .09
    if k == 'riser':
        t = T(1.0); n = rng.normal(0, 1, len(t))
        return ((n - lp(n, 3)) * .06 + np.sin(2 * np.pi * np.cumsum(200 + 1400 * t ** 2) / SR) * .05) * (t / 1.0) ** 2
    return np.zeros(1)


def soundtrack(meta, path):
    end = meta['END']; N = int((end + 1) * SR)
    mus = np.zeros(N)
    bpm = 96; beat = 60 / bpm; bar = 4 * beat
    prog = [[57, 64, 69, 72], [53, 60, 65, 69], [48, 55, 64, 67], [55, 62, 67, 71]]   # Am F C G (voicings)
    t0, b = 0.0, 0
    while t0 < end:
        add(mus, t0, pad(prog[b % 4], bar + 1.0), 1)
        add(mus, t0, np.sin(2 * np.pi * hz(prog[b % 4][0] - 24) * T(bar)) * np.minimum(1, T(bar) * 20) * np.exp(-T(bar) * .6) * .18)
        if t0 >= 3.7:                                  # pulse after the hook
            for q in range(4):
                add(mus, t0 + q * beat, kick(), .5 if q % 2 == 0 else .25)
                for e in range(2):
                    tt = T(.05); add(mus, t0 + q * beat + e * beat / 2, (rng.normal(0, 1, len(tt)) - lp(rng.normal(0, 1, len(tt)), 3)) * np.exp(-tt * 80) * .05)
        t0 += bar; b += 1
    ei = int(end * SR)
    f = int(2.0 * SR); mus[ei - f:ei] *= np.linspace(1, 0, f); mus[ei:] = 0
    fx = np.zeros(N); duck = np.ones(N)
    for t, k in meta['EV']:
        add(fx, t, sfx(k))
        if k in ('hit', 'whoosh'):
            i = int(t * SR); L = int(.5 * SR); duck[i:i + L] = np.minimum(duck[i:i + L], np.linspace(.55, 1, len(duck[i:i + L])))
    mix = (mus * .55 * duck + fx)[:ei]
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)
    mix /= np.abs(mix).max() / .9
    st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    only = [int(a) for a in sys.argv[1:]] or None
    meta = asyncio.run(capture(only))
    print('END', meta['END'], 's  frames', int(round(meta['END'] * FPS)), flush=True)
    with open(lib.out(f'meta_{EP}'), 'w') as fh:
        fh.write(f'FR={FPS}\nCF={int(1.6 * FPS)}\n')     # cover: hook frame (headline + lens)
    if only is None:
        soundtrack(meta, lib.out(f'audio_{EP}.wav'))

"""Tech Wall HOST engine: an animated presenter (the Tech Wall host character) talks the viewer
through a tip while a phone on the right shows each tap. 30 fps, 1080x1920, result-first.

An episode is a small .py file with a SPEC dict (see hostlock.py) and:
    if __name__ == '__main__': host.run(EP, SPEC)

    ./build.sh hostlock                 # voice + lip-sync + frames + soundtrack -> out/hostlock.mp4 (+ cover)
    python3 hostlock.py 0 150 400       # preview single frames -> out/frames_hostlock/

Pipeline: TTS per beat (English: Kokoro, Arabic: Piper "Kareem") -> silence trim -> timeline
-> Rhubarb Lip Sync mouth shapes -> loudness envelope -> event list (taps, keys, screen changes, fx)
-> synthesized SFX mix -> host/scene.html render(t) captured with Playwright/Chromium.
One-time setup (models + Rhubarb, ~450 MB, cached outside the repo): bash host/setup.sh
"""
import os, sys, re, json, hashlib, subprocess, asyncio, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib

FPS = 30
SR = 24000
MODELS = os.environ.get('TW_HOST_MODELS', os.path.expanduser('~/.cache/techwall-host'))
SCENE = 'file://' + os.path.join(HERE, 'host', 'scene.html')
WORKERS = 3
GAP = 0.6           # silence between beats (s)
PAUSE_COMMA = 0.24  # silence after , ; : inside a line (s)  (spec 'pause_comma')
PAUSE_STOP = 0.45   # silence after . ! ? … inside a line (s) (spec 'pause_stop')
LEAD = 0.35         # first word starts here; frame 0 (the cover) is silent with the hook caption on screen
END_HOLD = 1.8      # end card hold after the last word

# Voices: English = Kokoro voice ids (am_puck = current host voice; others: am_michael am_fenrir am_eric am_liam
# am_onyx bm_george bm_lewis bm_fable ...). Arabic = Piper voices downloaded by host/setup.sh.
AR_VOICES = {'kareem': 'vits-piper-ar_JO-kareem-medium/ar_JO-kareem-medium'}


def _dir(name):
    p = lib.out(name); os.makedirs(p, exist_ok=True); return p


# ----------------------------------------------------------------------------- TTS
def _trim(s, thr=0.012):
    idx = np.where(np.abs(s) > thr)[0]
    return s if not len(idx) else s[max(0, idx[0] - 240): idx[-1] + 600]


def _resample(s, sr_in, sr_out=SR):
    if sr_in == sr_out:
        return s.astype(np.float32)
    n = int(round(len(s) * sr_out / sr_in))
    return np.interp(np.linspace(0, len(s) - 1, n), np.arange(len(s)), s).astype(np.float32)


_STOP = re.compile(r'(?<=[.!?…؟])\s+')
_COMMA = re.compile(r'[,;:،؛](?=\s+\S)')


def _quietest(c, t_est, win=(-0.16, 0.1), hop=120, w=480):
    """Sample index of the quietest 20 ms window near t_est (s): where the voice breathes at a comma."""
    lo, hi = int(max(0, t_est + win[0]) * SR), int(min(len(c) / SR, t_est + win[1]) * SR)
    best, bi = 1e9, int(t_est * SR)
    for i in range(lo, max(lo + 1, hi - w), hop):
        e = float(np.mean(c[i:i + w] ** 2))
        if e < best: best, bi = e, i + w // 2
    return min(max(bi, 0), len(c))


def speak(lines, lang, voice, speed, pause_comma, pause_stop):
    """Natural-sounding lines with real pauses. Each sentence is voiced whole (keeps its melody) and sentences are
    joined by pause_stop. A comma's position is measured by voicing the sentence up to that comma; pause_comma of
    silence goes in at the quietest point there (never a gap inside a word like 'PS5').
    Returns [(clip, [[pause_start, pause_end] s, ...])]."""
    plan = []
    for ln in lines:
        sents = [x.strip() for x in _STOP.split(ln.strip()) if x.strip()]
        plan.append([(x, [x[:m.end()] for m in _COMMA.finditer(x)]) for x in sents])
    texts = [t for pl in plan for x, pre in pl for t in [x] + pre]
    clips = iter(tts(texts, lang, voice, speed))
    out = []
    for pl in plan:
        pieces, pauses, t = [], [], 0.0
        for si, (x, pre) in enumerate(pl):
            c = next(clips); cuts = []
            for p in pre:
                cuts.append(_quietest(c, len(next(clips)) / SR))
            last = 0
            for k in sorted(set(cuts)):
                pieces.append(c[last:k]); t += (k - last) / SR; last = k
                pieces.append(np.zeros(int(pause_comma * SR), np.float32)); pauses.append([round(t, 3), round(t + pause_comma, 3)]); t += pause_comma
            pieces.append(c[last:]); t += (len(c) - last) / SR
            if si < len(pl) - 1:
                pieces.append(np.zeros(int(pause_stop * SR), np.float32)); pauses.append([round(t, 3), round(t + pause_stop, 3)]); t += pause_stop
        out.append((np.concatenate(pieces).astype(np.float32), pauses))
    return out


def tts(lines, lang, voice, speed):
    if lang == 'en':
        from kokoro_onnx import Kokoro
        k = Kokoro(f'{MODELS}/kokoro.onnx', f'{MODELS}/voices.bin')
        out = []
        for ln in lines:
            v = voice if '+' not in voice else np.mean([k.get_voice_style(x) for x in voice.split('+')], axis=0)
            s, sr = k.create(ln, voice=v, speed=speed, lang='en-gb' if voice.startswith('b') else 'en-us')
            out.append(_trim(_resample(np.asarray(s), sr)))
        return out
    if lang == 'ar':
        import sherpa_onnx
        p = f'{MODELS}/{AR_VOICES.get(voice, voice)}'
        d = os.path.dirname(p)
        cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=p + '.onnx', tokens=d + '/tokens.txt',
                                                       data_dir=d + '/espeak-ng-data'), num_threads=4),
            max_num_sentences=1)
        t = sherpa_onnx.OfflineTts(cfg)
        out = []
        for ln in lines:
            a = t.generate(ln, sid=0, speed=speed)
            out.append(_trim(_resample(np.asarray(a.samples, np.float32), a.sample_rate), 0.015))
        return out
    raise ValueError(f'unsupported lang {lang!r}')


def rhubarb(wav, lang, dialog_text):
    exe = shutil.which('rhubarb') or f'{MODELS}/rhubarb/rhubarb'
    cmd = [exe, '-q', '-f', 'json', '--extendedShapes', 'GHX', wav]
    if lang == 'en':
        dlg = wav + '.txt'
        open(dlg, 'w').write(dialog_text)
        cmd[1:1] = ['-d', dlg]
    else:
        cmd[1:1] = ['-r', 'phonetic']      # language-independent recognizer
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return [[c['start'], c['value']] for c in json.loads(res.stdout)['mouthCues']]


# ----------------------------------------------------------------------------- SFX (synthesized)
_rng = np.random.default_rng(7)
def _t(d): return np.arange(int(d * SR)) / SR
def sfx_pop():
    x = _t(0.12); f = 300 + 900 * x / 0.12
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 30) * 0.6
def sfx_tap():
    x = _t(0.06); return (np.sin(2 * np.pi * 1700 * x) * np.exp(-x * 90) + _rng.normal(0, 1, len(x)) * np.exp(-x * 400) * 0.3) * 0.55
def sfx_key():
    x = _t(0.04); return (np.sin(2 * np.pi * 1150 * x) * np.exp(-x * 120) + _rng.normal(0, 1, len(x)) * np.exp(-x * 600) * 0.25) * 0.4
def sfx_whoosh(d=0.38):
    x = _t(d); n = _rng.normal(0, 1, len(x))
    for _ in range(3): n = np.convolve(n, np.ones(9) / 9, mode='same')
    return n * np.sin(np.pi * x / d) ** 2 * 1.4
def sfx_chime():
    a = sfx_tap() * 1.2; x = _t(0.9)
    ch = (np.sin(2 * np.pi * 1046 * x) * 0.5 + np.sin(2 * np.pi * 1568 * x) * 0.35) * np.exp(-x * 5) * 0.35
    out = np.zeros(int(1.1 * SR)); out[:len(a)] += a; out[int(0.12 * SR):int(0.12 * SR) + len(ch)] += ch
    return out


# ----------------------------------------------------------------------------- timeline
def build(ep, spec):
    lang, voice, speed = spec.get('lang', 'en'), spec.get('voice', 'am_puck' if spec.get('lang', 'en') == 'en' else 'kareem'), spec.get('speed', 1.0 if spec.get('lang', 'en') == 'en' else 1.3)
    beats = spec['beats']
    says = [b['say'] for b in beats]
    cache = _dir(f'host_{ep}')
    pc, ps = spec.get('pause_comma', PAUSE_COMMA), spec.get('pause_stop', PAUSE_STOP)
    key = hashlib.sha1(json.dumps([lang, voice, speed, says, 'sentences+commas', pc, ps]).encode()).hexdigest()[:12]
    cpath = f'{cache}/voice_{key}.npz'
    if os.path.exists(cpath):
        z = np.load(cpath, allow_pickle=True); clips, pauses = list(z['clips']), [list(p) for p in z['pauses']]
    else:
        print(f'[host] TTS {len(says)} lines ({lang}/{voice}, speed {speed}) ...', flush=True)
        res = speak(says, lang, voice, speed, pc, ps); clips, pauses = [r[0] for r in res], [r[1] for r in res]
        np.savez(cpath, clips=np.array(clips, dtype=object), pauses=np.array(pauses, dtype=object))
    # layout
    t = LEAD; B = []
    for b, c, pz in zip(beats, clips, pauses):
        d = len(c) / SR
        B.append({'start': round(t, 3), 'end': round(t + d, 3), 'cap': b.get('cap', b['say']),
                  'pose': b.get('pose'), 'hook': bool(b.get('hook')), 'step': b.get('step'),
                  'pauses': [[round(t + a, 3), round(t + e, 3)] for a, e in pz]})
        t += d + b.get('gap', spec.get('gap', GAP))
    total = B[-1]['end'] + END_HOLD
    N = int(np.ceil(total * SR)); voice_track = np.zeros(N, np.float32)
    for bb, c in zip(B, clips):
        a = int(bb['start'] * SR); voice_track[a:a + len(c)] += c
    # lip-sync
    import soundfile as sf
    vwav = f'{cache}/voice_{key}.wav'
    sf.write(vwav, voice_track, SR, subtype='PCM_16')
    cj = f'{cache}/cues_{key}.json'
    if os.path.exists(cj):
        cues = json.load(open(cj))
    else:
        print('[host] Rhubarb lip-sync ...', flush=True)
        cues = rhubarb(vwav, lang, '\n'.join(says)); json.dump(cues, open(cj, 'w'))
    hop = SR // FPS; nf = int(np.ceil(total * FPS))
    env = np.array([np.sqrt(np.mean(voice_track[i * hop:(i + 1) * hop] ** 2)) if i * hop < N else 0 for i in range(nf)])
    env = np.clip(env / (np.percentile(env[env > 0.005], 92) + 1e-9), 0, 1.2)
    # events
    ev = []; cur = spec['start']; sfx = []
    for b, bb in zip(beats, B):
        s0, dur = bb['start'], bb['end'] - bb['start']
        at = lambda f: s0 + f * dur
        if b.get('screen'):
            ev.append({'k': 'nav', 't': s0 - 0.05, 'to': b['screen'], 'style': b.get('style', 'fade')}); cur = b['screen']
            sfx.append(('whoosh', s0 - 0.05, 0.6))
        if b.get('end'):
            ev.append({'k': 'phone_out', 't': s0 - 0.2}); sfx += [('whoosh', s0 - 0.2, 1), ('pop', s0 + 0.25, 1)]
        for a in b.get('do', []):
            if 'tap' in a:
                tt = at(a.get('at', 0.5))
                ev.append({'k': 'tap', 't': tt, 'target': f"{cur}:{a['tap']}", 'fx': a.get('fx', 0.62),
                           'hold': a.get('hold', 0.55 if a.get('nav') else 0.35)}); sfx.append(('tap', tt, 1))
                if a.get('nav'):
                    ev.append({'k': 'nav', 't': tt + 0.22, 'to': a['nav'], 'style': 'pop' if a.get('back') else 'push'})
                    sfx.append(('whoosh', tt + 0.2, 0.6)); cur = a['nav']
            elif 'nav' in a:
                tt = at(a.get('at', 0)); ev.append({'k': 'nav', 't': tt, 'to': a['nav'], 'style': a.get('style', 'fade')})
                sfx.append(('whoosh', tt, 0.7)); cur = a['nav']
            elif 'type' in a:
                ks = a['type']; ts = np.linspace(at(a.get('from', 0.2)), at(a.get('to', 0.5)), len(ks))
                for d, tt in zip(ks, ts):
                    ev.append({'k': 'key', 't': float(tt), 'd': d, 'screen': cur}); sfx.append(('key', float(tt), 1))
            elif 'reprompt' in a:
                ev.append({'k': 'passreset', 't': at(a.get('at', 0.5)), 'screen': cur}); sfx.append(('whoosh', at(a.get('at', 0.5)), 0.7))
            elif 'keys' in a:                                   # laptop: keyboard shortcut chord
                tt = at(a.get('at', 0.5)); ev.append({'k': 'keys', 't': tt, 'keys': a['keys'], 'hold': a.get('hold', 1.6)})
                sfx += [('key', tt + i * 0.09, 1.2) for i in range(len(a['keys']))]
            elif 'focus' in a:                                  # tv: D-pad moves the highlight
                tt = at(a.get('at', 0.5)); ev.append({'k': 'focus', 't': tt, 'target': f"{cur}:{a['focus']}"})
                if a.get('button'): ev.append({'k': 'button', 't': tt, 'b': a['button']})
                sfx.append(('key', tt, 1))
            elif 'button' in a:                                 # tv: controller press (+ optional screen change)
                tt = at(a.get('at', 0.5)); ev.append({'k': 'button', 't': tt, 'b': a['button']}); sfx.append(('tap', tt, 1))
                if a.get('nav'):
                    ev.append({'k': 'nav', 't': tt + 0.2, 'to': a['nav'], 'style': 'pop' if a.get('back') else 'push'})
                    sfx.append(('whoosh', tt + 0.18, 0.6)); cur = a['nav']
            elif 'show' in a or 'hide' in a:                    # overlays declared in a screen's 'pops'
                nm = a.get('show') or a.get('hide'); tt = at(a.get('at', 0.5))
                ev.append({'k': 'show' if 'show' in a else 'hide', 't': tt, 'el': nm if ':' in nm else f'{cur}:{nm}'})
                sfx.append(('pop', tt, 0.8))
            elif 'typetext' in a:                               # text appearing in a 'window' screen
                t0, t1 = at(a.get('from', 0.3)), at(a.get('to', 0.6)); into = a.get('into', 'text')
                ev.append({'k': 'typetext', 't': t0, 't0': t0, 't1': t1, 'text': a['typetext'],
                           'el': into if ':' in into else f'{cur}:{into}', 'replace': bool(a.get('replace'))})
                n = max(1, len(a['typetext'])); sfx += [('key', float(x), 0.8) for x in np.linspace(t0, t1, min(n, 14))]
            elif 'set' in a:                                    # change a row's value / toggle without a tap
                tt = at(a.get('at', 0)); e = {'k': 'set', 't': tt, 'target': f"{a.get('screen', cur)}:{a['set']}"}
                if 'value' in a: e['value'] = a['value']
                if 'toggle' in a: e['toggle'] = a['toggle']
                ev.append(e)
            elif 'fx' in a:
                tt = at(a.get('at', 0)); ev.append({'k': 'fx', 't': tt, 'fx': a['fx'], 'dur': a.get('dur', 3)})
                if a['fx'] == 'lock_close': sfx.append(('chime', tt, 1))
                if a['fx'] in ('confetti', 'thumb'): sfx.append(('pop', tt, 0.8))
        if bb['step']:
            sfx.append(('pop', s0 - 0.1, 0.5))
    ev.sort(key=lambda e: e['t'])
    # soundtrack: voice + SFX (no music: the page's audio is instrument-free)
    fx = np.zeros(N, np.float32)
    lib_sfx = {'pop': sfx_pop, 'tap': sfx_tap, 'key': sfx_key, 'whoosh': sfx_whoosh, 'chime': sfx_chime}
    sfx.append(('pop', 0.05, 0.7))
    for kind, tt, g in sfx:
        sig = lib_sfx[kind](); a = int(max(0, tt) * SR); bnd = min(N, a + len(sig))
        fx[a:bnd] += (sig[:bnd - a] * g).astype(np.float32)
    mix = voice_track + fx * 0.45
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.95)
    sf.write(lib.out(f'audio_{ep}.wav'), mix, SR)
    with open(lib.out(f'meta_{ep}'), 'w') as f:
        f.write(f'FR={FPS}\nCF=0\n')
    keep = ('title', 'tag', 'tip', 'endline', 'follow', 'clock', 'start', 'screens', 'device', 'devices', 'start_pops')
    host = {k: spec[k] for k in keep if k in spec}
    host.update({'fps': FPS, 'total': total, 'lang': lang, 'beats': B, 'events': ev,
                 'env': [round(float(x), 3) for x in env], 'cues': cues})
    json.dump(host, open(f'{cache}/host.json', 'w'))
    return host


# ----------------------------------------------------------------------------- capture
async def _capture(ep, host, frames):
    from playwright.async_api import async_playwright
    out = _dir(f'frames_{ep}')
    async with async_playwright() as p:
        # cloud sessions ship a Chromium at /opt/pw-browsers/chromium that may be older than the installed Playwright
        exe = os.environ.get('TW_CHROME') or ('/opt/pw-browsers/chromium' if os.path.exists('/opt/pw-browsers/chromium') else None)
        br = await p.chromium.launch(executable_path=exe, args=['--allow-file-access-from-files', '--disable-web-security'])
        async def page():
            pg = await br.new_page(viewport={'width': 1080, 'height': 1920})
            await pg.add_init_script(f'window.HOST={json.dumps(host)};')
            await pg.goto(SCENE)
            await pg.wait_for_function('window.READY===true', timeout=60000)
            return pg
        pages = [await page() for _ in range(WORKERS)]
        q = list(frames); done = [0]
        async def work(pg):
            while q:
                fi = q.pop(0)
                await pg.evaluate(f'render({fi / FPS})')
                await pg.screenshot(path=f'{out}/{fi:05d}.png')
                done[0] += 1
                if done[0] % 150 == 0:
                    print(f'[host] {done[0]}/{len(frames)} frames', flush=True)
        await asyncio.gather(*(work(pg) for pg in pages))
        await br.close()


def run(ep, spec):
    host = build(ep, spec)
    n = int(round(host['total'] * FPS))
    frames = [int(a) for a in sys.argv[1:]] or list(range(n))
    print(f'[host] {ep}: {host["total"]:.1f} s, {n} frames, rendering {len(frames)} ...', flush=True)
    asyncio.run(_capture(ep, host, frames))
    print(f'[host] done -> out/frames_{ep}/  (audio out/audio_{ep}.wav)')

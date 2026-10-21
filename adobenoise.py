"""Tech Wall HOST episode (laptop) with a supplied voice-over: Adobe Podcast Enhance Speech removes background noise.
    ./build.sh adobenoise  |  python3 adobenoise.py 0 150 400
Voice: the user's generated audio (host/voices/adobe.flac); beat 't' = [start, end] s in it.
Before/after demo: an 'insert' clip played after "Listen to the difference" (the host stays silent, later lines move by
its length). DEMO = host/voices/adobe_demo_sim.flac is a SIMULATION (the user's own line with synthetic traffic, fan and
chatter noise, then clean) and is labelled on screen; swap in the user's real original + Adobe-enhanced clips (one file:
0.3 s silence, original, 0.6 s, enhanced, 0.3 s) and recompute BARS_* from them.
Facts (2026): free web tool at podcast.adobe.com/enhance; free plan about 1 h of audio per day, files up to 30 min;
video files need Premium. Generic browser + page look-alike, no Adobe logo."""
import host

EP = 'adobenoise'
DEMO, DEMO_AT = 'host/voices/adobe_demo_sim.flac', 20.5
DEMO_LEN, CLIP, SIMULATED = 5.36, 2.08, True
SHIFT = lambda x: round(x + DEMO_LEN, 3) if x >= DEMO_AT else x
P0 = DEMO_AT + 0.3                                # original plays [P0, P0+CLIP]
P1 = P0 + CLIP + 0.6                              # enhanced plays [P1, P1+CLIP]

BARS_ORIG = [0.31, 0.332, 0.817, 0.622, 0.659, 0.68, 0.766, 0.798, 0.844, 0.616, 0.558, 0.598, 0.5, 0.646, 0.451, 0.512,
             0.443, 0.495, 0.452, 0.33, 0.491, 0.56, 0.916, 0.586, 0.336, 0.865, 0.616, 0.376, 0.468, 0.559, 0.957, 0.883,
             0.417, 0.322, 0.673, 0.776, 0.745, 1.0, 0.77, 0.851, 0.658, 0.544, 0.66, 0.637, 0.576, 0.335, 0.32, 0.642,
             0.433, 0.383, 0.532, 0.441, 0.487, 0.419, 0.386, 0.82]
BARS_CLEAN = [0.046, 0.107, 0.75, 0.573, 0.555, 0.716, 0.708, 0.673, 0.65, 0.561, 0.417, 0.532, 0.439, 0.511, 0.375, 0.38,
              0.397, 0.29, 0.218, 0.025, 0.263, 0.501, 1.0, 0.579, 0.027, 0.701, 0.547, 0.107, 0.373, 0.553, 0.822, 0.74,
              0.258, 0.115, 0.524, 0.669, 0.663, 0.992, 0.623, 0.713, 0.431, 0.506, 0.584, 0.586, 0.444, 0.012, 0.095,
              0.547, 0.311, 0.314, 0.39, 0.348, 0.38, 0.212, 0.087, 0.04]
RED, GRN, VIO = '#ff5a5f', '#34d399', '#8b7cff'

CHROME = ('<div style="position:absolute;left:0;right:0;top:0;height:74px;background:#e9ecf2;font-family:Poppins">'
          '<div style="position:absolute;left:14px;top:12px;display:flex;gap:7px"><i style="width:12px;height:12px;border-radius:50%;background:#ff5f57"></i>'
          '<i style="width:12px;height:12px;border-radius:50%;background:#febc2e"></i><i style="width:12px;height:12px;border-radius:50%;background:#28c840"></i></div>'
          '<div style="position:absolute;left:84px;top:6px;width:210px;height:26px;border-radius:9px 9px 0 0;background:#fff;font-size:13px;'
          'padding:5px 12px;color:#333">🎙️ Enhance Speech</div>'
          '<div style="position:absolute;left:14px;right:14px;top:38px;height:28px;border-radius:14px;background:#fff;font-size:15px;'
          'padding:4px 16px;color:#333">🔒 podcast.adobe.com/enhance</div></div>')
PAGE = 'position:absolute;left:0;right:0;top:74px;bottom:0;background:linear-gradient(160deg,#171a2b,#0e1020);color:#fff;font-family:Poppins'


def wave(bars, col, x, y, w=600, h=86):
    bw = w / len(bars)
    return (f'<svg viewBox="0 0 {w} {h}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            + ''.join(f'<rect x="{i * bw + 1:.1f}" y="{h / 2 - max(2, v * h / 2):.1f}" width="{bw - 3:.1f}" height="{max(4, v * h):.1f}" '
                      f'rx="2" fill="{col}"/>' for i, v in enumerate(bars)) + '</svg>')


def badge(win, x, y, txt, bg, fg='#fff', size=17):
    return (f'<div data-in="{win}" style="position:absolute;left:{x}px;top:{y}px;background:{bg};color:{fg};font-weight:800;'
            f'font-size:{size}px;padding:5px 12px;border-radius:12px;white-space:nowrap">{txt}</div>')


def playhead(t0, t1, x, y, w=600):
    return (f'<div data-in="{t0 - .1:.2f},{t1 + .15:.2f}" style="position:absolute;left:0;top:0">'
            f'<div data-keys="{t0:.2f},{x},{y};{t1:.2f},{x + w},{y}" data-ease="linear" style="position:absolute;left:0;top:0;'
            'width:4px;height:100px;margin-left:-2px;background:#fff;box-shadow:0 0 10px #fff;border-radius:2px"></div></div>')


ENH = (CHROME + f'<div style="{PAGE}">'
       '<div style="position:absolute;left:28px;top:16px;font-size:26px;font-weight:800">Enhance Speech</div>'
       '<div style="position:absolute;left:28px;top:52px;font-size:14px;color:#aab0c8">Remove background noise from voice recordings</div>'
       f'<div style="position:absolute;right:26px;top:22px;display:flex;align-items:center;gap:10px;font-size:15px">Enhance'
       f'<span style="width:46px;height:26px;border-radius:13px;background:{VIO};position:relative"><i style="position:absolute;right:3px;top:3px;'
       'width:20px;height:20px;border-radius:50%;background:#fff"></i></span></div>'
       f'<div style="position:absolute;left:28px;top:112px;font-size:17px;font-weight:700;color:{RED}">Original</div>'
       + wave(BARS_ORIG, RED, 160, 96)
       + f'<div style="position:absolute;left:28px;top:252px;font-size:17px;font-weight:700;color:{GRN}">Enhanced ✨</div>'
       + wave(BARS_CLEAN, GRN, 160, 236)
       + badge('-1,6.0', 640, 92, 'NOISY 😖', RED) + badge('-1,6.0', 640, 232, 'CLEAN ✨', GRN, '#0b2b1e')
       + badge('6.3,10.1', 690, 340, 'FREE · AI', VIO)
       + playhead(P0, P0 + CLIP, 160, 89) + playhead(P1, P1 + CLIP, 160, 229)
       + badge(f'{P0 - .1:.2f},{P0 + CLIP + .2:.2f}', 640, 92, '▶ ORIGINAL', RED)
       + badge(f'{P1 - .1:.2f},{P1 + CLIP + .2:.2f}', 640, 232, '▶ ENHANCED', GRN, '#0b2b1e')
       + (badge(f'{DEMO_AT:.2f},{DEMO_AT + DEMO_LEN:.2f}', 28, 380, 'Simulated example', 'rgba(255,255,255,.14)', '#cfd6ee', 13)
          if SIMULATED else '')
       + f'<div data-in="{SHIFT(24.3):.2f}" style="position:absolute;left:-2px;top:-42px;width:920px;height:34px;'
         f'border:3px solid #ffd54a;border-radius:16px;box-shadow:0 0 18px rgba(255,213,74,.7)"></div>'
       + '</div>')

UPLOAD = (CHROME + f'<div style="{PAGE}">'
          '<div style="position:absolute;left:28px;top:16px;font-size:26px;font-weight:800">Enhance Speech</div>'
          '<div style="position:absolute;left:28px;top:52px;font-size:14px;color:#aab0c8">Remove background noise from voice recordings</div>'
          '<div style="position:absolute;left:140px;top:90px;width:640px;height:300px;border:3px dashed #5a6290;border-radius:22px;'
          'text-align:center;padding-top:40px"><div style="font-size:54px">☁️</div><div style="font-size:22px;font-weight:700;margin-top:6px">'
          'Drag & drop your audio</div><div style="font-size:15px;color:#aab0c8;margin-top:4px">or</div>'
          f'<div data-id="choose" style="display:inline-block;margin-top:10px;background:{VIO};border-radius:20px;padding:8px 26px;'
          'font-weight:700;font-size:17px">Choose files</div></div>'
          '<div data-keys="13.7,460,520;14.5,460,250" style="position:absolute;left:0;top:0;width:340px;height:74px;margin:-37px 0 0 -170px;'
          'background:#fff;color:#111;border-radius:16px;box-shadow:0 12px 30px rgba(0,0,0,.4);display:flex;align-items:center;gap:12px;'
          'padding:0 16px;font-size:16px;font-weight:700"><span style="font-size:30px">🎵</span><div style="flex:1">my-video-audio.wav'
          '<div style="height:8px;border-radius:4px;background:#e3e6ef;margin-top:6px;overflow:hidden">'
          f'<div data-ring="15.4,19.25" style="height:8px;width:calc(var(--p,0) * 100%);background:{VIO}"></div></div></div></div>'
          + badge('15.3,19.6', 360, 300, 'Enhancing with AI… ✨', VIO, size=19) + '</div>')

SPEC = {
    'audio': 'host/voices/adobe.flac', 'insert': {'at': DEMO_AT, 'audio': DEMO}, 'lang': 'en', 'device': 'laptop',
    'title': "Don't delete that noisy video! 🎙️", 'tag': 'AI TOOL · NOISE REMOVAL', 'tip': 'AI #01',
    'start': 'enh',
    'screens': {'enh': {'type': 'html', 'bg': '#0e1020', 'html': ENH},
                'upload': {'type': 'html', 'bg': '#0e1020', 'html': UPLOAD}},
    'beats': [
        {'t': [0.17, 5.45], 'say': "Recorded a video with traffic, fans, or people talking in the background? Don't delete it yet!",
         'cap': "Noisy video? Don't delete it yet! 🎙️", 'pose': 'welcome', 'hook': True},
        {'t': [6.12, 9.98], 'say': 'This free AI tool from Adobe can clean up the voice in seconds.',
         'cap': 'This free Adobe AI tool cleans up the voice in seconds', 'pose': 'talk'},
        {'t': [10.56, 13.05], 'say': 'Just open Adobe Podcast Enhance Speech,',
         'cap': 'Step 1: Open Adobe Podcast Enhance Speech', 'pose': 'point', 'step': 1, 'screen': 'upload', 'style': 'fade'},
        {'t': [13.41, 14.91], 'say': 'upload the audio from your video,',
         'cap': 'Step 2: Upload the audio from your video', 'pose': 'point', 'step': 2, 'do': [{'tap': 'choose', 'at': .12}]},
        {'t': [15.27, 18.70], 'say': 'and let AI remove the background noise while making your voice clearer.',
         'cap': 'Step 3: AI removes the noise and makes your voice clearer ✨', 'pose': 'point', 'step': 3},
        {'t': [19.42, 20.24], 'say': 'Listen to the difference.', 'cap': 'Listen to the difference 🎧', 'pose': 'talk',
         'do': [{'nav': 'enh', 'style': 'fade', 'at': .0}]},
        {'t': [20.94, 23.74], 'say': "It's like upgrading your microphone without buying new equipment!",
         'cap': 'Like upgrading your mic without buying new gear 🎤', 'pose': 'welcome', 'do': [{'fx': 'thumb', 'at': .2, 'dur': 2.4}]},
        {'t': [24.37, 28.45], 'say': 'Try it free at podcast dot adobe dot com slash enhance.',
         'cap': 'Try it free: podcast.adobe.com/enhance', 'pose': 'point'},
        {'t': [28.79, 31.17], 'say': 'Follow Tech Wall for more AI tools worth knowing.',
         'cap': 'Follow Tech Wall for more AI tools worth knowing! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

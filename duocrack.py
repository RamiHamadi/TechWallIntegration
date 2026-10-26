"""Tech Wall HOST news explainer with a supplied voice-over: crack reports on Apple's first foldable (iPhone Duo).
    ./build.sh duocrack  |  python3 duocrack.py 0 150 400
Device 'stage' (blueprint illustration, no logos): a generic unfolded foldable with a crack along the crease, a magnifier,
hinge-vs-display question, a side-view fold loop with a fold counter and a display-layer stack, status + poll cards.
Voice: the user's generated audio, pauses between phrases shortened to 0.2 s (host/voices/duocrack.flac).
Facts (The National 2026-10-25, MacRumors via TBS/Gulf Business/Switching to Mac, The Next Web, Tom's Guide): iPhone Duo,
$1,999, on sale 2026-10-23; first-week owners report cracks / a line of bright pixels along the hinge (about 10 public
cases, no verified failure rate); Apple's support article says the fix is replacing the inner display; units sent to
engineering; no confirmed cause, recall or repair program."""
import host

EP = 'duocrack'
INK, CY, YEL, RED, GRN = '#e9f1ff', '#5ce1ff', '#ffd54a', '#ff6b6b', '#7CFC9A'
PX, PY, PW, PH = 265, 30, 470, 460            # unfolded phone on the stage
CX = PX + PW // 2                             # crease x


def pin(win, x, y, w, h, inner, extra=''):
    return f'<div data-in="{win}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">{inner}</div>'


def card(win, tag, title, body, col=YEL, top=575):
    return (f'<div data-in="{win}" style="position:absolute;left:455px;top:{top}px;width:530px;background:rgba(6,20,52,.88);'
            f'border:4px solid {col};border-radius:24px;padding:16px 20px;box-shadow:0 12px 30px rgba(0,0,0,.35)">'
            f'<div style="display:inline-block;background:{col};color:#0a2b66;font-weight:800;font-size:22px;padding:4px 14px;'
            f'border-radius:14px">{tag}</div><div style="font-weight:800;font-size:34px;margin-top:6px;line-height:1.15">{title}</div>'
            f'<div style="font-size:24px;color:#cfe3ff;line-height:1.35;margin-top:6px">{body}</div></div>')


CRACK = 'M0 0 L9 34 L-6 70 L7 104 L-4 140 L10 176 L-3 212 L6 250'


def phone(crack_win, glow=True):
    """Generic unfolded foldable (no logo): two halves, a crease, a crack + a bright pixel line along the crease."""
    half = (f'position:absolute;top:14px;width:{PW // 2 - 18}px;height:{PH - 28}px;background:linear-gradient(160deg,#3a6bd8 0%,#7a4fd6 55%,#1b1f6b 100%)')
    return (f'<div style="position:absolute;left:{PX}px;top:{PY}px;width:{PW}px;height:{PH}px;border-radius:34px;background:#0b0f1a;'
            'box-shadow:0 0 0 4px #2b3a55,0 30px 60px rgba(0,0,0,.45)">'
            f'<div style="{half};left:14px;border-radius:22px 4px 4px 22px"></div>'
            f'<div style="{half};right:14px;border-radius:4px 22px 22px 4px"></div>'
            f'<div style="position:absolute;left:{PW // 2 - 4}px;top:14px;width:8px;height:{PH - 28}px;'
            'background:linear-gradient(90deg,rgba(0,0,0,.35),rgba(255,255,255,.18),rgba(0,0,0,.35))"></div>'
            '<div style="position:absolute;left:34px;top:40px;color:#fff;font-size:44px;font-weight:300">10:08</div>'
            '<div style="position:absolute;left:34px;top:96px;color:#dfe6ff;font-size:18px">Sunday, 26 October</div>'
            + pin(crack_win, PW // 2, 80, 30, 260,
                  '<svg width="40" height="270" viewBox="-15 -5 40 270" style="position:absolute;left:-15px;top:-5px">'
                  f'<path d="{CRACK}" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round" '
                  'style="filter:drop-shadow(0 0 6px #fff)"/>'
                  f'<path d="M3 20 L22 44 M-4 120 L-14 150 M5 190 L19 214" stroke="#fff" stroke-width="2.5"/></svg>'
                  + (f'<div style="position:absolute;left:6px;top:-66px;width:4px;height:{PH - 28}px;background:#bdf6ff;'
                     'box-shadow:0 0 12px #5ce1ff,0 0 24px #5ce1ff"></div>' if glow else ''))
            + '</div>')


PRICE = pin('-1', 660, 8, 170, 76,
            f'<div style="transform:rotate(8deg);background:{YEL};color:#0a2b66;border-radius:14px;padding:6px 14px;font-weight:900;'
            'font-size:38px;text-align:center;box-shadow:0 10px 20px rgba(0,0,0,.35)">$1,999</div>')
WARN = pin('-1', 150, 30, 120, 120,
           f'<div style="width:110px;height:110px;border-radius:50%;background:{RED};display:grid;place-items:center;font-size:58px;'
           'box-shadow:0 0 0 6px rgba(255,107,107,.3),0 12px 24px rgba(0,0,0,.35)">⚠️</div>', '')
LABEL = pin('-1', 300, 505, 400, 60,
            '<div style="text-align:center;font-size:26px;font-weight:800;letter-spacing:3px;color:#cfe3ff">iPHONE DUO · FOLDABLE</div>')
# magnifier on the crease (reports)
MAG = (pin('5.3,9.95', 700, 130, 290, 290,
           '<div style="position:absolute;inset:0;border-radius:50%;border:8px solid #dfe6f5;overflow:hidden;'
           'background:linear-gradient(90deg,#3a6bd8 0 46%,#283a8a 46% 54%,#7a4fd6 54% 100%);box-shadow:0 18px 40px rgba(0,0,0,.45)">'
           '<svg width="290" height="290" viewBox="0 0 290 290" style="position:absolute;left:-8px;top:-8px">'
           '<path d="M140 0 L160 60 L130 120 L158 180 L132 240 L150 290" fill="none" stroke="#fff" stroke-width="7" '
           'style="filter:drop-shadow(0 0 8px #fff)"/><path d="M150 40 L196 82 M134 150 L96 196" stroke="#fff" stroke-width="4"/>'
           '<rect x="160" y="0" width="7" height="290" fill="#bdf6ff" style="filter:drop-shadow(0 0 10px #5ce1ff)"/></svg></div>'
           '<div style="position:absolute;right:-8px;bottom:-14px;background:#0a2b66;border:3px solid #fff;border-radius:12px;'
           'padding:2px 10px;font-size:18px;font-weight:800">CREASE ×6</div>')
       + pin('5.3,9.95', 528, 240, 175, 6, f'<div style="height:4px;background:#dfe6f5;border-radius:2px;transform:rotate(-8deg)"></div>'))

MAIN = (phone('-1') + PRICE + WARN + LABEL + MAG
        + card('5.4,9.95', 'REPORTED · WEEK 1', 'Cracks along the hinge', 'A line of bright pixels on the inner screen ·<br>'
               'about 10 public cases so far', RED))

# hinge vs display
VS = (phone('-1', glow=False)
      + pin('11.4', 40, 110, 240, 260,
            '<div style="text-align:center"><div style="width:190px;height:190px;margin:0 auto;border-radius:50%;background:rgba(6,20,52,.9);'
            f'border:5px solid {CY};display:grid;place-items:center;font-size:96px">🔩</div>'
            '<div style="font-size:34px;font-weight:900;margin-top:10px">The hinge?</div></div>')
      + pin('13.5', 720, 110, 260, 260,
            '<div style="text-align:center"><div style="width:190px;height:190px;margin:0 auto;border-radius:50%;background:rgba(6,20,52,.9);'
            f'border:5px solid {YEL};display:grid;place-items:center;font-size:96px">📱</div>'
            '<div style="font-size:34px;font-weight:900;margin-top:10px;line-height:1.1">The ultra-thin<br>display?</div></div>')
      + pin('13.0', 445, 505, 110, 90, f'<div style="font-size:64px;font-weight:900;color:{RED};text-align:center">VS</div>')
      + card('10.15', 'THE BIG QUESTION', 'What is cracking the screen?', 'Hinge pressure… or a fragile display?', CY))

# fold loop + layers
HX, HY = 270, 250                              # hinge (side view)
FOLD_KEYS = ';'.join(f'{16.6 + i * .42:.2f},0,0,{0 if i % 2 == 0 else -165}' for i in range(14))
COUNT = [('1', 16.5), ('10', 17.4), ('100 a day', 18.3), ('3,000 a month', 19.3), ('36,500 a year', 20.4)]
COUNTER = ''.join(pin(f'{t:.2f},{(COUNT[i + 1][1] if i + 1 < len(COUNT) else 99):.2f}', 40, 420, 460, 80,
                      f'<div style="font-size:54px;font-weight:900;color:{YEL}">{n}</div>') for i, (n, t) in enumerate(COUNT))
LAYERS = [('Protective film', '#9fb6ff'), ('Ultra-thin cover layer', '#5ce1ff'), ('Touch layer', '#7CFC9A'),
          ('OLED panel', '#ff9f6b'), ('Support plate', '#b0b8c8')]
STACK = ''.join(pin(f'{19.2 + i * .25:.2f}', 560, 80 + i * 96, 430, 84,
                    f'<div style="display:flex;align-items:center;gap:16px"><div style="width:130px;height:{20 + (i == 1) * 8}px;'
                    f'border-radius:9px;background:{c};box-shadow:0 0 14px {c}"></div><div style="font-size:30px;font-weight:800;line-height:1.1">{n}</div></div>')
                for i, (n, c) in enumerate(LAYERS))
LAYERS_SCR = (f'<div style="position:absolute;left:30px;top:{HY - 11}px;width:{HX - 30}px;height:22px;border-radius:11px;background:#dfe6f5"></div>'
              f'<div data-keys="{FOLD_KEYS}" style="position:absolute;left:{HX}px;top:{HY - 11}px;width:240px;height:22px;border-radius:11px;'
              f'background:#dfe6f5;transform-origin:0 50%"></div>'
              f'<div style="position:absolute;left:{HX - 30}px;top:{HY - 30}px;width:60px;height:60px;border-radius:50%;background:{CY};'
              'box-shadow:0 0 18px #5ce1ff"></div>'
              f'<div style="position:absolute;left:30px;top:40px;font-size:36px;font-weight:800;color:#cfe3ff">Open · close · open…</div>'
              f'<div style="position:absolute;left:40px;top:370px;font-size:32px;font-weight:700;color:#cfe3ff">Folds:</div>' + COUNTER
              + f'<div style="position:absolute;left:560px;top:20px;font-size:34px;font-weight:900;color:{YEL}">Inside the screen</div>' + STACK
              + pin('20.0', 470, 90, 80, 440, f'<div style="font-size:64px;color:{RED};text-align:center;line-height:1.7">↕<br>↕<br>↕</div>'))

STATUS = (phone('-1') + PRICE + LABEL
          + card('22.2,25.1', 'STATUS', 'Cause not confirmed yet', "Apple's fix so far: replace the inner display ·<br>"
                 'units sent to engineers', YEL)
          + card('25.2', 'YOUR TURN', 'Would you pay $1,999 for a foldable iPhone?',
                 f'<div style="display:flex;gap:14px;margin-top:6px"><span style="flex:1;background:{GRN};color:#0a2b66;border-radius:14px;'
                 'text-align:center;font-weight:900;font-size:30px;padding:4px">YES 👍</span><span style="flex:1;background:'
                 f'{RED};color:#fff;border-radius:14px;text-align:center;font-weight:900;font-size:30px;padding:4px">NO 👎</span></div>', CY)
          + pin('27.6', 20, 440, 250, 70, '<div style="background:#fff;color:#111;border-radius:22px 22px 22px 6px;padding:12px 18px;'
                'font-size:24px;font-weight:700;box-shadow:0 12px 24px rgba(0,0,0,.35)">💬 Comment below 👇</div>'))

SPEC = {
    'audio': 'host/voices/duocrack.flac', 'lang': 'en', 'device': 'stage',
    'title': "Foldable iPhone cracking? ⚠️", 'tag': 'TECH NEWS · iPHONE DUO', 'tip': 'NEWS #01',
    'start': 'main',
    'screens': {
        'main': {'type': 'html', 'bg': 'transparent', 'html': MAIN},
        'vs': {'type': 'html', 'bg': 'transparent', 'html': VS},
        'layers': {'type': 'html', 'bg': 'transparent', 'html': LAYERS_SCR},
        'status': {'type': 'html', 'bg': 'transparent', 'html': STATUS},
    },
    'beats': [
        {'t': [0.0, 4.70], 'say': "Apple's two thousand dollar foldable iPhone could have a serious problem!",
         'cap': "REPORTS: APPLE'S $2,000 FOLDABLE iPHONE IS CRACKING ⚠️", 'capsize': 78, 'pose': 'point', 'hook': True},
        {'t': [4.90, 9.93], 'say': "Reports of cracked displays near the folding hinge are raising concerns about the phone's durability.",
         'cap': 'Owners report cracks along the folding hinge', 'pose': 'talk'},
        {'t': [10.13, 16.31], 'say': "But here's the big question: is the hinge damaging the screen, or is the ultra-thin display itself the weak point?",
         'cap': 'The hinge… or the ultra-thin display? 🤔', 'pose': 'welcome', 'do': [{'nav': 'vs', 'style': 'fade', 'at': 0}]},
        {'t': [16.51, 21.95], 'say': 'Foldable screens bend thousands of times, putting repeated stress on delicate display layers.',
         'cap': 'Every fold stresses the thin display layers', 'pose': 'talk', 'do': [{'nav': 'layers', 'style': 'fade', 'at': 0}]},
        {'t': [22.15, 24.97], 'say': 'Until the cause is confirmed, buyers should be cautious.',
         'cap': 'Until the cause is confirmed, be cautious ⚠️', 'pose': 'point', 'do': [{'nav': 'status', 'style': 'fade', 'at': 0}]},
        {'t': [25.17, 27.39], 'say': 'Would you spend two thousand dollars on a foldable iPhone?',
         'cap': 'Would you spend $2,000 on a foldable iPhone? 💬', 'pose': 'welcome'},
        {'t': [27.59, 28.35], 'say': 'Comment below', 'cap': 'Comment below 👇', 'pose': 'point'},
        {'t': [28.37, 30.43], 'say': 'and follow Tech Wall for daily tech news!', 'cap': 'Follow Tech Wall for daily tech news! 🚀',
         'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

"""Tech Wall HOST episode with a supplied voice-over: an AI chat that still answers in Airplane Mode (PocketPal).
    ./build.sh offlineai  |  python3 offlineai.py 0 150 400
Samsung Galaxy (One UI look-alike) running a generic PocketPal look-alike; chalk cards on the left ('overlay').
Voice: the user's generated audio, pauses between phrases shortened to 0.2 s (host/voices/offlineai.flac).
Facts (PocketPal GitHub + App Store, AnythingLLM docs, 2026): PocketPal AI is free and open source on iPhone and Android;
Menu > Models > download a small GGUF model (Gemma, Llama, Qwen, Phi; ~1 GB) once, Load it, then it chats with no
connection; prompts and answers stay on the device. Speed depends on the phone. Fictional chats, no logos."""
import host

EP = 'offlineai'
CY, YEL, BLU, GRN = '#5ce1ff', '#ffd54a', '#3e91ff', '#34d399'
T_DL = 6.98 + .38 * 5.2                   # "Download" tapped
T_DONE = 11.7                             # model on the phone
T_LOAD = 12.38 + .06 * 2.18               # "Load" tapped
T_PLANE = 12.38 + .62 * 2.18              # Airplane Mode tapped
T_SEND = 14.86 + .2 * 4.04                # question sent

SB_PLANE = ('<div class="sb"><span>10:08</span><span style="display:flex;gap:8px;align-items:center;font-size:15px">'
            '✈️<span class="bat"></span></span></div>')
SB_NET = ('<div class="sb"><span>10:08</span><span style="display:flex;gap:8px;align-items:center;font-size:13px">'
          '5G ▂▄▆█<span class="bat"></span></span></div>')


def bubble(side, inner, extra=''):
    me = side == 'me'
    return (f'<div {extra} style="display:flex;justify-content:{"flex-end" if me else "flex-start"};margin:0 14px 10px">'
            f'<div style="max-width:{"78%" if me else "88%"};background:{"#3e91ff" if me else "#fff"};color:{"#fff" if me else "#111"};'
            f'border-radius:20px;{"border-bottom-right-radius:6px" if me else "border-bottom-left-radius:6px"};padding:10px 15px;'
            f'font-size:19px;line-height:1.38;box-shadow:0 2px 6px rgba(0,0,0,.06)">{inner}</div></div>')


ANS_A = ('<b>Day 1:</b> Colosseum, Roman Forum, then dinner in Trastevere 🍝 '
         '<span data-type="chat:ansA"></span>')
CHAT = (SB_PLANE
        + '<div style="display:flex;align-items:center;gap:10px;padding:6px 18px 8px"><span style="font-size:28px">☰</span>'
          '<div style="flex:1"><div style="font-size:25px;font-weight:700">PocketPal</div>'
          '<div style="font-size:15px;color:#5a6b8c">Gemma 3 1B · on this phone</div></div>'
          '<span style="background:#e7f6ee;color:#137a43;border-radius:12px;padding:4px 12px;font-size:15px;font-weight:700">'
          '✈️ Offline</span></div>'
        + '<div style="height:1px;background:#e3e5ea;margin:0 0 12px"></div>'
        + bubble('me', 'Plan a 2-day trip to Rome 🇮🇹')
        + bubble('ai', ANS_A)
        + bubble('me', 'Write a birthday text for Mom 🎂', f'data-in="{T_SEND + .12:.2f}"')
        + f'<div data-in="{T_SEND + .2:.2f},{T_SEND + .75:.2f}" style="margin:0 14px 10px;width:80px;background:#fff;border-radius:20px;'
          'padding:8px 14px;font-size:24px;letter-spacing:3px;color:#8a8f99">•••</div>'
        + f'<div data-in="{T_SEND + .7:.2f}">' + bubble('ai', '<span data-type="chat:ansB"></span>') + '</div>'
        + '<div style="position:absolute;left:12px;right:12px;bottom:26px;height:54px;background:#fff;border-radius:27px;'
          'display:flex;align-items:center;padding:0 8px 0 18px;box-shadow:0 2px 10px rgba(0,0,0,.08)">'
          '<div style="flex:1;font-size:18px;color:#111;white-space:nowrap;overflow:hidden">'
          f'<span data-in="-1,{T_SEND + .1:.2f}"><span data-type="chat:q"></span></span></div>'
          f'<div data-id="send" style="width:40px;height:40px;border-radius:50%;background:{BLU};color:#fff;display:grid;'
          'place-items:center;font-size:20px">➤</div></div>')

MODEL_ROWS = [('gemma', 'Gemma 3 1B', '≈ 0.8 GB · Google'), ('llama', 'Llama 3.2 1B', '≈ 1.3 GB · Meta'),
              ('qwen', 'Qwen 2.5 1.5B', '≈ 1.1 GB · Alibaba')]


def model_card(k, mid, name, sub):
    top = 168 + k * 124
    card = (f'<div style="position:absolute;left:12px;right:12px;top:{top}px;height:112px;background:#fff;border-radius:22px;'
            f'padding:18px 18px;box-sizing:border-box"><div style="font-size:22px;font-weight:700">🧠 {name}</div>'
            f'<div style="font-size:16px;color:#8a8f99">{sub}</div></div>'
            f'<div data-id="dl_{mid}" style="position:absolute;right:28px;top:{top + 28}px;width:110px;height:42px;border-radius:21px;'
            f'background:#e8f1ff;color:{BLU};font-weight:700;font-size:16px;display:grid;place-items:center">⬇ Download</div>')
    if mid != 'gemma':
        return card
    # Gemma: progress bar while downloading, then "Load" (tap target) and "Loaded ✓"
    return (card
            + f'<div data-in="{T_DL + .15:.2f},{T_DONE:.2f}" style="position:absolute;left:30px;right:30px;top:{top + 94}px;height:8px;'
              'border-radius:4px;background:#e3e5ea;overflow:hidden">'
              f'<div data-ring="{T_DL + .25:.2f},{T_DONE - .1:.2f}" style="height:100%;width:calc(var(--p,0)*100%);background:{BLU}"></div></div>'
            + f'<div data-in="{T_DL + .15:.2f}" style="position:absolute;right:28px;top:{top + 28}px;width:110px;height:42px;'
              'border-radius:21px;background:#fff;color:#5a6b8c;font-weight:700;font-size:15px;display:grid;place-items:center">'
              f'<span data-in="{T_DL + .15:.2f},{T_DONE:.2f}">Downloading…</span></div>'
            + f'<div data-in="{T_DONE:.2f}" style="position:absolute;right:28px;top:{top + 28}px;width:110px;height:42px;'
              f'border-radius:21px;background:{BLU};color:#fff;font-weight:700;font-size:17px;display:grid;place-items:center">Load</div>'
            + f'<div data-in="{T_LOAD + .2:.2f}" style="position:absolute;right:28px;top:{top + 28}px;width:110px;height:42px;'
              'border-radius:21px;background:#e7f6ee;color:#137a43;font-weight:800;font-size:16px;display:grid;place-items:center">'
              'Loaded ✓</div>'
            + f'<div data-in="{T_DONE:.2f}" style="position:absolute;left:30px;top:{top + 80}px;font-size:14px;color:#137a43;'
              'font-weight:700">✓ Saved on this phone</div>')


def tile(left, top, icon, label, on_win, off_win):
    """One UI quick-panel tile: grey (off) and blue (on) versions, each shown over its window."""
    base = (f'position:absolute;left:{left}px;top:{top}px;width:76px;text-align:center;font-size:12px;color:#fff;')
    circ = 'width:62px;height:62px;margin:0 auto 6px;border-radius:50%;display:grid;place-items:center;font-size:28px;'
    out = ''
    if off_win:
        out += f'<div data-in="{off_win}" style="{base}"><div style="{circ}background:#3a3d46">{icon}</div>{label}</div>'
    if on_win:
        out += f'<div data-in="{on_win}" style="{base}"><div style="{circ}background:{BLU}">{icon}</div>{label}</div>'
    return out


PANEL = (f'<div data-keys="{T_LOAD + .35:.2f},0,-900;{T_LOAD + .75:.2f},0,0" style="position:absolute;left:0;top:0;width:404px;'
         'height:842px;background:linear-gradient(#181a20 0,#181a20 500px,rgba(10,12,18,.55) 500px);z-index:5;color:#fff">'
         '<div style="padding:22px 26px 0;font-size:30px;font-weight:300">10:08</div>'
         '<div style="padding:0 26px 16px;font-size:14px;color:#aab">Thu, 23 Oct</div>'
         + tile(26, 110, '📶', 'Wi-Fi', f'-1,{T_PLANE + .1:.2f}', f'{T_PLANE + .1:.2f}')
         + tile(118, 110, '🔊', 'Sound', '-1', None)
         + tile(210, 110, '🔵', 'Bluetooth', f'-1,{T_PLANE + .1:.2f}', f'{T_PLANE + .1:.2f}')
         + f'<div data-id="plane" style="position:absolute;left:302px;top:110px;width:76px;height:90px"></div>'
         + tile(302, 110, '✈️', 'Airplane mode', f'{T_PLANE + .1:.2f}', f'-1,{T_PLANE + .1:.2f}')
         + tile(26, 220, '📱', 'Mobile data', f'-1,{T_PLANE + .1:.2f}', f'{T_PLANE + .1:.2f}')
         + tile(118, 220, '🔦', 'Flashlight', None, '-1')
         + tile(210, 220, '🔄', 'Auto rotate', '-1', None)
         + tile(302, 220, '🌙', 'Dark mode', None, '-1')
         + f'<div data-in="{T_PLANE + .2:.2f}" style="position:absolute;left:26px;right:26px;top:350px;background:#22324f;'
           'border-radius:18px;padding:12px 16px;font-size:15px;line-height:1.5">✈️ Airplane mode is on<br>'
           '<span style="color:#aab">No internet · no Wi-Fi · no signal</span></div></div>')

MODELS = (SB_NET
          + '<div style="padding:34px 26px 6px;font-size:40px;font-weight:600">Models</div>'
          + '<div style="padding:0 26px;font-size:17px;color:#3e91ff;font-weight:600">Download once, use offline</div>'
          + ''.join(model_card(k, *m) for k, m in enumerate(MODEL_ROWS))
          + PANEL)


def card(win, top, html, border=CY, width=520):
    return (f'<div data-in="{win}" style="position:absolute;left:40px;top:{top}px;width:{width}px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.88);border:3px solid {border};border-radius:26px;padding:16px 22px">{html}</div>')


def chip(win, top, icon, text, col='#ff6b6b'):
    return card(win, top, f'<div style="display:flex;align-items:center;gap:16px;font-size:36px;font-weight:800">'
                          f'<span>{icon}</span><span style="flex:1">{text}</span><span style="color:{col};font-size:44px">✕</span></div>',
                col)


OVERLAY = (
    # frame 0 (cover): the payoff in words
    card('-1,3.95', 250, f'<div style="font-size:62px;font-weight:900;color:{YEL};line-height:1.08">✈️ AIRPLANE<br>MODE: ON</div>'
                         '<div style="font-size:34px;font-weight:700;margin-top:12px;line-height:1.45">🌐 Internet: none<br>'
                         f'<span style="color:{GRN}">⚡ AI still answering</span></div>', YEL)
    # "No internet. No Wi-Fi. No signal."
    + chip('4.0,6.95', 270, '🌐', 'No internet') + chip('4.95,6.95', 400, '📶', 'No Wi-Fi') + chip('6.08,6.95', 530, '📡', 'No signal')
    # the app
    + card('7.7,14.6', 250, '<div style="font-size:44px;font-weight:900">📲 PocketPal</div>'
                           '<div style="font-size:31px;line-height:1.6;margin-top:6px">Free · iPhone + Android<br>'
                           '🧠 Gemma · Llama · Qwen<br>📦 ~1 GB, download once</div>')
    # the result
    + card('19.15,21.4', 250, f'<div style="font-size:46px;font-weight:900;color:{YEL};line-height:1.12">📱 = your own<br>AI computer</div>'
                               '<div style="font-size:30px;line-height:1.6;margin-top:10px">✈️ Works offline<br>'
                               '🔒 Chats stay on your phone<br>💸 Free app</div>', YEL)
    + card('21.6', 330, '<div style="font-size:64px;font-weight:900;text-align:center">🔖 SAVE<br>THIS HACK</div>', YEL, 440)
)

SPEC = {
    'audio': 'host/voices/offlineai.flac', 'lang': 'en', 'device': 'galaxy', 'overlay': OVERLAY,
    'title': 'AI that works in Airplane Mode ✈️', 'tag': 'OFFLINE AI · POCKETPAL', 'tip': 'TIP #09',
    'start': 'chat',
    'screens': {
        'chat': {'type': 'html', 'bg': '#f4f4f6', 'html': CHAT},
        'models': {'type': 'html', 'bg': '#f4f4f6', 'html': MODELS},
    },
    'beats': [
        {'t': [0.0, 3.86], 'say': 'What if your AI assistant still worked with your phone in Airplane Mode?',
         'cap': 'RUN AI LIKE CHATGPT WITH NO INTERNET 📱✈️', 'capsize': 84, 'pose': 'point', 'hook': True,
         'do': [{'typetext': 'Day 2: Vatican Museums, St. Peter\'s, then sunset at the Spanish Steps 🌅',
                 'into': 'ansA', 'from': .02, 'to': .95}]},
        {'t': [4.06, 6.78], 'say': 'No internet. No Wi-Fi. No signal.',
         'cap': 'No internet. No Wi-Fi. No signal. 📵', 'pose': 'talk'},
        {'t': [6.98, 12.18], 'say': "Here's the trick: PocketPal lets you download an AI model directly onto your phone.",
         'cap': 'Step 1: In the free PocketPal app, download a small AI model (once)', 'pose': 'point', 'step': 1,
         'do': [{'nav': 'models', 'style': 'fade', 'at': 0}, {'tap': 'dl_gemma', 'at': .38, 'fx': .8}]},
        {'t': [12.38, 14.56], 'say': "Once it's downloaded, switch to Airplane Mode,",
         'cap': 'Step 2: Load it, then turn on Airplane Mode ✈️', 'pose': 'point', 'step': 2,
         'do': [{'tap': 'dl_gemma', 'at': .06, 'fx': .8}, {'tap': 'plane', 'at': .62}]},
        {'t': [14.86, 18.90], 'say': 'ask a question, and watch it generate an answer completely offline!',
         'cap': 'Step 3: Ask anything, it answers completely offline ⚡', 'pose': 'welcome', 'step': 3,
         'do': [{'nav': 'chat', 'style': 'fade', 'at': 0},
                {'typetext': 'Write a birthday text for Mom 🎂', 'into': 'q', 'from': .02, 'to': .17},
                {'tap': 'send', 'at': .2},
                {'typetext': 'Happy birthday, Mom! 🎂 Thank you for your love, your patience and the best hugs. '
                             'Have the most wonderful day! ❤️', 'into': 'ansB', 'from': .33, 'to': .97}]},
        {'t': [19.10, 21.44], 'say': 'Your phone becomes its own little AI computer.',
         'cap': 'Your phone becomes its own little AI computer 🧠', 'pose': 'talk',
         'do': [{'fx': 'thumb', 'at': .25, 'dur': 2.0}]},
        {'t': [21.64, 22.35], 'say': 'Save this hack', 'cap': 'Save this hack 🔖', 'pose': 'point'},
        {'t': [22.53, 23.94], 'say': 'and follow Tech Wall for more!', 'cap': 'Follow Tech Wall for more! 🚀',
         'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

"""Tech Wall HOST episode with a supplied voice-over: Google Find Hub finds an Android phone that is offline or switched off.
    ./build.sh findhub  |  python3 findhub.py 0 150 400
Samsung Galaxy (One UI look-alike) showing a Find Hub look-alike map, then the offline-finding setting; the network
(lost phone's Bluetooth beacon, nearby Android phones, encrypted reports) is drawn as chalk cards on the left ('overlay').
Voice: the user's generated audio, pauses between phrases shortened to 0.2 s (host/voices/findhub.flac).
Facts (Google Pixel Help 9338817, Android Help 3265955, 2026): Find Hub network uses nearby Android devices to locate
offline devices; Settings > Google > All services > Find Hub > Find your offline devices (Pixel: Settings > Security >
Find Hub) > Off / With network in high-traffic areas only / With network in all areas; needs a screen lock; Pixel 8, 9
and 10 series can be located for several hours after being switched off or running out of battery (not every Android).
Generic look-alikes, no logos, fictional data."""
import host

EP = 'findhub'
CY, YEL, BLU, GRN, RED = '#5ce1ff', '#ffd54a', '#3e91ff', '#34d399', '#ff6b6b'
T_ALL = 27.62 + .62 * 3.42                 # "With network in all areas" tapped

SB = '<div class="sb"><span>10:08</span><span class="bat"></span></div>'

ROADS = ''.join(f'<div style="position:absolute;{s};background:#fff;box-shadow:0 0 0 1px #d5dde8"></div>' for s in (
    'left:0;right:0;top:150px;height:16px', 'left:0;right:0;top:330px;height:22px', 'left:0;right:0;top:470px;height:12px',
    'left:90px;top:0;bottom:0;width:18px', 'left:250px;top:0;bottom:0;width:14px', 'left:330px;top:0;bottom:0;width:22px'))
BLOCKS = ''.join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:8px;background:{c}"></div>'
                 for x, y, w, h, c in [(118, 175, 120, 140, '#d7ecd3'), (272, 180, 50, 140, '#e2e6ee'), (118, 362, 120, 96, '#e2e6ee'),
                                       (10, 175, 70, 140, '#e2e6ee'), (272, 362, 50, 96, '#cfe6f7')])

FINDMAP = (SB
           + '<div style="position:absolute;left:0;right:0;top:62px;bottom:0;background:#eef2f7;overflow:hidden">' + ROADS + BLOCKS
           + '<div style="position:absolute;left:0;right:0;top:0;height:64px;background:linear-gradient(#eef2f7,rgba(238,242,247,0));'
             'display:flex;align-items:center;padding:0 22px;font-size:26px;font-weight:700">Find Hub</div>'
           # pin + accuracy circle
           + f'<div data-ring="0,1.2;1.6,2.8;3.2,4.4;4.8,6;14.8,16;16.4,17.6" style="position:absolute;left:150px;top:230px;width:110px;height:110px;'
             f'border-radius:50%;background:rgba(62,145,255,.18);border:2px solid {BLU};transform:scale(calc(.6 + var(--p,0) * .9));'
             'opacity:calc(1 - var(--p,0) * .8)"></div>'
           + f'<div style="position:absolute;left:170px;top:200px;width:70px;height:84px">'
             f'<div style="width:70px;height:70px;border-radius:50% 50% 50% 6px;transform:rotate(-45deg);background:{BLU};'
             'box-shadow:0 8px 16px rgba(0,0,0,.25)"></div><div style="position:absolute;left:21px;top:15px;width:28px;height:42px;'
             'border-radius:6px;background:#1b1f2a;border:2px solid #fff"></div></div>'
           # bottom sheet
           + '<div style="position:absolute;left:0;right:0;bottom:0;height:330px;background:#fff;border-radius:30px 30px 0 0;'
             'box-shadow:0 -6px 20px rgba(0,0,0,.12);padding:14px 24px;box-sizing:border-box">'
             '<div style="width:50px;height:5px;border-radius:3px;background:#d0d4dc;margin:0 auto 14px"></div>'
             '<div style="font-size:26px;font-weight:800">My phone</div>'
             '<div style="font-size:17px;color:#5a6b8c;margin-top:2px">Pixel 9</div>'
             '<div style="margin-top:14px;font-size:18px;line-height:1.7">⏻ <b>Turned off</b> · seen 12 min ago<br>'
             f'<span style="color:{BLU};font-weight:700">📶 Found by the Find Hub network</span></div>'
             f'<div data-in="15.4" style="position:absolute;right:20px;top:34px;background:#e7f6ee;color:#137a43;border-radius:12px;'
             'padding:3px 10px;font-size:14px;font-weight:800">🔒 Encrypted report</div>'
             '<div style="display:flex;gap:10px;margin-top:18px">'
             f'<div style="flex:1;height:52px;border-radius:26px;background:{BLU};color:#fff;display:grid;place-items:center;'
             'font-size:18px;font-weight:700">➤ Directions</div><div style="flex:1;height:52px;border-radius:26px;background:#eef2f7;'
             'color:#8a8f99;display:grid;place-items:center;font-size:18px;font-weight:700">🔔 Play sound</div></div></div></div>')


def radio(top, win=None):
    if win is None:
        return (f'<div style="position:absolute;left:30px;top:{top}px;width:28px;height:28px;border-radius:50%;background:#fff;'
                'border:2px solid #8a8f99"></div>')
    return (f'<div data-in="{win}" style="position:absolute;left:30px;top:{top}px;width:28px;height:28px;border-radius:50%;'
            f'background:#fff;border:2px solid {BLU}"><i style="position:absolute;left:5px;top:5px;width:14px;height:14px;'
            f'border-radius:50%;background:{BLU}"></i></div>')


OPTS = [('off', 'Off'), ('busy', 'With network in high-traffic areas only'), ('all', 'With network in all areas')]
OFFLINE = (SB + '<div class="nav"></div><div class="big" style="padding-bottom:18px">Find your offline devices</div>'
           '<div style="padding:0 30px 14px;font-size:15px;color:#5a6b8c;line-height:1.45">Nearby Android devices help locate your '
           'devices when they\'re offline. Locations are encrypted.</div>'
           '<div style="position:relative;margin:0 12px;background:#fff;border-radius:26px;height:236px">'
           + ''.join(f'<div data-id="{i}" style="position:absolute;left:0;right:0;top:{8 + k * 74}px;height:70px;display:flex;'
                     f'align-items:center;padding:0 18px 0 74px;font-size:19px;line-height:1.25">{lab}</div>' for k, (i, lab) in enumerate(OPTS))
           + radio(28) + radio(102) + radio(176) + radio(28, f'-1,{T_ALL:.2f}') + radio(176, f'{T_ALL:.2f}') + '</div>'
           f'<div data-in="{T_ALL + .2:.2f}" style="margin:16px 12px 0;background:#e7f6ee;color:#137a43;border-radius:20px;padding:12px 18px;'
           'font-size:17px;font-weight:700">✓ Offline finding is on</div>')


# ---------- chalk illustrations on the left (overlay, video seconds) ----------
def phone_icon(x, y, scale=1.0, off=False, win='-1'):
    w, h = 64 * scale, 116 * scale
    return (f'<div data-in="{win}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w:.0f}px;height:{h:.0f}px;'
            f'border-radius:{12 * scale:.0f}px;background:#0b0f1a;border:3px solid {"#8a93b0" if off else "#dfe6f5"};'
            'box-shadow:0 10px 20px rgba(0,0,0,.35)">'
            f'<div style="position:absolute;inset:{6 * scale:.0f}px;border-radius:{8 * scale:.0f}px;'
            f'background:{"#1b1f2a" if off else "linear-gradient(160deg,#3a6bd8,#7a4fd6)"};display:grid;place-items:center;'
            f'font-size:{30 * scale:.0f}px;color:#8a93b0">{"⏻" if off else ""}</div></div>')


LX, LY = 300, 590                            # the lost phone
HELP = [(110, 360), (470, 330), (500, 760)]
PULSES = ';'.join(f'{5.4 + i * .8:.2f},{6.6 + i * .8:.2f}' for i in range(16))
RINGS = ''.join(f'<div data-ring="{";".join(f"{5.4 + i * .8 + d:.2f},{6.6 + i * .8 + d:.2f}" for i in range(16))}" '
                f'style="position:absolute;left:{LX - 150}px;top:{LY - 150}px;width:300px;height:300px;border-radius:50%;'
                f'border:4px solid {CY};transform:scale(calc(.25 + var(--p,0) * .9));opacity:calc(1 - var(--p,0))"></div>' for d in (0, .4))


def report(hx, hy, t0):
    """Dot travelling from a helper phone up to the cloud (encrypted report)."""
    keys = ';'.join(f'{t0 + i * 1.2:.2f},{hx},{hy};{t0 + i * 1.2 + .9:.2f},300,250' for i in range(4))
    return (f'<div data-keys="{keys}" data-ease="linear" style="position:absolute;left:0;top:0;width:16px;height:16px;margin:-8px 0 0 -8px;'
            f'border-radius:50%;background:{GRN};box-shadow:0 0 12px {GRN}"></div>')


NETWORK = (f'<div data-in="5.3,18.9" style="position:absolute;inset:0">'
           + RINGS + phone_icon(LX, LY, 1.2, off=True)
           + f'<div style="position:absolute;left:{LX - 110}px;top:{LY + 82}px;width:220px;text-align:center;font-size:22px;font-weight:800">'
             '⏻ Lost phone · OFF</div>'
           + ''.join(phone_icon(x, y, .8, win=f'{6.6 + k * .5:.2f}') for k, (x, y) in enumerate(HELP))
           + '</div>'
           + f'<div data-in="12.5,18.9" style="position:absolute;inset:0">'
           + '<div style="position:absolute;left:220px;top:200px;width:160px;height:96px;border-radius:48px;background:rgba(6,20,52,.9);'
             f'border:3px solid {GRN};display:grid;place-items:center;font-size:24px;font-weight:800">☁️ 🔒</div>'
           + ''.join(report(x, y, 12.7 + k * .35) for k, (x, y) in enumerate(HELP))
           + '<div style="position:absolute;left:40px;top:860px;width:520px"></div></div>')


def card(win, top, html, border=YEL, width=520):
    return (f'<div data-in="{win}" style="position:absolute;left:40px;top:{top}px;width:{width}px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:16px 22px">{html}</div>')


OVERLAY = (
    card('-1,5.25', 260, f'<div style="font-size:52px;font-weight:900;color:{YEL};line-height:1.1">⏻ Phone OFF</div>'
                         '<div style="font-size:36px;font-weight:800;margin-top:8px">📍 still on the map</div>'
                         '<div style="font-size:24px;color:#cfe3ff;margin-top:8px">Supported phones only</div>')
    + NETWORK
    + card('19.0,27.5', 250, '<div style="font-size:30px;font-weight:800;color:#cfe3ff">🔋 Switched off?</div>'
                             f'<div style="font-size:44px;font-weight:900;color:{YEL};line-height:1.15">Pixel 8, 9 & 10</div>'
                             '<div style="font-size:30px;font-weight:800;line-height:1.3">findable for several hours</div>')
    + card('25.3,27.5', 520, '<div style="font-size:36px;font-weight:900">⚠️ Not every Android<br>supports this</div>', RED)
    + card('27.6', 250, '<div style="font-size:28px;font-weight:800;color:#cfe3ff">Turn it on now:</div>'
                        '<div style="font-size:30px;font-weight:800;line-height:1.45">Settings › Google ›<br>All services › Find Hub ›<br>'
                        f'<span style="color:{YEL}">Find your offline devices</span></div>', GRN))

SPEC = {
    'audio': 'host/voices/findhub.flac', 'lang': 'en', 'device': 'galaxy', 'overlay': OVERLAY,
    'title': 'Find your phone even when it\'s off 📍', 'tag': 'ANDROID · FIND HUB', 'tip': 'TIP #12',
    'start': 'map',
    'screens': {
        'map': {'type': 'html', 'bg': '#eef2f7', 'html': FINDMAP},
        'offline': {'type': 'html', 'bg': '#f4f4f6', 'html': OFFLINE},
    },
    'beats': [
        {'t': [0.0, 5.15], 'say': 'What if I told you Google could help find your Android phone even after you switch it off?',
         'cap': "FIND YOUR ANDROID EVEN WHEN IT'S OFF 📍", 'capsize': 82, 'pose': 'point', 'hook': True},
        {'t': [5.35, 12.40], 'say': "Google's Find Hub network can use nearby Android devices to detect your lost phone's Bluetooth signal and help locate it.",
         'cap': 'Find Hub: nearby Android phones pick up its Bluetooth signal', 'pose': 'talk'},
        {'t': [12.60, 18.58], 'say': "Nearby phones securely report its location, helping you find your device even when it can't connect to the internet itself.",
         'cap': 'They report its location securely, even with no internet 🔒', 'pose': 'welcome'},
        {'t': [19.01, 27.42], 'say': 'Some supported phones, including certain Pixel models, can remain findable for several hours after shutdown. But not every Android supports this!',
         'cap': 'Pixel 8, 9 & 10: findable for hours after shutdown (not every Android)', 'pose': 'talk'},
        {'t': [27.62, 31.04], 'say': 'Enable offline finding before you lose your phone.',
         'cap': 'Turn on "Find your offline devices" now ✅', 'pose': 'point',
         'do': [{'nav': 'offline', 'style': 'fade', 'at': 0}, {'tap': 'all', 'at': .62, 'fx': .5}]},
        {'t': [31.24, 33.30], 'say': 'Follow Tech Wall for daily tech secrets!', 'cap': 'Follow Tech Wall for daily tech secrets! 🚀',
         'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

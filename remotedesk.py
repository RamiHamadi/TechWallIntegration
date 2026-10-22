"""Tech Wall HOST episode with a supplied voice-over: control your computer from your phone (Chrome Remote Desktop).
    ./build.sh remotedesk  |  python3 remotedesk.py 0 150 400
Both rigs on stage together ('together' + 'rig_pos'): laptop left, Samsung Galaxy right, a live connection arc between
them ('overlay'). The phone shows a mirror of the PC desktop; every window opens on both at the same moment (data-in).
Voice: the user's generated audio (host/voices/remotedesk.flac); beat 't' = [start, end] s in it.
Facts (Google help + guides, 2026): on the computer open remotedesktop.google.com/access > Set up remote access >
install the host > name the computer > PIN (6+ digits); on the phone open the Chrome Remote Desktop app (Android / iOS),
same Google account, pick the computer, enter the PIN. Free; Windows, Mac, Linux hosts; the computer must be on and
online; Macs also need Screen Recording + Accessibility permissions. Generic look-alikes, no logos, fictional data."""
import math
import host

EP = 'remotedesk'
CY, GRN, YEL, VIO = '#5ce1ff', '#34d399', '#ffd54a', '#8b7cff'
T_NOTES1, T_FILES, T_NOTES2 = 1.9, 17.55, 16.55        # windows open (video s): hook demo, then "open apps, access files"
LIVE1, LIVE2 = '-1,5.75', '15.0'                       # remote session visible (hook) and after connecting


def win(show, x, y, w, h, title, body, col='#fff'):
    return (f'<div data-in="{show}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{col};'
            'border-radius:10px;box-shadow:0 16px 40px rgba(0,0,0,.4);overflow:hidden;color:#111;font-family:Poppins">'
            f'<div style="height:34px;background:#eef1f7;display:flex;align-items:center;justify-content:space-between;padding:0 12px;'
            f'font-size:14px;font-weight:700">{title}<span style="letter-spacing:6px;color:#666;font-weight:400">— ☐ ✕</span></div>{body}</div>')


NOTES_BODY = ('<div style="padding:14px 18px;font-size:20px;line-height:1.5">Meeting notes ✍️<br>• Send report to Sam<br>'
              '• Book flights ✈️</div>')
PHOTOS_BODY = ('<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:12px">'
               + ''.join(f'<div style="height:78px;border-radius:8px;background:linear-gradient(135deg,{a},{b})"></div>' for a, b in
                         [('#ffb36b', '#ff6f61'), ('#7fd1ff', '#3a7bd5'), ('#9be15d', '#00b09b'), ('#f6d365', '#fda085'),
                          ('#a18cd1', '#fbc2eb'), ('#84fab0', '#8fd3f4'), ('#fccb90', '#d57eeb'), ('#5ee7df', '#b490ca')])
               + '</div>')
FILES_BODY = ('<div style="display:flex;height:100%"><div style="width:120px;background:#f5f7fb;padding:10px;font-size:14px;line-height:2">'
              '⭐ Quick access<br>📁 Documents<br>🖼️ Pictures<br>⬇️ Downloads</div><div style="flex:1;padding:12px;display:grid;'
              'grid-template-columns:repeat(3,1fr);gap:10px;font-size:13px;text-align:center">'
              + ''.join(f'<div><div style="font-size:40px">{i}</div>{n}</div>' for i, n in
                        [('📁', 'Work'), ('📁', 'Photos'), ('📄', 'Report.pdf'), ('📊', 'Budget.xlsx'), ('🎵', 'Podcast.mp3'), ('📄', 'Notes.txt')])
              + '</div></div>')


def desktop(prefix):
    """The PC desktop (920x518). prefix 'm_' = the phone's mirror copy (its icons are the phone's tap targets)."""
    icons = [('notes', '📝', 'Notes', '#ffd54a'), ('files', '📁', 'Files', '#5ac8fa'), ('web', '🌐', 'Browser', '#34c759'),
             ('photos', '🖼️', 'Photos', '#ff7a45')]
    ic = ''.join(f'<div data-id="{prefix}{i}" style="position:absolute;left:22px;top:{22 + k * 96}px;width:84px;text-align:center;'
                 f'color:#fff;font-size:14px;font-weight:600"><div style="width:58px;height:58px;margin:0 auto 4px;border-radius:14px;'
                 f'background:{c};display:grid;place-items:center;font-size:32px">{e}</div>{n}</div>'
                 for k, (i, e, n, c) in enumerate(icons))
    return ('<div style="position:absolute;left:0;top:0;width:920px;height:518px;overflow:hidden;'
            'background:linear-gradient(135deg,#1b3b8a 0%,#3f6fd8 55%,#9cc0ff 100%)">' + ic
            + win('-1,5.75', 330, 150, 440, 240, 'Photos', PHOTOS_BODY)
            + win(f'{T_NOTES1},{5.75}', 200, 56, 470, 250, 'Notes', NOTES_BODY)
            + win(f'{T_NOTES2}', 200, 50, 470, 250, 'Notes', NOTES_BODY)
            + win(f'{T_FILES}', 300, 110, 560, 320, 'Files', FILES_BODY)
            + '<div style="position:absolute;left:0;right:0;bottom:0;height:46px;background:rgba(240,243,250,.92);display:flex;'
              'align-items:center;justify-content:center;gap:16px"><span style="width:26px;height:26px;border-radius:50%;'
              'background:radial-gradient(circle at 35% 35%,#7fb3ff,#2a62d6)"></span><span style="background:#fff;border-radius:16px;'
              'padding:4px 40px 4px 14px;color:#888;font-size:15px">⌕ Search</span><span style="position:absolute;right:16px;'
              'font-size:14px;color:#333">10:08</span></div></div>')


BANNER = (f'<div data-in="{{w}}" style="position:absolute;left:300px;top:10px;background:rgba(6,20,52,.9);color:#fff;'
          f'border:2px solid {GRN};border-radius:16px;padding:5px 14px;font-size:15px;font-weight:700;z-index:9">'
          '🔗 Remote session · connected from phone</div>')
DESK = desktop('d_') + BANNER.replace('{w}', LIVE1) + BANNER.replace('{w}', LIVE2)

CRDWEB = ('<div style="position:absolute;inset:0;background:#f6f8fc;font-family:Poppins;color:#111">'
          '<div style="height:70px;background:#e9ecf2;position:relative"><div style="position:absolute;left:14px;right:14px;top:34px;height:28px;'
          'border-radius:14px;background:#fff;font-size:15px;padding:4px 16px;color:#333">🔒 remotedesktop.google.com/access</div></div>'
          '<div style="padding:18px 34px"><div style="font-size:30px;font-weight:800">Remote Desktop</div>'
          '<div style="display:flex;gap:10px;margin-top:8px">'
          + ''.join(f'<span style="background:#e7f6ee;color:#137a43;border-radius:12px;padding:3px 12px;font-size:15px;font-weight:700">{c}</span>'
                    for c in ('Free', 'Windows', 'Mac', 'Linux'))
          + '</div><div style="margin-top:18px;background:#fff;border-radius:18px;box-shadow:0 6px 20px rgba(0,0,0,.08);padding:18px 22px;'
            'display:flex;align-items:center;justify-content:space-between"><div><div style="font-size:22px;font-weight:800">'
            'Set up remote access</div><div style="font-size:15px;color:#666">Install the host on this computer</div></div>'
            '<div data-id="install" style="background:#1a73e8;color:#fff;border-radius:20px;padding:10px 26px;font-weight:700;'
            'font-size:18px">Install</div></div>'
            '<div data-in="11.65" style="margin-top:14px;background:#fff;border-radius:18px;box-shadow:0 6px 20px rgba(0,0,0,.08);'
            'padding:14px 22px;font-size:18px"><b>Name:</b> Home-PC &nbsp;·&nbsp; <b>PIN:</b> <span style="letter-spacing:6px">••••••</span>'
            ' <span style="color:#137a43;font-weight:800">✓ Ready</span></div></div></div>')

MIRROR = ('<div class="sb" style="color:#fff"><span>10:08</span><span class="bat"></span></div>'
          '<div style="position:absolute;left:0;right:0;top:62px;height:56px;display:flex;align-items:center;justify-content:space-between;'
          'padding:0 18px;color:#fff;font-size:19px;font-weight:700">Home-PC<span style="font-size:15px;color:#34d399">● Connected</span></div>'
          '<div style="position:absolute;left:0;top:130px;width:920px;height:518px;transform:scale(0.4391);transform-origin:0 0">'
          + desktop('m_') + '</div>'
          '<div style="position:absolute;left:20px;right:20px;top:380px;text-align:center;color:#aab3c8;font-size:16px;line-height:1.5">'
          'Tap to click · drag to move<br>pinch to zoom</div>'
          '<div style="position:absolute;left:28px;right:28px;top:470px;border-radius:20px;background:rgba(255,255,255,.07);'
          'border:1px solid rgba(255,255,255,.14);padding:16px 20px;color:#dfe6f5;font-size:18px;line-height:1.75">'
          '🔒 Encrypted session<br>💻 Home-PC · Windows<br>🌍 Works from almost anywhere</div>'
          '<div style="position:absolute;left:50%;bottom:60px;margin-left:-110px;width:220px;height:56px;border-radius:28px;'
          'background:rgba(255,255,255,.12);display:flex;justify-content:space-around;align-items:center;font-size:24px">⌨️ 🖱️ ⋮</div>')

PAPP = ('<div class="sb"><span>10:08</span><span class="bat"></span></div>'
        '<div style="padding:40px 26px 0;font-size:34px;font-weight:700">Remote Desktop</div>'
        '<div style="padding:8px 26px 14px;font-size:16px;color:#3e91ff;font-weight:600">My computers</div>'
        '<div data-id="pc" style="margin:0 14px;background:#fff;border-radius:24px;height:96px;display:flex;align-items:center;gap:16px;'
        'padding:0 20px"><div style="font-size:42px">💻</div><div><div style="font-size:21px;font-weight:700">Home-PC</div>'
        '<div style="font-size:15px;color:#8a8f99">Offline · not set up</div></div></div>'
        '<div data-in="12.0" style="position:absolute;left:14px;right:14px;top:209px;height:96px;background:#fff;border-radius:24px;'
        'display:flex;align-items:center;gap:16px;padding:0 20px"><div style="font-size:42px">💻</div><div><div style="font-size:21px;'
        'font-weight:700">Home-PC</div><div style="font-size:15px;color:#137a43;font-weight:700">● Online</div></div></div>')
PPIN = ('<div class="sb"><span>10:08</span><span class="bat"></span></div>'
        '<div style="padding:60px 26px 0;font-size:30px;font-weight:700;text-align:center">Home-PC</div>'
        '<div style="text-align:center;font-size:17px;color:#666;margin-top:6px">Enter your PIN</div>'
        '<div style="margin:30px 60px 0;border-bottom:3px solid #3e91ff;height:56px;font-size:36px;letter-spacing:10px;text-align:center">'
        '<span data-type="ppin:pin"></span></div>'
        '<div data-id="connect" style="position:absolute;left:40px;right:40px;top:330px;height:58px;border-radius:29px;background:#3e91ff;'
        'color:#fff;font-weight:700;font-size:20px;display:grid;place-items:center">Connect</div>')


ARC = ((928, 492), (905, 290), (792, 330))           # connection arc: phone top -> laptop screen edge (quadratic)


def arc_keys(t0, t1, period=1.1):
    """Dense keys for a dot travelling the connection arc (phone -> laptop), repeating every `period` s."""
    (ax, ay), (bx, by), (cx, cy) = ARC
    out, t = [], t0
    while t < t1:
        for k in range(9):
            u = k / 8; x = (1 - u) ** 2 * ax + 2 * u * (1 - u) * bx + u * u * cx; y = (1 - u) ** 2 * ay + 2 * u * (1 - u) * by + u * u * cy
            out.append(f'{t + period * u:.3f},{x:.1f},{y:.1f}')
        t += period
    return ';'.join(out)


def link(win):
    dots = (f'<div data-keys="{arc_keys(-1 if win.startswith("-") else float(win.split(",")[0]), 40)}" data-ease="linear" '
            f'style="position:absolute;left:0;top:0;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:{CY};'
            'box-shadow:0 0 12px #5ce1ff"></div>')
    (ax, ay), (bx, by), (cx, cy) = ARC
    return (f'<div data-in="{win}" style="position:absolute;inset:0">'
            f'<svg width="1080" height="1920" style="position:absolute;left:0;top:0"><path d="M{ax} {ay} Q{bx} {by} {cx} {cy}" fill="none" '
            f'stroke="{CY}" stroke-width="4" stroke-dasharray="10 10" opacity=".85"/></svg>{dots}'
            f'<div style="position:absolute;left:840px;top:228px;background:rgba(6,20,52,.9);border:2px solid {CY};border-radius:14px;'
            'padding:4px 12px;font-size:15px;font-weight:800">🔒 Remote link</div></div>')


OVERLAY = link(LIVE1) + link(LIVE2)

SPEC = {
    'audio': 'host/voices/remotedesk.flac', 'lang': 'en', 'devices': ['laptop', 'galaxy'], 'together': True,
    'rig_pos': {'laptop': {'left': 22, 'top': 205, 'scale': 0.8}, 'galaxy': {'left': 786, 'top': 500, 'scale': 0.66}},
    'overlay': OVERLAY,
    'title': 'Your phone can control your PC 💻📱', 'tag': 'CHROME REMOTE DESKTOP', 'tip': 'TIP #08',
    'start': 'desk',
    'screens': {
        'desk': {'dev': 'laptop', 'type': 'html', 'bg': '#1b3b8a', 'html': DESK},
        'crdweb': {'dev': 'laptop', 'type': 'html', 'bg': '#f6f8fc', 'html': CRDWEB},
        'mirror': {'dev': 'galaxy', 'type': 'html', 'bg': '#0b0d14', 'html': MIRROR},
        'papp': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': PAPP},
        'ppin': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': PPIN},
    },
    'beats': [
        {'t': [0.22, 5.13], 'say': "You can control your entire computer from your phone, even when you're miles away!",
         'cap': 'YOUR PHONE CAN CONTROL YOUR PC 💻📱', 'pose': 'welcome', 'hook': True,
         'do': [{'nav': 'mirror', 'style': 'none', 'at': 0}, {'tap': 'm_notes', 'at': .28}]},
        {'t': [5.81, 10.31], 'say': "Meet Chrome Remote Desktop. It's free and works with PCs and Macs.",
         'cap': 'Chrome Remote Desktop: free, for PCs and Macs', 'pose': 'talk',
         'do': [{'nav': 'crdweb', 'style': 'fade', 'at': .0}, {'nav': 'papp', 'style': 'fade', 'at': .02}]},
        {'t': [11.02, 12.24], 'say': 'Set it up on your computer,',
         'cap': 'Step 1: On the computer, set up remote access (install + PIN)', 'pose': 'point', 'step': 1,
         'do': [{'nav': 'crdweb', 'style': 'none', 'at': 0}, {'tap': 'install', 'at': .3}]},
        {'t': [12.48, 15.65], 'say': 'connect from your phone, and control your desktop remotely.',
         'cap': 'Step 2: Open the app on your phone, pick your PC, enter the PIN', 'pose': 'point', 'step': 2,
         'do': [{'nav': 'papp', 'style': 'none', 'at': 0}, {'tap': 'pc', 'at': .12, 'nav': 'ppin', 'fx': .5},
                {'typetext': '••••••', 'into': 'pin', 'from': .32, 'to': .5}, {'tap': 'connect', 'at': .6, 'nav': 'mirror', 'style': 'fade', 'fx': .5},
                {'nav': 'desk', 'style': 'fade', 'at': .7}]},
        {'t': [16.13, 19.66], 'say': 'Open apps, access files, and work from almost anywhere!',
         'cap': 'Open apps, access files, work from almost anywhere ✨', 'pose': 'welcome',
         'do': [{'nav': 'mirror', 'style': 'none', 'at': 0}, {'tap': 'm_notes', 'at': .04}, {'tap': 'm_files', 'at': .32},
                {'fx': 'thumb', 'at': .6, 'dur': 2.2}]},
        {'t': [20.37, 22.14], 'say': 'Follow Tech Wall for more tech secrets.',
         'cap': 'Follow Tech Wall for more tech secrets! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

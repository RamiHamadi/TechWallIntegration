"""Tech Wall HOST episode (laptop) with a supplied voice-over: reveal a saved Wi-Fi password with one CMD command.
    ./build.sh wifipass  |  python3 wifipass.py 0 150 400
Voice: the user's generated audio, pauses between phrases shortened to 0.2 s (host/voices/wifipass.flac).
Facts (Microsoft netsh docs + 2026 guides): WIN + R > cmd; CTRL + SHIFT + ENTER opens it as administrator (key=clear
often shows no "Key Content" in a normal prompt); netsh wlan show profile name="<Wi-Fi name>" key=clear >
Security settings > Key Content = the password; netsh wlan show profiles lists the saved names.
Generic look-alikes, no logos; fictional network "Home" / "SunnyDays2024"."""
import host

EP = 'wifipass'
YEL, CY, GRN = '#ffd54a', '#5ce1ff', '#34d399'
T_RUN = 4.84 + .2 * 3.13 + .25            # Run dialog opens (WIN + R pressed)
T_ADMIN = 4.84 + .86 * 3.13               # CTRL + SHIFT + ENTER
T_ENTER = 8.17 + .86 * 3.99               # Enter after the command
T_HL = 12.55                              # "Key Content" highlighted
CMD = 'netsh wlan show profile name="Home" key=clear'

TASKBAR = ('<div style="position:absolute;left:0;right:0;bottom:0;height:46px;background:rgba(240,243,250,.94);display:flex;'
           'align-items:center;justify-content:center;gap:16px;z-index:8"><span style="width:26px;height:26px;border-radius:6px;'
           'background:linear-gradient(135deg,#7fb3ff,#2a62d6)"></span><span style="background:#fff;border-radius:16px;'
           'padding:4px 40px 4px 14px;color:#888;font-size:15px;font-family:Poppins">⌕ Search</span>'
           '<span style="position:absolute;right:16px;font-size:14px;color:#333;font-family:Poppins">📶 10:08</span></div>')
WALL = 'position:absolute;inset:0;background:linear-gradient(135deg,#1b3b8a 0%,#3f6fd8 55%,#9cc0ff 100%)'
MONO = "font-family:'DejaVu Sans Mono',Consolas,monospace"

OUTPUT = ['', 'Profile Home on interface Wi-Fi:', '=' * 34, '', 'Security settings', '-' * 17,
          '    Authentication     : WPA2-Personal', '    Cipher             : CCMP',
          '    Security key       : Present', '    Key Content        : SunnyDays2024', '', r'C:\Windows\System32>']
LH, TOP = 22, 46                          # console line height / first line y inside the window


def console(static):
    """Administrator Command Prompt window (860x470 at 30,20). static=True: the finished result (frame 0)."""
    head = ['Microsoft Windows [Version 10.0.26100.2033]', '(c) Microsoft Corporation. All rights reserved.', '']
    typed = CMD if static else '<span data-type="cmd:line"></span><span style="background:#ccc;color:#ccc">_</span>'
    out_in = '' if static else f' data-in="{T_ENTER + .15:.2f}"'
    hl_in = '' if static else f' data-in="{T_HL:.2f}"'
    body = (''.join(f'<div style="height:{LH}px;white-space:pre">{h}</div>' for h in head)
            + f'<div style="height:{LH}px;white-space:pre">C:\\Windows\\System32&gt;{" " if static else ""}{typed}</div>'
            + f'<div{out_in} style="transform-origin:0 0">'
            + ''.join(f'<div style="height:{LH}px;white-space:pre{";color:#fff;font-weight:700" if "Key Content" in o else ""}">{o}</div>'
                      for o in OUTPUT) + '</div>')
    key_y = TOP + (len(head) + 1 + 9) * LH - 3
    hl = (f'<div{hl_in} style="position:absolute;left:12px;top:{key_y}px;width:430px;height:{LH + 6}px;border:3px solid {YEL};'
          'border-radius:8px;box-shadow:0 0 0 4px rgba(255,213,74,.25),0 0 22px rgba(255,213,74,.6)"></div>')
    win = (f'<div style="position:absolute;left:30px;top:20px;width:860px;height:440px;background:#0c0c0c;border-radius:10px;'
           'overflow:hidden;box-shadow:0 18px 40px rgba(0,0,0,.45)">'
           '<div style="height:34px;background:#1f1f1f;color:#ddd;display:flex;align-items:center;justify-content:space-between;'
           'padding:0 14px;font-size:14px;font-family:Poppins"><span>▣&nbsp; Administrator: Command Prompt</span>'
           '<span style="letter-spacing:8px">— ☐ ✕</span></div>'
           f'<div style="position:absolute;left:18px;top:{TOP - 34 + 34}px;right:10px;color:#cccccc;font-size:16px;{MONO}">'
           + body + '</div>' + hl + '</div>')
    if static:
        return f'<div style="{WALL}"></div>' + win + TASKBAR
    # zoom: on the command while it is typed, out for the output, then onto "Key Content"
    zoom = (f'{8.4:.2f},0,0,0,1;{8.9:.2f},-34,14,0,1.3;{T_ENTER - .05:.2f},-34,14,0,1.3;{T_ENTER + .35:.2f},0,0,0,1;'
            f'{T_HL - .1:.2f},0,0,0,1;{T_HL + .5:.2f},32,-357,0,1.7;15.5,32,-357,0,1.7;16.0,0,0,0,1')
    return (f'<div style="{WALL}"></div><div data-keys="{zoom}" style="position:absolute;left:0;top:0;width:920px;height:518px;'
            f'transform-origin:0 0">{win}</div>' + TASKBAR)


RUN = (f'<div data-in="{T_RUN:.2f}" style="position:absolute;left:24px;top:248px;width:470px;height:212px;background:#f3f3f3;'
       'border-radius:10px;box-shadow:0 18px 40px rgba(0,0,0,.45);font-family:Poppins;color:#111;overflow:hidden;z-index:9">'
       '<div style="height:32px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;font-size:14px">'
       '<span>▭ Run</span><span>✕</span></div>'
       '<div style="display:flex;gap:12px;padding:6px 18px 0;font-size:13px;line-height:1.4"><span style="font-size:30px">🏃</span>'
       'Type the name of a program, folder, document, or Internet resource, and Windows will open it for you.</div>'
       '<div style="display:flex;align-items:center;gap:10px;padding:12px 18px 0;font-size:15px">Open:'
       '<div style="flex:1;height:30px;border:2px solid #2a62d6;border-radius:4px;background:#fff;padding:2px 8px;font-size:17px">'
       '<span data-type="desk:run"></span></div></div>'
       '<div style="display:flex;justify-content:flex-end;gap:10px;padding:16px 18px 0">'
       + ''.join(f'<span style="width:82px;height:30px;border-radius:5px;background:{"#2a62d6" if b == "OK" else "#fff"};'
                 f'color:{"#fff" if b == "OK" else "#111"};border:1px solid #bbb;display:grid;place-items:center;font-size:14px">{b}</span>'
                 for b in ('OK', 'Cancel', 'Browse…'))
       + '</div></div>'
       f'<div data-in="{T_ADMIN - .45:.2f},{T_ADMIN + .5:.2f}" style="position:absolute;left:510px;top:330px;width:380px;background:{YEL};'
       'color:#111;border-radius:14px;padding:10px 14px;font-family:Poppins;font-size:17px;font-weight:800;z-index:9">'
       'CTRL + SHIFT + ENTER<br><span style="font-weight:600;font-size:15px">= open it as administrator</span></div>')

UAC = (f'<div data-in="{T_ADMIN + .3:.2f}" style="position:absolute;inset:0;background:rgba(0,0,0,.55);z-index:10">'
       '<div style="position:absolute;left:230px;top:70px;width:460px;background:#fff;border-radius:12px;overflow:hidden;'
       'font-family:Poppins;color:#111;box-shadow:0 18px 50px rgba(0,0,0,.5)">'
       '<div style="padding:16px 22px 8px;font-size:14px;color:#555">User Account Control</div>'
       '<div style="padding:0 22px;font-size:20px;font-weight:700;line-height:1.3">Do you want to allow this app to make changes to '
       'your device?</div><div style="padding:14px 22px;font-size:16px">▣ Windows Command Processor</div>'
       '<div style="display:flex;gap:12px;padding:10px 22px 18px;background:#f3f3f3">'
       '<div data-id="yes" style="flex:1;height:38px;border-radius:6px;background:#2a62d6;color:#fff;display:grid;place-items:center;'
       'font-weight:700">Yes</div><div style="flex:1;height:38px;border-radius:6px;background:#fff;border:1px solid #bbb;'
       'display:grid;place-items:center">No</div></div></div></div>')

DESK = (f'<div style="{WALL}"></div>'
        + ''.join(f'<div style="position:absolute;left:22px;top:{22 + k * 96}px;width:84px;text-align:center;color:#fff;'
                  f'font-size:14px;font-weight:600;font-family:Poppins"><div style="width:58px;height:58px;margin:0 auto 4px;'
                  f'border-radius:14px;background:{c};display:grid;place-items:center;font-size:32px">{e}</div>{n}</div>'
                  for k, (e, n, c) in enumerate([('🗑️', 'Recycle Bin', '#8e9bb3'), ('📁', 'Files', '#5ac8fa'),
                                                 ('🌐', 'Browser', '#34c759')]))
        + RUN + UAC + TASKBAR)


def card(win, top, html, border=YEL):
    return (f'<div data-in="{win}" style="position:absolute;left:560px;top:{top}px;width:480px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:14px 22px;color:#fff;'
            f'font-family:Poppins">{html}</div>')


PASS = ('<div style="font-size:24px;font-weight:700;color:#aab8d8">🔓 Key Content</div>'
        f'<div style="font-size:44px;font-weight:900;color:{YEL};letter-spacing:.5px">SunnyDays2024</div>')
OVERLAY = (card('-1,4.7', 840, PASS)
           + card('9.4,12.3', 840, '<div style="font-size:27px;font-weight:800;line-height:1.35">✏️ Replace <span style="color:'
                                    f'{YEL}">Home</span><br>with YOUR Wi-Fi name</div>', CY)
           + card(f'{T_HL + .3:.2f}', 840, PASS)
           + card('15.7', 1030, '<div style="font-size:52px;font-weight:900;text-align:center">🔖 SAVE THIS</div>'))

SPEC = {
    'audio': 'host/voices/wifipass.flac', 'lang': 'en', 'device': 'laptop', 'overlay': OVERLAY,
    'title': 'Reveal a saved Wi-Fi password 🔓', 'tag': 'WINDOWS · CMD · NETSH', 'tip': 'TIP #10',
    'start': 'cmdres',
    'screens': {
        'cmdres': {'type': 'html', 'bg': '#1b3b8a', 'html': console(True)},
        'desk': {'type': 'html', 'bg': '#1b3b8a', 'html': DESK},
        'cmd': {'type': 'html', 'bg': '#1b3b8a', 'html': console(False)},
    },
    'beats': [
        {'t': [0.0, 4.64], 'say': 'Forgot your Wi-Fi password? Windows has a secret command that can reveal it!',
         'cap': 'FIND YOUR SAVED WI-FI PASSWORD 🔓', 'capsize': 84, 'pose': 'point', 'hook': True},
        {'t': [4.84, 7.97], 'say': 'Press Windows plus R, type CMD, and hit Enter.',
         'cap': 'Step 1: WIN + R, type cmd, then CTRL + SHIFT + ENTER (admin)', 'pose': 'point', 'step': 1,
         'do': [{'nav': 'desk', 'style': 'fade', 'at': 0}, {'keys': ['WIN', 'R'], 'at': .2, 'hold': 1.0},
                {'typetext': 'cmd', 'into': 'run', 'from': .5, 'to': .62},
                {'keys': ['CTRL', 'SHIFT', 'ENTER'], 'at': .86, 'hold': 1.1}]},
        {'t': [8.17, 12.16], 'say': 'Now type this command, replacing YourWiFi with your network name.',
         'cap': 'Step 2: Type this command with YOUR Wi-Fi name, press Enter', 'pose': 'talk', 'step': 2,
         'do': [{'tap': 'yes', 'at': .02, 'nav': 'cmd', 'style': 'fade'},
                {'typetext': CMD, 'into': 'line', 'from': .12, 'to': .78}, {'keys': ['ENTER'], 'at': .86, 'hold': .9}]},
        {'t': [12.36, 15.64], 'say': "Look for Key Content. There's your saved Wi-Fi password!",
         'cap': 'Step 3: “Key Content” = your saved password 🔓', 'pose': 'point', 'step': 3,
         'do': [{'fx': 'confetti', 'at': .6}]},
        {'t': [15.84, 16.58], 'say': 'Save this trick,', 'cap': 'Save this trick 🔖', 'pose': 'welcome'},
        {'t': [16.62, 18.98], 'say': 'and follow Tech Wall for more Windows secrets!',
         'cap': 'Follow Tech Wall for more Windows secrets! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

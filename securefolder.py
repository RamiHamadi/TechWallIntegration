"""Tech Wall HOST episode with a supplied voice-over: hide private photos and apps in Samsung Secure Folder.
    ./build.sh securefolder  |  python3 securefolder.py 0 150 400
Samsung Galaxy (One UI look-alike). Voice: the user's generated audio, pauses between phrases shortened to 0.2 s
(host/voices/securefolder.flac).
Facts (Samsung support + 2026 guides): Settings > search "Secure Folder" (or Security and privacy > More security
settings > Secure Folder) > Continue (Samsung account sign-in may be asked) > lock type Pattern / PIN / Password, plus
fingerprints or face if supported; then Gallery > select > Move to Secure Folder, or Secure Folder > Add apps / Add files.
The Secure Folder has its own lock, separate from the phone's. Generic look-alikes, no logos, fictional data."""
import host

EP = 'securefolder'
GAL = {'dev': 'galaxy'}
CY, YEL, BLU, GRN = '#5ce1ff', '#ffd54a', '#3e91ff', '#34d399'
SB = '<div class="sb"><span>10:08</span><span class="bat"></span></div>'
SBW = '<div class="sb" style="color:#fff"><span>10:08</span><span class="bat"></span></div>'
PHOTOS = [('#ffb36b', '#ff6f61'), ('#7fd1ff', '#3a7bd5'), ('#9be15d', '#00b09b'), ('#f6d365', '#fda085'),
          ('#a18cd1', '#fbc2eb'), ('#84fab0', '#8fd3f4'), ('#fccb90', '#d57eeb'), ('#5ee7df', '#b490ca'), ('#ff9a9e', '#fad0c4')]


def thumbs(n, size=118, gap=8, sel=None):
    out = ''
    for i in range(n):
        a, b = PHOTOS[i % len(PHOTOS)]
        tick = (f'<div style="position:absolute;right:6px;top:6px;width:24px;height:24px;border-radius:50%;background:{BLU};'
                'color:#fff;font-size:15px;display:grid;place-items:center;border:2px solid #fff">✓</div>') if sel and i in sel else ''
        out += (f'<div style="position:relative;width:{size}px;height:{size}px;border-radius:12px;'
                f'background:linear-gradient(135deg,{a},{b})">{tick}</div>')
    return f'<div style="display:grid;grid-template-columns:repeat(3,{size}px);gap:{gap}px;justify-content:center">{out}</div>'


APP_TILES = [('🗂️', 'My Files'), ('💬', 'Chat'), ('🏦', 'Bank'), ('📝', 'Notes')]
SF_HOME = (f'<div style="position:absolute;inset:0;background:linear-gradient(170deg,#0d2a6b,#1c4fb8 60%,#3a6bd8)"></div>' + SBW
           + '<div style="position:relative;padding:22px 24px 6px;color:#fff;display:flex;align-items:center;gap:10px">'
             '<span style="font-size:30px">🔒</span><span style="font-size:30px;font-weight:700">Secure Folder</span></div>'
           + '<div style="position:relative;padding:0 26px 16px;color:#cfe0ff;font-size:15px">Separate lock · hidden from your phone</div>'
           + '<div style="position:relative;margin:0 12px;background:rgba(255,255,255,.12);border-radius:24px;padding:14px 12px">'
             '<div style="color:#fff;font-size:17px;font-weight:700;margin:0 6px 10px">Private photos</div>' + thumbs(6, 112) + '</div>'
           + '<div style="position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:16px 12px 0;color:#fff;'
             'font-size:14px;text-align:center">'
           + ''.join(f'<div><div style="width:64px;height:64px;margin:0 auto 6px;border-radius:22px;background:rgba(255,255,255,.18);'
                     f'display:grid;place-items:center;font-size:32px">{e}</div>{n}</div>' for e, n in APP_TILES)
           + '</div><div style="position:relative;margin:18px 12px 0;height:54px;border-radius:27px;background:rgba(255,255,255,.16);'
             'color:#fff;display:grid;place-items:center;font-size:17px;font-weight:700">＋ Add apps · Add files</div>')

LOCK = (f'<div style="position:absolute;inset:0;background:linear-gradient(170deg,#0d2a6b,#1c4fb8 60%,#3a6bd8)"></div>' + SBW
        + '<div style="position:relative;text-align:center;color:#fff;padding-top:90px"><div style="font-size:64px">🔒</div>'
          '<div style="font-size:28px;font-weight:700;margin-top:10px">Secure Folder</div>'
          '<div style="font-size:17px;color:#cfe0ff;margin-top:6px">Enter your Secure Folder PIN</div>'
          '<div style="display:flex;justify-content:center;gap:14px;margin-top:26px">'
          + ''.join('<i style="width:16px;height:16px;border-radius:50%;border:2px solid #fff"></i>' for _ in range(6)) + '</div>'
          '<div style="margin:30px auto 0;width:300px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px;font-size:30px">'
          + ''.join(f'<div style="height:62px;display:grid;place-items:center">{d}</div>' for d in '123456789 0⌫') + '</div>'
          '<div style="font-size:15px;color:#cfe0ff;margin-top:6px">🔑 Separate from your phone\'s lock</div></div>')

GHOME_APPS = [{'id': 'gallery', 'label': 'Gallery', 'icon': 'photos', 'bg': 'linear-gradient(#ff8a65,#e8507a)'},
              {'id': 'camera', 'label': 'Camera', 'icon': 'camera', 'bg': 'linear-gradient(#ff6b6b,#d63a3a)'},
              {'id': 'settings', 'label': 'Settings', 'icon': 'gear', 'bg': 'linear-gradient(#8e8e93,#636366)'},
              {'id': 'msgs', 'label': 'Messages', 'icon': 'chat', 'bg': 'linear-gradient(#5ac8fa,#0a84ff)'},
              {'id': 'clock', 'label': 'Clock', 'icon': 'clock', 'bg': 'linear-gradient(#5c6cff,#3d4bd6)'},
              {'id': 'notes', 'label': 'Notes', 'icon': 'notes', 'bg': 'linear-gradient(#ffd54a,#ffb300)'},
              {'id': 'music', 'label': 'Music', 'icon': 'music', 'bg': 'linear-gradient(#ff6b81,#ff2d55)'},
              {'id': 'sf', 'label': 'Secure Folder', 'icon': 'lock', 'bg': 'linear-gradient(#3e91ff,#1c4fb8)'}]

SETTINGS = (SB + '<div style="display:flex;justify-content:flex-end;padding:6px 18px 0">'
            '<div data-id="search" style="width:48px;height:48px;border-radius:50%;display:grid;place-items:center;font-size:24px">🔍</div></div>'
            '<div class="big" style="padding-top:30px">Settings</div>'
            + ''.join(f'<div style="margin:0 12px 12px;background:#fff;border-radius:26px;padding:4px 0">'
                      + ''.join(f'<div style="height:62px;display:flex;align-items:center;gap:16px;padding:0 20px;font-size:19px">'
                                f'<span style="width:34px;height:34px;border-radius:50%;background:{c};display:grid;place-items:center;'
                                f'font-size:17px">{e}</span>{n}</div>' for e, n, c in grp) + '</div>'
                      for grp in [[('📶', 'Connections', '#3e91ff'), ('🔊', 'Sounds and vibration', '#a066ff'),
                                   ('🔔', 'Notifications', '#ff6b6b')],
                                  [('☀️', 'Display', '#3cb371'), ('🔋', 'Battery', '#3cb371'),
                                   ('🛡️', 'Security and privacy', '#4b7bec')]]))

SEARCH = (SB + '<div style="display:flex;align-items:center;gap:12px;margin:10px 14px 18px;height:56px;background:#fff;border-radius:28px;'
          'padding:0 18px;font-size:19px"><span>‹</span><span data-type="gsearch:q" style="flex:1"></span>'
          '<span style="color:#8a8f99">✕</span></div>'
          '<div data-in="12.4" style="margin:0 12px;background:#fff;border-radius:26px;padding:6px 0">'
          '<div data-id="res" style="padding:12px 20px"><div style="font-size:19px;font-weight:700"><span style="color:#3e91ff">Secure Folder</span></div>'
          '<div style="font-size:14px;color:#8a8f99">Security and privacy › More security settings</div></div>'
          '<div style="padding:12px 20px;font-size:17px;color:#5a6b8c">Secure Folder type</div></div>')

SETUP = (SB + '<div style="text-align:center;padding-top:70px"><div style="width:120px;height:120px;margin:0 auto;border-radius:36px;'
         'background:linear-gradient(#3e91ff,#1c4fb8);display:grid;place-items:center;font-size:62px">🔒</div>'
         '<div style="font-size:30px;font-weight:700;margin-top:20px">Secure Folder</div>'
         '<div style="font-size:16px;color:#5a6b8c;margin:10px 36px 0;line-height:1.5">Keep your private files and apps safe '
         'in a separate space, protected by its own lock.</div></div>'
         '<div data-id="cont" style="position:absolute;left:40px;right:40px;bottom:60px;height:58px;border-radius:29px;background:#3e91ff;'
         'color:#fff;font-weight:700;font-size:20px;display:grid;place-items:center">Continue</div>')


def radio(top, win=None):
    if win is None:
        return (f'<div style="position:absolute;left:28px;top:{top}px;width:28px;height:28px;border-radius:50%;background:#fff;'
                'border:2px solid #8a8f99"></div>')
    return (f'<div data-in="{win}" style="position:absolute;left:28px;top:{top}px;width:28px;height:28px;border-radius:50%;'
            f'background:#fff;border:2px solid {BLU}"><i style="position:absolute;left:5px;top:5px;width:14px;height:14px;'
            f'border-radius:50%;background:{BLU}"></i></div>')


T_PIN = 14.93 + .3 * 3.4
LOCKTYPE = (SB + '<div class="nav"></div><div class="big" style="padding-bottom:18px">Secure Folder lock type</div>'
            '<div style="position:relative;margin:0 12px;background:#fff;border-radius:26px;height:216px">'
            + ''.join(f'<div data-id="{i}" style="position:absolute;left:0;right:0;top:{8 + k * 68}px;height:64px;display:flex;'
                      f'align-items:center;padding-left:72px;font-size:20px">{lab}</div>'
                      for k, (i, lab) in enumerate([('pattern', 'Pattern'), ('pin', 'PIN'), ('pw', 'Password')]))
            + radio(26) + radio(94) + radio(162) + radio(94, f'{T_PIN + .1:.2f}') + '</div>'
            '<div style="margin:14px 12px 0;background:#fff;border-radius:26px;padding:4px 0">'
            '<div style="height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 20px;font-size:19px">'
            '👆 Fingerprints<span style="width:50px;height:28px;border-radius:14px;background:#3e91ff;position:relative">'
            '<i style="position:absolute;right:3px;top:3px;width:22px;height:22px;border-radius:50%;background:#fff"></i></span></div></div>'
            f'<div data-in="{T_PIN + .35:.2f}" style="position:absolute;left:12px;right:12px;bottom:40px;background:#fff;border-radius:26px;'
            'padding:20px;text-align:center"><div style="font-size:18px;color:#5a6b8c">Enter a PIN</div>'
            '<div style="font-size:36px;letter-spacing:12px;margin-top:8px;min-height:44px"><span data-type="locktype:pinin"></span></div>'
            f'<div data-in="{T_PIN + 1.9:.2f}" style="font-size:17px;color:#137a43;font-weight:800;margin-top:6px">✓ Secure Folder ready</div></div>')

GALLERY = (SB + '<div style="display:flex;align-items:center;justify-content:space-between;padding:20px 22px 14px">'
           '<span style="font-size:24px;font-weight:700">3 selected</span><span style="font-size:24px">⋮</span></div>'
           + thumbs(9, 120, 6, sel={0, 2, 4})
           + f'<div data-in="{18.53 + .1 * 2.97:.2f}" style="position:absolute;left:30px;right:30px;bottom:30px;background:#fff;'
             'border-radius:24px;box-shadow:0 10px 30px rgba(0,0,0,.2);padding:8px 0;font-size:19px">'
             '<div style="padding:14px 22px">Share</div><div style="padding:14px 22px">Add to album</div>'
             '<div data-id="move" style="padding:14px 22px;font-weight:700;color:#3e91ff">🔒 Move to Secure Folder</div></div>')


def card(win, top, html, border=YEL, left=40, width=520):
    return (f'<div data-in="{win}" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:16px 22px">{html}</div>')


def space(icon, title, sub, col):
    return (f'<div style="flex:1;border:3px dashed {col};border-radius:22px;padding:14px 10px;text-align:center">'
            f'<div style="font-size:48px">{icon}</div><div style="font-size:26px;font-weight:900">{title}</div>'
            f'<div style="font-size:19px;color:#cfe3ff">{sub}</div></div>')


OVERLAY = (
    card('-1,4.1', 260, f'<div style="font-size:48px;font-weight:900;color:{YEL};line-height:1.1">🔒 Secure Folder</div>'
                        '<div style="font-size:30px;font-weight:800;margin-top:8px;line-height:1.3">Private photos & apps,<br>'
                        'behind their own lock</div>')
    + card('4.2,10.6', 260, '<div style="font-size:30px;font-weight:800;color:#cfe3ff">Built into Samsung</div>'
                            f'<div style="font-size:44px;font-weight:900;color:{YEL};line-height:1.15">2 locks</div>'
                            '<div style="font-size:28px;font-weight:700;line-height:1.4">📱 Phone lock<br>🔒 Secure Folder lock</div>', CY)
    + card('21.6,24.6', 250, '<div style="display:flex;gap:14px">' + space('📱', 'Phone', 'what a borrower sees', CY)
           + space('🔒', 'Secure Folder', 'locked & hidden', YEL) + '</div>', GRN))

SPEC = {
    'audio': 'host/voices/securefolder.flac', 'lang': 'en', 'device': 'galaxy', 'overlay': OVERLAY,
    'title': 'Hide private photos & apps 🔒', 'tag': 'SAMSUNG · SECURE FOLDER', 'tip': 'TIP #13',
    'start': 'sfhome',
    'screens': {
        'sfhome': {**GAL, 'type': 'html', 'bg': '#1c4fb8', 'html': SF_HOME},
        'ghome': {**GAL, 'type': 'home', 'apps': GHOME_APPS, 'wallpaper': 'linear-gradient(160deg,#2a5bd7 0%,#6a3fd1 55%,#1b1f6b 100%)'},
        'lock': {**GAL, 'type': 'html', 'bg': '#1c4fb8', 'html': LOCK},
        'gset': {**GAL, 'type': 'html', 'bg': '#f4f4f6', 'html': SETTINGS},
        'gsearch': {**GAL, 'type': 'html', 'bg': '#f4f4f6', 'html': SEARCH},
        'setup': {**GAL, 'type': 'html', 'bg': '#f4f4f6', 'html': SETUP},
        'locktype': {**GAL, 'type': 'html', 'bg': '#f4f4f6', 'html': LOCKTYPE},
        'gallery': {**GAL, 'type': 'html', 'bg': '#f4f4f6', 'html': GALLERY},
    },
    'beats': [
        {'t': [0.0, 3.95], 'say': 'Let someone borrow your Samsung phone without exposing your private photos and apps!',
         'cap': 'LEND YOUR SAMSUNG WITHOUT EXPOSING YOUR PRIVATE STUFF 🔒', 'capsize': 76, 'pose': 'point', 'hook': True},
        {'t': [4.15, 10.54], 'say': 'Samsung has a built-in feature called Secure Folder that protects your private files and apps behind a separate lock.',
         'cap': 'Secure Folder: private files & apps behind a separate lock 🔐', 'pose': 'talk',
         'do': [{'nav': 'ghome', 'style': 'fade', 'at': 0}, {'tap': 'sf', 'at': .5, 'nav': 'lock', 'style': 'zoom'}]},
        {'t': [10.74, 14.73], 'say': 'Open Settings, search for Secure Folder, and follow the setup instructions.',
         'cap': 'Step 1: Settings › search “Secure Folder” › follow the setup', 'pose': 'point', 'step': 1,
         'do': [{'nav': 'gset', 'style': 'fade', 'at': 0}, {'tap': 'search', 'at': .14, 'nav': 'gsearch', 'style': 'fade'},
                {'typetext': 'Secure Folder', 'into': 'q', 'from': .28, 'to': .44},
                {'tap': 'res', 'at': .58, 'nav': 'setup', 'style': 'fade', 'fx': .4}, {'tap': 'cont', 'at': .9, 'nav': 'locktype'}]},
        {'t': [14.93, 18.33], 'say': 'Choose a PIN, password, or supported biometric lock.',
         'cap': 'Step 2: Choose a PIN, password or biometric lock', 'pose': 'point', 'step': 2,
         'do': [{'tap': 'pin', 'at': .3, 'fx': .3}, {'typetext': '••••••', 'into': 'pinin', 'from': .45, 'to': .75}]},
        {'t': [18.53, 24.50], 'say': "Now move your private photos, files, and apps inside. They'll be protected separately from your regular phone space.",
         'cap': 'Step 3: Move private photos, files & apps inside ✅', 'pose': 'point', 'step': 3,
         'do': [{'nav': 'gallery', 'style': 'fade', 'at': 0}, {'tap': 'move', 'at': .3, 'nav': 'sfhome', 'style': 'fade', 'fx': .5},
                {'fx': 'lock_close', 'at': .45}]},
        {'t': [24.70, 26.09], 'say': 'Want more hidden tech features?', 'cap': 'Want more hidden tech features? 👀', 'pose': 'talk'},
        {'t': [26.29, 28.37], 'say': 'Follow Tech Wall for daily tech secrets!', 'cap': 'Follow Tech Wall for daily tech secrets! 🚀',
         'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

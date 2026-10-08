"""Tech Wall HOST episode (TV + phone, two rigs): play your PS5 on your phone with Remote Play.
    ./build.sh remoteplay  |  python3 remoteplay.py 0 150 400
PlayStation Support: PS5 Settings > System > Remote Play > Enable Remote Play; PS Remote Play app (iOS / Android),
sign in with the same account as on the PS5, select the console. To start from Rest Mode: Settings > System >
Power Saving > Features Available in Rest Mode > Stay Connected to the Internet + Enable Turning On PS5 from Network.
Generic look-alikes only (no logos, unlabelled face buttons, generic app icon)."""
import host

EP = 'remoteplay'
PAD_GLYPH = ('<svg viewBox="0 0 64 40" style="width:{w}px"><path d="M14 4h36c8 0 12 6 13 14l1 10c1 8-7 12-12 6l-5-6H17l-5 6'
             'c-5 6-13 2-12-6l1-10C2 10 6 4 14 4z" fill="#fff"/><path d="M15 15v10M10 20h10" stroke="#1f4fd8" stroke-width="3.4"'
             ' stroke-linecap="round"/><circle cx="45" cy="16" r="2.8" fill="#1f4fd8"/><circle cx="51" cy="22" r="2.8" fill="#1f4fd8"/></svg>')
SB_DARK = '<div class="sb" style="color:#fff"><span>10:08</span><span class="bat"></span></div>'
DARK = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 15%,#1d3f9e 0%,#0a1a4a 55%,#030a22 100%);color:#fff;font-family:Poppins'

# Result screen: the game streams in the top half, touch controls below (portrait layout of the app)
GAME = f'''<div style="position:absolute;inset:0;background:#05070d;color:#fff;font-family:Poppins">{SB_DARK}
<div style="position:absolute;left:18px;right:18px;top:70px;display:flex;justify-content:space-between;align-items:center;font-size:15px;font-weight:600">
  <span style="background:#e53935;border-radius:8px;padding:3px 10px;letter-spacing:1px">● LIVE</span><span style="color:#9fb0d6">Streaming from PS5</span></div>
<div style="position:absolute;left:0;right:0;top:112px;height:232px;overflow:hidden;background:linear-gradient(#5ab8ff 0%,#bfe6ff 46%,#3aa655 46%)">
  <div style="position:absolute;left:0;right:0;top:46%;bottom:0;background:repeating-linear-gradient(#3aa655 0 18px,#2f8f48 18px 36px)" data-scroll="0,240"></div>
  <div style="position:absolute;left:0;right:0;top:46%;bottom:0;background:#4a4f5c;clip-path:polygon(46% 0,54% 0,100% 100%,0 100%)"></div>
  <div style="position:absolute;left:0;right:0;top:46%;bottom:0;clip-path:polygon(49.4% 0,50.6% 0,53% 100%,47% 100%);background:repeating-linear-gradient(#fff 0 16px,transparent 16px 34px)" data-scroll="0,240"></div>
  <div style="position:absolute;left:30px;top:34px;width:70px;height:22px;border-radius:12px;background:#fff;opacity:.85" data-bob="14"></div>
  <div style="position:absolute;left:150px;top:150px;width:98px;height:62px" data-bob="12">
    <div style="position:absolute;left:4px;right:4px;top:0;height:30px;border-radius:14px 14px 4px 4px;background:#c62828"></div>
    <div style="position:absolute;left:16px;right:16px;top:5px;height:14px;border-radius:6px;background:#263238"></div>
    <div style="position:absolute;left:0;right:0;top:24px;height:24px;border-radius:8px;background:#e53935"></div>
    <div style="position:absolute;left:8px;top:30px;width:16px;height:8px;border-radius:3px;background:#ffd54a"></div>
    <div style="position:absolute;right:8px;top:30px;width:16px;height:8px;border-radius:3px;background:#ffd54a"></div>
    <div style="position:absolute;left:2px;top:44px;width:22px;height:18px;border-radius:5px;background:#111"></div>
    <div style="position:absolute;right:2px;top:44px;width:22px;height:18px;border-radius:5px;background:#111"></div></div>
  <div style="position:absolute;left:12px;top:10px;font-weight:800;font-size:17px;text-shadow:0 2px 4px #0008">LAP 2/3</div>
  <div style="position:absolute;right:12px;top:10px;font-weight:800;font-size:17px;color:#ffd54a;text-shadow:0 2px 4px #0008">1st</div>
  <div style="position:absolute;right:12px;bottom:8px;font-weight:800;font-size:24px;text-shadow:0 2px 4px #0008">212 <small style="font-size:13px">km/h</small></div></div>
<div style="position:absolute;left:34px;top:420px;width:130px;height:130px">
  <div style="position:absolute;left:44px;top:0;width:42px;height:130px;border-radius:10px;background:#2a3147"></div>
  <div style="position:absolute;left:0;top:44px;width:130px;height:42px;border-radius:10px;background:#2a3147"></div></div>
<div style="position:absolute;right:30px;top:410px;width:150px;height:150px">
  <i style="position:absolute;left:52px;top:0;width:46px;height:46px;border-radius:50%;border:4px solid #5ce1ff"></i>
  <i style="position:absolute;left:104px;top:52px;width:46px;height:46px;border-radius:50%;border:4px solid #ff7a45"></i>
  <i style="position:absolute;left:52px;top:104px;width:46px;height:46px;border-radius:50%;border:4px solid #7CFC9A"></i>
  <i style="position:absolute;left:0;top:52px;width:46px;height:46px;border-radius:50%;border:4px solid #ffd54a"></i></div>
<div style="position:absolute;left:150px;top:372px;width:36px;height:14px;border-radius:7px;background:#2a3147"></div>
<div style="position:absolute;right:150px;top:372px;width:36px;height:14px;border-radius:7px;background:#2a3147"></div>
<div style="position:absolute;left:90px;top:610px;width:84px;height:84px;border-radius:50%;background:#1a2033;box-shadow:inset 0 0 0 3px #2a3147">
  <i style="position:absolute;left:20px;top:20px;width:44px;height:44px;border-radius:50%;background:#3a4766"></i></div>
<div style="position:absolute;right:90px;top:610px;width:84px;height:84px;border-radius:50%;background:#1a2033;box-shadow:inset 0 0 0 3px #2a3147">
  <i style="position:absolute;left:20px;top:20px;width:44px;height:44px;border-radius:50%;background:#3a4766"></i></div>
<div style="position:absolute;left:0;right:0;bottom:44px;text-align:center;font-size:15px;color:#7CFC9A;font-weight:600">● Connected</div></div>'''

STORE = f'''<div style="position:absolute;inset:0;background:#fff;color:#111;font-family:Poppins">
<div class="sb"><span>10:08</span><span class="bat"></span></div><div class="nav">‹ Search</div>
<div style="display:flex;gap:18px;padding:18px 22px 0">
  <div style="width:118px;height:118px;border-radius:28px;flex:none;display:grid;place-items:center;background:linear-gradient(135deg,#3d8bff,#0a2b8a);box-shadow:0 6px 14px rgba(0,0,0,.2)">{PAD_GLYPH.format(w=76)}</div>
  <div style="flex:1"><div style="font-size:23px;font-weight:700;line-height:1.15">PS Remote Play</div>
    <div style="font-size:15px;color:#8a8a8e;margin-top:4px">Play your console games</div>
    <div data-id="get" style="display:inline-block;margin-top:16px;background:#0a7aff;color:#fff;font-weight:700;font-size:18px;padding:7px 26px;border-radius:20px"><span class="val">GET</span></div></div></div>
<div style="display:flex;justify-content:space-around;margin:26px 22px 0;padding:14px 0;border-top:1px solid #e3e3e8;border-bottom:1px solid #e3e3e8;font-size:14px;color:#8a8a8e;text-align:center">
  <div><b style="font-size:20px;color:#3a3a3c">4.5</b><br>★★★★★</div><div><b style="font-size:20px;color:#3a3a3c">Free</b><br>Price</div><div><b style="font-size:20px;color:#3a3a3c">4+</b><br>Age</div></div>
<div style="display:flex;gap:14px;padding:22px 22px 0">
  <div style="flex:1;height:330px;border-radius:18px;background:linear-gradient(#5ab8ff 0%,#bfe6ff 40%,#3aa655 40%);position:relative;overflow:hidden">
    <div style="position:absolute;left:0;right:0;top:40%;bottom:0;background:#4a4f5c;clip-path:polygon(44% 0,56% 0,100% 100%,0 100%)"></div>
    <div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:#05070d"></div></div>
  <div style="flex:1;height:330px;border-radius:18px;background:linear-gradient(160deg,#5c6cff,#1b1f6b);position:relative">
    <div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:#05070d;border-radius:0 0 18px 18px"></div></div></div></div>'''

SIGNIN = f'''<div style="{DARK}">{SB_DARK}
<div style="text-align:center;margin-top:120px">{PAD_GLYPH.format(w=150)}</div>
<div style="text-align:center;font-size:34px;font-weight:800;margin-top:26px">Remote Play</div>
<div style="text-align:center;font-size:17px;color:#bfd0ff;margin:12px 40px 0;line-height:1.4">Play games on your console<br>from this device.</div>
<div data-id="signin" style="position:absolute;left:40px;right:40px;top:560px;height:62px;border-radius:31px;background:#fff;color:#0a2b8a;font-weight:800;font-size:21px;display:grid;place-items:center">Sign In</div>
<div style="position:absolute;left:30px;right:30px;top:640px;text-align:center;font-size:14px;color:#9fb0d6">Use the same account as on your console</div></div>'''

CONSOLES = f'''<div style="{DARK}">{SB_DARK}
<div style="font-size:28px;font-weight:800;padding:40px 26px 6px">Choose your console</div>
<div style="font-size:15px;color:#9fb0d6;padding:0 26px 22px">Signed in as Sam</div>
<div data-id="ps5" style="margin:0 20px;height:120px;border-radius:20px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.25);display:flex;align-items:center;gap:20px;padding:0 22px">
  <div style="width:34px;height:84px;border-radius:12px 12px 6px 6px;background:#fff;position:relative;flex:none"><i style="position:absolute;left:14px;top:0;width:6px;height:84px;background:#0a1a4a"></i></div>
  <div><div style="font-size:26px;font-weight:800">PS5</div><div style="font-size:15px;color:#7CFC9A">● Ready to connect</div></div></div>
<div style="margin:16px 20px 0;height:96px;border-radius:20px;border:2px dashed rgba(255,255,255,.2);display:grid;place-items:center;font-size:16px;color:#9fb0d6">Search again</div></div>'''

CONNECTING = f'''<div style="{DARK}">{SB_DARK}
<div style="position:absolute;left:129px;top:250px;width:140px;height:140px;border-radius:50%;border:10px solid rgba(255,255,255,.15);border-top-color:#5ce1ff" data-spin="420"></div>
<div style="position:absolute;left:0;right:0;top:430px;text-align:center;font-size:24px;font-weight:700">Connecting to PS5…</div>
<div style="position:absolute;left:0;right:0;top:470px;text-align:center;font-size:15px;color:#9fb0d6">Keep your phone on a fast connection</div></div>'''

TV = {'dev': 'tv'}
SPEC = {
    'devices': ['phone', 'tv'], 'lang': 'en', 'voice': 'am_puck', 'speed': 0.92,
    'title': 'Play your PS5 on your phone 🎮', 'tag': 'REMOTE PLAY · PS5 → PHONE', 'tip': 'TIP #03',
    'start': 'play',
    'screens': {
        # phone (iPhone look; the app is the same on Android)
        'play': {'type': 'html', 'bg': '#05070d', 'html': GAME},
        'store': {'type': 'html', 'bg': '#fff', 'html': STORE},
        'signin': {'type': 'html', 'bg': '#0a1a4a', 'html': SIGNIN},
        'consoles': {'type': 'html', 'bg': '#0a1a4a', 'html': CONSOLES},
        'connecting': {'type': 'html', 'bg': '#0a1a4a', 'html': CONNECTING},
        # TV + console
        'home': {**TV, 'type': 'tiles', 'title': 'Games', 'focus': 'g1', 'top': [{'id': 'settings', 'icon': 'gear'}],
                 'tiles': [{'id': 'g1', 'label': 'Racing', 'color': 'linear-gradient(135deg,#ff7a45,#c2185b)'},
                           {'id': 'g2', 'label': 'Space', 'color': 'linear-gradient(135deg,#5c6cff,#1b1f6b)'},
                           {'id': 'g3', 'label': 'Football', 'color': 'linear-gradient(135deg,#34c759,#0b6b2b)'},
                           {'id': 'g4', 'label': 'Puzzle', 'color': 'linear-gradient(135deg,#ffd54a,#e07b00)'},
                           {'id': 'g5', 'label': 'Music', 'color': 'linear-gradient(135deg,#bf5af2,#5b1f8a)'}]},
        'settings': {**TV, 'type': 'menu', 'title': 'Settings', 'focus': 'network', 'rows': [
            {'id': 'network', 'label': 'Network', 'icon': 'wifi', 'color': '#2f6fe0'},
            {'id': 'users', 'label': 'Users and Accounts', 'icon': 'person', 'color': '#2f6fe0'},
            {'id': 'access', 'label': 'Accessibility', 'icon': 'hand', 'color': '#2f6fe0'},
            {'id': 'system', 'label': 'System', 'icon': 'general', 'color': '#2f6fe0'},
            {'id': 'sound', 'label': 'Sound', 'icon': 'sound', 'color': '#2f6fe0'},
            {'id': 'screen', 'label': 'Screen and Video', 'icon': 'display', 'color': '#2f6fe0'}]},
        'system': {**TV, 'type': 'menu', 'path': 'Settings', 'title': 'System', 'focus': 'sw', 'rows': [
            {'id': 'sw', 'label': 'System Software'}, {'id': 'power', 'label': 'Power Saving'},
            {'id': 'remote', 'label': 'Remote Play'}, {'id': 'hdmi', 'label': 'HDMI'},
            {'id': 'beeps', 'label': 'Beeps'}, {'id': 'lang', 'label': 'Language'}]},
        'remote': {**TV, 'type': 'menu', 'path': 'Settings › System', 'title': 'Remote Play', 'focus': 'enable',
                   'note': 'Play games on this console from your phone, tablet or PC.',
                   'rows': [{'id': 'enable', 'label': 'Enable Remote Play', 'toggle': False},
                            {'id': 'link', 'label': 'Link Device'}]},
        'rest': {**TV, 'type': 'menu', 'path': 'Settings › System › Power Saving', 'title': 'Features Available in Rest Mode',
                 'focus': 'usb', 'note': 'Lets Remote Play wake your PS5 from Rest Mode.',
                 'rows': [{'id': 'usb', 'label': 'Supply Power to USB Ports', 'value': '3 Hours'},
                          {'id': 'net', 'label': 'Stay Connected to the Internet', 'toggle': False},
                          {'id': 'wake', 'label': 'Enable Turning On PS5 from Network', 'toggle': False}]},
    },
    'beats': [
        {'say': 'Play your PS5 games, right on your phone!', 'cap': 'Play your PS5 games on your phone 📱🎮',
         'pose': 'welcome', 'hook': True},
        {'say': 'On the couch, in bed, even away from home.', 'cap': 'On the couch, in bed, even away from home 🛋️',
         'pose': 'talk'},
        {'say': "Here's how. On your PS5, open Settings.", 'cap': "Here's how: on your PS5, open Settings", 'pose': 'talk',
         'screen': 'home', 'do': [{'focus': 'settings', 'button': 'up', 'at': .55}, {'button': 'a', 'at': .86, 'nav': 'settings'}]},
        {'say': 'Step one. Go to System, then Remote Play.', 'cap': 'Step 1: System › Remote Play', 'pose': 'point', 'step': 1,
         'do': [{'focus': 'system', 'button': 'down', 'at': .45}, {'button': 'a', 'at': .57, 'nav': 'system'},
                {'focus': 'remote', 'button': 'down', 'at': .78}, {'button': 'a', 'at': .9, 'nav': 'remote'}]},
        {'say': 'Step two. Turn on, Enable Remote Play.', 'cap': 'Step 2: Turn on Enable Remote Play', 'pose': 'point', 'step': 2,
         'do': [{'button': 'a', 'at': .58}, {'set': 'enable', 'toggle': True, 'at': .6}]},
        {'say': 'Step three. On your phone, get the free PS Remote Play app.',
         'cap': 'Step 3: Get the free PS Remote Play app (iPhone & Android)', 'pose': 'talk', 'step': 3, 'screen': 'store',
         'do': [{'tap': 'get', 'at': .7, 'fx': .5}, {'set': 'get', 'value': 'OPEN', 'at': .86}]},
        {'say': 'Step four. Sign in with the same PlayStation account, and pick your PS5.',
         'cap': 'Step 4: Sign in (same account) › pick your PS5', 'pose': 'point', 'step': 4,
         'do': [{'tap': 'get', 'at': .03, 'fx': .5, 'nav': 'signin'}, {'tap': 'signin', 'at': .35, 'fx': .5, 'nav': 'consoles'},
                {'tap': 'ps5', 'at': .82, 'fx': .5, 'nav': 'connecting'}]},
        {'say': 'And boom! Your PS5 games, now on your phone!', 'cap': 'Done ✅ Your PS5, now on your phone!', 'pose': 'welcome',
         'do': [{'nav': 'play', 'style': 'zoom', 'at': .02}, {'fx': 'thumb', 'at': .1, 'dur': 2.6}, {'fx': 'confetti', 'at': .12}]},
        {'say': 'Bonus! Turn these two on, and leave your PS5 in Rest Mode, not off.',
         'cap': 'Bonus: turn both on, and leave your PS5 in Rest Mode', 'pose': 'point', 'screen': 'rest',
         'do': [{'focus': 'net', 'button': 'down', 'at': .21}, {'button': 'a', 'at': .27}, {'set': 'net', 'toggle': True, 'at': .28},
                {'focus': 'wake', 'button': 'down', 'at': .35}, {'button': 'a', 'at': .41}, {'set': 'wake', 'toggle': True, 'at': .42}]},
        {'say': 'Follow Tech Wall for more quick tips!', 'cap': 'Follow Tech Wall for more quick tips! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

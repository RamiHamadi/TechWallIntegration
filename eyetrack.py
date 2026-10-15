"""Tech Wall HOST episode with a supplied voice-over: control your iPhone with only your eyes (Eye Tracking).
    ./build.sh eyetrack  |  python3 eyetrack.py 0 150 400
Voice: the user's generated audio (host/voices/eyetrack.flac); each beat's 't' = [start, end] s in it.
Apple: Settings > Accessibility > Eye Tracking (Physical and Motor) > turn on > follow the dot to calibrate; look at an
item to move the pointer, hold your gaze to select it (Dwell Control). iOS 18+, iPhone 12 and later, iPhone SE (3rd gen).
The gaze pointer glides with data-keys (video time) and its dwell ring fills with data-ring."""
import host

EP = 'eyetrack'
SB = '<div class="sb"><span>10:08</span><span class="bat"></span></div>'

# gaze pointer: grey disc + white dwell ring (fills while the gaze holds); times are video seconds
GAZE = ('<div style="position:absolute;left:0;right:0;top:66px;text-align:center"><span style="background:rgba(0,0,0,.45);'
        'color:#fff;font-weight:700;font-size:15px;padding:6px 14px;border-radius:16px">◉ Eye Tracking on</span></div>'
        '<div data-keys="0,@home:camera;1.2,@home:camera;2.1,@home:weather;3.3,@home:weather;4.2,@home:notes;12.9,@home:notes;'
        '13.0,199,560;14.3,@home:photos;40,@home:photos" style="position:absolute;left:0;top:0;width:66px;height:66px;'
        'margin:-33px 0 0 -33px;z-index:30">'
        '<div data-ring="-0.7,1.0;15.9,17.0" style="position:absolute;inset:-13px;border-radius:50%;'
        'background:conic-gradient(#ffd54a calc(var(--p,0)*1turn),rgba(0,0,0,.28) 0);'
        '-webkit-mask:radial-gradient(circle closest-side,transparent 70%,#000 72%);mask:radial-gradient(circle closest-side,transparent 70%,#000 72%)"></div>'
        '<div style="position:absolute;inset:0;border-radius:50%;background:rgba(255,255,255,.35);border:4px solid #fff;'
        'box-shadow:0 0 0 3px rgba(10,43,102,.55),0 0 26px 6px rgba(255,255,255,.75)"></div>'
        '<div style="position:absolute;left:25px;top:25px;width:16px;height:16px;border-radius:50%;background:#fff"></div></div>')

CALIB = f'''<div style="position:absolute;inset:0;background:#fff;color:#111;font-family:Poppins">{SB}
<div style="position:absolute;left:0;right:0;top:380px;text-align:center;font-size:18px;color:#8a8a8e">Follow the dot with your eyes</div>
<div data-keys="11.2,199,300;11.6,60,120;12.0,338,120;12.35,338,720;12.75,60,720" style="position:absolute;left:0;top:0;width:40px;height:40px;
margin:-20px 0 0 -20px;border-radius:50%;background:radial-gradient(circle,#0a84ff 0 38%,rgba(10,132,255,.25) 40%);box-shadow:0 0 22px rgba(10,132,255,.6)"></div></div>'''

TILES = ['#ff9a62,#e8507a', '#5ac8fa,#007aff', '#76e07a,#2fb344', '#ffd60a,#ff9500', '#bf5af2,#5b4bd6', '#64d2ff,#0a84ff',
         '#ff6b81,#ff2d55', '#30d158,#248a3d', '#ffb340,#ff9500', '#5c6cff,#1b1f6b', '#ff7a45,#c2185b', '#34c759,#0b6b2b']
PHOTOS = (f'<div style="position:absolute;inset:0;background:#fff;color:#111;font-family:Poppins">{SB}'
          '<div style="font-size:32px;font-weight:700;padding:4px 20px 12px">Photos</div>'
          '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3px">'
          + ''.join(f'<div style="height:128px;background:linear-gradient(135deg,{c})"></div>' for c in TILES) + '</div></div>')

SPEC = {
    'audio': 'host/voices/eyetrack.flac', 'lang': 'en',
    'title': 'Control your iPhone with your eyes 👀', 'tag': 'ACCESSIBILITY · EYE TRACKING', 'tip': 'TIP #05',
    'start': 'home', 'start_pops': ['home:gaze'],
    'screens': {
        'home': {'type': 'home', 'pops': {'gaze': GAZE}},
        'settings': {'type': 'list', 'title': 'Settings', 'search': True, 'groups': [
            {'rows': [{'id': 'wifi', 'label': 'Wi-Fi', 'icon': 'wifi', 'color': '#0a84ff', 'value': 'Home', 'chev': True},
                      {'id': 'bt', 'label': 'Bluetooth', 'icon': 'bluetooth', 'color': '#0a84ff', 'value': 'On', 'chev': True}]},
            {'rows': [{'id': 'general', 'label': 'General', 'icon': 'general', 'color': '#8e8e93', 'chev': True},
                      {'id': 'access', 'label': 'Accessibility', 'icon': 'person', 'color': '#0a84ff', 'chev': True},
                      {'id': 'camera', 'label': 'Camera', 'icon': 'dot', 'color': '#8e8e93', 'chev': True},
                      {'id': 'display', 'label': 'Display & Brightness', 'icon': 'display', 'color': '#0a84ff', 'chev': True}]}]},
        'access': {'type': 'list', 'back': 'Settings', 'title': 'Accessibility', 'groups': [
            {'header': 'Vision', 'rows': [{'id': 'vo', 'label': 'VoiceOver', 'icon': 'sound', 'color': '#1c1c1e', 'value': 'Off', 'chev': True},
                                          {'id': 'zoom', 'label': 'Zoom', 'icon': 'general', 'color': '#1c1c1e', 'value': 'Off', 'chev': True},
                                          {'id': 'text', 'label': 'Display & Text Size', 'icon': 'display', 'color': '#0a84ff', 'chev': True}]},
            {'header': 'Physical and Motor', 'rows': [
                {'id': 'touch', 'label': 'Touch', 'icon': 'hand', 'color': '#0a84ff', 'chev': True},
                {'id': 'eye', 'label': 'Eye Tracking', 'icon': 'eye', 'color': '#0a84ff', 'value': 'Off', 'chev': True},
                {'id': 'faceid', 'label': 'Face ID & Attention', 'icon': 'faceid', 'color': '#34c759', 'chev': True},
                {'id': 'switch', 'label': 'Switch Control', 'icon': 'dot', 'color': '#1c1c1e', 'value': 'Off', 'chev': True},
                {'id': 'voicec', 'label': 'Voice Control', 'icon': 'sound', 'color': '#0a84ff', 'value': 'Off', 'chev': True}]}]},
        'eye': {'type': 'list', 'back': 'Accessibility', 'title': 'Eye Tracking', 'groups': [
            {'rows': [{'id': 'eyeon', 'label': 'Eye Tracking', 'toggle': False}],
             'footer': 'Control your iPhone with your eyes: look at an item to move the pointer, hold your gaze to select it.'},
            {'rows': [{'id': 'snap', 'label': 'Snap to Item', 'toggle': True},
                      {'id': 'autohide', 'label': 'Auto-Hide', 'toggle': True},
                      {'id': 'dwell', 'label': 'Dwell Control', 'value': 'On', 'chev': True}]}]},
        'calib': {'type': 'html', 'bg': '#fff', 'html': CALIB},
        'photosapp': {'type': 'html', 'bg': '#fff', 'html': PHOTOS},
    },
    'beats': [
        {'t': [0.24, 5.28], 'say': 'Did you know you can control your iPhone using only your eyes, without touching the screen?',
         'cap': 'Control your iPhone with ONLY your eyes 👀', 'pose': 'welcome', 'hook': True},
        {'t': [5.92, 9.28], 'say': 'Go to Settings, Accessibility, then Eye Tracking.',
         'cap': 'Step 1: Settings › Accessibility › Eye Tracking', 'pose': 'point', 'step': 1,
         'do': [{'hide': 'gaze', 'at': .02}, {'tap': 'settings', 'at': .2, 'nav': 'settings'},
                {'tap': 'access', 'at': .52, 'nav': 'access', 'fx': .4}, {'tap': 'eye', 'at': .86, 'nav': 'eye', 'fx': .4}]},
        {'t': [10.0, 12.22], 'say': 'Turn it on and follow the calibration steps.',
         'cap': 'Step 2: Turn it on › follow the calibration dot', 'pose': 'talk', 'step': 2,
         'do': [{'tap': 'eyeon', 'at': .22, 'fx': .86}, {'nav': 'calib', 'style': 'fade', 'at': .55}]},
        {'t': [12.78, 15.22], 'say': 'Now look at an app to move the cursor,',
         'cap': 'Step 3: Look at an app to move the pointer', 'pose': 'point', 'step': 3, 'screen': 'home',
         'do': [{'show': 'gaze', 'at': .04}]},
        {'t': [15.66, 17.42], 'say': 'and hold your gaze to select it.',
         'cap': 'Step 4: Hold your gaze to select it', 'pose': 'point', 'step': 4,
         'do': [{'nav': 'photosapp', 'style': 'zoom', 'at': .86}]},
        {'t': [18.18, 20.72], 'say': 'No hands, no touching. Just your eyes.',
         'cap': 'No hands. No touching. Just your eyes ✨', 'pose': 'welcome',
         'do': [{'fx': 'thumb', 'at': .1, 'dur': 2.4}, {'fx': 'confetti', 'at': .12}]},
        {'t': [21.38, 22.06], 'say': 'Would you try this?', 'cap': 'Would you try this? 🤔', 'pose': 'talk'},
        {'t': [22.64, 24.60], 'say': 'Follow Tech Wall for more hidden tech tricks.',
         'cap': 'Follow Tech Wall for more hidden tech tricks! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

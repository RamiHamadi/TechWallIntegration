"""Tech Wall HOST episode with a supplied voice-over: control your iPhone just by moving your head (Switch Control).
    ./build.sh headswitch  |  python3 headswitch.py 0 150 400
Voice: the user's generated audio (host/voices/headswitch.flac); each beat's 't' = [start, end] s in it.
Apple: Settings > Accessibility > Switch Control > Switches > Add New Switch > Camera > Left / Right Head Movement >
choose an action (one switch must be Select Item), then turn Switch Control on. The voice skips the action and the
toggle, so the screens show both. Home-screen scanning highlight + front-camera bubble animate with data-keys/data-ring."""
import host

EP = 'headswitch'
SB = '<div class="sb"><span>10:08</span><span class="bat"></span></div>'
ROWS = (131, 252, 373)                          # centres of the three app rows on the home screen
SELECT = (2.2, 5.6, 21.6)                       # head turns left -> Select (video seconds)


def scan_keys(t0, t1, step=1.1):
    """Auto-scanning highlight: one row after another between t0 and t1 (eased 0.25 s moves)."""
    keys, t, i = [], t0, 0
    while t < t1:
        y = ROWS[i % 3]; keys += [f'{t:.2f},199,{y}', f'{t + step - 0.25:.2f},199,{y}']; t += step; i += 1
    return keys


HL_KEYS = ';'.join(scan_keys(0, 8.2) + ['20.4,199,131'] + scan_keys(20.6, 27))
TURN = ';'.join(f'{a:.2f},0,0;{a + 0.18:.2f},-26,0;{a + 0.55:.2f},-26,0;{a + 0.8:.2f},0,0' for a in SELECT)
FLASH = ';'.join(f'{a + 0.15:.2f},{a + 0.35:.2f}' for a in SELECT)
SCAN = (f'<div data-keys="{HL_KEYS}" style="position:absolute;left:0;top:0;width:384px;height:128px;margin:-64px 0 0 -192px;'
        'border:6px solid #0a84ff;border-radius:24px;box-shadow:0 0 0 3px rgba(255,255,255,.85),0 0 24px rgba(10,132,255,.8);z-index:25">'
        f'<div data-ring="{FLASH}" style="position:absolute;inset:0;border-radius:18px;background:rgba(255,213,74,.55);'
        'opacity:calc(var(--p,0) * 3)"></div></div>'
        # front-camera bubble: a face that turns left on each Select
        '<div style="position:absolute;right:16px;top:430px;width:104px;height:104px;border-radius:50%;overflow:hidden;'
        'background:radial-gradient(circle at 50% 35%,#3a4766,#141c2e);border:4px solid #fff;box-shadow:0 10px 24px rgba(0,0,0,.35);z-index:26">'
        f'<svg data-keys="{TURN}" viewBox="0 0 100 100" style="position:absolute;left:0;top:0;width:104px;height:104px">'
        '<ellipse cx="50" cy="52" rx="24" ry="29" fill="#f2c9a0"/><path d="M26 44c0-20 48-20 48 0-6-8-42-8-48 0z" fill="#3b2a20"/>'
        '<circle cx="41" cy="50" r="3.2" fill="#222"/><circle cx="59" cy="50" r="3.2" fill="#222"/>'
        '<path d="M42 64q8 6 16 0" stroke="#222" stroke-width="3" fill="none" stroke-linecap="round"/></svg></div>'
        f'<div data-ring="{FLASH}" style="position:absolute;left:0;right:0;top:548px;text-align:center;opacity:calc(var(--p,0) * 4);z-index:27">'
        '<span style="background:#ffd54a;color:#0a2b66;font-weight:800;font-size:19px;padding:8px 16px;border-radius:18px">'
        '◀ Head left = Select</span></div>'
        '<div style="position:absolute;left:0;right:0;top:652px;text-align:center;z-index:27"><span style="background:rgba(0,0,0,.45);'
        'color:#fff;font-weight:700;font-size:15px;padding:6px 14px;border-radius:16px">◉ Switch Control on</span></div>')

SPEC = {
    'audio': 'host/voices/headswitch.flac', 'lang': 'en',
    'title': 'Control your iPhone with your head 🤯', 'tag': 'ACCESSIBILITY · SWITCH CONTROL', 'tip': 'TIP #06',
    'start': 'home', 'start_pops': ['home:scan'],
    'screens': {
        'home': {'type': 'home', 'pops': {'scan': SCAN}},
        'settings': {'type': 'list', 'title': 'Settings', 'search': True, 'groups': [
            {'rows': [{'id': 'wifi', 'label': 'Wi-Fi', 'icon': 'wifi', 'color': '#0a84ff', 'value': 'Home', 'chev': True},
                      {'id': 'bt', 'label': 'Bluetooth', 'icon': 'bluetooth', 'color': '#0a84ff', 'value': 'On', 'chev': True}]},
            {'rows': [{'id': 'general', 'label': 'General', 'icon': 'general', 'color': '#8e8e93', 'chev': True},
                      {'id': 'access', 'label': 'Accessibility', 'icon': 'person', 'color': '#0a84ff', 'chev': True},
                      {'id': 'camera', 'label': 'Camera', 'icon': 'dot', 'color': '#8e8e93', 'chev': True},
                      {'id': 'display', 'label': 'Display & Brightness', 'icon': 'display', 'color': '#0a84ff', 'chev': True}]}]},
        'access': {'type': 'list', 'back': 'Settings', 'title': 'Accessibility', 'groups': [
            {'header': 'Vision', 'rows': [{'id': 'vo', 'label': 'VoiceOver', 'icon': 'sound', 'color': '#1c1c1e', 'value': 'Off', 'chev': True},
                                          {'id': 'zoom', 'label': 'Zoom', 'icon': 'general', 'color': '#1c1c1e', 'value': 'Off', 'chev': True}]},
            {'header': 'Physical and Motor', 'rows': [
                {'id': 'touch', 'label': 'Touch', 'icon': 'hand', 'color': '#0a84ff', 'chev': True},
                {'id': 'eye', 'label': 'Eye Tracking', 'icon': 'eye', 'color': '#0a84ff', 'value': 'Off', 'chev': True},
                {'id': 'faceid', 'label': 'Face ID & Attention', 'icon': 'faceid', 'color': '#34c759', 'chev': True},
                {'id': 'switch', 'label': 'Switch Control', 'icon': 'dot', 'color': '#1c1c1e', 'value': 'Off', 'chev': True},
                {'id': 'voicec', 'label': 'Voice Control', 'icon': 'sound', 'color': '#0a84ff', 'value': 'Off', 'chev': True}]}]},
        'sc': {'type': 'list', 'back': 'Accessibility', 'title': 'Switch Control', 'groups': [
            {'rows': [{'id': 'scon', 'label': 'Switch Control', 'toggle': False}],
             'footer': 'Switch Control lets you use your iPhone by sequentially highlighting items on the screen that can be activated through an adaptive accessory.'},
            {'rows': [{'id': 'switches', 'label': 'Switches', 'value': '0', 'chev': True},
                      {'id': 'recipes', 'label': 'Recipes', 'chev': True},
                      {'id': 'style', 'label': 'Scanning Style', 'value': 'Auto Scanning', 'chev': True}]}]},
        'switches': {'type': 'list', 'back': 'Switch Control', 'title': 'Switches', 'groups': [
            {'rows': [{'id': 'add', 'label': 'Add New Switch…', 'style': 'blue'}]}]},
        'source': {'type': 'list', 'back': 'Switches', 'title': 'Source', 'groups': [
            {'rows': [{'id': 'external', 'label': 'External', 'chev': True},
                      {'id': 'screen', 'label': 'Screen', 'chev': True},
                      {'id': 'camera', 'label': 'Camera', 'chev': True}]}]},
        'camera': {'type': 'list', 'back': 'Source', 'title': 'Camera', 'groups': [
            {'rows': [{'id': 'left', 'label': 'Left Head Movement', 'chev': True},
                      {'id': 'right', 'label': 'Right Head Movement', 'chev': True}]}]},
        'action': {'type': 'list', 'back': 'Camera', 'title': 'Left Head Movement', 'groups': [
            {'header': 'Scanner', 'rows': [{'id': 'select', 'label': 'Select Item'},
                                           {'id': 'next', 'label': 'Move to Next Item'}]},
            {'header': 'System', 'rows': [{'id': 'home', 'label': 'Home'},
                                          {'id': 'switcher', 'label': 'App Switcher'}]}]},
    },
    'beats': [
        {'t': [0.24, 3.54], 'say': 'Did you know you can control your iPhone just by moving your head?',
         'cap': 'Control your iPhone just by moving your head 🤯', 'pose': 'welcome', 'hook': True},
        {'t': [4.0, 7.66], 'say': 'No hands, no touching the screen, just simple head gestures.',
         'cap': 'No hands. No touching. Just head gestures 🙌', 'pose': 'talk'},
        {'t': [8.4, 12.56], 'say': 'Go to Settings, Accessibility, Switch Control, Switches,',
         'cap': 'Step 1: Settings › Accessibility › Switch Control › Switches', 'pose': 'point', 'step': 1,
         'do': [{'hide': 'scan', 'at': .0}, {'tap': 'settings', 'at': .14, 'nav': 'settings'},
                {'tap': 'access', 'at': .38, 'nav': 'access', 'fx': .4}, {'tap': 'switch', 'at': .66, 'nav': 'sc', 'fx': .4},
                {'tap': 'switches', 'at': .93, 'nav': 'switches', 'fx': .4}]},
        {'t': [13.02, 14.88], 'say': 'Add new switch, then camera.',
         'cap': 'Step 2: Add New Switch › Camera', 'pose': 'point', 'step': 2,
         'do': [{'tap': 'add', 'at': .22, 'nav': 'source', 'fx': .3}, {'tap': 'camera', 'at': .82, 'nav': 'camera', 'fx': .3}]},
        {'t': [15.54, 18.52], 'say': 'Choose Head Movement and select left or right.',
         'cap': 'Step 3: Left or Right Head Movement › pick an action', 'pose': 'point', 'step': 3,
         'do': [{'tap': 'left', 'at': .55, 'nav': 'action', 'fx': .35}, {'tap': 'select', 'at': .9, 'nav': 'sc', 'back': True, 'fx': .3},
                {'set': 'switches', 'screen': 'sc', 'value': '1', 'at': .95}]},
        {'t': [19.16, 22.32], 'say': 'Now you can use your head movements to trigger actions on your iPhone.',
         'cap': 'Turn Switch Control on, then turn your head to act ✨', 'pose': 'welcome', 'step': 4,
         'do': [{'tap': 'scon', 'at': .1, 'fx': .86}, {'nav': 'home', 'style': 'fade', 'at': .36}, {'show': 'scan', 'at': .4},
                {'fx': 'confetti', 'at': .78}]},
        {'t': [22.82, 23.52], 'say': 'Try it yourself.', 'cap': 'Try it yourself! 🙂', 'pose': 'talk'},
        {'t': [23.9, 26.26], 'say': 'And follow Tech Wall for more hidden tech tricks.',
         'cap': 'Follow Tech Wall for more hidden tech tricks! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

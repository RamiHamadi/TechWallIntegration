"""Tech Wall HOST episode with a supplied voice-over: which apps can use your microphone (Android + iPhone).
    ./build.sh micperm  |  python3 micperm.py 0 150 400
Two rigs: a Samsung Galaxy (One UI look-alike, device 'galaxy') for the Android part and the iPhone for the iPhone part.
Voice: the user's generated audio (host/voices/micperm.flac); beat 't' = [start, end] s in it.
Samsung (2026 guides): Settings > Privacy > Permission manager > Microphone > app > Don't allow.
iPhone: Settings > Privacy & Security > Microphone > per-app toggles. Fictional apps, no logos."""
import host

EP = 'micperm'
GAL = {'dev': 'galaxy'}
RED = '#ff4d4f'

MIC_APPS = [('rec', 'Voice Recorder', 'sound', '#ff6b6b'), ('chat', 'Chat', 'person', '#34c759'),
            ('video', 'Video Call', 'display', '#5c6cff'), ('cam', 'Camera', 'eye', '#8e8e93'),
            ('flash', 'Flashlight Pro', 'star', '#ffb300')]
SURPRISE = ('<div style="position:absolute;left:14px;right:14px;top:700px;background:#fff;border:3px solid ' + RED + ';'
            'border-radius:22px;padding:12px 16px;box-shadow:0 12px 26px rgba(0,0,0,.18);text-align:center">'
            '<div style="font-size:20px;font-weight:800;color:' + RED + '">🤔 A flashlight with mic access?</div>'
            '<div style="font-size:15px;color:#555;margin-top:2px">Flashlight Pro · Allowed only while in use</div></div>')
RING = ('<div style="position:absolute;left:12px;right:12px;top:525px;height:66px;border-radius:22px;border:4px solid ' + RED + ';'
        'box-shadow:0 0 0 4px rgba(255,77,79,.25)"></div>')

def radio(top, win=None):
    """One UI radio: grey ring; with win, the blue selected ring + dot pops in/out over that window (video seconds)."""
    if win is None:
        return (f'<div style="position:absolute;left:30px;top:{top}px;width:28px;height:28px;border-radius:50%;background:#fff;'
                'border:2px solid #8a8f99"></div>')
    return (f'<div data-in="{win}" style="position:absolute;left:30px;top:{top}px;width:28px;height:28px;border-radius:50%;'
            'background:#fff;border:2px solid #3e91ff"><i style="position:absolute;left:5px;top:5px;width:14px;height:14px;'
            'border-radius:50%;background:#3e91ff"></i></div>')


OPTS = [('allow', 'Allow only while using the app'), ('ask', 'Ask every time'), ('dont', "Don't allow")]
T_DONT = 14.76 + 0.8 * (18.88 - 14.76)          # the moment "Don't allow" is tapped
APP_HTML = ('<div class="sb"><span>10:08</span><span class="bat"></span></div><div class="nav"></div>'
            '<div class="big">Flashlight Pro</div><div class="sect">Microphone access for this app</div>'
            '<div style="position:relative;margin:0 12px;background:#fff;border-radius:26px;height:204px">'
            + ''.join(f'<div data-id="{i}" style="position:absolute;left:0;right:0;top:{8 + k * 64}px;height:60px;display:flex;'
                      f'align-items:center;padding-left:74px;font-size:19px">{lab}</div>' for k, (i, lab) in enumerate(OPTS))
            + radio(24) + radio(88) + radio(152) + radio(24, f'-1,{T_DONT:.2f}') + radio(152, f'{T_DONT:.2f}') + '</div>')


SPEC = {
    'audio': 'host/voices/micperm.flac', 'lang': 'en', 'devices': ['galaxy', 'phone'],
    'title': 'Which apps can hear you? 🎤', 'tag': 'PRIVACY · MICROPHONE', 'tip': 'TIP #07',
    'start': 'gmic', 'start_pops': ['gmic:surprise', 'gmic:ring'],
    'screens': {
        # ---- Samsung Galaxy (One UI look-alike) ----
        'gmic': {**GAL, 'type': 'list', 'back': 'Permission manager', 'title': 'Microphone', 'groups': [
            {'header': 'Allowed only while in use', 'rows': [{'id': i, 'label': l, 'icon': ic, 'color': c} for i, l, ic, c in MIC_APPS]},
            {'header': 'Not allowed', 'rows': [{'id': 'game', 'label': 'Puzzle Game', 'icon': 'star', 'color': '#bf5af2'}]}],
            'pops': {'surprise': SURPRISE, 'ring': RING}},
        'ghome': {**GAL, 'type': 'home', 'wallpaper': 'linear-gradient(160deg,#2a5bd7 0%,#6a3fd1 55%,#1b1f6b 100%)'},
        'gset': {**GAL, 'type': 'list', 'title': 'Settings', 'groups': [
            {'rows': [{'id': 'conn', 'label': 'Connections', 'icon': 'wifi', 'color': '#3e91ff'},
                      {'id': 'sound', 'label': 'Sounds and vibration', 'icon': 'sound', 'color': '#a066ff'},
                      {'id': 'notif', 'label': 'Notifications', 'icon': 'bell', 'color': '#ff6b6b'},
                      {'id': 'display', 'label': 'Display', 'icon': 'display', 'color': '#3cb371'},
                      {'id': 'battery', 'label': 'Battery', 'icon': 'battery', 'color': '#3cb371'}]},
            {'rows': [{'id': 'security', 'label': 'Security', 'icon': 'lock', 'color': '#4b7bec'},
                      {'id': 'privacy', 'label': 'Privacy', 'icon': 'privacy', 'color': '#4b7bec'},
                      {'id': 'location', 'label': 'Location', 'icon': 'dot', 'color': '#34c759'}]}]},
        'gpriv': {**GAL, 'type': 'list', 'back': 'Settings', 'title': 'Privacy', 'groups': [
            {'rows': [{'id': 'used', 'label': 'Permissions used in last 24 hours'},
                      {'id': 'permman', 'label': 'Permission manager'},
                      {'id': 'controls', 'label': 'Controls and alerts'}]},
            {'rows': [{'id': 'other', 'label': 'Other privacy settings'}]}]},
        'gperm': {**GAL, 'type': 'list', 'back': 'Privacy', 'title': 'Permission manager', 'groups': [
            {'rows': [{'id': 'p_cal', 'label': 'Calendar', 'icon': 'dot', 'color': '#3e91ff'},
                      {'id': 'p_cam', 'label': 'Camera', 'icon': 'eye', 'color': '#3e91ff'},
                      {'id': 'p_con', 'label': 'Contacts', 'icon': 'person', 'color': '#3e91ff'},
                      {'id': 'p_loc', 'label': 'Location', 'icon': 'dot', 'color': '#3e91ff'},
                      {'id': 'mic', 'label': 'Microphone', 'icon': 'sound', 'color': '#3e91ff'},
                      {'id': 'p_near', 'label': 'Nearby devices', 'icon': 'bluetooth', 'color': '#3e91ff'},
                      {'id': 'p_not', 'label': 'Notifications', 'icon': 'bell', 'color': '#3e91ff'}]}]},
        'gmic2': {**GAL, 'type': 'list', 'back': 'Permission manager', 'title': 'Microphone', 'groups': [
            {'header': 'Allowed only while in use', 'rows': [{'id': i, 'label': l, 'icon': ic, 'color': c} for i, l, ic, c in MIC_APPS]},
            {'header': 'Not allowed', 'rows': [{'id': 'game', 'label': 'Puzzle Game', 'icon': 'star', 'color': '#bf5af2'}]}]},
        'gapp': {**GAL, 'type': 'html', 'bg': '#f4f4f6', 'html': APP_HTML},
        # ---- iPhone ----
        'ihome': {'dev': 'phone', 'type': 'home'},
        'iset': {'dev': 'phone', 'type': 'list', 'title': 'Settings', 'search': True, 'groups': [
            {'rows': [{'id': 'wifi', 'label': 'Wi-Fi', 'icon': 'wifi', 'color': '#0a84ff', 'value': 'Home', 'chev': True},
                      {'id': 'bt', 'label': 'Bluetooth', 'icon': 'bluetooth', 'color': '#0a84ff', 'value': 'On', 'chev': True}]},
            {'rows': [{'id': 'general', 'label': 'General', 'icon': 'general', 'color': '#8e8e93', 'chev': True},
                      {'id': 'battery', 'label': 'Battery', 'icon': 'battery', 'color': '#34c759', 'chev': True},
                      {'id': 'privsec', 'label': 'Privacy & Security', 'icon': 'hand', 'color': '#0a84ff', 'chev': True}]}]},
        'ipriv': {'dev': 'phone', 'type': 'list', 'back': 'Settings', 'title': 'Privacy & Security', 'groups': [
            {'rows': [{'id': 'loc', 'label': 'Location Services', 'icon': 'dot', 'color': '#0a84ff', 'value': 'On', 'chev': True},
                      {'id': 'track', 'label': 'Tracking', 'icon': 'eye', 'color': '#ff9500', 'chev': True}]},
            {'rows': [{'id': 'contacts', 'label': 'Contacts', 'icon': 'person', 'color': '#8e8e93', 'chev': True},
                      {'id': 'photos', 'label': 'Photos', 'icon': 'star', 'color': '#ff9500', 'chev': True},
                      {'id': 'bt2', 'label': 'Bluetooth', 'icon': 'bluetooth', 'color': '#0a84ff', 'chev': True},
                      {'id': 'imic', 'label': 'Microphone', 'icon': 'sound', 'color': '#ff9500', 'chev': True},
                      {'id': 'camera', 'label': 'Camera', 'icon': 'eye', 'color': '#8e8e93', 'chev': True}]}]},
        'imicl': {'dev': 'phone', 'type': 'list', 'back': 'Privacy & Security', 'title': 'Microphone', 'groups': [
            {'rows': [{'id': 'i_rec', 'label': 'Voice Memos', 'icon': 'sound', 'color': '#ff3b30', 'toggle': True},
                      {'id': 'i_chat', 'label': 'Chat', 'icon': 'person', 'color': '#34c759', 'toggle': True},
                      {'id': 'i_video', 'label': 'Video Call', 'icon': 'display', 'color': '#5c6cff', 'toggle': True},
                      {'id': 'i_flash', 'label': 'Flashlight Pro', 'icon': 'star', 'color': '#ffb300', 'toggle': True}],
             'footer': 'Applications that have requested access to the microphone will appear here.'}]},
    },
    'beats': [
        {'t': [0.27, 3.70], 'say': 'Your phone can show you which apps have access to your microphone.',
         'cap': 'Your phone shows which apps can use your microphone 🎤', 'pose': 'welcome', 'hook': True},
        {'t': [4.35, 6.15], 'say': 'And you might be surprised by what you find.',
         'cap': 'You might be surprised by what you find 😳', 'pose': 'talk'},
        {'t': [6.94, 11.02], 'say': 'On Android, open Settings, then Privacy, and tap Permission Manager.',
         'cap': 'Android (Samsung): Settings › Privacy › Permission manager', 'pose': 'point', 'step': 1, 'screen': 'ghome',
         'do': [{'tap': 'settings', 'at': .22, 'nav': 'gset'}, {'tap': 'privacy', 'at': .53, 'nav': 'gpriv', 'fx': .4},
                {'tap': 'permman', 'at': .87, 'nav': 'gperm', 'fx': .4}]},
        {'t': [11.67, 13.99], 'say': 'Choose Microphone to see which apps can use it.',
         'cap': 'Step 2: Tap Microphone to see which apps can use it', 'pose': 'point', 'step': 2,
         'do': [{'tap': 'mic', 'at': .25, 'nav': 'gmic2', 'fx': .4}]},
        {'t': [14.76, 18.88], 'say': "If an app doesn't need microphone access, you can change its permission to Don't allow.",
         'cap': "Step 3: Don't need it? Set it to Don't allow 🚫", 'pose': 'point', 'step': 3,
         'do': [{'tap': 'flash', 'at': .2, 'nav': 'gapp', 'fx': .4}, {'tap': 'dont', 'at': .78, 'fx': .4},
]},
        {'t': [19.71, 23.28], 'say': 'On iPhone, go to Settings, Privacy and Security, then Microphone.',
         'cap': 'iPhone: Settings › Privacy & Security › Microphone', 'pose': 'point', 'step': 4, 'screen': 'ihome',
         'do': [{'tap': 'settings', 'at': .26, 'nav': 'iset'}, {'tap': 'privsec', 'at': .58, 'nav': 'ipriv', 'fx': .4},
                {'tap': 'imic', 'at': .9, 'nav': 'imicl', 'fx': .4}]},
        {'t': [24.04, 30.45], 'say': "Remember, microphone permission doesn't mean an app is secretly recording you. But checking your permissions is a smart privacy habit.",
         'cap': 'Permission ≠ secretly recording, but checking is a smart habit ✅', 'pose': 'talk',
         'do': [{'tap': 'i_flash', 'at': .78, 'fx': .86}, {'fx': 'thumb', 'at': .84, 'dur': 2.2}]},
        {'t': [31.06, 33.39], 'say': 'Follow Tech Wall for more tech tricks you should know.',
         'cap': 'Follow Tech Wall for more tech tricks! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

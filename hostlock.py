"""Tech Wall HOST episode: lock your iPhone with a passcode (first Host-format episode, result-first).
    ./build.sh hostlock             -> out/hostlock.mp4 + out/cover_hostlock.jpg
    python3 hostlock.py 0 150 400   -> preview frames in out/frames_hostlock/
Path checked against Apple Support "Use a passcode with your iPhone": Settings > Face ID & Passcode > Turn Passcode On.
"""
import host

EP = 'hostlock'
SPEC = {
    'lang': 'en', 'voice': 'am_puck', 'speed': 0.92,           # Arabic: 'lang': 'ar', 'voice': 'kareem' (say = text with tashkeel)
    'title': 'How to lock your iPhone 🔒', 'tag': 'SCREEN LOCK · SETUP', 'tip': 'TIP #01',
    'start': 'lock',                                            # result-first: frame 0 shows the payoff
    'screens': {
        'lock': {'type': 'lock', 'badge': '✅ Passcode is ON'},
        'home': {'type': 'home'},
        'settings': {'type': 'list', 'title': 'Settings', 'search': True, 'groups': [
            {'rows': [{'label': 'Airplane Mode', 'icon': 'airplane', 'color': '#ff9500'},
                      {'label': 'Wi-Fi', 'icon': 'wifi', 'color': '#0a84ff', 'chev': True},
                      {'label': 'Bluetooth', 'icon': 'bluetooth', 'color': '#0a84ff', 'chev': True}]},
            {'rows': [{'label': 'Notifications', 'icon': 'bell', 'color': '#ff3b30', 'chev': True},
                      {'label': 'Sounds & Haptics', 'icon': 'sound', 'color': '#ff2d55', 'chev': True},
                      {'label': 'Focus', 'icon': 'moon', 'color': '#5e5ce6', 'chev': True}]},
            {'rows': [{'label': 'General', 'icon': 'general', 'color': '#8e8e93', 'chev': True},
                      {'label': 'Display & Brightness', 'icon': 'display', 'color': '#0a84ff', 'chev': True},
                      {'id': 'face', 'label': 'Face ID & Passcode', 'icon': 'faceid', 'color': '#30d158', 'chev': True},
                      {'label': 'Battery', 'icon': 'battery', 'color': '#30d158', 'chev': True},
                      {'label': 'Privacy & Security', 'icon': 'privacy', 'color': '#0a84ff', 'chev': True}]}]},
        'face': {'type': 'list', 'back': 'Settings', 'title': 'Face ID & Passcode', 'groups': [
            {'header': 'Use Face ID for:', 'rows': [{'label': 'iPhone Unlock', 'style': 'grey'},
                                                   {'label': 'Wallet & Payments', 'style': 'grey'}]},
            {'rows': [{'label': 'Set Up Face ID', 'style': 'blue'}]},
            {'rows': [{'id': 'on', 'label': 'Turn Passcode On', 'style': 'blue'},
                      {'label': 'Change Passcode', 'style': 'grey'}],
             'footer': 'A passcode protects your data and is needed to unlock your phone.'}]},
        'pass': {'type': 'passcode', 'title': 'Set Passcode'},
    },
    'beats': [
        {'say': 'Hey! Want to stop people snooping on your phone?',
         'cap': 'Hey! Want to stop people snooping on your phone? 👀', 'pose': 'welcome', 'hook': True},
        {'say': "Here's how. It takes twenty seconds.", 'cap': "Here's how. It takes 20 seconds.",
         'pose': 'talk', 'screen': 'home'},
        {'say': 'Step one. Open Settings, and tap Face ID and Passcode.',
         'cap': 'Step 1: Open Settings → tap Face ID & Passcode', 'pose': 'point', 'step': 1,
         'do': [{'tap': 'settings', 'at': .30, 'nav': 'settings'}, {'tap': 'face', 'at': .80, 'nav': 'face'}]},
        {'say': 'Step two. Tap, Turn Passcode On.', 'cap': 'Step 2: Tap Turn Passcode On', 'pose': 'point', 'step': 2,
         'do': [{'tap': 'on', 'at': .55, 'nav': 'pass'}]},
        {'say': 'Step three. Type a six digit code, then type it again to confirm.',
         'cap': 'Step 3: Type a 6-digit code, then type it again to confirm', 'pose': 'talk', 'step': 3,
         'do': [{'type': '258014', 'from': .16, 'to': .42}, {'reprompt': True, 'at': .50},
                {'type': '258014', 'from': .58, 'to': .86}]},
        {'say': 'And done! Your phone now locks itself. Nobody gets in without your code.',
         'cap': 'Done! ✅ Your phone now locks itself.', 'pose': 'welcome',
         'do': [{'nav': 'lock', 'at': 0, 'style': 'zoom'}, {'fx': 'lock_close', 'at': .12},
                {'fx': 'confetti', 'at': .14}, {'fx': 'thumb', 'at': .04, 'dur': 3.4}]},
        {'say': 'Follow Tech Wall for more quick tips!', 'cap': 'Follow Tech Wall for more quick tips! 🚀',
         'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

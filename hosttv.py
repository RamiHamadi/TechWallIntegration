"""Tech Wall HOST episode (TV + console): charge controllers in Rest Mode (template for console tips).
    ./build.sh hosttv  |  python3 hosttv.py 0 200 400
PlayStation Support: Settings > System > Power Saving > Features Available in Rest Mode > Supply Power to USB Ports (Always / 3 Hours).
Generic controller and menus (no brand marks)."""
import host

EP = 'hosttv'
OPTS = ('<div style="position:absolute;left:520px;top:150px;width:330px;background:#1c2748;border-radius:14px;padding:10px;'
        'box-shadow:0 18px 40px rgba(0,0,0,.5)">'
        + ''.join(f'<div class="mrow" data-id="opt-{k}">{v}</div>' for k, v in (('off', "Don't Supply"), ('3h', '3 Hours'), ('always', 'Always')))
        + '</div>')
SPEC = {
    'device': 'tv', 'lang': 'en', 'voice': 'am_puck', 'speed': 1.08,
    'title': 'Charge controllers in Rest Mode 🎮', 'tag': 'REST MODE · USB POWER', 'tip': 'TIP #03',
    'start': 'rest',
    'screens': {
        'home': {'type': 'tiles', 'title': 'Games', 'focus': 'g1', 'top': [{'id': 'settings', 'icon': 'gear'}],
                 'tiles': [{'id': 'g1', 'label': 'Racing', 'color': 'linear-gradient(135deg,#ff7a45,#c2185b)'},
                           {'id': 'g2', 'label': 'Space', 'color': 'linear-gradient(135deg,#5c6cff,#1b1f6b)'},
                           {'id': 'g3', 'label': 'Football', 'color': 'linear-gradient(135deg,#34c759,#0b6b2b)'},
                           {'id': 'g4', 'label': 'Puzzle', 'color': 'linear-gradient(135deg,#ffd54a,#e07b00)'},
                           {'id': 'g5', 'label': 'Music', 'color': 'linear-gradient(135deg,#bf5af2,#5b1f8a)'}]},
        'settings': {'type': 'menu', 'title': 'Settings', 'focus': 'network', 'rows': [
            {'id': 'network', 'label': 'Network', 'icon': 'wifi', 'color': '#2f6fe0'},
            {'id': 'users', 'label': 'Users and Accounts', 'icon': 'person', 'color': '#2f6fe0'},
            {'id': 'access', 'label': 'Accessibility', 'icon': 'hand', 'color': '#2f6fe0'},
            {'id': 'system', 'label': 'System', 'icon': 'general', 'color': '#2f6fe0'},
            {'id': 'sound', 'label': 'Sound', 'icon': 'sound', 'color': '#2f6fe0'},
            {'id': 'screen', 'label': 'Screen and Video', 'icon': 'display', 'color': '#2f6fe0'}]},
        'system': {'type': 'menu', 'path': 'Settings', 'title': 'System', 'focus': 'sw', 'rows': [
            {'id': 'sw', 'label': 'System Software'}, {'id': 'power', 'label': 'Power Saving'},
            {'id': 'beeps', 'label': 'Beeps'}, {'id': 'lang', 'label': 'Language'}, {'id': 'date', 'label': 'Date and Time'}]},
        'power': {'type': 'menu', 'path': 'Settings › System', 'title': 'Power Saving', 'focus': 'time', 'rows': [
            {'id': 'time', 'label': 'Set Time Until Console Enters Rest Mode'},
            {'id': 'feat', 'label': 'Features Available in Rest Mode'}]},
        'rest': {'type': 'menu', 'path': 'System › Power Saving', 'title': 'Features Available in Rest Mode', 'focus': 'usb',
                 'note': 'Controllers plugged into the console keep charging while it rests.',
                 'rows': [{'id': 'usb', 'label': 'Supply Power to USB Ports', 'value': 'Always'},
                          {'id': 'net', 'label': 'Stay Connected to the Internet', 'toggle': True},
                          {'id': 'wake', 'label': 'Enable Turning On from Network', 'toggle': False}],
                 'pops': {'opts': OPTS}},
    },
    'beats': [
        {'say': 'Your controllers can charge, while the console sleeps.', 'cap': 'Charge controllers while your PS5 sleeps 🔋',
         'pose': 'welcome', 'hook': True},
        {'say': "Here's how. Open Settings, at the top right.", 'cap': "Here's how: Settings (top right)", 'pose': 'talk',
         'screen': 'home', 'do': [{'set': 'usb', 'screen': 'rest', 'value': "Don't Supply", 'at': .05},
                                  {'focus': 'settings', 'button': 'up', 'at': .5}, {'button': 'a', 'at': .85, 'nav': 'settings'}]},
        {'say': 'Step one. Go to System, then Power Saving.', 'cap': 'Step 1: System › Power Saving', 'pose': 'point', 'step': 1,
         'do': [{'focus': 'system', 'button': 'down', 'at': .18}, {'button': 'a', 'at': .36, 'nav': 'system'},
                {'focus': 'power', 'button': 'down', 'at': .62}, {'button': 'a', 'at': .82, 'nav': 'power'}]},
        {'say': 'Step two. Open, Features Available in Rest Mode.', 'cap': 'Step 2: Features Available in Rest Mode',
         'pose': 'point', 'step': 2, 'do': [{'focus': 'feat', 'button': 'down', 'at': .35}, {'button': 'a', 'at': .7, 'nav': 'rest'}]},
        {'say': 'Step three. Set Supply Power to USB Ports, to Always.', 'cap': 'Step 3: Supply Power to USB Ports › Always',
         'pose': 'talk', 'step': 3, 'do': [{'button': 'a', 'at': .25}, {'show': 'opts', 'at': .27},
                                          {'focus': 'opt-always', 'button': 'down', 'at': .5}, {'button': 'a', 'at': .74},
                                          {'hide': 'opts', 'at': .76}, {'set': 'usb', 'value': 'Always', 'at': .78},
                                          {'focus': 'usb', 'at': .79}]},
        {'say': 'Done! Now they charge, even in Rest Mode.', 'cap': 'Done ✅ They charge in Rest Mode', 'pose': 'welcome',
         'do': [{'fx': 'thumb', 'at': .05, 'dur': 2.6}, {'fx': 'confetti', 'at': .1}]},
        {'say': 'Follow Tech Wall for more quick tips!', 'cap': 'Follow Tech Wall for more quick tips! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

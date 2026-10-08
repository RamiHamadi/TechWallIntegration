"""Tech Wall HOST episode (laptop): the hidden emoji panel, WIN + . (template for PC tips).
    ./build.sh hostpc  |  python3 hostpc.py 0 200 400
Microsoft Support: "Windows logo key + period (.)" opens the emoji panel; Windows 11 adds GIFs, kaomoji and symbols.
"""
import host

EP = 'hostpc'
_E = '😎😂😍🥳👍🔥🎉😅🤔🙌💯😴😭🤯🍕☕🚀❤️'
EMOJI = ''.join('<span style="display:grid;place-items:center;height:52px;border-radius:8px"%s>%s</span>'
                % (' data-id="e1"' if i == 0 else '', e) for i, e in enumerate(_E))
PANEL = ('<div style="position:absolute;left:478px;top:62px;width:404px;height:356px;background:#fbfbfd;border-radius:14px;'
         'box-shadow:0 18px 40px rgba(0,0,0,.35);padding:12px;font-family:Poppins">'
         '<div style="display:flex;gap:8px;margin-bottom:10px;font-size:18px;font-weight:700;color:#334">'
         '<span data-id="tab-emo" style="padding:6px 14px">😊</span><span data-id="tab-gif" style="padding:6px 14px">GIF</span>'
         '<span data-id="tab-kao" style="padding:6px 14px">;-)</span><span data-id="tab-sym" style="padding:6px 14px">Ω</span></div>'
         f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;font-size:34px">{EMOJI}</div></div>')
SPEC = {
    'device': 'laptop', 'lang': 'en', 'voice': 'am_puck', 'speed': 1.0,
    'title': 'Emojis on your PC 😎', 'tag': 'WIN + . · EMOJI PANEL', 'tip': 'TIP #02',
    'start': 'doc', 'start_pops': ['doc:emoji'],                 # result-first: panel open, emoji typed
    'screens': {'doc': {'type': 'window', 'title': 'Notepad', 'text': 'See you at 7 😎', 'focus': 'tab-emo',
                        'pops': {'emoji': PANEL}}},
    'beats': [
        {'say': 'Did you know your PC has a hidden emoji keyboard?', 'cap': 'Your PC has a hidden emoji keyboard 😎',
         'pose': 'welcome', 'hook': True},
        {'say': "Here's how. Click in any text box, like Notepad.", 'cap': "Here's how: click in any text box",
         'pose': 'talk', 'do': [{'hide': 'emoji', 'at': 0}, {'typetext': 'See you at 7 ', 'replace': True, 'from': 0, 'to': .01},
                                {'tap': 'body', 'at': .7}]},
        {'say': 'Step one. Press the Windows key and the period key, together.', 'cap': 'Step 1: Press WIN + . (period)',
         'pose': 'point', 'step': 1, 'do': [{'keys': ['WIN', '.'], 'at': .55, 'hold': 1.8}, {'show': 'emoji', 'at': .75}]},
        {'say': 'Step two. Click any emoji, and it lands right in your text.', 'cap': "Step 2: Click an emoji ✅",
         'pose': 'talk', 'step': 2, 'do': [{'tap': 'e1', 'at': .35}, {'typetext': '😎', 'from': .42, 'to': .44}]},
        {'say': 'It also has GIFs, kaomoji and symbols, on Windows eleven.', 'cap': 'Bonus: GIFs, kaomoji & symbols (Windows 11)',
         'pose': 'welcome', 'do': [{'tap': 'tab-gif', 'at': .25}, {'focus': 'tab-gif', 'at': .27},
                                   {'tap': 'tab-kao', 'at': .5}, {'focus': 'tab-kao', 'at': .52},
                                   {'tap': 'tab-sym', 'at': .75}, {'focus': 'tab-sym', 'at': .77}, {'fx': 'thumb', 'at': .1, 'dur': 2.6}]},
        {'say': 'Follow Tech Wall for more quick tips!', 'cap': 'Follow Tech Wall for more quick tips! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

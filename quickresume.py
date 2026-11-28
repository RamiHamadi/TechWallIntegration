"""Tech Wall HOST episode (TV + console, English): Xbox Series X|S Quick Resume (library #10).
    ./build.sh quickresume  |  python3 quickresume.py 0 200 400
Facts (Xbox Wire, March 2022 Xbox update; Trusted Reviews): Xbox Series X|S keeps several games suspended with Quick
Resume; they are listed in the Quick Resume group in My games & apps; highlight a game, press the Menu button, choose
"Pin to Quick Resume"; up to 2 pinned games, which only drop out if you unpin them or the game takes a required update.
Generic console UI and controller (no brand marks); made-up game tiles. Template hosttv.py."""
import host

EP = 'quickresume'
QR_BADGE = ('<span style="position:absolute;left:8px;top:8px;background:rgba(0,0,0,.55);color:#7CFC9A;border-radius:8px;'
            'padding:2px 8px;font-size:11px;font-weight:800;letter-spacing:.5px">⏸ QUICK RESUME</span>')
GAMES = [('g1', 'Racing', 'linear-gradient(135deg,#ff7a45,#c2185b)', '🏎️'),
         ('g2', 'Space', 'linear-gradient(135deg,#5c6cff,#1b1f6b)', '🚀'),
         ('g3', 'Puzzle', 'linear-gradient(135deg,#ffd54a,#e07b00)', '🧩'),
         ('g4', 'Football', 'linear-gradient(135deg,#34c759,#0b6b2b)', '⚽')]


def tile(tid, label, colour, emoji, badge=True, extra=''):
    return (f'<div class="tile" data-id="{tid}" style="background:{colour};position:relative;flex-direction:column;justify-content:flex-end;'
            f'align-items:flex-start"><span style="position:absolute;left:0;right:0;top:34px;text-align:center;font-size:54px">{emoji}</span>'
            + (QR_BADGE if badge else '') + f'<span>{label}</span>{extra}</div>')


def chome(title, inner, top=''):
    return (f'<div class="chome" style="position:absolute;inset:0">{top}'
            f'<div class="ch-row">{inner}</div><div class="ch-title">{title}</div></div>')


HOME = chome('Home', tile('mygames', 'My games &amp; apps', 'linear-gradient(135deg,#3b4c7a,#1b2440)', '▦', False)
             + ''.join(tile(i, l, c, e, False) for i, l, c, e in GAMES))

PIN = ('<span style="position:absolute;right:-10px;top:-12px;width:46px;height:46px;border-radius:50%;background:#fff;display:grid;'
       'place-items:center;font-size:26px;box-shadow:0 4px 12px rgba(0,0,0,.5);border:3px solid #ffd54a">📌</span>')
QRG = chome('Quick Resume', ''.join(tile(i, l, c, e) for i, l, c, e in GAMES),
            '<div style="position:absolute;left:40px;top:40px;font-size:16px;color:#9fb0d6;letter-spacing:.5px">My games &amp; apps › Groups</div>')
OPTS = ('<div style="position:absolute;left:250px;top:150px;width:360px;background:#1c2748;border-radius:14px;padding:10px;'
        'box-shadow:0 18px 40px rgba(0,0,0,.5);color:#fff">'
        + ''.join(f'<div class="mrow" data-id="opt-{k}">{v}</div>' for k, v in (('manage', 'Manage game and add-ons'),
                                                                               ('pin', '📌 Pin to Quick Resume'), ('quit', 'Quit')))
        + '</div>')
PINS = {'pin1': f'<div style="position:absolute;left:40px;top:110px;width:170px;height:170px;pointer-events:none">{PIN}</div>'}


def game(sky, ground, emoji, hud, resumed=True):
    """A made-up game in progress (frame 0 = racing): sky, track/floor, hero emoji, HUD and a 'Resumed' chip."""
    return (f'<div style="position:absolute;inset:0;background:linear-gradient({sky})"></div>'
            f'<div style="position:absolute;left:-10%;right:-10%;bottom:0;height:46%;background:{ground};'
            'clip-path:polygon(38% 0,62% 0,100% 100%,0 100%)"></div>'
            '<div data-scroll="0,260" style="position:absolute;left:49%;width:2%;bottom:0;height:46%;'
            'background-image:linear-gradient(#fff 50%,transparent 50%);background-size:100% 60px;opacity:.8"></div>'
            f'<div data-bob="4" style="position:absolute;left:0;right:0;bottom:40px;text-align:center;font-size:120px">{emoji}</div>'
            f'<div style="position:absolute;left:24px;top:18px;color:#fff;font-weight:800;font-size:24px;text-shadow:0 2px 6px rgba(0,0,0,.6)">{hud}</div>'
            + ('<div style="position:absolute;right:24px;top:18px;background:rgba(0,0,0,.55);color:#7CFC9A;border-radius:12px;padding:6px 14px;'
               'font-weight:800;font-size:18px">▶ RESUMED · no loading</div>' if resumed else ''))


RACE = game('#2b5bd7,#7cc4ff 60%', 'linear-gradient(#5b5f6b,#2c2f36)', '🏎️', 'LAP 2/3 · 1st 🏁')
SPACE = game('#05061a,#1b1f6b 70%', 'linear-gradient(#2b2f6b,#0b0d2a)', '🚀', 'LEVEL 7 · ⭐ 1,240')
PUZZLE = game('#ffcf6e,#ff8f3a 70%', 'linear-gradient(#8a4b1f,#5a2e0f)', '🧩', 'LEVEL 12 · 3 moves left')

SPEC = {
    'device': 'tv', 'lang': 'en', 'voice': 'am_puck', 'speed': 1.0,
    'title': 'Jump between games instantly 🎮', 'tag': 'XBOX SERIES X|S · QUICK RESUME', 'tip': 'TIP #20',
    'start': 'race',
    'screens': {
        'race': {'type': 'html', 'bg': '#000', 'html': RACE},
        'puzzle': {'type': 'html', 'bg': '#000', 'html': PUZZLE},
        'home': {'type': 'html', 'bg': '#0d1428', 'html': HOME, 'focus': 'g1'},
        'groups': {'type': 'menu', 'path': 'My games & apps', 'title': 'Groups', 'focus': 'full', 'rows': [
            {'id': 'full', 'label': 'Full library', 'icon': 'general', 'color': '#2f6fe0'},
            {'id': 'qr', 'label': 'Quick Resume', 'icon': 'moon', 'color': '#1f9d55', 'value': '4 games'},
            {'id': 'recent', 'label': 'Recently added', 'icon': 'display', 'color': '#2f6fe0'},
            {'id': 'pins', 'label': 'Pins', 'icon': 'general', 'color': '#2f6fe0'}]},
        'qrg': {'type': 'html', 'bg': '#0d1428', 'html': QRG, 'focus': 'g1', 'pops': {'opts': OPTS, **PINS}},
        'space': {'type': 'html', 'bg': '#000', 'html': SPACE},
    },
    'beats': [
        {'say': 'Switch games, and pick up exactly where you left off.', 'cap': 'Switch games, keep your spot 🎮',
         'capsize': 84, 'pose': 'welcome', 'hook': True,
         'do': [{'button': 'a', 'at': .5, 'nav': 'puzzle', 'style': 'zoom'}]},
        {'say': "Here's how, on Xbox Series X and S. Open My games and apps.", 'cap': "Here's how (Xbox Series X|S): My games & apps",
         'pose': 'talk', 'screen': 'home',
         'do': [{'focus': 'mygames', 'button': 'left', 'at': .62}, {'button': 'a', 'at': .86, 'nav': 'groups'}]},
        {'say': 'Then go to Groups, and open Quick Resume.', 'cap': 'Step 1: Groups › Quick Resume', 'pose': 'point', 'step': 1,
         'do': [{'focus': 'qr', 'button': 'down', 'at': .45}, {'button': 'a', 'at': .78, 'nav': 'qrg'}]},
        {'say': "Pick any game, and you're back mid-level, with no loading screen.",
         'cap': "Step 2: pick a game: you're back mid-level, no loading", 'pose': 'point', 'step': 2,
         'do': [{'focus': 'g2', 'button': 'right', 'at': .2}, {'button': 'a', 'at': .42, 'nav': 'space', 'style': 'zoom'}]},
        {'say': 'To keep a game there, press the Menu button, and choose, Pin to Quick Resume.',
         'cap': 'Step 3: Menu button › Pin to Quick Resume 📌', 'pose': 'point', 'step': 3, 'screen': 'qrg', 'style': 'fade',
         'do': [{'focus': 'g1', 'at': .05}, {'button': 'menu', 'at': .42}, {'show': 'opts', 'at': .44},
                {'focus': 'opt-pin', 'button': 'down', 'at': .7}, {'button': 'a', 'at': .86}, {'hide': 'opts', 'at': .88},
                {'show': 'pin1', 'at': .89}]},
        {'say': 'You can pin up to two games. They stay ready until you unpin them, or the game needs an update.',
         'cap': 'Done ✅ Up to 2 pinned games stay ready', 'pose': 'welcome',
         'do': [{'fx': 'thumb', 'at': .05, 'dur': 2.6}, {'fx': 'confetti', 'at': .1}]},
        {'say': 'Follow Tech Wall for more quick tips!', 'cap': 'Follow Tech Wall for more quick tips! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

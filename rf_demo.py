"""Tech Wall — TEST episode for the result-first opening (dummy topic: Back Tap = screenshot, ~25 s).
Frame 0 already shows the payoff (phone from the back, TAP! TAP!, screenshot saved), then "here's how" in 5 taps.
Reuses the Back Tap screens/props from movie.py + movie_blue.py; only the timeline differs.
Build:  ./build.sh rf_demo
"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import movie as m
import movie_blue as mb
from movie import spec, row_point

EP = 'rf_demo'
OUT = __import__('lib').out(f'frames_{EP}')
mb.OUT = OUT


def fig_head(badge):
    if badge.isdigit():
        return f"HERE'S HOW  /  STEP {badge} OF 5"
    return {'H': 'TECH WALL  /  iPHONE TIP', 'ok': 'RESULT  /  OK', 'check': 'RESULT  /  OK',
            '!': 'FIELD TEST', '+': 'BONUS'}[badge]


mb.fig_head = fig_head


def build():
    t = m.TL()
    # 0:00 — result first: phone from the back, double tap, screenshot
    mb.result_first(t, spec('home'), 'H', 'TAP THE BACK OF YOUR iPHONE = SCREENSHOT')
    t.ph['side'] = 'back'
    bx, by = t.s2c(300, 640)
    t.hand = dict(x=bx, y=by, press=False)
    for k in range(2):
        t.press(bx, by, 'knock')
        t.fx.append(('burst', t.f, bx + (-210 if k == 0 else 190), by - 260 + 60 * k, k))
        t.hold(2)
        t.hand['press'] = False
        t.hand['y'] -= 22
        t.hold(2)
        t.hand['y'] += 22
    t.hold(3)
    t.hand_out(3)
    t.flip('front')
    t.sound('shutter')
    for fl in (1.0, 0.55):
        t.ph['flash'] = fl; t.snap()
    t.ph['flash'] = 0.0
    t.ph['thumb'] = 0.0
    for p in (0.0, 0.35, 0.7, 0.9, 1.0):
        t.ph['thumb'] = p; t.snap()
    t.hold(14)
    # 0:03 — here's how
    t.ph['thumb'] = None
    t.cap('1', "Here's how: Settings, then Accessibility", m.MINT)
    t.navigate(spec('settings'))
    t.hold(5)
    t.tap('accessibility', nav=spec('accessibility'), n_move=5)
    t.cap('2', 'Tap Touch', m.SKY)
    t.hold(3)
    t.tap('touch', nav=spec('touch'), n_move=4)
    t.cap('3', 'Scroll down, tap Back Tap', m.PEACH)
    t.hold(3)
    t.swipe(420)
    t.tap('backtap', nav=spec('backtap'), n_move=4)
    t.cap('4', 'Tap Double Tap', m.YELLOW)
    t.hold(3)
    t.tap('double', nav=spec('doubletap', ov={'sel': 'none'}), n_move=4)
    t.cap('5', 'Choose Screenshot', m.PINK)
    t.hold(3)
    t.swipe(300, y=950)
    t.tap('screenshot', ov={'sel': 'screenshot'}, n_move=4)
    t.hold(4)
    t.tap('back', nav=spec('backtap', ov={'dt': 'Screenshot'}), back=True, fx=0.3, n_move=4)
    t.cap('ok', "That's it! Double tap = screenshot", m.MINT)
    t.move_hand(*t.s2c(*row_point(t.ph['spec'], 'double', 0.82)), 4)
    t.hold(18)
    # bonus
    t.cap('+', 'Set Triple Tap to Flashlight', m.SKY)
    t.ph['spec'] = spec('backtap', ov={'dt': 'Screenshot', 'tt': 'Flashlight'}); t.sound('ding')
    t.move_hand(*t.s2c(*row_point(t.ph['spec'], 'triple', 0.82)), 4)
    t.hold(14)
    t.hand_out(3)
    mb.end_card(t)
    return t


if __name__ == '__main__':
    t = build()
    for e in t.fx:
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))
    mb.finish(t, EP, mb.init_props)

"""Tech Wall — SHORT test cut (~19 s) of the iPhone Wi-Fi password episode.
Result-first hook: frame 0 already shows the revealed password, then "here's how" in 3 taps.
Reuses wifi.py screens/props; only the timeline, captions and end-card pacing differ.
Build:  ./build.sh wifi_short
"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import ImageDraw
import movie as m
import movie_blue as mb
import wifi as W
from lib import FPS

OUT = __import__('lib').out('frames_wifi_short')
mb.OUT = OUT
m.TL.cap = mb._cap            # no automatic +0.5 s hold per caption in the short cut

# ---- yellow highlight around the password row (hook + reveal frames)
_detail = W.detail_content


def detail_content(ov, hl):
    img, rows = _detail(ov, hl)
    if ov.get('glow'):
        x0, y0, x1, y1 = rows['password']
        ImageDraw.Draw(img).rounded_rectangle((x0 - 6, y0 - 6, x1 + 6, y1 + 6), 22, outline=mb.YEL, width=7)
    return img, rows


W.detail_content = detail_content


def fig_head(badge):
    return {'H': 'TECH WALL  /  iPHONE TIP', 'how': "HERE'S HOW  /  3 TAPS",
            '1': "HERE'S HOW  /  STEP 1 OF 3", '2': 'STEP 2 OF 3', '3': 'STEP 3 OF 3',
            'ok': 'RESULT  /  OK', 'share': 'TIP  /  SHARE IT', '+': 'BONUS'}[badge]


mb.fig_head = fig_head
spec = W.spec


def build():
    t = m.TL()
    # 0:00 — result first: phone already on screen, password revealed + highlighted
    t.ph['y'] = m.PHY
    t.ph['spec'] = spec('wifidetail', ov={'pw': 'shown', 'glow': True})
    t.cap('H', 'FORGOT YOUR WI-FI PASSWORD?', m.YELLOW)
    t.caps[-1]['inn'] = -4              # already settled on frame 0
    t.snd = [(0, 'pop')]
    t.hold(20)
    # 0:01.7 — rewind to Settings
    t.cap('1', "Here's how: tap Wi-Fi", m.MINT)
    t.navigate(spec('settings'), back=True)
    t.hold(5)
    t.tap('wifi', nav=spec('wifi'), n_move=5)
    t.cap('2', 'Tap the (i) next to your network', m.SKY)
    t.hold(3)
    t.tap('home_i', nav=spec('wifidetail', ov={'pw': 'dots'}), fx=0.5, n_move=4)
    t.cap('3', 'Tap Password, unlock with Face ID', m.PEACH)
    t.hold(3)
    t.tap('password', fx=0.5, n_move=4)
    t.move_hand(t.hand['x'] + 170, t.hand['y'] + 330, 3)
    t.ph['spec']['ov'] = {'pw': 'faceid'}; t.sound('pop'); t.hold(7)
    t.ph['spec']['ov'] = {'pw': 'shown', 'glow': True}; t.sound('ding')
    t.cap('ok', "That's it! Your iPhone knew it all along", m.MINT)
    t.hold(18)
    # share
    t.ph['spec']['ov'] = {'pw': 'shown', 'copy': True}
    t.cap('share', 'Tap Copy to send it to guests', m.YELLOW)
    t.hold(4)
    t.tap('copybtn', fx=0.5, ov={'copy': False}, n_move=4)
    t.fx.append(('burst', t.f, 790, 760, 2)); t.sound('pop')
    t.hold(10)
    # bonus: every saved network
    t.cap('+', 'Tap Edit to see every saved network', m.SKY)
    t.tap('back', nav=spec('wifi'), back=True, fx=0.2, n_move=4)
    t.tap('edit', fx=0.5, n_move=4)
    t.move_hand(t.hand['x'] + 120, t.hand['y'] + 520, 3)
    t.ph['spec']['ov'] = {'faceid': True}; t.sound('pop'); t.hold(6)
    t.ph['spec']['ov'] = {'edit': True}; t.sound('ding')
    t.move_hand(*t.s2c(*W.row_point(t.ph['spec'], 'k3', 0.5)), 4); t.hold(14)
    t.hand_out(3)
    t.cap_off()
    t.phone_to(2700, 4)
    t.fx.append(('end', t.f)); t.hold(40)
    return t


# ---- faster end card (everything in within ~1.4 s, then hold)
END_SEQ = [('e_head', 540, 300, 1)] + \
    [(('chip', i), [470, 600, 470, 600][i], 560 + 185 * i, 3 + 2 * i) for i in range(4)] + \
    [(('arrow', i), (190, 950, 190)[i], 652 + 185 * i, 4 + 2 * i) for i in range(3)] + \
    [('e_s1', 540, 1340, 12), ('e_s2', 540, 1470, 14), ('e_s3', 540, 1640, 16)]


def draw_end(cv, f, a):
    P = m.P
    for key, x, y, off in END_SEQ:
        yy = m.drop_y(f, a + off, y)
        if yy is None:
            continue
        if isinstance(key, tuple):
            sp = P['e_chips'][key[1]] if key[0] == 'chip' else P['e_arrows'][key[1]]
        else:
            sp = P[key]
        m.put(cv, sp, x, yy, f, key)


m.draw_end = draw_end

# ---- persistent "YOUR PASSWORD" tag while the revealed password is on screen
_fx = m.draw_fx


def draw_fx(cv, f, fxs):
    _fx(cv, f, fxs)
    sp = m.TLD['frames'][f]['ph']['spec']
    if sp['name'] == 'wifidetail' and sp['ov'].get('glow') and not m.TLD['frames'][f]['ph']['trans']:
        if 'pwtag' not in m.P:
            import themes as th
            m.P['pwtag'] = mb.label('YOUR PASSWORD', th.JB(800, 46), bg=mb.YEL, tape=False, rot=-5, padx=26, pady=12)
        m.put(cv, m.P['pwtag'], 800, 1000, f, 'pwtag')


m.draw_fx = draw_fx


def add_sounds(t):
    for e in t.fx:
        if e[0] == 'end':
            for key, x, y, off in END_SEQ:
                if not (isinstance(key, tuple) and key[0] == 'arrow'):
                    t.snd.append((e[1] + off, 'pop'))


if __name__ == '__main__':
    t = build()
    add_sounds(t)
    m.TLD = dict(frames=t.frames, fx=t.fx, caps=t.caps, snd=t.snd)
    n = len(t.frames)
    print('frames', n, 'seconds', round(n / FPS, 2), flush=True)
    for c in t.caps:
        print(f"{max(0, c['inn']) / FPS:5.1f}s  {c['text']}")
    os.makedirs(OUT, exist_ok=True)
    W.init_props()
    only = [int(a) for a in sys.argv[1:]]
    if only:
        for f in only:
            if f < n:
                mb.render(f)
    else:
        with Pool(2) as pool:
            for i, _ in enumerate(pool.imap(mb.render, range(n), chunksize=8)):
                if i % 100 == 0:
                    print('rendered', i, flush=True)
        m.make_audio(m.TLD, n, __import__('lib').out('audio_wifi_short.wav'))

"""Tech Wall — #7 re-cut with the short-form structure: Hook -> Lead -> 3 quick points -> CTA, looping (~16 s).
Hook (0-2 s): surprising claim on frame 0 with the three switches ON, they flip OFF (the payoff).
Lead (2-4 s): the promise, "3 switches, 10 seconds", the chat bubble bounces off the padlock.
Points (4-13 s): one cut per app, a new picture every 2-3 s, one click each.
CTA (13-16 s): specific ("Save this, then comment: which AI do you use?") on the same three-panel screen the
video opens with, so the replay flows straight back into the hook (loop). No end card (it would be padding).
Screens, rig and render come from aitrain.py.
Build:  ./build.sh aitrain2
"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
import movie as m
import movie_blue as mb
from lib import FPS
import aitrain as AT
from aitrain import TL, SW

EP = 'aitrain2'
AT.OUT = __import__('lib').out(f'frames_{EP}')


def build():
    t = TL()
    # HOOK — frame 0: surprising claim, all three switches ON; they flip OFF (payoff) within ~1.5 s
    t.cur['scr'] = dict(view='triple', off=0, glow=False)
    t.cap('TECH WALL  /  AI TIP', 'YOUR AI CHATS MAY BE TRAINING THE AI')
    t.caps[-1]['inn'] = -4
    t.snd = [(0, 'pop')]
    t.hold(9)
    for k in (1, 2, 3):
        t.scr(off=k); t.sound('tap'); t.hold(3)
    t.scr(glow=True); t.sound('ding'); t.hold(8)
    # LEAD — the promise + a new picture
    t.cap('3 SWITCHES  /  10 SECONDS', '3 switches, 10 seconds:')
    t.cur['scr'] = dict(view='proof', p=0); t.sound('swish')
    for p in (.2, .45, .66, .8, .62, .5):
        t.scr(p=p); t.snap()
    t.sound('knock'); t.fx.append(('burst', t.f, 800, 640, 0)); t.hold(16)
    # POINT 1 — ChatGPT (straight to the right page, one click)
    t.cap('SWITCH 1 OF 3', 'ChatGPT > Data controls')
    t.cur['scr'] = dict(view='gpt', nav='data', on=True); t.sound('swish'); t.hold(8)
    t.click_row('tog', lambda: (t.scr(on=False), t.sound('ding')), n=3)
    t.cursor_to(SW - 260, 360, 3); t.hold(11)
    # POINT 2 — Claude
    t.cap('SWITCH 2 OF 3', 'Claude > Privacy')
    t.cur['scr'] = dict(view='claude', nav='privacy', on=True); t.sound('swish'); t.hold(8)
    t.click_row('tog', lambda: (t.scr(on=False), t.sound('ding')), n=3)
    t.cursor_to(SW - 260, 360, 3); t.hold(11)
    # POINT 3 — Gemini (Keep Activity: On -> Turn off)
    t.cap('SWITCH 3 OF 3', 'Gemini > Activity')
    t.cur['scr'] = dict(view='gemini', stage='activity', keep='On'); t.sound('swish'); t.hold(6)
    t.click_row('btn', lambda: t.scr(stage='drop'), n=3)
    t.hold(2)
    t.click_row('d0', lambda: (t.scr(stage='activity', keep='Off'), t.sound('ding')), n=3)
    t.cursor_to(SW - 120, 380, 3); t.hold(15)
    # CTA — on the opening screen (switches now OFF), so the loop restarts cleanly into the hook
    t.cap('SAVE THIS  /  FOR LATER', 'Save this, then comment: which AI do you use?')
    t.cur['scr'] = dict(view='triple', off=3, glow=True); t.cur['cursor'] = None; t.sound('swish')
    t.hold(40)
    return t


if __name__ == '__main__':
    t = build()
    for e in t.fx:
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))
    AT.TLD = dict(frames=t.frames, fx=t.fx, caps=t.caps, snd=t.snd)
    n = len(t.frames)
    print('frames', n, 'seconds', round(n / FPS, 2), flush=True)
    for c in t.caps:
        print(f"{max(0, c['inn']) / FPS:5.1f}s  {c['text']}")
    os.makedirs(AT.OUT, exist_ok=True)
    AT.init_props()
    mb.write_meta(EP, 0)
    only = [int(a) for a in sys.argv[1:]]
    if only:
        for f in only:
            if f < n:
                AT.render(f)
    else:
        with Pool(2) as pool:
            for i, _ in enumerate(pool.imap(AT.render, range(n), chunksize=8)):
                if i % 100 == 0:
                    print('rendered', i, flush=True)
        m.make_audio(AT.TLD, n, __import__('lib').out(f'audio_{EP}.wav'))

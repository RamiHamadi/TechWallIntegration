"""Tech Wall — AI tip: stop ChatGPT, Claude and Gemini from training on your chats (laptop), result-first (~28 s).
Frame 0 shows the payoff (three settings panels, every switch OFF) with the hook; a chat bubble bounces off a
padlock as proof; then one step per app with the mouse, a Temporary/Incognito bonus and the fast end card.
PC rig (monitor + keyboard + cursor) from winv.py / emoji.py; app screens are generic look-alikes (names as text,
no logos). Paths verified 2026-10-06 on help.openai.com, Anthropic help/Tom's Guide, support.google.com/gemini.
Build:  ./build.sh aitrain
"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter
import movie as m
import movie_blue as mb
import themes as th
from movie_blue import label, center_label, path_label, chalk_arrow, dashed_ring, NAVY, MID, YEL, PAPER
from lib import F, rotate_sprite, rng_for, FPS, ease, jit, draw_sprite, blit, apply_tex, paper_tex
import winv as wv
import emoji as E
from emoji import keyboard_raw, key_sprite, ACTIVE, key_center
from winv import MON_W, MON_RAW_H, SW, SH, MONX, MONY, KBX, KBY, scr_origin, monitor_raw, cursor_sprite, wallpaper

EP = 'aitrain'
OUT = __import__('lib').out(f'frames_{EP}')
TXT, SUB, LINE = (28, 30, 40), (110, 114, 128), (226, 228, 236)
GREEN, OFFG = (52, 168, 83), (196, 198, 206)
APPS = [('ChatGPT', 'Improve the model', 'for everyone'), ('Claude', 'Help improve', 'Claude'), ('Gemini', 'Keep Activity', '(Gemini Apps)')]


# ======================================================================= screen helpers
def switch(d, x, cy, on, s=1.0):
    w, h = 74 * s, 40 * s
    d.rounded_rectangle((x, cy - h / 2, x + w, cy + h / 2), h / 2, fill=GREEN if on else OFFG)
    kx = x + w - h / 2 if on else x + h / 2
    d.ellipse((kx - h / 2 + 4, cy - h / 2 + 4, kx + h / 2 - 4, cy + h / 2 - 4), fill=(255, 255, 255))


def padlock(d, cx, cy, s=1.0, col=NAVY):
    d.rounded_rectangle((cx - 18 * s, cy - 4 * s, cx + 18 * s, cy + 24 * s), int(5 * s), fill=col)
    d.arc((cx - 12 * s, cy - 24 * s, cx + 12 * s, cy + 6 * s), 180, 360, fill=col, width=max(3, int(5 * s)))


def window(im, title, side=None):
    """generic app window filling the screen; returns draw + content origin"""
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((16, 14, SW - 16, SH - 54), 14, fill=(252, 252, 254), outline=(200, 205, 215), width=2)
    d.rounded_rectangle((16, 14, SW - 16, 58), 14, fill=(236, 238, 244)); d.rectangle((16, 44, SW - 16, 58), fill=(236, 238, 244))
    d.text((40, 36), title, font=F(600, 22), fill=(60, 64, 80), anchor='lm')
    for i, x in enumerate((SW - 104, SW - 72, SW - 40)):
        if i == 0:
            d.line([(x - 7, 36), (x + 7, 36)], fill=(80, 80, 90), width=2)
        elif i == 1:
            d.rectangle((x - 7, 29, x + 7, 43), outline=(80, 80, 90), width=2)
        else:
            d.line([(x - 7, 29), (x + 7, 43)], fill=(80, 80, 90), width=2); d.line([(x - 7, 43), (x + 7, 29)], fill=(80, 80, 90), width=2)
    return d


def taskbar(im):
    d = ImageDraw.Draw(im)
    d.rectangle((0, SH - 46, SW, SH), fill=(232, 236, 244))
    for i in range(5):
        x = SW / 2 - 110 + i * 48
        d.rounded_rectangle((x, SH - 37, x + 30, SH - 9), 7, fill=[(0, 103, 192), (255, 185, 0), (90, 90, 100), (16, 160, 110), (220, 70, 70)][i])
    d.text((SW - 20, SH - 23), '9:41', font=th.JB(600, 18), fill=(40, 40, 50), anchor='rm')


def nav_list(d, items, sel, hl, x0=30, y0=96, w=230, rh=52):
    rows = {}
    for i, (rid, lab) in enumerate(items):
        y = y0 + i * rh
        if rid == sel:
            d.rounded_rectangle((x0, y, x0 + w, y + rh - 8), 10, fill=(226, 232, 246))
        if rid == hl:
            d.rounded_rectangle((x0, y, x0 + w, y + rh - 8), 10, outline=YEL, width=3)
        d.text((x0 + 16, y + (rh - 8) / 2), lab, font=F(600 if rid == sel else 500, 23), fill=TXT, anchor='lm')
        rows[rid] = (x0, y, x0 + w, y + rh - 8)
    return rows


# ======================================================================= screens
ROWS = {}


def triple_screen(s):
    im = wallpaper(); d = ImageDraw.Draw(im)
    for i, (name, l1, l2) in enumerate(APPS):
        x0 = 22 + i * 274; x1 = x0 + 262
        d.rounded_rectangle((x0, 22, x1, SH - 60), 18, fill=(252, 252, 254), outline=YEL if s.get('glow') else (210, 214, 224),
                            width=5 if s.get('glow') else 2)
        cx = (x0 + x1) / 2
        d.text((cx, 74), name, font=F(600, 36), fill=TXT, anchor='mm')
        d.line([(x0 + 24, 110), (x1 - 24, 110)], fill=LINE, width=2)
        d.text((cx, 156), l1, font=F(500, 25), fill=TXT, anchor='mm')
        d.text((cx, 190), l2, font=F(500, 25), fill=TXT, anchor='mm')
        on = i >= s.get('off', 3)
        switch(d, cx - 56, 272, on, 1.5)
        d.text((cx, 334), 'ON' if on else 'OFF', font=F(600, 34), fill=GREEN if on else (200, 60, 60), anchor='mm')
        if not on:
            padlock(d, cx, 390, 1.1)
    taskbar(im)
    return im


def proof_screen(s):
    im = wallpaper(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((SW - 250, 150, SW - 40, 330), 18, fill=(40, 46, 70))
    d.text((SW - 145, 210), 'AI', font=F(600, 40), fill=(255, 255, 255), anchor='mm')
    d.text((SW - 145, 262), 'TRAINING', font=F(600, 28), fill=(200, 210, 235), anchor='mm')
    bx = 40 + 360 * s.get('p', 0)
    d.rounded_rectangle((bx, 180, bx + 220, 270), 24, fill=(255, 255, 255))
    d.polygon([(bx + 30, 266), (bx + 20, 300), (bx + 64, 266)], fill=(255, 255, 255))
    d.text((bx + 110, 210), 'My private', font=F(500, 25), fill=TXT, anchor='mm')
    d.text((bx + 110, 244), 'question...', font=F(500, 25), fill=TXT, anchor='mm')
    d.rounded_rectangle((SW - 300, 120, SW - 278, 360), 10, fill=YEL)
    padlock(d, SW - 289, 224, 1.7)
    taskbar(im)
    return im


def gpt_screen(s):
    im = wallpaper(); d = window(im, 'ChatGPT  ·  Settings')
    hl = s.get('hl')
    ROWS['gpt'] = nav_list(d, [('general', 'General'), ('notif', 'Notifications'), ('pers', 'Personalization'),
                               ('data', 'Data controls'), ('security', 'Security'), ('account', 'Account')], s.get('nav'), hl)
    d.line([(280, 76), (280, SH - 70)], fill=LINE, width=2)
    if s.get('nav') == 'data':
        d.text((304, 104), 'Data controls', font=F(600, 30), fill=TXT, anchor='lm')
        y = 170
        d.text((304, y), 'Improve the model', font=F(500, 25), fill=TXT, anchor='lm')
        d.text((304, y + 32), 'for everyone', font=F(500, 25), fill=TXT, anchor='lm')
        if hl == 'tog':
            d.rounded_rectangle((SW - 150, y - 10, SW - 46, y + 46), 14, outline=YEL, width=3)
        switch(d, SW - 136, y + 16, s.get('on', True))
        ROWS['gpt']['tog'] = (SW - 150, y - 10, SW - 46, y + 46)
        d.line([(304, y + 70), (SW - 40, y + 70)], fill=LINE, width=2)
        d.text((304, y + 106), 'Shared links', font=F(500, 25), fill=TXT, anchor='lm')
        d.text((304, y + 162), 'Export data', font=F(500, 25), fill=TXT, anchor='lm')
    else:
        d.text((304, 104), 'General', font=F(600, 30), fill=TXT, anchor='lm')
        for i, lab in enumerate(['Theme', 'Language', 'Voice']):
            d.text((304, 170 + i * 56), lab, font=F(500, 25), fill=TXT, anchor='lm')
            d.text((SW - 50, 170 + i * 56), ['System', 'Auto-detect', 'Default'][i], font=F(400, 23), fill=SUB, anchor='rm')
    taskbar(im)
    return im


def claude_screen(s):
    im = wallpaper(); d = window(im, 'Claude  ·  Settings')
    hl = s.get('hl')
    ROWS['claude'] = nav_list(d, [('profile', 'Profile'), ('appear', 'Appearance'), ('account', 'Account'),
                                  ('privacy', 'Privacy'), ('billing', 'Billing')], s.get('nav'), hl)
    d.line([(280, 76), (280, SH - 70)], fill=LINE, width=2)
    if s.get('nav') == 'privacy':
        d.text((304, 104), 'Privacy', font=F(600, 30), fill=TXT, anchor='lm')
        y = 170
        d.text((304, y + 14), 'Help improve Claude', font=F(500, 25), fill=TXT, anchor='lm')
        if hl == 'tog':
            d.rounded_rectangle((SW - 150, y - 10, SW - 46, y + 46), 14, outline=YEL, width=3)
        switch(d, SW - 136, y + 16, s.get('on', True))
        ROWS['claude']['tog'] = (SW - 150, y - 10, SW - 46, y + 46)
        d.text((304, y + 56), 'Allow chats to train future models', font=F(400, 20), fill=SUB, anchor='lm')
        d.line([(304, y + 90), (SW - 40, y + 90)], fill=LINE, width=2)
        d.text((304, y + 126), 'Export data', font=F(500, 25), fill=TXT, anchor='lm')
    else:
        d.text((304, 104), 'Profile', font=F(600, 30), fill=TXT, anchor='lm')
        d.text((304, 170), 'Full name', font=F(500, 25), fill=TXT, anchor='lm')
        d.text((SW - 50, 170), 'Sam', font=F(400, 23), fill=SUB, anchor='rm')
    taskbar(im)
    return im


def gemini_screen(s):
    im = wallpaper(); d = window(im, 'Gemini')
    hl = s.get('hl'); rows = {}
    stage = s.get('stage', 'home')
    d.rectangle((18, 60, 250, SH - 56), fill=(240, 243, 250))
    for i, lab in enumerate(['New chat', 'Recent', 'Gems']):
        d.text((40, 100 + i * 48), lab, font=F(500, 23), fill=TXT, anchor='lm')
    sy = SH - 100
    if hl == 'settings':
        d.rounded_rectangle((26, sy - 24, 242, sy + 24), 10, outline=YEL, width=3)
    d.text((44, sy), 'Settings & help', font=F(600, 23), fill=TXT, anchor='lm')
    rows['settings'] = (26, sy - 24, 242, sy + 24)
    if stage in ('home', 'menu'):
        d.text((520, 200), 'Hello, Sam', font=F(600, 40), fill=TXT, anchor='mm')
        d.rounded_rectangle((300, 300, SW - 40, 352), 26, fill=(240, 243, 250))
        d.text((326, 326), 'Ask Gemini', font=F(400, 23), fill=SUB, anchor='lm')
    if stage == 'menu':
        x0, y0 = 40, SH - 290
        d.rounded_rectangle((x0, y0, x0 + 260, y0 + 160), 14, fill=(255, 255, 255), outline=(210, 214, 224), width=2)
        for i, lab in enumerate(['Activity', 'Saved info', 'Settings']):
            yy = y0 + 30 + i * 50
            if hl == f'm{i}':
                d.rounded_rectangle((x0 + 8, yy - 22, x0 + 252, yy + 22), 10, outline=YEL, width=3)
            d.text((x0 + 26, yy), lab, font=F(500, 24), fill=TXT, anchor='lm')
            rows[f'm{i}'] = (x0 + 8, yy - 22, x0 + 252, yy + 22)
    if stage in ('activity', 'drop'):
        d.text((290, 104), 'Gemini Apps Activity', font=F(600, 30), fill=TXT, anchor='lm')
        keep = s.get('keep', 'On')
        d.text((290, 170), 'Keep Activity', font=F(500, 26), fill=TXT, anchor='lm')
        bx = SW - 190
        if hl == 'btn':
            d.rounded_rectangle((bx - 6, 146, bx + 156, 196), 24, outline=YEL, width=3)
        d.rounded_rectangle((bx, 150, bx + 150, 192), 21, fill=(226, 232, 246) if keep == 'On' else (250, 230, 230))
        d.text((bx + 64, 171), keep, font=F(600, 24), fill=TXT, anchor='mm')
        d.polygon([(bx + 112, 166), (bx + 128, 166), (bx + 120, 176)], fill=TXT)
        rows['btn'] = (bx, 150, bx + 150, 192)
        d.text((290, 232), 'Off: chats are not saved to your account', font=F(400, 20), fill=SUB, anchor='lm')
        d.text((290, 262), '(kept up to 72 h) and not used to train AI.', font=F(400, 20), fill=SUB, anchor='lm')
        d.text((290, 292), 'Note: this also turns off chat history.', font=F(600, 20), fill=(190, 70, 50), anchor='lm')
        if stage == 'drop':
            x0, y0 = SW - 330, 200
            d.rounded_rectangle((x0, y0, x0 + 290, y0 + 110), 14, fill=(255, 255, 255), outline=(210, 214, 224), width=2)
            for i, lab in enumerate(['Turn off', 'Turn off and delete activity']):
                yy = y0 + 30 + i * 50
                if hl == f'd{i}':
                    d.rounded_rectangle((x0 + 8, yy - 22, x0 + 282, yy + 22), 10, outline=YEL, width=3)
                d.text((x0 + 24, yy), lab, font=F(500, 22), fill=TXT, anchor='lm')
                rows[f'd{i}'] = (x0 + 8, yy - 22, x0 + 282, yy + 22)
    ROWS['gemini'] = rows
    taskbar(im)
    return im


def temp_screen(s):
    im = wallpaper(); d = window(im, 'ChatGPT')
    hl = s.get('hl')
    bx = SW - 230
    if hl == 'temp':
        d.rounded_rectangle((bx - 6, 74, bx + 196, 124), 24, outline=YEL, width=3)
    d.rounded_rectangle((bx, 78, bx + 190, 120), 21, fill=(40, 46, 70) if s.get('temp') else (236, 238, 244))
    d.text((bx + 95, 99), 'Temporary', font=F(600, 22), fill=(255, 255, 255) if s.get('temp') else TXT, anchor='mm')
    ROWS['temp'] = {'temp': (bx, 78, bx + 190, 120)}
    if s.get('temp'):
        d.text((SW / 2, 220), 'Temporary Chat', font=F(600, 38), fill=TXT, anchor='mm')
        d.text((SW / 2, 272), "Won't appear in history", font=F(500, 24), fill=SUB, anchor='mm')
        d.text((SW / 2, 306), "or be used to train models", font=F(500, 24), fill=SUB, anchor='mm')
    else:
        d.text((SW / 2, 240), 'What can I help with?', font=F(600, 36), fill=TXT, anchor='mm')
    d.rounded_rectangle((90, 360, SW - 90, 412), 26, fill=(240, 243, 250))
    d.text((116, 386), 'Ask anything', font=F(400, 23), fill=SUB, anchor='lm')
    taskbar(im)
    return im


SCREENS = {'triple': triple_screen, 'proof': proof_screen, 'gpt': gpt_screen, 'claude': claude_screen,
           'gemini': gemini_screen, 'temp': temp_screen}
_sc = {}


def render_screen(s):
    key = repr(sorted(s.items()))
    if key not in _sc:
        if len(_sc) > 30:
            _sc.clear()
        _sc[key] = SCREENS[s['view']](s)
    return _sc[key].copy()


def pt(s, rid):
    """screen point of a clickable row on screen spec s"""
    SCREENS[s['view']](s)
    x0, y0, x1, y1 = ROWS[{'temp': 'temp'}.get(s['view'], s['view'])][rid]
    return (x0 + x1) / 2, (y0 + y1) / 2


# ======================================================================= timeline
class TL(E.TL):
    def __init__(s):
        super().__init__()
        s.cur['scr'] = dict(view='triple', off=3, glow=True)
        s.cur['mon_dy'] = 0; s.cur['kb_dy'] = 0

    def click_row(s, rid, after, n=4):
        x, y = pt(s.cur['scr'], rid)
        s.cursor_to(x, y, n)
        s.scr(hl=rid); s.hold(1)
        s.click(lambda: (s.scr(hl=None), after()))


def build():
    t = TL()
    # 0:00 — result first: all three switches OFF
    t.cap('TECH WALL  /  AI TIP', 'YOUR CHATS MAY TRAIN AI: TURN THIS OFF')
    t.caps[-1]['inn'] = -4
    t.snd = [(0, 'pop')]
    t.hold(16)
    # proof: a private chat bounces off the padlock
    t.cur['scr'] = dict(view='proof', p=0); t.sound('swish')
    for p in (.15, .35, .55, .72, .8, .62, .5):
        t.scr(p=p); t.snap()
    t.sound('knock'); t.fx.append(('burst', t.f, 800, 640, 0)); t.hold(14)
    # step 1 — ChatGPT
    t.cap("HERE'S HOW  /  STEP 1 OF 3", 'ChatGPT: open Settings, then Data controls')
    t.cur['scr'] = dict(view='gpt', nav='general', on=True); t.sound('swish'); t.hold(10)
    t.click_row('data', lambda: t.scr(nav='data'))
    t.hold(6)
    t.click_row('tog', lambda: (t.scr(on=False), t.sound('ding')))
    t.cursor_to(SW - 260, 360, 3)
    t.hold(8)
    # step 2 — Claude
    t.cap("HERE'S HOW  /  STEP 2 OF 3", 'Claude: open Settings, then Privacy')
    t.cur['scr'] = dict(view='claude', nav='profile', on=True); t.sound('swish'); t.hold(10)
    t.click_row('privacy', lambda: t.scr(nav='privacy'))
    t.hold(6)
    t.click_row('tog', lambda: (t.scr(on=False), t.sound('ding')))
    t.cursor_to(SW - 260, 360, 3)
    t.hold(8)
    # step 3 — Gemini
    t.cap("HERE'S HOW  /  STEP 3 OF 3", 'Gemini: Settings & help, then Activity')
    t.cur['scr'] = dict(view='gemini', stage='home'); t.sound('swish'); t.hold(8)
    t.click_row('settings', lambda: t.scr(stage='menu'))
    t.hold(3)
    t.click_row('m0', lambda: t.scr(stage='activity', keep='On'))
    t.hold(8)
    t.click_row('btn', lambda: t.scr(stage='drop'))
    t.hold(3)
    t.click_row('d0', lambda: (t.scr(stage='activity', keep='Off'), t.sound('ding')))
    t.cursor_to(SW - 120, 380, 3)
    t.hold(14)
    # result
    t.cap('RESULT  /  OK', "Your new chats won't train the AI")
    t.cur['scr'] = dict(view='triple', off=3, glow=True); t.cur['cursor'] = None; t.sound('swish')
    t.hold(24)
    # bonus — one private chat
    t.cap('BONUS', 'Private chat? Use Temporary or Incognito')
    t.cur['scr'] = dict(view='temp', temp=False); t.sound('swish'); t.hold(8)
    t.click_row('temp', lambda: (t.scr(temp=True), t.sound('ding')))
    t.hold(24)
    # end
    t.cap_off()
    t.cur['cursor'] = None
    t.sound('whoosh')
    for i in range(1, 5):
        e = ease(i / 4); t.cur['mon_dy'] = -1600 * e; t.cur['kb_dy'] = 1000 * e; t.snap()
    a = t.f
    t.fx.append(('end', a))
    for key, x, y, off in mb.FAST_END:
        if not (isinstance(key, tuple) and key[0] == 'arrow'):
            t.snd.append((a + off, 'pop'))
    t.hold(40)
    return t


# ======================================================================= render
P = {}
TLD = None


def init_props():
    P['bg'] = th.bg_blue(with_dims=False)
    P['mon'] = th.sprite(monitor_raw(), border=8, off=(16, 22), blur=14, op=.42)
    P['kb'] = th.sprite(keyboard_raw(), border=8, off=(12, 18), blur=12, op=.42)
    P['keys'] = {(k, p): key_sprite(k, p, p) for k in ACTIVE for p in (False, True)}
    P['cursor'], P['ctip'] = cursor_sprite()
    P['rings'] = [dashed_ring(r, YEL, w) for r, w in [(30, 8), (50, 7), (70, 5)]]
    P['notes'] = {}
    P['bursts'] = [label('PRIVATE!', th.JB(800, 64), bg=YEL, tape=True, rot=-7, padx=30, pady=12)]
    P['e_head'] = center_label('SAVE THIS TIP', th.JB(800, 92), rot=-2.5, padx=56, pady=30)
    P['e_chips'] = [rotate_sprite(path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('ChatGPT: Data controls', (16, 140, 100), 'gear', -2), ('Claude: Privacy', (200, 110, 70), 'gear', 1.5),
        ('Gemini: Activity', (66, 133, 244), 'gear', -1.5), ('Switch it OFF', NAVY, 'touch', 2)])]
    P['e_arrows'] = [chalk_arrow(r) for r in (14, -14, 14)]
    P['e_s1'] = center_label('APPLIES TO YOUR WHOLE ACCOUNT', th.JB(800, 42), bg=YEL, rot=-1.5)
    P['e_s2'] = center_label("PAST CHATS AREN'T AFFECTED", th.JB(800, 42), rot=1.5)
    P['e_s3'] = center_label('Gemini: this also turns off chat history', th.JB(600, 32), fg=MID, rot=-1, pady=18)
    P['e_follow'] = center_label('FOLLOW  TECH WALL', th.JB(800, 40), bg=YEL, rot=1, pady=18)


wv.P = P
put = wv.put
draw_caps = wv.draw_caps


def draw_end(cv, f, a):
    for key, x, y, off in mb.FAST_END:
        yy = m.drop_y(f, a + off, y)
        if yy is None:
            continue
        if isinstance(key, tuple):
            sp = P['e_chips'][key[1]] if key[0] == 'chip' else P['e_arrows'][key[1]]
        else:
            sp = P[key]
        put(cv, sp, x, yy, f, key)


_stex = None


def render(f):
    global _stex
    tl = TLD
    st = tl['frames'][f]
    cv = P['bg'].copy()
    for e in tl['fx']:
        if e[0] == 'end' and f >= e[1]:
            draw_end(cv, f, e[1])
    if st['kb_dy'] < 850:
        jx, jy = jit(f, 'kb', 1.2)
        draw_sprite(cv, P['kb'], KBX + jx, KBY + st['kb_dy'] + jy)
        for k in ACTIVE:
            cx, cy = key_center(k)
            draw_sprite(cv, P['keys'][(k, False)], cx + jx, cy + st['kb_dy'] + jy)
    if st['mon_dy'] > -1450:
        mx, my = MONX, MONY + st['mon_dy']
        jx, jy = jit(f, 'mon', 1.2)
        sh, body = P['mon']
        body = body.copy()
        scr = render_screen(st['scr'])
        if _stex is None:
            _stex = paper_tex(SW, SH, seed=77, strength=.7)
        scr = apply_tex(scr, _stex)
        ox = (body.width - MON_W) // 2 + 24; oy = (body.height - MON_RAW_H) // 2 + 24
        mask = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, SW - 1, SH - 1), 10, fill=255)
        body.paste(scr, (ox, oy), mask)
        draw_sprite(cv, (sh, body), mx + jx, my + jy)
        c = st['cursor']
        if c:
            sx0, sy0 = scr_origin(st['mon_dy'])
            csh, cbody = P['cursor']
            pad_ = (cbody.width - 60) // 2
            x = sx0 + c['x'] + jx - (pad_ + 4) + (2 if c['p'] else 0)
            y = sy0 + c['y'] + jy - ((cbody.height - 84) // 2 + 4) + (2 if c['p'] else 0)
            blit(cv, csh, x, y); blit(cv, cbody, x, y)
    for e in tl['fx']:
        k = f - e[1]
        if e[0] == 'ring' and 0 <= k < 3:
            put(cv, P['rings'][k], e[2], e[3], f, 'ring', .5)
        elif e[0] == 'burst' and 0 <= k < 12:
            sc = {0: 0.5, 1: 1.08}.get(k, 1.0)
            sp = P['bursts'][e[4]]
            if sc != 1.0:
                sp = tuple(s_.resize((int(s_.width * sc), int(s_.height * sc)), Image.BILINEAR) for s_ in sp)
            put(cv, sp, e[2], e[3], f, ('burst', e[1]))
    draw_caps(cv, f, tl['caps'])
    k = 1 + rng_for(f, 'flicker').uniform(-0.016, 0.016)
    out = cv.convert('RGB').point(lambda v: min(255, int(v * k)))
    out.save(f'{OUT}/{f:05d}.png', compress_level=1)
    return f


if __name__ == '__main__':
    t = build()
    for e in t.fx:
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))
    TLD = dict(frames=t.frames, fx=t.fx, caps=t.caps, snd=t.snd)
    n = len(t.frames)
    print('frames', n, 'seconds', round(n / FPS, 2), flush=True)
    for c in t.caps:
        print(f"{max(0, c['inn']) / FPS:5.1f}s  {c['text']}")
    os.makedirs(OUT, exist_ok=True)
    init_props()
    mb.write_meta(EP, 0)
    only = [int(a) for a in sys.argv[1:]]
    if only:
        for f in only:
            if f < n:
                render(f)
    else:
        with Pool(2) as pool:
            for i, _ in enumerate(pool.imap(render, range(n), chunksize=8)):
                if i % 100 == 0:
                    print('rendered', i, flush=True)
        m.make_audio(TLD, n, __import__('lib').out(f'audio_{EP}.wav'))

"""Tech Wall ep.7 — Windows emoji panel (WIN + .) — Blueprint stop-motion (PC rig from winv.py)"""
import sys, os, copy
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import movie as m
import themes as th
from movie_blue import label, center_label, path_label, chalk_arrow, dashed_ring, NAVY, MID, YEL, PAPER
from lib import rotate_sprite, rng_for, FPS, ease, jit, draw_sprite, blit, apply_tex, paper_tex
import winv as wv
from winv import (MON_W, MON_RAW_H, SW, SH, MONX, MONY, KBX, KBY, KB_W, KB_H, HIDE, BLUEW, scr_origin, monitor_raw,
                  draw_key, cursor_sprite, wallpaper)

OUT = __import__('lib').out('frames_emoji')

# ------------------------------------------------------------------ keyboard: winv layout + , and .
KEYS = dict(wv.KEYS)
KEYS.update({',': (130 + 7 * 88, 210, 78), '.': (130 + 8 * 88, 210, 78)})
ACTIVE = ['WIN', '.', 'P', 'I', 'Z', 'A']
KLAB = dict(wv.KLAB)


def key_center(k):
    x, y, w = KEYS[k]
    return KBX - KB_W / 2 + x + w / 2, KBY - KB_H / 2 + y + 37


def keyboard_raw():
    im = Image.new('RGBA', (KB_W, KB_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, KB_W, KB_H), 34, fill=(214, 218, 228))
    d.rounded_rectangle((8, 8, KB_W - 8, KB_H - 8), 28, outline=(190, 196, 210), width=3)
    for k, (x, y, w) in KEYS.items():
        if k in ACTIVE:
            continue
        draw_key(d, x, y, w, KLAB.get(k, k), False)
    return im


def key_sprite(k, pressed, hl):
    x, y, w = KEYS[k]
    im = Image.new('RGBA', (w + 4, 80), (0, 0, 0, 0))
    draw_key(ImageDraw.Draw(im), 2, 2, w, KLAB.get(k, k), pressed, hl)
    return th.sprite(im, border=0, off=(2, 3) if pressed else (4, 6), blur=2 if pressed else 4, op=.35, tex=True, tex_strength=.5)


# ------------------------------------------------------------------ emoji + text helpers
EMOJI_FONT = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'   # OFL; apt: fonts-noto-color-emoji
SYM_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
_emo = {}


def emo(ch, size):
    k = (ch, size)
    if k not in _emo:
        f = ImageFont.truetype(EMOJI_FONT, 109)
        im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        im = im.crop(im.getbbox())
        sc = size / max(im.size)
        _emo[k] = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    return _emo[k]


def is_emo(ch):
    return ord(ch) > 0x2400


def rich(im, x, cy, text, font, fill):
    """draw text with inline colour emoji; returns end x"""
    d = ImageDraw.Draw(im)
    es = int(font.size * 1.25)
    for ch in text:
        if is_emo(ch):
            e = emo(ch, es)
            im.paste(e, (int(x + 2), int(cy - e.height / 2)), e)
            x += es + 4
        else:
            d.text((x, cy), ch, font=font, fill=fill, anchor='lm')
            x += font.getlength(ch)
    return x


def rich_len(text, font):
    return sum(int(font.size * 1.25) + 4 if is_emo(ch) else font.getlength(ch) for ch in text)


# ------------------------------------------------------------------ screen
MOST = '😂💙👍😊🔥🎉😍🙏😎🤔👀💯🍔🎂☕🌟🚀🎮😢😡🥳🤩💪✅'
SEARCH = {'p': '🐼🍑🐧🍍🥞🐷🎹📌🍕🥧🌴🎉', 'pi': '🍕🥧🐷🍍📌🎹', 'piz': '🍕', 'pizz': '🍕', 'pizza': '🍕'}
KAO = ['(^_^)', '(>_<)', '(o_O)', '\\(^o^)/', '(T_T)', '(-_-)', '(^_~)', '(*_*)', '(=^.^=)', '(._.)']
SYMS = list('€£¥¢$©®™°±×÷½¼¾') + ['→', '←', '↑', '↓', '∞', '≠', '≤', '≥', '✓']
PANEL = (480, 30, 834, 414)
TABS = ['emoji', 'gif', 'kao', 'sym', 'clip']
F24 = th.JB(600, 24)
IN_BOX = (40, 418, 700, 462)
SEND = (712, 418, 812, 462)
BODY_Y = {'b1': 196, 'b2': 240}


def cell_point(i):
    x0, y0, _, _ = PANEL
    r, c = divmod(i, 6)
    return x0 + 20 + c * 54 + 27, y0 + 142 + r * 56 + 28


def tab_point(name):
    x0, y0, _, _ = PANEL
    return x0 + 38 + TABS.index(name) * 66, y0 + 32


def sym_point(i):
    return cell_point(i)


def caret_point(s):
    if s['app'] == 'chat':
        return 56 + rich_len(s['input'], F24), (IN_BOX[1] + IN_BOX[3]) / 2
    key = s['caret']
    return 50 + rich_len(s[key], F24), BODY_Y[key]


_wp = None
_scache = {}


def render_screen(s):
    global _wp
    key = repr(sorted(s.items()))
    if key in _scache:
        return _scache[key].copy()
    if len(_scache) > 40:
        _scache.clear()
    if _wp is None:
        _wp = wallpaper()
    im = _wp.copy()
    d = ImageDraw.Draw(im)
    # window
    d.rounded_rectangle((22, 18, 830, 478), 14, fill=(250, 250, 252), outline=(200, 205, 215), width=2)
    d.rounded_rectangle((22, 18, 830, 62), 14, fill=(236, 238, 244))
    d.rectangle((22, 46, 830, 62), fill=(236, 238, 244))
    d.text((44, 40), 'Chat  ·  Sam' if s['app'] == 'chat' else 'New message', font=th.JB(600, 20), fill=(60, 64, 80), anchor='lm')
    for i, x in enumerate((744, 776, 808)):
        if i == 0:
            d.line([(x - 7, 40), (x + 7, 40)], fill=(80, 80, 90), width=2)
        elif i == 1:
            d.rectangle((x - 7, 33, x + 7, 47), outline=(80, 80, 90), width=2)
        else:
            d.line([(x - 7, 33), (x + 7, 47)], fill=(80, 80, 90), width=2); d.line([(x - 7, 47), (x + 7, 33)], fill=(80, 80, 90), width=2)
    caret = s.get('caret')
    if s['app'] == 'chat':
        d.text((48, 92), 'Sam', font=th.JB(700, 16), fill=(120, 124, 140), anchor='lm')
        w = rich_len('Dinner tonight?', F24)
        d.rounded_rectangle((44, 106, 44 + w + 36, 152), 20, fill=(232, 234, 240))
        rich(im, 62, 129, 'Dinner tonight?', F24, (30, 32, 44))
        if s.get('sent'):
            txt = s['sent']
            w = rich_len(txt, F24)
            d.rounded_rectangle((806 - w - 40, 178, 806, 226), 20, fill=BLUEW)
            rich(im, 806 - w - 20, 202, txt, F24, (255, 255, 255))
            d.text((806, 240), 'Delivered', font=th.JB(600, 15), fill=(120, 124, 140), anchor='rm')
        d.rounded_rectangle(IN_BOX, 12, fill=(255, 255, 255), outline=(190, 196, 210), width=2)
        cy = (IN_BOX[1] + IN_BOX[3]) / 2
        if s['input']:
            rich(im, 56, cy, s['input'], F24, (30, 32, 44))
        else:
            d.text((56, cy), 'Type a message', font=F24, fill=(160, 164, 176), anchor='lm')
        d.rounded_rectangle(SEND, 12, fill=(0, 84, 160) if s.get('send_hl') else BLUEW)
        d.text(((SEND[0] + SEND[2]) / 2, cy), 'Send', font=th.JB(800, 22), fill=(255, 255, 255), anchor='mm')
    else:
        for y, lab, val in ((92, 'To:', 'sam@example.com'), (136, 'Subject:', 'Team update')):
            d.text((50, y), lab, font=th.JB(600, 20), fill=(120, 124, 140), anchor='lm')
            d.text((160, y), val, font=th.JB(600, 22), fill=(30, 32, 44), anchor='lm')
            d.line([(44, y + 22), (806, y + 22)], fill=(225, 228, 236), width=2)
        for k in ('b1', 'b2'):
            rich(im, 50, BODY_Y[k], s[k], F24, (30, 32, 44))
    if caret and not s.get('panel_hide_caret'):
        cx, cy = caret_point(s)
        d.line([(cx + 2, cy - 15), (cx + 2, cy + 15)], fill=(30, 32, 44), width=3)
    # taskbar
    d.rectangle((0, SH - 46, SW, SH), fill=(232, 236, 244))
    for i in range(5):
        x = SW / 2 - 110 + i * 48
        d.rounded_rectangle((x, SH - 37, x + 30, SH - 9), 7, fill=[(0, 103, 192), (255, 185, 0), (90, 90, 100), (16, 160, 110), (220, 70, 70)][i])
    d.text((SW - 20, SH - 23), '9:41', font=th.JB(600, 18), fill=(40, 40, 50), anchor='rm')
    if s.get('panel'):
        draw_panel(im, s)
    _scache[key] = im.copy()
    return im


def draw_panel(im, s):
    x0, y0, x1, y1 = PANEL
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 6, y0 + 10, x1 + 6, y1 + 10), 16, fill=(0, 0, 0, 90))
    base = im.convert('RGBA'); base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); im.paste(base.convert('RGB'))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, y0, x1, y1), 16, fill=(246, 247, 251), outline=(205, 210, 222), width=2)
    tab = s['panel']
    dark = (60, 64, 80)
    for name in TABS:
        cx, cy = tab_point(name)
        if s.get('tab_hl') == name:
            d.rounded_rectangle((cx - 28, cy - 20, cx + 28, cy + 20), 8, fill=(225, 232, 246))
        if name == 'emoji':
            e = emo('😊', 30); im.paste(e, (int(cx - e.width / 2), int(cy - e.height / 2)), e)
        elif name == 'gif':
            d.text((cx, cy), 'GIF', font=th.JB(800, 18), fill=dark, anchor='mm')
        elif name == 'kao':
            d.text((cx, cy), ';-)', font=th.JB(800, 20), fill=dark, anchor='mm')
        elif name == 'sym':
            d.text((cx, cy), 'Ω', font=ImageFont.truetype(SYM_FONT, 26), fill=dark, anchor='mm')
        else:
            d.rounded_rectangle((cx - 10, cy - 13, cx + 10, cy + 13), 3, outline=dark, width=3)
            d.rectangle((cx - 5, cy - 16, cx + 5, cy - 10), fill=dark)
        if name == tab:
            d.line([(cx - 18, cy + 24), (cx + 18, cy + 24)], fill=BLUEW, width=4)
    # search box
    q = s.get('query', '')
    d.rounded_rectangle((x0 + 14, y0 + 64, x1 - 14, y0 + 102), 10, fill=(255, 255, 255), outline=(0, 103, 192) if q else (210, 214, 224), width=2)
    d.ellipse((x0 + 28, y0 + 74, x0 + 44, y0 + 90), outline=dark, width=2); d.line([(x0 + 42, y0 + 88), (x0 + 50, y0 + 96)], fill=dark, width=2)
    if q:
        d.text((x0 + 60, y0 + 83), q, font=th.JB(700, 22), fill=(30, 32, 44), anchor='lm')
        qx = x0 + 62 + th.JB(700, 22).getlength(q)
        d.line([(qx, y0 + 72), (qx, y0 + 94)], fill=(30, 32, 44), width=2)
    else:
        d.text((x0 + 60, y0 + 83), 'Search', font=th.JB(600, 20), fill=(150, 154, 168), anchor='lm')
    hl = s.get('cell_hl')
    head = {'emoji': 'Results' if q else 'Most used', 'gif': 'Trending GIFs', 'kao': 'Kaomoji', 'sym': 'Currency & more'}[tab]
    d.text((x0 + 22, y0 + 124), head, font=th.JB(700, 17), fill=(110, 114, 130), anchor='lm')
    if tab == 'emoji':
        items = SEARCH.get(q, MOST) if q else MOST
        for i, ch in enumerate(items[:24]):
            cx, cy = cell_point(i)
            if hl == i:
                d.rounded_rectangle((cx - 25, cy - 25, cx + 25, cy + 25), 8, fill=(205, 222, 248))
            e = emo(ch, 38); im.paste(e, (int(cx - e.width / 2), int(cy - e.height / 2)), e)
    elif tab == 'gif':
        cols = [((255, 196, 70), (240, 120, 90)), ((120, 200, 160), (60, 140, 200)), ((180, 140, 230), (250, 120, 170)),
                ((100, 180, 240), (255, 220, 120)), ((250, 150, 110), (120, 110, 210)), ((150, 220, 120), (40, 160, 160))]
        for i, (c1, c2) in enumerate(cols):
            r, c = divmod(i, 2)
            bx, by = x0 + 20 + c * 160, y0 + 140 + r * 82
            d.rounded_rectangle((bx, by, bx + 150, by + 72), 10, fill=c1)
            d.ellipse((bx + 50 + (i * 13) % 40, by + 14, bx + 90 + (i * 13) % 40, by + 54), fill=c2)
            d.rounded_rectangle((bx + 6, by + 48, bx + 44, by + 66), 5, fill=(30, 32, 44))
            d.text((bx + 25, by + 57), 'GIF', font=th.JB(800, 12), fill=(255, 255, 255), anchor='mm')
    elif tab == 'kao':
        for i, k in enumerate(KAO):
            r, c = divmod(i, 2)
            d.text((x0 + 24 + c * 160, y0 + 160 + r * 48), k, font=th.JB(700, 22), fill=(30, 32, 44), anchor='lm')
    elif tab == 'sym':
        sf = ImageFont.truetype(SYM_FONT, 30)
        for i, ch in enumerate(SYMS[:24]):
            cx, cy = cell_point(i)
            if hl == i:
                d.rounded_rectangle((cx - 25, cy - 25, cx + 25, cy + 25), 8, fill=(205, 222, 248))
            d.text((cx, cy), ch, font=sf, fill=(30, 32, 44), anchor='mm')


# ================================================================== timeline
class TL(wv.TL):
    def __init__(s):
        super().__init__()
        s.cur['scr'] = dict(app='chat', input='Pizza tonight?', caret='in', panel=None)

    def combo(s, hold_key, key, label_txt, after=None, n=6):
        s.cur['keys'] = [hold_key]; s.cur['combo'] = dict(t=label_txt, f=s.f); s.sound('tap')
        s.hold(2)
        s.hand_to(*key_center(key), n)
        s.hold(1)
        s.cur['hand']['p'] = True; s.cur['keys'] = [hold_key, key]; s.sound('tap')
        s.fx.append(('ring', s.f, *key_center(key)))
        s.hold(2)
        if after:
            after()
        s.hold(3)
        s.cur['hand']['p'] = False; s.cur['keys'] = []
        s.hand_to(key_center(key)[0] + 60, key_center(key)[1] + 120, 3)

    def type_key(s, k, after=None, n=3):
        s.hand_to(*key_center(k), n)
        s.cur['hand']['p'] = True; s.cur['keys'] = [k]; s.sound('tap')
        s.fx.append(('ring', s.f, *key_center(k)))
        if after:
            after()
        s.hold(2)
        s.cur['hand']['p'] = False; s.cur['keys'] = []
        s.snap()


def build():
    t = TL()
    t.fx.append(('title', 0, 86)); t.hold(92)
    # props in
    t.sound('whoosh')
    for i in range(1, 8):
        e = ease(i / 7)
        t.cur['mon_dy'] = -1500 * (1 - e) + (24 if i == 6 else 0)
        t.cur['kb_dy'] = 900 * (1 - ease(max(0, i - 1) / 6)) + (-20 if i == 7 else 0)
        t.snap()
    t.cur['kb_dy'] = 0; t.cur['mon_dy'] = 0; t.hold(3)
    # ---- problem: hunting for an emoji button
    t.cap('FIG. 00  /  THE PROBLEM', 'Want an emoji on your PC? No button?'); t.hold(6)
    for (x, y) in [(640, 440), (770, 40), (420, 300)]:
        t.cursor_to(x, y, 5); t.hold(3)
    t.fx.append(('burst', t.f, 850, 650, 0)); t.sound('knock'); t.hold(12)
    t.cap('FIG. 00  /  THE FIX', 'One shortcut, every emoji'); t.hold(30)
    # ---- step 1
    t.cap('FIG. 01  /  STEP 1 OF 2', 'Press WIN + . (period)'); t.hold(10)
    t.cursor_to(*caret_point(t.cur['scr']), 5)
    t.combo('WIN', '.', 'WIN + .', after=lambda: (t.scr(panel='emoji', query=''), t.sound('pop')))
    t.hold(6)
    # ---- step 2: type to search, click to add
    t.cap('FIG. 02  /  STEP 2 OF 2', 'Type to search, then click it'); t.hold(6)
    q = ''
    for ch in 'pizza':
        q += ch
        t.type_key(ch.upper(), after=lambda q=q: t.scr(query=q))
    t.hand_out(3)
    t.cursor_to(*cell_point(0), 6); t.scr(cell_hl=0); t.hold(3)
    t.click(lambda: (t.scr(input='Pizza tonight? 🍕', cell_hl=None), t.sound('ding')))
    t.hold(8)
    t.cursor_to((SEND[0] + SEND[2]) / 2, (SEND[1] + SEND[3]) / 2, 5); t.scr(send_hl=True); t.hold(2)
    t.click(lambda: (t.scr(panel=None, query='', send_hl=False, sent='Pizza tonight? 🍕', input=''), t.sound('swish')))
    t.cap('RESULT  /  OK', 'Emoji sent, no copy-paste needed')
    t.fx.append(('burst', t.f, 880, 640, 1)); t.hold(30)
    # ---- field test: works in email too
    t.cap('FIG. 03  /  FIELD TEST', 'Works in email too')
    t.scr(app='mail', b1='Meeting moved to Friday', b2='Tickets: 20', caret='b1', sent=None, input=''); t.sound('swish')
    t.hold(8)
    t.cursor_to(*caret_point(t.cur['scr']), 5); t.click()
    t.combo('WIN', '.', 'WIN + .', after=lambda: (t.scr(panel='emoji', query=''), t.sound('pop')), n=5)
    t.hand_out(3)
    t.cursor_to(*cell_point(2), 5); t.scr(cell_hl=2); t.hold(2)
    t.click(lambda: (t.scr(b1='Meeting moved to Friday 👍', cell_hl=None), t.sound('ding')))
    t.hold(12)
    # ---- bonus: GIFs, kaomoji & symbols
    t.cap('APPENDIX  /  BONUS', 'Bonus: GIFs, kaomoji & symbols too'); t.hold(4)
    t.scr(panel=None, caret='b2')
    t.cursor_to(*caret_point(t.cur['scr']), 5); t.click()
    t.combo('WIN', '.', 'WIN + .', after=lambda: (t.scr(panel='emoji', query=''), t.sound('pop')), n=4)
    t.hand_out(3)
    for name in ('gif', 'kao', 'sym'):
        t.cursor_to(*tab_point(name), 4); t.scr(tab_hl=name); t.hold(1)
        t.click(lambda name=name: t.scr(panel=name, tab_hl=None)); t.hold(7)
    t.cursor_to(*sym_point(0), 4); t.scr(cell_hl=0); t.hold(2)
    t.click(lambda: (t.scr(b2='Tickets: 20€', cell_hl=None), t.sound('ding')))
    t.hold(18)
    # ---- end
    t.cap_off()
    t.cur['cursor'] = None
    t.sound('whoosh')
    for i in range(1, 6):
        e = ease(i / 5); t.cur['mon_dy'] = -1600 * e; t.cur['kb_dy'] = 1000 * e; t.snap()
    t.fx.append(('end', t.f)); t.hold(72)
    return t


# ================================================================== render
P = {}
TLD = None


def init_props():
    P['bg'] = th.bg_blue(with_dims=False)
    P['mon'] = th.sprite(monitor_raw(), border=8, off=(16, 22), blur=14, op=.42)
    P['kb'] = th.sprite(keyboard_raw(), border=8, off=(12, 18), blur=12, op=.42)
    P['keys'] = {(k, p): key_sprite(k, p, p) for k in ACTIVE for p in (False, True)}
    P['hand'] = {'hover': th.hand_sprite('blue', press=False), 'press': th.hand_sprite('blue', press=True)}
    P['cursor'], P['ctip'] = cursor_sprite()
    P['rings'] = [dashed_ring(r, YEL, w) for r, w in [(30, 8), (50, 7), (70, 5)]]
    P['hold'] = label('HOLD', th.JB(800, 26), bg=YEL, rot=-6, padx=14, pady=6)
    P['notes'] = {}
    P['combo'] = {}
    P['bursts'] = [label('NOPE!', th.JB(800, 64), tape=True, rot=-8, padx=30, pady=12),
                   label('SENT!', th.JB(800, 64), bg=YEL, tape=True, rot=7, padx=30, pady=12)]
    # title
    P['tiles'] = [rotate_sprite(th.stencil_letter(ch, PAPER), rng_for('em', i).uniform(-4, 4)) for i, ch in enumerate('EMOJI')]
    P['t_label'] = label('SPEC // PC tip', th.JB(700, 34), fg=MID, rot=-2, padx=30, pady=16)
    P['t_s1'] = center_label('EMOJIS ON YOUR PC?', th.JB(800, 46), rot=1.5)
    P['t_s1b'] = center_label('ONE SHORTCUT, EVERY APP', th.JB(800, 46), rot=-1)
    P['t_s2'] = center_label('emoji panel', th.JB(700, 40), bg=YEL, rot=-2)
    P['t_kw'] = key_sprite('WIN', False, True); P['t_kv'] = key_sprite('.', False, True)
    P['t_plus'] = center_label('+', th.JB(800, 60), bg=PAPER, padx=24, pady=6)
    P['t_burst'] = label(['WINDOWS', '10 & 11'], th.JB(800, 36), rot=6, padx=26, pady=16)
    # end
    P['e_head'] = center_label('SAVE THIS TIP', th.JB(800, 92), rot=-2.5, padx=56, pady=30)
    P['e_chips'] = [rotate_sprite(path_label(tx, c, g, i + 1, hot=(i == 3)), r) for i, (tx, c, g, r) in enumerate([
        ('Any text box', (90, 90, 100), 'dot', -2), ('WIN + .', (0, 103, 192), 'grid', 1.5), ('Type to search', (0, 103, 192), 'zoom', -1.5),
        ('Click it', NAVY, 'touch', 2)])]
    P['e_arrows'] = [chalk_arrow(r) for r in (14, -14, 14)]
    P['e_s1'] = center_label('GIFS · KAOMOJI · SYMBOLS', th.JB(800, 44), bg=YEL, rot=-1.5)
    P['e_s2'] = center_label('WORKS IN ANY APP', th.JB(800, 44), rot=1.5)
    P['e_s3'] = center_label('Windows 10 & 11 (GIFs: Windows 11)', th.JB(600, 34), fg=MID, rot=-1, pady=18)
    P['e_follow'] = center_label('FOLLOW  TECH WALL', th.JB(800, 40), bg=YEL, rot=1, pady=18)


wv.P = P
put = wv.put
draw_title = wv.draw_title
draw_caps = wv.draw_caps


def draw_end(cv, f, a):
    wv.draw_end(cv, f, a)
    yy = m.drop_y(f, a + 36, 1770)
    if yy is not None:
        put(cv, P['e_follow'], 600, yy, f, 'e_follow')


_stex = None


def render(f):
    global _stex
    tl = TLD
    st = tl['frames'][f]
    cv = P['bg'].copy()
    for e in tl['fx']:
        if e[0] == 'title' and f < e[2] + 8:
            draw_title(cv, f, e[1], e[2])
        if e[0] == 'end' and f >= e[1]:
            draw_end(cv, f, e[1])
    # keyboard
    if st['kb_dy'] < 850:
        kx, ky = KBX, KBY + st['kb_dy']
        jx, jy = jit(f, 'kb', 1.2)
        draw_sprite(cv, P['kb'], kx + jx, ky + jy)
        for k in ACTIVE:
            pressed = k in st['keys']
            sp = P['keys'][(k, pressed)]
            cx, cy = key_center(k)
            draw_sprite(cv, sp, cx + jx, cy + st['kb_dy'] + jy + (3 if pressed else 0))
        if 'WIN' in st['keys']:
            cx, cy = key_center('WIN')
            draw_sprite(cv, P['hold'], cx + jx, cy + st['kb_dy'] - 66 + jy)
        if st['combo'] and f - st['combo']['f'] < 40:
            t_ = st['combo']['t']
            if t_ not in P['combo']:
                P['combo'][t_] = label(t_, th.JB(800, 48), bg=YEL, tape=True, rot=-3, padx=28, pady=12)
            age = f - st['combo']['f']
            yy = {0: 1180, 1: 1340, 2: 1312}.get(age, 1320)
            put(cv, P['combo'][t_], 905, yy - 30 + st['kb_dy'], f, 'combo')
    # monitor
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
    # fx: rings + taped bursts
    for e in tl['fx']:
        k = f - e[1]
        if e[0] == 'ring' and 0 <= k < 3:
            put(cv, P['rings'][k], e[2], e[3], f, 'ring', .5)
        elif e[0] == 'burst' and 0 <= k < 10:
            sc = {0: 0.5, 1: 1.08}.get(k, 1.0)
            sp = P['bursts'][e[4]]
            if sc != 1.0:
                sp = tuple(s_.resize((int(s_.width * sc), int(s_.height * sc)), Image.BILINEAR) for s_ in sp)
            put(cv, sp, e[2], e[3], f, ('burst', e[1]))
    hd = st['hand']
    if hd:
        sh_, body_, tip = P['hand']['press' if hd['p'] else 'hover']
        jx, jy = jit(f, 'hand', 1.4)
        blit(cv, sh_, hd['x'] - tip[0] + jx, hd['y'] - tip[1] + jy); blit(cv, body_, hd['x'] - tip[0] + jx, hd['y'] - tip[1] + jy)
    draw_caps(cv, f, tl['caps'])
    k = 1 + rng_for(f, 'flicker').uniform(-0.016, 0.016)
    out = cv.convert('RGB').point(lambda v: min(255, int(v * k)))
    out.save(f'{OUT}/{f:05d}.png', compress_level=1)
    return f


def add_title_end_sounds(t):
    for e in t.fx:
        if e[0] == 'title':
            a = e[1]
            for ap in [a + 1] + [a + 4 + 2 * i for i in range(5)] + [a + 16, a + 19, a + 23, a + 27, a + 28, a + 29, a + 32]:
                t.snd.append((ap, 'pop'))
            t.snd.append((e[2] + 1, 'whoosh'))
        if e[0] == 'end':
            a = e[1]
            for ap in [a + 2] + [a + 6 + 4 * i for i in range(4)] + [a + 24, a + 28, a + 32, a + 36]:
                t.snd.append((ap, 'pop'))
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))


if __name__ == '__main__':
    t = build()
    add_title_end_sounds(t)
    TLD = dict(frames=t.frames, fx=t.fx, caps=t.caps, snd=t.snd)
    n = len(t.frames)
    print('frames', n, 'seconds', n / FPS, flush=True)
    for c in t.caps:
        print(c['inn'], c['out'], c['text'])
    os.makedirs(OUT, exist_ok=True)
    init_props()
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
        m.make_audio(TLD, n, __import__('lib').out('audio_emoji.wav'))

"""Blueprint-themed stop-motion render — reuses the stop-motion timeline from movie.py"""
import sys, os
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from multiprocessing import Pool
from PIL import Image, ImageDraw
import movie as m
import themes as th
from lib import rotate_sprite, rng_for, FPS, ease, jit, draw_sprite
from screens import glyph, BLUE, GRAYI

OUT = __import__('lib').out('frames_movie_blue')
NAVY, MID, YEL, PAPER = (20, 40, 92), (30, 74, 160), (255, 196, 70), (250, 250, 246)

# ---- slower pacing: every caption gets an extra half-second of hold
_cap = m.TL.cap
def _slow_cap(self, *a, **k):
    _cap(self, *a, **k)
    self.hold(6)
m.TL.cap = _slow_cap


def label(text, font, fg=NAVY, bg=PAPER, padx=40, pady=24, tape=False, head=None, rot=0):
    lines = text if isinstance(text, list) else [text]
    lh = font.size * 1.18
    hh = 54 if head else 0
    w = int(max(font.getlength(l) for l in lines) + 2 * padx)
    h = int(lh * len(lines) + 2 * pady + hh)
    img = Image.new('RGBA', (w, h), bg + (255,))
    d = ImageDraw.Draw(img)
    y = pady
    if head:
        d.text((padx, y + 16), head, font=th.JB(700, 26), fill=MID, anchor='lm')
        d.line([(padx, y + 40), (w - padx, y + 40)], fill=(160, 180, 215), width=2)
        y += hh
    for i, l in enumerate(lines):
        d.text((padx, y + lh * i + lh / 2), l, font=font, fill=fg, anchor='lm')
    sh, body = th.sprite(img, border=0, off=(7, 11), blur=7, op=.42)
    if tape:
        body = body.copy()
        tp = Image.new('RGBA', (200, 52), (232, 216, 168, 205)).rotate(-4, expand=True, resample=Image.BICUBIC)
        body.alpha_composite(tp, (body.width // 2 - tp.width // 2 + 60, (body.height - h) // 2 - 28))
    sp = (sh, body)
    return rotate_sprite(sp, rot) if rot else sp


def center_label(text, font, fg=NAVY, bg=PAPER, rot=0, padx=44, pady=26):
    w = int(font.getlength(text) + 2 * padx); hgt = int(font.size * 1.2 + 2 * pady)
    img = Image.new('RGBA', (w, hgt), bg + (255,))
    ImageDraw.Draw(img).text((w / 2, hgt / 2), text, font=font, fill=fg, anchor='mm')
    sp = th.sprite(img, border=0, off=(7, 11), blur=7, op=.42)
    return rotate_sprite(sp, rot) if rot else sp


def dashed_ring(r_, col, wdt):
    s = 2 * r_ + 24
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    th.dashed_circle(ImageDraw.Draw(im), s / 2, s / 2, r_, col + (255,), wdt, seg=16)
    return th.sprite(im, border=0, off=(3, 5), blur=3, op=.35, tex=False)


def vellum_phone():
    w, h = 300, 560
    im = Image.new('RGBA', (w, h), (230, 240, 255, 70))
    d = ImageDraw.Draw(im)
    C = th.CHALK + (255,)
    d.rounded_rectangle((20, 20, w - 20, h - 20), 46, outline=C, width=5)
    d.rounded_rectangle((40, 40, 140, 140), 26, outline=C, width=4)
    for cy in (68, 112):
        d.ellipse((56, cy - 16, 88, cy + 16), outline=C, width=3)
    cx, cy = w / 2, h / 2 + 30
    for r_ in (26, 54, 82):
        th.dashed_circle(d, cx, cy, r_, (YEL + (255,)) if r_ == 26 else C, 4)
    d.line([(cx - 110, cy), (cx + 110, cy)], fill=C, width=2)
    d.line([(cx, cy - 110), (cx, cy + 110)], fill=C, width=2)
    sp = th.sprite(im, border=0, off=(6, 9), blur=6, op=.3, tex=False)
    return rotate_sprite(sp, 8)


def chalk_arrow(rot):
    im = Image.new('RGBA', (90, 130), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in range(0, 92, 18):
        d.line([(45, 6 + k), (45, 16 + k)], fill=th.CHALK + (255,), width=7)
    d.polygon([(20, 92), (70, 92), (45, 126)], fill=th.CHALK + (255,))
    sp = th.sprite(im, border=0, off=(3, 4), blur=3, op=.3, tex=False)
    return rotate_sprite(sp, rot)


def path_label(txt, icol, gl, idx, hot=False):
    f = th.JB(800, 52)
    w = int(f.getlength(txt) + 260); h = 128
    bg = YEL if hot else PAPER
    img = Image.new('RGBA', (w, h), bg + (255,))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((28, 24, 108, 104), 20, fill=icol)
    glyph(d, gl, 28, 24, 80)
    d.text((136, h / 2), txt, font=f, fill=NAVY, anchor='lm')
    d.text((w - 30, h / 2), f'0{idx}', font=th.JB(700, 26), fill=MID, anchor='rm')
    return th.sprite(img, border=0, off=(7, 11), blur=7, op=.42)


def init_props():
    P = m.P
    P['bg_plain'] = th.bg_blue(with_dims=False)
    P['bg_dims'] = th.bg_blue(with_dims=True)
    P['bg'] = P['bg_plain']
    P['front'] = th.sprite(th.phone_raw('front'), border=8, off=(16, 22), blur=14, op=.4)
    P['back'] = th.sprite(th.phone_raw('back'), border=8, off=(16, 22), blur=14, op=.4)
    P['hand'] = {'hover': th.hand_sprite('blue', press=False), 'press': th.hand_sprite('blue', press=True)}
    P['rings'] = [dashed_ring(r, YEL, w) for r, w in [(30, 8), (50, 7), (70, 5)]]
    P['notes'] = {}
    # title
    P['tiles'] = [rotate_sprite(th.stencil_letter(ch, PAPER if i < 4 else YEL), rng_for('t', i).uniform(-4, 4))
                  for i, ch in enumerate('BACKTAP')]
    P['t_label'] = label('SPEC // iPhone tip', th.JB(700, 34), fg=MID, rot=-2, padx=30, pady=16)
    P['t_s1'] = center_label('THE HIDDEN iPHONE SHORTCUT', th.JB(800, 44), rot=1.5)
    P['t_s2'] = center_label('tap the back = screenshot', th.JB(700, 40), bg=YEL, rot=-2)
    P['t_phone'] = vellum_phone()
    P['t_burst'] = label(['TAP x2', '= SCREENSHOT'], th.JB(800, 40), rot=5, padx=30, pady=18)
    # end card
    P['e_head'] = center_label('SAVE THIS TIP', th.JB(800, 92), rot=-2.5, padx=56, pady=30)
    P['e_chips'] = [path_label('Settings', GRAYI, 'gear', 1), path_label('Accessibility', BLUE, 'person', 2),
                    path_label('Touch', BLUE, 'touch', 3), path_label('Back Tap', NAVY, 'touch', 4, hot=True)]
    P['e_chips'] = [rotate_sprite(s, r) for s, r in zip(P['e_chips'], (-2, 1.5, -1.5, 2))]
    P['e_arrows'] = [chalk_arrow(r) for r in (14, -14, 14)]
    P['e_s1'] = center_label('DOUBLE TAP = SCREENSHOT', th.JB(800, 46), bg=YEL, rot=-1.5)
    P['e_s2'] = center_label('TRIPLE TAP = FLASHLIGHT', th.JB(800, 46), rot=1.5)
    P['e_s3'] = center_label('works on iPhone 8+ · iOS 14+', th.JB(600, 34), fg=MID, rot=-1, pady=18)
    P['e_follow'] = center_label('FOLLOW  TECH WALL', th.JB(800, 40), bg=YEL, rot=1, pady=18)
    P['bursts'] = [label('TAP!', th.JB(800, 76), tape=True, rot=-12, padx=34, pady=14),
                   label('TAP!', th.JB(800, 76), bg=YEL, tape=True, rot=10, padx=34, pady=14)]


def fig_head(badge):
    if badge.isdigit():
        return f'FIG. 0{badge}  /  STEP {badge} OF 6'
    return {'check': 'RESULT  /  OK', '!': 'FIG. 07  /  FIELD TEST', '+': 'APPENDIX  /  BONUS'}[badge]


def draw_caps(cv, f, caps):
    for c in caps:
        k = f - c['inn']
        if k < 0:
            continue
        y = {0: -260, 1: 380, 2: 268, 3: 312}.get(k, 300)
        if c['out'] is not None and f >= c['out']:
            e = f - c['out']
            if e > 2:
                continue
            y = (230, -10, -400)[e]
        key = (c['badge'], c['text'])
        if key not in m.P['notes']:
            m.P['notes'][key] = rotate_sprite(th.cap_blue(fig_head(c['badge']), c['text']), c['rot'] * 0.6)
        m.put(cv, m.P['notes'][key], 540, y, f, ('cap', c['text']), amp=1.8)


m.draw_caps = draw_caps

_draw_end = m.draw_end


def draw_end(cv, f, a):
    """standard end card + the 'FOLLOW TECH WALL' strip (ownership mark)"""
    _draw_end(cv, f, a)
    if 'e_follow' in m.P:
        yy = m.drop_y(f, a + 36, 1770)
        if yy is not None:
            m.put(cv, m.P['e_follow'], 600, yy, f, 'e_follow')


m.draw_end = draw_end


def render(f):
    tl = m.TLD
    st = tl['frames'][f]
    P = m.P
    ph = st['ph']
    P['bg'] = P['bg_dims'] if abs(ph['y'] - m.PHY) < 60 else P['bg_plain']
    cv = P['bg'].copy()
    for e in tl['fx']:
        if e[0] == 'title' and f < e[2] + 8:
            m.draw_title(cv, f, e[1], e[2])
        if e[0] == 'end' and f >= e[1]:
            m.draw_end(cv, f, e[1])
    m.draw_phone(cv, f, ph)
    m.draw_fx(cv, f, tl['fx'])
    m.draw_hand(cv, f, st['hand'])
    m.draw_caps(cv, f, tl['caps'])
    k = 1 + rng_for(f, 'flicker').uniform(-0.016, 0.016)
    out = cv.convert('RGB').point(lambda v: min(255, int(v * k)))
    out.save(f'{OUT}/{f:05d}.png', compress_level=1)
    return f


if __name__ == '__main__':
    t = m.build()
    m.add_title_end_sounds(t)
    m.TLD = dict(frames=t.frames, fx=t.fx, caps=t.caps, snd=t.snd)
    n = len(t.frames)
    print('frames', n, 'seconds', n / FPS, flush=True)
    os.makedirs(OUT, exist_ok=True)
    init_props()
    only = [int(a) for a in sys.argv[1:]]
    if only:
        for f in only:
            render(f)
    else:
        with Pool(2) as pool:
            for i, _ in enumerate(pool.imap(render, range(n), chunksize=8)):
                if i % 100 == 0:
                    print('rendered', i, flush=True)
        m.make_audio(m.TLD, n, __import__('lib').out('audio_movie_blue.wav'))

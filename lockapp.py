"""Tech Wall — iPhone: lock (or hide) an app with Face ID. Short-form structure (~19 s, loops):
Hook (frame 0: "Photos is Locked"; a stranger's Use Face ID fails -> LOCKED!) -> lead (lending your phone?) ->
3 quick steps (touch & hold > Require Face ID / confirm with Face ID / Hide and Require Face ID -> Hidden folder
in App Library) -> specific CTA on the opening screen, so the replay flows back into the hook. No end card.
Screens are generic look-alikes; "Diary" is a fictional App Store app (only downloaded apps can be hidden).
Verified 2026-10-07: support.apple.com "Lock or hide an app on iPhone" (iOS 18+; Calculator, Camera, Clock,
Contacts, Find My, Maps, Settings and Shortcuts can't be locked; built-in apps can't be hidden).
Build:  ./build.sh lockapp
"""
import sys, os, math
import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import screens as S
from screens import F, SW, SH, TXT, GRAY, BLUE, BG_UI
import movie as m
import movie_blue as mb
import themes as th

EP = 'lockapp'
OUT = __import__('lib').out(f'frames_{EP}')
mb.OUT = OUT
YEL = mb.YEL
WHITE = (255, 255, 255)
RED = (255, 59, 48)
GREEN = (52, 199, 89)
DIARY = (40, 170, 160)

# a fictional App Store app takes the last home-screen slot
S.HOME_APPS[15] = ('Diary', DIARY, 'diary')
_home_icon = S.home_icon


def home_icon(d, kind, x, y, s, bg):
    if kind != 'diary':
        return _home_icon(d, kind, x, y, s, bg)
    d.rounded_rectangle((x + s * .26, y + s * .18, x + s * .74, y + s * .82), 6, fill=WHITE)
    d.rectangle((x + s * .26, y + s * .18, x + s * .34, y + s * .82), fill=(200, 235, 230))
    for i in range(3):
        d.line([(x + s * .42, y + s * (.36 + .14 * i)), (x + s * .66, y + s * (.36 + .14 * i))], fill=DIARY, width=3)


S.home_icon = home_icon
APP = {'photos': 1, 'diary': 15}


def slot(app):
    r, c = divmod(APP[app], 4)
    return 72 + 139 * c, 200 + 186 * r


# ======================================================================= glyphs
def faceid_glyph(d, cx, cy, s, col, w=5):
    h = s / 2; k = s * .28
    for sx in (-1, 1):
        for sy in (-1, 1):
            x0, y0 = cx + sx * h, cy + sy * h
            d.line([(x0, y0 - sy * k), (x0, y0), (x0 - sx * k, y0)], fill=col, width=w)
    d.line([(cx - s * .18, cy - s * .14), (cx - s * .18, cy - s * .04)], fill=col, width=w)
    d.line([(cx + s * .18, cy - s * .14), (cx + s * .18, cy - s * .04)], fill=col, width=w)
    d.line([(cx + s * .02, cy - s * .14), (cx + s * .02, cy + s * .08), (cx - s * .06, cy + s * .08)], fill=col, width=w - 1)
    d.arc((cx - s * .2, cy - s * .02, cx + s * .2, cy + s * .26), 30, 150, fill=col, width=w)


def padlock(d, cx, cy, s, col, w=None):
    w = w or max(4, int(s * .1))
    d.arc((cx - s * .3, cy - s * .62, cx + s * .3, cy - s * .02), 180, 360, fill=col, width=w)
    d.line([(cx - s * .3 + w / 2 - 1, cy - s * .32), (cx - s * .3 + w / 2 - 1, cy - s * .05)], fill=col, width=w)
    d.line([(cx + s * .3 - w / 2, cy - s * .32), (cx + s * .3 - w / 2, cy - s * .05)], fill=col, width=w)
    d.rounded_rectangle((cx - s * .45, cy - s * .08, cx + s * .45, cy + s * .55), int(s * .1), fill=col)


def hud(d, ov, cy=560):
    st = ov.get('faceid')
    if not st:
        return
    cx = SW / 2 + ov.get('shk', 0)
    d.rounded_rectangle((cx - 110, cy - 110, cx + 110, cy + 110), 36, fill=(44, 44, 48))
    if st == 'ok':
        faceid_glyph(d, cx, cy - 14, 96, GREEN)
        d.text((cx, cy + 72), 'Face ID', font=F(600, 24), fill=WHITE, anchor='mm')
    elif st == 'fail':
        faceid_glyph(d, cx, cy - 14, 96, RED)
        d.text((cx, cy + 72), 'Not Recognized', font=F(600, 22), fill=WHITE, anchor='mm')
    else:
        faceid_glyph(d, cx, cy - 14, 96, WHITE)
        d.text((cx, cy + 72), 'Face ID', font=F(600, 24), fill=WHITE, anchor='mm')


# ======================================================================= screens
def quick_menu(img, d, rows, app, hl):
    cx, cy = slot(app)
    items = [('Require Face ID', 'face'), ('Edit Home Screen', None), ('Share App', None), ('Remove App', None)]
    w, rh = 330, 66
    x0 = 40 if cx < SW / 2 else SW - 40 - w
    y0 = cy + 84
    d.rounded_rectangle((x0, y0, x0 + w, y0 + rh * len(items)), 26, fill=(246, 246, 248))
    for i, (t, g) in enumerate(items):
        y = y0 + rh * i
        if hl == 'rq' and i == 0:
            d.rounded_rectangle((x0 + 4, y + 4, x0 + w - 4, y + rh - 4), 20, fill=(214, 214, 220))
        col = RED if t == 'Remove App' else TXT
        d.text((x0 + 26, y + rh / 2), t, font=F(600 if i == 0 else 500, 25), fill=col, anchor='lm')
        if g:
            faceid_glyph(d, x0 + w - 40, y + rh / 2, 30, TXT, w=3)
        if i < len(items) - 1:
            d.line([(x0 + 12, y + rh), (x0 + w - 12, y + rh)], fill=(222, 222, 228), width=2)
    rows['rq'] = (x0, y0, x0 + w, y0 + rh)


def action_sheet(d, rows, app, hl):
    name = app.capitalize()
    items = [('sh_req', 'Require Face ID')]
    if app == 'diary':
        items.append(('sh_hide', 'Hide and Require Face ID'))
    rh = 74
    top = SH - 60 - 84 - 20 - 96 - rh * len(items)
    d.rounded_rectangle((20, top, SW - 20, top + 96 + rh * len(items)), 26, fill=(246, 246, 248))
    d.text((SW / 2, top + 34), f'Require Face ID for "{name}"?', font=F(600, 22), fill=GRAY, anchor='mm')
    d.text((SW / 2, top + 66), 'Face ID will be needed to open it.', font=F(500, 20), fill=GRAY, anchor='mm')
    for i, (rid, t) in enumerate(items):
        y = top + 96 + rh * i
        d.line([(20, y), (SW - 20, y)], fill=(222, 222, 228), width=2)
        if hl == rid:
            d.rectangle((22, y + 2, SW - 22, y + rh - 2), fill=(214, 214, 220))
        d.text((SW / 2, y + rh / 2), t, font=F(500, 28), fill=BLUE, anchor='mm')
        rows[rid] = (20, y, SW - 20, y + rh)
    cy = SH - 60 - 42
    d.rounded_rectangle((20, cy - 42, SW - 20, cy + 42), 26, fill=WHITE)
    d.text((SW / 2, cy), 'Cancel', font=F(600, 28), fill=BLUE, anchor='mm')


def lhome_content(ov, hl):
    img, rows = S.home_content()
    img = img.copy(); rows = dict(rows)
    if ov.get('gone'):
        cx, cy = slot('diary')
        wp = S.wallpaper().crop((int(cx - 70), int(cy - 60), int(cx + 70), int(cy + 90)))
        img.paste(wp, (int(cx - 70), int(cy - 60)))
    app = ov.get('menu') or ov.get('sheet')
    if app:
        cx, cy = slot(app)
        icon = img.crop((int(cx - 56), int(cy - 56), int(cx + 56), int(cy + 56)))
        img = img.filter(ImageFilter.GaussianBlur(9))
        img = Image.blend(img, Image.new('RGB', img.size, (40, 40, 50)), 0.3)
        if ov.get('menu'):
            img.paste(icon, (int(cx - 56), int(cy - 56)))
    d = ImageDraw.Draw(img)
    if ov.get('menu'):
        quick_menu(img, d, rows, ov['menu'], hl)
    if ov.get('sheet'):
        action_sheet(d, rows, ov['sheet'], hl)
    hud(d, ov)
    return img, rows


def locked_content(ov, hl):
    im = Image.new('RGB', (SW, SH), WHITE); d = ImageDraw.Draw(im); rows = {}
    cols = [(250, 190, 150), (150, 200, 240), (180, 230, 170), (250, 220, 120), (210, 180, 240), (240, 160, 170)]
    for i in range(24):
        r, c = divmod(i, 4)
        d.rectangle((c * 140 + 3, 110 + r * 140 + 3, c * 140 + 137, 110 + r * 140 + 137), fill=cols[(i * 5 + r) % 6])
    im = im.filter(ImageFilter.GaussianBlur(26))
    im = Image.blend(im, Image.new('RGB', im.size, (248, 248, 250)), 0.62)
    d = ImageDraw.Draw(im)
    padlock(d, SW / 2, 390, 150, TXT)
    d.text((SW / 2, 530), 'Photos is Locked', font=F(600, 46), fill=TXT, anchor='mm')
    d.text((SW / 2, 588), 'Use Face ID to view Photos.', font=F(500, 28), fill=GRAY, anchor='mm')
    bx0, by0, bx1, by1 = SW / 2 - 150, 650, SW / 2 + 150, 726
    d.rounded_rectangle((bx0, by0, bx1, by1), 33, fill=(214, 214, 220) if hl == 'useid' else (232, 232, 238))
    d.text((SW / 2, (by0 + by1) / 2), 'Use Face ID', font=F(600, 32), fill=BLUE, anchor='mm')
    rows['useid'] = (bx0, by0, bx1, by1)
    hud(d, ov, cy=880)
    return im, rows


def folder(img, d, x, y, s, label, kinds=None, hidden=False, hot=False):
    over = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(over).rounded_rectangle((x, y, x + s, y + s), 40, fill=(255, 255, 255, 110))
    img.paste(Image.alpha_composite(img.convert('RGBA'), over).convert('RGB'))
    d = ImageDraw.Draw(img)
    if hot:
        d.rounded_rectangle((x - 6, y - 6, x + s + 6, y + s + 6), 44, outline=YEL, width=6)
    if hidden:
        faceid_glyph(d, x + s / 2, y + s / 2 - 8, 70, WHITE)
        padlock(d, x + s - 34, y + s - 40, 34, WHITE, w=4)
    else:
        q = (s - 54) / 2
        for i, (bg, kind) in enumerate(kinds):
            r, c = divmod(i, 2)
            ix, iy = int(x + 18 + c * (q + 18)), int(y + 18 + r * (q + 18))
            icon = Image.new('RGB', (int(q), int(q)), bg)
            home_icon(ImageDraw.Draw(icon), kind, 0, 0, int(q), bg)
            mk = Image.new('L', icon.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, q - 1, q - 1), 18, fill=255)
            img.paste(icon, (ix, iy), mk)
    d.text((x + s / 2 + 1, y + s + 25), label, font=F(600, 22), fill=(60, 40, 40), anchor='mm')
    d.text((x + s / 2, y + s + 24), label, font=F(600, 22), fill=WHITE, anchor='mm')
    return d


def library_content(ov, hl):
    img = S.wallpaper().filter(ImageFilter.GaussianBlur(18))
    img = Image.blend(img, Image.new('RGB', img.size, (90, 70, 80)), 0.25)
    d = ImageDraw.Draw(img); rows = {}
    d.rounded_rectangle((30, 106, SW - 30, 160), 18, fill=(255, 255, 255))
    d.text((SW / 2, 133), 'App Library', font=F(500, 26), fill=GRAY, anchor='mm')
    A = {k: (bg, kind) for _, bg, kind in S.HOME_APPS for k in [kind]}
    groups = [('Suggestions', ['cal', 'flower', 'mail', 'notes']), ('Recently Added', ['sun', 'book', 'note', 'heart']),
              ('Utilities', ['clock', 'gear', 'grid', 'pin']), ('Creativity', ['cam', 'flower', 'note', 'book'])]
    s = 226
    for i, (lab, ks) in enumerate(groups):
        r, c = divmod(i, 2)
        d = folder(img, d, 40 + c * (s + 28), 200 + r * (s + 70), s, lab, [A[k] for k in ks])
    y = 200 + 2 * (s + 70)
    d = folder(img, d, 40, y, s, 'Hidden', hidden=True, hot=bool(ov.get('hot')))
    rows['hidden'] = (40, y, 40 + s, y + s)
    return img, rows


BUILD = {'lhome': lhome_content, 'locked': locked_content, 'library': library_content}
_orig = S.screen_content
_cache = {}


def screen_content(name, ov=None, hl=None):
    ov = ov or {}
    if name not in BUILD:
        return _orig(name, ov, hl)
    key = (name, tuple(sorted(ov.items())), hl)
    if key not in _cache:
        if len(_cache) > 30:
            _cache.clear()
        _cache[key] = BUILD[name](ov, hl)
    return _cache[key]


S.screen_content = screen_content
_view = S.view


def view(spec):
    if spec['name'] not in BUILD:
        return _view(spec)
    v = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))[0].copy()
    S.status_bar(v, dark_text=spec['name'] != 'library')
    return v


m.view = view


def row_point(spec, rid, fx=0.5):
    _, rows = screen_content(spec['name'], spec.get('ov'), spec.get('hl'))
    x0, y0, x1, y1 = rows[rid]
    return x0 + (x1 - x0) * fx, (y0 + y1) / 2


m.row_point = row_point


# ======================================================================= timeline
def fig_head(badge):
    if badge.isdigit():
        return f'STEP {badge} OF 3'
    return {'H': 'TECH WALL  /  iPHONE TIP', 'L': 'iOS 18 OR LATER', 'cta': 'SAVE THIS  /  FOR LATER'}[badge]


mb.fig_head = fig_head
spec = m.spec


def long_press(t, rid, ov, n_move=5):
    """touch & hold an icon: press, keep holding (the icon lifts), then the quick menu opens"""
    sp = t.ph['spec']
    tx, ty = t.s2c(*row_point(sp, rid))
    t.move_hand(tx, ty, n_move)
    t.hold(1)
    t.press(tx, ty)
    t.hold(6)
    sp['ov'].update(ov)
    t.sound('pop')
    t.hold(2)
    t.hand['press'] = False


def face_ok(t, ov_after=None):
    sp = t.ph['spec']
    sp['ov']['faceid'] = 'scan'; t.sound('whoosh'); t.hold(5)
    sp['ov']['faceid'] = 'ok'; t.sound('ding'); t.hold(5)
    sp['ov'].pop('faceid')
    sp['ov'].pop('sheet', None)
    if ov_after:
        sp['ov'].update(ov_after)
    t.snap()


def build():
    t = m.TL()
    # HOOK — frame 0: Photos is Locked; a borrower's Use Face ID fails -> LOCKED!
    mb.result_first(t, spec('locked', ov={}), 'H', 'LOCK AN APP WITH FACE ID')
    t.hold(5)
    t.tap('useid', n_move=4, fx=0.5)
    t.hand_out(3)
    sp = t.ph['spec']
    sp['ov']['faceid'] = 'scan'; t.sound('whoosh'); t.hold(3)
    sp['ov']['faceid'] = 'fail'; t.sound('knock')
    for dx in (-14, 14, -10, 10, -5, 0):
        sp['ov']['shk'] = dx; t.snap()
    t.fx.append(('burst', t.f, 790, 1690, 0))
    t.hold(11)
    sp['ov'].clear(); t.snap()
    # LEAD — the promise
    t.cap('L', 'Lending your phone? Lock the private apps:', m.YELLOW)
    t.navigate(spec('lhome', ov={}), back=True)
    t.hold(20)
    # STEP 1 — touch & hold the app > Require Face ID
    t.cap('1', 'Touch & hold the app > Require Face ID', m.MINT)
    t.hold(3)
    long_press(t, 'app_photos', {'menu': 'photos'})
    t.hold(4)
    t.tap('rq', ov={'menu': None, 'sheet': 'photos'}, n_move=4, fx=0.4)
    t.ph['spec']['ov'].pop('menu')
    t.hand_out(3); t.hold(5)
    # STEP 2 — confirm with Face ID
    t.cap('2', "Confirm with Face ID and it's locked", m.SKY)
    t.hold(4)
    t.tap('sh_req', n_move=3, fx=0.5)
    t.hand_out(3)
    face_ok(t)
    t.fx.append(('burst', t.f, 380, 1000, 0)); t.hold(12)
    # STEP 3 — or hide it: Hide and Require Face ID -> Hidden folder in App Library
    t.cap('3', 'Or hide it: it moves to a Hidden folder', m.PEACH)
    t.hold(3)
    long_press(t, 'app_diary', {'menu': 'diary'})
    t.hold(3)
    t.tap('rq', ov={'menu': None, 'sheet': 'diary'}, n_move=4, fx=0.4)
    t.ph['spec']['ov'].pop('menu')
    t.hold(3)
    t.tap('sh_hide', n_move=4, fx=0.5)
    t.hand_out(3)
    face_ok(t, {'gone': True})
    t.sound('swish'); t.hold(5)
    t.navigate(spec('library', ov={'hot': True}))
    t.fx.append(('burst', t.f + 1, 760, 1480, 1)); t.hold(15)
    # CTA — back on the opening screen so the replay flows into the hook
    t.cap('cta', 'Save this. Which app would you lock first?', m.YELLOW)
    t.navigate(spec('locked', ov={}), back=True)
    t.hold(42)
    return t


def init_props():
    mb.init_props()
    m.P['bursts'] = [mb.label('LOCKED!', th.JB(800, 64), bg=YEL, tape=True, rot=-7, padx=30, pady=12),
                     mb.label('HIDDEN!', th.JB(800, 64), bg=YEL, tape=True, rot=6, padx=30, pady=12)]


if __name__ == '__main__':
    t = build()
    for e in t.fx:
        if e[0] == 'burst':
            t.snd.append((e[1], 'pop'))
    mb.finish(t, EP, init_props)

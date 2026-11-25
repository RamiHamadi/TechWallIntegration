"""Tech Wall HOST explainer (Arabic) with a supplied voice-over: how Face ID recognises your face.
    ./build.sh faceid  |  python3 faceid.py 0 150 400
No device: 'stage' = a frameless illustration area above the host, drawn in the blueprint style (template flashlight.py,
whose drawing helpers it reuses). Voice: the user's Lebanese-Arabic generated audio, pauses between phrases shortened to
0.2 s (host/voices/faceid.flac); beat 't' = [start, end] s in it; script transcribed with the multilingual Whisper turbo model.
Facts (Apple: "About Face ID advanced technology" support.apple.com/102381, Platform Security guide, Face ID & Privacy page):
the TrueDepth camera (flood illuminator, dot projector, infrared camera) projects and reads over 30,000 invisible infrared
dots, builds a depth map + 2D infrared image, turns it into a mathematical representation and compares it inside the
Secure Enclave; the data never leaves the device (not sent to Apple, not in backups); it resists photos and masks and
adapts to changes such as facial hair, and works with glasses. iPhone feature (most Android face unlock is 2D), so the
tag says iPhone. Generic drawings, no logos."""
import random
import host
from flashlight import box, txt, chip, glow, mover, AR, PANEL, INK, CYAN, YEL, RED, GRN

EP = 'faceid'
IR = '255,70,90'                                  # infrared drawn as a soft red (invisible in reality)


def face(cx, cy, s=1.0, beard=False, glasses=False, stroke=INK, extra=''):
    """Line-art face (about 300x380 at s=1), centred on (cx, cy)."""
    w = 2.0 * s
    bd = (f'<path d="M-118 40 Q-110 170 0 192 Q110 170 118 40 Q90 120 0 130 Q-90 120 -118 40Z" fill="rgba(233,241,255,.28)" '
          f'stroke="{stroke}" stroke-width="{3 / s:.1f}"/>' if beard else '')
    gl = (f'<g fill="rgba(92,225,255,.12)" stroke="{stroke}" stroke-width="{5 / s:.1f}"><rect x="-108" y="-44" width="86" height="58" rx="18"/>'
          f'<rect x="22" y="-44" width="86" height="58" rx="18"/><path d="M-22 -24 Q0 -36 22 -24" fill="none"/></g>' if glasses else '')
    return (f'<svg viewBox="-200 -240 400 480" style="position:absolute;left:{cx - 200 * s:.0f}px;top:{cy - 240 * s:.0f}px;'
            f'width:{400 * s:.0f}px;height:{480 * s:.0f}px;overflow:visible"><g fill="none" stroke="{stroke}" stroke-width="{5 / s * w / 2:.1f}" '
            'stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M0 -200 Q140 -200 146 -40 Q150 110 70 172 Q0 214 -70 172 Q-150 110 -146 -40 Q-140 -200 0 -200Z" fill="rgba(6,20,52,.55)"/>'
            '<path d="M-146 -20 Q-178 -24 -170 30 Q-164 70 -140 62 M146 -20 Q178 -24 170 30 Q164 70 140 62"/>'
            '<path d="M-100 -70 Q-66 -88 -34 -70 M34 -70 Q66 -88 100 -70"/>'
            '<ellipse cx="-64" cy="-16" rx="22" ry="12"/><ellipse cx="64" cy="-16" rx="22" ry="12"/>'
            '<path d="M0 -10 L-16 64 Q0 76 18 64"/><path d="M-50 112 Q0 136 50 112"/>'
            f'{bd}{gl}{extra}</g></svg>')


def iphone(x, y, w=230, h=470, inner='', attr=''):
    """Front of a generic iPhone-like phone with the sensor strip at the top."""
    return box(x, y, w, h, f'border:6px solid {INK};border-radius:46px;box-sizing:border-box;background:linear-gradient(170deg,#132e6e,#0a1d4c);'
               'overflow:hidden', box(w / 2 - 60, 12, 108, 30, 'background:#050b1c;border-radius:16px') + inner, attr)


def padlock(x, y, w_open=None, col='#fff', s=1.0):
    """Padlock that opens (shackle lifts and turns green) at w_open (s)."""
    sh = (f'<div data-keys="0,0,0;{w_open},0,0;{w_open + .35:.2f},0,-22" style="position:absolute;left:{14 * s:.0f}px;top:0;width:{52 * s:.0f}px;'
          f'height:{50 * s:.0f}px;border:{9 * s:.0f}px solid {col};border-bottom:none;border-radius:{30 * s:.0f}px {30 * s:.0f}px 0 0;box-sizing:border-box"></div>'
          if w_open else
          f'<div style="position:absolute;left:{14 * s:.0f}px;top:0;width:{52 * s:.0f}px;height:{50 * s:.0f}px;border:{9 * s:.0f}px solid {col};'
          f'border-bottom:none;border-radius:{30 * s:.0f}px {30 * s:.0f}px 0 0;box-sizing:border-box"></div>')
    body = box(0, 40 * s, 80 * s, 64 * s, f'background:{col};border-radius:{14 * s:.0f}px')
    ok = (box(0, 40 * s, 80 * s, 64 * s, f'background:{GRN};border-radius:{14 * s:.0f}px;display:grid;place-items:center;font-size:{40 * s:.0f}px;'
              'color:#06331f;font-weight:900', '✓', f'data-in="{w_open + .3:.2f}"') if w_open else '')
    return box(x - 40 * s, y - 52 * s, 80 * s, 104 * s, '', sh + body + ok)


def beams(x1, y1, pts, col=IR, w_in=None, dash=True):
    da = ' stroke-dasharray="8 10"' if dash else ''
    paths = ''.join(f'<path d="M{x1} {y1} L{x} {y}" stroke="rgba({col},.75)" stroke-width="3"{da}/>' for x, y in pts)
    a = f'data-in="{w_in}" ' if w_in else ''
    return f'<svg {a}viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px;overflow:visible">{paths}</svg>'


# ------------------------------------------------------------------ 1 · hook: phone unlocks by looking at it, in the dark
FX, FY = 290, 290
HOOK = (txt(40, 20, 200, '🌙', 90, '#fff', None, 800, 'line-height:1.2')
        + face(FX, FY, .95)
        + beams(690, 120, [(FX + 40, FY - 120), (FX + 120, FY), (FX + 40, FY + 120)], IR)
        + iphone(580, 70, 230, 470, box(40, 130, 150, 40, '', '') + txt(0, 74, 218, '10:08', 46, '#fff', None, 800, 'font-family:Poppins'))
        + padlock(695, 330, 2.2, '#fff', 1.1)
        + txt(560, 560, 270, 'فتح دغري ✅', 40, GRN, '2.6,4.1')
        + txt(560, 560, 270, '؟', 150, YEL, '4.2', 900, 'line-height:1;text-shadow:0 8px 24px rgba(0,0,0,.4)'))

# ------------------------------------------------------------------ 2 · the three hidden parts (TrueDepth)
STRIP_Y = 150


def part(w_in, x, icon, label, sub, col):
    return (box(x, STRIP_Y - 50, 100, 100, f'background:#050b1c;border:5px solid {col};border-radius:50%;box-sizing:border-box;'
                f'display:grid;place-items:center;font-size:52px;box-shadow:0 0 26px rgba({IR},.35)', icon, f'data-in="{w_in}"')
            + chip(w_in, x - 60, STRIP_Y + 90, 220, f'{label}<div style="font-size:22px;color:#cfe3ff;font-weight:700">{sub}</div>', col, 30, pad=12)
            + f'<svg data-in="{w_in}" viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
              f'<path d="M{x + 50} {STRIP_Y + 52} V{STRIP_Y + 88}" stroke="{col}" stroke-width="4" stroke-dasharray="6 6"/></svg>')


PARTS = (box(40, STRIP_Y - 80, 920, 160, f'background:#050b1c;border:5px solid {INK};border-radius:80px;box-sizing:border-box')
         + txt(330, 18, 340, 'فوق الشاشة 📱', 30, '#cfe3ff')
         + part('7.9', 780, '💡', 'ضو مخفي', 'ما بتشوفه بعينك', '#ff8a9a')
         + part('10.1', 450, '✳️', 'بروجكتور', 'صغير كتير', YEL)
         + part('12.7', 120, '📷', 'كاميرا خاصّة', 'بتشوف الأحمر', CYAN)
         + chip('13.75', 520, 480, 450, '🔴 أشعّة تحت الحمرا<div style="font-size:24px;color:#cfe3ff;font-weight:700">العين ما بتشوفها</div>', '#ff8a9a', 36))

# ------------------------------------------------------------------ 3 · flood → 30,000 dots → depth → 3D map
SX, SY, SS = 300, 330, 1.1                       # the face on the scan screen
random.seed(11)


def in_face(x, y):
    return ((x - SX) / (140 * SS)) ** 2 + ((y - SY + 10) / (196 * SS)) ** 2 < 1


DOTS = []
while len(DOTS) < 150:
    x, y = random.uniform(SX - 160, SX + 160), random.uniform(SY - 220, SY + 220)
    if in_face(x, y):
        DOTS.append((x, y))
DOTS.sort(key=lambda p: (p[1], p[0]))
NOSE, EYE = (SX - 6, SY + 40), (SX + 112, SY - 26)
PH = (860, 330)                                  # the phone (seen from the side) on the right

SCAN = (box(SX - 190, SY - 250, 380, 500, f'border-radius:50%;background:radial-gradient(ellipse,rgba({IR},.42),rgba({IR},.1) 60%,transparent 72%)',
            '', 'data-in="16.4,20.0"')
        + face(SX, SY, SS)
        + iphone(PH[0] - 40, PH[1] - 170, 80, 340)
        + beams(PH[0] - 40, PH[1] - 140, [(SX + 150, SY - 180), (SX + 160, SY + 120)], IR, '16.4,19.9')
        + chip('17.6,19.9', 560, 520, 330, 'في وجّ قدّام التلفون؟ ✓', '#ff8a9a', 32)
        + ''.join(box(x - 5, y - 5, 10, 10, f'background:rgb({IR});border-radius:50%;box-shadow:0 0 8px rgba({IR},.9)', '',
                      f'data-in="{20.3 + i * 0.022:.2f}"') for i, (x, y) in enumerate(DOTS))
        + chip('21.5,27.2', 560, 470, 380, f'<div style="font-size:66px;color:{YEL};line-height:1.15;font-family:Poppins" dir="ltr">+30,000</div>'
                                         'نقطة على وجّك', YEL, 34)
        + chip('24.5,27.2', 560, 680, 180, '👁️ ✗', RED, 42) + chip('25.6,27.2', 770, 680, 180, '📷 ✓', GRN, 42)
        # depth: two measuring lines from the phone
        + beams(PH[0] - 40, PH[1] - 10, [NOSE], '92,225,255', '30.0', False)
        + beams(PH[0] - 40, PH[1] - 10, [EYE], '255,213,74', '33.4', False)
        + box(NOSE[0] - 14, NOSE[1] - 14, 28, 28, f'border:5px solid {CYAN};border-radius:50%;box-sizing:border-box', '', 'data-in="30.0"')
        + box(EYE[0] - 14, EYE[1] - 14, 28, 28, f'border:5px solid {YEL};border-radius:50%;box-sizing:border-box', '', 'data-in="33.4"')
        + chip('30.1,35.3', 560, 470, 190, '👃 أقرب', CYAN, 34) + chip('33.5,35.3', 770, 470, 190, '👁️ أبعد', YEL, 34)
        + chip('27.5,35.3', 560, 640, 400, 'الوجّ مش مسطّح ⇠ مسافات مختلفة', '#fff', 28))


def mesh(cx, cy, s=1.0, col=CYAN):
    """Wireframe 3D face map: contour rings + vertical meridians."""
    rings = ''.join(f'<ellipse cx="0" cy="{10 - k * 4}" rx="{146 - k * 24}" ry="{204 - k * 30}"/>' for k in range(6))
    mer = ''.join(f'<path d="M{x} -196 Q{x * 1.25:.0f} 0 {x} 196"/>' for x in (-110, -70, -30, 30, 70, 110))
    hz = ''.join(f'<path d="M-140 {y} Q0 {y + 26} 140 {y}"/>' for y in (-140, -80, -20, 40, 100, 150))
    return (f'<svg viewBox="-200 -240 400 480" style="position:absolute;left:{cx - 200 * s:.0f}px;top:{cy - 240 * s:.0f}px;'
            f'width:{400 * s:.0f}px;height:{480 * s:.0f}px;overflow:visible"><g fill="none" stroke="{col}" stroke-width="2.6" opacity=".9">'
            f'{rings}{mer}{hz}<path d="M0 -10 L-18 66 Q0 80 20 66" stroke-width="5"/><ellipse cx="-64" cy="-16" rx="22" ry="12" stroke-width="4"/>'
            f'<ellipse cx="64" cy="-16" rx="22" ry="12" stroke-width="4"/></g></svg>')


NUMS = '0.42 · 1.87 · 3.05 · 0.91 · 2.64 · 1.12 · 4.38 · 0.77 · 2.09 · 3.51 · 1.46 · 0.28 · '
MAP = (f'<div data-keys="0,0,0,0,1;36.0,0,0,0,1;39.8,0,0,-8,1;41.6,0,0,8,1" style="position:absolute;left:0;top:0;width:1000px;height:900px">'
       + mesh(SX, SY, SS) + '</div>'
       + chip('36.0', 560, 120, 380, f'<div style="font-size:60px;color:{CYAN};line-height:1.2;font-family:Poppins">3D</div>خريطة لوجّك', CYAN, 34)
       # numbers stream into the secure chip
       + box(560, 400, 400, 60, f'{PANEL};border:3px solid {INK};border-radius:30px;overflow:hidden',
             f'<div data-scroll="-120,0" style="position:absolute;inset:0;background-image:none"></div>'
             f'<div data-keys="0,0,0;39.9,0,0;45.8,-700,0" data-ease="linear" style="position:absolute;left:14px;top:8px;white-space:nowrap;'
             f'font-family:Poppins;font-size:30px;font-weight:700;color:#bfe9ff">{NUMS * 3}</div>', 'data-in="39.9"')
       + txt(560, 470, 400, '↓', 54, '#fff', '41.9', 900, 'line-height:1')
       + box(640, 540, 240, 170, f'background:#0b1d4a;border:5px solid {YEL};border-radius:24px;box-sizing:border-box;'
             'box-shadow:0 0 30px rgba(255,213,74,.35)',
             ''.join(box(26 + i * 50, -18, 16, 18, f'background:{INK};border-radius:4px 4px 0 0') + box(26 + i * 50, 166, 16, 18, f'background:{INK};border-radius:0 0 4px 4px') for i in range(4))
             + txt(0, 26, 230, '🔒', 54, '#fff', None, 800, 'line-height:1.2') + txt(0, 96, 230, 'شريحة آمنة', 30, YEL), 'data-in="42.2"')
       + box(560, 740, 400, 96, f'{PANEL};border:4px solid {GRN};border-radius:26px;display:grid;place-items:center',
             txt(0, 18, 400, '✅ تطابق! بيفتح دغري', 36, GRN), 'data-in="46.1"')
       + padlock(920, 625, 46.3, '#fff', .8))

# ------------------------------------------------------------------ 4 · privacy: nothing leaves the phone
PRIV = (iphone(120, 120, 250, 500, txt(0, 150, 238, '🛡️', 110, '#fff', None, 800, 'line-height:1.2')
                + txt(0, 300, 238, 'المعالجة<br>جوّا التلفون', 30, GRN))
        + f'<svg data-in="48.4" viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
          f'<path d="M380 300 Q560 200 700 230" stroke="rgba(233,241,255,.7)" stroke-width="5" stroke-dasharray="14 12" fill="none"/></svg>'
        + txt(700, 120, 260, '☁️', 150, '#fff', '48.3', 800, 'line-height:1.2')
        + txt(700, 300, 260, 'سيرفر برّا', 32, '#cfe3ff', '48.3')
        + txt(500, 196, 120, '✗', 120, RED, '50.6', 900, 'line-height:1;text-shadow:0 6px 18px rgba(0,0,0,.45)')
        + chip('51.2', 560, 470, 400, 'ملامح وجّك ما بتنبعت<br>ولا بتنحفظ برّا 🔒', GRN, 32))

# ------------------------------------------------------------------ 5 · a photo can't fool it; beard + glasses still work
SPOOF = (box(80, 80, 300, 380, f'background:#e9f1ff;border:10px solid #fff;box-sizing:border-box;transform:rotate(-6deg);'
             'box-shadow:0 14px 30px rgba(0,0,0,.4)', face(140, 180, .62, stroke='#1b3f8f'), 'data-in="-1,61.0"')
         + txt(60, 470, 340, 'صورة مسطّحة 🖼️', 34, '#fff', '-1,61.0')
         + txt(140, 140, 200, '✗', 220, RED, '58.0,61.0', 900, 'line-height:1;text-shadow:0 8px 24px rgba(0,0,0,.45)')
         + chip('59.0,61.0', 560, 120, 400, 'ما فيها عمق ⇠ ما بتخدعه بسهولة', RED, 30)
         + face(300, 330, 1.0, beard=True, glasses=True).replace('<svg ', '<svg data-in="61.2" ')
         + chip('61.9', 600, 120, 360, '🧔 دقن', CYAN, 34) + chip('62.8', 600, 230, 360, '👓 نضّارات', CYAN, 34)
         + chip('64.0', 600, 360, 360, 'بيتعرّف عليك ✅', GRN, 36))

# ------------------------------------------------------------------ 6 · recap: your face is the password
RECAP = (face(300, 320, 1.0)
         + chip('66.0', 540, 160, 420, f'<div style="font-size:44px;color:{YEL}">وجّك =</div>'
                                       f'<div style="font-size:64px;font-family:Poppins;color:#fff;line-height:1.2" dir="ltr">🔑 password</div>', YEL, 34)
         + padlock(750, 470, 66.9, '#fff', 1.0))

SPEC = {
    'audio': 'host/voices/faceid.flac', 'lang': 'ar', 'device': 'stage',
    'title': 'كيف بيعرفك الآيفون من وجّك؟ 🔓', 'tag': 'iPHONE · FACE ID · TRUEDEPTH', 'tip': 'TECH #04',
    'start': 'hook',
    'screens': {
        'hook': {'type': 'html', 'bg': 'transparent', 'html': HOOK},
        'parts': {'type': 'html', 'bg': 'transparent', 'html': PARTS},
        'scan': {'type': 'html', 'bg': 'transparent', 'html': SCAN},
        'map': {'type': 'html', 'bg': 'transparent', 'html': MAP},
        'priv': {'type': 'html', 'bg': 'transparent', 'html': PRIV},
        'spoof': {'type': 'html', 'bg': 'transparent', 'html': SPOOF},
        'recap': {'type': 'html', 'bg': 'transparent', 'html': RECAP},
    },
    'beats': [
        {'t': [0.04, 4.02], 'say': 'لك، بتطلّع بتلفونك، بيفتح دغري، حتى بالعتمة!',
         'cap': 'بتطلّع بتلفونك… بيفتح دغري، حتى بالعتمة 🔓', 'capsize': 84, 'pose': 'welcome', 'hook': True},
        {'t': [4.22, 6.17], 'say': 'طيّب، كيف عرف إنّو هيدا وجّك؟',
         'cap': 'طيّب، كيف عرف إنّو هيدا وجّك؟ 🤔', 'pose': 'talk'},
        {'t': [6.37, 13.46], 'say': 'فوق الشاشة في تلات قطع مخبّايين: ضو ما بتشوفه بعينك، بروجكتور صغير كتير، وكاميرا خاصّة.',
         'cap': 'فوق الشاشة 3 قطع مخبّايين: ضو مخفي، بروجكتور صغير، وكاميرا خاصّة', 'pose': 'point',
         'screen': 'parts', 'style': 'fade'},
        {'t': [13.66, 16.11], 'say': 'والتلاتة بيشتغلوا بالأشعّة تحت الحمرا.',
         'cap': 'والتلاتة بيشتغلوا بالأشعّة تحت الحمرا 🔴', 'pose': 'talk'},
        {'t': [16.31, 19.70], 'say': 'أوّل شي، الضو بيكشف إذا في وجّ قدّام التلفون.',
         'cap': 'أوّل شي: الضو بيكشف إذا في وجّ قدّام التلفون', 'pose': 'point', 'step': 1,
         'screen': 'scan', 'style': 'fade'},
        {'t': [19.90, 24.22], 'say': 'بعدين البروجكتور بيرسم على وجّك أكتر من تلاتين ألف نقطة.',
         'cap': 'بعدين البروجكتور بيرسم على وجّك أكتر من 30,000 نقطة', 'pose': 'point', 'step': 2},
        {'t': [24.42, 27.17], 'say': 'إنت ما بتشوفن، بس الكاميرا بتشوفن كلّن.',
         'cap': 'إنت ما بتشوفن، بس الكاميرا بتشوفن كلّن 📷', 'pose': 'talk'},
        {'t': [27.37, 35.27], 'say': 'وبما إنّو وجّك مش مسطّح، هالنقاط بتطلع بمسافات مختلفة: عند المنخار بتكون أقرب، وبجنب العين أبعد.',
         'cap': 'وجّك مش مسطّح: عند المنخار النقاط أقرب، وبجنب العين أبعد', 'pose': 'point'},
        {'t': [35.47, 39.68], 'say': 'ومن هالفرق، التلفون بيرسم خريطة تلاتيّة الأبعاد لوجّك.',
         'cap': 'ومن هالفرق: خريطة 3D لوجّك 🗺️', 'pose': 'welcome', 'step': 3,
         'screen': 'map', 'style': 'fade'},
        {'t': [39.88, 45.82], 'say': 'هيدي الخريطة بتتحوّل لأرقام، والتلفون بيقارنها مع الأرقام المحفوظة بشريحة آمنة جوّاتو.',
         'cap': 'الخريطة بتصير أرقام، وبتنقارن بشريحة آمنة جوّا التلفون 🔒', 'pose': 'point', 'step': 4},
        {'t': [46.02, 47.47], 'say': 'إذا تطابقت، بيفتح دغري.',
         'cap': 'إذا تطابقت: بيفتح دغري ✅', 'pose': 'welcome'},
        {'t': [47.67, 55.64], 'say': 'والأحلى، إنّو ملامح وجّك ما بتنبعت ولا بتنحفظ عند أي سيرفر برّا، لأنّو المعالجة بتصير جوّا التلفون.',
         'cap': 'والأحلى: ملامح وجّك ما بتطلع لأي سيرفر، كل شي جوّا التلفون 🛡️', 'pose': 'talk',
         'screen': 'priv', 'style': 'fade'},
        {'t': [55.84, 60.94], 'say': 'كمان، هيك صورة ما بتقدر تخدعه بسهولة، لأنّها مسطّحة وما فيها عمق.',
         'cap': 'صورة ما بتخدعه بسهولة: مسطّحة وما فيها عمق 🖼️', 'pose': 'point', 'screen': 'spoof', 'style': 'fade'},
        {'t': [61.14, 65.56], 'say': 'وحتى لو ربّيت دقنك أو لبست نضّارات، النظام بيقدر يتعرّف عليك.',
         'cap': 'ولو ربّيت دقنك أو لبست نضّارات، بيتعرّف عليك 🧔👓', 'pose': 'talk'},
        {'t': [65.76, 68.38], 'say': 'يعني باختصار، وجّك هو الـ password.',
         'cap': 'يعني باختصار: وجّك هو الـpassword 🔑', 'pose': 'welcome', 'screen': 'recap', 'style': 'fade'},
        {'t': [68.58, 69.72], 'say': 'تابعونا على Tech Wall.',
         'cap': 'تابعونا على Tech Wall 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

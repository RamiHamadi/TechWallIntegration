"""Tech Wall HOST explainer (Arabic) with a supplied voice-over: how the phone's flashlight (LED flash) works.
    ./build.sh flashlight  |  python3 flashlight.py 0 150 400
No device: 'stage' = a frameless illustration area above the host, drawn in the blueprint style (template teslaflip.py).
Voice: the user's Lebanese-Arabic generated audio, pauses between phrases shortened to 0.2 s (host/voices/flashlight.flac);
beat 't' = [start, end] s in it (phrase times measured, script transcribed with the multilingual Whisper turbo model
from the sherpa-onnx GitHub releases, language 'ar').
Facts: a white LED is a blue InGaN LED under a yellow phosphor (YAG:Ce) that converts part of the blue to yellow, and
blue + yellow looks white; light comes from electrons recombining with holes at the junction; a flash-driver IC sets the
LED current (short high-current pulse for photos, lower continuous current in torch mode) and reduces it when hot.
The voice says "millions per second"; the real number of recombinations is far higher, so the card adds "and far more".
Generic drawings, no logos. Motion: data-keys, data-in, data-scroll (flowing dashes), data-spin, data-bob, data-ring."""
import random
import host

EP = 'flashlight'
INK, CYAN, YEL, RED, BLUE, GRN = '#e9f1ff', '#5ce1ff', '#ffd54a', '#ff6b6b', '#3d8bff', '#34d399'
AR = 'font-family:Cairo,Poppins,sans-serif'
PANEL = 'background:rgba(6,20,52,.86);box-shadow:0 12px 30px rgba(0,0,0,.35)'


def box(x, y, w, h, style='', inner='', attr=''):
    return f'<div {attr} style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}">{inner}</div>'


def win(w):
    return f'data-in="{w}"' if w else ''


def txt(x, y, w, s, size=30, col='#fff', w_in=None, weight=800, extra=''):
    return (f'<div {win(w_in)} dir="rtl" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:center;'
            f'font-size:{size}px;font-weight:{weight};color:{col};line-height:1.3;{AR};{extra}">{s}</div>')


def chip(w_in, x, y, w, s, col=YEL, size=32, strike=False, pad=16):
    st = (f'<div style="position:absolute;left:-8px;right:-8px;top:50%;height:7px;background:{RED};transform:rotate(-7deg)"></div>'
          if strike else '')
    return (f'<div {win(w_in)} dir="rtl" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;box-sizing:border-box;{PANEL};'
            f'border:3px solid {col};border-radius:22px;padding:{pad}px 10px;text-align:center;font-size:{size}px;font-weight:800;'
            f'line-height:1.3;{AR}">{s}{st}</div>')


def flow(x, y, w, h, col, v=130, w_in=None, dash=16):
    """A band of dashes that flows to the right (v px/s; negative = to the left)."""
    return (f'<div {win(w_in)} data-scroll="{v},0" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background-image:linear-gradient(90deg,{col} 58%,transparent 58%);background-size:{2 * dash}px 100%;'
            f'border-radius:{h / 2:.0f}px"></div>')


def mover(keys, w, h, inner, style='', ease=''):
    e = ' data-ease="linear"' if ease == 'linear' else ''
    return (f'<div data-keys="{keys}"{e} style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;'
            f'margin:-{h / 2:.0f}px 0 0 -{w / 2:.0f}px;{style}">{inner}</div>')


def glow(x, y, d, col='255,236,170', w_in=None, a=.95):
    return (f'<div {win(w_in)} style="position:absolute;left:{x - d / 2:.0f}px;top:{y - d / 2:.0f}px;width:{d}px;height:{d}px;border-radius:50%;'
            f'background:radial-gradient(circle,rgba(255,255,255,{a}) 0 10%,rgba({col},.75) 24%,rgba({col},.22) 46%,transparent 68%)"></div>')


def rays(x, y, d, col='255,236,170', spin=14):
    return (f'<div data-spin="{spin}" style="position:absolute;left:{x - d / 2:.0f}px;top:{y - d / 2:.0f}px;width:{d}px;height:{d}px;border-radius:50%;'
            f'background:repeating-conic-gradient(rgba({col},.6) 0 5deg,transparent 5deg 30deg);'
            '-webkit-mask-image:radial-gradient(circle,transparent 0 16%,#000 22%,transparent 68%);'
            'mask-image:radial-gradient(circle,transparent 0 16%,#000 22%,transparent 68%)"></div>')


def spark(w_in, x, y, s=96, col='140,190,255'):
    return (f'<div data-in="{w_in}" style="position:absolute;left:{x - s / 2:.0f}px;top:{y - s / 2:.0f}px;width:{s}px;height:{s}px;'
            f'border-radius:50%;background:radial-gradient(circle,#fff 0 16%,rgba({col},.9) 30%,rgba({col},.25) 52%,transparent 68%);'
            f'display:grid;place-items:center;font-size:{s * .5:.0f}px;color:#fff;line-height:1">✦</div>')


def battery(x, y, w=170, h=84, level=3):
    cells = ''.join(box(10 + i * ((w - 26) / 4), 10, (w - 26) / 4 - 6, h - 26, f'background:{GRN};border-radius:6px') for i in range(level))
    return (box(x, y, w, h, f'border:5px solid {INK};border-radius:16px;box-sizing:border-box;background:rgba(6,20,52,.7)', cells)
            + box(x + w, y + h / 2 - 16, 12, 32, f'background:{INK};border-radius:0 6px 6px 0'))


def led_lamp(x, y, s=96, on=True):
    """Small LED package seen from above: yellow phosphor square in a white frame."""
    return box(x - s / 2, y - s / 2, s, s, f'border:5px solid {INK};border-radius:20px;box-sizing:border-box;background:#f4f1e6',
               box(s * .16, s * .16, s * .58, s * .58, 'background:linear-gradient(135deg,#ffe27a,#ffc93a);border-radius:10px'))


# ------------------------------------------------------------------ 1 · phone back, the yellow square, "LED"
PX, PY = 330, 340                                # phone centre
FX, FY = PX - 34, PY - 234                       # the flash on the phone back


def phone_back():
    cam = (box(26, 26, 150, 150, 'background:#0b1d4a;border:3px solid rgba(233,241,255,.7);border-radius:38px;box-sizing:border-box',
               ''.join(box(lx, ly, 54, 54, 'border-radius:50%;background:radial-gradient(circle,#27407e 0 30%,#060f2a 34% 60%,#3a4c7a 64%)')
                       for lx, ly in [(12, 12), (12, 78)])
               + box(88, 16, 40, 40, 'background:linear-gradient(135deg,#ffe27a,#ffc93a);border-radius:10px;border:2px solid #fff3c4;box-sizing:border-box')
               + box(102, 96, 12, 12, 'background:#1c2f66;border-radius:50%')))
    return box(PX - 170, PY - 300, 340, 600, f'border:5px solid {INK};border-radius:54px;box-sizing:border-box;'
               'background:linear-gradient(160deg,#1b3f8f,#0f2a66)', cam)


def bubble():
    """Magnifier on the camera corner: the small yellow square = the LED."""
    inner = (box(-40, 40, 230, 230, 'border-radius:50%;background:radial-gradient(circle,#27407e 0 30%,#060f2a 34% 60%,#3a4c7a 64%)')
             + box(-70, 290, 200, 200, 'border-radius:50%;background:radial-gradient(circle,#27407e 0 30%,#060f2a 34% 60%,#3a4c7a 64%)')
             + box(190, 120, 150, 150, 'background:linear-gradient(135deg,#ffe27a,#ffc93a);border-radius:34px;border:5px solid #fff3c4;box-sizing:border-box',
                   box(52, 52, 36, 36, 'background:#e8b62a;border-radius:8px;border:2px solid #c9961a;box-sizing:border-box')))
    return (f'<svg data-in="5.0" viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
            f'<path d="M{FX + 16} {FY - 12} L640 140 M{FX + 16} {FY + 16} L610 430" stroke="{INK}" stroke-width="3" stroke-dasharray="10 10" fill="none"/></svg>'
            + box(560, 100, 400, 400, f'border:6px solid {INK};border-radius:50%;box-sizing:border-box;overflow:hidden;background:#0b1d4a;'
                  'box-shadow:0 14px 34px rgba(0,0,0,.4)', inner, 'data-in="5.05"')
            + box(736, 206, 178, 178, f'border:6px dashed {YEL};border-radius:42px;box-sizing:border-box', '', 'data-in="5.7"'))


S1 = (rays(FX, FY, 620) + phone_back() + glow(FX, FY, 330)
      + txt(600, 110, 320, '؟', 230, YEL, '-1,4.75', 900, 'text-shadow:0 8px 24px rgba(0,0,0,.4);line-height:1')
      + txt(560, 400, 400, 'من وين جايي هالضو؟', 38, '#fff', '-1,4.75')
      + bubble()
      + chip('7.1,8.85', 580, 540, 360, '💡 لمبة عاديّة', RED, 38, True)
      + txt(560, 505, 400, '<span dir="ltr">LED</span>', 120, YEL, '9.0', 900, 'line-height:1.1;font-family:Poppins;letter-spacing:6px')
      + chip('9.9', 780, 668, 190, '⚡ كهربا', CYAN, 34)
      + txt(722, 676, 56, '←', 50, '#fff', '10.9', 900, 'line-height:1')
      + chip('11.3', 470, 668, 250, '💡 ضو دغري', YEL, 34))

# ------------------------------------------------------------------ 2 · inside the LED: electrons fall into holes
EL = [(190, 402), (300, 508), (170, 526), (335, 422), (250, 470)]          # electrons (left, N side)
HO = [(650, 402), (770, 508), (830, 410), (700, 520), (600, 470)]          # holes (right, P side)
GO = [(20.2, 20.9), (21.0, 21.7), (22.1, 22.8), (22.9, 23.5), (23.5, 24.0)]
random.seed(4)
MANY = [(random.uniform(23.95, 25.6), random.randint(140, 860), random.randint(360, 560)) for _ in range(22)]

E_DOT = (f'<div data-bob="3" style="width:42px;height:42px;border-radius:50%;background:{CYAN};color:#0a2b66;display:grid;'
         'place-items:center;font-size:34px;font-weight:900;line-height:1;box-shadow:0 0 14px rgba(92,225,255,.8)">−</div>')

S2 = (box(40, 70, 150, 150, f'border:6px solid {YEL};border-radius:50%;box-sizing:border-box;{PANEL};display:grid;place-items:center;font-size:76px',
          '🔦', 'data-id="btn"')
      + f'<svg viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
        f'<path d="M196 145 H256" stroke="{INK}" stroke-width="4" stroke-dasharray="8 8"/>'
        f'<path d="M496 145 H770" stroke="rgba(233,241,255,.45)" stroke-width="4"/></svg>'
      + battery(260, 92, 220, 106) + txt(260, 204, 220, 'بطّاريّة', 30, '#cfe3ff')
      + flow(496, 131, 274, 28, CYAN, 150, '14.5')
      + glow(840, 145, 300, '255,236,170', '15.0') + led_lamp(840, 145, 130) + txt(760, 214, 160, '<span dir="ltr">LED</span>', 30, '#cfe3ff', None, 800, 'font-family:Poppins')
      # the die, zoomed
      + f'<svg data-in="16.2" viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
        f'<path d="M780 214 L80 310 M902 214 L920 310" stroke="{INK}" stroke-width="3" stroke-dasharray="10 10" fill="none"/></svg>'
      + box(80, 310, 840, 290, f'border:5px solid {INK};border-radius:30px;box-sizing:border-box;overflow:hidden;'
            'background:linear-gradient(90deg,rgba(92,225,255,.16) 0 50%,rgba(255,213,74,.16) 50% 100%)',
            box(412, 0, 0, 290, f'border-left:4px dashed {INK}'), 'data-in="16.25"')
      + txt(100, 322, 300, 'إلكترونات', 30, CYAN, '16.6') + txt(600, 322, 300, 'فراغات', 30, YEL, '17.9')
      + ''.join(box(hx - 26, hy - 26, 52, 52, f'border:4px dashed {YEL};border-radius:50%;box-sizing:border-box', '', f'data-in="{17.9 + i * .12:.2f}"')
                for i, (hx, hy) in enumerate(HO))
      + ''.join(f'<div data-in="{16.6 + i * .1:.2f}" style="position:absolute;inset:0">'
                + mover(f'0,{ex},{ey};{a},{ex},{ey};{b},{hx},{hy}', 42, 42, E_DOT) + '</div>'
                for i, ((ex, ey), (hx, hy), (a, b)) in enumerate(zip(EL, HO, GO)))
      + ''.join(spark(f'{b:.2f},{b + .6:.2f}', hx, hy, 130) for (hx, hy), (a, b) in zip(HO, GO))
      + ''.join(spark(f'{t:.2f},{t + .32:.2f}', x, y, 70) for t, x, y in MANY)
      + chip('20.2,23.85', 490, 630, 480, '<span style="color:#5ce1ff">⊖ إلكترون</span> + <span style="color:#ffd54a">◯ فراغ</span> = ✨ ضو', '#fff', 30)
      + chip('24.0', 520, 630, 450, f'<div style="font-size:50px;color:{YEL};line-height:1.2">ملايين بالثانية ⚡</div>'
                                    '<div style="font-size:24px;color:#cfe3ff;font-weight:700">وبالحقيقة أكتر بكتير!</div>', YEL, 32))

# ------------------------------------------------------------------ 3 · blue light + yellow phosphor = white
BY = 300                                         # beam axis


def lane(x, y, w, col, w_in=None, v=170):
    return flow(x, y, w, 20, col, v, w_in, 14)


S3 = (glow(130, BY, 300, '70,140,255')
      + box(60, BY - 60, 140, 120, f'border:5px solid {INK};border-radius:22px;box-sizing:border-box;background:linear-gradient(135deg,#4a93ff,#1f55d6);'
            'display:grid;place-items:center;font-size:40px;font-weight:900;font-family:Poppins;letter-spacing:3px', 'LED')
      + lane(206, BY - 24, 664, BLUE) + lane(206, BY + 4, 664, BLUE)
      # the yellow lane wipes in from the phosphor, over the lower blue lane
      + box(540, BY + 4, 330, 20, 'overflow:hidden;border-radius:10px',
            f'<div data-keys="0,-340,0;32.3,-340,0;33.3,0,0" style="position:absolute;left:0;top:0;width:330px;height:20px">'
            + box(0, 0, 330, 20, 'background:#12306f') + lane(0, 0, 330, YEL) + '</div>')
      + chip('26.15,27.15', 380, 70, 300, 'المفاجأة! 😲', YEL, 40)
      + txt(250, 60, 560, 'الضو الأصلي: <span style="color:#7db4ff">أزرق</span> 🔵', 50, '#fff', '27.3,29.4', 900)
      + mover(f'0,505,-260;29.5,505,-260;30.3,505,{BY}', 76, 280,
              box(0, 0, 76, 280, 'background:linear-gradient(180deg,#ffe27a,#ffc93a);border:4px solid #fff3c4;border-radius:20px;'
                  'box-sizing:border-box;box-shadow:0 0 30px rgba(255,213,74,.55)'))
      + txt(385, 96, 240, 'فوسفور', 42, YEL, '30.9', 900)
      + txt(545, 200, 400, 'شوي من الأزرق ← أصفر', 30, '#fff', '32.6,37.6')
      + glow(934, BY, 250, '255,255,255', '36.0', .8)
      + txt(880, BY - 62, 110, '👁️', 96, '#fff', '34.6', 800, 'line-height:1.25')
      + chip('34.95', 835, 500, 140, '🔵<br>أزرق', BLUE, 30, False, 10)
      + txt(790, 528, 44, '+', 50, '#fff', '35.3', 900, 'line-height:1')
      + chip('35.35', 650, 500, 140, '🟡<br>أصفر', YEL, 30, False, 10)
      + txt(605, 528, 44, '=', 50, '#fff', '36.0', 900, 'line-height:1')
      + chip('36.05', 440, 500, 164, '⚪<br>أبيض', '#fff', 30, False, 10))

# ------------------------------------------------------------------ 4 · the driver chip = a tap for the current
CY4 = 250
PINS = ''.join(box(18 + i * 36, -16, 14, 16, f'background:{INK};border-radius:4px 4px 0 0') + box(18 + i * 36, 150, 14, 16, f'background:{INK};border-radius:0 0 4px 4px')
               for i in range(4))
S4 = (f'<svg viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
      f'<path d="M232 {CY4} H790" stroke="rgba(233,241,255,.45)" stroke-width="4"/></svg>'
      + battery(50, CY4 - 42) + txt(40, CY4 + 52, 190, 'بطّاريّة', 26, '#cfe3ff')
      + mover(f'0,850,{CY4},0,1;43.3,850,{CY4},0,1;44.1,850,{CY4},0,1.75;45.1,850,{CY4},0,1.75;45.9,850,{CY4},0,.62', 240, 240,
              glow(120, 120, 240))
      + led_lamp(850, CY4) + txt(770, CY4 + 58, 160, '<span dir="ltr">LED</span>', 26, '#cfe3ff', None, 800, 'font-family:Poppins')
      + flow(236, CY4 - 9, 180, 18, CYAN, 130, '41.5') + flow(588, CY4 - 9, 204, 18, CYAN, 130, '41.5')
      + flow(236, CY4 - 30, 180, 14, '#bff3ff', 260, '43.5,45.1', 12) + flow(588, CY4 - 30, 204, 14, '#bff3ff', 260, '43.5,45.1', 12)
      + flow(236, CY4 + 16, 180, 14, '#bff3ff', 260, '43.6,45.1', 12) + flow(588, CY4 + 16, 204, 14, '#bff3ff', 260, '43.6,45.1', 12)
      + box(420, CY4 - 75, 164, 150, f'border:5px solid {INK};border-radius:20px;box-sizing:border-box;background:#0b1d4a;'
            'box-shadow:0 12px 30px rgba(0,0,0,.35)', PINS + txt(0, 30, 154, 'شريحة<br>التحكّم', 30, '#fff'), 'data-in="39.5"')
      + txt(440, 30, 120, '🚰', 100, '#fff', '40.7', 800, 'line-height:1.2')
      # brightness slider
      + box(540, 520, 420, 150, f'{PANEL};border:3px solid {CYAN};border-radius:26px;box-sizing:border-box',
            txt(0, 12, 414, 'قوّة الضو', 28, '#cfe3ff')
            + box(70, 86, 280, 14, 'background:rgba(233,241,255,.3);border-radius:7px')
            + txt(8, 62, 60, '🔅', 40) + txt(352, 60, 60, '🔆', 44)
            + mover('0,180,93;43.3,180,93;44.1,330,93;45.1,330,93;45.9,120,93', 46, 46,
                    box(0, 0, 46, 46, f'background:{YEL};border-radius:50%;border:4px solid #fff;box-sizing:border-box;box-shadow:0 4px 12px rgba(0,0,0,.4)')),
            'data-in="43.25"')
      + txt(540, 690, 420, 'بتفتح أكتر ← ضو أقوى', 32, YEL, '43.9,45.1')
      + txt(540, 690, 420, 'بتسكّر شوي ← ضو أخفّ', 32, CYAN, '45.5'))

# ------------------------------------------------------------------ 5 · photo pulse vs steady torch, heat protection


def graph(x, w_in, title, path, col, note, extra=''):
    return (f'<div {win(w_in)} style="position:absolute;left:{x}px;top:40px;width:440px;height:350px;{PANEL};border:3px solid {col};'
            'border-radius:28px;box-sizing:border-box">'
            + txt(0, 10, 434, title, 32, '#fff')
            + f'<svg viewBox="0 0 440 350" style="position:absolute;inset:0;width:440px;height:350px">'
              f'<path d="M50 70 V290 H410" stroke="rgba(233,241,255,.6)" stroke-width="4" fill="none"/>'
              f'<path d="{path}" stroke="{col}" stroke-width="8" fill="none" stroke-linejoin="round" stroke-linecap="round"/>{extra}</svg>'
            + txt(0, 296, 434, note, 26, col) + '</div>')


S5 = (graph(40, '46.95', '📸 تصوير (فلاش)', 'M54 286 H200 V96 H236 V286 H400', YEL, 'دفشة قويّة · جزء من الثانية')
      + spark('48.0,48.7', 258, 150, 300, '255,240,190')
      + graph(520, '50.4', '🔦 بيل', 'M54 220 H250', CYAN, 'ضو أهدى · ثابت',
              f'<path d="M250 220 H400" stroke="{CYAN}" stroke-width="8" stroke-linecap="round" stroke-dasharray="2 16" opacity=".5"/>')
      + f'<svg data-in="55.0" viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
        f'<path d="M770 260 V298 H920" stroke="{RED}" stroke-width="8" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>'
      + box(540, 430, 430, 300, f'{PANEL};border:3px solid {RED};border-radius:28px;box-sizing:border-box',
            box(40, 30, 44, 200, 'background:rgba(233,241,255,.2);border:4px solid #fff;border-radius:22px;box-sizing:border-box;overflow:hidden',
                f'<div data-ring="53.5,57.2" style="position:absolute;left:0;right:0;bottom:0;height:calc(18% + var(--p,0) * 82%);background:{RED}"></div>')
            + box(26, 214, 72, 72, f'background:{RED};border:4px solid #fff;border-radius:50%;box-sizing:border-box')
            + txt(120, 28, 290, '📱🔥', 70, '#fff', None, 800, 'line-height:1.2')
            + txt(120, 136, 290, 'حمي التلفون؟', 34, '#fff')
            + txt(120, 190, 290, 'الضو بيوطى لحاله 🛡️', 30, YEL),
            'data-in="53.4"'))

# ------------------------------------------------------------------ 6 · recap


def big(w_in, x, num, icon, title, col):
    return (f'<div data-in="{w_in}" dir="rtl" style="position:absolute;left:{x}px;top:210px;width:300px;height:330px;{PANEL};'
            f'border:4px solid {col};border-radius:30px;text-align:center;box-sizing:border-box;padding-top:18px;{AR}">'
            f'<div style="font-size:44px;font-weight:900;color:{col};line-height:1.2">{num}</div>'
            f'<div style="font-size:96px;line-height:1.25">{icon}</div>'
            f'<div style="font-size:32px;font-weight:800;line-height:1.3">{title}</div></div>')


S6 = (rays(500, 100, 330, '255,236,170', 20) + glow(500, 100, 210) + txt(440, 40, 120, '🔦', 90, '#fff', None, 800, 'line-height:1.3')
      + big('57.1', 670, '①', '🔵', '<span dir="ltr">LED</span> أزرق', BLUE)
      + big('57.6', 350, '②', '🟡', 'طبقة فوسفور', YEL)
      + big('58.1', 30, '③', '🚰', 'شريحة التحكّم', CYAN))

SPEC = {
    'audio': 'host/voices/flashlight.flac', 'lang': 'ar', 'device': 'stage',
    'title': 'كيف بيشتغل فلاش التلفون؟ 🔦', 'tag': 'LED · PHOSPHOR · DRIVER CHIP', 'tip': 'TECH #03',
    'start': 'phone',
    'screens': {
        'phone': {'type': 'html', 'bg': 'transparent', 'html': S1},
        'inside': {'type': 'html', 'bg': 'transparent', 'html': S2},
        'white': {'type': 'html', 'bg': 'transparent', 'html': S3},
        'driver': {'type': 'html', 'bg': 'transparent', 'html': S4},
        'modes': {'type': 'html', 'bg': 'transparent', 'html': S5},
        'recap': {'type': 'html', 'bg': 'transparent', 'html': S6},
    },
    'beats': [
        {'t': [0.30, 4.75], 'say': 'كل يوم منضوّي فلاش التلفون، بس عمرك سألت حالك من وين جايي هالضو؟',
         'cap': 'من وين جايي ضو فلاش التلفون؟ 🔦', 'capsize': 84, 'pose': 'welcome', 'hook': True},
        {'t': [4.95, 8.74], 'say': 'حدّ الكاميرا في مربّع أصفر صغير. هيدا مش لمبة عاديّة،',
         'cap': 'حدّ الكاميرا في مربّع أصفر صغير… مش لمبة عاديّة!', 'pose': 'point'},
        {'t': [8.94, 12.99], 'say': 'هيدا LED: قطعة إلكترونيّة بتحوّل الكهربا لضو دغري.',
         'cap': 'هيدا LED: قطعة إلكترونيّة بتحوّل الكهربا لضو دغري ⚡', 'pose': 'talk', 'step': 1},
        {'t': [13.19, 16.01], 'say': 'لمّا تكبس الزرّ، البطّاريّة بتبعت تيّار.',
         'cap': 'بتكبس الزرّ: البطّاريّة بتبعت تيّار 🔋', 'pose': 'point', 'screen': 'inside', 'style': 'fade',
         'do': [{'tap': 'btn', 'at': .12}]},
        {'t': [16.21, 19.90], 'say': 'جوّا الـLED، الإلكترونات بتلتقى بفراغات ناطرتُن.',
         'cap': 'جوّا الـLED: الإلكترونات بتلاقي فراغات ناطرتها', 'pose': 'talk'},
        {'t': [20.10, 23.74], 'say': 'وكل ما واحد يوقع بمطرحه، بتطلع شرارة ضو صغيرة.',
         'cap': 'كل ما واحد يوقع بمطرحه: شرارة ضو صغيرة ✨', 'pose': 'point'},
        {'t': [23.94, 25.92], 'say': 'ملايين منّن بالثانية.',
         'cap': 'ملايين منها بالثانية! 🤯', 'pose': 'welcome'},
        {'t': [26.12, 29.26], 'say': 'بس المفاجأة: الضو الأصلي لونه أزرق.',
         'cap': 'المفاجأة: الضو الأصلي لونه أزرق 🔵', 'pose': 'welcome', 'screen': 'white', 'style': 'fade'},
        {'t': [29.46, 34.72], 'say': 'لهيك فوقه طبقة صفرا اسمها فوسفور، بتاخد شوي من الأزرق وبتحوّله أصفر.',
         'cap': 'فوقه طبقة فوسفور صفرا: بتحوّل شوي من الأزرق لأصفر 🟡', 'pose': 'point', 'step': 2},
        {'t': [34.92, 37.46], 'say': 'أزرق مع أصفر، عينك بتشوفه أبيض.',
         'cap': 'أزرق + أصفر = عينك بتشوفه أبيض ⚪', 'pose': 'talk'},
        {'t': [37.66, 43.04], 'say': 'وبين البطّاريّة والـLED في شريحة صغيرة، متل الحنفيّة، بتتحكّم بكمّيّة التيّار.',
         'cap': 'بين البطّاريّة والـLED: شريحة متل الحنفيّة بتتحكّم بالتيّار 🚰', 'pose': 'point', 'step': 3,
         'screen': 'driver', 'style': 'fade'},
        {'t': [43.24, 46.71], 'say': 'بتعلّي الضو، بتفتح أكتر. بتوطّي، بتسكّر شوي.',
         'cap': 'بتعلّي الضو: بتفتح أكتر · بتوطّي: بتسكّر شوي', 'pose': 'talk'},
        {'t': [46.91, 50.17], 'say': 'بالتصوير، بيضرب دفشة قويّة لجزء من الثانية.',
         'cap': 'بالتصوير: دفشة قويّة لجزء من الثانية 📸', 'pose': 'point', 'screen': 'modes', 'style': 'fade'},
        {'t': [50.37, 53.16], 'say': 'ولمّا تستعمله بيل: ضو أهدى بس ثابت.',
         'cap': 'ولمّا تستعمله بيل: ضو أهدى بس ثابت 🔦', 'pose': 'talk'},
        {'t': [53.36, 56.79], 'say': 'وإذا حمي التلفون، بيوطّي لحاله تيحمي حاله.',
         'cap': 'وإذا حمي التلفون: بيوطّي لحاله تيحمي حاله 🌡️', 'pose': 'point'},
        {'t': [56.99, 59.09], 'say': 'هلّأ صرت تعرف شو في ورا هالكبسة.',
         'cap': 'هلّأ صرت تعرف شو في ورا هالكبسة 😉', 'pose': 'welcome', 'screen': 'recap', 'style': 'fade'},
        {'t': [59.29, 60.97], 'say': 'تابعونا على Tech Wall.',
         'cap': 'تابعونا على Tech Wall 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

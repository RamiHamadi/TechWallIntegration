"""Tech Wall HOST explainer with a supplied voice-over: Apple's HomeView smart display (announced 2026-10-13).
    ./build.sh homeview  |  python3 homeview.py 0 150 400
Device 'stage': a generic tabletop smart display (no logo) whose screen changes with the voice; props pop in around it.
Voice: the user's generated audio (host/voices/homeview.flac); beat 't' = [start, end] s in it.
Facts (Apple coverage: MacObserver, Popular Science, Fox News, AppleInsider, Cult of Mac, 2026-10-13..15): $299 tabletop
or wall-mounted, ships Nov 13; A18 chip, Siri AI; face recognition for up to 6 people, each with their own Home Screen;
the Home Camera face shows up to 9 live camera feeds (compatible cameras; some features need iCloud+); locks, thermostats,
lights, blinds by touch or voice. Fictional names (Mom, Dad, Sam)."""
import host

EP = 'homeview'
INK, CYAN, YEL, GRN, RED = '#e9f1ff', '#5ce1ff', '#ffd54a', '#7CFC9A', '#ff6b6b'
SX, SY, SW, SH = 234, 54, 532, 332             # the display's screen area inside the stage


def at(win, x, y, w, h, inner, extra=''):
    return (f'<div data-in="{win}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">{inner}</div>')


def card(win, tag, title, body, col=YEL):
    return (f'<div data-in="{win}" style="position:absolute;left:455px;top:575px;width:530px;background:rgba(6,20,52,.86);'
            f'border:4px solid {col};border-radius:24px;padding:16px 20px;box-shadow:0 12px 30px rgba(0,0,0,.35)">'
            f'<div style="display:inline-block;background:{col};color:#0a2b66;font-weight:800;font-size:22px;padding:4px 14px;'
            f'border-radius:14px">{tag}</div><div style="font-weight:800;font-size:34px;margin-top:6px">{title}</div>'
            f'<div style="font-size:24px;color:#cfe3ff;line-height:1.35;margin-top:6px">{body}</div></div>')


def bubble(icon, label, col):
    return (f'<div style="width:150px;text-align:center"><div style="width:110px;height:110px;margin:0 auto;border-radius:50%;'
            f'background:rgba(6,20,52,.85);border:4px solid {col};display:grid;place-items:center;font-size:54px;'
            f'box-shadow:0 0 22px rgba(92,225,255,.35)">{icon}</div><div style="font-weight:800;font-size:22px;margin-top:8px">{label}</div></div>')


# ---------- the display (always on the main screen) ----------
DEVICE = (f'<div style="position:absolute;left:220px;top:40px;width:560px;height:360px;border-radius:30px;background:#0b0f1a;'
          'box-shadow:0 0 0 4px #2b3a55,0 30px 60px rgba(0,0,0,.45)"></div>'
          '<div style="position:absolute;left:330px;top:398px;width:340px;height:110px;border-radius:0 0 46px 46px;'
          'background:repeating-radial-gradient(circle at 50% 0,#d9dee8 0 3px,#c3cad8 3px 6px);box-shadow:0 18px 30px rgba(0,0,0,.35)"></div>'
          f'<div style="position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;border-radius:18px;overflow:hidden;'
          'background:radial-gradient(ellipse at 30% 20%,#2c4f9e,#101a3a 70%)"></div>')


def widget(icon, title, val, col):
    return (f'<div style="background:rgba(255,255,255,.12);border-radius:18px;padding:12px 14px;color:#fff">'
            f'<div style="font-size:30px">{icon}</div><div style="font-size:19px;opacity:.85;margin-top:2px">{title}</div>'
            f'<div style="font-size:28px;font-weight:800;color:{col}">{val}</div></div>')


DASH = at('-1,9.3', SX, SY, SW, SH,
          '<div style="padding:16px 20px;color:#fff"><div style="display:flex;justify-content:space-between;align-items:baseline">'
          '<b style="font-size:30px">Good evening</b><span style="font-size:24px;opacity:.85">10:08</span></div>'
          '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px">'
          + widget('💡', 'Lights', '3 on', YEL) + widget('🔒', 'Front Door', 'Locked', GRN)
          + widget('🌡️', 'Thermostat', '72°F', CYAN) + widget('📷', 'Cameras', '9 live', RED) + '</div></div>')

FAMILY = [('Mom', '#ff7a45', 9.6, 10.7), ('Dad', '#5c6cff', 10.7, 11.8), ('Sam', '#34c759', 11.8, 13.65)]
FACES = ''.join(
    at(f'{a},{b}', SX, SY, SW, SH,
       '<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff">'
       f'<div style="width:150px;height:150px;border:5px dashed {CYAN};border-radius:30px;display:grid;place-items:center">'
       f'<div style="width:104px;height:104px;border-radius:50%;background:{col};display:grid;place-items:center;font-size:48px;font-weight:800">{name[0]}</div></div>'
       f'<div style="font-size:30px;font-weight:800;margin-top:14px">Hi, {name} 👋</div>'
       '<div style="font-size:18px;opacity:.8">Your apps · your widgets</div></div>')
    for name, col, a, b in FAMILY)

CAM_TILES = ''.join(
    f'<div data-in="{15.2 + i * 0.17:.2f},22.6" style="position:relative;border-radius:8px;overflow:hidden;'
    f'background:linear-gradient(135deg,{c1},{c2})"><span style="position:absolute;left:6px;top:4px;font-size:11px;font-weight:800;'
    f'background:#ff3b30;color:#fff;border-radius:5px;padding:0 5px">● LIVE</span><span style="position:absolute;left:6px;bottom:4px;'
    f'font-size:14px;font-weight:700;color:#fff;text-shadow:0 1px 2px #000">{lab}</span></div>'
    for i, (lab, c1, c2) in enumerate([('Front door', '#4b6584', '#1e272e'), ('Driveway', '#576574', '#222f3e'),
                                         ('Backyard', '#218c74', '#0b3d2e'), ('Garage', '#636e72', '#2d3436'),
                                         ('Living room', '#a17a69', '#3d2c26'), ('Kitchen', '#b8860b', '#4a3606'),
                                         ('Side gate', '#3c6382', '#0a3d62'), ('Porch', '#6a89cc', '#1e3799'),
                                         ('Nursery', '#8e7cc3', '#3c2f6b')]))
CAMS = at('14.9,22.7', SX, SY, SW, SH,
          f'<div style="position:absolute;inset:10px;display:grid;grid-template-columns:repeat(3,1fr);gap:8px">{CAM_TILES}</div>')

ORBIT = (f'<svg data-in="-1,6.0" viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
         '<g stroke="rgba(233,241,255,.55)" stroke-width="3" stroke-dasharray="8 8" fill="none">'
         '<path d="M150 150 L234 150"/><path d="M150 360 L234 330"/><path d="M850 150 L766 150"/><path d="M850 360 L766 330"/></g></svg>'
         + at('-1,6.0', 5, 80, 150, 160, bubble('💡', 'Lights', YEL)) + at('-1,6.0', 5, 300, 150, 160, bubble('🔒', 'Locks', GRN))
         + at('-1,6.0', 845, 80, 150, 160, bubble('🌡️', 'Climate', CYAN)) + at('-1,6.0', 845, 300, 150, 160, bubble('📷', 'Cameras', RED)))

CHIP = at('6.3,13.6', 20, 110, 180, 200,
          '<div style="width:150px;height:150px;margin:0 auto;border-radius:26px;background:linear-gradient(135deg,#3a4766,#141c2e);'
          'border:4px solid #9aa6bd;display:grid;place-items:center;font-size:44px;font-weight:800;color:#fff;'
          'box-shadow:0 0 0 8px rgba(154,166,189,.25)">A18</div><div style="text-align:center;font-weight:800;font-size:22px;margin-top:10px">Chip</div>')
AIORB = at('7.6,13.6', 805, 110, 180, 200,
           '<div data-spin="120" style="width:150px;height:150px;margin:0 auto;border-radius:50%;'
           'background:conic-gradient(#5ce1ff,#bf5af2,#ff7a45,#ffd54a,#5ce1ff);filter:blur(1px);box-shadow:0 0 36px rgba(191,90,242,.6)"></div>'
           '<div style="text-align:center;font-weight:800;font-size:22px;margin-top:10px">Siri AI</div>')
LOCK = at('18.1,22.7', 5, 110, 190, 220, bubble('🔒', 'Locked ✓', GRN))
THERMO = at('18.9,22.7', 805, 110, 190, 220,
            '<div style="width:150px;text-align:center"><div style="width:120px;height:120px;margin:0 auto;border-radius:50%;'
            f'background:conic-gradient({CYAN} 0 62%,rgba(255,255,255,.12) 0);display:grid;place-items:center">'
            '<div style="width:92px;height:92px;border-radius:50%;background:#0a1a4a;display:grid;place-items:center;font-size:32px;font-weight:800">68°</div></div>'
            '<div style="font-weight:800;font-size:22px;margin-top:8px">Thermostat</div></div>')

MAIN = (DEVICE + DASH + FACES + CAMS + ORBIT + CHIP + AIORB + LOCK + THERMO
        + card('2.9,6.0', 'HOMEVIEW', 'AI control center', 'Lights, locks, climate and cameras on one screen.', CYAN)
        + card('6.3,9.3', 'A18 + SIRI AI', 'On-device brains', 'The A18 chip runs Siri AI on HomeView.')
        + card('9.4,13.6', 'FACE RECOGNITION', 'One screen, many people', 'Recognises up to 6 family members, each with their own Home Screen.', GRN)
        + card('14.9,19.9', 'HOME CAMERA', '9 live feeds at once', 'Every security camera on one screen (compatible cameras).', RED)
        + card('20.0,22.7', 'VOICE', '“Good night” →', 'Lights off · doors locked · thermostat 68°', CYAN))

PRICE = ('<div data-in="23.0" style="position:absolute;left:250px;top:60px;width:500px;height:300px">'
         '<div data-bob="6" style="position:absolute;inset:0;background:#ffd54a;color:#0a2b66;border-radius:30px;'
         'clip-path:polygon(14% 0,100% 0,100% 100%,14% 100%,0 50%);display:grid;place-items:center;font-size:130px;font-weight:800;'
         'box-shadow:0 18px 40px rgba(0,0,0,.4)"><span style="padding-left:60px">$299</span></div>'
         '<div style="position:absolute;left:30px;top:130px;width:40px;height:40px;border-radius:50%;background:#0a2b66"></div></div>'
         + at('23.8', 120, 400, 360, 90, '<div style="background:rgba(6,20,52,.86);border:3px solid #5ce1ff;border-radius:20px;padding:18px;'
              'text-align:center;font-size:28px;font-weight:800">Tabletop or wall</div>')
         + at('24.2', 520, 400, 360, 90, '<div style="background:rgba(6,20,52,.86);border:3px solid #5ce1ff;border-radius:20px;padding:18px;'
              'text-align:center;font-size:28px;font-weight:800">Ships Nov 13</div>')
         + at('25.3', 455, 575, 530, 230, '<div style="background:rgba(6,20,52,.86);border:4px solid #ffd54a;border-radius:24px;padding:18px;'
              'text-align:center"><div style="font-size:44px;font-weight:800">Worth it?</div><div style="font-size:64px;margin-top:6px">👍 👎</div></div>'))

SPEC = {
    'audio': 'host/voices/homeview.flac', 'lang': 'en', 'device': 'stage',
    'title': "Apple's HomeView, explained 🏠", 'tag': 'SMART HOME · SIRI AI', 'tip': 'TECH #02',
    'start': 'main',
    'screens': {
        'main': {'type': 'html', 'bg': 'transparent', 'html': MAIN},
        'price': {'type': 'html', 'bg': 'transparent', 'html': PRICE},
    },
    'beats': [
        {'t': [0.25, 5.55], 'say': "Apple's new HomeView isn't just a screen. It's an AI-powered control center for your home.",
         'cap': "Apple's HomeView: an AI-powered control center for your home 🏠", 'pose': 'welcome', 'hook': True},
        {'t': [6.18, 13.17], 'say': 'Its A18 chip powers Siri AI, while facial recognition personalizes the experience for different family members.',
         'cap': 'A18 chip + Siri AI, and face recognition for each family member', 'pose': 'point'},
        {'t': [13.70, 22.46], 'say': "Here's the interesting part: you can view up to nine security camera feeds at once, control smart locks and thermostats, and use voice commands to automate your home.",
         'cap': '9 camera feeds at once, smart locks, thermostats & voice automations', 'pose': 'point'},
        {'t': [23.05, 26.08], 'say': 'But at two hundred and ninety-nine dollars, is it worth it?',
         'cap': 'But at $299… is it worth it? 🤔', 'pose': 'front', 'screen': 'price', 'style': 'fade'},
        {'t': [26.73, 28.92], 'say': 'Follow Tech Wall for more tech explained!',
         'cap': 'Follow Tech Wall for more tech explained! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

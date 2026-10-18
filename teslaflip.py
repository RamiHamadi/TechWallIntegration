"""Tech Wall HOST explainer with a supplied voice-over: how the Tesla Roadster flips in mid-air (demo 2026-10-15).
    ./build.sh teslaflip  |  python3 teslaflip.py 0 150 400
No phone or TV: device 'stage' = a frameless illustration area above the host, drawn in the blueprint style.
Voice: the user's generated audio (host/voices/teslaflip.flac); beat 't' = [start, end] s in it, phrase times measured.
Facts (TechCrunch / Motor1 / Fox Business, 2026-10-15): a fan system under the car creates suction that held it to an
inverted ramp until fully upside down; SpaceX-built cold-gas thrusters (10, fed by ~600 L of compressed air) push and
spin it in the air; Tesla plans production in 2028; road-legal use of the flight hardware is not confirmed.
Generic car silhouette, no logos. Motion: data-keys "t,x,y,rot" (dense keys, linear), data-in, data-spin, data-bob."""
import math
import host

EP = 'teslaflip'
CX, CY, RT, RC = 500, 300, 240, 194             # loop centre, track radius, car-centre radius (inside the loop)
INK, CYAN, YEL, RED = '#e9f1ff', '#5ce1ff', '#ffd54a', '#ff6b6b'


def smooth(u):
    return u * u * (3 - 2 * u)


def path_keys(t0, t1, fn, n=24):
    """Dense keys along fn(u) -> (x, y, rot) with smooth start/stop (the element uses linear easing between keys)."""
    out = []
    for i in range(n + 1):
        u = i / n; x, y, r = fn(smooth(u))
        out.append(f'{t0 + (t1 - t0) * u:.3f},{x:.1f},{y:.1f},{r:.1f}')
    return out


def arc(u):                                     # bottom of the loop -> right wall -> ceiling (driving on the inside)
    a = math.radians(90 - 180 * u)              # 90 deg (bottom, y down) -> -90 deg (top)
    return CX + RC * math.cos(a), CY + RC * math.sin(a), -360 - 180 * u


def flip(u):                                    # released from the ceiling: falls, swings right, rotates 180, lands
    x = 500 + 110 * math.sin(math.pi * u) - 120 * u
    y = 106 + (494 - 106) * u * u
    return x, y, -540 - 180 * u


def drive(xa, xb):
    return lambda u: (xa + (xb - xa) * u, 494, -360)


def hook_flip(u):                               # frame 0: already mid-flip (the cover), then lands
    return 560 - 180 * u, 250 + 244 * u * u, -270 - 90 * u


KEYS = (path_keys(0.0, 1.4, hook_flip, 10) + ['4.20,380,494,-360', '4.30,-170,494,-360', '6.95,-170,494,-360']
        + path_keys(7.0, 8.5, drive(-170, CX), 10) + ['10.45,500,494,-360']
        + path_keys(10.5, 13.1, arc, 30) + ['20.25,500,106,-540']
        + path_keys(20.3, 23.0, flip, 30) + ['23.15,380,487,-720', '23.35,380,494,-720', '40,380,494,-720'])

CAR_SVG = (f'<svg viewBox="0 0 260 96" style="position:absolute;left:0;top:0;width:260px;height:96px;overflow:visible">'
           f'<path d="M12 64 Q12 48 38 44 L92 34 Q122 12 162 14 Q200 16 224 38 L248 46 Q258 50 256 64 L252 72 L12 72 Z" '
           f'fill="{INK}" stroke="#0a2b66" stroke-width="3"/>'
           '<path d="M100 36 Q126 20 160 20 Q190 22 210 38 Z" fill="#1b3f8f"/>'
           '<rect x="236" y="50" width="16" height="7" rx="3" fill="#ffd54a"/><rect x="14" y="52" width="12" height="7" rx="3" fill="#ff5a5a"/>'
           '<circle cx="64" cy="74" r="17" fill="#1c2233"/><circle cx="64" cy="74" r="7" fill="#9aa6bd"/>'
           '<circle cx="204" cy="74" r="17" fill="#1c2233"/><circle cx="204" cy="74" r="7" fill="#9aa6bd"/></svg>')
FAN = ('<div data-spin="900" style="position:absolute;left:{x}px;top:66px;width:26px;height:26px;border-radius:50%;'
       f'background:conic-gradient({CYAN} 0 20%,transparent 0 25%,{CYAN} 0 45%,transparent 0 50%,{CYAN} 0 70%,transparent 0 75%,{CYAN} 0 95%,transparent 0);'
       'box-shadow:0 0 10px rgba(92,225,255,.8)"></div>')
SUCK = ''.join(f'<div style="position:absolute;left:{x}px;top:96px;width:0;height:0;border-left:9px solid transparent;'
               f'border-right:9px solid transparent;border-top:16px solid {CYAN}"></div>' for x in (92, 121, 150))


def puffs(win):
    """Two gas jets on opposite corners (front-top up, rear-bottom down) = a torque that spins the car."""
    jet = ('<div data-bob="3" style="position:absolute;left:{x}px;top:{y}px;width:34px;height:{h}px;border-radius:17px;'
           'background:linear-gradient({d},rgba(255,255,255,.95),rgba(92,225,255,.55),transparent);filter:blur(1px)"></div>')
    return (f'<div data-in="{win}" style="position:absolute;inset:0">'
            + jet.format(x=200, y=-58, h=62, d='to top') + jet.format(x=226, y=-44, h=48, d='to top')
            + jet.format(x=20, y=86, h=62, d='to bottom') + jet.format(x=-6, y=80, h=48, d='to bottom') + '</div>')


CAR = (f'<div data-keys="{";".join(KEYS)}" data-ease="linear" style="position:absolute;left:0;top:0;width:260px;height:96px;'
       'margin:-48px 0 0 -130px;z-index:5">' + CAR_SVG + FAN.format(x=96) + FAN.format(x=140)
       + f'<div data-in="9.5,14.9" style="position:absolute;inset:0">{SUCK}</div>' + puffs('-1,1.0') + puffs('17.3,23.0') + '</div>')

TRACK = (f'<svg viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
         f'<path d="M0 {CY + RT} H{CX} A{RT} {RT} 0 0 0 {CX + RT} {CY} A{RT} {RT} 0 0 0 {CX} {CY - RT} H140" fill="none" stroke="{INK}" '
         'stroke-width="7" stroke-linecap="round"/>'
         f'<path d="M0 {CY + RT + 16} H{CX} A{RT + 16} {RT + 16} 0 0 0 {CX + RT + 16} {CY} A{RT + 16} {RT + 16} 0 0 0 {CX} {CY - RT - 16} H140" '
         'fill="none" stroke="rgba(233,241,255,.35)" stroke-width="2" stroke-dasharray="10 10"/>'
         f'<text x="{CX + RT + 30}" y="{CY + 8}" fill="rgba(233,241,255,.55)" font-size="18" letter-spacing="3" '
         f'transform="rotate(90 {CX + RT + 30} {CY})" font-family="Poppins">SPECIAL TRACK</text></svg>')


def card(win, x, y, w, tag, title, body, col=YEL):
    return (f'<div data-in="{win}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;background:rgba(6,20,52,.86);'
            f'border:4px solid {col};border-radius:24px;padding:16px 20px;box-shadow:0 12px 30px rgba(0,0,0,.35)">'
            f'<div style="display:inline-block;background:{col};color:#0a2b66;font-weight:800;font-size:22px;padding:4px 14px;'
            f'border-radius:14px">{tag}</div><div style="font-weight:800;font-size:36px;margin-top:6px">{title}</div>'
            f'<div style="font-size:24px;color:#cfe3ff;line-height:1.35;margin-top:6px">{body}</div></div>')


TRACK_HTML = (TRACK + CAR
              + f'<div data-in="-1,3.9" style="position:absolute;left:10px;top:110px;width:270px;text-align:center">'
                f'<div style="font-size:150px;font-weight:800;color:{YEL};line-height:1;text-shadow:0 8px 20px rgba(0,0,0,.4)">?</div>'
                '<div style="font-size:30px;font-weight:800;letter-spacing:2px">MID-AIR FLIP</div></div>'
              + card('7.5,14.7', 455, 585, 530, '① SUCTION FANS', 'Sticks to the track',
                     'Fans pull the air out from under the car: low pressure holds it on.', CYAN)
              + f'<div data-in="13.1,14.9" style="position:absolute;left:330px;top:250px;width:340px;text-align:center;'
                f'font-size:34px;font-weight:800;color:{YEL}">EVEN UPSIDE DOWN 🙃</div>'
              + card('15.3,23.9', 455, 585, 530, '② GAS THRUSTERS', 'Push + spin',
                     'Compressed gas blasts out of nozzles: thrust that pushes and rotates the car.')
              + f'<div data-in="23.0,24.3" style="position:absolute;left:270px;top:360px;width:220px;text-align:center;'
                f'font-size:32px;font-weight:800;color:#7CFC9A">LANDED ✓</div>')

ICON_FAN = (f'<div data-spin="500" style="width:110px;height:110px;margin:0 auto;border-radius:50%;'
            f'background:conic-gradient({CYAN} 0 20%,transparent 0 25%,{CYAN} 0 45%,transparent 0 50%,{CYAN} 0 70%,transparent 0 75%,'
            f'{CYAN} 0 95%,transparent 0);box-shadow:0 0 24px rgba(92,225,255,.7)"></div>')
ICON_JET = ('<div style="position:relative;width:110px;height:110px;margin:0 auto">'
            f'<div style="position:absolute;left:30px;top:6px;width:50px;height:60px;border-radius:12px;background:{INK}"></div>'
            f'<div style="position:absolute;left:40px;top:62px;width:30px;height:16px;background:#9aa6bd;clip-path:polygon(15% 0,85% 0,100% 100%,0 100%)"></div>'
            '<div data-bob="4" style="position:absolute;left:30px;top:78px;width:50px;height:34px;border-radius:25px;'
            'background:linear-gradient(to bottom,#fff,rgba(92,225,255,.6),transparent)"></div></div>')


def big_card(win, x, num, icon, title, col):
    return (f'<div data-in="{win}" style="position:absolute;left:{x}px;top:250px;width:420px;height:400px;background:rgba(6,20,52,.82);'
            f'border:4px solid {col};border-radius:30px;text-align:center;padding-top:30px">'
            f'<div style="font-size:54px;font-weight:800;color:{col}">{num}</div>{icon}'
            f'<div style="font-size:34px;font-weight:800;margin-top:26px">{title}</div></div>')


TWO = (big_card('4.5', 50, '①', ICON_FAN, 'SUCTION FANS', CYAN) + big_card('5.3', 530, '②', ICON_JET, 'GAS THRUSTERS', YEL))


def chip(win, x, y, txt, col, w=280, strike=False):
    s = (f'<div style="position:absolute;left:-8px;right:-8px;top:50%;height:7px;background:{RED};transform:rotate(-8deg)"></div>'
         if strike else '')
    return (f'<div data-in="{win}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;background:rgba(6,20,52,.82);'
            f'border:3px solid {col};border-radius:20px;padding:22px 10px;text-align:center;font-size:34px;font-weight:800">{txt}{s}</div>')


COMBO = (f'<div style="position:absolute;left:0;right:0;top:120px;text-align:center;font-size:26px;letter-spacing:3px;color:#bfe9ff">NOT USING</div>'
         + chip('25.3', 150, 170, '✈️ WINGS', RED, 300, True) + chip('26.5', 550, 170, '🔥 JET ENGINES', RED, 300, True)
         + f'<div data-in="27.6" style="position:absolute;left:0;right:0;top:400px;text-align:center;font-size:26px;letter-spacing:3px;color:#bfe9ff">COMBINING</div>'
         + chip('28.4', 40, 450, '💨 AIRFLOW', CYAN) + chip('29.1', 360, 450, '🎯 PRESSURE', YEL) + chip('29.9', 680, 450, '🕹️ CONTROL', '#7CFC9A')
         + f'<div data-in="29.0" style="position:absolute;left:320px;top:470px;font-size:44px;font-weight:800;color:#fff">+</div>'
         + f'<div data-in="29.8" style="position:absolute;left:641px;top:470px;font-size:44px;font-weight:800;color:#fff">+</div>')

FUTURE = (f'<svg viewBox="0 0 1000 900" style="position:absolute;inset:0;width:1000px;height:900px">'
          f'<path d="M0 560 H1000" stroke="{INK}" stroke-width="6"/><path d="M40 600 H960" stroke="rgba(233,241,255,.4)" '
          'stroke-width="4" stroke-dasharray="40 30"/></svg>'
          f'<div style="position:absolute;left:370px;top:464px;width:260px;height:96px">{CAR_SVG}</div>'
          f'<div data-in="31.9" style="position:absolute;left:0;right:0;top:40px;text-align:center;font-size:180px;font-weight:800;'
          f'color:{YEL};line-height:1;text-shadow:0 8px 24px rgba(0,0,0,.4)">?</div>'
          + chip('32.6', 60, 270, "Tesla's plan: production in 2028", CYAN, 420)
          + chip('33.6', 520, 270, 'Road-legal flight? Not confirmed', RED, 420))

SPEC = {
    'audio': 'host/voices/teslaflip.flac', 'lang': 'en', 'device': 'stage',
    'title': 'How a Tesla flips in mid-air 🤯', 'tag': 'FAN SUCTION · GAS THRUSTERS', 'tip': 'TECH #01',
    'start': 'track',
    'screens': {
        'track': {'type': 'html', 'bg': 'transparent', 'html': TRACK_HTML},
        'two': {'type': 'html', 'bg': 'transparent', 'html': TWO},
        'combo': {'type': 'html', 'bg': 'transparent', 'html': COMBO},
        'future': {'type': 'html', 'bg': 'transparent', 'html': FUTURE},
    },
    'beats': [
        {'t': [0.22, 3.86], 'say': 'How can a Tesla actually flip in midair?',
         'cap': 'How can a Tesla actually flip in mid-air? 🤯', 'pose': 'welcome', 'hook': True},
        {'t': [4.32, 6.56], 'say': 'It uses two incredible technologies.',
         'cap': 'It uses 2 incredible technologies', 'pose': 'talk', 'do': [{'nav': 'two', 'style': 'fade', 'at': .0}]},
        {'t': [6.96, 14.40], 'say': 'First, powerful fans underneath the car create suction, helping it stick to a specially designed track, even upside down.',
         'cap': '① Fans underneath create suction to stick to the track 🙃', 'pose': 'point', 'step': 1,
         'screen': 'track', 'style': 'fade'},
        {'t': [14.92, 23.88], 'say': 'Then, SpaceX-inspired thrusters release highly pressurized gas through nozzles, creating thrust that can push and rotate the car in the air.',
         'cap': '② SpaceX-inspired thrusters push & rotate the car 🚀', 'pose': 'point', 'step': 2},
        {'t': [24.40, 31.28], 'say': "The car isn't using wings or traditional jet engines. It's combining airflow, pressure, and precise control.",
         'cap': 'No wings, no jet engines: airflow + pressure + precise control', 'pose': 'talk', 'screen': 'combo', 'style': 'fade'},
        {'t': [31.84, 35.14], 'say': 'But can this technology become a real production feature?',
         'cap': 'Could this become a real production feature? 🤔', 'pose': 'front', 'screen': 'future', 'style': 'fade'},
        {'t': [35.58, 37.96], 'say': 'Follow Tech Wall for more mind-blowing tech.',
         'cap': 'Follow Tech Wall for more mind-blowing tech! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

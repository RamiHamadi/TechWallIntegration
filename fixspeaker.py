"""Tech Wall HOST episode (Galaxy, Arabic) with a supplied voice-over: push water out of a phone speaker with a tone site.
    ./build.sh fixspeaker  |  python3 fixspeaker.py 0 150 400
Voice: the user's Lebanese-Arabic audio, pauses between phrases shortened to 0.2 s (host/voices/fixspeaker.flac);
beats aligned to the script by its sentence pauses (template translate.py). Captions and chalk cards in Arabic.
Facts (tool maker's post + 2026 guides): fixmyspeakers.com plays a low tone in the browser (Android + iPhone) that
vibrates the speaker to push droplets out; no independent tests found, so it is shown as "may help"; don't poke the
grille with a needle; use medium volume and short runs (max volume on repeat may damage the speaker).
Generic site look-alike (no logos); the water droplets are an illustration."""
import math
import host

EP = 'fixspeaker'
YEL, CY, GRN, BLU, RED = '#ffd54a', '#5ce1ff', '#34d399', '#3e91ff', '#ff6b6b'
AR = 'font-family:Cairo,Poppins,sans-serif'
SB = '<div class="sb"><span>10:08</span><span class="bat"></span></div>'
T_TAP = 6.21 + .8 * 4.75                      # "Eject water" pressed
PLAY = [(-1, 3.75), (T_TAP + .25, 16.3)]       # windows where the tone plays


def ring_windows(t0, t1, period=.6):
    out, t = [], t0
    while t < t1:
        out.append(f'{t:.2f},{t + period:.2f}'); t += period
    return ';'.join(out)


def site(playing_wins):
    """fixmyspeakers.com look-alike: one big button; while playing, sound rings pulse from it."""
    rings = ''.join(f'<div data-ring="{ring_windows(max(a, -1) + d, b)}" style="position:absolute;left:102px;top:270px;width:200px;'
                    'height:200px;border-radius:50%;border:4px solid #3e91ff;transform:scale(calc(.9 + var(--p,0) * .9));'
                    'opacity:calc(1 - var(--p,0))"></div>' for a, b in playing_wins for d in (0, .3))
    state = ''.join(f'<div data-in="{a:.2f},{b:.2f}" style="position:absolute;left:0;right:0;top:500px;text-align:center;'
                    f'color:{BLU};font-size:20px;font-weight:800">🔊 Playing… water ejecting</div>' for a, b in playing_wins)
    return (SB + '<div style="margin:6px 12px 0;height:44px;background:#fff;border-radius:22px;display:flex;align-items:center;'
            'padding:0 16px;font-size:16px;color:#333">🔒 fixmyspeakers.com</div>'
            '<div style="text-align:center;margin-top:40px;font-size:28px;font-weight:800">Fix My Speakers</div>'
            '<div style="text-align:center;font-size:15px;color:#5a6b8c;margin-top:4px">Water in your speaker? Press the button.</div>'
            + rings
            + '<div data-id="eject" style="position:absolute;left:102px;top:270px;width:200px;height:200px;border-radius:50%;'
              'background:radial-gradient(circle at 35% 30%,#7fc0ff,#1f6fe0);box-shadow:0 14px 30px rgba(31,111,224,.45);'
              'display:grid;place-items:center;color:#fff;font-size:22px;font-weight:800;text-align:center;line-height:1.3">'
              '<div><div style="font-size:56px">💧</div>Eject water</div></div>'
            + state
            + '<div style="position:absolute;left:22px;right:22px;bottom:46px;background:#fff;border-radius:18px;padding:12px 16px;'
              'font-size:14px;color:#5a6b8c;line-height:1.5">Tip: medium volume, speaker facing down, run it a few times.</div>')


MUSIC = (SB + '<div style="text-align:center;margin-top:30px;font-size:15px;color:#5a6b8c">Now playing</div>'
         '<div style="margin:16px auto 0;width:280px;height:280px;border-radius:28px;background:linear-gradient(135deg,#ff8a65,#7a4fd6)"></div>'
         '<div style="text-align:center;margin-top:18px;font-size:22px;font-weight:700">Summer Song</div>'
         '<div style="text-align:center;font-size:15px;color:#8a8f99">Example artist</div>'
         '<div style="display:flex;justify-content:center;gap:5px;align-items:flex-end;height:50px;margin-top:20px">'
         + ''.join(f'<i style="width:8px;height:{h}px;border-radius:4px;background:#c4c9d4"></i>' for h in (8, 12, 6, 10, 7, 9, 5, 11, 6, 8))
         + '</div><div style="margin:18px 30px 0;background:#ffecec;color:#c62828;border-radius:16px;padding:10px;text-align:center;'
           'font-size:17px;font-weight:800">🔉 Sound is quiet & muffled</div>')


# water droplets ejected from the bottom speaker grille of the Galaxy (overlay coords; rig bottom ≈ y 1122)
GX, GY = 880, 1124


def drops():
    out = ''
    for k in range(7):
        ang = math.radians(20 + k * 9)
        for a, b in PLAY:
            t, keys = max(a, -1) + k * .14, []
            while t < b:
                d = 190 + (k % 3) * 50
                keys.append(f'{t:.2f},{GX},{GY},0,.4;{t + .7:.2f},{min(1060, GX + d * math.cos(ang) * .55):.0f},{GY + d * math.sin(ang):.0f},0,1.1')
                t += .95
            out += (f'<div data-in="{a:.2f},{b:.2f}" style="position:absolute;inset:0;transform-origin:{GX}px {GY}px">'
                    f'<div data-keys="{";".join(keys)}" data-ease="linear" style="position:absolute;left:0;top:0;width:30px;height:38px;'
                    'margin:-19px 0 0 -15px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:radial-gradient(circle at 35% 30%,#e8f8ff,#5cc8ff);'
                    'box-shadow:0 0 8px rgba(92,200,255,.7)"></div></div>')
    return out


GRILLE = (f'<div style="position:absolute;left:{GX - 34}px;top:{GY - 6}px;display:flex;gap:5px">'
          + ''.join('<i style="width:6px;height:6px;border-radius:50%;background:#5a6380"></i>' for _ in range(8)) + '</div>')


def card(win, top, html, border=YEL, width=520):
    return (f'<div data-in="{win}" dir="rtl" style="position:absolute;left:40px;top:{top}px;width:{width}px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:16px 22px;color:#fff;{AR}">{html}</div>')


OVERLAY = (GRILLE + drops()
           + card('-1,3.7', 260, f'<div style="font-size:52px;font-weight:900;color:{YEL};line-height:1.2">💧 المي بتطلع<br>من السماعة</div>'
                                 '<div style="font-size:30px;font-weight:800;margin-top:6px">🔊 بصوت واهتزاز بس</div>', CY)
           + card('3.85,6.1', 260, '<div style="font-size:120px;text-align:center;line-height:1.1">🪡<span style="color:#ff6b6b">✕</span></div>'
                                   '<div style="font-size:38px;font-weight:900;text-align:center">لا إبرة ولا أي شي حاد!</div>', RED)
           + card('6.3,11.0', 260, '<div style="font-size:28px;font-weight:700;color:#cfe3ff">افتح من تلفونك</div>'
                                   f'<div style="font-size:40px;font-weight:900;color:{YEL};direction:ltr;text-align:right">fixmyspeakers.com</div>'
                                   '<div style="font-size:30px;font-weight:800">واضغط عالزر 💧</div>', GRN)
           + card('11.2,16.35', 260, '<div style="font-size:40px;font-weight:900;line-height:1.4">🔊 اهتزاز الصوت<br>💧 ← المي بتطلع</div>'
                                     '<div style="font-size:26px;font-weight:700;color:#cfe3ff">يمكن يساعد، مش مضمون 100%</div>', CY)
           + card('16.5,18.3', 260, '<div style="font-size:34px;font-weight:900;line-height:1.5">🔉 صوت متوسط<br>🔁 كرّرها كم مرة بس</div>', YEL))

SPEC = {
    'audio': 'host/voices/fixspeaker.flac', 'lang': 'ar', 'device': 'galaxy', 'overlay': OVERLAY,
    'title': 'طلّع المي من سماعة تلفونك 💧', 'tag': 'SPEAKER · WATER EJECT', 'tip': 'TIP #17',
    'start': 'play',
    'screens': {
        'play': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': site(PLAY[:1])},
        'music': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': MUSIC},
        'site': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': site(PLAY[1:])},
    },
    'beats': [
        {'t': [0.0, 3.60], 'say': 'وقع تلفونك بالمي؟ وصار صوت السماعة خفيف ومكتوم؟',
         'cap': 'وقع تلفونك بالمي؟ طلّع المي من السماعة 💧', 'capsize': 84, 'pose': 'point', 'hook': True},
        {'t': [3.80, 6.01], 'say': 'ما تحاول تحطّ فيها إبرة أو أي شي حاد!',
         'cap': 'ما تحطّ فيها إبرة أو أي شي حاد! ❌', 'pose': 'talk', 'do': [{'nav': 'music', 'style': 'fade', 'at': 0}]},
        {'t': [6.21, 10.96], 'say': 'في موقع اسمه FixMySpeakers.com، افتحو من تلفونك واضغط عالزر!',
         'cap': 'افتح موقع FixMySpeakers.com من تلفونك واضغط عالزر', 'pose': 'point', 'step': 1,
         'do': [{'nav': 'site', 'style': 'fade', 'at': 0}, {'tap': 'eject', 'at': .8}]},
        {'t': [11.16, 16.27], 'say': 'رح تسمع صوت معيّن، واهتزاز هالصوت بيساعد يطلّع المي اللي عالقة جوّا السماعة!',
         'cap': 'اهتزاز الصوت بيساعد يطلّع المي العالقة بالسماعة 🔊', 'pose': 'welcome', 'step': 2},
        {'t': [16.47, 18.22], 'say': 'جرّبها إذا صار معك هالموقف،', 'cap': 'جرّبها إذا صار معك هالموقف 👍', 'pose': 'talk'},
        {'t': [18.44, 22.47], 'say': 'وما تنسى تعمل فولو لـ Tech Wall لمزيد من الحيل التكنولوجية!',
         'cap': 'اعمل فولو لـ Tech Wall لمزيد من الحيل التكنولوجية! 🚀', 'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

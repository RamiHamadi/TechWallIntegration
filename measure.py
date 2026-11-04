"""Tech Wall HOST episode (iPhone + Galaxy, Arabic) with a supplied voice-over: measure objects with the phone camera (AR).
    ./build.sh measure  |  python3 measure.py 0 150 400
Voice: the user's Lebanese-Arabic audio, pauses between phrases shortened to 0.2 s (host/voices/measure.flac); beats
aligned to the script by its sentence pauses (template translate.py). Captions and chalk cards in Arabic.
Facts (Apple Measure guide; 9to5Google 2021-06, 2026-09): iPhone > Measure app > aim at the object > tap + at the start
point > move to the end > tap + again; LiDAR models (iPhone 12 Pro and later Pro, iPad Pro) measure faster and more
accurately and add a Ruler view. Google's Measure app was discontinued in 2021 (only on phones that already had it);
Android users can use ARCore ruler apps such as AR Ruler (Samsung's Quick Measure is retired end of 2026).
AR estimates, not a tape measure. Generic look-alikes, no logos."""
import host

EP = 'measure'
YEL, CY, GRN, RED = '#ffd54a', '#5ce1ff', '#34d399', '#ff6b6b'
AR = 'font-family:Cairo,Poppins,sans-serif'
X0, X1, LY = 62, 330, 452                      # desk edge measured (screen px)
T_A, T_B = 11.57 + .35, 13.6                   # first "+" tap, end of the drag
T_C = 15.05                                    # second "+" tap → measurement shown


def scene(w, h):
    """Camera view of a room: wall, floor and a desk (the measured object)."""
    return (f'<div style="position:absolute;inset:0;background:linear-gradient(#d9cdb8 0 52%,#a88a64 52% 100%)"></div>'
            f'<div style="position:absolute;left:0;right:0;top:{h * .52 - 4:.0f}px;height:8px;background:#8a6d4b"></div>'
            '<div style="position:absolute;left:250px;top:150px;width:110px;height:140px;border:8px solid #6b4f33;background:#9fc6e0"></div>'
            f'<div style="position:absolute;left:{X0 - 6}px;top:{LY}px;width:{X1 - X0 + 12}px;height:26px;background:#7a5536;'
            'box-shadow:0 10px 20px rgba(0,0,0,.25)"></div>'
            f'<div style="position:absolute;left:{X0 + 8}px;top:{LY + 26}px;width:16px;height:180px;background:#6b4a2e"></div>'
            f'<div style="position:absolute;left:{X1 - 24}px;top:{LY + 26}px;width:16px;height:180px;background:#6b4a2e"></div>'
            f'<div style="position:absolute;left:{X0 + 40}px;top:{LY - 46}px;width:70px;height:46px;border-radius:6px;background:#3a4a6b"></div>')


def tape(label, win=None, ticks=False):
    """Yellow-white measuring line along the desk edge with a label pill; win = data-in window (None = always)."""
    tick = ''.join(f'<i style="position:absolute;left:{x}px;top:-9px;width:2px;height:{14 if k % 5 == 0 else 8}px;background:#fff"></i>'
                   for k, x in enumerate(range(0, X1 - X0, 9))) if ticks else ''
    attr = f' data-in="{win}"' if win else ''
    return (f'<div{attr} style="position:absolute;left:{X0}px;top:{LY - 3}px;width:{X1 - X0}px;height:6px;background:#fff;'
            f'border-radius:3px;box-shadow:0 0 0 2px rgba(0,0,0,.25);transform-origin:0 50%">{tick}'
            '<i style="position:absolute;left:-7px;top:-4px;width:14px;height:14px;border-radius:50%;background:#fff"></i>'
            '<i style="position:absolute;right:-7px;top:-4px;width:14px;height:14px;border-radius:50%;background:#fff"></i>'
            f'<span style="position:absolute;left:50%;top:-50px;transform:translateX(-50%);background:#fff;color:#111;border-radius:16px;'
            f'padding:4px 14px;font-size:22px;font-weight:800;white-space:nowrap;font-family:Poppins">{label}</span></div>')


def ios(static, lidar=False):
    """iPhone Measure look-alike (398x828)."""
    top = ('<div class="sb" style="color:#fff;position:relative;z-index:3"><span>10:08</span><span class="bat"></span></div>'
           '<div style="position:absolute;left:0;right:0;top:64px;text-align:center;z-index:3"><span style="background:rgba(0,0,0,.45);'
           'color:#fff;border-radius:14px;padding:5px 14px;font-size:15px">' + ('Ruler view · LiDAR' if lidar else 'Measure') + '</span></div>')
    plus = ('<div data-id="plus" style="position:absolute;left:159px;bottom:60px;width:80px;height:80px;border-radius:50%;background:#fff;'
            'display:grid;place-items:center;font-size:48px;font-weight:300;color:#111;box-shadow:0 4px 16px rgba(0,0,0,.3);z-index:3">+</div>')
    if static:
        return scene(398, 828) + tape('1.20 m', ticks=lidar) + top + plus
    reticle_keys = f'{T_A:.2f},{X0},{LY};{T_A + .3:.2f},{X0},{LY};{T_B:.2f},{X1},{LY}'
    drag = (f'<div data-ring="{T_A + .3:.2f},{T_B:.2f}" style="position:absolute;left:{X0}px;top:{LY - 3}px;width:{X1 - X0}px;height:6px;'
            'background:#fff;border-radius:3px;clip-path:inset(0 calc((1 - var(--p,0)) * 100%) 0 0)"></div>'
            f'<i data-in="{T_A:.2f}" style="position:absolute;left:{X0 - 7}px;top:{LY - 7}px;width:14px;height:14px;border-radius:50%;background:#fff"></i>')
    hint = (f'<div data-in="-1,{T_A:.2f}" style="position:absolute;left:0;right:0;top:110px;text-align:center;color:#fff;font-size:17px;'
            'font-weight:700;text-shadow:0 1px 4px rgba(0,0,0,.6);z-index:3">Aim at the start point, tap +</div>')
    reticle = (f'<div data-keys="{reticle_keys}" style="position:absolute;left:0;top:0;width:44px;height:44px;margin:-22px 0 0 -22px;'
               'border:3px solid #fff;border-radius:50%;box-shadow:0 0 0 2px rgba(0,0,0,.25);z-index:2">'
               '<i style="position:absolute;left:17px;top:17px;width:6px;height:6px;border-radius:50%;background:#fff"></i></div>')
    return scene(398, 828) + drag + tape('1.20 m', f'{T_C + .1:.2f}') + hint + reticle + top + plus


def android():
    """Galaxy with an AR ruler app look-alike (404x842)."""
    return (scene(404, 842) + tape('120 cm', '18.0')
            + '<div class="sb" style="color:#fff;position:relative;z-index:3"><span>10:08</span><span class="bat"></span></div>'
              '<div style="position:absolute;left:14px;right:14px;top:58px;height:48px;border-radius:24px;background:rgba(0,0,0,.5);'
              'color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 18px;font-size:17px;font-weight:700;z-index:3">'
              '📏 AR Ruler<span style="font-size:14px;opacity:.85">cm · m · in</span></div>'
            + '<div style="position:absolute;left:0;right:0;bottom:60px;display:flex;justify-content:center;gap:22px;z-index:3">'
              + ''.join(f'<div style="width:66px;height:66px;border-radius:50%;background:{b};display:grid;place-items:center;'
                        f'font-size:28px;color:{c}">{e}</div>' for e, b, c in [('↶', 'rgba(0,0,0,.5)', '#fff'), ('+', '#fff', '#111'),
                                                                                  ('📷', 'rgba(0,0,0,.5)', '#fff')])
              + '</div>')


def card(win, top, html, border=YEL, width=520):
    return (f'<div data-in="{win}" dir="rtl" style="position:absolute;left:40px;top:{top}px;width:{width}px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:16px 22px;color:#fff;{AR}">{html}</div>')


LIDAR_CAM = ('<div style="position:relative;width:200px;height:200px;margin:8px auto 0;border-radius:44px;background:#2b3245;'
             'border:3px solid #8a93b0">'
             + ''.join(f'<i style="position:absolute;left:{x}px;top:{y}px;width:70px;height:70px;border-radius:50%;background:#0b0f1a;'
                       'border:6px solid #5a6380"></i>' for x, y in [(18, 18), (18, 108), (108, 62)])
             + f'<i style="position:absolute;left:128px;top:150px;width:26px;height:26px;border-radius:50%;background:#111;'
               f'box-shadow:0 0 0 4px {CY},0 0 18px {CY}"></i></div>')

OVERLAY = (
    card('-1,6.2', 260, f'<div style="font-size:56px;font-weight:900;color:{YEL};line-height:1.15">📏 <span dir="ltr">1.20 m</span></div>'
                        '<div style="font-size:30px;font-weight:800;margin-top:6px">بكاميرا التلفون، بلا متر</div>')
    + card('6.4,16.75', 260, '<div style="font-size:30px;font-weight:800;color:#cfe3ff">📱 آيفون</div>'
                             f'<div style="font-size:44px;font-weight:900;color:{YEL};direction:ltr;text-align:right">Measure</div>'
                             '<div style="font-size:26px;font-weight:700;line-height:1.5">➕ نقطة البداية<br>↔️ حرّك<br>➕ نقطة النهاية</div>', CY)
    + card('16.95,26.7', 260, '<div style="font-size:30px;font-weight:800;color:#cfe3ff">🤖 أندرويد</div>'
                              f'<div style="font-size:44px;font-weight:900;color:{YEL};direction:ltr;text-align:right">AR Ruler</div>'
                              '<div style="font-size:24px;font-weight:700">أو أي تطبيق قياس بالواقع المعزّز</div>', GRN)
    + card('22.4,26.7', 520, '<div style="font-size:24px;font-weight:700;line-height:1.45">ℹ️ Google Measure توقّف من 2021<br>'
                             '(بس إذا كان عندك من قبل)</div>', '#8a93b0')
    + card('26.9,33.85', 250, f'<div style="font-size:34px;font-weight:900;color:{YEL};direction:ltr;text-align:right">LiDAR</div>'
                              + LIDAR_CAM + '<div style="font-size:24px;font-weight:700;margin-top:8px">آيفون Pro وأجهزة تانية: قياس أدقّ</div>', CY)
    + card('34.0,39.9', 270, '<div style="font-size:42px;font-weight:900;line-height:1.3">⚠️ قياس تقريبي</div>'
                             '<div style="font-size:28px;font-weight:700">للدقة العالية: المتر الحقيقي 📏</div>', RED))

SPEC = {
    'audio': 'host/voices/measure.flac', 'lang': 'ar', 'devices': ['phone', 'galaxy'], 'overlay': OVERLAY,
    'title': 'حوّل تلفونك لمتر 📏', 'tag': 'AR MEASURE · iPHONE · ANDROID', 'tip': 'TIP #18',
    'start': 'res',
    'screens': {
        'res': {'dev': 'phone', 'type': 'html', 'bg': '#d9cdb8', 'html': ios(True)},
        'ios': {'dev': 'phone', 'type': 'html', 'bg': '#d9cdb8', 'html': ios(False)},
        'droid': {'dev': 'galaxy', 'type': 'html', 'bg': '#d9cdb8', 'html': android()},
        'lidar': {'dev': 'phone', 'type': 'html', 'bg': '#d9cdb8', 'html': ios(True, lidar=True)},
    },
    'beats': [
        {'t': [0.0, 6.16], 'say': 'بتعرف إنّو فيك تحوّل تلفونك لمتر وتقيس طول أي غرض حواليك، من دون ما تحتاج متر حقيقي؟',
         'cap': 'حوّل تلفونك لمتر وقيس أي غرض حواليك 📏📱', 'capsize': 84, 'pose': 'point', 'hook': True},
        {'t': [6.36, 11.37], 'say': 'إذا معك آيفون، افتح تطبيق اسمه Measure، وجّه الكاميرا عالغرض اللي بدك تقيسه،',
         'cap': 'آيفون: افتح تطبيق Measure ووجّه الكاميرا عالغرض', 'pose': 'point', 'step': 1,
         'do': [{'nav': 'ios', 'style': 'fade', 'at': 0}]},
        {'t': [11.57, 16.71], 'say': 'حدّد نقطة البداية، وحرّك التلفون لنقطة النهاية. ورح يطلعلك القياس عالشاشة!',
         'cap': 'اكبس + عالبداية، حرّك للنهاية واكبس + كمان مرة ✅', 'pose': 'point', 'step': 2,
         'do': [{'tap': 'plus', 'at': .07}, {'tap': 'plus', 'at': (T_C - 11.57) / 5.14}]},
        {'t': [16.91, 26.66], 'say': 'أما إذا معك أندرويد، فيك تستخدم تطبيق Google Measure إذا كان متوفّر على جهازك، أو تطبيق قياس بيعتمد على الواقع المعزّز، متل AR Ruler.',
         'cap': 'أندرويد: تطبيق قياس بالواقع المعزّز متل AR Ruler', 'pose': 'talk', 'step': 3,
         'do': [{'nav': 'droid', 'at': 0}]},
        {'t': [26.86, 33.78], 'say': 'وفي بعض أجهزة الآيفون البرو وأجهزة تانية فيها حساس LiDAR، بتعطي قياسات أدقّ ببعض الحالات.',
         'cap': 'أجهزة فيها حساس LiDAR بتعطي قياس أدقّ ببعض الحالات', 'pose': 'welcome',
         'do': [{'nav': 'lidar', 'at': 0}]},
        {'t': [33.98, 39.83], 'say': 'بس انتبه، هالطريقة للقياسات التقريبية، مش بديلة عن المتر الحقيقي إذا بدك دقّة عالية.',
         'cap': '⚠️ قياس تقريبي، مش بديل عن المتر الحقيقي', 'pose': 'talk'},
        {'t': [40.03, 44.10], 'say': 'جرّبها، واعمل فولو لـ Tech Wall لمزيد من الحيل التكنولوجية!',
         'cap': 'جرّبها واعمل فولو لـ Tech Wall 🚀', 'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

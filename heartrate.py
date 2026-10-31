"""Tech Wall HOST episode (Galaxy, Arabic) with a supplied voice-over: measure your heart rate with the phone camera.
    ./build.sh heartrate  |  python3 heartrate.py 0 150 400
Voice: the user's Lebanese-Arabic audio, pauses between phrases shortened to 0.2 s (host/voices/heartrate.flac);
beats aligned to the script by its sentence pauses (template translate.py). Captions and chalk cards in Arabic.
Facts (Azumio app listings + reviews): Instant Heart Rate is free on Google Play and the App Store; fingertip over the
rear camera (and flash), hold still ~10 s; it reads the colour change of the fingertip with each beat (PPG) and shows
beats per minute; "for recreational and fitness use only". App and store screens are generic look-alikes, no logos."""
import host

EP = 'heartrate'
RED, YEL, CY, GRN = '#ff4d5e', '#ffd54a', '#5ce1ff', '#34d399'
AR = 'font-family:Cairo,Poppins,sans-serif'
SB = '<div class="sb"><span>10:08</span><span class="bat"></span></div>'
SBW = '<div class="sb" style="color:#fff"><span>10:08</span><span class="bat"></span></div>'
BEAT = 60 / 72                                     # 72 BPM


def beats(t0, t1):
    """Contiguous data-ring windows, one per heartbeat (--p 0->1 each beat)."""
    out, t = [], t0
    while t < t1:
        out.append(f'{t:.2f},{t + BEAT:.2f}'); t += BEAT
    return ';'.join(out)


WAVE = ("url(&quot;data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='90'>"
        "<path d='M0 60 L40 60 L52 58 L62 20 L72 75 L82 52 L96 60 L200 60' fill='none' stroke='%23ff4d5e' stroke-width='4' "
        "stroke-linejoin='round'/></svg>&quot;)")


def heart(win, size=130):
    return (f'<div data-ring="{win}" style="font-size:{size}px;line-height:1;text-align:center;'
            'transform:scale(calc(1.16 - var(--p,0) * .16));filter:drop-shadow(0 8px 18px rgba(255,77,94,.45))">❤️</div>')


RESULT = (SB + '<div style="padding:14px 24px 0;display:flex;align-items:center;gap:10px;font-size:22px;font-weight:700">'
          f'<span style="color:{RED}">♥</span> Instant Heart Rate</div>'
          '<div style="margin-top:46px">' + heart(beats(-1, 40)) + '</div>'
          f'<div style="text-align:center;margin-top:18px"><span style="font-size:110px;font-weight:800;color:{RED};line-height:1">72</span>'
          '<span style="font-size:28px;font-weight:700;color:#5a6b8c"> BPM</span></div>'
          f'<div data-scroll="-160,0" style="margin:22px 18px 0;height:90px;border-radius:18px;background:#fff {WAVE} repeat-x;'
          'box-shadow:0 2px 10px rgba(0,0,0,.06)"></div>'
          '<div style="text-align:center;margin-top:18px;font-size:17px;color:#137a43;font-weight:700">✓ Measured with your camera</div>'
          '<div style="text-align:center;margin-top:6px;font-size:14px;color:#8a8f99">Estimate · not a medical device</div>')

STORE = (SB + '<div style="margin:10px 14px 16px;height:54px;background:#fff;border-radius:27px;display:flex;align-items:center;'
         'padding:0 18px;gap:12px;font-size:18px"><span>🔍</span>Instant Heart Rate</div>'
         '<div style="margin:0 14px;background:#fff;border-radius:24px;padding:18px">'
         '<div style="display:flex;gap:16px;align-items:center"><div style="width:84px;height:84px;border-radius:22px;'
         f'background:linear-gradient(135deg,#ff6b7a,#d81b3c);display:grid;place-items:center;font-size:44px;color:#fff">♥</div>'
         '<div><div style="font-size:21px;font-weight:700">Instant Heart Rate</div>'
         '<div style="font-size:15px;color:#5a6b8c">Azumio · Health & Fitness</div>'
         '<div style="font-size:14px;color:#137a43;font-weight:700;margin-top:2px">Free</div></div></div>'
         '<div style="position:relative;height:50px;margin-top:16px">'
         '<div data-id="install" style="position:absolute;inset:0;border-radius:25px;background:#1a8a4a;color:#fff;display:grid;'
         'place-items:center;font-size:18px;font-weight:700">Install</div>'
         f'<div data-in="{4.16 + .72 * 4.28:.2f}" style="position:absolute;inset:0;border-radius:25px;background:#e7f6ee;'
         'color:#137a43;display:grid;place-items:center;font-size:18px;font-weight:800">✓ Installed · Open</div></div></div>'
         '<div style="display:flex;gap:10px;margin:14px 14px 0">'
         + ''.join(f'<div style="flex:1;height:250px;border-radius:18px;background:{b}"></div>'
                   for b in ('linear-gradient(#fff0f2,#ffd6dc)', 'linear-gradient(#f2f6ff,#d8e4ff)', 'linear-gradient(#fff7e8,#ffe2b8)'))
         + '</div>')

T_M0, T_M1 = 8.64, 20.2                          # measuring window (hold still … result)
MEASURE = ('<div data-ring="' + beats(T_M0, 30) + '" style="position:absolute;inset:0;'
           'background:radial-gradient(circle at 50% 46%,#ff5a4a 0%,#c4141e 45%,#5a0308 100%);'
           'filter:brightness(calc(1.12 - var(--p,0) * .2))"></div>' + SBW
           + '<div style="position:relative;text-align:center;color:#fff;padding-top:26px;font-size:21px;font-weight:700">'
             'Place your fingertip on the camera</div>'
           + '<div style="position:relative;text-align:center;color:#ffd6d6;font-size:15px;margin-top:4px">Cover the lens and the flash</div>'
           + f'<div data-ring="{T_M0 + .5:.2f},{T_M1 - .3:.2f}" style="position:absolute;left:82px;top:230px;width:240px;height:240px;'
             'border-radius:50%;background:conic-gradient(#fff calc(var(--p,0) * 360deg), rgba(255,255,255,.22) 0);'
             '-webkit-mask:radial-gradient(circle,transparent 104px,#000 106px);mask:radial-gradient(circle,transparent 104px,#000 106px)"></div>'
           + f'<div data-in="-1,{T_M1:.2f}" style="position:absolute;left:82px;top:230px;width:240px;height:240px;display:grid;'
             'place-items:center;color:#fff;font-size:22px;font-weight:700;text-align:center;line-height:1.3">Hold still…<br>'
             '<span style="font-size:15px;font-weight:500">Detecting pulse</span></div>'
           + f'<div data-in="{T_M1:.2f}" style="position:absolute;left:82px;top:230px;width:240px;height:240px;display:grid;'
             'place-items:center;color:#fff;text-align:center"><div><div style="font-size:84px;font-weight:800;line-height:1">72</div>'
             '<div style="font-size:22px;font-weight:700">BPM</div></div></div>'
           + f'<div data-scroll="-160,0" style="position:absolute;left:18px;right:18px;top:520px;height:90px;border-radius:18px;'
             f'background:rgba(0,0,0,.25) {WAVE.replace("%23ff4d5e", "%23ffffff")} repeat-x"></div>'
           + '<div style="position:absolute;left:0;right:0;top:630px;text-align:center;color:#ffd6d6;font-size:15px">'
             'Camera sees each beat as a tiny colour change</div>')


def card(win, top, html, border=YEL, width=520):
    return (f'<div data-in="{win}" dir="rtl" style="position:absolute;left:40px;top:{top}px;width:{width}px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:16px 22px;color:#fff;{AR}">{html}</div>')


# rear view of a phone with the fingertip over camera + flash (left of the stage, B2)
PHONE_BACK = (f'<div data-in="8.7,14.3" style="position:absolute;left:170px;top:230px;width:240px;height:420px">'
              '<div style="position:absolute;inset:0;border-radius:40px;background:#1b2233;border:4px solid #8a93b0"></div>'
              '<div style="position:absolute;left:34px;top:34px;width:100px;height:150px;border-radius:30px;background:#0b0f1a"></div>'
              '<div style="position:absolute;left:52px;top:52px;width:60px;height:60px;border-radius:50%;background:#222a40;border:4px solid #5a6380"></div>'
              f'<div data-ring="{beats(8.7, 15)}" style="position:absolute;left:146px;top:60px;width:30px;height:30px;border-radius:50%;'
              'background:#fff7c2;box-shadow:0 0 calc(30px + var(--p,0) * 10px) 12px rgba(255,240,150,.85)"></div>'
              '<div data-keys="9.4,120,-140,0,1;10.6,10,10,0,1" style="position:absolute;left:0;top:0;font-size:150px;'
              'transform-origin:50% 50%">☝️</div></div>'
              + card('8.7,14.3', 675, f'<div style="font-size:30px;font-weight:900;color:{YEL}">☝️ على الكاميرا والفلاش</div>'
                                      '<div style="font-size:26px;font-weight:700">خلّيه ثابت حوالي ١٠ ثواني</div>', CY))

PPG = ("<svg width='460' height='120' viewBox='0 0 460 120'><path d='M0 80 "
       + ' '.join(f'L{x + 30} 80 L{x + 45} 30 L{x + 60} 95 L{x + 75} 70 L{x + 92} 80' for x in range(0, 460, 92))
       + f"' fill='none' stroke='{RED}' stroke-width='6' stroke-linejoin='round'/></svg>")
OVERLAY = (
    card('-1,4.05', 260, f'<div style="font-size:50px;font-weight:900;color:{YEL};line-height:1.2">❤️ ٧٢ نبضة<br>بالدقيقة</div>'
                         '<div style="font-size:28px;font-weight:700;margin-top:6px">📱 من كاميرا التلفون بس</div>', RED)
    + card('4.2,8.5', 260, '<div style="font-size:28px;font-weight:700;color:#cfe3ff">تطبيق مجاني</div>'
                           f'<div style="font-size:38px;font-weight:900;color:{YEL};direction:ltr;text-align:right">Instant Heart Rate</div>'
                           '<div style="font-size:26px;font-weight:700;direction:ltr;text-align:right">Google Play · App Store</div>', GRN)
    + PHONE_BACK
    + card('14.4,20.35', 260, '<div style="font-size:30px;font-weight:900;color:#cfe3ff">كيف بيشتغل؟</div>'
                              f'<div style="margin:8px 0;background:rgba(255,255,255,.06);border-radius:16px">{PPG}</div>'
                              '<div style="font-size:25px;font-weight:700;line-height:1.5">كل نبضة بتغيّر لون إصبعك شوي<br>'
                              f'والتطبيق بيعدّ النبضات <span style="color:{YEL}">بالدقيقة</span></div>', RED)
    + card('20.55,25.3', 260, '<div style="display:flex;gap:34px;justify-content:center;font-size:52px;font-weight:900;text-align:center;line-height:1.2">'
                              '<div>⌚<br><span style="color:#ff6b6b">✕</span></div><div>🩺<br><span style="color:#ff6b6b">✕</span></div>'
                              f'<div>📱<br><span style="color:{GRN}">✓</span></div></div>'
                              '<div style="font-size:26px;font-weight:700;text-align:center;margin-top:6px">بلا ساعة ذكية أو جهاز خاص</div>', CY)
    + card('25.5,29.2', 300, '<div style="font-size:40px;font-weight:900;line-height:1.3">⚠️ النتيجة تقديرية</div>'
                             '<div style="font-size:28px;font-weight:700">مش بديل عن جهاز طبي</div>', '#ff6b6b'))

SPEC = {
    'audio': 'host/voices/heartrate.flac', 'lang': 'ar', 'device': 'galaxy', 'overlay': OVERLAY,
    'title': 'نبضات قلبك من الكاميرا ❤️', 'tag': 'HEALTH · CAMERA HEART RATE', 'tip': 'TIP #15',
    'start': 'res',
    'screens': {
        'res': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': RESULT},
        'store': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': STORE},
        'measure': {'dev': 'galaxy', 'type': 'html', 'bg': '#c4141e', 'html': MEASURE},
    },
    'beats': [
        {'t': [0.0, 3.96], 'say': 'بتعرف إنّو فيك تعرف قديش قلبك عم يدقّ، بس من كاميرا تلفونك؟',
         'cap': 'اعرف دقّات قلبك من كاميرا تلفونك ❤️📱', 'capsize': 84, 'pose': 'point', 'hook': True},
        {'t': [4.16, 8.44], 'say': 'في تطبيق اسمه Instant Heart Rate، فيك تنزّله من Google Play أو App Store.',
         'cap': 'نزّل تطبيق Instant Heart Rate من Google Play أو App Store', 'pose': 'point', 'step': 1,
         'do': [{'nav': 'store', 'style': 'fade', 'at': 0}, {'tap': 'install', 'at': .7}]},
        {'t': [8.64, 14.16], 'say': 'افتح التطبيق، وحطّ راس إصبعك على كاميرا التلفون، وخلّيه ثابت مع الفلاش لثواني.',
         'cap': 'افتح التطبيق وحطّ راس إصبعك على الكاميرا والفلاش ☝️', 'pose': 'talk', 'step': 2,
         'do': [{'nav': 'measure', 'style': 'fade', 'at': 0}]},
        {'t': [14.36, 20.32], 'say': 'التطبيق بيحلّل التغيّر بلون إصبعك مع كل نبضة، وبيحسبلك قديش نبضة قلبك بالدقيقة!',
         'cap': 'بيحلّل لون إصبعك مع كل نبضة وبيحسب نبضاتك بالدقيقة', 'pose': 'welcome', 'step': 3},
        {'t': [20.52, 25.25], 'say': 'يعني فيك تاخد فكرة عن دقّات قلبك من دون ساعة ذكية أو جهاز خاص.',
         'cap': 'فكرة عن دقّات قلبك بلا ساعة ذكية أو جهاز خاص ⌚', 'pose': 'talk',
         'do': [{'nav': 'res', 'style': 'fade', 'at': .05}]},
        {'t': [25.45, 29.12], 'say': 'بس تذكّر، النتيجة تقديرية ومش بديل عن جهاز طبي.',
         'cap': '⚠️ النتيجة تقديرية ومش بديل عن جهاز طبي', 'pose': 'point'},
        {'t': [29.32, 31.73], 'say': 'جرّبها وشوف قديش دقّات قلبك!', 'cap': 'جرّبها وشوف قديش دقّات قلبك! ❤️', 'pose': 'welcome',
         'do': [{'fx': 'confetti', 'at': .3}]},
        {'t': [31.93, 35.10], 'say': 'وتابع Tech Wall لمزيد من أسرار التكنولوجيا!',
         'cap': 'تابع Tech Wall لمزيد من أسرار التكنولوجيا! 🚀', 'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

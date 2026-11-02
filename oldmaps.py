"""Tech Wall HOST episode (Galaxy, Arabic) with a supplied voice-over: see your area 100 years ago with Old Maps Online.
    ./build.sh oldmaps  |  python3 oldmaps.py 0 150 400
Voice: the user's Lebanese-Arabic audio, pauses between phrases shortened to 0.2 s (host/voices/oldmaps.flac); beats
aligned to the script by its sentence pauses (template translate.py). Captions and chalk cards in Arabic.
Facts (oldmapsonline.org news 2023-01 + help 2024 + app page): search engine for historical maps from libraries
worldwide, by place and with a time slider; since Dec 2022 maps can be stacked/overlaid on today's map with a
transparency slider (also in the mobile app). Generic look-alikes (no logos); both maps are illustrations, not scans,
and the old map is labelled "example"."""
import host

EP = 'oldmaps'
YEL, CY, GRN, SEP = '#ffd54a', '#5ce1ff', '#34d399', '#8a6a3a'
AR = 'font-family:Cairo,Poppins,sans-serif'
SB = '<div class="sb"><span>10:08</span><span class="bat"></span></div>'
MW, MH = 404, 560                                  # map area inside the phone
SEA = 'M0 0 H404 V70 C320 96 240 52 160 104 C96 146 44 132 0 176 Z'
HWY = 'M-10 520 C120 470 240 400 414 300'          # today's road (fields in the old map)


def modern():
    streets = ''.join(f'<path d="{d}" stroke="#d6dae1" stroke-width="10" fill="none"/><path d="{d}" stroke="#fff" stroke-width="6" fill="none"/>'
                      for d in ['M0 230 H404', 'M0 300 H404', 'M0 380 H404', 'M0 450 H404', 'M60 150 V560', 'M140 120 V560',
                                'M220 100 V560', 'M300 90 V560', 'M370 80 V560', 'M0 200 L404 560', 'M180 110 L60 560'])
    blocks = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#e1e4ea"/>'
                     for x, y, w, h in [(70, 240, 60, 50), (150, 310, 60, 60), (230, 240, 60, 50), (310, 390, 50, 50),
                                        (70, 390, 60, 50), (230, 460, 60, 80), (150, 160, 60, 60), (310, 160, 50, 60)])
    return (f'<svg width="{MW}" height="{MH}" viewBox="0 0 {MW} {MH}"><rect width="{MW}" height="{MH}" fill="#eef0f3"/>'
            f'<path d="{SEA}" fill="#a9d3f5"/>{blocks}{streets}'
            f'<path d="{HWY}" stroke="#e8a93a" stroke-width="16" fill="none"/><path d="{HWY}" stroke="#ffd27a" stroke-width="11" fill="none"/>'
            '<text x="250" y="545" font-family="Poppins" font-size="18" font-weight="700" fill="#5a6b8c">2026</text></svg>')


def old(sfx):
    fields = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#crop{sfx})" stroke="#7d8a4a" stroke-width="1.5"/>'
                     for x, y, w, h in [(0, 430, 130, 110), (130, 380, 120, 120), (250, 300, 154, 130), (40, 470, 160, 90)])
    roads = ''.join(f'<path d="{d}" stroke="{SEP}" stroke-width="3" fill="none"/>'
                    for d in ['M0 250 C120 240 250 260 404 240', 'M140 120 C150 220 120 330 150 420', 'M300 96 C280 200 320 260 300 300',
                              'M60 160 C80 200 70 260 90 300'])
    houses = ''.join(f'<rect x="{x}" y="{y}" width="12" height="9" fill="#a0784a"/>'
                     for x, y in [(110, 200), (128, 214), (150, 196), (170, 230), (95, 262), (260, 210), (282, 226), (300, 190), (190, 270)])
    return (f'<svg width="{MW}" height="{MH}" viewBox="0 0 {MW} {MH}"><defs>'
            f'<pattern id="crop{sfx}" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">'
            '<rect width="10" height="10" fill="#d9d6a0"/><line x1="0" y1="0" x2="0" y2="10" stroke="#9aa45a" stroke-width="3"/></pattern>'
            f'<pattern id="wave{sfx}" width="24" height="10" patternUnits="userSpaceOnUse"><path d="M0 6 Q6 0 12 6 T24 6" fill="none" '
            'stroke="#7f9a8a" stroke-width="1.5"/></pattern></defs>'
            f'<rect width="{MW}" height="{MH}" fill="#ecdcb6"/><path d="{SEA}" fill="#c9d3bd"/><path d="{SEA}" fill="url(#wave{sfx})"/>'
            f'{fields}{roads}{houses}'
            '<text x="170" y="170" font-family="Georgia,serif" font-style="italic" font-size="26" fill="#5a3d1e">Beyrouth</text>'
            '<text x="40" y="545" font-family="Georgia,serif" font-size="18" fill="#5a3d1e">1912 · example</text>'
            '<text x="350" y="530" font-size="36" fill="#5a3d1e">✥</text></svg>')


def compare(keys_d, sfx):
    """Swipe compare: old map on the left of a divider, today on the right. keys_d = [(t, d)] where d = width hidden
    from the right (0 = all old, MW = all modern)."""
    k_box = ';'.join(f'{t:.2f},{-d},0' for t, d in keys_d)
    k_in = ';'.join(f'{t:.2f},{d},0' for t, d in keys_d)
    k_div = ';'.join(f'{t:.2f},{MW - d},0' for t, d in keys_d)
    return (f'<div style="position:absolute;left:0;top:150px;width:{MW}px;height:{MH}px;overflow:hidden">{modern()}'
            f'<div data-keys="{k_box}" style="position:absolute;left:0;top:0;width:{MW}px;height:{MH}px;overflow:hidden">'
            f'<div data-keys="{k_in}" style="position:absolute;left:0;top:0">{old(sfx)}</div></div>'
            f'<div data-keys="{k_div}" style="position:absolute;left:-2px;top:0;width:4px;height:{MH}px;background:#fff;'
            'box-shadow:0 0 8px rgba(0,0,0,.4)"><div style="position:absolute;left:-20px;top:250px;width:44px;height:44px;'
            'border-radius:50%;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.35);display:grid;place-items:center;'
            'font-size:18px;font-weight:800;color:#333">↔</div></div></div>')


HEAD = (SB + '<div style="padding:8px 20px 0;display:flex;align-items:center;gap:10px;font-size:21px;font-weight:700">'
        '🗺️ Old Maps Online</div>'
        '<div style="margin:10px 14px 0;height:46px;background:#fff;border-radius:23px;display:flex;align-items:center;'
        'padding:0 16px;gap:10px;font-size:17px;box-shadow:0 2px 8px rgba(0,0,0,.06)">🔍 <span>Beirut</span>'
        '<span style="margin-left:auto;font-size:14px;color:#5a6b8c">1912 ↔ today</span></div>')
D0 = MW // 2
RES_KEYS = [(-1, D0), (2.5, D0 - 70), (4.5, D0 + 70), (6.0, D0)]
COMPARE_KEYS = [(19.72, D0), (21.0, 40), (22.6, MW - 40), (24.0, D0), (26.5, D0), (27.6, 70), (34.6, 70), (35.6, D0)]
LEGEND = ('<div style="position:absolute;left:14px;right:14px;top:722px;display:flex;justify-content:space-between;font-size:15px;'
          'font-weight:700"><span style="color:#8a6a3a">◀ 1912</span><span style="color:#5a6b8c">Opacity / swipe</span>'
          '<span style="color:#3e6fb0">Today ▶</span></div>')
RES = HEAD + compare(RES_KEYS, 'a') + LEGEND
CMP = HEAD + compare(COMPARE_KEYS, 'b') + LEGEND + (
    f'<div data-in="28.4,34.5" style="position:absolute;left:120px;top:440px;width:200px;height:150px;border:4px dashed {YEL};'
    'border-radius:20px;box-shadow:0 0 18px rgba(255,213,74,.6)"></div>')

RESULTS = [('1876', '#e6d3a8'), ('1912', '#ecdcb6'), ('1936', '#e2d6bd'), ('1958', '#dfe3d6')]
SEARCH = (SB + '<div style="padding:8px 20px 0;display:flex;align-items:center;gap:10px;font-size:21px;font-weight:700">'
          '🗺️ Old Maps Online</div>'
          '<div style="margin:10px 14px 0;height:46px;background:#fff;border-radius:23px;display:flex;align-items:center;'
          'padding:0 16px;gap:10px;font-size:17px;box-shadow:0 2px 8px rgba(0,0,0,.06)">🔍 <span data-type="search:q"></span></div>'
          # world map with pins (before the search)
          '<div data-in="-1,14.6" style="position:absolute;left:14px;right:14px;top:150px;height:300px;border-radius:20px;'
          'background:#cfe4f5;overflow:hidden">'
          '<svg width="376" height="300" viewBox="0 0 376 300"><g fill="#e9e2cc">'
          '<path d="M30 70 C70 40 120 50 140 90 C150 130 110 150 90 190 C70 170 40 130 30 70Z"/>'
          '<path d="M170 60 C210 40 260 50 300 70 C330 90 340 130 300 150 C270 160 240 140 210 150 C190 130 170 100 170 60Z"/>'
          '<path d="M200 160 C230 160 250 190 240 240 C225 270 205 250 200 210Z"/>'
          '<path d="M290 200 C320 195 345 215 335 240 C315 250 295 235 290 200Z"/></g>'
          + ''.join(f'<circle data-in="{6.6 + i * .25:.2f}" cx="{x}" cy="{y}" r="7" fill="#d9534f" stroke="#fff" stroke-width="2"/>'
                    for i, (x, y) in enumerate([(80, 90), (110, 150), (200, 80), (240, 95), (262, 118), (280, 75), (220, 200),
                                                (310, 215), (60, 120), (250, 140)]))
          + '</svg></div>'
          # timeline (with the world map, before the search)
          '<div data-in="-1,14.6" style="position:absolute;left:14px;right:14px;top:466px;background:#fff;border-radius:18px;padding:12px 16px">'
          '<div style="display:flex;justify-content:space-between;font-size:13px;color:#5a6b8c"><span>1700</span><span>Year</span><span>2026</span></div>'
          '<div style="position:relative;height:6px;border-radius:3px;background:#e3e5ea;margin-top:8px">'
          '<div style="position:absolute;left:52%;right:8%;top:0;bottom:0;background:#3e91ff;border-radius:3px"></div>'
          '<i style="position:absolute;left:52%;top:-7px;width:20px;height:20px;margin-left:-10px;border-radius:50%;background:#3e91ff"></i>'
          '<i style="position:absolute;left:92%;top:-7px;width:20px;height:20px;margin-left:-10px;border-radius:50%;background:#3e91ff"></i></div></div>'
          # results (after the search)
          f'<div data-in="14.6" style="position:absolute;left:14px;right:14px;top:150px">'
          '<div style="font-size:15px;color:#5a6b8c;margin:0 4px 8px">Maps of Beirut · 1700–2026</div>'
          + ''.join(f'<div data-id="m{y}" style="display:flex;gap:12px;align-items:center;background:#fff;border-radius:16px;'
                    f'padding:8px;margin-bottom:8px"><div style="width:62px;height:62px;border-radius:10px;background:{c};'
                    'border:1px solid #c9b48a;display:grid;place-items:center;font-size:24px">🗺️</div>'
                    f'<div><div style="font-size:18px;font-weight:700">Beirut · {y}</div>'
                    '<div style="font-size:13px;color:#8a8f99">Historical map · library scan</div></div></div>' for y, c in RESULTS)
          + '</div>')


def card(win, top, html, border=YEL, width=520):
    return (f'<div data-in="{win}" dir="rtl" style="position:absolute;left:40px;top:{top}px;width:{width}px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:16px 22px;color:#fff;{AR}">{html}</div>')


OVERLAY = (
    card('-1,5.9', 260, f'<div style="font-size:54px;font-weight:900;color:{YEL};line-height:1.15">🕰️ 1912 ← 2026</div>'
                        '<div style="font-size:32px;font-weight:800;margin-top:6px">نفس المنطقة، من تلفونك 📱</div>')
    + card('6.1,12.8', 260, '<div style="font-size:28px;font-weight:700;color:#cfe3ff">موقع مجاني</div>'
                            f'<div style="font-size:44px;font-weight:900;color:{YEL};direction:ltr;text-align:right">Old Maps Online</div>'
                            '<div style="font-size:28px;font-weight:700">🌍 خرائط قديمة من مكتبات العالم</div>', CY)
    + card('13.0,19.6', 260, '<div style="font-size:34px;font-weight:900;line-height:1.45">🛣️ شوارع<br>🏘️ أحياء<br>🏛️ مباني</div>'
                             f'<div style="font-size:28px;font-weight:800;color:{YEL}">من عشرات لمئات السنين</div>', GRN)
    + card('19.8,25.7', 260, '<div style="font-size:40px;font-weight:900;line-height:1.3">📜 زمان ↔️ اليوم</div>'
                             '<div style="font-size:28px;font-weight:700">اسحب وشوف قديش تغيّرت</div>', CY)
    + card('25.9,34.6', 260, '<div style="font-size:30px;font-weight:800;color:#cfe3ff">جرّب منطقتك بلبنان 🇱🇧</div>'
                             f'<div style="font-size:44px;font-weight:900;color:{YEL};line-height:1.3">🌾 أرض زراعية<br>← 🛣️ شارعك اليوم</div>', GRN)
    + card('34.8,40.95', 260, '<div style="font-size:36px;font-weight:900;line-height:1.5">🔮 المستقبل<br>📜 وأسرار الماضي</div>'
                              f'<div style="font-size:28px;font-weight:700;color:{YEL}">التكنولوجيا بتكشف الاثنين</div>', CY))

SPEC = {
    'audio': 'host/voices/oldmaps.flac', 'lang': 'ar', 'device': 'galaxy', 'overlay': OVERLAY,
    'title': 'شوف منطقتك قبل 100 سنة 🗺️', 'tag': 'OLD MAPS ONLINE · HISTORY', 'tip': 'TIP #16',
    'start': 'res',
    'screens': {
        'res': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': RES},
        'search': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': SEARCH},
        'cmp': {'dev': 'galaxy', 'type': 'html', 'bg': '#f4f4f6', 'html': CMP},
    },
    'beats': [
        {'t': [0.0, 5.81], 'say': 'تخيّل لو فيك ترجع بالزمن وتشوف كيف كانت منطقتك قبل مية سنة، وكل هيدا من تلفونك!',
         'cap': 'شوف كيف كانت منطقتك قبل 100 سنة 🗺️', 'capsize': 84, 'pose': 'point', 'hook': True},
        {'t': [6.01, 12.70], 'say': 'في موقع اسمه Old Maps Online، بيخلّيك تكتشف خرائط قديمة لمدن ومناطق من كل أنحاء العالم.',
         'cap': 'موقع Old Maps Online فيه خرائط قديمة من كل العالم 🌍', 'pose': 'point', 'step': 1,
         'do': [{'nav': 'search', 'style': 'fade', 'at': 0}]},
        {'t': [12.90, 19.52], 'say': 'يعني فيك تفتّش عن مدينتك وتشوف كيف كانت شوارعها وأحياؤها ومبانيها من عشرات أو حتى مئات السنين.',
         'cap': 'فتّش عن مدينتك وشوف شوارعها ومبانيها من مئات السنين', 'pose': 'talk', 'step': 2,
         'do': [{'typetext': 'Beirut', 'into': 'q', 'from': .05, 'to': .2}, {'tap': 'm1912', 'at': .78, 'nav': 'cmp', 'style': 'zoom', 'fx': .4}]},
        {'t': [19.72, 25.62], 'say': 'والأحلى؟ فيك تقارن الخريطة القديمة مع شكل المنطقة اليوم، وتشوف قديش تغيّرت مع الوقت.',
         'cap': 'قارن الخريطة القديمة مع اليوم وشوف قديش تغيّرت ↔️', 'pose': 'point', 'step': 3},
        {'t': [25.82, 34.53], 'say': 'جرّب فتّش عن منطقتك بلبنان، ويمكن تكتشف إنو الشارع اللي بتمرق فيه كل يوم كان زمان أرض زراعية أو حتى ما كان موجود!',
         'cap': 'جرّب منطقتك بلبنان: يمكن شارعك كان أرض زراعية! 🌾', 'pose': 'welcome'},
        {'t': [34.73, 40.89], 'say': 'التكنولوجيا مش بس بتفرجينا شو جايي بالمستقبل، كمان بتخلّينا نكتشف أسرار من الماضي!',
         'cap': 'التكنولوجيا بتكشف أسرار الماضي كمان 📜', 'pose': 'talk'},
        {'t': [41.09, 44.40], 'say': 'تابع Tech Wall لتكتشف كل يوم شي جديد!',
         'cap': 'تابع Tech Wall لتكتشف كل يوم شي جديد! 🚀', 'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

"""Tech Wall HOST episode (laptop, Arabic) with a supplied voice-over: translate a whole website in one click (Chrome / Edge).
    ./build.sh translate  |  python3 translate.py 0 150 400
Voice: the user's Lebanese-Arabic audio, pauses between phrases shortened to 0.2 s (host/voices/translate.flac);
beats were aligned to the script by its sentence pauses (the offline Whisper model is English-only); lip-sync uses
Rhubarb's phonetic recognizer. Captions are Arabic (RTL, Cairo font).
Facts (Chrome / Edge help, 2026): Chrome > ⋮ > Translate… translates the page; Edge shows a translate icon in the
address bar on foreign pages > Translate; both offer Show original. Generic browser look-alikes, no logos; the site is
fictional (cafe.example.com)."""
import host

EP = 'translate'
YEL, CY, GRN, BLU = '#ffd54a', '#5ce1ff', '#34d399', '#1a73e8'
T_CHR = 10.28 + .82 * 3.95 + .22           # Chrome page translated
T_EDGE = 14.43 + .84 * 4.45 + .22          # Edge page translated
AR = "font-family:Cairo,Poppins,sans-serif"

DE = {'nav': ['Startseite', 'Rezepte', 'Reisen', 'Kontakt'], 'title': 'Die 10 besten Cafés in Berlin',
      'p': 'Von gemütlichen Ecken bis zu modernen Röstereien: hier sind unsere Lieblingsorte für den perfekten Kaffee.',
      'more': 'Weiterlesen', 'sub': 'Abonnieren', 'side': 'Beliebte Artikel', 'list': ['Reiseführer München', 'Brezeln selber backen'],
      'font': 'font-family:Poppins', 'dir': 'ltr'}
ARB = {'nav': ['الرئيسية', 'وصفات', 'سفر', 'اتصل بنا'], 'title': 'أفضل 10 مقاهٍ في برلين',
       'p': 'من الزوايا الدافئة إلى المحامص الحديثة: هذه أماكننا المفضلة لفنجان قهوة مثالي.',
       'more': 'اقرأ المزيد', 'sub': 'اشترك', 'side': 'مقالات شائعة', 'list': ['دليل السفر إلى ميونخ', 'خبز البريتزل في البيت'],
       'font': AR, 'dir': 'rtl'}


def page(L, hl=None):
    """The fictional café blog (920x442 under the browser bar). hl = (t_nav, t_article, t_buttons) highlight rings."""
    ring = lambda t, x, y, w, h: (f'<div data-in="{t:.2f},{t + 2.6:.2f}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
                                  f'height:{h}px;border:4px solid {YEL};border-radius:14px;box-shadow:0 0 18px rgba(255,213,74,.7)"></div>')
    return (f'<div style="position:absolute;left:0;right:0;top:76px;bottom:0;background:#fffaf3;color:#2b1d12;{L["font"]}">'
            '<div style="height:56px;background:#3b2a1e;color:#fff;display:flex;align-items:center;gap:26px;padding:0 26px;font-size:17px">'
            '<b style="font-size:20px;font-family:Poppins">☕ Café Blog</b>'
            + ''.join(f'<span dir="{L["dir"]}">{n}</span>' for n in L['nav']) + '</div>'
            '<div style="display:flex;gap:24px;padding:20px 26px">'
            f'<div style="flex:1" dir="{L["dir"]}"><div style="font-size:31px;font-weight:800;line-height:1.25">{L["title"]}</div>'
            '<div style="height:120px;border-radius:14px;margin:12px 0;background:linear-gradient(135deg,#c08552,#5e3b1f)"></div>'
            f'<div style="font-size:16px;line-height:1.6;color:#4a3a2c">{L["p"]}</div>'
            '<div style="display:flex;gap:10px;margin-top:12px">'
            f'<span style="background:#c0392b;color:#fff;border-radius:18px;padding:6px 18px;font-size:15px;font-weight:700">{L["more"]}</span>'
            f'<span style="border:2px solid #3b2a1e;border-radius:18px;padding:4px 16px;font-size:15px;font-weight:700">{L["sub"]}</span></div></div>'
            f'<div style="width:220px;background:#f3e6d6;border-radius:14px;padding:14px" dir="{L["dir"]}">'
            f'<div style="font-weight:800;font-size:17px;margin-bottom:8px">{L["side"]}</div>'
            + ''.join(f'<div style="font-size:15px;padding:6px 0;border-top:1px solid #e0cdb8">{x}</div>' for x in L['list'])
            + '</div></div>'
            + (ring(hl[0], 6, 4, 620, 50) + ring(hl[1], 18, 70, 640, 300) + ring(hl[2], 452, 286, 210, 56) if hl else '')
            + '</div>')


def chrome(url, edge=False, tr_icon=False, menu=False):
    """Generic browser chrome: tab strip + address bar (Chrome-like, or Edge-like with a translate icon in the bar)."""
    tab_bg, bar_bg = ('#dee1e6', '#fff') if not edge else ('#f3f3f3', '#fff')
    name = 'Edge' if edge else 'Chrome'
    icon = (f'<span data-id="tricon" style="width:34px;height:30px;border-radius:8px;display:grid;place-items:center;font-size:16px;'
            f'font-weight:800;color:{BLU};background:#e8f0fe">文A</span>') if tr_icon else ''
    dots = '<span data-id="menu" style="width:30px;height:30px;display:grid;place-items:center;font-size:22px;color:#444">⋮</span>' \
        if menu else '<span style="width:30px;text-align:center;font-size:20px;color:#444">⋯</span>'
    return (f'<div style="position:absolute;left:0;right:0;top:0;height:36px;background:{tab_bg};display:flex;align-items:flex-end;'
            'padding-left:12px;font-family:Poppins;font-size:13px">'
            f'<span style="background:{bar_bg};border-radius:{"10px 10px 0 0" if not edge else "8px 8px 0 0"};padding:8px 18px;'
            'min-width:180px;color:#333">☕ Café Blog</span>'
            f'<span style="margin-left:auto;margin-right:14px;align-self:center;color:#777;font-size:12px;font-weight:700">{name}</span></div>'
            f'<div style="position:absolute;left:0;right:0;top:36px;height:40px;background:{bar_bg};display:flex;align-items:center;gap:10px;'
            'padding:0 12px;border-bottom:1px solid #e3e3e3;font-family:Poppins;font-size:14px;color:#333">'
            '<span style="color:#777">‹ ›</span><span style="flex:1;background:#f1f3f4;border-radius:16px;padding:5px 14px">'
            f'🔒 {url}</span>{icon}{dots}</div>')


CHROME_MENU = ('<div style="position:absolute;right:14px;top:74px;width:230px;background:#fff;border-radius:10px;'
               'box-shadow:0 10px 30px rgba(0,0,0,.3);padding:6px 0;font-family:Poppins;font-size:15px;color:#222;z-index:9">'
               + ''.join(f'<div{" data-id=\"tr\"" if i == "Translate…" else ""} style="padding:8px 18px'
                         f'{";background:#e8f0fe;font-weight:700" if i == "Translate…" else ""}">{i}</div>'
                         for i in ('New tab', 'History', 'Downloads', 'Translate…', 'Settings')) + '</div>')
EDGE_POP = ('<div style="position:absolute;right:46px;top:74px;width:300px;background:#fff;border-radius:10px;'
            'box-shadow:0 10px 30px rgba(0,0,0,.3);padding:14px 16px;font-family:Poppins;font-size:14px;color:#222;z-index:9">'
            '<div style="font-weight:700;font-size:16px">Translate page?</div>'
            f'<div style="margin-top:6px">German › <span style="{AR}">العربية</span></div>'
            f'<div data-id="go" style="margin-top:10px;background:{BLU};color:#fff;border-radius:6px;padding:7px;text-align:center;'
            'font-weight:700">Translate</div></div>')


def bubble(win, orig=False):
    return (f'<div data-in="{win}" style="position:absolute;right:46px;top:74px;width:250px;background:#fff;border-radius:10px;'
            'box-shadow:0 10px 30px rgba(0,0,0,.3);padding:10px 14px;font-family:Poppins;font-size:14px;color:#222;z-index:9">'
            f'<div>✓ Translated from German</div><div style="display:flex;gap:8px;margin-top:8px">'
            f'<span style="flex:1;border:1px solid #ccc;border-radius:6px;padding:4px;text-align:center">German</span>'
            f'<span style="flex:1;background:{BLU};color:#fff;border-radius:6px;padding:4px;text-align:center;{AR}">العربية</span></div>'
            + (f'<div data-id="orig" style="margin-top:8px;color:{BLU};font-weight:700;text-align:center">↩ Show original</div>' if orig else '')
            + '</div>')


URL = 'cafe.example.com/de'
SCREENS = {
    'res': {'type': 'html', 'bg': '#fff', 'html': chrome(URL) + page(ARB) + bubble('-1')},
    'chr_de': {'type': 'html', 'bg': '#fff', 'html': chrome(URL, menu=True) + page(DE), 'pops': {'menu': CHROME_MENU}},
    'chr_ar': {'type': 'html', 'bg': '#fff', 'html': chrome(URL) + page(ARB) + bubble(f'{T_CHR:.2f},{T_CHR + 2.2:.2f}')},
    'edge_de': {'type': 'html', 'bg': '#fff', 'html': chrome(URL, edge=True, tr_icon=True) + page(DE), 'pops': {'pop': EDGE_POP}},
    'edge_ar': {'type': 'html', 'bg': '#fff', 'html': chrome(URL, edge=True, tr_icon=True) + page(ARB, (19.9, 21.3, 22.6))
                + bubble('24.6', orig=True)},
    'edge_back': {'type': 'html', 'bg': '#fff', 'html': chrome(URL, edge=True, tr_icon=True) + page(DE)},
}


def card(win, top, html, border=YEL):
    return (f'<div data-in="{win}" style="position:absolute;left:560px;top:{top}px;width:480px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:14px 22px;color:#fff;{AR}" dir="rtl">'
            f'{html}</div>')


OVERLAY = (card('-1,5.75', 840, f'<div style="font-size:30px;font-weight:800;color:#cfe3ff;{AR}">🇩🇪 ألماني ← 🇱🇧 عربي</div>'
                                 f'<div style="font-size:44px;font-weight:900;color:{YEL}">بكبسة زر وحدة</div>')
           + card('5.9,10.1', 840, '<div style="font-size:30px;font-weight:800;line-height:1.5">📋 نسخ ← 🌐 ترجمة ← 📋 لزق</div>'
                                   f'<div style="font-size:40px;font-weight:900;color:#ff6b6b">❌ ما بقا في داعي</div>', '#ff6b6b')
           + card('10.3,14.3', 840, '<div style="font-size:34px;font-weight:900;direction:ltr">Chrome</div>'
                                    f'<div style="font-size:30px;font-weight:800;color:{YEL};direction:ltr">⋮ › Translate</div>', CY)
           + card('14.45,18.9', 840, '<div style="font-size:34px;font-weight:900;direction:ltr">Edge</div>'
                                     f'<div style="font-size:30px;font-weight:800;color:{YEL}">أيقونة 文A حدّ شريط العنوان</div>', CY))

SPEC = {
    'audio': 'host/voices/translate.flac', 'lang': 'ar', 'device': 'laptop', 'overlay': OVERLAY,
    'title': 'ترجم أي موقع بكبسة زر 🌐', 'tag': 'CHROME · EDGE · TRANSLATE', 'tip': 'TIP #14',
    'start': 'res', 'screens': SCREENS,
    'beats': [
        {'t': [0.0, 5.70], 'say': 'تخيّل تفتح موقع بلغة ما بتفهمها، وبكبسة زر وحدة بيصير الموقع كلّه بلغتك!',
         'cap': 'ترجم أي موقع كامل بكبسة زر وحدة 🌐', 'capsize': 84, 'pose': 'point', 'hook': True},
        {'t': [5.90, 10.08], 'say': 'ما بقا مضطر تنسخ النص وتروح على Google Translate وترجع تلزّقو.',
         'cap': 'ما في داعي تنسخ وتلزّق بموقع ترجمة ❌', 'pose': 'talk',
         'do': [{'nav': 'chr_de', 'style': 'fade', 'at': 0}]},
        {'t': [10.28, 14.23], 'say': 'إذا عم تستعمل Chrome، اكبس على الثلاث نقاط واختار Translate،',
         'cap': 'بـ Chrome اكبس الثلاث نقاط ⋮ واختار Translate', 'pose': 'point',
         'do': [{'tap': 'menu', 'at': .45}, {'show': 'menu', 'at': .52}, {'tap': 'tr', 'at': .82, 'nav': 'chr_ar', 'style': 'fade'}]},
        {'t': [14.43, 18.88], 'say': 'وإذا عم تستعمل Microsoft Edge، اكبس على أيقونة الترجمة حدّ شريط العنوان.',
         'cap': 'بـ Edge اكبس أيقونة الترجمة حدّ شريط العنوان', 'pose': 'point',
         'do': [{'nav': 'edge_de', 'style': 'fade', 'at': 0}, {'tap': 'tricon', 'at': .55}, {'show': 'pop', 'at': .6},
                {'tap': 'go', 'at': .84, 'nav': 'edge_ar', 'style': 'fade'}]},
        {'t': [19.08, 24.40], 'say': 'بثواني، الموقع كلّه بيصير بلغتك، من المقالات للقوائم والأزرار!',
         'cap': 'بثواني الموقع كلّه بلغتك: المقالات، القوائم والأزرار ✅', 'pose': 'welcome'},
        {'t': [24.60, 27.72], 'say': 'والأحلى؟ فيك ترجع للغة الأصلية بأي وقت.',
         'cap': 'والأحلى؟ فيك ترجع للغة الأصلية بأي وقت ↩️', 'pose': 'talk',
         'do': [{'tap': 'orig', 'at': .55, 'nav': 'edge_back', 'style': 'fade'}]},
        {'t': [27.92, 31.84], 'say': 'تابع Tech Wall لتكتشف أسرار وحيل تكنولوجية جديدة كل يوم!',
         'cap': 'تابع Tech\u00a0Wall لأسرار تكنولوجية جديدة كل يوم! 🚀', 'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

"""Tech Wall HOST episode (iPhone, Arabic) with a supplied voice-over: see less inappropriate content on Instagram.
    ./build.sh igsafe  |  python3 igsafe.py 0 150 400
Voice: the user's Lebanese-Arabic generated audio, pauses between phrases shortened to 0.2 s (host/voices/igsafe.flac);
beat 't' = [start, end] s in it; script transcribed with the multilingual Whisper turbo model (template flashlight.py).
Facts (Instagram Help Center "About Sensitive Content Control" + iPhone app article; about.instagram.com updates):
Profile > menu (top right) > Suggested content > Sensitive content > More / Standard (default) / Less ("More" is not
available under 18); it applies to recommendations (Explore, Reels, Search, suggested posts) from accounts you DON'T
follow; Suggested content also has Specific words and phrases (hide suggested posts with those words) and Reset
suggested content; "Not interested" in a post's ... menu. Newer app versions name the page "Content preferences".
Generic look-alike screens (no logo, no real accounts), fictional data. Chalk cards on the left: spec 'overlay'."""
import host

EP = 'igsafe'
YEL, CY, GRN, RED = '#ffd54a', '#5ce1ff', '#34d399', '#ff6b6b'
AR = 'font-family:Cairo,Poppins,sans-serif'
BLUE = '#0095f6'
T_LESS = 20.84                                   # "Less" radio tapped
T_W = (31.4, 32.2, 33.0)                          # word chips typed
T_DOTS, T_NI = 42.37, 44.56                       # "..." tapped, "Not interested" tapped
T_RESET, T_RESET2 = 54.84, 57.35                  # "Reset suggested content" row, then the dialog's Reset button
T_UNF = 67.58                                     # "Following" tapped -> unfollow


def sb(col='#111'):
    return f'<div class="sb" style="color:{col};position:relative;z-index:3"><span>10:08</span><span class="bat"></span></div>'


def top(title, back=True):
    b = '<span style="position:absolute;left:18px;top:8px;font-size:30px;line-height:1">‹</span>' if back else ''
    return (f'<div style="position:relative;height:52px;border-bottom:1px solid #e6e6e6;text-align:center;font-weight:700;font-size:19px;'
            f'line-height:52px">{b}{title}</div>')


def row(label, rid=None, sub='', value='', chev=True, col='#111', icon=''):
    a = f' data-id="{rid}"' if rid else ''
    ic = f'<span style="width:30px;font-size:20px;text-align:center">{icon}</span>' if icon else ''
    return (f'<div{a} style="display:flex;align-items:center;gap:12px;padding:14px 18px;min-height:30px;background:#fff">{ic}'
            f'<div style="flex:1"><div style="font-size:17px;color:{col}">{label}</div>'
            + (f'<div style="font-size:13px;color:#8e8e8e;margin-top:2px">{sub}</div>' if sub else '') + '</div>'
            + (f'<span style="font-size:15px;color:#8e8e8e">{value}</span>' if value else '')
            + ('<span style="color:#c7c7cc;font-size:22px">›</span>' if chev else '') + '</div>')


def section(t):
    return f'<div style="padding:16px 18px 6px;font-size:14px;font-weight:700;color:#8e8e8e;background:#fff">{t}</div>'


def nav_bar(active='home'):
    items = [('home', '⌂'), ('search', '⌕'), ('add', '⊕'), ('reels', '▶'), ('me', '◉')]
    return ('<div style="position:absolute;left:0;right:0;bottom:0;height:78px;background:#fff;border-top:1px solid #e6e6e6;'
            'display:flex;justify-content:space-around;align-items:flex-start;padding-top:12px;font-size:26px;z-index:3">'
            + ''.join(f'<span style="color:{"#111" if k == active else "#9a9a9a"}">{g}</span>' for k, g in items) + '</div>')


def post(user, colour, body, rid_dots=None, cap='', blur=False):
    dots = f' data-id="{rid_dots}"' if rid_dots else ''
    pic = (f'<div style="height:300px;background:{colour};position:relative;overflow:hidden;display:grid;place-items:center;'
           f'font-size:110px">{body}'
           + ('<div style="position:absolute;inset:0;backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);background:rgba(20,20,30,.35);'
              'display:grid;place-items:center;color:#fff;text-align:center;font-size:18px;font-weight:700">'
              '<div><div style="font-size:54px">⚠️</div>Sensitive content</div></div>' if blur else '') + '</div>')
    return (f'<div style="background:#fff"><div style="display:flex;align-items:center;gap:10px;padding:10px 14px">'
            f'<span style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#f9a825,#d81b60)"></span>'
            f'<b style="flex:1;font-size:15px">{user}</b><span{dots} style="font-size:24px;padding:0 6px;letter-spacing:1px">⋯</span></div>'
            f'{pic}<div style="padding:8px 14px;font-size:22px;letter-spacing:6px">♡ ◯ ➤</div>'
            + (f'<div style="padding:0 14px 10px;font-size:14px">{cap}</div>' if cap else '') + '</div>')


def feed_top():
    return ('<div style="height:50px;display:flex;align-items:center;justify-content:space-between;padding:0 18px;background:#fff">'
            '<b style="font-size:23px;font-family:Georgia,serif;font-style:italic">For you ▾</b><span style="font-size:24px">♡ ✉</span></div>')


FEED = ('<div style="position:absolute;inset:0;background:#fff">' + sb() + feed_top()
        + post('suggested.clips', '#3b2a4a', '🎬', cap='Suggested for you', blur=True)
        + post('daily.vids', '#2c3e50', '📹', blur=True) + '</div>' + nav_bar('home'))

PROFILE = ('<div style="position:absolute;inset:0;background:#fff">' + sb()
           + '<div style="height:52px;display:flex;align-items:center;justify-content:space-between;padding:0 18px">'
             '<b style="font-size:21px">family.home ▾</b><span style="display:flex;gap:18px;font-size:26px"><span>⊕</span>'
             '<span data-id="menu" style="font-size:28px;padding:0 4px">☰</span></span></div>'
           + '<div style="display:flex;align-items:center;gap:26px;padding:10px 20px">'
             '<span style="width:86px;height:86px;border-radius:50%;background:linear-gradient(135deg,#ffd54a,#ff6b6b)"></span>'
           + ''.join(f'<div style="text-align:center"><b style="font-size:18px">{n}</b><div style="font-size:13px">{l}</div></div>'
                     for n, l in [('24', 'posts'), ('180', 'followers'), ('95', 'following')]) + '</div>'
           + '<div style="padding:0 20px;font-size:15px;font-weight:600">Family Home</div>'
           + '<div style="display:flex;gap:8px;padding:14px 20px"><div style="flex:1;background:#efefef;border-radius:10px;padding:8px;'
             'text-align:center;font-size:14px;font-weight:600">Edit profile</div><div style="flex:1;background:#efefef;border-radius:10px;'
             'padding:8px;text-align:center;font-size:14px;font-weight:600">Share profile</div></div>'
           + '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-top:10px">'
           + ''.join(f'<div style="height:130px;background:{c};display:grid;place-items:center;font-size:44px">{e}</div>'
                     for c, e in [('#ffe0b2', '🍰'), ('#c8e6c9', '🌳'), ('#bbdefb', '🏖️'), ('#f8bbd0', '🎂'), ('#d1c4e9', '🐶'), ('#fff9c4', '🌻')])
           + '</div></div>' + nav_bar('me'))

MENU = ('<div style="position:absolute;inset:0;background:#f2f2f2">' + sb() + top('Settings and activity')
        + '<div style="margin:8px 0">' + section('How you use Instagram')
        + row('Saved', icon='🔖') + row('Archive', icon='🕘') + row('Your activity', icon='📊') + row('Notifications', icon='🔔')
        + row('Time management', icon='⏱️') + '</div><div>' + section('What you see')
        + row('Favorites', icon='☆') + row('Muted accounts', icon='🔕')
        + row('Suggested content', 'sugg', icon='📋') + row('Like and share counts', icon='♡') + '</div></div>')


def sugg_html():
    sens_val = (f'<span data-in="-1,{T_LESS + .25:.2f}">Standard</span>'
                f'<span data-in="{T_LESS + .25:.2f}" style="color:{BLUE};font-weight:700">Less</span>')
    words_val = f'<span data-in="{T_W[2] + .3:.2f}" style="color:{BLUE};font-weight:700">3</span>'
    dialog = (f'<div data-in="{T_RESET + .25:.2f},{T_RESET2 + .3:.2f}" style="position:absolute;inset:0;background:rgba(0,0,0,.45);z-index:5">'
              '<div style="position:absolute;left:34px;right:34px;top:250px;background:#fff;border-radius:18px;overflow:hidden;text-align:center">'
              '<div style="padding:22px 20px 8px;font-weight:700;font-size:19px">Reset suggested content?</div>'
              '<div style="padding:0 22px 16px;font-size:14px;color:#737373">Your suggestions will start fresh. Accounts you follow stay the same.</div>'
              f'<div data-id="resetbtn" style="border-top:1px solid #e6e6e6;padding:14px;color:#ed4956;font-weight:700;font-size:17px">Reset</div>'
              '<div style="border-top:1px solid #e6e6e6;padding:14px;font-size:17px">Cancel</div></div></div>')
    toast = (f'<div data-in="{T_RESET2 + .3:.2f}" style="position:absolute;left:24px;right:24px;bottom:40px;background:#262626;color:#fff;'
             'border-radius:12px;padding:14px 16px;font-size:15px;z-index:6">✓ Suggested content reset</div>')
    return ('<div style="position:absolute;inset:0;background:#f2f2f2">' + sb() + top('Suggested content')
            + '<div style="padding:12px 18px;font-size:13px;color:#737373;background:#fff">Choose what you see in Explore, Reels, Search and suggested posts.</div>'
            + row('Sensitive content', 'sens', value=sens_val)
            + row('Political content', value='Limit')
            + row('Specific words and phrases', 'words', value=words_val)
            + row('Snooze suggested posts in feed', chev=False, value='<span style="display:inline-block;width:46px;height:28px;border-radius:14px;background:#d1d1d6"></span>')
            + '<div style="height:12px"></div>'
            + row('Reset suggested content', 'reset', col='#ed4956', chev=False)
            + '<div style="padding:12px 18px;font-size:12px;color:#8e8e8e">Some app versions: Settings › Content preferences</div></div>'
            + dialog + toast)


def radio(on_at=None, default_on=False):
    ring = 'width:24px;height:24px;border-radius:50%;border:2px solid #c7c7cc;box-sizing:border-box;position:relative;flex:none'
    dot = (f'<i data-in="{on_at:.2f}" style="position:absolute;inset:-2px;border-radius:50%;border:7px solid #111"></i>' if on_at else
           ('<i data-in="-1,%.2f" style="position:absolute;inset:-2px;border-radius:50%%;border:7px solid #111"></i>' % (T_LESS + .1) if default_on else ''))
    return f'<span style="{ring}">{dot}</span>'


def opt(label, sub, rid=None, r=''):
    a = f' data-id="{rid}"' if rid else ''
    return (f'<div{a} style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;background:#fff;border-bottom:1px solid #efefef">'
            f'<div style="flex:1"><div style="font-size:17px;font-weight:600">{label}</div><div style="font-size:13px;color:#737373;margin-top:3px">{sub}</div></div>{r}</div>')


SENS = ('<div style="position:absolute;inset:0;background:#f2f2f2">' + sb() + top('Sensitive content')
        + '<div style="padding:14px 18px;font-size:14px;color:#737373;background:#fff">Some posts may be upsetting. Choose how much you see in Explore, Reels, Search and suggested posts.</div>'
        + opt('More', 'Not available for people under 18', r=radio())
        + opt('Standard (Default)', 'You may see some sensitive content', r=radio(default_on=True))
        + opt('Less', 'You may see less sensitive content', 'less', r=radio(T_LESS + .1))
        + f'<div data-in="{T_LESS + .3:.2f}" style="margin:18px;padding:12px;border-radius:12px;background:#e8f8ef;color:#137a3d;font-size:15px;'
          'font-weight:600;text-align:center">✓ Less selected</div></div>')

CHIP = ('<span data-in="{t:.2f}" style="display:inline-block;margin:6px;padding:8px 14px;border-radius:18px;background:#efefef;'
        'font-size:15px;font-weight:600">{w} ✕</span>')
WORDS = ('<div style="position:absolute;inset:0;background:#fff">' + sb() + top('Specific words and phrases')
         + '<div style="padding:14px 18px;font-size:14px;color:#737373">Don\'t show suggested posts with these words, phrases or emojis.</div>'
         + '<div style="margin:6px 18px;padding:12px 14px;border:1px solid #dbdbdb;border-radius:12px;font-size:16px;color:#8e8e8e">Add words…</div>'
         + '<div style="padding:8px 12px">' + ''.join(CHIP.format(t=t, w=w) for t, w in zip(T_W, ['horror', 'violence', 'scary'])) + '</div>'
         + '<div style="position:absolute;left:0;right:0;bottom:0;height:250px;background:#d1d3d9;display:grid;grid-template-columns:repeat(10,1fr);'
           'gap:6px;padding:12px 6px 40px;box-sizing:border-box">'
         + ''.join(f'<span style="background:#fff;border-radius:6px;display:grid;place-items:center;font-size:17px">{k}</span>'
                   for k in 'qwertyuiopasdfghjkl;zxcvbnm,.?') + '</div></div>')

SHEET = (f'<div data-in="{T_DOTS + .25:.2f},{T_NI + .3:.2f}" style="position:absolute;inset:0;background:rgba(0,0,0,.4);z-index:5">'
         '<div style="position:absolute;left:0;right:0;bottom:0;background:#fff;border-radius:18px 18px 0 0;padding:10px 0 34px">'
         '<div style="width:40px;height:5px;border-radius:3px;background:#dbdbdb;margin:0 auto 8px"></div>'
         + row('Interested', chev=False, icon='👁️') + row('Not interested', 'notint', chev=False, icon='🚫')
         + row('Why you\'re seeing this post', chev=False, icon='ℹ️') + row('Report', chev=False, col='#ed4956', icon='⚠️') + '</div></div>')
POST = ('<div style="position:absolute;inset:0;background:#fff">' + sb() + feed_top()
        + f'<div data-in="-1,{T_NI + .35:.2f}">' + post('random.clips', '#4a2c2c', '🎭', 'dots', 'Suggested for you') + '</div>'
        + f'<div data-in="{T_NI + .35:.2f}" style="position:absolute;left:0;right:0;top:112px;background:#fafafa;padding:30px 24px;text-align:center;'
          'font-size:16px;color:#262626">✓ We\'ll suggest fewer posts like this<div style="font-size:14px;color:#8e8e8e;margin-top:6px">Post hidden</div></div>'
        + '</div>' + nav_bar('home') + SHEET)

ACCT = ('<div style="position:absolute;inset:0;background:#fff">' + sb()
        + '<div style="height:52px;display:flex;align-items:center;gap:14px;padding:0 18px;font-size:19px"><span style="font-size:30px">‹</span>'
          '<b>loud.prank.page</b></div>'
        + '<div style="display:flex;align-items:center;gap:26px;padding:10px 20px">'
          '<span style="width:86px;height:86px;border-radius:50%;background:linear-gradient(135deg,#8e8e8e,#3a3a3a)"></span>'
        + ''.join(f'<div style="text-align:center"><b style="font-size:18px">{n}</b><div style="font-size:13px">{l}</div></div>'
                  for n, l in [('812', 'posts'), ('40K', 'followers'), ('12', 'following')]) + '</div>'
        + '<div style="display:flex;gap:8px;padding:14px 20px"><div data-id="following" style="flex:1;border-radius:10px;padding:9px;text-align:center;'
          'font-size:15px;font-weight:700;position:relative">'
          f'<span data-in="-1,{T_UNF + .25:.2f}" style="position:absolute;inset:0;background:#efefef;border-radius:10px;display:grid;place-items:center">Following ▾</span>'
          f'<span data-in="{T_UNF + .25:.2f}" style="position:absolute;inset:0;background:{BLUE};color:#fff;border-radius:10px;display:grid;place-items:center">Follow</span>'
          '&nbsp;</div><div style="flex:1;background:#efefef;border-radius:10px;padding:9px;text-align:center;font-size:15px;font-weight:600">Message</div></div>'
        + '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-top:10px">'
        + ''.join('<div style="height:130px;background:#2c2c34;display:grid;place-items:center;color:#fff;font-size:15px;font-weight:700">⚠️</div>' for _ in range(6))
        + '</div>'
        + f'<div data-in="{T_UNF + .4:.2f}" style="position:absolute;left:24px;right:24px;bottom:110px;background:#262626;color:#fff;border-radius:12px;'
          'padding:14px 16px;font-size:15px">✓ Unfollowed loud.prank.page</div></div>' + nav_bar('search'))

CLEAN = ('<div style="position:absolute;inset:0;background:#fff">' + sb() + feed_top()
         + post('kitchen.daily', '#ffe0b2', '🍰', cap='Easy family cake 🎂') + post('pets.world', '#d1c4e9', '🐶') + '</div>' + nav_bar('home'))


def card(win, top_, html, border=YEL, width=520):
    return (f'<div data-in="{win}" dir="rtl" style="position:absolute;left:40px;top:{top_}px;width:{width}px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:16px 22px;color:#fff;{AR}">{html}</div>')


def step(n, title, path, col=YEL):
    return (f'<div style="font-size:30px;font-weight:900;color:{col}">{n}</div>'
            f'<div style="font-size:34px;font-weight:900;direction:ltr;text-align:right;line-height:1.25">{title}</div>'
            f'<div style="font-size:22px;font-weight:700;color:#cfe3ff;direction:ltr;text-align:right;margin-top:6px">{path}</div>')


OVERLAY = (
    card('-1,4.7', 250, f'<div style="font-size:46px;font-weight:900;color:{YEL};line-height:1.3">⚠️ فيديو مش لائق</div>'
                        '<div style="font-size:32px;font-weight:800">… والولاد حدّك! 👨‍👩‍👧</div>', RED)
    + card('4.9,9.7', 250, f'<div style="font-size:44px;font-weight:900;color:{YEL}">⏱️ أقلّ من دقيقة</div>'
                           '<div style="font-size:28px;font-weight:800">وبتخفّف هالنوع من المحتوى</div>', CY)
    + card('10.1,27.2', 250, step('① حساسيّة المحتوى', 'Sensitive content › Less', '☰ › Suggested content › Sensitive content'), YEL)
    + card('21.8,27.2', 540, '<div style="font-size:26px;font-weight:800;line-height:1.5">بيخفّف بالاقتراحات:<br>'
                             '<span dir="ltr">Explore · Reels · Search</span></div>', CY)
    + card('27.6,38.7', 250, step('② كلمات بعينها', 'Specific words and phrases', 'اكتب الكلمات اللي ما بدّك تشوفها'), YEL)
    + card('38.85,50.0', 250, step('③ ما عجبك؟', '⋯ › Not interested', 'بيفهم إنستغرام شو ما بدّك'), YEL)
    + card('50.15,58.7', 250, step('④ صفحة جديدة', 'Reset suggested content', 'الاقتراحات بترجع من الأوّل'), YEL)
    + card('58.85,65.0', 250, '<div style="font-size:36px;font-weight:900;color:' + YEL + '">⚠️ انتبه</div>'
                              '<div style="font-size:28px;font-weight:800;line-height:1.45">هالإعدادات بتأثّر على الاقتراحات<br>من حسابات <u>مش متابعها</u></div>', RED)
    + card('65.15,70.1', 250, '<div style="font-size:30px;font-weight:800;line-height:1.45">حساب إنت متابعه<br>وعم ينزّل هالمحتوى؟</div>'
                              f'<div style="font-size:44px;font-weight:900;color:{YEL};direction:ltr;text-align:right">Unfollow</div>', RED)
    + card('70.3,76.0', 250, f'<div style="font-size:42px;font-weight:900;color:{GRN};line-height:1.3">✅ إنستغرام أنضف</div>'
                             '<div style="font-size:30px;font-weight:800">وأنسب إلك ولعيلتك 👨‍👩‍👧‍👦</div>', GRN))

SPEC = {
    'audio': 'host/voices/igsafe.flac', 'lang': 'ar', 'device': 'phone', 'overlay': OVERLAY,
    'title': 'خفّف المحتوى المش لائق على إنستغرام 🛡️', 'tag': 'INSTAGRAM · SENSITIVE CONTENT', 'tip': 'TIP #19',
    'start': 'feed',
    'screens': {
        'feed': {'type': 'html', 'bg': '#fff', 'html': FEED},
        'profile': {'type': 'html', 'bg': '#fff', 'html': PROFILE},
        'menu': {'type': 'html', 'bg': '#f2f2f2', 'html': MENU},
        'sugg': {'type': 'html', 'bg': '#f2f2f2', 'html': sugg_html()},
        'sens': {'type': 'html', 'bg': '#f2f2f2', 'html': SENS},
        'words': {'type': 'html', 'bg': '#fff', 'html': WORDS},
        'post': {'type': 'html', 'bg': '#fff', 'html': POST},
        'acct': {'type': 'html', 'bg': '#fff', 'html': ACCT},
        'clean': {'type': 'html', 'bg': '#fff', 'html': CLEAN},
    },
    'beats': [
        {'t': [0.24, 4.62], 'say': 'فتحت إنستغرام، وفجأة طلعلك فيديو مش لائق، وولادك قاعدين حدّك؟',
         'cap': 'فيديو مش لائق على إنستغرام… والولاد حدّك؟ 😳', 'capsize': 84, 'pose': 'welcome', 'hook': True},
        {'t': [5.00, 9.62], 'say': 'تعا خلّيني فرجيك كيف بتخفّف ظهور هالنوع من المحتوى، بأقلّ من دقيقة.',
         'cap': 'تعا فرجيك كيف بتخفّفه بأقلّ من دقيقة ⏱️', 'pose': 'talk'},
        {'t': [10.24, 17.69], 'say': 'أوّل شي، فوت عالبروفايل تبعك، واكبس عالتلات خطوط اللي فوق عاليمين. نزال شوي، وفوت على Suggested content.',
         'cap': 'افتح البروفايل، اكبس ☰ وفوت على Suggested\u00a0content', 'pose': 'point', 'step': 1, 'screen': 'profile', 'style': 'fade',
         'do': [{'tap': 'menu', 'at': .45, 'nav': 'menu'}, {'tap': 'sugg', 'at': .88, 'nav': 'sugg'}]},
        {'t': [17.93, 21.57], 'say': 'هلّق اكبس على Sensitive content، واختار Less.',
         'cap': 'اكبس على Sensitive\u00a0content واختار Less ✅', 'pose': 'point',
         'do': [{'tap': 'sens', 'at': .3, 'nav': 'sens'}, {'tap': 'less', 'at': (T_LESS - 17.93) / 3.64}]},
        {'t': [21.83, 27.15], 'say': 'هيك إنستغرام بيخفّفلك ظهور هالنوع من المحتوى بالـExplore والـReels والـSearch.',
         'cap': 'بيخفّفلك هالمحتوى بالـExplore والـReels والـSearch', 'pose': 'talk'},
        {'t': [27.69, 34.33], 'say': 'تاني خطوة، بنفس الصفحة، فوت على Specific words and phrases، واكتب الكلمات اللي ما بدّك تشوف محتوى عنها.',
         'cap': 'فوت على Specific\u00a0words\u00a0and\u00a0phrases واكتب الكلمات اللي ما بدّك تشوفها', 'pose': 'point', 'step': 2,
         'do': [{'nav': 'sugg', 'style': 'pop', 'at': 0}, {'tap': 'words', 'at': .38, 'nav': 'words'}]},
        {'t': [34.61, 38.59], 'say': 'هيك إنستغرام بيخفّفلك المنشورات المقترحة اللي فيها هالكلمات.',
         'cap': 'وبيخفّف المنشورات المقترحة اللي فيها هالكلمات', 'pose': 'talk'},
        {'t': [38.94, 45.18], 'say': 'تالت خطوة، إذا طلعلك فيديو أو بوست ما عجبك، اكبس عالتلات نقاط واختار Not interested.',
         'cap': 'بوست ما عجبك؟ اكبس ⋯ واختار Not\u00a0interested', 'pose': 'point', 'step': 3, 'screen': 'post', 'style': 'fade',
         'do': [{'tap': 'dots', 'at': (T_DOTS - 38.94) / 6.24}, {'tap': 'notint', 'at': (T_NI - 38.94) / 6.24}]},
        {'t': [45.60, 49.92], 'say': 'وكل ما تعمل هيك، بتساعد إنستغرام يفهم شو المحتوى اللي ما بدّك ياه.',
         'cap': 'وكل مرّة بتساعد إنستغرام يفهم شو ما بدّك 🧠', 'pose': 'talk'},
        {'t': [50.24, 58.60], 'say': 'وإذا حسّيت إنّو الاقتراحات كلّها صارت بعيدة عن اهتماماتك، فيك تفوت على Reset suggested content، وترجع الاقتراحات من الأوّل.',
         'cap': 'الاقتراحات بعيدة عنك؟ اكبس Reset\u00a0suggested\u00a0content 🔄', 'pose': 'point', 'step': 4, 'screen': 'sugg', 'style': 'fade',
         'do': [{'tap': 'reset', 'at': (T_RESET - 50.24) / 8.36}, {'tap': 'resetbtn', 'at': (T_RESET2 - 50.24) / 8.36}]},
        {'t': [58.88, 64.90], 'say': 'بس انتبه، هالإعدادات بتأثّر بشكل أساسي عالمحتوى المقترح من حسابات مش متابعها.',
         'cap': 'انتبه: بتأثّر على المقترح من حسابات مش متابعها ⚠️', 'pose': 'talk'},
        {'t': [65.21, 69.95], 'say': 'أمّا إذا في حساب إنت متابعه وعم ينزّل هالنوع من المحتوى، لازم تعمله Unfollow.',
         'cap': 'حساب متابعه وعم ينزّل هالمحتوى؟ اعمله Unfollow', 'pose': 'point', 'screen': 'acct', 'style': 'fade',
         'do': [{'tap': 'following', 'at': (T_UNF - 65.21) / 4.74}]},
        {'t': [70.50, 75.56], 'say': 'هيك بتكون أخدت خطوات بسيطة، لتخلّي إنستغرام أنضف وأنسب إلك ولعيلتك.',
         'cap': 'خطوات بسيطة: إنستغرام أنضف وأنسب إلك ولعيلتك ✅', 'pose': 'welcome', 'screen': 'clean', 'style': 'fade',
         'do': [{'fx': 'thumb', 'at': .05, 'dur': 3}, {'fx': 'confetti', 'at': .1}]},
        {'t': [75.85, 78.89], 'say': 'تابعونا على Tech Wall للمزيد من أسرار التكنولوجيا.',
         'cap': 'تابعونا على Tech Wall للمزيد من أسرار التكنولوجيا 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

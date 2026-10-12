"""Tech Wall HOST episode with a supplied voice-over: protect your WhatsApp with two-step verification.
    ./build.sh whatsapp2fa  |  python3 whatsapp2fa.py 0 150 400
The voice is the user's generated audio (host/voices/whatsapp2fa.flac); each beat's 't' = [start, end] s in it.
WhatsApp Help Center (two-step verification): Settings > Account > Two-step verification > Turn on, create the
credential, add an email address (optional, used to reset it). Since 2026-08-25 WhatsApp is replacing the 6-digit PIN
with a password (8+ characters, a letter and a number), rolling out gradually; existing PINs keep working.
Generic chat-app look-alike: no logo, fictional data (Sam, Mom, sam@example.com)."""
import host

EP = 'whatsapp2fa'
G = '#1fa855'                                   # generic chat-app green (no logo anywhere)
SB = '<div class="sb"><span>10:08</span><span class="bat"></span></div>'
SB_DARK = '<div class="sb" style="color:#fff"><span>10:08</span><span class="bat"></span></div>'
BTN = (f'position:absolute;left:28px;right:28px;height:58px;border-radius:29px;background:{G};color:#fff;'
       'font-weight:700;font-size:20px;display:grid;place-items:center')
SHIELD = ('<svg viewBox="0 0 120 140" style="width:{w}px"><path d="M60 6c22 14 34 16 52 16 0 58-18 94-52 112C26 116 8 80 8 22c18 0 '
          '30-2 52-16z" fill="{c}"/>{inner}</svg>')
LOCK_IN = ('<path d="M44 66V56a16 16 0 0 1 32 0v10" fill="none" stroke="#fff" stroke-width="8"/>'
           '<rect x="36" y="64" width="48" height="38" rx="8" fill="#fff"/><circle cx="60" cy="83" r="6" fill="{c}"/>')
CHECK_IN = '<path d="M38 72l15 15 30-32" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'


def avatar(ch, col):
    return (f'<div style="width:54px;height:54px;border-radius:50%;background:{col};color:#fff;font-weight:700;'
            f'font-size:22px;display:grid;place-items:center;flex:none">{ch}</div>')


def chat_row(ch, col, name, msg, time):
    return (f'<div style="display:flex;gap:14px;align-items:center;padding:12px 18px;border-bottom:1px solid #eee">'
            f'{avatar(ch, col)}<div style="flex:1"><div style="display:flex;justify-content:space-between">'
            f'<b style="font-size:18px">{name}</b><span style="font-size:14px;color:#8a8a8e">{time}</span></div>'
            f'<div style="font-size:15px;color:#6d6d72;margin-top:3px">{msg}</div></div></div>')


TABS = ''.join(f'<div{" data-id=%s" % chr(34) + "settings" + chr(34) if k == "Settings" else ""} style="flex:1;text-align:center;'
               f'font-size:12px;color:{G if k == "Chats" else "#3a3a3c"};font-weight:{700 if k == "Chats" else 500}">'
               f'<div style="width:26px;height:26px;margin:0 auto 4px;border-radius:{8 if k != "Settings" else 13}px;'
               f'background:{G if k == "Chats" else "#c7c7cc"}"></div>{k}</div>'
               for k in ('Updates', 'Calls', 'Communities', 'Chats', 'Settings'))

CHATS = f'''<div style="position:absolute;inset:0;background:#fff;color:#111;font-family:Poppins">{SB}
<div style="font-size:34px;font-weight:700;padding:6px 20px 10px">Chats</div>
<div style="margin:0 16px 10px;height:40px;border-radius:12px;background:#efeff4;color:#8a8a8e;font-size:16px;display:flex;align-items:center;padding:0 14px">⌕ Ask or Search</div>
{chat_row('M', '#ff7a45', 'Mom', 'Dinner at 8? 🍝', '10:02')}
{chat_row('S', '#5c6cff', 'Sam', 'Sent you the photos', '09:41')}
{chat_row('F', '#34c759', 'Family', 'Dad: Who is coming Sunday?', 'Yesterday')}
{chat_row('W', '#bf5af2', 'Work Team', 'Meeting moved to 3 pm', 'Yesterday')}
<div style="position:absolute;left:0;right:0;bottom:0;height:96px;border-top:1px solid #e3e3e8;background:#f9f9f9;display:flex;align-items:flex-start;padding:12px 6px 0">{TABS}</div></div>'''

INTRO = f'''<div style="position:absolute;inset:0;background:#fff;color:#111;font-family:Poppins">{SB}
<div class="nav" style="color:{G}">‹ Account</div>
<div style="text-align:center;margin-top:40px">{SHIELD.format(w=150, c=G, inner=LOCK_IN.format(c=G))}</div>
<div style="text-align:center;font-size:26px;font-weight:700;margin-top:18px">Two-step verification</div>
<div style="font-size:17px;color:#6d6d72;text-align:center;margin:14px 34px 0;line-height:1.45">For extra security, turn on two-step verification. You'll need it when you register your phone number with WhatsApp again.</div>
<div data-id="turnon" style="{BTN};top:600px">Turn on</div></div>'''

PASSWORD = f'''<div style="position:absolute;inset:0;background:#fff;color:#111;font-family:Poppins">{SB}
<div class="nav" style="color:{G}">‹ Back</div>
<div style="text-align:center;font-size:26px;font-weight:700;margin-top:30px">Create a password</div>
<div style="font-size:16px;color:#6d6d72;text-align:center;margin:12px 34px 0;line-height:1.45">At least 8 characters, with at least one letter and one number.</div>
<div style="margin:44px 34px 0;border-bottom:3px solid {G};height:56px;font-size:34px;letter-spacing:6px;display:flex;align-items:center;justify-content:center"><span data-type="password:pw"></span><span class="caret"></span></div>
<div style="font-size:14px;color:#8a8a8e;text-align:center;margin-top:12px">Older versions ask for a 6-digit PIN</div>
<div data-id="next" style="{BTN};top:600px">Next</div></div>'''

EMAIL = f'''<div style="position:absolute;inset:0;background:#fff;color:#111;font-family:Poppins">{SB}
<div class="nav" style="color:{G}">‹ Back</div>
<div style="text-align:center;margin-top:20px">{SHIELD.format(w=90, c='#e8f7ee', inner='<text x="60" y="88" text-anchor="middle" font-size="48" fill="' + G + '">@</text>')}</div>
<div style="text-align:center;font-size:26px;font-weight:700;margin-top:10px">Add email address</div>
<div style="font-size:16px;color:#6d6d72;text-align:center;margin:12px 34px 0;line-height:1.45">Add an email address so you can reset your password if you ever forget it.</div>
<div style="margin:40px 34px 0;border-bottom:3px solid {G};height:52px;font-size:22px;display:flex;align-items:center"><span data-type="email:addr"></span><span class="caret"></span></div>
<div data-id="enext" style="{BTN};top:600px">Next</div></div>'''

RESULT = f'''<div style="position:absolute;inset:0;background:#fff;color:#111;font-family:Poppins">{SB}
<div class="nav" style="color:{G}">‹ Account</div>
<div style="text-align:center;margin-top:36px">{SHIELD.format(w=160, c=G, inner=CHECK_IN)}</div>
<div style="text-align:center;font-size:26px;font-weight:700;margin-top:18px">Two-step verification is on</div>
<div style="font-size:16px;color:#6d6d72;text-align:center;margin:12px 34px 0;line-height:1.45">A stolen code alone is no longer enough: you'll need your password to register WhatsApp again.</div>
<div style="margin:34px 16px 0;border-radius:14px;overflow:hidden;background:#f2f2f7">
  <div style="padding:16px 18px;font-size:18px;color:#ff3b30;border-bottom:1px solid #e3e3e8">Turn off</div>
  <div style="padding:16px 18px;font-size:18px;color:{G};border-bottom:1px solid #e3e3e8">Change password</div>
  <div style="padding:16px 18px;font-size:18px;color:{G}">Change email address</div></div></div>'''

RISK = f'''<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 20%,#4b2a6b 0%,#24123d 55%,#0c0618 100%);color:#fff;font-family:Poppins">{SB_DARK}
<div style="text-align:center;font-size:22px;font-weight:500;opacity:.9;margin-top:10px">Monday, October 12</div>
<div style="text-align:center;font-size:96px;font-weight:600;line-height:1;margin-top:4px">10:08</div>
<div style="position:absolute;left:16px;right:16px;top:290px;border-radius:22px;background:rgba(255,255,255,.88);color:#111;padding:14px 16px">
  <div style="display:flex;justify-content:space-between;font-size:14px;color:#6d6d72"><b style="color:#34c759">● MESSAGES</b><span>now</span></div>
  <div style="font-size:17px;margin-top:6px;line-height:1.35"><b>Your WhatsApp code: 483-921</b><br>Don't share this code with others.</div></div></div>'''
WARN = ('<div style="position:absolute;left:22px;right:22px;top:470px;border-radius:20px;background:#ff3b30;color:#fff;padding:18px;'
        'text-align:center;box-shadow:0 14px 30px rgba(0,0,0,.45)"><div style="font-size:40px">⚠️</div>'
        '<div style="font-size:20px;font-weight:800;margin-top:4px">Someone is logging in<br>with your number</div></div>')
NEVER = ('<div style="position:absolute;left:40px;right:40px;top:450px;height:240px;border-radius:28px;background:#fff;color:#111;'
         'text-align:center;box-shadow:0 18px 40px rgba(0,0,0,.5);padding-top:26px"><div style="width:96px;height:96px;margin:0 auto;'
         'border-radius:50%;border:10px solid #ff3b30;position:relative"><i style="position:absolute;left:-6px;right:-6px;top:33px;'
         'height:10px;background:#ff3b30;transform:rotate(-45deg)"></i></div><div style="font-size:24px;font-weight:800;margin-top:16px">'
         'Never share your code</div><div style="font-size:15px;color:#6d6d72">Not even with "WhatsApp support"</div></div>')

APPS = [{'id': 'photos', 'label': 'Photos', 'icon': 'photos', 'bg': 'linear-gradient(#fff,#f0f0f0)'},
        {'id': 'mail', 'label': 'Mail', 'icon': 'mail', 'bg': 'linear-gradient(#5ac8fa,#007aff)'},
        {'id': 'maps', 'label': 'Maps', 'icon': 'maps', 'bg': 'linear-gradient(#76e07a,#2fb344)'},
        {'id': 'clock', 'label': 'Clock', 'icon': 'clock', 'bg': '#1c1c1e'},
        {'id': 'camera', 'label': 'Camera', 'icon': 'camera', 'bg': 'linear-gradient(#d1d1d6,#8e8e93)'},
        {'id': 'wa', 'label': 'WhatsApp', 'icon': 'chat', 'bg': f'linear-gradient(#4cd47f,{G})'},
        {'id': 'notes', 'label': 'Notes', 'icon': 'notes', 'bg': 'linear-gradient(#fff6c2,#ffd60a)'},
        {'id': 'settings', 'label': 'Settings', 'icon': 'gear', 'bg': 'linear-gradient(#a1a1a6,#636366)'},
        {'id': 'weather', 'label': 'Weather', 'icon': 'weather', 'bg': 'linear-gradient(#64d2ff,#0a84ff)'},
        {'id': 'videos', 'label': 'Videos', 'icon': 'videos', 'bg': 'linear-gradient(#bf5af2,#7b2ff7)'},
        {'id': 'books', 'label': 'Books', 'icon': 'books', 'bg': 'linear-gradient(#ffb340,#ff9500)'},
        {'id': 'stocks', 'label': 'Stocks', 'icon': 'stocks', 'bg': 'linear-gradient(#30d158,#248a3d)'}]

SPEC = {
    'audio': 'host/voices/whatsapp2fa.flac', 'lang': 'en',
    'title': 'Protect your WhatsApp 🔐', 'tag': 'TWO-STEP VERIFICATION', 'tip': 'TIP #04',
    'start': 'result',
    'screens': {
        'result': {'type': 'html', 'bg': '#fff', 'html': RESULT},
        'risk': {'type': 'html', 'bg': '#24123d', 'html': RISK, 'pops': {'warn': WARN, 'never': NEVER}},
        'home': {'type': 'home', 'apps': APPS},
        'chats': {'type': 'html', 'bg': '#fff', 'html': CHATS},
        'settings': {'type': 'list', 'title': 'Settings', 'groups': [
            {'rows': [{'id': 'me', 'label': 'Sam · Hey there! I am using WhatsApp', 'icon': 'person', 'color': '#8e8e93'}]},
            {'rows': [{'id': 'account', 'label': 'Account', 'icon': 'key', 'color': G, 'chev': True},
                      {'id': 'privacy', 'label': 'Privacy', 'icon': 'lock', 'color': '#0a84ff', 'chev': True},
                      {'id': 'chatsrow', 'label': 'Chats', 'icon': 'chat', 'color': '#34c759', 'chev': True},
                      {'id': 'notif', 'label': 'Notifications', 'icon': 'bell', 'color': '#ff3b30', 'chev': True},
                      {'id': 'storage', 'label': 'Storage and data', 'icon': 'storage', 'color': '#30b0c7', 'chev': True}]}]},
        'account': {'type': 'list', 'back': 'Settings', 'title': 'Account', 'groups': [
            {'rows': [{'id': 'secnot', 'label': 'Security notifications', 'chev': True},
                      {'id': 'passkeys', 'label': 'Passkeys', 'chev': True},
                      {'id': 'emailrow', 'label': 'Email address', 'chev': True},
                      {'id': 'tsv', 'label': 'Two-step verification', 'chev': True},
                      {'id': 'number', 'label': 'Change number', 'chev': True}]},
            {'rows': [{'id': 'info', 'label': 'Request account info', 'chev': True},
                      {'id': 'delete', 'label': 'Delete account', 'style': 'red'}]}]},
        'intro': {'type': 'html', 'bg': '#fff', 'html': INTRO},
        'password': {'type': 'html', 'bg': '#fff', 'html': PASSWORD},
        'email': {'type': 'html', 'bg': '#fff', 'html': EMAIL},
    },
    # 't' = where each line sits in the voice file (measured: speech chunks + transcript)
    'beats': [
        {'t': [0.24, 5.24], 'say': 'Someone steals your WhatsApp verification code, and suddenly your account is at risk.',
         'cap': "Protect your WhatsApp before it's too late! 🔐", 'pose': 'welcome', 'hook': True,
         'do': [{'nav': 'risk', 'style': 'fade', 'at': .12}, {'show': 'warn', 'at': .72}]},
        {'t': [5.84, 8.80], 'say': "But there's a simple way to make it much harder for hackers.",
         'cap': 'A stolen code = a stolen account. Here is the fix', 'pose': 'talk',
         'do': [{'hide': 'warn', 'at': .1}, {'nav': 'home', 'style': 'fade', 'at': .82}]},
        {'t': [9.46, 12.46], 'say': 'Open WhatsApp. Go to settings, then account.',
         'cap': 'Step 1: Open WhatsApp › Settings › Account', 'pose': 'point', 'step': 1,
         'do': [{'tap': 'wa', 'at': .1, 'nav': 'chats'}, {'tap': 'settings', 'at': .55, 'nav': 'settings'},
                {'tap': 'account', 'at': .88, 'nav': 'account', 'fx': .4}]},
        {'t': [12.80, 14.98], 'say': 'And select two-step verification.',
         'cap': 'Step 2: Two-step verification', 'pose': 'point', 'step': 2,
         'do': [{'tap': 'tsv', 'at': .6, 'nav': 'intro', 'fx': .4}]},
        {'t': [15.86, 20.42], 'say': 'Enable it and create a strong password, or a PIN if your app still uses one.',
         'cap': 'Step 3: Turn on › create a strong password (or PIN)', 'pose': 'talk', 'step': 3,
         'do': [{'tap': 'turnon', 'at': .1, 'nav': 'password', 'fx': .5},
                {'typetext': '••••••••••', 'into': 'pw', 'from': .32, 'to': .62}, {'tap': 'next', 'at': .9, 'nav': 'email', 'fx': .5}]},
        {'t': [21.20, 23.10], 'say': "Don't forget to add your recovery email.",
         'cap': 'Step 4: Add a recovery email', 'pose': 'point', 'step': 4,
         'do': [{'typetext': 'sam@example.com', 'into': 'addr', 'from': .25, 'to': .7}, {'tap': 'enext', 'at': .92, 'fx': .5}]},
        {'t': [23.94, 29.02], 'say': "Now, even if someone steals your login code, there's an extra security barrier protecting your account.",
         'cap': 'Done ✅ A stolen code is no longer enough', 'pose': 'welcome',
         'do': [{'nav': 'result', 'style': 'zoom', 'at': .0}, {'fx': 'thumb', 'at': .3, 'dur': 2.6}, {'fx': 'confetti', 'at': .32}]},
        {'t': [29.74, 34.20], 'say': 'And remember... Never share your verification code with anyone.',
         'cap': 'Never share your verification code with anyone 🚫', 'pose': 'point',
         'do': [{'nav': 'risk', 'style': 'fade', 'at': .02}, {'show': 'never', 'at': .3}]},
        {'t': [34.82, 37.70], 'say': 'Secure your WhatsApp today and share this with someone who needs it.',
         'cap': 'Secure your WhatsApp today & share this! 🔐', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

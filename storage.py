"""Tech Wall HOST episode: iPhone storage full? Free up space without deleting photos (result-first).
    ./build.sh storage             -> out/storage.mp4 + out/cover_storage.jpg
    python3 storage.py 0 150 400   -> preview frames in out/frames_storage/
Path checked 2026-10-08 (iOS 17/18 guides, Vodafone device guides, Apple Community): Settings > General > iPhone Storage >
Recommendations > Offload Unused Apps > Enable; per app: iPhone Storage > app > Offload App (keeps documents & data,
icon stays with a cloud badge, tap to reinstall). The toggle also lives at Settings > Apps > App Store (iOS 18).
Bonus: iPhone Storage > Review Large Attachments. Library #105.
"""
import host

EP = 'storage'
WIFI = ''
def bar(used, total, color, segs):
    pct = used / total * 100
    seg = ''.join(f'<div style="width:{w}%;background:{c}"></div>' for w, c in segs)
    return (f'<div style="margin:0 16px 6px;display:flex;justify-content:space-between;font-size:17px">'
            f'<b>iPhone</b><span style="color:#8a8a8e">{used} GB of {total} GB used</span></div>'
            f'<div style="margin:0 16px 8px;height:16px;border-radius:8px;background:#e3e3e8;overflow:hidden;display:flex">{seg}</div>'
            f'<div style="margin:0 16px 18px;display:flex;gap:14px;font-size:13px;color:#6d6d72">'
            f'<span>● Apps</span><span>● Photos</span><span>● Messages</span><span>● System</span></div>')
LEG = lambda a, p, m, s: [(a, '#0a84ff'), (p, '#ffd60a'), (m, '#30d158'), (s, '#8e8e93')]
def rec(id_, label, size, action, fx=''):
    return (f'<div class="row" data-id="{id_}"><div class="flash"></div><span class="lbl">{label}'
            f'<br><span style="font-size:14px;color:#8a8a8e">{size}</span></span>'
            f'<span style="color:#0a7aff;font-weight:600">{action}</span></div>')
def app(id_, name, size, bg, glyph):
    return (f'<div class="row"{f" data-id=\"{id_}\"" if id_ else ""}><div class="flash"></div>'
            f'<div class="sq" style="background:{bg};width:40px;height:40px;border-radius:10px;font-size:20px">{glyph}</div>'
            f'<span class="lbl">{name}</span><span class="val">{size}</span><span class="chev">›</span></div>')
HEAD = '<div class="sb"><span>10:08</span><span class="bat"></span></div><div class="nav">‹ General</div><div class="big" style="font-size:32px">iPhone Storage</div>'
STORAGE_HTML = HEAD + bar(127.4, 128, '#ff3b30', LEG(46, 34, 13, 6)) + '<div class="sect">Recommendations</div><div class="group">' \
    + rec('enable', 'Offload Unused Apps', 'Save 18.4 GB', 'Enable') + rec('attach', 'Review Large Attachments', 'Save 9.2 GB', '›') \
    + '</div><div class="group">' + app('app', 'Games Bundle', '6.1 GB', 'linear-gradient(#bf5af2,#7b2ff7)', '🎮') \
    + app('', 'Video Editor', '4.8 GB', 'linear-gradient(#ff6b81,#ff2d55)', '🎬') + app('', 'Social', '3.9 GB', 'linear-gradient(#5ac8fa,#007aff)', '💬') \
    + app('', 'Maps', '2.2 GB', 'linear-gradient(#76e07a,#2fb344)', '🗺️') + '</div>'
STORAGE2_HTML = STORAGE_HTML.replace('<span style="color:#0a7aff;font-weight:600">Enable</span>', '<span style="color:#30d158;font-weight:700">Enabled ✓</span>')
RESULT_HTML = HEAD + bar(94.1, 128, '#30d158', LEG(22, 34, 10, 6)) + '''
<div style="margin:0 16px 14px;background:linear-gradient(135deg,#30d158,#1f8f4a);border-radius:18px;padding:16px;color:#fff;text-align:center">
  <div style="font-size:44px;line-height:1">📦</div>
  <div style="font-size:30px;font-weight:800;line-height:1.1;margin-top:6px">33 GB freed</div>
  <div style="font-size:18px;font-weight:600;margin-top:4px">0 photos deleted</div>
</div><div class="sect">Recommendations</div><div class="group">''' \
    + rec('', 'Offload Unused Apps', 'Keeps documents & data', '<span style="color:#30d158">Enabled ✓</span>') + '</div>'

SPEC = {
    'lang': 'en', 'voice': 'am_puck', 'speed': 1.08,
    'title': 'iPhone storage full? 📦', 'tag': 'STORAGE · CLEAN-UP', 'tip': 'TIP #02',
    'start': 'result',
    'screens': {
        'result': {'type': 'html', 'html': RESULT_HTML},
        'home': {'type': 'home'},
        'settings': {'type': 'list', 'title': 'Settings', 'search': True, 'groups': [
            {'rows': [{'label': 'Airplane Mode', 'icon': 'airplane', 'color': '#ff9500'},
                      {'label': 'Wi-Fi', 'icon': 'wifi', 'color': '#0a84ff', 'chev': True},
                      {'label': 'Bluetooth', 'icon': 'bluetooth', 'color': '#0a84ff', 'chev': True}]},
            {'rows': [{'label': 'Notifications', 'icon': 'bell', 'color': '#ff3b30', 'chev': True},
                      {'label': 'Sounds & Haptics', 'icon': 'sound', 'color': '#ff2d55', 'chev': True},
                      {'label': 'Focus', 'icon': 'moon', 'color': '#5e5ce6', 'chev': True}]},
            {'rows': [{'id': 'general', 'label': 'General', 'icon': 'general', 'color': '#8e8e93', 'chev': True},
                      {'label': 'Display & Brightness', 'icon': 'display', 'color': '#0a84ff', 'chev': True},
                      {'label': 'Battery', 'icon': 'battery', 'color': '#30d158', 'chev': True},
                      {'label': 'Privacy & Security', 'icon': 'privacy', 'color': '#0a84ff', 'chev': True}]}]},
        'general': {'type': 'list', 'back': 'Settings', 'title': 'General', 'groups': [
            {'rows': [{'label': 'About', 'chev': True}, {'label': 'Software Update', 'chev': True}]},
            {'rows': [{'label': 'AirDrop', 'chev': True}, {'label': 'AirPlay & Continuity', 'chev': True}]},
            {'rows': [{'id': 'storage', 'label': 'iPhone Storage', 'chev': True},
                      {'label': 'Background App Refresh', 'chev': True}]},
            {'rows': [{'label': 'Date & Time', 'chev': True}, {'label': 'Keyboard', 'chev': True}]}]},
        'storage': {'type': 'html', 'html': STORAGE_HTML},
        'storage2': {'type': 'html', 'html': STORAGE2_HTML},
        'appinfo': {'type': 'list', 'back': 'iPhone Storage', 'title': 'Games Bundle', 'groups': [
            {'rows': [{'label': 'App Size', 'value': '6.1 GB'}, {'label': 'Documents & Data', 'value': '212 MB'}]},
            {'rows': [{'id': 'offload', 'label': 'Offload App', 'style': 'blue'}],
             'footer': 'This frees up the storage used by the app, but keeps its documents and data. Reinstalling puts your data back.'},
            {'rows': [{'label': 'Delete App', 'style': 'red'}]}]},
        'attach': {'type': 'list', 'back': 'iPhone Storage', 'title': 'Large Attachments', 'groups': [
            {'header': 'Sorted by size', 'rows': [
                {'label': 'Birthday party.mov', 'value': '2.4 GB'}, {'label': 'Beach day.mov', 'value': '1.8 GB'},
                {'label': 'Concert clip.mov', 'value': '1.1 GB'}, {'label': 'Screen recording.mp4', 'value': '640 MB'}]}]},
    },
    'beats': [
        {'say': 'Storage full? Free up space without deleting a single photo.',
         'cap': 'iPhone storage full? 📦 Free up space without deleting a single photo', 'pose': 'front', 'hook': True},
        {'say': "Here's how. Three steps.", 'cap': "Here's how 👉 3 steps", 'pose': 'talk', 'screen': 'home'},
        {'say': 'Step one. Settings, General, then iPhone Storage.', 'cap': 'Step 1: Settings → General → iPhone Storage',
         'pose': 'point', 'step': 1,
         'do': [{'tap': 'settings', 'at': .22, 'nav': 'settings'}, {'tap': 'general', 'at': .52, 'nav': 'general'},
                {'tap': 'storage', 'at': .82, 'nav': 'storage'}]},
        {'say': 'Step two. Under Recommendations, tap Enable next to Offload Unused Apps.',
         'cap': 'Step 2: Recommendations → Offload Unused Apps → Enable', 'pose': 'point', 'step': 2,
         'do': [{'tap': 'enable', 'at': .72, 'fx': .88}, {'nav': 'storage2', 'at': .86, 'style': 'fade'}]},
        {'say': 'Step three. Tap a big app you rarely use, then tap Offload App.',
         'cap': 'Step 3: Tap a big app → Offload App', 'pose': 'point', 'step': 3,
         'do': [{'tap': 'app', 'at': .45, 'nav': 'appinfo'}, {'tap': 'offload', 'at': .88}]},
        {'say': 'Your data and the icon stay. Tap the icon later, and the app comes right back.',
         'cap': 'Your data & icon stay ☁️ Tap it later and the app comes back', 'pose': 'talk'},
        {'say': 'Done! Gigabytes back, zero photos deleted.', 'cap': 'Done! ✅ Gigabytes back, 0 photos deleted',
         'pose': 'welcome',
         'do': [{'nav': 'result', 'at': 0, 'style': 'zoom'}, {'fx': 'confetti', 'at': .12}, {'fx': 'thumb', 'at': .04, 'dur': 3.2}]},
        {'say': 'Bonus. Review Large Attachments shows the huge videos hiding in your Messages.',
         'cap': 'Bonus: Review Large Attachments 🎥 huge videos hiding in Messages', 'pose': 'point',
         'screen': 'attach', 'style': 'push'},
        {'say': 'Follow Tech Wall for more quick tips!', 'cap': 'Follow Tech Wall for more quick tips! 🚀',
         'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

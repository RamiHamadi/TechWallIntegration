"""Tech Wall HOST episode: your phone scans for Wi-Fi even when Wi-Fi is off (Android, result-first).
    ./build.sh gpsoff             -> out/gpsoff.mp4 + out/cover_gpsoff.jpg
    python3 gpsoff.py 0 150 400   -> preview frames in out/frames_gpsoff/
Path checked 2026-10-08 against Samsung Support "How to fix GPS signal loss or inaccurate location on your Galaxy"
(Settings > Location > Location services > Wi-Fi scanning / Bluetooth scanning: "Let apps use Wi-Fi for more accurate
location detection, even when Wi-Fi is off") and Google's Android help (same path on Pixel, Android 12+).
Bonus: per-app "Use precise location" toggle (Android 12+).
"""
import host

EP = 'gpsoff'
S = 'font-family:Poppins,sans-serif;'
RESULT_HTML = f'''
<div class="sb"><span>10:08</span><span class="bat"></span></div>
<div class="nav">‹ Location</div><div class="big" style="font-size:32px">Location services</div>
<div style="margin:6px 16px 14px;background:linear-gradient(135deg,#1f6feb,#3a2a9c);border-radius:18px;padding:18px 16px;color:#fff;text-align:center">
  <svg viewBox="0 0 100 100" style="width:92px;height:92px;display:block;margin:0 auto 6px">
    <path d="M50 8c-16 0-28 12-28 28 0 22 28 54 28 54s28-32 28-54c0-16-12-28-28-28z" fill="#fff"/>
    <circle cx="50" cy="36" r="11" fill="#3a2a9c"/>
    <path d="M18 84L82 16" stroke="#ff3b30" stroke-width="10" stroke-linecap="round"/>
  </svg>
  <div style="font-size:24px;font-weight:700;line-height:1.15">Nearby Wi-Fi &amp; Bluetooth<br>can't locate you</div>
</div>
<div class="group">
  <div class="row"><div class="sq" style="background:#0a84ff">{{WIFI}}</div><span class="lbl">Wi-Fi scanning</span><span class="tog"><i></i></span></div>
  <div class="row"><div class="sq" style="background:#0a84ff">{{BT}}</div><span class="lbl">Bluetooth scanning</span><span class="tog"><i></i></span></div>
</div>
<div class="foot" style="margin-top:-8px">Scanning is OFF. Apps and services can no longer use nearby networks to find you.</div>
'''
# the row glyphs come from host/screens.js ICONS; inline copies keep this screen self-contained
WIFI_SVG = '<svg viewBox="0 0 20 20"><path d="M3 8a10 10 0 0 1 14 0M6 11a6 6 0 0 1 8 0" stroke="#fff" stroke-width="2" fill="none"/><circle cx="10" cy="14.5" r="1.8" fill="#fff"/></svg>'
BT_SVG = '<svg viewBox="0 0 20 20"><path d="M6 6l8 8-4 3V3l4 3-8 8" stroke="#fff" stroke-width="2" fill="none"/></svg>'
RESULT_HTML = RESULT_HTML.replace('{WIFI}', WIFI_SVG).replace('{BT}', BT_SVG)

def sig(x, y, label, glyph):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:120px;text-align:center">'
            f'<div style="font-size:54px;line-height:1">{glyph}</div>'
            f'<div style="font-size:17px;font-weight:600;margin-top:4px">{label}</div></div>')
SIGNALS_HTML = f'''
<div class="sb" style="color:#fff"><span>10:08</span><span class="bat"></span></div>
<div style="text-align:center;color:#fff;font-size:26px;font-weight:700;padding:6px 20px 0">How your phone finds you</div>
<div style="position:absolute;left:0;top:140px;width:398px;height:640px;color:#fff">
  <svg viewBox="0 0 398 640" style="position:absolute;inset:0;width:398px;height:640px">
    <g stroke="#ffd60a" stroke-width="4" stroke-dasharray="12 10" fill="none" opacity=".9">
      <path d="M199 330 L95 225"/><path d="M199 330 L303 225"/><path d="M199 330 L95 445"/><path d="M199 330 L303 445"/>
    </g>
    <rect x="159" y="270" width="80" height="130" rx="16" fill="#111827" stroke="#fff" stroke-width="4"/>
    <rect x="171" y="286" width="56" height="94" rx="6" fill="#3a2a9c"/>
    <circle cx="199" cy="335" r="12" fill="#ffd60a"/>
  </svg>
  {sig(20, 60, 'GPS', '🛰️')}{sig(258, 60, 'Wi-Fi', '📶')}{sig(20, 440, 'Bluetooth', '📡')}{sig(258, 440, 'Cell towers', '🗼')}
</div>
'''

SPEC = {
    'lang': 'en', 'voice': 'am_puck', 'speed': 1.08,
    'title': 'Tracked with GPS off 📍 Android', 'tag': 'LOCATION · PRIVACY', 'tip': 'TIP #02',
    'start': 'result',
    'screens': {
        'result': {'type': 'html', 'html': RESULT_HTML},
        'signals': {'type': 'html', 'html': SIGNALS_HTML, 'bg': 'linear-gradient(170deg,#1f2a5c,#3a2a9c)'},
        'home': {'type': 'home'},
        'settings': {'type': 'list', 'title': 'Settings', 'search': True, 'groups': [
            {'rows': [{'label': 'Network & internet', 'icon': 'wifi', 'color': '#0a84ff', 'chev': True},
                      {'label': 'Connected devices', 'icon': 'bluetooth', 'color': '#0a84ff', 'chev': True},
                      {'label': 'Apps', 'icon': 'general', 'color': '#8e8e93', 'chev': True}]},
            {'rows': [{'label': 'Notifications', 'icon': 'bell', 'color': '#ff3b30', 'chev': True},
                      {'label': 'Battery', 'icon': 'battery', 'color': '#30d158', 'chev': True},
                      {'label': 'Display', 'icon': 'display', 'color': '#0a84ff', 'chev': True},
                      {'label': 'Sound & vibration', 'icon': 'sound', 'color': '#ff2d55', 'chev': True}]},
            {'rows': [{'label': 'Security & privacy', 'icon': 'privacy', 'color': '#0a84ff', 'chev': True},
                      {'id': 'location', 'label': 'Location', 'icon': 'dot', 'color': '#30d158', 'chev': True},
                      {'label': 'Safety & emergency', 'icon': 'star', 'color': '#ff3b30', 'chev': True}]}]},
        'location': {'type': 'list', 'back': 'Settings', 'title': 'Location', 'groups': [
            {'rows': [{'label': 'Use location', 'icon': 'dot', 'color': '#30d158', 'toggle': True}]},
            {'rows': [{'label': 'App location permissions', 'chev': True, 'value': '12 apps'},
                      {'id': 'services', 'label': 'Location services', 'chev': True}],
             'footer': 'Location may use sources like GPS, Wi-Fi, mobile networks and sensors.'}]},
        'services': {'type': 'list', 'back': 'Location', 'title': 'Location services', 'groups': [
            {'rows': [{'label': 'Earthquake alerts', 'chev': True},
                      {'label': 'Emergency Location Service', 'chev': True},
                      {'label': 'Location accuracy', 'chev': True}]},
            {'rows': [{'id': 'wifi', 'label': 'Wi-Fi scanning', 'icon': 'wifi', 'color': '#0a84ff', 'toggle': True},
                      {'id': 'bt', 'label': 'Bluetooth scanning', 'icon': 'bluetooth', 'color': '#0a84ff', 'toggle': True}],
             'footer': 'Allow apps and services to scan for Wi-Fi networks and nearby devices at any time, even when Wi-Fi or Bluetooth is off.'}]},
        'precise': {'type': 'list', 'back': 'Weather', 'title': 'Location permission', 'groups': [
            {'header': 'Location access for this app', 'rows': [
                {'label': 'Allow all the time'},
                {'label': 'Allow only while using the app', 'value': '✓'},
                {'label': 'Ask every time'},
                {'label': "Don't allow"}]},
            {'rows': [{'id': 'precise', 'label': 'Use precise location', 'icon': 'dot', 'color': '#30d158', 'toggle': True}],
             'footer': 'When off, the app only gets your approximate location.'}]},
    },
    'beats': [
        {'say': "Your phone scans for Wi-Fi even when Wi-Fi is off. That's how apps find you.",
         'cap': 'GPS off ≠ invisible 📍 Your phone scans Wi-Fi even when Wi-Fi is OFF', 'pose': 'front', 'hook': True},
        {'say': 'GPS is just one signal. Wi-Fi, Bluetooth and cell towers can place you too.',
         'cap': '4 ways your phone finds you: GPS · Wi-Fi · Bluetooth · cell towers', 'pose': 'point',
         'screen': 'signals', 'style': 'zoom'},
        {'say': "On Android, here's the switch most people never see.", 'cap': "Here's how 👉 Android",
         'pose': 'talk', 'screen': 'home'},
        {'say': 'Step one. Open Settings, and tap Location.', 'cap': 'Step 1: Settings → Location',
         'pose': 'point', 'step': 1,
         'do': [{'tap': 'settings', 'at': .30, 'nav': 'settings'}, {'tap': 'location', 'at': .78, 'nav': 'location'}]},
        {'say': 'Step two. Tap Location services.', 'cap': 'Step 2: Tap Location services', 'pose': 'point', 'step': 2,
         'do': [{'tap': 'services', 'at': .55, 'nav': 'services'}]},
        {'say': 'Step three. Turn off Wi-Fi scanning, and Bluetooth scanning.',
         'cap': 'Step 3: Turn OFF Wi-Fi scanning & Bluetooth scanning', 'pose': 'point', 'step': 3,
         'do': [{'tap': 'wifi', 'at': .45}, {'tap': 'bt', 'at': .82}]},
        {'say': "Done! Apps can't use nearby networks to find you anymore.",
         'cap': "Done! ✅ Apps can't use nearby networks to find you", 'pose': 'welcome',
         'do': [{'nav': 'result', 'at': 0, 'style': 'zoom'}, {'fx': 'confetti', 'at': .12},
                {'fx': 'thumb', 'at': .04, 'dur': 3.4}]},
        {'say': 'Bonus. Give weather apps approximate location, not precise.',
         'cap': 'Bonus: turn OFF Precise location for weather apps', 'pose': 'point',
         'screen': 'precise', 'style': 'push', 'do': [{'tap': 'precise', 'at': .68}]},
        {'say': "iPhone? Next video. Follow Tech Wall for more quick tips!",
         'cap': 'iPhone? Next video 📱 Follow Tech Wall for more quick tips! 🚀', 'pose': 'point', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

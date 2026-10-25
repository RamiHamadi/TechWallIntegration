"""Tech Wall HOST episode (laptop) with a supplied voice-over: AI app builders (Bolt.new / v0.app) build a web app from a prompt.
    ./build.sh aiapps  |  python3 aiapps.py 0 150 400
Voice: the user's generated audio, pauses between phrases shortened to 0.2 s (host/voices/aiapps.flac).
Facts (2026 pricing guides): bolt.new (StackBlitz) and v0.app (Vercel) turn a text prompt into a running web app
(code + live preview, deploy); both have free plans with daily/monthly limits. Simple apps take about a minute.
Generic builder look-alike (no logos); the habit tracker is an illustrative example, labelled on screen."""
import host

EP = 'aiapps'
YEL, CY, GRN, VIO = '#ffd54a', '#5ce1ff', '#34d399', '#8b7cff'
PROMPT = 'A habit tracker with streaks and a weekly chart'
T_GO = 9.14 + .02 * 6.07 + .22           # build screen appears
T_PREVIEW = 11.95                        # code view -> live preview
T_CHECK = 9.14 + .62 * 6.07              # habit ticked in the running app
SANS = 'font-family:Poppins'
MONO = "font-family:'DejaVu Sans Mono',Consolas,monospace"


def chrome(url):
    return ('<div style="height:40px;background:#e9ecf2;display:flex;align-items:center;gap:10px;padding:0 12px;'
            f'{SANS};font-size:13px;color:#333"><span style="display:flex;gap:6px"><i style="width:11px;height:11px;border-radius:50%;'
            'background:#ff5f57"></i><i style="width:11px;height:11px;border-radius:50%;background:#febc2e"></i><i style="width:11px;'
            'height:11px;border-radius:50%;background:#28c840"></i></span>'
            f'<span style="flex:1;background:#fff;border-radius:14px;padding:4px 14px">🔒 {url}</span></div>')


HABITS = [('h1', '💧 Drink water', True), ('h2', '📚 Read 20 min', False), ('h3', '🏃 Walk 8k steps', True),
          ('h4', '🧘 Meditate', True)]
WEEK = [40, 65, 55, 80, 70, 95, 60]


def app_preview(static):
    """The generated example app (habit tracker) inside the preview pane (640x438)."""
    pop = (lambda i: '') if static else (lambda i: f' data-in="{T_PREVIEW + .08 * i:.2f}"')
    rows = ''
    for k, (hid, label, done) in enumerate(HABITS):
        box = ('<span style="width:22px;height:22px;border-radius:6px;border:2px solid #8b7cff;display:inline-grid;place-items:center;'
               'position:relative">' + ('<b style="color:#8b7cff">✓</b>' if done or static else
                                         f'<b data-in="{T_CHECK + .1:.2f}" style="color:#8b7cff">✓</b>') + '</span>')
        rows += (f'<div{pop(3 + k)} data-id="{hid}" style="display:flex;align-items:center;gap:12px;background:#1d2236;'
                 f'border-radius:12px;padding:10px 14px;margin-bottom:9px;font-size:17px">{box}{label}</div>')
    bars = ''.join(f'<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:4px">'
                   f'<div style="width:70%;height:{h}%;border-radius:6px 6px 2px 2px;background:linear-gradient({VIO},{CY})"></div>'
                   f'<span style="font-size:11px;color:#8a93b0">{d}</span></div>' for h, d in zip(WEEK, 'MTWTFSS'))
    streak = '13' if static else f'12<span data-in="{T_CHECK + .1:.2f}" style="position:absolute;left:0;background:#151a2c">13</span>'
    return (f'<div style="position:absolute;inset:0;background:#0f1322;color:#eef1ff;{SANS};padding:16px 18px;box-sizing:border-box">'
            f'<div{pop(0)} style="display:flex;align-items:center;justify-content:space-between">'
            '<div style="font-size:26px;font-weight:800">Habit Tracker</div>'
            '<div style="position:relative;background:#151a2c;border:1px solid #2b3352;border-radius:14px;padding:4px 12px;font-size:15px;'
            f'font-weight:700">🔥 <span style="position:relative">{streak}</span> day streak</div></div>'
            '<div style="display:flex;gap:16px;margin-top:14px">'
            f'<div style="flex:1.05">{rows}</div>'
            f'<div{pop(2)} style="flex:1;background:#151a2c;border-radius:14px;padding:12px 14px">'
            '<div style="font-size:14px;font-weight:700;margin-bottom:8px">This week</div>'
            f'<div style="display:flex;gap:4px;height:150px">{bars}</div></div></div>'
            '<div style="position:absolute;right:12px;bottom:10px;background:rgba(255,213,74,.15);color:#ffd54a;border-radius:10px;'
            'padding:2px 10px;font-size:12px;font-weight:700">Example app</div></div>')


CODE = [('#c586c0', 'import'), ('#9cdcfe', ' { useState }'), ('#c586c0', ' from'), ('#ce9178', ' "react";'), None,
        ('#c586c0', 'export default function'), ('#dcdcaa', ' HabitTracker'), ('#ccc', '() {'), None,
        ('#ccc', '  const [habits, setHabits] = '), ('#dcdcaa', 'useState'), ('#ccc', '(DEFAULT);'), None,
        ('#ccc', '  const streak = '), ('#dcdcaa', 'calcStreak'), ('#ccc', '(habits);'), None,
        ('#c586c0', '  return'), ('#ccc', ' ('), None,
        ('#808080', '    <'), ('#4ec9b0', 'Header'), ('#9cdcfe', ' title'), ('#ccc', '='), ('#ce9178', '"Habit Tracker"'), ('#808080', ' />'), None,
        ('#808080', '    <'), ('#4ec9b0', 'HabitList'), ('#9cdcfe', ' items'), ('#ccc', '={habits}'), ('#808080', ' />'), None,
        ('#808080', '    <'), ('#4ec9b0', 'WeeklyChart'), ('#9cdcfe', ' data'), ('#ccc', '={week}'), ('#808080', ' />'), None,
        ('#ccc', '  );'), None, ('#ccc', '}'), None]


def code_lines():
    lines, cur = [], ''
    for p in CODE:
        if p is None:
            lines.append(cur); cur = ''
        else:
            cur += f'<span style="color:{p[0]}">{p[1].replace("<", "&lt;").replace(">", "&gt;")}</span>'
    t0, dt = T_GO + .35, (T_PREVIEW - .25 - T_GO - .35) / len(lines)
    return ''.join(f'<div data-in="{t0 + i * dt:.2f}" style="height:25px;white-space:pre;transform-origin:0 50%">'
                   f'<span style="color:#5a6380;display:inline-block;width:32px">{i + 1}</span>{l}</div>' for i, l in enumerate(lines))


STEPS = ['Created package.json', 'Wrote App.tsx', 'Wrote HabitList.tsx', 'Wrote WeeklyChart.tsx', 'npm install', 'Preview ready ✨']


def builder(static):
    """Builder workspace: chat + steps on the left, code / live preview on the right (920x518 laptop screen)."""
    st = ''.join(f'<div{"" if static else f" data-in=\"{T_GO + .4 + i * (T_PREVIEW - T_GO - .3) / len(STEPS):.2f}\""} '
                 f'style="font-size:12.5px;color:#c9cfe6;margin:5px 0;transform-origin:0 50%">'
                 f'<span style="color:{GRN}">✓</span> {s}</div>' for i, s in enumerate(STEPS))
    left = (f'<div style="position:absolute;left:0;top:40px;width:260px;bottom:0;background:#0b0e19;border-right:1px solid #222a40;'
            f'{SANS};color:#fff;padding:14px;box-sizing:border-box">'
            f'<div style="background:{VIO};border-radius:14px 14px 4px 14px;padding:9px 12px;font-size:14px;line-height:1.35">{PROMPT}</div>'
            '<div style="margin-top:14px;font-size:13px;font-weight:700;color:#aab3d6">⚡ Building your app…</div>' + st + '</div>')
    tabs = ('<div style="position:absolute;left:260px;right:0;top:40px;height:36px;background:#0b0e19;display:flex;gap:6px;'
            f'align-items:center;padding:0 12px;{SANS};font-size:13px;color:#aab3d6;border-bottom:1px solid #222a40">'
            + ('<span style="padding:4px 12px">Code</span><span style="padding:4px 12px;background:#222a40;border-radius:8px;color:#fff">'
               'Preview</span>' if static else
               '<span style="position:relative;width:132px;height:26px"><span style="position:absolute;left:0;padding:4px 12px">Code</span>'
               f'<span data-in="-1,{T_PREVIEW:.2f}" style="position:absolute;left:0;padding:4px 12px;background:#222a40;border-radius:8px;'
               'color:#fff">Code</span><span style="position:absolute;left:62px;padding:4px 12px">Preview</span>'
               f'<span data-in="{T_PREVIEW:.2f}" style="position:absolute;left:62px;padding:4px 12px;background:#222a40;border-radius:8px;'
               'color:#fff">Preview</span></span>')
            + '<span style="margin-left:auto;color:#34d399;font-weight:700">● Live</span></div>')
    pane = ('<div style="position:absolute;left:260px;right:0;top:76px;bottom:0;overflow:hidden;background:#0f1322">'
            + (app_preview(True) if static else
               f'<div style="position:absolute;inset:0;padding:14px 16px;font-size:16px;{MONO};color:#ccc">{code_lines()}</div>'
               f'<div data-in="{T_PREVIEW:.2f}" style="position:absolute;inset:0;transform-origin:50% 50%">{app_preview(False)}</div>')
            + '</div>')
    return chrome('bolt.new') + left + tabs + pane


HOME = (chrome('bolt.new')
        + f'<div style="position:absolute;left:0;right:0;top:40px;bottom:0;background:radial-gradient(circle at 50% 0,#2a2f6b,#0b0e19 70%);'
          f'{SANS};color:#fff;text-align:center">'
          '<div style="margin-top:70px;font-size:40px;font-weight:800">What do you want to build?</div>'
          '<div style="font-size:16px;color:#aab3d6;margin-top:6px">Describe your app. AI writes the code and runs it.</div>'
          '<div style="position:relative;margin:30px auto 0;width:640px;height:120px;background:#151a2c;border:2px solid #3b4470;'
          'border-radius:18px;text-align:left;padding:16px 18px;box-sizing:border-box;font-size:20px">'
          '<span style="color:#5a6380" data-in="-1,6.9">Build a…</span><span data-type="home:prompt"></span>'
          f'<div data-id="go" style="position:absolute;right:14px;bottom:12px;width:46px;height:46px;border-radius:14px;background:{VIO};'
          'display:grid;place-items:center;font-size:24px;font-weight:800">↑</div></div>'
          '<div style="display:flex;justify-content:center;gap:10px;margin-top:22px;font-size:14px;color:#c9cfe6">'
          + ''.join(f'<span style="border:1px solid #3b4470;border-radius:16px;padding:5px 14px">{c}</span>'
                    for c in ('🌐 Landing page', '📊 Dashboard', '🧾 Invoice tool', '🎮 Mini game'))
          + '</div></div>')


def card(win, top, html, border=YEL):
    return (f'<div data-in="{win}" style="position:absolute;left:560px;top:{top}px;width:480px;box-sizing:border-box;'
            f'background:rgba(6,20,52,.9);border:3px solid {border};border-radius:26px;padding:14px 22px;color:#fff;'
            f'font-family:Poppins">{html}</div>')


OVERLAY = (card('-1,4.75', 840, f'<div style="font-size:40px;font-weight:900;color:{YEL}">⚡ 1 sentence</div>'
                                '<div style="font-size:30px;font-weight:800">= a working web app</div>')
           + card('5.0,9.1', 840, '<div style="font-size:24px;font-weight:700;color:#aab8d8">Open one of these</div>'
                                  f'<div style="font-size:42px;font-weight:900;color:{YEL}">bolt.new</div>'
                                  f'<div style="font-size:42px;font-weight:900;color:{CY}">v0.app</div>'
                                  '<div style="font-size:20px;color:#aab8d8">Free plans · daily limits</div>', CY)
           + card('12.25,15.3', 840, '<div style="font-size:36px;font-weight:900">🌐 Website</div>', CY)
           + card('13.65,15.3', 935, '<div style="font-size:36px;font-weight:900">📊 Dashboard</div>', CY)
           + card('14.4,15.3', 1030, '<div style="font-size:36px;font-weight:900">🧾 Business tool</div>', CY)
           + card('15.45', 1030, '<div style="font-size:52px;font-weight:900;text-align:center">🔖 SAVE THIS</div>'))

SPEC = {
    'audio': 'host/voices/aiapps.flac', 'lang': 'en', 'device': 'laptop', 'overlay': OVERLAY,
    'title': 'AI builds your web app ⚡', 'tag': 'AI TOOLS · BOLT.NEW · V0.APP', 'tip': 'TIP #11',
    'start': 'res',
    'screens': {
        'res': {'type': 'html', 'bg': '#0b0e19', 'html': builder(True)},
        'home': {'type': 'html', 'bg': '#0b0e19', 'html': HOME},
        'build': {'type': 'html', 'bg': '#0b0e19', 'html': builder(False)},
    },
    'beats': [
        {'t': [0.0, 4.65], 'say': 'This secret AI tool builds full working web apps in sixty seconds!',
         'cap': 'AI BUILDS A WORKING WEB APP IN 60 SECONDS ⚡', 'capsize': 84, 'pose': 'point', 'hook': True},
        {'t': [4.85, 8.94], 'say': 'Just open Bolt.new or v0.app and describe the app you want.',
         'cap': 'Step 1: Open bolt.new or v0.app and describe your app', 'pose': 'point', 'step': 1,
         'do': [{'nav': 'home', 'style': 'fade', 'at': 0}, {'typetext': PROMPT, 'into': 'prompt', 'from': .5, 'to': .93}]},
        {'t': [9.14, 15.21], 'say': 'Watch AI generate the code and turn your idea into an interactive website, dashboard, or business tool!',
         'cap': 'Step 2: AI writes the code and runs your app live ✨', 'pose': 'welcome', 'step': 2,
         'do': [{'tap': 'go', 'at': .02, 'nav': 'build', 'style': 'fade'}, {'tap': 'h2', 'at': .62}]},
        {'t': [15.41, 16.27], 'say': 'Save this video', 'cap': 'Save this video 🔖', 'pose': 'talk'},
        {'t': [16.29, 18.40], 'say': 'and follow Tech Wall for more AI tricks!', 'cap': 'Follow Tech Wall for more AI tricks! 🚀',
         'pose': 'welcome', 'end': True},
    ],
}

if __name__ == '__main__':
    host.run(EP, SPEC)

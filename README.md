# Tech Wall: Video Kit

The engine behind the **Tech Wall** Facebook page's videos: short, vertical, **Blueprint-style stop-motion** tech tips.
Everything needed to rebuild the existing 5 episodes or make new ones that look exactly the same.

---

## 1. Quick start

```bash
pip install -r requirements.txt          # Pillow, numpy, qrcode, imageio-ffmpeg (add --break-system-packages if pip asks)
# uses system ffmpeg if present, else the imageio-ffmpeg binary

python3 sharewifi.py 40 200 345          # preview: renders only those frames -> out/frames_sharewifi/00040.png …
./build.sh sharewifi                     # full render + soundtrack + encode  -> out/sharewifi.mp4  (~1–2 min)
python3 brand.py                         # page cover + profile pictures -> out/brand/
```

| Episode file | Topic | Device | Length |
|---|---|---|---|
| `movie_blue.py` | Back Tap: double-tap the back for a screenshot | iPhone | 47 s |
| `winv.py` | Clipboard history (Win + V) | Windows PC | 46 s |
| `restmode.py` | PS5: charge controllers in Rest Mode (TV + console + generic controller rig, D-pad navigation) | Console | 46 s |
| `animscale.py` | Android animation scale 0.5x (Developer options), result-first | Android | 26 s |
| `lens.py` | AI tip: translate anything with your camera (Google Lens), result-first | Any phone (Android rig) | 21 s |
| `aitrain.py` | AI tip: stop ChatGPT, Claude and Gemini from training on your chats (PC rig, result-first, fast end card) | Laptop | 25 s |
| `wifi.py` | See your saved Wi-Fi password | iPhone | 37 s |
| `android.py` | Notification history | Android | 42 s |
| `sharewifi.py` | Share Wi-Fi with a QR code | Android | 43 s |
| `trackpad.py` | Keyboard trackpad: hold the spacebar to move the cursor | iPhone | 43 s |
| `emoji.py` | Emoji panel (WIN + .): emoji, GIFs, kaomoji, symbols. Needs the system font Noto Color Emoji (`fonts-noto-color-emoji`) | Windows PC | 46 s |
| `movie.py` | Back Tap in the *original* kraft-paper style (not used for posting) | iPhone | 47 s |
| `themes.py` | Style frames for the 3 tech themes (A Circuit, **B Blueprint**, C Neon) | n/a | stills |
| `brand.py` | Facebook cover 1640×624 + profile 720×720 | n/a | stills |
| `reels.py` | Facebook + Instagram Reels via the Meta Graph API, see `REELS.md` | n/a | tool |
| `tiktok.py` | TikTok upload (drafts / direct post) via the Content Posting API, see `TIKTOK.md` | n/a | tool |
| `youtube.py` | YouTube Shorts upload (resumable) via the YouTube Data API v3, see `YOUTUBE.md` | n/a | tool |

---

## 2. Brand & page

- **Page name:** Tech Wall · **Tagline:** *Everything tech, pinned to one wall*
- **Scope:** phones, tablets, PCs, consoles, games, general tech. **Not** only hidden features.
- **Bio (96 chars):** `📌 Everything tech, pinned to one wall. Tips, tricks & how-tos for phones, PCs, consoles & games.`
- **Category:** Digital creator · Handle: @techwall (fallback @techwall.tips)
- **Accounts:** Facebook page Tech Wall · Instagram **@techwalll** · TikTok **@techwallz** · YouTube **Tech Wall (@techwall0)**. Credentials and how to add another page/brand: `SETUP.md`.
- Brand images are in `brand/` (use the **TW monogram** profile; skip the phone-only alt).
- Rotate devices week to week (phone → PC → console → tablet) so the page reads as "all tech".

---

## 3. Visual style spec ("B · Blueprint" stop-motion)

| Element | Spec |
|---|---|
| Canvas | **1080×1920** vertical, rendered at **12 fps** (stop-motion), encoded at 24 fps H.264 |
| Background | Navy blueprint paper `#1A3E80` with grid (minor 30 px, major 150 px), chalk registration marks, a drawing-info box bottom-left; chalk **dimension lines** around the phone when it sits at its home position |
| Chalk / ink | Chalk white `#E2ECFC` · accent yellow `#FFC446` · navy text `#14285C` · mid-blue `#1E4AA0` · paper `#FAFAF6` |
| Cut-paper look | Every prop is a paper cut-out: soft drop shadow, paper texture, **per-frame jitter ±1.5 px** + exposure flicker ±1.6 % (the "boil") |
| Fonts | Titles: **Allerta Stencil** (white + yellow letters, each a separate cut-out, random ±4° tilt). Labels/captions: **JetBrains Mono** 700/800. Phone UI: **Fredoka** |
| Captions | Taped white spec label at top (y≈300): header `FIG. 0n  /  STEP n OF N` (or `FIG. 00 / THE PROBLEM`, `RESULT / OK`, `FIG. 0x / FIELD TEST`, `APPENDIX / BONUS`) + **max 2 lines** of JetBrains Mono 800 54 px (≈25 chars per line). Drops in with an overshoot, flies out upward |
| Hand | Paper hand, navy sleeve with white stripes; hover vs press shadows; dashed **yellow target ring** on every tap |
| Opening (result-first) | No title card: frame 0 already shows the payoff screen/mini-scene with the hook on a taped spec caption (`TECH WALL / <DEVICE> TIP`); frame 0 is also the Reel cover. (Old title card: `SPEC // <device> tip` label → stencil tiles → strips → chalk sketch; episodes 1–10 only.) |
| End card | `SAVE THIS TIP` + 4 numbered path labels joined by dashed chalk arrows (last one yellow) + yellow result strip + white strip + small "works on…" strip |
| Audio | Synthesized: pluck-chord music loop + SFX `tap pop whoosh paper swish knock shutter ding`. All original, safe to post |

**Pacing:** caption on screen ≥ 2.5 s (the kit adds +0.5 s to every caption automatically); result/"ta-da" moments ~2.5–3 s; total 35–50 s.

---

## 4. Architecture

```
lib.py         canvas size, fonts, paper textures, sprite/cut-out helpers, jitter, easing, wrap()
screens.py     iPhone-style screens (SCREENS dict) + view()/row_point()   [iOS look]
props.py       iPhone body (front/back), hand, sticky notes, strips, rings, bursts
movie.py       ENGINE: timeline class TL, phone/hand/caption drawing, SFX + music, make_audio()
themes.py      Blueprint background, cap_blue() caption, stencil_letter(), hand_sprite(), sprite()
movie_blue.py  Blueprint skin over movie.py: init_props(), label()/center_label()/path_label(), render()
               (also patches TL.cap to hold +0.5 s)
android.py     Android phone + Material-style screens (BUILDERS dict), compose_screen override
wifi.py / winv.py / sharewifi.py   episodes (each = screens + timeline + title/end-card props)
mgfx.py        MOTION-GRAPHICS engine (30 fps): eased keyframe tracks (Track/Step), class MG timeline in
               seconds, smooth phone/hand/caption/tap-ring animation, custom draw layers; same Blueprint assets
battery.py     first motion-graphics episode (template for future ones)
camera18.py + camera18/scene.html
               PREMIUM motion graphics: a deterministic render(t) on an HTML canvas (cinematic dark navy,
               Inter + JetBrains Mono, Tech Wall yellow accents, TW chrome + progress bar), captured at
               30 fps with Playwright/Chromium, cinematic synthesized score. Use for product/feature explainers.
```

### Motion-graphics episodes (`mgfx.py`)
Same Blueprint look (navy grid, chalk dims, paper cut-outs, taped captions, paper hand, yellow rings, FOLLOW TECH WALL end strip) but **30 fps with smooth easing, no jitter/flicker**: animated chalk graphics, counters, flowing dashed lines, eased screen pushes. Use it when the tip is better *explained* than *clicked through* (e.g. "why your battery drains").
- Timeline is in **seconds**: `mg.cap(head, text)`, `mg.tap(row_id, nav=spec(...), ov={...}, fx=.62)`, `mg.navigate()`, `mg.phone_to(y=, scale=, dims=)`, `mg.hand_to()/hand_out()`, `mg.wait(s)`, `mg.sound(kind)`; tracks `G.Track(v).to(t0, dur, v, 'io'|'o5'|'back'|…)`.
- Custom screens: register `fn(ov, hl) -> (img 560xH, rows)` in `mgfx.SCREEN_FN` (see `battery.py` `card()` helper for iOS cards with icons, toggles, checks, subtitles).
- Custom graphics: append `fn(cv, t, mg)` to `mg.layers` (under the phone) or `mg.top_layers` (above).
- `G.run(mg, '<id>', cover_t=…)` renders, writes `out/meta_<id>` (FR=30, cover frame) and the soundtrack; `./build.sh <id>` reads that file and encodes at 30 fps.
- **Premium HTML style** (`camera18.py`): edit `camera18/scene.html` (`render(t)`, scene table `S`, sound events `EV`); preview with `python3 camera18.py 0 300 600`. Capture takes ~6–8 min for 37 s; it skips frames already on disk, so if a command times out just run `python3 camera18.py` again, then encode as in `build.sh`.
- Hook rule (tested with `wifi_short.py`, standard for every engine since `rf_demo.py`): the payoff/graphic must be on screen at **frame 0**, no separate title card; aim for 20–35 s.

Each episode file has the same 5 parts: **(1) custom screens**, **(2) `build()` timeline**, **(3) `fig_head()` caption headers**, **(4) `init_props()` title + end-card sprites**, **(5) `draw_title()`**, plus the standard `__main__` (renders with a 2-process pool, then `make_audio`).

### Timeline API (`movie.TL`, 12 fps; every call appends frames)

| Call | Effect |
|---|---|
| `t.hold(n)` | hold n frames (12 = 1 s) |
| `t.phone_to(y, n, keys=-40)` | slide phone to y (`m.PHY`=1205 home; `2700` = off-screen) with overshoot |
| `t.cap(badge, text, color)` | new caption; badge `'1'..'9'`, `'check'`, `'+'`, or custom letters mapped in `fig_head()`; colors `m.YELLOW PINK MINT SKY PEACH` (ignored by Blueprint, which uses white labels) |
| `t.cap_off()` | remove current caption |
| `t.tap(row_id, nav=spec(...), back=False, ov={...}, fx=0.62)` | hand moves to row → press ring + highlight → optional `ov` update (+ding) → optional screen push |
| `t.navigate(spec, back=False)` | screen push/pop transition without a tap |
| `t.swipe(dist, x=300, y=900)` | drag-scroll the current screen |
| `t.move_hand(x, y, n)` / `t.hand_out(n)` / `t.press(x, y, kind)` | manual hand control (canvas coords) |
| `t.s2c(x, y)` | phone-screen coords → canvas coords |
| `t.ph['spec']['ov'] = {...}` then `t.snap()` | change screen state for one frame (e.g. Face ID overlay, banners) |
| `t.ph['x']`, `t.ph['friend']` | move phone sideways; draw a 2nd phone (see `sharewifi.py`) |
| `t.flip('back'/'front')` | 3-D-ish paper flip (iPhone back, `movie_blue.py`) |
| `t.fx.append(('burst', t.f, x, y, idx))` | pop a taped label from `P['bursts'][idx]` |
| `t.fx.append(('title', 0, 50))` / `('end', t.f)` | title card / end card |
| `t.sound(kind, df=0)` | SFX at current frame |

`spec(name, scroll=0, hl=None, ov={})` = which screen is shown. `ov` = per-screen state dict (values, toggles, overlays). Content is cached per `(name, ov, hl)`.

### Screens
- **iPhone**: add to `screens.SCREENS` — blocks `('back',label) ('title',t) ('search',) ('hdr',t) ('card',[rows]) ('foot',text)`; row = `(id, label, icon_color|None, value|'@ovkey'|None, kind, glyph)`, kind ∈ `chev toggle_on toggle_off sel none`. Fully custom iOS screens: monkey-patch `screens.screen_content` (see `wifi.py`).
- **Android**: register `name → fn(ov, hl) -> (image 560×H, rows{id: box})` in `android.BUILDERS`; helpers `list_rows`, `notif_card`, `mswitch`, `arrow_back`, `app_icon`, `bell`, `status_bar`. Home screen supports a heads-up banner via `ov={'banner': x_offset, 'bkey': 'mom'|'guest'|…}` (`android.NOTIFS`).
- **PC**: `winv.py` (monitor + keyboard + mouse cursor, its own `TL`).
- `row_point(spec, id, fx)` returns the tap point; screen size is **560×1184**.

---

## 5. Recipe: new episode

1. **Pick & verify the tip.** Check the exact menu path on the vendor's official support page (Apple / Google / Samsung / Microsoft) plus one recent guide. Note OS version limits and brand differences (put the Samsung path on the end card).
2. **Copy the closest episode:** result-first templates: iPhone → `rf_demo.py` / `wifi_short.py`, motion graphics → `battery.py`. Screens/props: Android → `sharewifi.py` (or `android.py`); PC → `emoji.py`; console → `restmode.py` (give them the result-first opening when copying). Rename (e.g. `circle.py`); the output auto-names to `out/frames_circle`, `out/audio_circle.wav`.
3. **Screens:** build only the screens on the path; row ids for everything the hand taps. Use fictional data (network "Home", password "SunnyDays2024", contacts "Mom"/"Sam", domain example.com).
4. **Timeline (`build()`), result-first (standard since `rf_demo.py`):** the payoff is on screen at **frame 0**: `mb.result_first(t, spec(<result screen>), 'H', '<HOOK>')` (phone already in place, hook caption settled, pop; no title card, no home screen, no "Open Settings" tap) → mini-scene that proves it (≤ 2 s) → `hold(~14–20)` → "Here's how" caption + `t.navigate(spec(<first screen>), back=True)` → one caption per step (`hold(3–5)` before each tap, `n_move=4–5`) → result caption (hold ≥ 18 f) → bonus → `mb.end_card(t)` (phone out + fast end card, everything in within ~1.4 s, `hold(40)`). 12 fps, **20–35 s**. Caption headers come from `fig_head()` (`'H'` → `TECH WALL / iPHONE TIP`, steps → `HERE'S HOW / STEP n OF N`). The `__main__` is just `mb.finish(t, EP, init_props)` (renders, soundtrack, and writes `out/meta_<id>` with `CF=0` so `build.sh` takes frame 0 as the Reel cover). Old opening (title card `fx (title, 0, 86)` + `hold(92)` → phone in → problem caption) is kept in `wifi.py`, `sharewifi.py`, `emoji.py`, `restmode.py` for reference only.
5. **Captions:** test wrapping before rendering:
   `python3 -c "import themes as th; from lib import wrap; print(wrap('Your caption here', th.JB(800,54), 820))"` → must be ≤ 2 lines.
6. **End card** in `init_props()`: `e_head`, `e_chips` (4 path labels, last `hot=True`), `e_arrows`, `e_s1 e_s2 e_s3`, `e_follow`. Keep path labels ≤ ~20 chars. (Title props `tiles t_label t_s1 …` are only needed by the old title-card opening.)
7. **Preview** 8–10 frames (`python3 ep.py 40 90 150 …`), make a contact sheet, check: caption not truncated, hand not covering the key UI (move hand away before overlays), screens correct.
8. **Build:** `./build.sh ep` → `out/ep.mp4` + `out/cover_ep.jpg` (frame 0 = the hook; look at it).

### Content rules
- Facts must match official docs; hooks honest (e.g. animation-speed trick "*feels* faster").
- **No brand logos/trademark artwork** (no Apple/Windows/PlayStation logos; key says "WIN"; generic controller). App screens are generic look-alikes.
- No real personal data; QR codes encode only the fictional network.

---

## 6. Posting

Caption template:
```
<Hook question or claim> 🤯

📌 <Menu › path › exactly › as shown>
(Samsung: <alternate path>)

<1–2 lines: what it does / bonus>
<OS requirement>

<CTA: Save this / Tag someone who… 👇>

#TechWall #<Device>Tips #<Topic> #TechTips
```
Posting is automated after the video is approved: **Facebook + Instagram** Reels via `reels.py` / `REELS.md` (caption and cover set by the API), then **TikTok** via `TIKTOK.md`. Until TikTok audits the app, TikTok gets a **draft without caption**: the user pastes this same caption in the TikTok app, picks the title card as cover and taps Post. Then **YouTube Shorts** via `YOUTUBE.md` Part D: same caption (title = hook + #Shorts, hashtags become tags); until the Google API audit the Short is uploaded **private** and the user switches it to Public in YouTube Studio. Setup of all platforms, tokens and the cloud environment: `SETUP.md` + `TIKTOK.md` (Parts A–C) + `YOUTUBE.md` (Parts A–C).

---

## 7. Episode log & idea backlog

**Done:** Back Tap (iPhone) · Win+V clipboard history (PC) · Saved Wi-Fi password (iPhone) · Notification history (Android) · Share Wi-Fi QR (Android) · Keyboard trackpad (iPhone, `trackpad.py`, Reel posted 2026-10-01) · Emoji panel WIN + . (PC, `emoji.py`, Reel posted 2026-10-01) · PS5 Rest Mode charging (console, `restmode.py`, Reel posted 2026-10-02 on Facebook + Instagram) · Android animation scale 0.5x (Android, `animscale.py`, result-first, posted 2026-10-05 on Facebook + Instagram + YouTube Shorts, TikTok draft) · Battery drain / Background App Refresh (iPhone, `battery.py`, first **motion-graphics** episode, 31.7 s @ 30 fps, built 2026-10-04, awaiting review) · Wi-Fi password short cut (iPhone, `wifi_short.py`, 18 s result-first test) · Result-first opening test (`rf_demo.py`, dummy Back Tap topic, 21 s, approved 2026-10-03: the standard opening for every episode since) · iPhone 18 Pro variable aperture explainer (`camera18.py`, premium HTML-canvas motion graphics, 37 s @ 30 fps, built 2026-10-04, awaiting review)

**Backlog:** the full ordered idea list (100 ideas, with status and publish dates) lives in [`VIDEO_LIBRARY.md`](VIDEO_LIBRARY.md). The table below is the original short list; those ideas are already in the library.

| Device | Idea | Hook |
|---|---|---|
| Android | Developer options → animation scales 0.5x | "Make your Android *feel* 2× faster" |
| Android | Circle to Search (newer Pixel/Samsung) | "Search anything by circling it" |
| iPhone | Hold spacebar → keyboard trackpad | "Stop tapping to fix typos" |
| PS5 | Rest Mode › Supply power to USB ports | "Charge controllers while the PS5 sleeps" |
| PS5 | Create button → Easy Screenshots | "Screenshot your game with one press" |
| Windows | Win + . emoji panel | "Emojis on your PC 😎" |
| iPad | Swipe from bottom-right corner → Quick Note | "Fastest way to take notes" |

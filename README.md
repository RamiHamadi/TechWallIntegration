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
| `wifi.py` | See your saved Wi-Fi password | iPhone | 37 s |
| `android.py` | Notification history | Android | 42 s |
| `sharewifi.py` | Share Wi-Fi with a QR code | Android | 43 s |
| `trackpad.py` | Keyboard trackpad: hold the spacebar to move the cursor | iPhone | 43 s |
| `movie.py` | Back Tap in the *original* kraft-paper style (not used for posting) | iPhone | 47 s |
| `themes.py` | Style frames for the 3 tech themes (A Circuit, **B Blueprint**, C Neon) | n/a | stills |
| `brand.py` | Facebook cover 1640×624 + profile 720×720 | n/a | stills |

---

## 2. Brand & page

- **Page name:** Tech Wall · **Tagline:** *Everything tech, pinned to one wall*
- **Scope:** phones, tablets, PCs, consoles, games, general tech. **Not** only hidden features.
- **Bio (96 chars):** `📌 Everything tech, pinned to one wall. Tips, tricks & how-tos for phones, PCs, consoles & games.`
- **Category:** Digital creator · Handle: @techwall (fallback @techwall.tips)
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
| Title card | `SPEC // <device> tip` label → stencil title tiles → two white strips (the hook) → yellow strip (feature name) → tracing-paper chalk sketch → small taped label (OS version) |
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
```

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
2. **Copy the closest episode:** iPhone → `wifi.py`; Android → `sharewifi.py` (or `android.py`); PC → `winv.py`. Rename (e.g. `circle.py`); the output auto-names to `out/frames_circle`, `out/audio_circle.wav`.
3. **Screens:** build only the screens on the path; row ids for everything the hand taps. Use fictional data (network "Home", password "SunnyDays2024", contacts "Mom"/"Sam", domain example.com).
4. **Timeline (`build()`):** title (`fx (title, 0, 86)` + `hold(92)`: the full title stays readable ~4 s; older episodes used 56 f, which proved too fast) → phone in → *problem* caption + mini-scene → steps (one caption per step, `hold(8–12)` before each tap) → result caption (hold ≥ 24 f) → *field test* demo → bonus → `cap_off()`, phone out, end card `hold(72)`.
5. **Captions:** test wrapping before rendering:
   `python3 -c "import themes as th; from lib import wrap; print(wrap('Your caption here', th.JB(800,54), 820))"` → must be ≤ 2 lines.
6. **Title/end card** in `init_props()`: `P['tiles']` (stencil letters), `t_label t_s1 t_s1b t_s2 t_phone t_burst`, `e_chips` (4 path labels, last `hot=True`), `e_s1 e_s2 e_s3`. Keep path labels ≤ ~20 chars.
7. **Preview** 8–10 frames (`python3 ep.py 40 90 150 …`), make a contact sheet, check: caption not truncated, hand not covering the key UI (move hand away before overlays), screens correct.
8. **Build:** `./build.sh ep` → `out/ep.mp4`.

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
Post as a **Reel** (Meta Business Suite → Create reel), optionally cross-post to Instagram. Metricool can schedule posts if connected.

---

## 7. Episode log & idea backlog

**Done:** Back Tap (iPhone) · Win+V clipboard history (PC) · Saved Wi-Fi password (iPhone) · Notification history (Android) · Share Wi-Fi QR (Android) · Keyboard trackpad (iPhone, `trackpad.py`, Reel posted 2026-10-01)

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

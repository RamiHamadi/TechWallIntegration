# Tech Wall: video engine

This repo builds the videos for **Tech Wall**, a Facebook page ("Everything tech, pinned to one wall") posting short vertical tech tips for phones, tablets, PCs, consoles and games, in a **Blueprint-style stop-motion** look. **Read `README.md` fully before building anything**: style spec, architecture, timeline API, episode recipe, content rules, posting template, idea backlog.

## Setup (once per session)
```bash
pip install -r requirements.txt        # add --break-system-packages if pip refuses
python3 sharewifi.py 40 200 345        # sanity check: preview frames -> out/frames_sharewifi/
```
`build.sh` uses system `ffmpeg`, or falls back to the `imageio-ffmpeg` binary.

## Making a new episode
1. **Idea:** if no topic is given, propose 3–4 ideas (rotate devices) with one-line hooks. When the user says "idea first", present the idea + a storyboard table and wait for approval.
2. **Verify** the exact menu path on the official support page (Apple / Google / Samsung / Microsoft / Sony) plus one recent guide. Note OS-version limits and brand differences (the Samsung path goes on the end card). Hooks must be honest.
3. **Copy the closest episode** as the template: iPhone → `wifi.py`, Android → `sharewifi.py` / `android.py`, PC → `emoji.py` (or `winv.py`). File name = episode id (outputs go to `out/frames_<id>/`, `out/audio_<id>.wav`).
4. **Screens:** only those on the path; row ids for everything tapped; fictional data only (network "Home", password "SunnyDays2024", contacts Mom/Sam, example.com).
5. **Timeline:** title (`fx (title, 0, 86)` + `hold(92)`, so the finished title stays readable ~4 s) → phone in → problem caption + mini scene → one caption per step (hold 8–12 f before each tap) → result caption (hold ≥ 24 f) → field-test demo → bonus → `cap_off()`, phone out, end card `hold(72)`. 12 fps, 35–50 s.
6. **Captions** must wrap to ≤ 2 lines: `python3 -c "import themes as th; from lib import wrap; print(wrap('text', th.JB(800,54), 820))"`.
7. **Preview** 8–10 frames, make a contact sheet and actually look at it: captions not truncated, the hand isn't covering key UI (move it away before overlays), screens correct. Then `./build.sh <id>` and spot-check frames from the MP4 and `out/cover_<id>.jpg`.

## Rules
- The look must stay **identical** to earlier episodes: navy grid + chalk dims, paper cut-outs with jitter, navy-sleeve hand, yellow dashed tap rings, taped spec captions, stencil titles, synthesized music + SFX.
- **Ownership mark (standard since ep. 6):** the Blueprint background carries a chalk `TECH WALL` annotation on the left edge plus `TECH WALL` in the drawing box (`themes.bg_blue`), and the end card ends with a yellow `FOLLOW TECH WALL` strip (`movie_blue.draw_end`, add a pop at `a + 36`). PC episodes: copy `emoji.py` (it reuses the `winv.py` rig and already has the strip, period key, typing hand and taped bursts).
- No brand logos or trademark artwork (the Windows key is labelled WIN, controllers are generic, app screens are generic look-alikes). No real personal data.
- Don't commit rendered output (`out/` is git-ignored). Commit new episode `.py` files.

## Video Library approval loop (`VIDEO_LIBRARY.md`)
Only one row is in progress at a time, so the 30-minute timer only matters *between* ideas. There are **no recurring timers**: the timer is a durable one-shot (`send_later`, server-side, survives session restarts and closed windows).
1. **Timer fires** ("Tech Wall: send the next video idea"): `git pull`. If a row is `⏳ Awaiting idea approval`, `🎬 In production` or `👀 Awaiting video review`, stop (reply one line). Otherwise take the **first** `💡 Idea` row, verify the path (step 2 above), set it to `⏳ Awaiting idea approval`, commit + push, and send the user the idea with a storyboard table.
2. **Idea approved** → `🎬 In production`, build the episode (steps 3–7), send the MP4 and set `👀 Awaiting video review`. **Rejected** → `❌ Rejected` (or `⏭️ Skipped` if postponed), then go to step 4.
3. **Video approved** → post it as a Reel on the Tech Wall page by following **`REELS.md`** (VIDEO = `out/<id>.mp4`, COVER = `out/cover_<id>.jpg`, rebuilt with `./build.sh <id>` if the session restarted; CAPTION = the approved README §6 caption; MODE = PUBLISHED), fill in **Date published**, set `✅ Published`, commit + push. Changes requested → fix, re-send, stay in `👀`.
4. **Row finished** (✅ / ❌ / ⏭️) → schedule the next idea with `send_later` (`delay_minutes: 30`, name "Tech Wall: next video idea", message "Tech Wall: send the next video idea (see CLAUDE.md, Video Library approval loop)"). If the user asks for the next idea sooner, send it now and skip the timer.
Never post without both approvals. Act on the user's replies immediately; don't wait for a timer.
Whenever something needs the user (new idea sent, MP4 ready, post published or failed), also send a one-line `PushNotification`.

## Publishing a Reel
Whenever a video has to be posted to the Tech Wall Facebook page, follow **`REELS.md`** step by step (prepare → start session → upload → publish → confirm → report). Use MODE = DRAFT for any test. Only publish after the user has approved the video.
**Cover:** `build.sh` saves the finished title card as `out/cover_<id>.jpg`; `REELS.md` step 7 uploads it as the Reel cover and checks it. Never skip it: frame 0 of our videos is an empty blueprint, which Facebook would use as a blank thumbnail. Look at the cover JPG when spot-checking the build.

## Deliver
- Send the MP4 with a short scene-by-scene summary.
- Give a ready-to-paste Reel caption (README §6 template), list the sources used, and suggest the next idea.
- Add the episode to the log in README §7.

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
3. **Copy the closest episode** as the template: iPhone → `wifi.py`, Android → `sharewifi.py` / `android.py`, PC → `winv.py`. File name = episode id (outputs go to `out/frames_<id>/`, `out/audio_<id>.wav`).
4. **Screens:** only those on the path; row ids for everything tapped; fictional data only (network "Home", password "SunnyDays2024", contacts Mom/Sam, example.com).
5. **Timeline:** title (56 f) → phone in → problem caption + mini scene → one caption per step (hold 8–12 f before each tap) → result caption (hold ≥ 24 f) → field-test demo → bonus → `cap_off()`, phone out, end card `hold(72)`. 12 fps, 35–50 s.
6. **Captions** must wrap to ≤ 2 lines: `python3 -c "import themes as th; from lib import wrap; print(wrap('text', th.JB(800,54), 820))"`.
7. **Preview** 8–10 frames, make a contact sheet and actually look at it: captions not truncated, the hand isn't covering key UI (move it away before overlays), screens correct. Then `./build.sh <id>` and spot-check frames from the MP4.

## Rules
- The look must stay **identical** to earlier episodes: navy grid + chalk dims, paper cut-outs with jitter, navy-sleeve hand, yellow dashed tap rings, taped spec captions, stencil titles, synthesized music + SFX.
- No brand logos or trademark artwork (the Windows key is labelled WIN, controllers are generic, app screens are generic look-alikes). No real personal data.
- Don't commit rendered output (`out/` is git-ignored). Commit new episode `.py` files.

## Deliver
- Send the MP4 with a short scene-by-scene summary.
- Give a ready-to-paste Reel caption (README §6 template), list the sources used, and suggest the next idea.
- Add the episode to the log in README §7.

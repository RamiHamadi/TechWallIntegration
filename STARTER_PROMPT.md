# Starter prompt (only needed if this repo is NOT connected; otherwise CLAUDE.md is loaded automatically)

I run a Facebook page called **Tech Wall** ("Everything tech, pinned to one wall") that posts short vertical tech-tip videos in a **Blueprint-style stop-motion** look. I've attached `techwall_kit.zip`: the complete engine, fonts and brand assets used for my previous episodes.

Please:
1. Unzip it, install the requirements (`pip install -r requirements.txt`; ffmpeg is needed), and **read README.md fully before doing anything**. It has the style spec, architecture, timeline API, episode recipe and content rules.
2. Sanity-check the setup by rendering a few preview frames of an existing episode (e.g. `python3 sharewifi.py 40 200 345`) and looking at them.
3. Then make a new episode about: **<TOPIC / DEVICE HERE>**
   - First verify the exact steps on the official support page (Apple/Google/Samsung/Microsoft/Sony) and tell me the idea + storyboard before building if anything is uncertain.
   - Copy the closest existing episode as the template (iPhone → `wifi.py`, Android → `sharewifi.py`, PC → `winv.py`) and keep the look **identical**: same captions format, title card, end card, hand, jitter, sounds, 1080×1920 @ 12 fps.
   - Preview frames, check captions fit in 2 lines and the hand doesn't hide key UI, then `./build.sh <episode>` and send me the MP4.
4. Finish with a ready-to-paste Facebook caption (template in README §6) and the sources you used.

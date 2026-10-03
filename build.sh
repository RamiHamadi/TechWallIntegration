#!/usr/bin/env bash
# Usage: ./build.sh <episode>        e.g.  ./build.sh sharewifi
# Renders all frames + soundtrack with <episode>.py, then encodes out/<episode>.mp4
# Preview single frames instead:      python3 <episode>.py 40 120 300   (writes PNGs to out/frames_<episode>/)
set -e
EP="$1"
[ -z "$EP" ] && { echo "usage: ./build.sh <episode>  (movie_blue | winv | wifi | android | sharewifi | movie)"; exit 1; }
cd "$(dirname "$0")"
FF=$(command -v ffmpeg || python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
rm -rf "out/frames_$EP" "out/meta_$EP"
python3 "$EP.py"
# frame rate + cover frame: 12 fps stop-motion by default; episodes may write out/meta_<id> (FR=..., CF=...):
# mgfx.py episodes (FR=30) and result-first episodes (movie_blue.finish -> CF=0, the hook frame is the cover)
FR=12; CF=${COVER_FRAME:-70}
[ -f "out/meta_$EP" ] && . "out/meta_$EP"
OUTFR=$(( FR > 24 ? FR : 24 ))
"$FF" -y -loglevel error -framerate $FR -i "out/frames_$EP/%05d.png" -i "out/audio_$EP.wav" \
  -vf "fps=$OUTFR,format=yuv420p" -c:v libx264 -crf 19 -preset medium -c:a aac -b:a 160k \
  -shortest -movflags +faststart "out/$EP.mp4"
# Reel cover: result-first episodes use frame 0 (the hook); old title-card episodes use the finished title (frame 70)
python3 -c "from PIL import Image; Image.open('out/frames_$EP/%05d.png' % $CF).convert('RGB').save('out/cover_$EP.jpg', quality=92)"
echo "done -> out/$EP.mp4  (cover -> out/cover_$EP.jpg)"

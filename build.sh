#!/usr/bin/env bash
# Usage: ./build.sh <episode>        e.g.  ./build.sh sharewifi
# Renders all frames + soundtrack with <episode>.py, then encodes out/<episode>.mp4
# Preview single frames instead:      python3 <episode>.py 40 120 300   (writes PNGs to out/frames_<episode>/)
set -e
EP="$1"
[ -z "$EP" ] && { echo "usage: ./build.sh <episode>  (movie_blue | winv | wifi | android | sharewifi | movie)"; exit 1; }
cd "$(dirname "$0")"
FF=$(command -v ffmpeg || python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
rm -rf "out/frames_$EP"
python3 "$EP.py"
"$FF" -y -loglevel error -framerate 12 -i "out/frames_$EP/%05d.png" -i "out/audio_$EP.wav" \
  -vf "fps=24,format=yuv420p" -c:v libx264 -crf 19 -preset medium -c:a aac -b:a 160k \
  -shortest -movflags +faststart "out/$EP.mp4"
echo "done -> out/$EP.mp4"

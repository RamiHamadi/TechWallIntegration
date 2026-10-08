#!/usr/bin/env bash
# One-time setup for the Host engine (host.py). Downloads ~450 MB into $TW_HOST_MODELS
# (default ~/.cache/techwall-host), never into the repo. Safe to re-run: skips what exists.
#   English voice : Kokoro-82M (Apache-2.0)            github.com/thewh1teagle/kokoro-onnx
#   Arabic voice  : Piper ar_JO "kareem" via sherpa-onnx github.com/k2-fsa/sherpa-onnx (tts-models)
#   Lip-sync      : Rhubarb Lip Sync 1.14 (MIT)         github.com/DanielSWolf/rhubarb-lip-sync
set -e
cd "$(dirname "$0")/.."
M="${TW_HOST_MODELS:-$HOME/.cache/techwall-host}"; mkdir -p "$M"
pip install -q -r requirements.txt -r host/requirements.txt 2>/dev/null || \
  pip install -q --break-system-packages -r requirements.txt -r host/requirements.txt
get() { [ -s "$M/$2" ] || { echo "downloading $2 ..."; curl -fsSL --retry 3 -o "$M/$2.part" "$1" && mv "$M/$2.part" "$M/$2"; }; }
get https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx kokoro.onnx
get https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin voices.bin
if [ ! -d "$M/vits-piper-ar_JO-kareem-medium" ]; then
  get https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-ar_JO-kareem-medium.tar.bz2 kareem.tar.bz2
  tar xjf "$M/kareem.tar.bz2" -C "$M" && rm "$M/kareem.tar.bz2"
fi
if [ ! -x "$M/rhubarb/rhubarb" ]; then
  get https://github.com/DanielSWolf/rhubarb-lip-sync/releases/download/v1.14.0/Rhubarb-Lip-Sync-1.14.0-Linux.zip rhubarb.zip
  python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$M/rhubarb.zip" "$M"
  rm -rf "$M/rhubarb"; mv "$M/Rhubarb-Lip-Sync-1.14.0-Linux" "$M/rhubarb"; chmod +x "$M/rhubarb/rhubarb"; rm "$M/rhubarb.zip"
fi
python3 -c "import playwright" && (python3 -m playwright install chromium >/dev/null 2>&1 || true)
echo "host engine ready: models in $M"

#!/usr/bin/env bash
# Push the working branch and fast-forward main to it, so main always mirrors the Video Library.
# The user asked for this to happen automatically (no confirmation) after every library update.
set -e
cd "$(dirname "$0")"
B=$(git rev-parse --abbrev-ref HEAD)
[ "$B" = "main" ] && { echo "run this from the working branch, not main"; exit 1; }
git fetch -q origin main
git merge -q --no-edit origin/main      # bring in anything committed to main elsewhere
git push -q origin "$B"
git push -q origin "HEAD:main"
echo "synced $B -> main ($(git rev-parse --short HEAD))"

# Reels on Tech Wall (Facebook + Instagram)

How Tech Wall posts Reels to the Facebook page and the linked Instagram account @techwalll with the **Meta Graph
API**. All calls go through `reels.py` (stdlib Python, runs in the cloud session and on a Windows PC), like
`tiktok.py` and `youtube.py`. The raw `curl` steps are kept at the end as a manual fallback.

| What | Value |
|---|---|
| "App" | a Meta developer app with a **page token** for the Tech Wall page (setup: `SETUP.md`, Facebook + Instagram) |
| Accounts | Facebook page Tech Wall (`FB_PAGE_ID`), Instagram @techwalll (IG user id 17841414742744549, linked to the page) |
| Token in the cloud | **injected by the environment proxy** for `graph.facebook.com` + `rupload.facebook.com`; the session never sees it |
| Token on a PC | `FB_PAGE_TOKEN` environment variable (a page token made from a long-lived user token does not expire) |
| Environment variables | `FB_PAGE_ID`, `FB_API_VERSION` (optional `IG_USER_ID`, otherwise looked up from the page) |
| Network allowlist | `graph.facebook.com`, `rupload.facebook.com` |
| Status | working (script tested 2026-10-03: draft Reel on Facebook + unpublished Instagram container) |

## Rules
- Never request, print or store tokens. Do not modify the repository unless asked.
- Never publish publicly when the task says DRAFT or TEST: use `--draft`.
- Facebook first, then Instagram. If Instagram fails after Facebook succeeded, do **not** repost to Facebook:
  retry Instagram alone (`reels.py instagram ...`), then report.

## Posting an approved video (every episode)

Input: VIDEO = `out/<id>.mp4` (rebuilt with `./build.sh <id>` if the session restarted), CAPTION = the approved
README §6 caption in `/tmp/caption.txt`, COVER = `out/cover_<id>.jpg`, MODE = PUBLISHED (default) or DRAFT.

1. `python3 reels.py check` > expect `facebook page: Tech Wall` and `instagram: @techwalll`.
2. `python3 reels.py post out/<id>.mp4 --caption-file /tmp/caption.txt --cover out/cover_<id>.jpg` (add `--draft`
   for a test). The script runs the steps below in order and stops with a clear message on any error:
   - format check (H.264 + AAC MP4, 9:16, 3-90 s, 24-60 fps); converts to 1080x1920 / 30 fps if needed, never
     cuts a video longer than 90 s;
   - Facebook: start session > upload > finish (PUBLISHED or DRAFT, caption) > wait until ready > upload the
     cover as the preferred thumbnail and verify it (our frame 0 is an empty blueprint, so never skip the cover);
   - Instagram: container (REELS, share to feed, cover at 5833 ms = title card) > upload > wait for FINISHED >
     publish (skipped with `--draft`: Instagram has no drafts, the container expires after 24 h) > permalink.
3. `python3 reels.py status <video_id>` shows the Facebook processing state later if needed.
4. Report: Facebook video id, mode, cover set, link `https://www.facebook.com/reel/<video_id>`; Instagram media id
   and permalink (or why it was not published).

One platform alone: `python3 reels.py facebook ...` or `python3 reels.py instagram ...` (same options).

### Caption (if not given)
- English, 1 strong hook line + 1-3 short lines explaining the value
- At most 3 emojis; 3-5 hashtags at the end, always including #TechWall
- Accurate, no invented facts, no clickbait

### Errors
| Message | Cause | Fix |
|---|---|---|
| `no valid page token ... [code 190]` / `[code 104]` | cloud: proxy injection missing; PC: `FB_PAGE_TOKEN` unset or revoked | `SETUP.md` (Facebook + Instagram): new page token |
| `cannot reach graph.facebook.com` / proxy 403 | network allowlist | add `graph.facebook.com` + `rupload.facebook.com` |
| `... upload failed` after 3 tries | upload interrupted | run the same command again (for Instagram only: `reels.py instagram`) |
| `Instagram container ERROR` | format rejected | check the `video:` line; the script converts anything off-spec |
| `cover not set` | thumbnail endpoint refused | retry step 7 of the manual fallback for that video id; never repost |

---

## Manual fallback (raw Graph API, same steps as reels.py)

### Step 1 - Prepare the video (file input only)
1. If VIDEO is a URL, download it: curl -sL -o /tmp/input.mp4 "<url>"
2. Inspect it: ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of json /tmp/input.mp4
3. Reel requirements: MP4, H.264 video + AAC audio, vertical 9:16 (1080x1920 recommended),
   3-90 seconds, 24-60 fps.
4. If it does not meet them, convert:
   ffmpeg -y -i /tmp/input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 128k -ar 48000 -movflags +faststart /tmp/reel.mp4
   If it has no audio track, add: -f lavfi -i anullsrc=r=48000:cl=stereo -shortest
   If longer than 90s, stop and report instead of cutting.
5. If ffmpeg is missing: apt-get update && apt-get install -y ffmpeg

### Step 2 - Start the upload session
curl -s -X POST "https://graph.facebook.com/$FB_API_VERSION/$FB_PAGE_ID/video_reels" -d "upload_phase=start"
-> Save "video_id" from the response. Stop and report if there is an error.

### Step 3 - Upload the file
SIZE=$(stat -c%s /tmp/reel.mp4)
curl -s -X POST "https://rupload.facebook.com/video-upload/$FB_API_VERSION/$VIDEO_ID" \
  -H "offset: 0" -H "file_size: $SIZE" --data-binary "@/tmp/reel.mp4"
-> Expect {"success":true}. If it fails, retry once, then stop and report.

### Step 4 - Write the caption (if not given)
- English, 1 strong hook line + 1-3 short lines explaining the value
- At most 3 emojis; 3-5 hashtags at the end, always including #TechWall
- Accurate, no invented facts, no clickbait
Save it to /tmp/caption.txt
IG_USER_ID = 17841414742744549 (or: curl -sg "https://graph.facebook.com/$FB_API_VERSION/$FB_PAGE_ID?fields=instagram_business_account")

### Step 5 - Publish (or save as draft)
curl -s -X POST "https://graph.facebook.com/$FB_API_VERSION/$FB_PAGE_ID/video_reels" \
  -d "upload_phase=finish" -d "video_id=$VIDEO_ID" -d "video_state=<PUBLISHED or DRAFT>" \
  --data-urlencode "description@/tmp/caption.txt"
-> Expect {"success":true}.

### Step 6 - Confirm processing
Every 15 seconds, up to 5 minutes:
curl -s "https://graph.facebook.com/$FB_API_VERSION/$VIDEO_ID?fields=status"
- Done when status.video_status is "ready" (or publishing_phase.status is "complete").
- If any phase shows "error", report the full status object.

### Step 7 - Set the cover (always)
Our videos start on an empty frame, so Facebook would show a blank thumbnail. Upload the cover:
curl -s -F "source=@<COVER>" -F "is_preferred=true" "https://graph.facebook.com/$FB_API_VERSION/$VIDEO_ID/thumbnails"
-> Expect {"success":true}. Then check it is the preferred thumbnail:
curl -s "https://graph.facebook.com/$FB_API_VERSION/$VIDEO_ID/thumbnails?fields=is_preferred,width,height"
-> One entry must have "is_preferred":true. If not, retry once, then stop and report.

### Step 8 - Instagram (always, after Facebook)
Instagram has no drafts: in DRAFT or TEST mode do 8.1-8.3 only (the container expires unpublished after 24 h).
8.1 Create the container (thumb_offset = cover time in ms; Tech Wall episodes: 5833 = title card at frame 70):
curl -s -X POST "https://graph.facebook.com/$FB_API_VERSION/$IG_USER_ID/media" -d "media_type=REELS" \
  -d "upload_type=resumable" -d "share_to_feed=true" -d "thumb_offset=5833" --data-urlencode "caption@/tmp/caption.txt"
-> Save "id" as CONTAINER_ID.
8.2 Upload the file:
curl -s -X POST "https://rupload.facebook.com/ig-api-upload/$FB_API_VERSION/$CONTAINER_ID" \
  -H "offset: 0" -H "file_size: $SIZE" --data-binary "@/tmp/reel.mp4"
-> Expect {"success":true}. "upstream request failed" is a proxy glitch: retry (up to 3 times).
8.3 Every 15 seconds, up to 5 minutes:
curl -s "https://graph.facebook.com/$FB_API_VERSION/$CONTAINER_ID?fields=status_code,status"
-> Wait for status_code FINISHED. On ERROR or EXPIRED, report the full status.
8.4 Publish (PUBLISHED mode only):
curl -s -X POST "https://graph.facebook.com/$FB_API_VERSION/$IG_USER_ID/media_publish" -d "creation_id=$CONTAINER_ID"
-> Save "id" as IG_MEDIA_ID, then get the link:
curl -s "https://graph.facebook.com/$FB_API_VERSION/$IG_MEDIA_ID?fields=permalink"
If Instagram fails after Facebook succeeded, do not repost to Facebook: retry Instagram alone, then report.

### Step 9 - Report
- Facebook: video_id, final status, mode (PUBLISHED/DRAFT), cover set (yes/no), the caption, and
  the link https://www.facebook.com/reel/<video_id>
- Instagram: IG_MEDIA_ID and the permalink (or why it was not published)

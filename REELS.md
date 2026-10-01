# Upload a video as a Facebook Reel to Tech Wall

## Rules
- FB_PAGE_ID and FB_API_VERSION are set. Auth is added automatically by the proxy for
  graph.facebook.com and rupload.facebook.com. Never request, print, or store tokens.
- Do not modify the repository unless asked.
- Never publish publicly when the task says DRAFT or TEST.

## Input
- VIDEO: a file path (e.g. videos/wifi-qr.mp4) OR a public https URL.
- CAPTION: given in the task, or write one (see step 4).
- MODE: PUBLISHED (default) or DRAFT.

## Step 1 - Prepare the video (file input only)
1. If VIDEO is a URL, download it: curl -sL -o /tmp/input.mp4 "<url>"
2. Inspect it: ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of json /tmp/input.mp4
3. Reel requirements: MP4, H.264 video + AAC audio, vertical 9:16 (1080x1920 recommended),
   3-90 seconds, 24-60 fps.
4. If it does not meet them, convert:
   ffmpeg -y -i /tmp/input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 128k -ar 48000 -movflags +faststart /tmp/reel.mp4
   If it has no audio track, add: -f lavfi -i anullsrc=r=48000:cl=stereo -shortest
   If longer than 90s, stop and report instead of cutting.
5. If ffmpeg is missing: apt-get update && apt-get install -y ffmpeg

## Step 2 - Start the upload session
curl -s -X POST "https://graph.facebook.com/$FB_API_VERSION/$FB_PAGE_ID/video_reels" -d "upload_phase=start"
-> Save "video_id" from the response. Stop and report if there is an error.

## Step 3 - Upload the file
SIZE=$(stat -c%s /tmp/reel.mp4)
curl -s -X POST "https://rupload.facebook.com/video-upload/$FB_API_VERSION/$VIDEO_ID" \
  -H "offset: 0" -H "file_size: $SIZE" --data-binary "@/tmp/reel.mp4"
-> Expect {"success":true}. If it fails, retry once, then stop and report.

## Step 4 - Write the caption (if not given)
- English, 1 strong hook line + 1-3 short lines explaining the value
- At most 3 emojis; 3-5 hashtags at the end, always including #TechWall
- Accurate, no invented facts, no clickbait
Save it to /tmp/caption.txt

## Step 5 - Publish (or save as draft)
curl -s -X POST "https://graph.facebook.com/$FB_API_VERSION/$FB_PAGE_ID/video_reels" \
  -d "upload_phase=finish" -d "video_id=$VIDEO_ID" -d "video_state=<PUBLISHED or DRAFT>" \
  --data-urlencode "description@/tmp/caption.txt"
-> Expect {"success":true}.

## Step 6 - Confirm processing
Every 15 seconds, up to 5 minutes:
curl -s "https://graph.facebook.com/$FB_API_VERSION/$VIDEO_ID?fields=status"
- Done when status.video_status is "ready" (or publishing_phase.status is "complete").
- If any phase shows "error", report the full status object.

## Step 7 - Report
- video_id, final status, mode (PUBLISHED/DRAFT), the caption, and
  the link https://www.facebook.com/reel/<video_id>

# Post a video to TikTok (@techwallz)

Run this **after** `REELS.md` (Facebook + Instagram), for the same approved video. Everything goes through `tiktok.py`.

## Rules
- Credentials live in the environment, never in the repo or the chat: `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`,
  `TIKTOK_REFRESH_TOKEN`. The network must allow `*.tiktokapis.com` (uploads go to a regional host such as
  `open-upload-sg.tiktokapis.com`). Never print or store tokens; `.tiktok_tokens.json` is a git-ignored cache.
- The app is **unaudited** (Sandbox, target user techwallz): direct posts are refused for public accounts
  (`unaudited_client_can_only_post_to_private_accounts`). Until TikTok approves the app, use **DRAFT**.
- Never post without both approvals (idea + video).

## Input
- VIDEO: `out/<id>.mp4` (rebuild with `./build.sh <id>` if the session restarted). 3 s to 10 min, MP4 H.264.
- CAPTION: the approved README §6 caption, saved to `/tmp/caption.txt`.
- MODE: DRAFT (default, until the audit) or PUBLISHED.

## Step 1 - Check the connection
python3 tiktok.py check
-> Expect `account: Tech Wall (@techwallz)`. On `token request failed`: the refresh token expired or was
   revoked. Ask the user to redo the login (Step 4) and update `TIKTOK_REFRESH_TOKEN`; stop here.
   On `cannot reach`: the network does not allow `*.tiktokapis.com`; tell the user and stop.

## Step 2a - DRAFT (current default)
python3 tiktok.py draft out/<id>.mp4
-> Expect `SEND_TO_USER_INBOX`. Tell the user: open TikTok on @techwallz, tap the "ready to edit" notification
   (or Profile > Drafts/Inbox), paste the caption from /tmp/caption.txt, set the cover to the title card, and post.

## Step 2b - PUBLISHED (only after TikTok has audited the app)
python3 tiktok.py post out/<id>.mp4 --caption-file /tmp/caption.txt --privacy PUBLIC_TO_EVERYONE --cover-ms 5833
-> `--cover-ms 5833` is the finished title card (frame 70), same as Instagram's thumb_offset.
-> Expect `PUBLISH_COMPLETE` and a link. If it times out, run `python3 tiktok.py status <publish_id>`.

## Step 3 - Report
- MODE, publish_id, final status, and the link (PUBLISHED) or "draft waiting in the TikTok app" (DRAFT).
- If TikTok fails after Facebook/Instagram succeeded, do not repost those: retry TikTok alone, then report.

## Step 4 - New login (about once a year, or when the refresh token stops working)
Done by the user on their own PC (Python 3 + this repo; in Command Prompt first run
`set TIKTOK_CLIENT_KEY=...` and `set TIKTOK_CLIENT_SECRET=...`):
1. `python tiktok.py login-url` -> open the link in an incognito window, log in as Tech Wall, press Continue.
2. Copy the GitHub address you land on, then: `python tiktok.py exchange "<that address>" --show`
3. Put the printed `TIKTOK_REFRESH_TOKEN` value into the cloud environment settings (not the chat).
The redirect URI registered in the app's Login Kit must equal `https://github.com/ramihamadi/techwallintegration`
(or set `TIKTOK_REDIRECT_URI`).

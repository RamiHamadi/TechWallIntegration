# TikTok (@techwallz): setup, tokens and posting

Everything we learned connecting Tech Wall to the TikTok **Content Posting API**. Parts A-C are one-time setup
(done by the user, verified 2026-10-03); Part D is what an agent runs for every approved video.
All API calls go through `tiktok.py` (stdlib Python, runs in the cloud session and on a Windows PC).

| What | Value |
|---|---|
| Developer app | **TeckWallApp** (developers.tiktok.com), using its **Sandbox** "Tech Wall" (app name TeckWallAppSandbox) |
| Client key (sandbox) | starts with `sb...`; production keys start with `aw...` and do nothing until TikTok approves the app |
| TikTok account | **Tech Wall (@techwallz)**, the sandbox target user |
| Redirect URI (Web) | `https://github.com/ramihamadi/techwallintegration` (any https page works; we only read `?code=` from the address bar) |
| Scopes | `user.info.basic`, `video.upload` (drafts), `video.publish` (direct post) |
| Environment variables | `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN` (optional `TIKTOK_REDIRECT_URI`) |
| Network allowlist | `*.tiktokapis.com` (or `open.tiktokapis.com` + `open-upload-sg.tiktokapis.com`) |
| Token lifetimes | access token 24 h (refreshed automatically), refresh token 365 days |

---

## Part A - Developer portal setup (one time)

1. developers.tiktok.com > **Manage apps** > create the app (icon 1024x1024, name, category, description).
2. Switch the toggle at the top from **Production** to **Sandbox** and create a sandbox. Work only in the sandbox
   until the app is audited; it has its **own client key and secret** (Sandbox > App details > Credentials).
3. **Basic information > Platforms:** tick **Web** ("Configure for Web"). Without it the Login Kit shows
   "Turn on Configure for Web" and you cannot enter a redirect URI. If a website URL is asked, use the redirect URI.
4. **Products > Add products:** add **Login Kit** and **Content Posting API**.
   - Login Kit > Redirect URI > **Web**: enter the redirect URI exactly (https, no `?`/`#`, mind upper/lower case
     and trailing `/`; the authorize link must match it character for character).
   - Content Posting API: turn **Direct Post** on (needed for `video.publish`). **Verify domains** is only for
     `PULL_FROM_URL`; we upload the file (`FILE_UPLOAD`), so skip it.
5. **Scopes > Add scopes:** `user.info.basic`, `video.upload`, `video.publish`.
6. **Sandbox settings > Target users > Add account:** log in as the TikTok account that will post (techwallz)
   and accept. Only target users can authorise a sandbox app.
7. Click the red **Apply changes** (top right). Nothing above takes effect until you do
   ("This form has unsaved changes").

## Part B - Getting the tokens (one time, then about once a year)

The client key + secret only identify the app; **posting needs a user token** from the account owner's login.

1. **Check the key/secret** (no login needed; a `clt.` token back means they are valid):
   `curl -X POST https://open.tiktokapis.com/v2/oauth/token/ -H "Content-Type: application/x-www-form-urlencoded" -d "client_key=KEY&client_secret=SECRET&grant_type=client_credentials"`
2. **Login link** (`python3 tiktok.py login-url` prints it), open it in an **incognito window** so the
   browser's existing TikTok session does not log in the wrong account:
   `https://www.tiktok.com/v2/auth/authorize/?client_key=KEY&scope=user.info.basic,video.upload,video.publish&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2Framihamadi%2Ftechwallintegration&state=techwall`
   Log in as Tech Wall, check the three permissions are on, press **Continue**.
3. The browser lands on `https://github.com/ramihamadi/techwallintegration?code=...&scopes=...&state=techwall`.
   The `code` is **single use and expires within minutes**. It is URL-encoded: `%2A` = `*`, `%21` = `!`
   (`tiktok.py exchange` decodes it for you).
4. **Exchange it right away:** `python tiktok.py exchange "<that address>" --show` (on the user's PC, with
   `set TIKTOK_CLIENT_KEY=...` and `set TIKTOK_CLIENT_SECRET=...` first), or by hand:
   `curl -X POST https://open.tiktokapis.com/v2/oauth/token/ -H "Content-Type: application/x-www-form-urlencoded" -d "client_key=KEY&client_secret=SECRET&grant_type=authorization_code&redirect_uri=https://github.com/ramihamadi/techwallintegration&code=DECODED_CODE"`
   Success = `access_token` (`act.`), `refresh_token` (`rft.`) and `"scope":"user.info.basic,video.publish,video.upload"`.
5. Put the `rft.` value in the environment as `TIKTOK_REFRESH_TOKEN`. Never in the repo or the chat.

Windows notes: use **Command Prompt** (Win+R > `cmd`); in old PowerShell `curl` is not real curl. In cmd, JSON
bodies need escaped quotes: `-d "{\"publish_id\":\"...\"}"`. Paste with right-click.

## Part C - Cloud environment (one time)

In the session title bar > environment > **Edit**:
1. **Environment variables:** `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN`.
2. **Network access > Custom:** keep the defaults and add `*.tiktokapis.com`. Each host is allowed separately:
   Facebook works because `graph.facebook.com` / `rupload.facebook.com` are allowed; TikTok hosts are not by default
   (`curl: (56) CONNECT tunnel failed, response 403`). Uploads go to a regional host (ours: `open-upload-sg`).
3. Settings only reach **new sessions**. Verify there with `python3 tiktok.py check`.

---

## Part D - Posting an approved video (every episode)

Run this **after** `REELS.md` (Facebook + Instagram), for the same approved video. Never post without both approvals.

Input: VIDEO = `out/<id>.mp4` (rebuild with `./build.sh <id>` if the session restarted; 3 s to 10 min, MP4 H.264),
CAPTION = the approved README §6 caption in `/tmp/caption.txt`, MODE = DRAFT (default until the audit) or PUBLISHED.

### Step 1 - Check the connection
`python3 tiktok.py check` -> expect `account: Tech Wall (@techwallz)`.
On `token request failed` the refresh token expired or was revoked: ask the user to redo Part B and stop.
On `cannot reach` the network does not allow `*.tiktokapis.com`: tell the user (Part C) and stop.

### Step 2a - DRAFT (current default)
`python3 tiktok.py draft out/<id>.mp4` -> expect `SEND_TO_USER_INBOX`.
**Drafts carry no caption, hashtags or cover** (the inbox endpoint only accepts the video). So also send the user
the caption, ready to copy, and tell them: open TikTok on @techwallz, tap the "ready to edit" notification
(or the inbox), paste the caption, choose the first frame (the hook) as cover, tap Post.

### Step 2b - PUBLISHED (only after TikTok has audited the app)
`python3 tiktok.py post out/<id>.mp4 --caption-file /tmp/caption.txt --privacy PUBLIC_TO_EVERYONE --cover-ms 5833`
-> caption and cover are set automatically (`5833` ms = the finished title card, same as Instagram's thumb_offset).
-> expect `PUBLISH_COMPLETE` and a link. If it times out: `python3 tiktok.py status <publish_id>`.

### Step 3 - Report
MODE, publish_id, final status, and the link (PUBLISHED) or "draft waiting in the TikTok app" + the caption (DRAFT).
If TikTok fails after Facebook/Instagram succeeded, do not repost those: retry TikTok alone, then report.

---

## Errors we hit and what they mean

| Where | Message | Fix |
|---|---|---|
| Login page | "Something went wrong ... `redirect_uri`" | The link's redirect URI differs from the one saved (case, trailing `/`), none is saved, Web is not enabled, or **Apply changes** was not clicked. Also happens with the production `aw...` key on an unapproved app: use the sandbox key. |
| Login page | `non_sandbox_target` | The account logging in is not a sandbox target user. Add it (Part A.6), Apply changes, retry in incognito. |
| Token | `invalid_client` "Client key or secret is incorrect" | Wrong secret (copy it from the portal, do not retype from a screenshot) or a sandbox key mixed with a production secret. |
| Token | `invalid_grant` | The code expired or was already used: log in again and exchange within a minute. |
| Direct post | `unaudited_client_can_only_post_to_private_accounts` | Expected until the audit. Use DRAFT, or (test only) make the account private temporarily. |
| Upload | `null` response to the PUT | Normal; then check status. |
| Status | `SEND_TO_USER_INBOX` / `PUBLISH_COMPLETE` / `PROCESSING_UPLOAD` / `FAILED` | Draft delivered / posted / wait and re-check / read `fail_reason`. |
| Cloud | `cannot reach open.tiktokapis.com` / proxy 403 | Network allowlist missing (Part C). |

## Rules and limits
- `creator_info` lists `PUBLIC_TO_EVERYONE`, but an **unaudited** app may only direct-post to **private** accounts.
  Public automatic posting needs the TikTok **audit**: switch to Production, fill in the app details, and submit for
  review (they check the posting UX against the Content Sharing Guidelines). Until then: drafts.
- Chunking: videos up to 64 MB go in one chunk (files under 5 MB must); bigger ones in 10 MB chunks, the last
  chunk takes the remainder. The upload URL is valid for about an hour.
- `.tiktok_tokens.json` is a git-ignored token cache. Never print, commit or paste tokens or the secret
  (the repo is **public**). If they leak: remove the app in TikTok (Settings and privacy > Security and permissions >
  Apps and services permissions), then redo Part B. We found no reset button for the sandbox secret; deleting and
  recreating the sandbox gives a new key + secret (then redo Part A).
- **Another TikTok account / brand:** same app; add the account as a target user, do Part B logged in as that
  account, and give its refresh token to that brand's environment (see `SETUP.md`).

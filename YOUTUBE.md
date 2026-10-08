# YouTube (Tech Wall Shorts): setup, tokens and posting

How Tech Wall uploads to YouTube with the **YouTube Data API v3**. Parts A-C are one-time setup (done by the
user); Part D is what an agent runs for every approved video. All API calls go through `youtube.py`
(stdlib Python, runs in the cloud session and on a Windows PC).

| What | Value |
|---|---|
| "App" | a **Google Cloud project** (`TechWall`) with the YouTube Data API v3 enabled and an OAuth client of type **Desktop app** |
| Redirect URI | `http://localhost` (allowed automatically for Desktop clients; the page does not load, we only read `?code=` from the address bar) |
| Scopes | `youtube.upload` (upload + thumbnail), `youtube.readonly` (`check`, `status`) |
| Environment variables | `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (optional `YT_REDIRECT_URI`) |
| Network allowlist | `oauth2.googleapis.com`, `www.googleapis.com` (already reachable in the Tech Wall environment) |
| Token lifetimes | access token 1 h (refreshed automatically); refresh token does not expire **once the app is published** (7 days while "Testing") |
| Channel | Tech Wall **@techwall0** (`UCjPfPTK-N34rH_8mdNvHYzA`) |
| Status | working, part of the approval loop (private test upload 2026-10-03); uploads stay private until the API audit |

---

## Part A - Google Cloud project (one time)

1. console.cloud.google.com, logged in as the Google account that owns or manages the Tech Wall channel.
   Project picker > **New project** > `TechWall` > Create.
2. **APIs & Services > Library** > "YouTube Data API v3" > **Enable**.
3. **Google Auth Platform** (OAuth consent screen):
   - Branding: app name `Tech Wall`, support + developer email.
   - Audience: **External**; add your Google account under **Test users**.
   - Data access > Add scopes: `.../auth/youtube.upload`, `.../auth/youtube.readonly`.
   - When it works: Audience > **Publish app** ("In production"). In "Testing" the refresh token dies after
     **7 days**. Verification is not needed for our own channel; the login just shows "Google hasn't verified
     this app" > **Advanced** > **Go to Tech Wall (unsafe)**.
4. **Clients > Create client** > type **Desktop app**, name `techwall-cli` > copy the **Client ID** and
   **Client secret** (never into the repo or the chat).

## Part B - Getting the refresh token (one time)

1. Put `YT_CLIENT_ID` / `YT_CLIENT_SECRET` in the environment (Part C) or, on a PC, `set YT_CLIENT_ID=...` and
   `set YT_CLIENT_SECRET=...` in cmd.
2. `python3 youtube.py login-url` > open the link in an **incognito window**, log in, **pick the Tech Wall
   channel** (brand channels are listed separately), allow both permissions.
3. The browser lands on `http://localhost/?state=techwall&code=4/0A...&scope=...` and shows "can't connect":
   that is expected. The code is single use and expires within minutes.
4. Right away: `python youtube.py exchange "<that address>" --show` (on the PC) > `YT_REFRESH_TOKEN=1//...`.
   Put it in the environment. If no refresh token comes back, revoke the app at myaccount.google.com >
   Security > Third-party access and log in again with the `login-url` link.

## Part C - Cloud environment (one time)

Session title bar > environment > **Edit**:
1. **Environment variables:** `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.
2. **Network:** `oauth2.googleapis.com` + `www.googleapis.com` must be reachable (they are today; add them to
   the Custom allowlist if a proxy 403 shows up).
3. New sessions only. Verify with `python3 youtube.py check` > `channel: Tech Wall (...)`.

---

## Part D - Posting an approved video (every episode)

Step 3 of the Video Library approval loop (`CLAUDE.md`): run after `REELS.md` and `TIKTOK.md`, for the same approved video. Never post without both approvals.

Input: VIDEO = `out/<id>.mp4` (vertical, under 3 min = a Short), CAPTION = the approved README §6 caption in
`/tmp/caption.txt`, COVER = `out/cover_<id>.jpg`.

1. `python3 youtube.py check` > expect the Tech Wall channel. `invalid_grant` = refresh token expired or
   revoked (redo Part B; publish the app if it is still "Testing"). `cannot reach` = network (Part C).
2. `python3 youtube.py upload out/<id>.mp4 --caption-file /tmp/caption.txt --privacy public --thumbnail out/cover_<id>.jpg`
   - Title = first caption line (the hook) + `#Shorts`, max 100 characters; override with `--title "..."`.
     Description = the caption; tags = its hashtags; category Science & Technology; not made for kids.
   - Until the API audit passes, YouTube forces **private**: the script prints a note. Tell the user to open
     YouTube Studio > Content > the Short > Visibility > **Public**.
   - `thumbnail: not set` is not fatal (see limits); the user picks the title-card frame in the YouTube app.
3. `python3 youtube.py status <video_id>` if processing is not finished.
4. Report: video id, privacy, link `https://youtube.com/shorts/<id>`, and whether the user must switch it to
   Public. If YouTube fails after the other platforms succeeded, retry YouTube alone, **but never blindly**:
   an upload error (e.g. `410 Gone`) can arrive after YouTube already stored the file, so a video may exist.
   `youtube.py` now looks for a video with the same title from the last 20 minutes, names it and refuses to upload
   a duplicate (2026-10-08: a blind retry left an empty 0-second "video" next to the real Short). If it names
   one: `youtube.py status <id>`; a `processed` 33 s video is the Short, done; an `uploaded` 0 s one is broken:
   the user deletes it in YouTube Studio, then re-run with `--force`.

## Rules and limits
- **Private lock:** videos uploaded by an unverified API project created after 28 July 2020 are private until
  the project passes the **YouTube API Services audit** (Google's "Audit and Quota Extension" form). After
  approval `--privacy public` works directly.
- **Quota:** uploads use their own daily bucket (about 100 a day per project since June 2026); other calls use
  the 10,000 units/day pool. Far beyond our needs.
- **Thumbnails:** need a phone-verified channel (youtube.com/verify; otherwise `403 ... permissions to upload and set custom video thumbnails`); custom Shorts thumbnails are rolling out to Partner Program
  channels first.
- Titles and descriptions may not contain `<` or `>` (the script strips them).
- `.youtube_tokens.json` is a git-ignored token cache. Never print, commit or paste the secret or tokens (the
  repo is **public**). If they leak: delete the OAuth client in the Cloud console, create a new one, redo Part B.

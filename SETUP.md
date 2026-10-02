# Setup: platforms, credentials and the cloud environment

How Tech Wall is wired to Facebook, Instagram and TikTok, and how to repeat it for a new page or brand.
Posting procedures: `REELS.md` (Facebook + Instagram) and `TIKTOK.md` (TikTok, including its full setup).

## Accounts

| Platform | Account | How the session posts |
|---|---|---|
| Facebook | Tech Wall page (`FB_PAGE_ID`) | Graph API; the page token is **injected by the environment proxy** for `graph.facebook.com` and `rupload.facebook.com` |
| Instagram | @techwalll (IG user id 17841414742744549, linked to the page) | same Graph API token |
| TikTok | Tech Wall (@techwallz) | `tiktok.py` with `TIKTOK_*` environment variables (drafts until the app is audited) |

## Cloud environment (session title bar > environment > Edit)

- **API credentials / proxy injection:** the Facebook/Instagram page token. The session never sees it.
- **Environment variables:** `FB_PAGE_ID`, `FB_API_VERSION`, `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN`.
- **Network access (Custom):** default package managers + `graph.facebook.com`, `rupload.facebook.com`,
  `*.tiktokapis.com`. Each host must be allowed on its own; a missing one shows as a proxy 403
  (`CONNECT tunnel failed`).
- Changes apply to **new sessions** only.

## Security rules
- The GitHub repo is **public**: never commit secrets, tokens or keys (bots scrape new ones within minutes and
  git history keeps them). Scripts read credentials from the environment; caches such as `.tiktok_tokens.json`
  are git-ignored.
- Never paste secrets or tokens into the chat. The one exception is a TikTok login `code`, which is single use,
  expires in minutes and is useless without the secret.

## Adding a new page / brand

You do **not** need a new developer app on Meta or TikTok. One app can serve several of your own pages and
accounts; what is per page is the **token**. Create a new app only if the page belongs to someone else (Meta
then requires App Review / Advanced Access) or you want the brands fully isolated.

**Facebook + Instagram**
1. Create the Facebook page. Switch the new Instagram account to **Business** or **Creator** and link it to the
   page (Meta Business Suite or Accounts Center).
2. Graph API Explorer, with the existing app: **Generate token** and tick the **new page** in the page picker.
   Permissions: `pages_show_list`, `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`,
   `instagram_content_publish`, `business_management`. While the app is in Development mode this works for pages
   where you are an admin.
3. Exchange it for a long-lived user token, then `GET /me/accounts` -> the new page's id and page token
   (a page token from a long-lived user token does not expire). `GET /<page id>?fields=instagram_business_account`
   -> the Instagram user id.

**TikTok**
4. Same TikTok app: add the new account under Sandbox > Target users, Apply changes, then do `TIKTOK.md` Part B
   logged in as that account to get its refresh token.

**Environment + repo**
5. The proxy injects one Facebook token per environment, so create a **second cloud environment** for the new
   brand: inject the new page token for `graph.facebook.com` + `rupload.facebook.com`, set its `FB_PAGE_ID`,
   `FB_API_VERSION` and `TIKTOK_*` values, and the same network allowlist.
6. Give it its own repo (or a copy of this one) with its own `CLAUDE.md`, `VIDEO_LIBRARY.md`, IG user id in
   `REELS.md`, account names in `TIKTOK.md`, and the redirect URI if it differs.

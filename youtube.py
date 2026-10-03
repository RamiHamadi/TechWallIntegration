"""Tech Wall: upload videos to YouTube (Shorts) through the YouTube Data API v3.

Credentials come from environment variables, never from this repo:
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
  YT_REDIRECT_URI (optional, default http://localhost; must be allowed by the OAuth client, Desktop clients allow it)

  python3 youtube.py check                     refresh the token, show the channel the uploads will go to
  python3 youtube.py upload out/<id>.mp4 --caption-file /tmp/caption.txt [--privacy private|unlisted|public]
                       [--title "..."] [--thumbnail out/cover_<id>.jpg]
                                               resumable upload as a Short (vertical, under 3 min);
                                               title = first caption line + #Shorts unless --title is given
  python3 youtube.py status <video_id>         processing + privacy state of an upload
  python3 youtube.py login-url                 link to authorise the Tech Wall channel (once)
  python3 youtube.py exchange "<redirect url>" [--show]
                                               turn the login redirect into tokens (--show prints the refresh
                                               token so you can store it as YT_REFRESH_TOKEN)

Tokens are cached in .youtube_tokens.json (git-ignored). Nothing secret is printed unless --show is given.
Only stdlib, so it runs the same in the cloud session and on a Windows PC.
"""
import sys, os, json, time, argparse, urllib.request, urllib.parse, urllib.error

TOKEN_URL = 'https://oauth2.googleapis.com/token'
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
API = 'https://www.googleapis.com/youtube/v3'
UPLOAD = 'https://www.googleapis.com/upload/youtube/v3'
REDIRECT = os.environ.get('YT_REDIRECT_URI', 'http://localhost')
SCOPES = 'https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly'
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.youtube_tokens.json')
CATEGORY = '28'  # Science & Technology


def die(msg):
    sys.exit('youtube: ' + msg)


def env(name):
    v = os.environ.get(name, '').strip()
    if not v:
        die(f'{name} is not set (add it in the environment settings, never in the repo)')
    return v


def http(method, url, data=None, headers=None, timeout=120):
    """-> (status, parsed JSON or raw text, response headers). HTTP errors are returned, not raised."""
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            code, body, hdrs = r.status, r.read(), r.headers
    except urllib.error.HTTPError as e:
        code, body, hdrs = e.code, e.read(), e.headers
    except urllib.error.URLError as e:
        die(f'cannot reach {urllib.parse.urlsplit(url).netloc}: {e.reason} '
            '(are oauth2.googleapis.com and www.googleapis.com allowed in the environment network settings?)')
    text = body.decode('utf-8', 'replace')
    try:
        return code, json.loads(text) if text.strip() else None, hdrs
    except ValueError:
        return code, text, hdrs


def err_text(r):
    if isinstance(r, dict):
        e = r.get('error')
        if isinstance(e, dict):
            reasons = ','.join(x.get('reason', '') for x in e.get('errors', []))
            return f'{e.get("message", "")} [{reasons}]' if reasons else e.get('message', '')
        return r.get('error_description') or e or r
    return r


# ---------- tokens ----------

def load_cache():
    try:
        with open(CACHE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_cache(tok):
    tok = dict(load_cache(), **tok, saved_at=int(time.time()))  # a refresh does not return the refresh token again
    fd = os.open(CACHE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f:
        json.dump(tok, f)
    return tok


def oauth(fields):
    fields = dict(fields, client_id=env('YT_CLIENT_ID'), client_secret=env('YT_CLIENT_SECRET'))
    code, r, _ = http('POST', TOKEN_URL, urllib.parse.urlencode(fields).encode(),
                      {'Content-Type': 'application/x-www-form-urlencoded'})
    if not isinstance(r, dict) or 'access_token' not in r:
        hint = ''
        if isinstance(r, dict) and r.get('error') == 'invalid_grant':
            hint = (' (refresh token expired or revoked: if the OAuth app is still in "Testing" it dies after 7 days;'
                    ' publish the app, then redo YOUTUBE.md Part B)')
        die(f'token request failed ({code}): {err_text(r)}{hint}')
    return r


def access_token():
    """Cached access token while valid, otherwise refresh it."""
    c = load_cache()
    if c.get('access_token') and time.time() < c.get('saved_at', 0) + c.get('expires_in', 0) - 300:
        return c['access_token']
    rt = os.environ.get('YT_REFRESH_TOKEN', '').strip() or c.get('refresh_token') or env('YT_REFRESH_TOKEN')
    r = oauth({'grant_type': 'refresh_token', 'refresh_token': rt})
    return save_cache(r)['access_token']


def api(method, path, params=None, body=None, base=API, data=None, headers=None, timeout=120):
    url = base + path + ('?' + urllib.parse.urlencode(params) if params else '')
    h = {'Authorization': 'Bearer ' + access_token()}
    if body is not None:
        data = json.dumps(body).encode()
        h['Content-Type'] = 'application/json; charset=UTF-8'
    h.update(headers or {})
    return http(method, url, data, h, timeout)


def ok(code, r, what):
    if code not in (200, 201) or not isinstance(r, dict):
        die(f'{what} failed ({code}): {err_text(r)}')
    return r


# ---------- helpers ----------

def clean(s):
    return s.replace('<', '').replace('>', '')  # YouTube rejects angle brackets in titles and descriptions


def make_title(caption, title):
    t = clean(title or (caption.strip().splitlines() or ['Tech Wall'])[0]).strip()
    if '#shorts' not in t.lower() and len(t) + 8 <= 100:
        t += ' #Shorts'
    return t[:100]


def tags_from(caption):
    return [w.lstrip('#') for w in caption.split() if w.startswith('#') and len(w) > 1][:15]


def put_video(url, path, size):
    with open(path, 'rb') as f:
        data = f.read()
    for attempt in range(4):
        code, r, _ = http('PUT', url, data, {'Content-Type': 'video/mp4', 'Content-Length': str(size)}, timeout=900)
        if code in (200, 201):
            return r
        if code not in (500, 502, 503, 504):
            break
        time.sleep(2 ** attempt)
    die(f'video upload failed ({code}): {err_text(r)}')


# ---------- commands ----------

def cmd_check(a):
    code, r, _ = api('GET', '/channels', {'part': 'snippet,statistics', 'mine': 'true'})
    items = ok(code, r, 'channels.list').get('items') or []
    if not items:
        die('this login has no YouTube channel (log in again and pick the Tech Wall channel, YOUTUBE.md Part B)')
    for ch in items:
        s, st = ch['snippet'], ch.get('statistics', {})
        print(f'channel: {s.get("title")} ({s.get("customUrl", "no handle")}) id {ch["id"]}')
        print(f'videos: {st.get("videoCount")}, subscribers: {st.get("subscriberCount", "hidden")}')


def cmd_upload(a):
    if not os.path.isfile(a.video):
        die(f'no such video: {a.video}')
    caption = open(a.caption_file, encoding='utf-8').read().strip() if a.caption_file else (a.caption or '')
    snippet = {'title': make_title(caption, a.title), 'description': clean(caption)[:5000],
               'tags': tags_from(caption), 'categoryId': CATEGORY}
    status = {'privacyStatus': a.privacy, 'selfDeclaredMadeForKids': False, 'embeddable': True}
    size = os.path.getsize(a.video)
    code, r, h = api('POST', '/videos', {'uploadType': 'resumable', 'part': 'snippet,status'},
                     {'snippet': snippet, 'status': status}, base=UPLOAD,
                     headers={'X-Upload-Content-Length': str(size), 'X-Upload-Content-Type': 'video/mp4'})
    if code != 200 or not h.get('Location'):
        die(f'starting the upload failed ({code}): {err_text(r)}')
    print(f'title: {snippet["title"]}')
    v = put_video(h['Location'], a.video, size)
    vid = v.get('id') or die(f'upload finished without a video id: {v}')
    got = v.get('status', {}).get('privacyStatus')
    print(f'uploaded: video id {vid}, privacy {got}')
    if got != a.privacy:
        print(f'note: asked for {a.privacy} but YouTube set {got}. An unaudited API project can only upload '
              'private videos: switch it to Public in YouTube Studio (YOUTUBE.md, Rules and limits).')
    if a.thumbnail:
        with open(a.thumbnail, 'rb') as f:
            img = f.read()
        mime = 'image/png' if a.thumbnail.lower().endswith('.png') else 'image/jpeg'
        code, r, _ = api('POST', '/thumbnails/set', {'videoId': vid}, base=UPLOAD, data=img,
                         headers={'Content-Type': mime, 'Content-Length': str(len(img))})
        if code == 200:
            print('thumbnail: set')
        else:  # not fatal: needs a phone-verified channel, and Shorts need Partner Program access
            print(f'thumbnail: not set ({code}): {err_text(r)}; pick the title-card frame in the YouTube app instead')
    print(f'link: https://youtube.com/shorts/{vid}')


def cmd_status(a):
    code, r, _ = api('GET', '/videos', {'part': 'status,processingDetails,snippet', 'id': a.video_id})
    items = ok(code, r, 'videos.list').get('items') or []
    if not items:
        die(f'no video {a.video_id} on this channel')
    v = items[0]
    st, pd = v.get('status', {}), v.get('processingDetails', {})
    print(f'title: {v["snippet"].get("title")}')
    print(f'upload: {st.get("uploadStatus")}  processing: {pd.get("processingStatus", "?")}  '
          f'privacy: {st.get("privacyStatus")}')
    for k in ('failureReason', 'rejectionReason'):
        if st.get(k):
            print(f'{k}: {st[k]}')
    print(f'link: https://youtube.com/shorts/{a.video_id}')


def cmd_login_url(a):
    q = urllib.parse.urlencode({'client_id': env('YT_CLIENT_ID'), 'redirect_uri': REDIRECT, 'response_type': 'code',
                                'scope': SCOPES, 'access_type': 'offline', 'prompt': 'consent',
                                'include_granted_scopes': 'true', 'state': 'techwall'})
    print('Open in an incognito window, log in, pick the Tech Wall channel, allow access, then copy the address you')
    print('land on (the page itself will not load, that is fine):')
    print(AUTH_URL + '?' + q)


def cmd_exchange(a):
    v = a.redirect.strip()
    code = urllib.parse.parse_qs(urllib.parse.urlsplit(v).query).get('code', [None])[0] if '://' in v else v
    if not code:
        die('no code= found in that address')
    r = oauth({'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT})
    if not r.get('refresh_token'):
        die('no refresh token returned: use the login-url link (it asks for offline access with prompt=consent)')
    save_cache(r)
    print(f'ok: scopes {r.get("scope")}; access token valid {r.get("expires_in")} s (cached in .youtube_tokens.json)')
    if a.show:
        print('YT_REFRESH_TOKEN=' + r['refresh_token'])
    else:
        print('run again with --show on your own PC to see the refresh token for the environment settings')


def main():
    p = argparse.ArgumentParser(description='Upload Tech Wall videos to YouTube')
    sp = p.add_subparsers(dest='cmd', required=True)
    sp.add_parser('check').set_defaults(f=cmd_check)
    s = sp.add_parser('upload'); s.add_argument('video')
    s.add_argument('--caption-file'); s.add_argument('--caption'); s.add_argument('--title')
    s.add_argument('--privacy', default='private', choices=['private', 'unlisted', 'public'])
    s.add_argument('--thumbnail'); s.set_defaults(f=cmd_upload)
    s = sp.add_parser('status'); s.add_argument('video_id'); s.set_defaults(f=cmd_status)
    sp.add_parser('login-url').set_defaults(f=cmd_login_url)
    s = sp.add_parser('exchange'); s.add_argument('redirect'); s.add_argument('--show', action='store_true')
    s.set_defaults(f=cmd_exchange)
    a = p.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()

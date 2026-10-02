"""Tech Wall: post videos to TikTok (@techwallz) through the Content Posting API.

Credentials come from environment variables, never from this repo:
  TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REFRESH_TOKEN
  TIKTOK_REDIRECT_URI (optional, default below; must match the app's Login Kit redirect URI)

  python3 tiktok.py check                      refresh the token, show the account + privacy options
  python3 tiktok.py draft out/<id>.mp4         upload to the TikTok inbox as a draft (finish posting in the app)
  python3 tiktok.py post out/<id>.mp4 --caption-file /tmp/caption.txt [--privacy SELF_ONLY] [--cover-ms 5833]
                                               direct post (public only once TikTok has audited the app)
  python3 tiktok.py status <publish_id>        poll a publish until it finishes
  python3 tiktok.py login-url                  link to authorise the Tech Wall account (about once a year)
  python3 tiktok.py exchange "<redirect url>" [--show]
                                               turn the login redirect into tokens (--show prints the refresh
                                               token so you can store it as TIKTOK_REFRESH_TOKEN)

Tokens are cached in .tiktok_tokens.json (git-ignored). Nothing secret is printed unless --show is given.
Only stdlib, so it runs the same in the cloud session and on a Windows PC.
"""
import sys, os, json, time, argparse, urllib.request, urllib.parse, urllib.error

API = 'https://open.tiktokapis.com/v2'
REDIRECT = os.environ.get('TIKTOK_REDIRECT_URI', 'https://github.com/ramihamadi/techwallintegration')
SCOPES = 'user.info.basic,video.upload,video.publish'
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.tiktok_tokens.json')
MB = 1024 * 1024


def die(msg):
    sys.exit('tiktok: ' + msg)


def env(name):
    v = os.environ.get(name, '').strip()
    if not v:
        die(f'{name} is not set (add it in the environment settings, never in the repo)')
    return v


def http(method, url, data=None, headers=None, timeout=120):
    """-> (status, parsed JSON or raw text). HTTP errors are returned, not raised."""
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            code, body = r.status, r.read()
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read()
    except urllib.error.URLError as e:
        die(f'cannot reach {urllib.parse.urlsplit(url).netloc}: {e.reason} '
            '(is *.tiktokapis.com allowed in the environment network settings?)')
    text = body.decode('utf-8', 'replace')
    try:
        return code, json.loads(text) if text.strip() else None
    except ValueError:
        return code, text


# ---------- tokens ----------

def load_cache():
    try:
        with open(CACHE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_cache(tok):
    tok = dict(tok, saved_at=int(time.time()))
    fd = os.open(CACHE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f:
        json.dump(tok, f)
    return tok


def oauth(fields):
    fields = dict(fields, client_key=env('TIKTOK_CLIENT_KEY'), client_secret=env('TIKTOK_CLIENT_SECRET'))
    code, r = http('POST', API + '/oauth/token/', urllib.parse.urlencode(fields).encode(),
                   {'Content-Type': 'application/x-www-form-urlencoded'})
    if not isinstance(r, dict) or 'access_token' not in r:
        err = r.get('error_description') or r.get('error') if isinstance(r, dict) else r
        die(f'token request failed ({code}): {err}')
    return r


def access_token():
    """Cached access token while valid, otherwise refresh it."""
    c = load_cache()
    if c.get('access_token') and time.time() < c.get('saved_at', 0) + c.get('expires_in', 0) - 300:
        return c['access_token']
    rt = c.get('refresh_token') or env('TIKTOK_REFRESH_TOKEN')
    r = oauth({'grant_type': 'refresh_token', 'refresh_token': rt})
    if r.get('refresh_token') and r['refresh_token'] != os.environ.get('TIKTOK_REFRESH_TOKEN', '').strip():
        print('note: TikTok issued a new refresh token (cached in .tiktok_tokens.json). If the next session '
              'fails to refresh, run login-url + exchange --show and update TIKTOK_REFRESH_TOKEN.')
    return save_cache(r)['access_token']


def api(path, body=None):
    code, r = http('POST', API + path, json.dumps(body or {}).encode(),
                   {'Authorization': 'Bearer ' + access_token(),
                    'Content-Type': 'application/json; charset=UTF-8'})
    err = (r or {}).get('error', {}) if isinstance(r, dict) else {}
    if not isinstance(r, dict) or err.get('code') != 'ok':
        die(f'{path} failed ({code}): {err.get("code", r)} {err.get("message", "")}'.strip())
    return r.get('data', {})


# ---------- upload ----------

def chunks(size):
    """TikTok rules: < 5 MB must be one chunk; chunks are 5-64 MB, the last one takes the remainder."""
    if size <= 64 * MB:
        return size, 1
    cs = 10 * MB
    return cs, size // cs


def source_info(path):
    if not os.path.isfile(path):
        die(f'no such video: {path}')
    size = os.path.getsize(path)
    cs, n = chunks(size)
    return size, cs, n, {'source': 'FILE_UPLOAD', 'video_size': size, 'chunk_size': cs, 'total_chunk_count': n}


def upload(url, path, size, cs, n):
    with open(path, 'rb') as f:
        for i in range(n):
            start = i * cs
            end = size - 1 if i == n - 1 else start + cs - 1
            f.seek(start)
            data = f.read(end - start + 1)
            for attempt in range(3):
                code, r = http('PUT', url, data, {'Content-Type': 'video/mp4', 'Content-Length': str(len(data)),
                                                  'Content-Range': f'bytes {start}-{end}/{size}'}, timeout=600)
                if code in (200, 201, 206):
                    break
                time.sleep(2 ** attempt)
            else:
                die(f'chunk {i + 1}/{n} upload failed ({code}): {r}')
            print(f'uploaded chunk {i + 1}/{n} ({end + 1}/{size} bytes)')


def wait(publish_id, done, timeout=300):
    t0 = time.time()
    while True:
        d = api('/post/publish/status/fetch/', {'publish_id': publish_id})
        s = d.get('status')
        if s in done:
            return d
        if s == 'FAILED':
            die(f'publish {publish_id} FAILED: {d.get("fail_reason")}')
        if time.time() - t0 > timeout:
            die(f'publish {publish_id} still {s} after {timeout}s; check again with: status {publish_id}')
        time.sleep(5)


# ---------- commands ----------

def cmd_check(a):
    d = api('/post/publish/creator_info/query/')
    print(f'account: {d.get("creator_nickname")} (@{d.get("creator_username")})')
    print(f'privacy options: {", ".join(d.get("privacy_level_options", []))}')
    print(f'max video length: {d.get("max_video_post_duration_sec")} s')


def cmd_draft(a):
    size, cs, n, si = source_info(a.video)
    d = api('/post/publish/inbox/video/init/', {'source_info': si})
    print(f'publish_id: {d["publish_id"]}')
    upload(d['upload_url'], a.video, size, cs, n)
    wait(d['publish_id'], {'SEND_TO_USER_INBOX', 'PUBLISH_COMPLETE'})
    print('SEND_TO_USER_INBOX: the draft is in the @techwallz TikTok inbox; open the app to finish posting.')


def cmd_post(a):
    info = api('/post/publish/creator_info/query/')
    if a.privacy not in info.get('privacy_level_options', []):
        die(f'privacy {a.privacy} not allowed; options: {info.get("privacy_level_options")}')
    title = open(a.caption_file, encoding='utf-8').read().strip() if a.caption_file else (a.caption or '')
    post = {'title': title[:2200], 'privacy_level': a.privacy}
    if a.cover_ms is not None:
        post['video_cover_timestamp_ms'] = a.cover_ms
    size, cs, n, si = source_info(a.video)
    d = api('/post/publish/video/init/', {'post_info': post, 'source_info': si})
    print(f'publish_id: {d["publish_id"]}')
    upload(d['upload_url'], a.video, size, cs, n)
    s = wait(d['publish_id'], {'PUBLISH_COMPLETE'})
    ids = s.get('publicaly_available_post_id') or s.get('publicly_available_post_id') or []
    print(f'PUBLISH_COMPLETE ({a.privacy})')
    for i in ids:
        print(f'link: https://www.tiktok.com/@{info.get("creator_username")}/video/{i}')


def cmd_status(a):
    print(json.dumps(wait(a.publish_id, {'SEND_TO_USER_INBOX', 'PUBLISH_COMPLETE'}), indent=1))


def cmd_login_url(a):
    q = urllib.parse.urlencode({'client_key': env('TIKTOK_CLIENT_KEY'), 'scope': SCOPES, 'response_type': 'code',
                                'redirect_uri': REDIRECT, 'state': 'techwall'}, safe=',')
    print('Open in an incognito window, log in as Tech Wall, press Continue, then copy the address you land on:')
    print('https://www.tiktok.com/v2/auth/authorize/?' + q)


def cmd_exchange(a):
    v = a.redirect.strip()
    code = urllib.parse.parse_qs(urllib.parse.urlsplit(v).query).get('code', [None])[0] if '://' in v else v
    if not code:
        die('no code= found in that address')
    r = save_cache(oauth({'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT}))
    print(f'ok: scopes {r.get("scope")}; access token valid {r.get("expires_in")} s, '
          f'refresh token valid {r.get("refresh_expires_in", 0) // 86400} days (cached in .tiktok_tokens.json)')
    if a.show:
        print('TIKTOK_REFRESH_TOKEN=' + r['refresh_token'])
    else:
        print('run again with --show on your own PC to see the refresh token for the environment settings')


def main():
    p = argparse.ArgumentParser(description='Post Tech Wall videos to TikTok')
    sp = p.add_subparsers(dest='cmd', required=True)
    sp.add_parser('check').set_defaults(f=cmd_check)
    s = sp.add_parser('draft'); s.add_argument('video'); s.set_defaults(f=cmd_draft)
    s = sp.add_parser('post'); s.add_argument('video')
    s.add_argument('--caption-file'); s.add_argument('--caption')
    s.add_argument('--privacy', default='SELF_ONLY',
                   choices=['SELF_ONLY', 'MUTUAL_FOLLOW_FRIENDS', 'FOLLOWER_OF_CREATOR', 'PUBLIC_TO_EVERYONE'])
    s.add_argument('--cover-ms', type=int); s.set_defaults(f=cmd_post)
    s = sp.add_parser('status'); s.add_argument('publish_id'); s.set_defaults(f=cmd_status)
    sp.add_parser('login-url').set_defaults(f=cmd_login_url)
    s = sp.add_parser('exchange'); s.add_argument('redirect'); s.add_argument('--show', action='store_true')
    s.set_defaults(f=cmd_exchange)
    a = p.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()

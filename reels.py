"""Tech Wall: post Reels to the Facebook page and Instagram (@techwalll) through the Meta Graph API.

Credentials never live in this repo:
  Cloud session: the page token is injected by the environment proxy for graph.facebook.com and
                 rupload.facebook.com, so nothing is set and the session never sees it.
  Windows PC:    set FB_PAGE_TOKEN as well (a page token, see SETUP.md "Facebook + Instagram").
  Always:        FB_PAGE_ID, FB_API_VERSION (e.g. v26.0); IG_USER_ID is optional (looked up from the page).

  python3 reels.py check                       show the page + linked Instagram account the Reels will go to
  python3 reels.py post out/<id>.mp4 --caption-file /tmp/caption.txt --cover out/cover_<id>.jpg [--draft]
                                               Facebook (REELS.md steps 1-7), then Instagram (step 8)
  python3 reels.py facebook out/<id>.mp4 --caption-file ... --cover ... [--draft]
                                               Facebook only
  python3 reels.py instagram out/<id>.mp4 --caption-file ... [--draft] [--thumb-offset 5833]
                                               Instagram only (retry it alone if it failed after Facebook)
  python3 reels.py status <facebook video id>  processing / publishing state of a Facebook Reel

--draft: Facebook saves a draft Reel; Instagram has no drafts, so the container is uploaded and checked but
not published (it expires after 24 h). Use it for every test.
Only stdlib (+ ffmpeg for the format check), so it runs the same in the cloud session and on a Windows PC.
"""
import sys, os, re, json, time, uuid, shutil, argparse, tempfile, subprocess
import urllib.request, urllib.parse, urllib.error

GRAPH = 'https://graph.facebook.com'
RUPLOAD = 'https://rupload.facebook.com'
POLL, POLL_MAX = 15, 300          # seconds between status checks, give up after
THUMB_OFFSET = 5833               # Instagram cover time in ms: Tech Wall title card = frame 70 at 12 fps


def die(msg):
    sys.exit('reels: ' + msg)


def env(name):
    v = os.environ.get(name, '').strip()
    if not v:
        die(f'{name} is not set (add it in the environment settings, never in the repo)')
    return v


def http(method, url, data=None, headers=None, timeout=120):
    """-> (status, parsed JSON or raw text). HTTP errors are returned, not raised."""
    h = dict(headers or {})
    tok = os.environ.get('FB_PAGE_TOKEN', '').strip()
    if tok:  # PC; in the cloud the proxy adds the token itself
        h['Authorization'] = 'OAuth ' + tok
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            code, body = r.status, r.read()
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read()
    except urllib.error.URLError as e:
        die(f'cannot reach {urllib.parse.urlsplit(url).netloc}: {e.reason} '
            '(are graph.facebook.com and rupload.facebook.com allowed in the environment network settings?)')
    text = body.decode('utf-8', 'replace')
    try:
        return code, json.loads(text) if text.strip() else None
    except ValueError:
        return code, text


def err_text(r):
    if isinstance(r, dict) and isinstance(r.get('error'), dict):
        e = r['error']
        msg = e.get('error_user_msg') or e.get('message', '')
        if e.get('code') in (104, 190):
            msg += (' (no valid page token: in the cloud check the proxy injection for graph.facebook.com,'
                    ' on a PC set FB_PAGE_TOKEN; see SETUP.md)')
        return f'{msg} [code {e.get("code")}{"/" + str(e["error_subcode"]) if e.get("error_subcode") else ""}]'
    if isinstance(r, dict) and r.get('debug_info'):
        return r['debug_info'].get('message', r)
    return r


def graph(method, path, params=None, form=None, data=None, headers=None):
    url = f'{GRAPH}/{env("FB_API_VERSION")}/{path}' + ('?' + urllib.parse.urlencode(params) if params else '')
    h = dict(headers or {})
    if form is not None:
        data = urllib.parse.urlencode(form).encode()
        h['Content-Type'] = 'application/x-www-form-urlencoded'
    return http(method, url, data, h)


def ok(code, r, what):
    if code != 200 or not isinstance(r, dict) or 'error' in r:
        die(f'{what} failed ({code}): {err_text(r)}')
    return r


def multipart(fields, files):
    b = 'techwall' + uuid.uuid4().hex
    out = []
    for k, v in fields.items():
        out.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, (name, blob, mime) in files.items():
        out.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{name}"\r\n'
                   f'Content-Type: {mime}\r\n\r\n'.encode() + blob + b'\r\n')
    out.append(f'--{b}--\r\n'.encode())
    return b''.join(out), 'multipart/form-data; boundary=' + b


def rupload(url, path, what):
    """Binary upload to rupload.facebook.com (Facebook video or Instagram container)."""
    with open(path, 'rb') as f:
        blob = f.read()
    for attempt in range(3):  # "upstream request failed" is a proxy glitch: retry
        code, r = http('POST', url, blob, {'offset': '0', 'file_size': str(len(blob)),
                                           'Content-Type': 'application/octet-stream'}, timeout=900)
        if code == 200 and isinstance(r, dict) and r.get('success'):
            return
        time.sleep(2 ** attempt)
    die(f'{what} upload failed ({code}): {err_text(r)}')


def wait(check, what):
    """Poll check() -> (done, info) every POLL s, up to POLL_MAX s."""
    t0 = time.time()
    while True:
        done, info = check()
        if done:
            return info
        if time.time() - t0 > POLL_MAX:
            die(f'{what} still not ready after {POLL_MAX // 60} min: {json.dumps(info)}')
        time.sleep(POLL)


# ---------- step 1: format check ----------

def ffmpeg_exe():
    exe = shutil.which('ffmpeg')
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return None


def prepare(video):
    """Return a file that meets the Reel spec: H.264 + AAC MP4, 9:16, 3-90 s, 24-60 fps (REELS.md step 1)."""
    if not os.path.isfile(video):
        die(f'no such video: {video}')
    ff = ffmpeg_exe()
    if not ff:
        print('note: ffmpeg not found, skipping the format check')
        return video
    info = subprocess.run([ff, '-hide_banner', '-i', video], capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', info)
    dur = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0
    v = re.search(r'Video: (\w+).*?, (\d{2,5})x(\d{2,5}).*?, ([\d.]+) fps', info)
    a = re.search(r'Audio: (\w+)', info)
    if dur > 90:
        die(f'{video} is {dur:.0f} s; Reels are 3-90 s (not cutting it automatically)')
    fine = (v and v[1] == 'h264' and int(v[2]) * 16 == int(v[3]) * 9 and 24 <= float(v[4]) <= 60
            and a and a[1] == 'aac' and dur >= 3)
    print(f'video: {os.path.basename(video)}, {dur:.1f} s, '
          + (f'{v[1]} {v[2]}x{v[3]} {v[4]} fps' if v else 'no video stream') + f', audio {a[1] if a else "none"}')
    if fine:
        return video
    out = os.path.join(tempfile.gettempdir(), 'techwall_reel.mp4')
    cmd = [ff, '-y', '-loglevel', 'error', '-i', video]
    if not a:
        cmd += ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest']
    cmd += ['-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '128k', '-ar', '48000', '-movflags', '+faststart', out]
    print('converting to the Reel format (1080x1920, 30 fps, H.264 + AAC)...')
    if subprocess.run(cmd).returncode:
        die('ffmpeg conversion failed')
    return out


def read_caption(a):
    if a.caption_file:
        return open(a.caption_file, encoding='utf-8').read().strip()
    if a.caption:
        return a.caption.strip()
    die('give the caption with --caption-file (README section 6 template)')


# ---------- Facebook (steps 2-7) ----------

def fb_status(vid):
    return ok(*graph('GET', vid, {'fields': 'status'}), 'status check').get('status', {})


def facebook(video, caption, cover, draft):
    page, ver = env('FB_PAGE_ID'), env('FB_API_VERSION')
    r = ok(*graph('POST', f'{page}/video_reels', form={'upload_phase': 'start'}), 'starting the Facebook upload')
    vid = r.get('video_id') or die(f'no video_id in {r}')
    rupload(f'{RUPLOAD}/video-upload/{ver}/{vid}', video, 'Facebook video')
    state = 'DRAFT' if draft else 'PUBLISHED'
    r = ok(*graph('POST', f'{page}/video_reels', form={'upload_phase': 'finish', 'video_id': vid,
                                                      'video_state': state, 'description': caption}),
           'finishing the Facebook Reel')
    if not r.get('success'):
        die(f'finishing the Facebook Reel failed: {r}')

    def check():
        st = fb_status(vid)
        bad = [k for k, x in st.items() if isinstance(x, dict) and x.get('status') == 'error']
        if bad or st.get('video_status') == 'error':
            die(f'Facebook processing error: {json.dumps(st)}')
        return st.get('video_status') == 'ready' or st.get('publishing_phase', {}).get('status') == 'complete', st
    st = wait(check, 'Facebook processing')
    print(f'facebook: video id {vid}, {state}, video_status {st.get("video_status")}, '
          f'publishing {st.get("publishing_phase", {}).get("publish_status", "?")}')
    print('facebook cover: ' + (set_cover(vid, cover) if cover else 'skipped (no --cover given)'))
    print(f'facebook link: https://www.facebook.com/reel/{vid}')
    return vid


def set_cover(vid, cover):
    """REELS.md step 7: upload the title card as the preferred thumbnail, verify, retry once."""
    with open(cover, 'rb') as f:
        img = f.read()
    mime = 'image/png' if cover.lower().endswith('.png') else 'image/jpeg'
    for attempt in range(2):
        body, ctype = multipart({'is_preferred': 'true'}, {'source': (os.path.basename(cover), img, mime)})
        code, r = graph('POST', f'{vid}/thumbnails', data=body, headers={'Content-Type': ctype})
        if code == 200:
            code, t = graph('GET', f'{vid}/thumbnails', {'fields': 'is_preferred,width,height'})
            pref = [x for x in (t or {}).get('data', []) if x.get('is_preferred')] if isinstance(t, dict) else []
            if pref:
                return f'set ({pref[0].get("width")}x{pref[0].get("height")})'
        time.sleep(5)
    die(f'cover not set on Facebook video {vid} ({code}): {err_text(r)}; '
        f'retry with the Graph API (REELS.md step 7), do not repost the video')


# ---------- Instagram (step 8) ----------

def ig_user():
    v = os.environ.get('IG_USER_ID', '').strip()
    if v:
        return v
    r = ok(*graph('GET', env('FB_PAGE_ID'), {'fields': 'instagram_business_account'}), 'Instagram account lookup')
    return (r.get('instagram_business_account') or {}).get('id') or die('no Instagram account linked to the page')


def instagram(video, caption, draft, thumb_offset):
    ig, ver = ig_user(), env('FB_API_VERSION')
    r = ok(*graph('POST', f'{ig}/media', form={'media_type': 'REELS', 'upload_type': 'resumable',
                                               'share_to_feed': 'true', 'thumb_offset': str(thumb_offset),
                                               'caption': caption}), 'creating the Instagram container')
    cid = r.get('id') or die(f'no container id in {r}')
    rupload(f'{RUPLOAD}/ig-api-upload/{ver}/{cid}', video, 'Instagram video')

    def check():
        s = ok(*graph('GET', cid, {'fields': 'status_code,status'}), 'Instagram status check')
        if s.get('status_code') in ('ERROR', 'EXPIRED'):
            die(f'Instagram container {s.get("status_code")}: {json.dumps(s)}')
        return s.get('status_code') == 'FINISHED', s
    wait(check, 'Instagram processing')
    if draft:
        print(f'instagram: container {cid} FINISHED, not published (draft/test; it expires after 24 h)')
        return None
    r = ok(*graph('POST', f'{ig}/media_publish', form={'creation_id': cid}), 'publishing on Instagram')
    mid = r.get('id') or die(f'no media id in {r}')
    code, p = graph('GET', mid, {'fields': 'permalink'})
    print(f'instagram: media id {mid}, PUBLISHED')
    print(f'instagram link: {p.get("permalink") if isinstance(p, dict) and p.get("permalink") else "(permalink not returned yet)"}')
    return mid


# ---------- commands ----------

def cmd_check(a):
    r = ok(*graph('GET', env('FB_PAGE_ID'), {'fields': 'name,instagram_business_account{username}'}), 'page lookup')
    ig = r.get('instagram_business_account') or {}
    print(f'facebook page: {r.get("name")} (id {r.get("id")})')
    print(f'instagram: @{ig.get("username")} (id {ig.get("id")})' if ig else 'instagram: none linked to the page')
    print('token: ' + ('FB_PAGE_TOKEN (PC; in the cloud the proxy token wins)' if os.environ.get('FB_PAGE_TOKEN', '').strip()
                       else 'injected by the environment proxy'))


def cmd_post(a):
    caption, video = read_caption(a), prepare(a.video)
    facebook(video, caption, a.cover, a.draft)
    try:
        instagram(video, caption, a.draft, a.thumb_offset)
    except SystemExit as e:
        print(e.code if isinstance(e.code, str) else '', file=sys.stderr)
        die(f'Facebook is done, Instagram failed: retry Instagram alone (do not repost to Facebook):\n'
            f'  python3 reels.py instagram {a.video} --caption-file <caption>' + (' --draft' if a.draft else ''))


def cmd_facebook(a):
    facebook(prepare(a.video), read_caption(a), a.cover, a.draft)


def cmd_instagram(a):
    instagram(prepare(a.video), read_caption(a), a.draft, a.thumb_offset)


def cmd_status(a):
    st = fb_status(a.video_id)
    print(json.dumps(st, indent=1))
    print(f'link: https://www.facebook.com/reel/{a.video_id}')


def main():
    p = argparse.ArgumentParser(description='Post Tech Wall Reels to Facebook and Instagram')
    sp = p.add_subparsers(dest='cmd', required=True)
    sp.add_parser('check').set_defaults(f=cmd_check)
    for name, f in (('post', cmd_post), ('facebook', cmd_facebook), ('instagram', cmd_instagram)):
        s = sp.add_parser(name); s.add_argument('video')
        s.add_argument('--caption-file'); s.add_argument('--caption')
        s.add_argument('--draft', action='store_true', help='test mode: nothing is published')
        if name != 'instagram':
            s.add_argument('--cover', help='out/cover_<id>.jpg')
        if name != 'facebook':
            s.add_argument('--thumb-offset', type=int, default=THUMB_OFFSET, help='Instagram cover time in ms')
        s.set_defaults(f=f)
    s = sp.add_parser('status'); s.add_argument('video_id'); s.set_defaults(f=cmd_status)
    a = p.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()

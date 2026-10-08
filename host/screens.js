/* Tech Wall Host engine: phone screens built from the episode spec (iOS-style look-alikes, generic, no logos).
   Screen types:
     home     {type:'home', apps:[{id,label,icon,bg}]?, dock:[icon...]?}            default app grid includes id 'settings'
     list     {type:'list', back:'Settings'|null, title, large:true, search:false,
               groups:[{header?, footer?, rows:[{id,label,icon?,color?,chev?,value?,toggle?:true|false,style?:'blue'|'grey'|'red'}]}]}
     passcode {type:'passcode', title, prompt, reprompt, digits:6}
     lock     {type:'lock', date, time, badge}
     html     {type:'html', html:'<div data-id="x">…</div>', bg:'#fff'}   any custom mock; tap targets carry data-id
   Every tappable element gets data-id="<screen>:<id>". */
(function(){
const ICONS = {
  gear:'<svg viewBox="0 0 40 40"><g fill="#e5e5ea"><circle cx="20" cy="20" r="11"/><g><rect x="17.5" y="4" width="5" height="8" rx="1.5"/><rect x="17.5" y="28" width="5" height="8" rx="1.5"/><rect x="4" y="17.5" width="8" height="5" rx="1.5"/><rect x="28" y="17.5" width="8" height="5" rx="1.5"/></g><g transform="rotate(45 20 20)"><rect x="17.5" y="4" width="5" height="8" rx="1.5"/><rect x="17.5" y="28" width="5" height="8" rx="1.5"/><rect x="4" y="17.5" width="8" height="5" rx="1.5"/><rect x="28" y="17.5" width="8" height="5" rx="1.5"/></g></g><circle cx="20" cy="20" r="5" fill="#636366"/></svg>',
  photos:'<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="none" stroke="#ff9500" stroke-width="4"/><circle cx="20" cy="20" r="6" fill="#ff2d55"/></svg>',
  mail:'<svg viewBox="0 0 40 40"><rect x="5" y="10" width="30" height="21" rx="3" fill="#fff"/><path d="M6 12l14 10 14-10" stroke="#007aff" stroke-width="3" fill="none"/></svg>',
  maps:'<svg viewBox="0 0 40 40"><path d="M10 30l20-20M10 10h10M30 30V20" stroke="#fff" stroke-width="4" stroke-linecap="round"/></svg>',
  clock:'<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="15" fill="#fff"/><path d="M20 10v10l7 5" stroke="#1c1c1e" stroke-width="3" fill="none" stroke-linecap="round"/></svg>',
  camera:'<svg viewBox="0 0 40 40"><rect x="5" y="12" width="30" height="20" rx="4" fill="#3a3a3c"/><circle cx="20" cy="22" r="7" fill="#d1d1d6"/></svg>',
  music:'<svg viewBox="0 0 40 40"><path d="M16 28V12l14-3v16" stroke="#fff" stroke-width="3.5" fill="none"/><circle cx="13" cy="28" r="4" fill="#fff"/><circle cx="27" cy="25" r="4" fill="#fff"/></svg>',
  notes:'<svg viewBox="0 0 40 40"><path d="M10 14h20M10 21h20M10 28h12" stroke="#8a6d00" stroke-width="3" stroke-linecap="round"/></svg>',
  weather:'<svg viewBox="0 0 40 40"><path d="M8 26c4-10 20-10 24 0" stroke="#fff" stroke-width="4" fill="none"/><circle cx="20" cy="14" r="5" fill="#fff"/></svg>',
  videos:'<svg viewBox="0 0 40 40"><path d="M14 10l14 10-14 10z" fill="#fff"/></svg>',
  books:'<svg viewBox="0 0 40 40"><rect x="9" y="8" width="22" height="26" rx="3" fill="#fff"/><path d="M13 16h14M13 22h14M13 28h8" stroke="#ff9500" stroke-width="2.5"/></svg>',
  stocks:'<svg viewBox="0 0 40 40"><path d="M10 28V18M17 28V12M24 28v-8M31 28V15" stroke="#fff" stroke-width="4" stroke-linecap="round"/></svg>',
  phone:'<svg viewBox="0 0 40 40"><path d="M13 9c2 0 3 5 2 7-1 1-2 2 0 5s4 4 5 3c2-1 7 0 7 2 0 3-3 5-6 4C14 28 10 20 9 15c-1-3 1-6 4-6z" fill="#fff"/></svg>',
  browser:'<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="14" fill="none" stroke="#fff" stroke-width="3"/><path d="M24 16l-3 8-5 0 3-8z" fill="#fff"/></svg>',
  chat:'<svg viewBox="0 0 40 40"><path d="M8 18c0-6 5-10 12-10s12 4 12 10-5 10-12 10c-2 0-3 0-5-1l-6 3 1-5c-1-2-2-4-2-7z" fill="#fff"/></svg>',
  // small row glyphs (20x20, white on the coloured square)
  airplane:'<svg viewBox="0 0 20 20"><path d="M3 11l14-6-4 12-3-4z" fill="#fff"/></svg>',
  wifi:'<svg viewBox="0 0 20 20"><path d="M3 8a10 10 0 0 1 14 0M6 11a6 6 0 0 1 8 0" stroke="#fff" stroke-width="2" fill="none"/><circle cx="10" cy="14.5" r="1.8" fill="#fff"/></svg>',
  bluetooth:'<svg viewBox="0 0 20 20"><path d="M6 6l8 8-4 3V3l4 3-8 8" stroke="#fff" stroke-width="2" fill="none"/></svg>',
  bell:'<svg viewBox="0 0 20 20"><rect x="4" y="4" width="12" height="12" rx="3" fill="#fff"/></svg>',
  sound:'<svg viewBox="0 0 20 20"><path d="M4 8h3l4-3v10l-4-3H4z" fill="#fff"/></svg>',
  moon:'<svg viewBox="0 0 20 20"><path d="M13 3a7 7 0 1 0 4 11A6 6 0 0 1 13 3z" fill="#fff"/></svg>',
  general:'<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="5" fill="none" stroke="#fff" stroke-width="2.5"/></svg>',
  display:'<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="4" fill="#fff"/></svg>',
  faceid:'<svg viewBox="0 0 20 20"><path d="M3 7V4h3M14 4h3v3M17 13v3h-3M6 16H3v-3" stroke="#fff" stroke-width="2" fill="none"/><path d="M7 12c2 2 4 2 6 0" stroke="#fff" stroke-width="1.8" fill="none"/></svg>',
  battery:'<svg viewBox="0 0 20 20"><rect x="3" y="6" width="12" height="8" rx="2" fill="#fff"/></svg>',
  privacy:'<svg viewBox="0 0 20 20"><path d="M10 3c3 2 4 2 6 2 0 6-2 10-6 12-4-2-6-6-6-12 2 0 3 0 6-2z" fill="#fff"/></svg>',
  lock:'<svg viewBox="0 0 20 20"><path d="M6 9V7a4 4 0 0 1 8 0v2" stroke="#fff" stroke-width="2" fill="none"/><rect x="4.5" y="9" width="11" height="8" rx="2" fill="#fff"/></svg>',
  eye:'<svg viewBox="0 0 20 20"><path d="M2 10s3-5 8-5 8 5 8 5-3 5-8 5-8-5-8-5z" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="10" cy="10" r="2.4" fill="#fff"/></svg>',
  hand:'<svg viewBox="0 0 20 20"><path d="M7 17V8a1.4 1.4 0 0 1 2.8 0v4V5a1.4 1.4 0 0 1 2.8 0v7V7a1.4 1.4 0 0 1 2.8 0v6c0 3-2 4-4.5 4z" fill="#fff"/></svg>',
  person:'<svg viewBox="0 0 20 20"><circle cx="10" cy="7" r="3.2" fill="#fff"/><path d="M4 17c0-4 3-6 6-6s6 2 6 6z" fill="#fff"/></svg>',
  star:'<svg viewBox="0 0 20 20"><path d="M10 2l2.4 5 5.6.6-4.2 3.8 1.2 5.6L10 14.2 5 17l1.2-5.6L2 7.6 7.6 7z" fill="#fff"/></svg>',
  dot:'<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="4" fill="#fff"/></svg>',
};
const DEFAULT_APPS = [
  {id:'photos',label:'Photos',icon:'photos',bg:'linear-gradient(#fff,#f0f0f0)'},
  {id:'mail',label:'Mail',icon:'mail',bg:'linear-gradient(#5ac8fa,#007aff)'},
  {id:'maps',label:'Maps',icon:'maps',bg:'linear-gradient(#76e07a,#2fb344)'},
  {id:'clock',label:'Clock',icon:'clock',bg:'#1c1c1e'},
  {id:'camera',label:'Camera',icon:'camera',bg:'linear-gradient(#d1d1d6,#8e8e93)'},
  {id:'music',label:'Music',icon:'music',bg:'linear-gradient(#ff6b81,#ff2d55)'},
  {id:'notes',label:'Notes',icon:'notes',bg:'linear-gradient(#fff6c2,#ffd60a)'},
  {id:'settings',label:'Settings',icon:'gear',bg:'linear-gradient(#a1a1a6,#636366)'},
  {id:'weather',label:'Weather',icon:'weather',bg:'linear-gradient(#64d2ff,#0a84ff)'},
  {id:'videos',label:'Videos',icon:'videos',bg:'linear-gradient(#bf5af2,#7b2ff7)'},
  {id:'books',label:'Books',icon:'books',bg:'linear-gradient(#ffb340,#ff9500)'},
  {id:'stocks',label:'Stocks',icon:'stocks',bg:'linear-gradient(#30d158,#248a3d)'},
];
const DEFAULT_DOCK = [
  {icon:'phone',bg:'linear-gradient(#5ef07f,#2fbf4f)'},{icon:'browser',bg:'linear-gradient(#5ac8fa,#0a84ff)'},
  {icon:'chat',bg:'linear-gradient(#5ef07f,#2fbf4f)'},{icon:'music',bg:'linear-gradient(#ff6b81,#ff2d55)'}];
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const sb = (dark, time) => `<div class="sb"${dark?' style="color:#fff"':''}><span>${time||''}</span><span class="bat"></span></div>`;

function home(name, s, time){
  const apps = s.apps || DEFAULT_APPS, dock = s.dock || DEFAULT_DOCK;
  return `<div class="scr home" style="background:${s.wallpaper||'linear-gradient(160deg,#ff9a62 0%,#e8507a 45%,#5b4bd6 100%)'}">${sb(true,time)}
    <div class="grid">${apps.map(a=>`<div class="app" data-id="${name}:${a.id}"><div class="ic" style="background:${a.bg}">${ICONS[a.icon]||''}</div>${esc(a.label)}</div>`).join('')}</div>
    <div class="dock">${dock.map(d=>`<div class="ic" style="background:${d.bg}">${ICONS[d.icon]||''}</div>`).join('')}</div></div>`;
}
function row(name, r){
  const cls = ['row']; if (r.style) cls.push(r.style);
  const ic = r.icon ? `<div class="sq" style="background:${r.color||'#8e8e93'}">${ICONS[r.icon]||''}</div>` : '';
  const right = r.toggle!==undefined ? `<span class="tog${r.toggle?' on':''}"><i></i></span>`
              : (r.value!==undefined ? `<span class="val">${esc(r.value)}</span>` : '') + (r.chev ? '<span class="chev">›</span>' : '');
  return `<div class="${cls.join(' ')}"${r.id?` data-id="${name}:${r.id}"`:''}${r.toggle!==undefined?` data-toggle="${r.toggle?1:0}"`:''}><div class="flash"></div>${ic}<span class="lbl">${esc(r.label)}</span>${right}</div>`;
}
function list(name, s, time){
  const groups = (s.groups||[]).map(g =>
    (g.header?`<div class="sect">${esc(g.header)}</div>`:'') +
    `<div class="group">${g.rows.map(r=>row(name,r)).join('')}</div>` +
    (g.footer?`<div class="foot">${esc(g.footer)}</div>`:'')).join('');
  return `<div class="scr list">${sb(false,time)}${s.back?`<div class="nav">‹ ${esc(s.back)}</div>`:''}
    <div class="big"${s.title&&s.title.length>16?' style="font-size:32px"':''}>${esc(s.title||'')}</div>
    ${s.search?'<div class="search">⌕ Search</div>':''}${groups}</div>`;
}
function passcode(name, s, time){
  const n = s.digits||6, L = ['','ABC','DEF','GHI','JKL','MNO','PQRS','TUV','WXYZ'];
  const keys = [1,2,3,4,5,6,7,8,9].map(k=>`<div class="k" data-k="${k}">${k}<small>${L[k-1]||'&nbsp;'}</small></div>`).join('')
             + '<div class="k blank"></div><div class="k" data-k="0">0</div><div class="k blank"></div>';
  return `<div class="scr pass">${sb(false,time)}<div style="padding:0 22px"><span class="blue" style="font-size:18px">Cancel</span></div>
    <div class="ptitle">${esc(s.title||'Set Passcode')}</div><div class="plabel"></div>
    <div class="dots">${'<i></i>'.repeat(n)}</div><div class="popts">Passcode Options</div><div class="pad">${keys}</div></div>`;
}
function lock(name, s){
  return `<div class="scr lockscr">${sb(true,'')}
    <svg class="padlock" viewBox="0 0 100 120"><path class="shackle" d="M25 52V36a25 25 0 0 1 50 0v16" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/><rect x="12" y="50" width="76" height="62" rx="14" fill="#fff"/><circle cx="50" cy="78" r="9" fill="#3a2a9c"/><rect x="46" y="80" width="8" height="18" rx="4" fill="#3a2a9c"/></svg>
    <div class="ldate">${esc(s.date||'Thursday, October 8')}</div><div class="ltime">${esc(s.time||'10:08')}</div>
    ${s.badge?`<div class="lbadge">${esc(s.badge)}</div>`:''}<div class="lbtn" style="left:44px"></div><div class="lbtn" style="right:44px"></div></div>`;
}
function html(name, s){
  const body = s.html.replace(/data-id="([^":]+)"/g, `data-id="${name}:$1"`);
  return `<div class="scr custom" style="background:${s.bg||'#f2f2f7'}">${body}</div>`;
}
const BUILD = {home, list, passcode, lock, html};
window.HostScreens = {
  ICONS,
  build(root, screens, time){
    const out = {};
    for (const [name, s] of Object.entries(screens)){
      const wrap = document.createElement('div');
      wrap.innerHTML = (BUILD[s.type]||html)(name, s, time).trim();
      const el = wrap.firstElementChild; el.dataset.screen = name; el.style.display = 'none';
      root.appendChild(el); out[name] = el;
    }
    return out;
  }
};
})();

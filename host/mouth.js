/* Mouth warp module: deforms the real pixels of the illustration (lower lip + jaw move,
   upper lip lifts, lips pucker) and paints a mouth cavity with teeth/tongue in the gap.
   Geometry is per pose, in cutout pixel coordinates. */
(function(){
  const POSE_MOUTH = {
    front:  {cx:360, cy:278, a:31, ang:0},
    talk:   {cx:390, cy:288, a:33, ang:-6},
    point:  {cx:395, cy:296, a:27, ang:-11.5},
    welcome:{cx:462, cy:287, a:38, ang:-2},
  };
  // Preston-Blair shapes (Rhubarb). o = opening as fraction of mouth half-width.
  const VIS = {
    X:{o:0,   s:1.00, up:.25, r:.2, tu:0,  tl:0,  tg:0},
    A:{o:0,   s:0.96, up:.25, r:.2, tu:0,  tl:0,  tg:0},
    B:{o:.17, s:1.00, up:.30, r:.0, tu:1,  tl:1,  tg:0},
    C:{o:.44, s:0.97, up:.30, r:.2, tu:1,  tl:.25,tg:.35},
    D:{o:.72, s:0.95, up:.32, r:.3, tu:1,  tl:.1, tg:.7},
    E:{o:.44, s:0.74, up:.25, r:.7, tu:.6, tl:0,  tg:.3},
    F:{o:.34, s:0.50, up:.20, r:1,  tu:0,  tl:0,  tg:0},
    G:{o:.10, s:1.00, up:.40, r:.0, tu:1,  tl:0,  tg:0},
    H:{o:.46, s:0.95, up:.30, r:.3, tu:.8, tl:0,  tg:1},
  };
  const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
  const sstep=(a,b,x)=>{x=clamp((x-a)/(b-a));return x*x*(3-2*x);};
  const ease=x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;};

  function visemeAt(cues, t){
    let i=0; while (i+1<cues.length && t>=cues[i+1][0]) i++;
    const cur=VIS[cues[i][1]], prev=i>0?VIS[cues[i-1][1]]:cur;
    const k=ease(clamp((t-cues[i][0])/0.075));
    const o={}; for (const key in cur) o[key]=prev[key]+(cur[key]-prev[key])*k;
    return o;
  }

  const srcCache = {};
  function srcData(name, im){
    if (!srcCache[name]){
      const c=document.createElement("canvas"); c.width=im.width; c.height=im.height;
      const x=c.getContext("2d"); x.drawImage(im,0,0);
      srcCache[name]={data:x.getImageData(0,0,im.width,im.height), w:im.width, h:im.height};
    }
    return srcCache[name];
  }

  // lip profile across the mouth: 1 at centre, 0 beyond the corners (smooth)
  function L(u, aw, ex){ const q=Math.abs(u)/aw; return q>=1?0:Math.pow(Math.cos(q*Math.PI/2),ex); }
  function W(u, a){ const q=Math.abs(u)/(2.4*a); return q>=1?0:Math.pow(Math.cos(q*Math.PI/2),2); }

  function makeField(P, v){
    const a=P.a, o=v.o*a, aw=a*(0.55+0.45*v.s)*1.12, pk=(1-v.s), ex=1.15-0.65*v.r;
    return {
      a, o, aw, pk,
      // displacement (du,dv) in mouth-local coords, evaluated at OUTPUT position
      disp(u, w){
        let dv=0, du=0;
        if (w>=0){
          dv = o*L(u,aw,ex)*Math.exp(-w/24) + 0.5*o*W(u,a)*sstep(0,26,w)*(1-sstep(45,150,w));
        } else {
          dv = -v.up*o*L(u,aw,ex)*Math.exp(w/9);
        }
        // pucker: pull lips toward the centre
        du = -u*pk*0.8*W(u,a*0.8)*Math.exp(-(w*w)/(28*28));
        return [du,dv];
      }
    };
  }

  /* Warp `off` canvas context (which already holds the pose image) in place. */
  function applyMouth(offc, name, im, v){
    const P=POSE_MOUTH[name]; if (!P || v.o<0.01) return;
    const S=srcData(name, im), F=makeField(P, v);
    const ca=Math.cos(P.ang*Math.PI/180), sa=Math.sin(P.ang*Math.PI/180);
    const x0=Math.round(P.cx-3*P.a), y0=Math.round(P.cy-2.2*P.a), w=Math.round(6*P.a), h=Math.round(6.6*P.a);
    const out=offc.createImageData(w,h), od=out.data, sd=S.data.data, SW=S.w, SH=S.h;
    for (let j=0;j<h;j++){
      for (let i=0;i<w;i++){
        const X=x0+i-P.cx, Y=y0+j-P.cy;
        const u= X*ca + Y*sa, ww=-X*sa + Y*ca;           // local coords (u along lip line, w down)
        const [du,dv]=F.disp(u,ww);
        const su=u-du, sw=ww-dv;
        const sx=P.cx + su*ca - sw*sa, sy=P.cy + su*sa + sw*ca;
        // bilinear sample
        const fx=Math.floor(sx), fy=Math.floor(sy), tx=sx-fx, ty=sy-fy;
        const o=(j*w+i)*4;
        if (fx<0||fy<0||fx+1>=SW||fy+1>=SH){ od[o+3]=0; continue; }
        const p00=(fy*SW+fx)*4, p10=p00+4, p01=p00+SW*4, p11=p01+4;
        for (let c=0;c<4;c++){
          od[o+c]=(sd[p00+c]*(1-tx)+sd[p10+c]*tx)*(1-ty)+(sd[p01+c]*(1-tx)+sd[p11+c]*tx)*ty;
        }
      }
    }
    offc.clearRect(x0,y0,w,h); offc.putImageData(out,x0,y0);

    // ---- mouth cavity between the displaced lips (local frame) ----
    const N=40, top=[], bot=[];
    for (let k=0;k<=N;k++){
      const u=-F.aw + 2*F.aw*k/N;
      // lower edge: smallest w>=0 whose source lands at/after the lip line
      let wb=0; while (wb<60 && wb - F.disp(u,wb)[1] < 0) wb+=0.25;
      let wt=0; while (wt>-30 && wt - F.disp(u,wt)[1] > 0) wt-=0.25;
      // pucker also squeezes the visible opening horizontally
      const uu=u*(1-F.pk*0.75);
      top.push([uu,wt]); bot.push([uu,wb]);
    }
    const hmax=Math.max(...bot.map((p,i)=>p[1]-top[i][1]));
    if (hmax<0.8) return;
    offc.save();
    offc.translate(P.cx,P.cy); offc.rotate(P.ang*Math.PI/180);
    offc.beginPath();
    top.forEach((p,i)=>i?offc.lineTo(p[0],p[1]):offc.moveTo(p[0],p[1]));
    for (let i=bot.length-1;i>=0;i--) offc.lineTo(bot[i][0],bot[i][1]);
    offc.closePath();
    offc.save(); offc.clip();
    const g=offc.createRadialGradient(0,hmax*0.2,1,0,hmax*0.2,F.aw);
    g.addColorStop(0,"#1a0707"); g.addColorStop(1,"#3d1512");
    offc.fillStyle=g; offc.fillRect(-F.aw-2,-40,2*F.aw+4,100);
    // tongue
    if (v.tg>0.05){
      offc.fillStyle=`rgba(190,86,92,${0.9*v.tg})`;
      offc.beginPath(); offc.ellipse(0, hmax*0.85, F.aw*0.55, Math.max(2,hmax*0.45), 0, 0, Math.PI*2); offc.fill();
    }
    // upper teeth: follow the upper lip edge, fade toward corners
    if (v.tu>0.05){
      const th=Math.min(hmax*0.42+0.6, P.a*0.17);
      const tg=offc.createLinearGradient(0,-4,0,th);
      tg.addColorStop(0,`rgba(240,232,222,${0.88*v.tu})`); tg.addColorStop(1,`rgba(196,184,172,${0.85*v.tu})`);
      offc.fillStyle=tg; offc.beginPath();
      top.forEach((p,i)=>{ const q=Math.abs(p[0])/F.aw; const y=p[1]-0.5; i?offc.lineTo(p[0],y):offc.moveTo(p[0],y); });
      for (let i=top.length-1;i>=0;i--){ const p=top[i]; const q=Math.abs(p[0])/F.aw; offc.lineTo(p[0], p[1]+th*Math.max(0,1-q*q*1.15)); }
      offc.closePath(); offc.fill();
    }
    if (v.tl>0.05){
      const th=Math.min(hmax*0.38+0.5, P.a*0.14);
      offc.fillStyle=`rgba(225,218,208,${0.9*v.tl})`; offc.beginPath();
      bot.forEach((p,i)=>{ const y=p[1]+0.5; i?offc.lineTo(p[0],y):offc.moveTo(p[0],y); });
      for (let i=bot.length-1;i>=0;i--){ const p=bot[i]; const q=Math.abs(p[0])/F.aw; offc.lineTo(p[0], p[1]-th*Math.max(0,1-q*q*1.3)); }
      offc.closePath(); offc.fill();
    }
    offc.restore();
    // soft inner-lip shadow so the cavity sits under the lips
    offc.lineWidth=1.6; offc.strokeStyle="rgba(60,20,16,.55)";
    offc.beginPath(); top.forEach((p,i)=>i?offc.lineTo(p[0],p[1]):offc.moveTo(p[0],p[1])); offc.stroke();
    offc.strokeStyle="rgba(60,20,16,.35)";
    offc.beginPath(); bot.forEach((p,i)=>i?offc.lineTo(p[0],p[1]):offc.moveTo(p[0],p[1])); offc.stroke();
    offc.restore();
  }
  window.Mouth = { visemeAt, applyMouth, VIS, POSE_MOUTH };
})();

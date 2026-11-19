#!/usr/bin/env python3
"""Unity .unitypackage icindeki ParticleSystem prefab'larinin YAKLASIK onizlemesi (Unity olmadan).
Okunan moduller: main (sure, gecikme, omur, hiz, boyut, renk, donus, maxParticles), emission (hiz + patlamalar),
shape (kure/yarim kure/koni/daire/kutu: yaricap, aci), sizeOverLifetime, colorOverLifetime, rotationOverLifetime,
textureSheetAnimation (tilesX/Y, frameOverTime), renderer (billboard / stretched / mesh->billboard yaklasimi), materyal (doku, renk, eklemeli/alfa).
Okunmayan: noise, collision, sub-emitter, trails, velocityOverLifetime egrileri (yalniz sabit), force, 3B mesh parcaciklar.
Kamera: onden ortografik (x saga, y yukari).  Kullanim: onizle.py PAKET_KLASORU CIKTI_KLASORU"""
import os, sys, re, math, glob, yaml, numpy as np
from PIL import Image
PK, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
# --- paket: guid -> (yol, dosya)
G = {}
for g in os.listdir(PK):
    pn = os.path.join(PK, g, "pathname")
    if os.path.exists(pn): G[g] = (open(pn).read().strip().splitlines()[0], os.path.join(PK, g, "asset"))
def ydocs(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    docs = {}
    for m in re.finditer(r"^--- !u!(\d+) &(-?\d+).*?$\n(.*?)(?=^--- |\Z)", t, re.S | re.M):
        try: d = yaml.safe_load(m.group(3))
        except Exception: continue
        if isinstance(d, dict): docs[int(m.group(2))] = (int(m.group(1)), list(d.values())[0])
    return docs
# --- egriler
def curve_eval(c, x):
    ks = c.get("m_Curve") or []
    if not ks: return 1.0
    ts = [k["time"] for k in ks]; vs = [k["value"] for k in ks]
    return float(np.interp(x, ts, vs))
def mm(c, t=0.0, rnd=None):
    """MinMaxCurve: t = normalize zaman (0-1)"""
    if c is None: return 0.0
    s = c.get("minMaxState", 0); sc = c.get("scalar", 0.0)
    rnd = np.random.random() if rnd is None else rnd
    if s == 0: return sc
    if s == 1: return sc * curve_eval(c["maxCurve"], t)
    if s == 2: return sc * (curve_eval(c["minCurve"], t) * (1 - rnd) + curve_eval(c["maxCurve"], t) * rnd)
    if s == 3: return c.get("minScalar", 0.0) * (1 - rnd) + sc * rnd
    return sc
def col(d): return np.array([d["r"], d["g"], d["b"], d["a"]], np.float32)
def grad_eval(g, t):
    nc, na = g.get("m_NumColorKeys", 2), g.get("m_NumAlphaKeys", 2)
    ck = [(g.get("ctime%d" % i, 0) / 65535, col(g["key%d" % i])[:3]) for i in range(nc)]
    ak = [(g.get("atime%d" % i, 0) / 65535, g["key%d" % i]["a"]) for i in range(na)]
    rgb = np.array([np.interp(t, [k[0] for k in ck], [k[1][j] for k in ck]) for j in range(3)])
    a = np.interp(t, [k[0] for k in ak], [k[1] for k in ak])
    return np.array([*rgb, a], np.float32)
def mmg(c, t=0.0, rnd=None):
    s = c.get("minMaxState", 0); rnd = np.random.random() if rnd is None else rnd
    if s == 0: return col(c["maxColor"])
    if s == 1: return grad_eval(c["maxGradient"], t)
    if s == 2: return col(c["minColor"]) * (1 - rnd) + col(c["maxColor"]) * rnd
    if s == 3: return grad_eval(c["minGradient"], t) * (1 - rnd) + grad_eval(c["maxGradient"], t) * rnd
    return grad_eval(c["maxGradient"], rnd)
# --- materyal -> (doku RGBA float, renk carpani, eklemeli mi)
TEXC, MATC = {}, {}
BUILTIN = {200: "Particles/Additive", 201: "Particles/~Additive-Multiply", 202: "Particles/Additive (Soft)", 203: "Particles/Alpha Blended", 10720: "Mobile/Particles/Additive"}
def texture(guid):
    if guid in TEXC: return TEXC[guid]
    im = None
    if guid in G:
        try: im = np.asarray(Image.open(G[guid][1]).convert("RGBA"), np.float32) / 255
        except Exception: im = None
    TEXC[guid] = im; return im
def material(ref):
    key = ref.get("guid")
    if key in MATC: return MATC[key]
    res = (None, np.ones(4, np.float32), True)
    if key in G:
        md = ydocs(G[key][1]); m = next((v for k, (cid, v) in md.items() if cid == 21), None)
        if m:
            sh = m.get("m_Shader", {}); shn = ""
            if sh.get("guid") in G: shn = os.path.basename(G[sh["guid"]][0])
            else: shn = BUILTIN.get(sh.get("fileID"), "")
            add = bool(re.search(r"(?i)add", shn)) and not re.search(r"(?i)blend|alpha", shn)
            tex, tint = None, np.ones(4, np.float32)
            for e in m["m_SavedProperties"].get("m_TexEnvs", []):
                k, v = list(e.items())[0]
                if k in ("_MainTex", "_BaseMap", "_MainTexture") and v["m_Texture"].get("guid"): tex = texture(v["m_Texture"]["guid"])
            for e in m["m_SavedProperties"].get("m_Colors", []):
                k, v = list(e.items())[0]
                if k in ("_TintColor", "_Color", "_BaseColor"): tint = col(v) * (2.0 if k == "_TintColor" else 1.0)
            res = (tex, tint, add)
    MATC[key] = res; return res
# --- parcacik sistemi simulasyonu
def simulate(ps, rend, pos, scl, T, dt, rng):
    main = ps.get("InitialModule", {}); em = ps.get("EmissionModule", {}); sh = ps.get("ShapeModule", {})
    dur = ps.get("lengthInSec", 1.0); delay = mm(ps.get("startDelay"), 0, 0.5) if ps.get("startDelay") else 0.0
    loop = ps.get("looping", 0); maxp = main.get("maxNumParticles", 1000)
    tex, tint, add = material(rend["m_Materials"][0]) if rend and rend.get("m_Materials") and rend["m_Materials"][0].get("guid") else (None, np.ones(4, np.float32), True)
    rmode = rend.get("m_RenderMode", 0) if rend else 0; lscale = rend.get("m_LengthScale", 2) if rend else 2
    uv = ps.get("UVModule", {}); tx = uv.get("tilesX", 1) if uv.get("enabled") else 1; ty = uv.get("tilesY", 1) if uv.get("enabled") else 1
    size_m, col_m, rot_m = ps.get("SizeModule", {}), ps.get("ColorModule", {}), ps.get("RotationModule", {})
    parts = []; frames = []; acc = 0.0; bursts_done = set(); t = 0.0
    bursts = em.get("m_Bursts", []) if em.get("enabled") else []
    for fi in range(int(T / dt)):
        t = fi * dt; lt = t - delay
        if lt >= 0 and (loop or lt <= dur):
            tn = (lt % dur) / dur if dur else 0
            n = 0
            if em.get("enabled"):
                acc += mm(em.get("rateOverTime"), tn) * dt; n = int(acc); acc -= n
                for bi, b in enumerate(bursts):
                    bt = b.get("time", 0)
                    if bi not in bursts_done and lt >= bt: bursts_done.add(bi); n += int(round(mm(b.get("countCurve"), 0)))
            for _ in range(n):
                if len(parts) >= maxp: break
                r = rng.random()
                life = max(mm(main.get("startLifetime"), tn, r), 1e-3)
                spd = mm(main.get("startSpeed"), tn, rng.random())
                sz = mm(main.get("startSize"), tn, rng.random())
                c0 = mmg(main.get("startColor"), tn, rng.random())
                rot = mm(main.get("startRotation"), tn, rng.random())
                p0 = np.zeros(3); d = np.array([0, 0, 1.0])
                if sh.get("enabled"):
                    typ = sh.get("type", 4); rad = sh.get("radius", {}).get("value", sh.get("radius", 1)) if isinstance(sh.get("radius"), dict) else sh.get("radius", 1)
                    v = rng.normal(size=3); v /= np.linalg.norm(v) + 1e-9
                    if typ in (0, 1, 2):          # sphere / hemisphere
                        if typ == 2 and v[2] < 0: v[2] = -v[2]
                        p0 = v * rad * (rng.random() ** (1 / 3) if typ != 1 else 1); d = v
                    elif typ in (4, 5, 7, 8):     # cone
                        a = math.radians(sh.get("angle", 25)); ph = rng.random() * 2 * math.pi; rr = rad * math.sqrt(rng.random())
                        p0 = np.array([rr * math.cos(ph), rr * math.sin(ph), 0]); th = a * (rr / max(rad, 1e-6))
                        d = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)])
                    elif typ in (10, 12, 17):     # circle / edge / donut (xy duzlemi)
                        ph = rng.random() * 2 * math.pi; p0 = np.array([math.cos(ph), math.sin(ph), 0]) * rad; d = p0 / (rad + 1e-9)
                    elif typ in (5, 13):          # box
                        p0 = (rng.random(3) - 0.5) * 1.0; d = np.array([0, 0, 1.0])
                parts.append(dict(p=p0 * scl + pos, v=d * spd * scl, life=life, age=0.0, sz=sz * scl, c=c0, rot=rot,
                                  av=mm(rot_m.get("curve"), 0, rng.random()) if rot_m.get("enabled") else 0.0, rs=rng.random()))
        snap = []
        for q in parts:
            q["age"] += dt; q["p"] = q["p"] + q["v"] * dt; q["rot"] += q["av"] * dt
            if q["age"] >= q["life"]: continue
            u = q["age"] / q["life"]
            s = q["sz"] * (mm(size_m.get("curve"), u, q["rs"]) if size_m.get("enabled") else 1.0)
            c = q["c"] * (mmg(col_m.get("gradient"), u, q["rs"]) if col_m.get("enabled") else 1.0) * tint
            fr = 0
            if tx * ty > 1: fr = int(mm(uv.get("frameOverTime"), u, q["rs"]) * tx * ty) % (tx * ty) if uv.get("frameOverTime") else int(u * tx * ty) % (tx * ty)
            snap.append((q["p"].copy(), q["v"].copy(), s, c, q["rot"], fr))
        parts = [q for q in parts if q["age"] < q["life"]]
        frames.append(snap)
    return frames, dict(tex=tex, add=add, rmode=rmode, lscale=lscale, tx=tx, ty=ty)
def render(all_frames, W=360, H=360, ext=2.0):
    out = []
    ppu = W / (2 * ext)
    for fi in range(len(all_frames[0][0]) if all_frames else 0):
        L = np.zeros((H, W, 3), np.float32); A = np.zeros((H, W, 3), np.float32)
        for frames, info in all_frames:
            tex = info["tex"]
            for (p, v, s, c, rot, fr) in frames[fi]:
                px, py = W / 2 + p[0] * ppu, H / 2 - p[1] * ppu
                half = max(s * ppu / 2, 0.5)
                sx = sy = half; ang = rot
                if info["rmode"] == 1:           # stretched: hiz yonunde uzat
                    vv = math.hypot(v[0], v[1]); sy = half; sx = half * max(info["lscale"], 1) + vv * ppu * 0.02
                    ang = -math.atan2(v[1], v[0])
                R = int(math.ceil(max(sx, sy) * 1.5)) + 1
                x0, x1, y0, y1 = int(px - R), int(px + R) + 1, int(py - R), int(py + R) + 1
                if x1 <= 0 or y1 <= 0 or x0 >= W or y0 >= H: continue
                xs = np.arange(max(x0, 0), min(x1, W)); ys = np.arange(max(y0, 0), min(y1, H))
                X, Y = np.meshgrid(xs - px, ys - py); ca, sa = math.cos(ang), math.sin(ang)
                u = (X * ca + Y * sa) / (2 * sx) + 0.5; w = (-X * sa + Y * ca) / (2 * sy) + 0.5
                inside = (u >= 0) & (u < 1) & (w >= 0) & (w < 1)
                if not inside.any(): continue
                if tex is not None:
                    th, tw = tex.shape[:2]; fx, fy = fr % info["tx"], fr // info["tx"]
                    cu = ((fx + np.clip(u, 0, 0.999)) / info["tx"] * tw).astype(int); cv = ((fy + np.clip(w, 0, 0.999)) / info["ty"] * th).astype(int)
                    cv = np.clip(cv, 0, th - 1); cu = np.clip(cu, 0, tw - 1)
                    t = tex[cv, cu]
                else:
                    rr = np.hypot(u - 0.5, w - 0.5) * 2; t = np.dstack([np.ones_like(rr)] * 3 + [np.clip(1 - rr, 0, 1)])
                rgb = t[..., :3] * c[:3]; a = t[..., 3] * c[3] * inside
                sl = (slice(ys[0], ys[-1] + 1), slice(xs[0], xs[-1] + 1))
                if info["add"]: L[sl] += rgb * a[..., None]
                else: A[sl] = A[sl] * (1 - a[..., None]) + rgb * a[..., None]
        out.append(np.clip(A + L, 0, 1))
    return out
# --- prefab'lar
pre = sorted([(p, f) for g, (p, f) in G.items() if p.endswith(".prefab")])
import subprocess, tempfile, shutil
ozet = []
for path, f in pre:
    ad = os.path.basename(path)[:-7]; D = ydocs(f)
    go = {k: v for k, (c, v) in D.items() if c == 1}; tr = {k: v for k, (c, v) in D.items() if c == 4}
    pss = {k: v for k, (c, v) in D.items() if c == 198}; rs = {k: v for k, (c, v) in D.items() if c == 199}
    def world(tid):
        p = np.zeros(3); s = np.ones(3)
        while tid and tid in tr:
            t = tr[tid]; lp = t.get("m_LocalPosition", {}); ls = t.get("m_LocalScale", {})
            p = p * np.array([ls.get("x", 1), ls.get("y", 1), ls.get("z", 1)]) + np.array([lp.get("x", 0), lp.get("y", 0), lp.get("z", 0)])
            s = s * np.array([ls.get("x", 1), ls.get("y", 1), ls.get("z", 1)]); tid = t.get("m_Father", {}).get("fileID")
        return p, float(np.mean(s))
    rng = np.random.default_rng(1); af = []; T = 0; dt = 1 / 30
    if not pss: continue
    for pk, ps in pss.items():                                  # sure: tek seferlik (loop olmayan) sistemlere gore; loop'lu ortam parcaciklari bu surede oynar
        if not ps.get("looping", 0):
            T = max(T, (ps.get("startDelay", {}) or {}).get("scalar", 0) + ps.get("lengthInSec", 1) + ps.get("InitialModule", {}).get("startLifetime", {}).get("scalar", 1) + 0.25)
    T = min(max(T, 0.8), 2.5) if T else 1.5
    for pk, ps in pss.items():
        gid = ps["m_GameObject"]["fileID"]; trid = next((k for k, t in tr.items() if t["m_GameObject"]["fileID"] == gid), None)
        r = next((v for v in rs.values() if v["m_GameObject"]["fileID"] == gid), None)
        if r is None or not r.get("m_Enabled", 1) or not go.get(gid, {}).get("m_IsActive", 1): continue   # kapali renderer / pasif nesne: oyunda gorunmez
        pos, sc = world(trid)
        fr, info = simulate(ps, r, pos, sc, T, dt, rng); info["loop"] = bool(ps.get("looping", 0)); af.append((fr, info))
    # kapsam
    pts = [abs(p[i]) + s * 0.5 for fr, inf in af if not inf["loop"] for snap in fr for (p, v, s, c, r_, f_) in snap for i in (0, 1)] or \
          [abs(p[i]) + s * 0.5 for fr, inf in af for snap in fr for (p, v, s, c, r_, f_) in snap for i in (0, 1)]
    ext = max(0.6, min(np.percentile(pts, 98) * 1.1 if pts else 1.5, 8))
    imgs = render(af, ext=ext)
    td = tempfile.mkdtemp()
    for i, im in enumerate(imgs): Image.fromarray((im * 255).astype(np.uint8)).save(os.path.join(td, "k_%03d.png" % i))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", td + "/k_%03d.png", "-vf", "split[a][b];[a]palettegen[p];[b][p]paletteuse", "-loop", "0", os.path.join(OUT, ad + ".gif")], check=True)
    best = max(range(max(1, int(len(imgs) * 0.6))), key=lambda i: imgs[i].sum()); Image.fromarray((imgs[best] * 255).astype(np.uint8)).save(os.path.join(OUT, ad + "_doruk.png"))
    shutil.rmtree(td); ozet.append((ad, len(pss), round(T, 2), round(ext, 2))); print(ad, len(pss), "sistem", round(T, 2), "sn", flush=True)
open(os.path.join(OUT, "ozet.txt"), "w").write("\n".join("%s\t%d sistem\t%.2f sn\tgorus +-%.2f birim" % o for o in ozet))

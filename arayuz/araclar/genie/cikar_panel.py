#!/usr/bin/env python3
"""Knight Genie paneli (sag ust): opak HUD ogesi. Alfa = sahne degistigi halde AYNI kalan pikseller
(g_once, g_aktif ve gorev kayitlarindaki q_once: uc farkli sahne). Renk g_once'dan.
Degisen yazilar (Time Left, Ares - 1, CR : ..., Channel 2) silinir: ayni satirin gercek dokusundan doldurulur."""
import json, numpy as np
from scipy import ndimage
from PIL import Image
from ortak import *
PX,PY,PX1,PY1=2308,50,2664,296
def kes(ad,kok=REF): 
    return np.asarray(Image.open(os.path.join(kok,ad+".jpg")).convert("RGB")).astype(float)[PY:PY1,PX:PX1]
G=os.path.join(REF,"..","gorev")
I=[kes("g_once"),kes("g_aktif"),kes("q_once",G),kes("q_open",G)]
d=np.max([np.abs(I[0]-I[k]).max(2) for k in range(1,4)],0)
al=np.clip(1-(d-14)/26.0,0,1)
al=ndimage.median_filter(al,3)
P=I[0].copy()
def satir_doldur(x0,y0,x1,y1,esik=28,mod="kaydir"):
    """Yazi blogunu (cekirdek yazi maskesinin sutun/satir kapsami) ayni satirlarin temiz kismindan
    kesintisiz bir seritle degistirir; seritler kenarda 5 px harmanlanir."""
    a,b,c,e=x0-PX,y0-PY,x1-PX,y1-PY
    blok=P[b:e,a:c].copy(); lum=blok.mean(2)
    med=np.median(lum,1,keepdims=True)
    cek=(lum-med)>esik                                  # parlak yazi cekirdegi
    cek[:, :3]=False; cek[:,-3:]=False
    if not cek.any(): return
    ys,xs=np.nonzero(cek); r0,r1=max(0,ys.min()-3),min(blok.shape[0],ys.max()+4)
    c0,c1=max(3,xs.min()-5),min(blok.shape[1]-3,xs.max()+6)
    if mod=="medyan":
        for r in range(r0,r1):
            m=np.zeros(blok.shape[1],bool); m[c0:c1]=True
            blok[r,m]=np.median(blok[r,~m],0)
    else:
        w=c1-c0; temiz=list(range(3,c0))[::-1]+list(range(c1,blok.shape[1]-3))   # once sol (aynali), sonra sag
        for i,x in enumerate(range(c0,c1)):
            k=temiz[i%len(temiz)] if i<w//2 else temiz[::-1][(c1-1-x)%len(temiz)]
            blok[r0:r1,x]=P[b+r0:b+r1,a+k]
        for x,t in ((c0,1),(c1-1,-1)):                     # kenar harmanlama
            for j in range(5):
                f=(j+1)/6.0; xx=x+t*j
                blok[r0:r1,xx]=f*blok[r0:r1,xx]+(1-f)*P[b+r0:b+r1,a+xx-t*(5-j)] if 0<=xx-t*(5-j)<blok.shape[1] else blok[r0:r1,xx]
    # dikey ek: yazinin ust/alt satirlarina gecis
    P[b:e,a:c]=blok
YAZI=dict(sure=(2356,129,2650,150),sunucu=(2356,152,2652,186),cr=(2356,198,2652,232),kanal=(2356,247,2652,284))
satir_doldur(*YAZI["sure"],esik=40,mod="medyan")
for k in ("sunucu","cr","kanal"): satir_doldur(*YAZI[k],esik=22)
for k,(x0,y0,x1,y1) in YAZI.items(): al[y0-PY-2:y1-PY+2,x0-PX-4:x1-PX+4]=1.0   # dolu dikdortgen cubuklar (opak)
yaz("genie_panel",np.dstack([P,al*255]))
json.dump(dict(panel=[PX,PY,PX1-PX,PY1-PY],yazi_kutulari=YAZI,
               dugmeler=dict(baslat=[2350,61,70,66],durdur=[2425,61,70,66],ac=[2500,61,68,66])),
          open(os.path.join(OUT,"..","panel_olculer.json"),"w"),indent=1)
print("panel",P.shape)

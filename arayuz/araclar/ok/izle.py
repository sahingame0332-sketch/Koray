#!/usr/bin/env python3
"""Ok izleme: kayit 60 kare/sn (cogu kare tekrar: gercek ~30). Zemin = penceredeki karelerin medyani (ok her pikselde kisa kalir).
Ok pikselleri: zeminden farkli + acik renk (min kanal > 120) + ince uzun bilesen. Uc = hedef yonundeki en uzak nokta.
Kullanim: izle.py KARE_KLASORU"""
import sys, glob, json, numpy as np
from PIL import Image
from scipy import ndimage
fs=sorted(glob.glob(sys.argv[1]+'/k_*.png'))
Y=lambda i: np.asarray(Image.open(fs[i]).convert('RGB')).astype(np.float32)
X0,Y0,X1,Y1=0,150,1500,990
def olc(i0,i1):
    S=np.stack([Y(i)[Y0:Y1,X0:X1] for i in range(i0,i1)]); B=np.median(S,0); sonuc=[]
    for k,i in enumerate(range(i0,i1)):
        D=np.abs(S[k]-B).max(2); m=(D>45)&(S[k].min(2)>110)
        m=ndimage.binary_opening(m,np.ones((2,2)))
        l,n=ndimage.label(m)
        if not n: sonuc.append((i,None)); continue
        best=None
        for j in range(1,n+1):
            ys,xs=np.nonzero(l==j)
            if len(xs)<15: continue
            # ince-uzun: PCA oran
            c=np.cov(np.vstack([xs,ys])); ev=np.sort(np.linalg.eigvalsh(c))
            uzun=np.sqrt(ev[1]); oran=np.sqrt(ev[1]/max(ev[0],1e-3))
            if oran>5 and uzun>12 and (best is None or len(xs)>best[0]): best=(len(xs),xs,ys,uzun,oran)
        if best is None: sonuc.append((i,None)); continue
        _,xs,ys,uzun,oran=best; k_=np.argmin(xs)          # ok sola gidiyor: uc = en soldaki
        sonuc.append((i,dict(uc=[int(xs[k_]+X0),int(ys[k_]+Y0)],kuyruk=[int(xs.max()+X0),int(ys[np.argmax(xs)]+Y0)],
                              uzunluk=round(float(xs.max()-xs.min()),1),piksel=len(xs))))
    return sonuc
r=olc(int(sys.argv[2]),int(sys.argv[3]))
for i,v in r:
    print(i,v)

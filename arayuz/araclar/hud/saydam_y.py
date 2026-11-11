#!/usr/bin/env python3
"""Yatay kenar icin zemin alfasi: sutun sutun, kenarin ustundeki dunya ile
panelin icindeki bos zemin karsilastirilir.  o = (1-a)*b  ->  alfa = 1 - o/b
Kullanim: saydam_y.py  DIS_Y0 DIS_Y1  IC_Y0 IC_Y1  X0 X1  [kare...]
"""
import sys, numpy as np
from PIL import Image
P="/home/user/Koray/arayuz/referans_gorseller/hud_ekranlar/hud_%02d.png"
dy0,dy1,iy0,iy1,x0,x1=map(int,sys.argv[1:7])
kare=[int(k) for k in sys.argv[7:]] or [1,2,3,4]
ts=[]
for k in kare:
    a=np.asarray(Image.open(P%k).convert("RGB")).astype(float)
    for x in range(x0,x1):
        d=a[dy0:dy1,x].mean(axis=1); i=a[iy0:iy1,x].mean(axis=1)
        if d.max()>248 or d.std()>12: continue
        dm=float(np.median(d))
        if dm<35: continue
        ts.append(float(np.percentile(i,10))/dm)
t=np.array(ts)
print("ornek sutun : %d"%len(t))
print("gecirgenlik : t=%.4f  (ceyrekler %.4f - %.4f)"%(np.median(t),np.percentile(t,25),np.percentile(t,75)))
print("ZEMIN ALFASI: %.3f"%(1-np.median(t)))

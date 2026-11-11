#!/usr/bin/env python3
"""Iki komsu dikdortgenin 4 karedeki ortalama parlaklik orani -> t, alfa=1-t.
Her iki tarafta da ayni istatistik (ortalama) kullanilir; bolgeler yazisiz secilmelidir."""
import sys, numpy as np
from PIL import Image
P="/home/user/Koray/arayuz/referans_gorseller/hud_ekranlar/hud_%02d.png"
def oran(ad,ic,dis,kare=(1,2,3,4)):
    ts=[]
    for k in kare:
        a=np.asarray(Image.open(P%k).convert("RGB")).astype(float)
        o=a[ic[1]:ic[3],ic[0]:ic[2]].mean(); b=a[dis[1]:dis[3],dis[0]:dis[2]].mean()
        ts.append(o/b)
    ts=np.array(ts)
    print("%-26s t=%.3f +-%.3f  -> ALFA %.3f   (kareler: %s)"%(
        ad,ts.mean(),ts.std(),1-ts.mean()," ".join("%.3f"%v for v in ts)))
    return 1-ts.mean()
if __name__=="__main__":
    oran("sohbet sag panel A",(1180,1040,1340,1318),(1380,1040,1540,1318))
    oran("sohbet sag panel B",(1180,1150,1340,1318),(1380,1150,1540,1318))
    oran("sohbet sol panel",  (640,1240,800,1316),  (640,1345,800,1400))
    oran("bildirim cubugu",   (700,924,760,972),    (830,924,890,972))

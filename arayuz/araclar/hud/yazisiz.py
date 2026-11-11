#!/usr/bin/env python3
"""Sprite'lardan yaziyi siler: yazi kutusunun solundaki ve sagindaki temiz
seritlerin satir medyanlari arasinda dogrusal gecisle doldurur."""
import os, numpy as np
from PIL import Image
S="/home/user/Koray/arayuz/kaynak/hud/sprites"
def sil(ad, kutular, cikti=None, serit=10):
    im=Image.open(os.path.join(S,ad+".png")); mod=im.mode
    a=np.asarray(im.convert("RGBA")).astype(float)
    for (x0,y0,x1,y1) in kutular:
        sl=max(0,x0-serit); sr=min(a.shape[1],x1+serit)
        for y in range(y0,y1):
            L=np.median(a[y,sl:x0,:3],axis=0) if x0>sl else np.median(a[y,x1:sr,:3],axis=0)
            R=np.median(a[y,x1:sr,:3],axis=0) if sr>x1 else L
            n=x1-x0
            for i in range(n):
                t=(i+0.5)/n
                a[y,x0+i,:3]=L*(1-t)+R*t
    out=cikti or (ad+"_yazisiz")
    Image.fromarray(a.astype(np.uint8),"RGBA").convert(mod).save(os.path.join(S,out+".png"))
    return out
# sag ust paneller: yazi ortada, kenarlar temiz
sil("panel_diez",[(40,6,290,40)])
sil("panel_cr",[(30,6,300,40)])
sil("panel_aktif_etkinlik",[(60,4,280,40)])
sil("panel_kanal",[(40,6,290,44)])
sil("cubuk_timeleft",[(35,2,290,23)])
# sekmeler
sil("sekme_normal",[(20,8,131,40)])
sil("sekme_secili",[(20,8,133,40)])
sil("sekme_notices",[(30,8,147,40)])
sil("panel_information",[(12,4,215,34)])
print("yazisiz sprite'lar hazir")

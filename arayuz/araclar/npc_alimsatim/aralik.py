#!/usr/bin/env python3
"""Punto + harf araligi birlikte: Roboto Slab Bold'u (p, aralik) ile cizip orijinal murekle IoU (en iyi kaydirma ile)."""
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from scipy import ndimage
SB='/home/user/Koray/arayuz/kaynak/char_info/fonts/RobotoSlab-Bold.ttf'
R='/home/user/Koray/arayuz/referans_gorseller/npc_alimsatim/'
def murek(m):
    ys,xs=np.nonzero(m); return m[ys.min():ys.max()+1,xs.min():xs.max()+1]
def ciz(t,p,s):
    f=ImageFont.truetype(SB,p); im=Image.new('L',(900,120),0); d=ImageDraw.Draw(im); x=20.0
    for ch in t: d.text((x,30),ch,font=f,fill=255); x+=f.getlength(ch)+s
    return murek(np.asarray(im)>110)
def iou(a,b):
    h=max(a.shape[0],b.shape[0])+4; w=max(a.shape[1],b.shape[1])+4; best=0
    for dy in range(-2,3):
        for dx in range(-3,4):
            A=np.zeros((h+8,w+8),bool); B=np.zeros((h+8,w+8),bool)
            A[4:4+a.shape[0],4:4+a.shape[1]]=a; B[4+dy:4+dy+b.shape[0],4+dx:4+dx+b.shape[1]]=b
            best=max(best,(A&B).sum()/(A|B).sum())
    return best
for ad,t,k,kutu in (("baslik","Holy water","al_adet",(1900,556,2065,592)),("need","Need Money : 70","al_para",(1868,590,2102,624)),
                    ("buy","Buy Item Count:","al_adet",(1870,592,2100,624)),("earn","Earn Money : 33","sat_para",(1866,592,2096,624))):
    O=np.asarray(Image.open(R+k+'.jpg')).astype(float)[kutu[1]:kutu[3],kutu[0]:kutu[2]]
    h=murek(O.min(2)>110)
    r=sorted(((iou(h,ciz(t,p,s)),p,s) for p in range(23,30) for s in np.arange(0,3.01,0.5)),reverse=True)[:3]
    print(ad,h.shape,[(round(v,3),p,s) for v,p,s in r])

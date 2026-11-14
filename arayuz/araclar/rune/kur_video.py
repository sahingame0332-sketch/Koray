#!/usr/bin/env python3
"""Alevli run halkasini kullanicinin kaydindaki karakterin (xDarKPasT) altina yerlestirir.
Kare: 56_skill_alinan_hasar.mp4, 0.5 sn (2266x1488 tablet). Karakter ~110 px (y 740-850), ayak (1130,848).
Perspektif basiklik: ayni karedeki mob secim halkasindan (245 x 120) -> 0.47. Cap = 1.6 x karakter boyu = 176 px; alevler yere yakin (duvar 0.12 x cap).
Yuz kamerasi bolgesi (sol ust) kirpilir; tam kare depoya konmaz. Kullanim: kur_video.py KARE.png"""
import sys, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
kod=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"kur.py")).read().split("S=np.asarray")[0]
exec(kod)
S=np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(float)
MERKEZ=(1130,846); CAP=176; BASIK=0.47      # cap 1.6 x karakter boyu (110 px)
yy,xx=np.mgrid[0:S.shape[0],0:S.shape[1]]
kutu=(xx>=1078)&(xx<=1182)&(yy>=735)&(yy<=858)
lum=S.mean(2); cim=(lum<85)&(np.abs(S[...,0]-S[...,1])<35)
kar=kutu&~cim
kar=ndimage.binary_opening(kar,np.ones((2,2))); kar=ndimage.binary_fill_holes(ndimage.binary_closing(kar,np.ones((5,5))))
kar=ndimage.gaussian_filter(kar.astype(float),0.8)[...,None]
YOGUNLUK=0.5      # genel parlaklik (eklemeli: dusuk = daha saydam); karakterin onune gecmesin
def bindir(t,g):
    g=g*YOGUNLUK
    h=int(CAP*BASIK); e=Image.fromarray((np.clip(kare(t,512,g),0,1)*255).astype(np.uint8)).resize((CAP,h),Image.LANCZOS)
    e=np.asarray(e).astype(float); O=S.copy(); x0=int(MERKEZ[0]-CAP/2); y0=int(MERKEZ[1]-h/2)
    O[y0:y0+h,x0:x0+CAP]+=e
    D=duvar(t,CAP,BASIK,g,S.shape[1],S.shape[0],MERKEZ)
    # arka yari duvar + zemin halkasi karakterin ARKASINDA; karakterin onunden gecen on yari icin kaba ayrim:
    on=(yy>MERKEZ[1])[...,None]                       # ayak cizgisinin alti = on taraf
    O=O+D*(1-on)
    O=O*(1-kar)+S*kar                                  # karakter zemin + arka duvarin onunde
    O=O+D*on                                           # on duvar karakterin onunde
    return np.clip(O,0,255)
KIRP=(860,600,1400,905)
zam=[0.15,0.6,1.2,2.4]; guc=[0.5,1,1,0.4]
ims=[Image.fromarray(bindir(t,g).astype(np.uint8)).crop(KIRP) for t,g in zip(zam,guc)]
orj=Image.fromarray(S.astype(np.uint8)).crop(KIRP)
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf"),20)
w,h=orj.size; c=Image.new("RGB",(w*2+10,(h+34)*2+44+h+34),(24,24,28)); d=ImageDraw.Draw(c)
d.text((8,8),"xDarKPasT + alevli run halkasi (kayit karesi 0.5 sn uzerine)",font=F,fill=(255,220,120))
buyuk=Image.fromarray(bindir(1.2,1).astype(np.uint8)).crop(KIRP)
c.paste(orj,(0,44+22)); d.text((6,44),"ORIJINAL KARE",font=F,fill=(200,200,200))
c.paste(buyuk,(w+10,44+22)); d.text((w+16,44),"EFEKTLI (1.2 sn)",font=F,fill=(140,230,140))
for i,(im,t) in enumerate(zip(ims,zam)):
    X=(i%2)*(w+10); Y=44+(h+34)*(1+i//2)+22; c.paste(im,(X,Y)); d.text((X+6,Y-22),"%.2f sn"%t,font=F,fill=(255,255,0))
c.save(os.path.join(ONZ,"rune_karakter.png")); buyuk.resize((w*2,h*2),Image.LANCZOS).save(os.path.join(ONZ,"rune_karakter_buyuk.png")); print(c.size)

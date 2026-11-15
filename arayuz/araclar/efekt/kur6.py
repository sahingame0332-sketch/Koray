#!/usr/bin/env python3
"""Altinci set dogrulamasi: zemin (efekt oncesi medyan) + karakter katmani + hedef katmani (eklemeli, kendi capalarinda) <-> orijinal.
Kullanim: kur6.py VIDEO -> onizlemeler/efekt6_onizleme.png, efekt6_animasyon.mp4/.gif"""
import os, sys, json, glob, subprocess, tempfile, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar6 import SKILL, KX, KY, KW, KH, kareler, Y
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
AD={"stroke":"Stroke","stab":"Stab","stab2":"Stab2"}
bil=json.load(open(os.path.join(K,"efekt_bilgisi.json")))
fs=kareler(sys.argv[1]); KIRP=(150,0,1450,1140)            # gosterim (calisma kutusu icinde)
def yeniden(ad,B,j):
    R=B.copy()
    for kn,kb in bil["yakin_"+ad]["katmanlar"].items():
        p=os.path.join(K,"yakin_%s_%s"%(ad,kn),"%s_%s_%02d.png"%(ad,kn,j))
        E=np.asarray(Image.open(p).convert("RGB")).astype(np.float32); x,y,w,h=kb["kutu_ekran"]
        R[y-KY:y-KY+h,x-KX:x-KX+w]+=E
    return np.clip(R,0,255)
satir=[]; ozet={}; anim={}
for ad,once,sonra,aralik,*_ in SKILL:
    B=np.median(np.stack([Y(fs[i]) for i in once]),0); n=len(aralik); sec=[int(round(k*(n-1)/5)) for k in range(6)]
    ww,hh=260,228; c=Image.new("RGB",(ww*6+110,hh*2+34),(24,24,28)); d=ImageDraw.Draw(c); hata=[]
    for t,j in enumerate(sec):
        O=Y(fs[aralik[j]]); R=yeniden(ad,B,j); hata.append(np.abs(R-O).mean())
        for s,A in enumerate((O,R)): c.paste(Image.fromarray(A.astype(np.uint8)).crop(KIRP).resize((ww,hh),Image.LANCZOS),(108+t*ww,34+s*hh))
        d.text((110+t*ww,36),"%.2f sn"%(j/30),font=F,fill=(255,255,0))
    ozet[ad]=round(float(np.mean(hata)),2)
    d.text((6,6),"%s — %d kare (30 kare/sn, %.2f sn) · ort. fark %.1f/255"%(AD[ad],n,n/30,ozet[ad]),font=F,fill=(255,220,120))
    d.text((6,34+hh//2),"ORİJİNAL",font=F,fill=(200,200,200)); d.text((6,34+hh+hh//2),"YENİ",font=F,fill=(140,230,140))
    satir.append(c); anim[ad]=(B,[Y(fs[i]) for i in aralik],n)
o=Image.new("RGB",(satir[0].width,sum(s.height+8 for s in satir)),(24,24,28)); yy=0
for s in satir: o.paste(s,(0,yy)); yy+=s.height+8
o.save(os.path.join(ONZ,"efekt6_onizleme.png")); print(ozet)
# hareketli: sol orijinal, sag yeni (zemin + katmanlar), uc skill arka arkaya
d=tempfile.mkdtemp(); t=0
for ad,(B,Os,n) in anim.items():
    for j in list(range(n))+[n-1]*10:
        O=Os[min(j,n-1)]; R=yeniden(ad,B,min(j,n-1)) if j<n else B
        a=Image.fromarray(O.astype(np.uint8)).crop(KIRP).resize((520,456),Image.LANCZOS); b=Image.fromarray(R.astype(np.uint8)).crop(KIRP).resize((520,456),Image.LANCZOS)
        c=Image.new("RGB",(1050,490),(24,24,28)); c.paste(a,(0,34)); c.paste(b,(530,34)); dr=ImageDraw.Draw(c)
        dr.text((6,6),AD[ad]+" — ORİJİNAL",font=F,fill=(200,200,200)); dr.text((536,6),AD[ad]+" — YENİ (zemin + efekt)",font=F,fill=(140,230,140))
        c.save(os.path.join(d,"a_%04d.png"%t)); t+=1
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","format=yuv420p","-c:v","libx264","-crf","20",os.path.join(ONZ,"efekt6_animasyon.mp4")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",d+"/a_%04d.png","-vf","fps=15,scale=840:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=160[p];[b][p]paletteuse=dither=bayer",os.path.join(ONZ,"efekt6_animasyon.gif")],check=True)
shutil.rmtree(d); json.dump(ozet,open(os.path.join(K,"efekt6_fark.json"),"w")); print(t,"kare")

#!/usr/bin/env python3
"""Efektlerin dogrulamasi: cikarilan kareler efektten onceki zemine EKLEMELI (Blend One One) bindirilir,
ayni anin orijinal karesiyle yan yana konur. Cikti: onizlemeler/efekt_onizleme.png"""
import os, sys, json, glob, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
def tum(video):
    d=tempfile.mkdtemp(); subprocess.run(["ffmpeg","-v","error","-y","-i",video,"-vsync","0",d+"/k_%04d.png"],check=True)
    return sorted(glob.glob(d+"/k_*.png"))
def Y(f): return np.asarray(Image.open(f).convert("RGB")).astype(np.float32)
v=sys.argv[1]; fs=tum(v); bil=json.load(open(os.path.join(K,"efekt_bilgisi.json")))
satir=[]
for ad,once,sec,olc in (("ates_sutunu",(96,110),[2,5,8,11,14,18,22],0.42),("vurus",(160,176),[1,2,4,6,8],0.62)):
    x,y,w,h=bil[ad]["ekran_kutu"]; i0,i1,adim=bil[ad]["kaynak_kareler"]
    B=np.median(np.stack([Y(fs[i]) for i in range(once[0],once[1],2)]),0)[y:y+h,x:x+w]
    ust=[];alt=[]; hata=[]
    for n in sec:
        O=Y(fs[i0+n*adim])[y:y+h,x:x+w]; E=Y(os.path.join(K,ad,"%s_%02d.png"%(ad,n)))
        R=np.clip(B+E,0,255)
        hata.append(np.abs(R-O).mean())
        ust.append(Image.fromarray(O.astype(np.uint8)).resize((int(w*olc),int(h*olc)))); alt.append(Image.fromarray(R.astype(np.uint8)).resize((int(w*olc),int(h*olc))))
    ww=ust[0].width; hh=ust[0].height
    c=Image.new("RGB",(ww*len(sec)+120,hh*2+40),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((8,4),"%s — üst: ORİJİNAL · alt: YENİ (zemin + eklemeli efekt)   ort. fark %.1f / 255"%(ad,np.mean(hata)),font=F,fill=(255,220,120))
    for i,(u,a) in enumerate(zip(ust,alt)):
        c.paste(u,(110+i*ww,34)); c.paste(a,(110+i*ww,34+hh))
        d.text((112+i*ww,36),"%.2f sn"%(sec[i]*adim/60.0),font=F,fill=(255,255,0))
    d.text((8,34+hh//2),"ORİJİNAL",font=F,fill=(200,200,200)); d.text((8,34+hh+hh//2),"YENİ",font=F,fill=(140,230,140))
    satir.append(c); print(ad,"ortalama mutlak fark %.2f"%np.mean(hata))
W=max(s.width for s in satir); o=Image.new("RGB",(W,sum(s.height+8 for s in satir)),(24,24,28)); yy=0
for s in satir: o.paste(s,(0,yy)); yy+=s.height+8
o.save(os.path.join(ONZ,"efekt_onizleme.png")); print(o.size)

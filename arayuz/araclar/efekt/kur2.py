#!/usr/bin/env python3
"""Ikinci efekt setinin dogrulamasi: zemin (efektten onceki karelerin medyani) + EKLEMELI efekt karesi
ile ayni anin orijinali yan yana; ucuncu satir efektin kendisi (siyah = saydam).
Kullanim: kur2.py VIDEO_A VIDEO_B  -> onizlemeler/efekt2_onizleme.png"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar2 import kareler
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
va,vb=sys.argv[1],sys.argv[2]; bil=json.load(open(os.path.join(K,"efekt_bilgisi.json")))
satir=[]
for ad,v,sec,olc,baslik in (("fire_burst",vb,[1,4,8,11,15,20,26],0.36,"Fire Burst (mob)"),
                            ("fire_blade",va,[1,3,5,7,9,12,15],0.40,"Fire Blade (mob)"),
                            ("vurus_tam",va,[0,2,4,6,8,11,14],0.56,"Karaktere vuruş (tam)")):
    b=bil[ad]; x,y,w,h=b["ekran_kutu"]; i0,i1,adim=b["kaynak_kareler"]
    idx=[i0+n*adim for n in sec]; Kd=kareler(v,(x,y,w,h),sorted(set(b["once"]+idx)))
    B=np.median(np.stack([Kd[i] for i in b["once"]]),0)
    sat=[[],[],[]]; hata=[]
    for n,i in zip(sec,idx):
        O=Kd[i]; E=np.asarray(Image.open(os.path.join(K,ad,"%s_%02d.png"%(ad,n))).convert("RGB")).astype(np.float32)
        R=np.clip(B+E,0,255); hata.append(np.abs(R-O).mean())
        for j,A in enumerate((O,R,E)): sat[j].append(Image.fromarray(A.astype(np.uint8)).resize((int(w*olc),int(h*olc))))
    ww,hh=sat[0][0].size
    c=Image.new("RGB",(ww*len(sec)+120,hh*3+40),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((8,4),"%s — %d kare, %.0f kare/sn · ort. fark (orijinal ↔ zemin+efekt) %.1f / 255"%(baslik,b["kare_sayisi"],b["fps"],np.mean(hata)),font=F,fill=(255,220,120))
    for k,(etk,renk) in enumerate((("ORİJİNAL",(200,200,200)),("YENİ",(140,230,140)),("EFEKT",(255,170,90)))):
        d.text((8,34+hh*k+hh//2),etk,font=F,fill=renk)
        for i,im in enumerate(sat[k]): c.paste(im,(110+i*ww,34+hh*k))
    for i,n in enumerate(sec): d.text((112+i*ww,36),"%.2f sn"%(n/b["fps"]),font=F,fill=(255,255,0))
    satir.append(c); print(ad,"ortalama mutlak fark %.2f"%np.mean(hata))
W=max(s.width for s in satir); o=Image.new("RGB",(W,sum(s.height+8 for s in satir)),(24,24,28)); yy=0
for s in satir: o.paste(s,(0,yy)); yy+=s.height+8
o.save(os.path.join(ONZ,"efekt2_onizleme.png")); print(o.size)

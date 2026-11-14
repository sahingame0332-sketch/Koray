#!/usr/bin/env python3
"""Manes Of Fire dogrulamasi: zemin (100-118 medyani) + eklemeli kare <-> orijinal; ucuncu satir efektin kendisi.
Kullanim: kur4.py VIDEO -> onizlemeler/efekt4_onizleme.png"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar2 import kareler
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),20)
b=json.load(open(os.path.join(K,"efekt_bilgisi.json")))["manes_of_fire"]; x,y,w,h=b["ekran_kutu"]; i0,_,adim=b["kaynak_kareler"]
sec=[0,4,8,12,16,20,26,32,38]; idx=[i0+n*adim for n in sec]
Kd=kareler(sys.argv[1],(x,y,w,h),sorted(set(b["once"]+idx))); B=np.median(np.stack([Kd[i] for i in b["once"]]),0)
olc=0.42; sat=[[],[],[]]; hata=[]
for n,i in zip(sec,idx):
    O=Kd[i]; E=np.asarray(Image.open(os.path.join(K,"manes_of_fire","manes_of_fire_%02d.png"%n)).convert("RGB")).astype(float)
    R=np.clip(B+E,0,255); hata.append(np.abs(R-O).mean())
    for j,A in enumerate((O,R,E)): sat[j].append(Image.fromarray(A.astype(np.uint8)).resize((int(w*olc),int(h*olc))))
ww,hh=sat[0][0].size; c=Image.new("RGB",(ww*len(sec)+110,hh*3+40),(24,24,28)); d=ImageDraw.Draw(c)
d.text((8,6),"Manes Of Fire (moba) — %d kare, 30 kare/sn · ort. fark (orijinal <-> zemin+efekt) %.1f / 255"%(b["kare_sayisi"],np.mean(hata)),font=F,fill=(255,220,120))
for k,(et,rk) in enumerate((("ORIJINAL",(200,200,200)),("YENI",(140,230,140)),("EFEKT",(255,170,90)))):
    d.text((6,34+hh*k+hh//2),et,font=F,fill=rk)
    for i,im in enumerate(sat[k]): c.paste(im,(105+i*ww,34+hh*k))
for i,n in enumerate(sec): d.text((108+i*ww,36),"%.2f sn"%(n/30),font=F,fill=(255,255,0))
c.save(os.path.join(ONZ,"efekt4_onizleme.png")); print("fark %.2f"%np.mean(hata),c.size)

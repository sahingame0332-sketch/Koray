#!/usr/bin/env python3
"""Besinci set dogrulamasi: her efekt icin zemin (efekt oncesi medyan) + eklemeli kare <-> orijinal; ucuncu satir efektin kendisi.
Kullanim: kur5.py KLASOR  -> onizlemeler/efekt5_onizleme.png (+ efekt5_<ad>.png)"""
import os, sys, json, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from cikar5 import KUTU, EFEKT, kareler, Y
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt"); ONZ=os.path.join(B_,"..","..","onizlemeler")
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),18)
AD={"dokum_yildizlari":"Döküm yıldızları (cast sırasında)","hide":"Hide","light_feet":"Light Feet","kedi_gozu":"Cat's / Lupine Eyes",
    "evade":"Evade","safety":"Safety","cure":"Cure Disease / Cure Curse","magic_shield":"Magic Shield",
    "sprint":"Sprint","swift":"Swift","strength_of_wolf":"Strength Of Wolf","minor_healing":"Minor Healing"}
x,y,w,h=KUTU; cache={}; satir=[]; ozet={}
for ad,v,once,aralik in EFEKT:
    if v not in cache: cache[v]=kareler(os.path.join(sys.argv[1],v+".mp4"))
    fs=cache[v][1]; aralik=[i for i in aralik if i<len(fs)]; B=np.median(np.stack([Y(fs[i]) for i in once]),0)
    n=len(aralik); sec=[int(round(k*(n-1)/5)) for k in range(6)]
    kirp=(150,250,600,800)                                   # gosterim: karakter cevresi (KUTU icinde)
    sat=[[],[],[]]; hata=[]
    for j in sec:
        O=Y(fs[aralik[j]]); E=np.asarray(Image.open(os.path.join(K,ad,"%s_%02d.png"%(ad,j))).convert("RGB")).astype(np.float32)
        R=np.clip(B+E,0,255); hata.append(np.abs(R-O)[200:860-50,100:620].mean())
        for t,A in enumerate((O,R,E)): sat[t].append(Image.fromarray(A.astype(np.uint8)).crop((100,150,620,860)).resize((182,249)))
    ozet[ad]=round(float(np.mean(hata)),2)
    ww,hh=182,249; c=Image.new("RGB",(ww*6+100,hh*3+30),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((6,5),"%s — %d kare, 30 kare/sn, %.1f sn · ort. fark %.1f/255"%(AD[ad],n,n/30,ozet[ad]),font=F,fill=(255,220,120))
    for t,(et,rk) in enumerate((("ORİJİNAL",(200,200,200)),("YENİ",(140,230,140)),("EFEKT",(255,170,90)))):
        d.text((6,30+hh*t+hh//2),et,font=F,fill=rk)
        for i,im in enumerate(sat[t]): c.paste(im,(98+i*ww,30+hh*t))
    for i,j in enumerate(sec): d.text((100+i*ww,32),"%.2f sn"%(j/30),font=F,fill=(255,255,0))
    c.save(os.path.join(ONZ,"efekt5_%s.png"%ad)); satir.append(c); print(ad,ozet[ad])
W=satir[0].width; o=Image.new("RGB",(W*2+10,(satir[0].height+8)*((len(satir)+1)//2)),(24,24,28))
for i,s in enumerate(satir): o.paste(s,((i%2)*(W+10),(i//2)*(s.height+8)))
o.save(os.path.join(ONZ,"efekt5_onizleme.png")); print(o.size)
json.dump(ozet,open(os.path.join(K,"efekt5_fark.json"),"w"))

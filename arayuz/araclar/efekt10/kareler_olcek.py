#!/usr/bin/env python3
"""Efekt 10 — karelerin efekt boyu (kullanici): kare 2 = kare 1'in %110'u; kare 3 = kare 2'nin %125'i (= kare 1'in %137.5'i).
Kaynak kareler 604x604 (kareler/kare_0N.png) olcekli tek tuvale (840x840, merkez ortada) yerlestirilir -> kareler/olcekli/kare_0N.png
Kare 4+ icin olcek kullanicidan gelince OLCEK'e eklenir."""
import os, numpy as np
from PIL import Image
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
OLCEK={1:1.0, 2:1.10, 3:1.10*1.25}          # kare 4 iptal (kullanici)
TUVAL=920
od=os.path.join(K,"olcekli"); os.makedirs(od,exist_ok=True)
ims=[]
for n,s in OLCEK.items():
    ad="kare_%02d.png"%n                       # kullanici: orijinal seftali renk (kirmizi surum kullanilmaz)
    im=Image.open(os.path.join(K,ad)).convert("RGBA")
    yeni=round(im.width*s); im=im.resize((yeni,yeni),Image.LANCZOS)
    t=Image.new("RGBA",(TUVAL,TUVAL),(0,0,0,0)); t.alpha_composite(im,((TUVAL-yeni)//2,(TUVAL-yeni)//2))
    t.save(os.path.join(od,"kare_%02d.png"%n)); ims.append(t)
o=Image.new("RGB",(len(ims)*(TUVAL//2)+20*(len(ims)-1),TUVAL),(20,20,24))
for j,t in enumerate(ims):
    for i,zr in enumerate(((255,255,255,255),(0,0,0,255))):
        z=Image.new("RGBA",t.size,zr); z.alpha_composite(t); o.paste(z.convert("RGB").resize((TUVAL//2,TUVAL//2)),(j*(TUVAL//2+20),i*(TUVAL//2)))
o.save(os.path.join(ONZ,"efekt10_kareler_olcekli.png")); print("tamam", {n:round(s,3) for n,s in OLCEK.items()})

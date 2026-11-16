#!/usr/bin/env python3
"""Efekt 8 karelerini iki katmana ayirir: ON = mob silueti icindeki isik (mobun onu), ARKA = siluet disi (siluet ici komsu isiktan
doldurulur; Unity'de mob orter). Toplam = cikar8 karesi. Cikti: kaynak/efekt8/skill_arka, skill_on (+ bilgi.json olculeri)."""
import os, sys, json, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
from cikar8 import OUT, KX, KY
b=json.load(open(os.path.join(OUT,"bilgi.json"))); rm=np.load(os.path.join(OUT,"mob_maskesi.npy"))
x,y,w,h=b["kutu_ekran"]; m=ndimage.binary_dilation(rm,np.ones((5,5)))[y-KY:y-KY+h,x-KX:x-KX+w]
for k in ("skill_arka","skill_on"):
    d=os.path.join(OUT,k); os.makedirs(d,exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d,f))
for n in range(b["kare"]):
    E=np.asarray(Image.open(os.path.join(OUT,"skill","skill_%02d.png"%n)).convert("RGB"),dtype=np.float32)
    on=np.where(m[...,None],E,0); ar=yumusak_doldur(np.where(m[...,None],0,E),m,n=14,k=15)
    Image.fromarray(np.clip(ar,0,255).round().astype(np.uint8)).save(os.path.join(OUT,"skill_arka","skill_arka_%02d.png"%n))
    Image.fromarray(np.clip(on,0,255).round().astype(np.uint8)).save(os.path.join(OUT,"skill_on","skill_on_%02d.png"%n))
print("tamam",b["kare"],"kare; kutu",b["kutu_ekran"],"pivot",b["pivot"],"genislik",b["genislik_mob_boyu"],"en_boy",b["en_boy"])

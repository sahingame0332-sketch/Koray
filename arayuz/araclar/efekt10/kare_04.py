#!/usr/bin/env python3
"""Efekt 10 — kare 4 (kullanici): kare 3 ile ayni; yalniz titanyum beyaz merkez kuculur. Efekt boyu kareler_olcek.py'de kare 3'un %110'u.
Merkez kucultme: parantezlerin icinde (R<170) yumusak radyal sikistirma — merkezde olcek K (0.65), R=170'te 1 (parantezler/disi aynen).
Cikti: kareler/kare_04.png (+ _siyah/_beyaz), onizlemeler/efekt10_kare_04.png"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
KUC,RM=0.65,170.0
a=np.asarray(Image.open(os.path.join(K,"kare_03.png")).convert("RGBA")).astype(np.float32)/255
L=a[...,:3]*a[...,3:4]; H,W=L.shape[:2]; cy,cx=(H-1)/2,(W-1)/2
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); dx,dy=xx-cx,yy-cy; R=np.hypot(dx,dy)
u=np.clip(1-R/RM,0,1); f=1+(1/KUC-1)*u*u*(3-2*u)                       # merkezde 1/KUC (kucuk gorunur), kenarda 1
T=np.stack([ndimage.map_coordinates(L[...,c],[cy+dy*f,cx+dx*f],order=1,mode="nearest") for c in range(3)],-1)
al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(K,"kare_04.png"))
im=Image.open(os.path.join(K,"kare_04.png"))
for ad,zr in (("siyah",(0,0,0,255)),("beyaz",(255,255,255,255))):
    z=Image.new("RGBA",im.size,zr); z.alpha_composite(im); z.convert("RGB").save(os.path.join(K,"kare_04_%s.png"%ad))
o=Image.new("RGB",(W*2+20,H),(20,20,24))
for i,ad in enumerate(("beyaz","siyah")): o.paste(Image.open(os.path.join(K,"kare_04_%s.png"%ad)),(i*(W+20),0))
o.save(os.path.join(ONZ,"efekt10_kare_04.png")); print("tamam")

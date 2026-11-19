#!/usr/bin/env python3
"""Efekt 10 — kare 1 ve 2: cekirdegin etrafi (titanyum beyaz ile parantez arasi seftali/somon/pembe katman) kirmiziya yakin renge cevrilir.
Parlaklik ve doku korunur (her pikselin en parlak kanali x hedef kirmizi); beyaz cekirdek, sari bant ve sari-yesil parantezler korunur.
Girdi: kareler/kare_01.png, kare_02.png (degismez)  Cikti: kareler/kare_01_kirmizi.png, kare_02_kirmizi.png"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler")
KIRMIZI=np.array([0xFF,0xA0,0xA0],np.float32)/255; GUC=0.85     # ilk iki resimdeki seftali-somon tonu (olculen oran 1 : 0.627 : 0.628)
for n in (1,2):
    a=np.asarray(Image.open(os.path.join(K,"kare_%02d.png"%n)).convert("RGBA")).astype(np.float32)/255
    L=a[...,:3]*a[...,3:4]; H,W=L.shape[:2]; cy,cx=(H-1)/2,(W-1)/2
    yy,xx=np.mgrid[0:H,0:W]; R=np.hypot(xx-cx,yy-cy)
    mx=np.maximum(L.max(2),1e-3)
    beyaz=np.clip((L.min(2)/mx-0.80)/0.12,0,1)*np.clip((mx-0.75)/0.15,0,1)          # titanyum / krem beyaz
    sari=np.clip((L[...,1]/mx-0.78)/0.10,0,1)*np.clip(1-L[...,2]/np.maximum(L[...,1],1e-3)*1.1,0,1)
    sari=np.maximum(sari,np.clip((L[...,1]-0.80*L[...,0])/0.12+0.5,0,1)*np.clip((R-165)/10,0,1))
    sarimsi=np.clip((L[...,1]/np.maximum(L[...,0],1e-3)-0.90)/0.05,0,1)*np.clip((0.86-L[...,2]/np.maximum(L[...,1],1e-3))/0.05,0,1)   # krem/sari bant
    sarimsi=ndimage.maximum_filter(sarimsi,3)
    bolge=np.clip((190-R)/14,0,1)*(1-np.clip(beyaz+sari+sarimsi,0,1))
    bolge=ndimage.gaussian_filter(bolge,1.5)*GUC
    hedef=mx[...,None]*KIRMIZI/KIRMIZI.max()
    T=L*(1-bolge[...,None])+hedef*bolge[...,None]
    al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
    Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(K,"kare_%02d_kirmizi.png"%n))
print("tamam")

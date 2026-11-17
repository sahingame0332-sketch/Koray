#!/usr/bin/env python3
"""Efekt 9 vurus -> renge gore iki tek basina efekt (kaynak kareler degismez):
  pembe : pembe-mor-beyaz patlama + yerde pembe halka + gokten turuncu-kirmizi isin
  sari  : yatay sari parlama + sari yildiz (yalniz patlama merkezi cevresi; havadaki altin yapraklar disarida)
Ayrim yumusak: sarilik = (min(R,G) - B) / max, G >= 0.75 R. Mobun mor govde artigi (gec karelerde merkezden uzak) atilir.
Cikti: kaynak/efekt9/renk_pembe/, renk_sari/ (vurus kutusuyla ayni koordinat), renk_olculer.json"""
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
import sys; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
K=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","efekt9")
J=json.load(open(os.path.join(K,"paket_olculer.json"))); x,y,w,h=J["vurus"]["kutu_ekran"]
MERKEZ=(485,665)
yy,xx=np.mgrid[0:h,0:w]; dx=xx+x-MERKEZ[0]; dy=yy+y-MERKEZ[1]; r=np.hypot(dx,dy)
isin=(np.abs(dx-(-0.36)*dy)<70)&(dy<0)                                   # gokten inen isin sutunu (yukari-sola egik)
for k in ("renk_pembe","renk_sari"):
    d=os.path.join(K,k); os.makedirs(d,exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d,f))
P=[];S=[]
for n in range(J["vurus"]["kare"]):
    E=np.asarray(Image.open(os.path.join(K,"paket_vurus","vurus_%02d.png"%n)).convert("RGB"),dtype=np.float32)
    R,G,B=E[...,0],E[...,1],E[...,2]; mx=np.maximum(E.max(2),1)
    sarilik=np.clip(((np.minimum(R,G)-B)/mx-0.18)/0.17,0,1)*np.clip((G/np.maximum(R,1)-0.70)/0.10,0,1)
    if n>=19: sarilik=np.maximum(sarilik,(r<260).astype(np.float32))             # pembe sonunca merkezdeki her sey yildiz
    ws=ndimage.gaussian_filter(sarilik,1.5)
    alan_s=((r<230)|((np.abs(dx)<480)&(np.abs(dy)<70))).astype(np.float32)     # yildiz + yatay parlama
    alan_p=((r<330)|isin).astype(np.float32)
    if n>=17: alan_p=np.minimum(alan_p,(r<170)|isin)                            # mobun gec mor izi
    alan_s=ndimage.gaussian_filter(alan_s,6)[...,None]; alan_p=ndimage.gaussian_filter(alan_p.astype(np.float32),6)[...,None]
    Pn=E*(1-ws)[...,None]*alan_p; Sn=E*ws[...,None]*alan_s
    # --- pembe tek basina: (a) altin yapraklar (merkezden ayri kucuk parlak parcalar) atilir
    mp=Pn.max(2); lb,nl=ndimage.label(mp>25)
    if nl:
        sz=ndimage.sum(np.ones_like(mp),lb,range(1,nl+1)); cm=ndimage.center_of_mass(np.ones_like(mp),lb,range(1,nl+1))
        at=[i+1 for i in range(nl) if sz[i]<3000 and np.hypot(cm[i][1]+x-MERKEZ[0],cm[i][0]+y-MERKEZ[1])>90]
        ym=ndimage.binary_dilation(np.isin(lb,at),np.ones((9,9))); Pn=Pn*(1-ndimage.gaussian_filter(ym.astype(np.float32),2))[...,None]
    #     (b) patlama govdesindeki delikler (mob silueti, ayrilan sari parlama) komsu pembe isikla doldurulur
    mp=Pn.max(2); govde=ndimage.binary_fill_holes(ndimage.binary_closing(mp>18,np.ones((25,25))))
    delik=govde&(mp<0.45*ndimage.maximum_filter(ndimage.gaussian_filter(mp,8),31))&(r<260)
    delik=ndimage.binary_opening(delik,np.ones((3,3)))
    if delik.any(): Pn=np.maximum(Pn,yumusak_doldur(Pn*(~delik)[...,None],delik,n=14,k=15)*delik[...,None])
    # --- sari tek basina: mobun mor artigi (B >= G) atilir
    mor=(Sn[...,2]>=Sn[...,1]-4)&(Sn.max(2)>15)&(r>60)
    Sn=Sn*(1-ndimage.gaussian_filter(ndimage.binary_dilation(mor,np.ones((7,7))).astype(np.float32),2))[...,None]
    Image.fromarray(np.clip(Pn,0,255).round().astype(np.uint8)).save(os.path.join(K,"renk_pembe","pembe_%02d.png"%n))
    Image.fromarray(np.clip(Sn,0,255).round().astype(np.uint8)).save(os.path.join(K,"renk_sari","sari_%02d.png"%n))
    P.append(float(Pn.max(2).mean())); S.append(float(Sn.max(2).mean()))
print("pembe",[round(v,1) for v in P]); print("sari",[round(v,1) for v in S])

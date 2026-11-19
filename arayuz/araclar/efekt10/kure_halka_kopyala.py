#!/usr/bin/env python3
"""Pembeli-temiz surumde somon-pembe halkanin SOL parcasini (kullanicinin isaretledigi: aci 180°±40°, yaricap ~92-162 px)
halkanin tamamina uygular. Kutupsal koordinatta sol dilim ayna-dongulu (ping-pong) olarak tum acilara yayilir -> dikis yok.
Halka disi (beyaz cekirdek, parantezler, dis sis) aynen kalir; halka sinirlarinda yumusak gecis.
Girdi: kure_ref_saydam_pembeli_temiz.png  Cikti: kure_ref_saydam_pembeli_halka.png + onizleme"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kure_ref"); ONZ=os.path.join(B_,"..","..","onizlemeler")
R0,R1,YARIM=92,162,np.radians(40)
a=np.asarray(Image.open(os.path.join(K,"kure_ref_saydam_pembeli_temiz.png")).convert("RGBA")).astype(np.float32)/255
L=a[...,:3]*a[...,3:4]; H,W=L.shape[:2]; cy,cx=(H-1)/2,(W-1)/2
yy,xx=np.mgrid[0:H,0:W]; R=np.hypot(xx-cx,yy-cy); th=np.arctan2(yy-cy,xx-cx)
# hedef acidan kaynak aciya: sol merkez (pi) etrafinda +-40° ucgen dalga (ayna)
d=np.angle(np.exp(1j*(th-np.pi)))                      # -pi..pi, sol merkez 0
per=4*YARIM; x=np.mod(d+YARIM,per); tri=np.where(x<2*YARIM,x,per-x)-YARIM   # -40°..+40°
kaynak=np.pi+tri
sx=cx+R*np.cos(kaynak); sy=cy+R*np.sin(kaynak)
K_=np.stack([ndimage.map_coordinates(L[...,c],[sy,sx],order=1) for c in range(3)],-1)
w=np.clip((R-(R0-8))/8,0,1)*np.clip(((R1+8)-R)/8,0,1)
w=w[...,None]
T=L*(1-w)+K_*w
# sag yari iz birakiyordu (kullanici isaretledi): halkanin SOL yarisi saga yatay ayna olarak yansitilir; ust-alt ortada 14 px yumusak gecis
mxr=np.clip(np.round(2*cx-xx).astype(int),0,W-1)
sag=np.clip((xx-cx+7)/14,0,1)[...,None]*w
T=T*(1-sag)+T[yy,mxr]*sag
# ust ve alt (tepe/dip) da iz birakiyordu: oralara sol parcanin 90° DONDURULMUS hali konur (ayna yok -> iz yok), yanlara yumusak gecis
dn=np.where(np.sin(th)<0,-np.pi/2,np.pi/2)                       # ust: -90° dondur, alt: +90° dondur -> kaynak sol (180°)
kx=cx+(xx-cx)*np.cos(-dn)-(yy-cy)*np.sin(-dn); ky=cy+(xx-cx)*np.sin(-dn)+(yy-cy)*np.cos(-dn)
D=np.stack([ndimage.map_coordinates(T[...,c],[ky,kx],order=1) for c in range(3)],-1)
q=np.clip((np.abs(np.sin(th))-0.62)/0.22,0,1); q=(q*q*(3-2*q))[...,None]*w
T=T*(1-q)+D*q
al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
out=os.path.join(K,"kure_ref_saydam_pembeli_halka.png")
Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(out)
im=Image.open(out); bz=Image.new("RGBA",im.size,(255,255,255,255)); bz.alpha_composite(im); sz=Image.new("RGBA",im.size,(0,0,0,255)); sz.alpha_composite(im)
o=Image.new("RGB",(im.width*2+20,im.height),(20,20,24)); o.paste(bz.convert("RGB"),(0,0)); o.paste(sz.convert("RGB"),(im.width+20,0))
o.save(os.path.join(ONZ,"efekt10_kure_pembeli_halka.png")); print("tamam")

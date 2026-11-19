#!/usr/bin/env python3
"""Efekt 10 — kare 5 (kullanici): kare 4 uzerine
  - sari-yesil parantezler disari dogru gider ve kaybolur (ara kare: yarim; kare 5: tamamen kaybolmus)
  - parantezlerin yeri seftali-somon olur (kure tumuyle seftali-somon)
  - titanyum beyaz sariya doner, yalniz en merkez beyaz kalir
  - fotograftaki gibi genis, yatay, dikenli sari isin (ust kenarinda sivri cikintilar, ortada asagi bir sivri)
  - boy: kareler_olcek.py'de kare 4'un %110'u
Kaynak tuval 1208x1208 (kure olcegi kare 1-4 ile ayni piksel boyunda, merkez ortada) -> isin sigsin.
Cikti: kareler/kare_05.png, kare_04b_ara.png (gecis), + _siyah/_beyaz, onizlemeler/efekt10_kare_05.png"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
a=np.asarray(Image.open(os.path.join(K,"kare_04.png")).convert("RGBA")).astype(np.float32)/255
S=a.shape[0]; N=2*S; o0=(N-S)//2
L4=np.zeros((N,N,3),np.float32); L4[o0:o0+S,o0:o0+S]=a[...,:3]*a[...,3:4]
cy=cx=(N-1)/2; yy,xx=np.mgrid[0:N,0:N].astype(np.float32); dx,dy=xx-cx,yy-cy; R=np.hypot(dx,dy); th=np.arctan2(dy,dx); ax=np.abs(dx)
def gur(sc,seed):
    z=np.random.default_rng(seed).standard_normal((N//sc+3,N//sc+3)).astype(np.float32)
    z=ndimage.zoom(ndimage.gaussian_filter(z,1.0),sc,order=3)[:N,:N]; return z/(z.std()+1e-6)
SARI=np.array([0xFC,0xFD,0x8A],np.float32)/255; ALTIN=np.array([0xFF,0xE6,0x5A],np.float32)/255; KREM=np.array([0xFF,0xFB,0xD8],np.float32)/255
mx=np.maximum(L4.max(2),1e-3)
par=np.clip((L4[...,1]-0.80*L4[...,0])/0.12+0.5,0,1)*np.clip((R-170)/12,0,1)*np.clip((L4.max(2)-0.15)/0.2,0,1)   # sari-yesil parantez
par=ndimage.gaussian_filter(np.clip(par*1.4,0,1),2.0)
def uret(t):
    # 1) parantezler disari (yaricap x (1+0.30t)) gider ve soner; dis sisleri de onlarla gider
    P=L4*par[...,None]; G=L4*(1-par[...,None])
    f=1/(1+0.30*t)
    Pm=np.stack([ndimage.map_coordinates(P[...,c],[cy+dy*f,cx+dx*f],order=1) for c in range(3)],-1)*(1-t)
    # 2) parantezlerin yeri seftali-somon: ayni acidaki somon halkadan (r 120-158) dokuyla, disa dogru soluk
    xr=np.mod(np.clip(R-165,0,None),76); rr=158-np.where(xr<38,xr,76-xr)
    Ls=np.stack([ndimage.map_coordinates(L4[...,c],[cy+rr*np.sin(th),cx+rr*np.cos(th)],order=1) for c in range(3)],-1)
    somon_maske=np.clip(ndimage.gaussian_filter(par,6)*1.6,0,1)*np.clip((250-R)/30,0,1)
    G=np.maximum(G,Ls*(somon_maske*min(1,1.4*t))[...,None])
    T=1-(1-G)*(1-np.clip(Pm,0,1))
    # 3) titanyum sariya: parlak beyaz/krem pikseller (dusuk doygunluk, yuksek parlaklik) sariya kayar, en merkez (r<16) beyaz kalir
    mxT=np.maximum(T.max(2),1e-3); beyazlik=np.clip((T.min(2)/mxT-0.70)/0.2,0,1)*np.clip((mxT-0.7)/0.2,0,1)*np.clip((R-16)/22,0,1)*(R<200)
    T=T*(1-(beyazlik*t)[...,None])+(SARI*mxT[...,None])*(beyazlik*t)[...,None]
    # 4) dikenli genis yatay sari isin (fotograftaki gibi)
    X=560.0
    ust=105*np.clip(1-ax/X,0,1)**0.9; alt=ust*0.8                                   # fotograftaki gibi kalin govde
    rg=np.random.default_rng(5)
    for xi,wi,hi in [(-150,40,130),(-70,26,110),(15,46,80),(95,30,170),(170,36,70),(-270,50,50),(300,60,55)]:   # yukari sivri dikenler
        ust=ust+hi*np.clip(1-np.abs(dx-xi)/wi,0,1)**1.7*np.clip(1-ax/X,0,1)**0.3
    for xi,wi,hi in [(10,26,190),(-120,36,50)]:                                                                  # asagi sivri
        alt=alt+hi*np.clip(1-np.abs(dx-xi)/wi,0,1)**1.8
    kenar=ust*(1+0.08*gur(8,3)); kenar2=alt*(1+0.08*gur(8,4))
    yuk=np.where(dy<0,kenar,kenar2)
    sb=np.clip(1-np.abs(dy)/np.maximum(yuk,1e-3),0,1)                                  # 1 merkez cizgisi, 0 kenar
    govde=np.clip(sb*1.6,0,1)**0.8*(ax<X)
    cek=np.exp(-(dy/(10+18*np.clip(1-ax/X,0,1)))**2)*np.clip(1-ax/X,0,1)**0.5           # parlak cekirdek cizgisi
    hale=ndimage.gaussian_filter(govde,22)*0.8
    renk=SARI*(1-sb[...,None])+KREM*sb[...,None]                                     # isin kenari parantez sarisi (#FCFD8A)
    isin=np.clip(renk*govde[...,None]*0.85+KREM*cek[...,None]*0.9+SARI*hale[...,None]*0.6,0,1)*t
    T=1-(1-T)*(1-isin)
    # en merkez beyaz
    T=np.maximum(T,np.ones(3,np.float32)*np.exp(-(R/14)**2)[...,None])
    return np.clip(T,0,1)
for ad,t in (("kare_04b_ara",0.5),("kare_05",1.0)):
    T=uret(t); al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
    Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(K,ad+".png"))
    im=Image.open(os.path.join(K,ad+".png"))
    for nm,zr in (("siyah",(0,0,0,255)),("beyaz",(255,255,255,255))):
        z=Image.new("RGBA",im.size,zr); z.alpha_composite(im); z.convert("RGB").save(os.path.join(K,"%s_%s.png"%(ad,nm)))
o=Image.new("RGB",(2*N//2+20,N),(20,20,24))
for i,nm in enumerate(("beyaz","siyah")): o.paste(Image.open(os.path.join(K,"kare_05_%s.png"%nm)).resize((N//2,N//2)),(0 if i==0 else N//2+20,0)) if False else None
o=Image.new("RGB",(N+20,N//2),(20,20,24))
for i,nm in enumerate(("beyaz","siyah")): o.paste(Image.open(os.path.join(K,"kare_05_%s.png"%nm)).resize((N//2,N//2)),(i*(N//2+20),0))
o.save(os.path.join(ONZ,"efekt10_kare_05.png")); print("tamam")

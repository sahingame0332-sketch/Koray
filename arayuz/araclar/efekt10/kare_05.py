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
SARI=np.array([0xFC,0xFD,0x8A],np.float32)/255; ALTIN=np.array([0xFF,0xE6,0x5A],np.float32)/255; KREM=np.array([0xFE,0xF6,0x8E],np.float32)/255         # isinin ortasi da sari (kullanici: cok beyazdi)
mx=np.maximum(L4.max(2),1e-3)
par=np.clip((L4[...,1]-0.80*L4[...,0])/0.12+0.5,0,1)*np.clip((R-170)/12,0,1)*np.clip((L4.max(2)-0.15)/0.2,0,1)   # sari-yesil parantez
par=ndimage.gaussian_filter(np.clip(par*1.4,0,1),2.0)
def uret(t):
    # 1) parantezler disari (yaricap x (1+0.30t)) gider ve soner; dis sisleri de onlarla gider
    P=L4*par[...,None]; G=L4*(1-par[...,None])
    f=1/(1+0.40*t)
    Pm=np.stack([ndimage.map_coordinates(P[...,c],[cy+dy*f,cx+dx*f],order=1) for c in range(3)],-1)
    # (kullanici) parantezler buyuyup disari acilirken soyutlasir ve seftali-somon kalir:
    lum=Pm.max(2,keepdims=True)
    SOMON=np.array([0xE3,0x96,0x96],np.float32)/255
    Pm=Pm*(1-t)+lum*SOMON/SOMON.max()*t                                              # renk sari-yesilden seftali-somona
    soyut=np.clip(0.55+0.65*ndimage.gaussian_filter(gur(14,21),1.5)+0.35*gur(6,22),0,1)   # parcali, bulutsu dagilma
    Pm=Pm*(1-t*(1-soyut[...,None]))
    Pm=np.stack([ndimage.gaussian_filter(Pm[...,c],1+5*t) for c in range(3)],-1)*(1-0.35*t)   # bulaniklasip biraz soner
    # 2) parantezlerin yeri seftali-somon: ayni acidaki somon halkadan (r 120-158) dokuyla, disa dogru soluk
    xr=np.mod(np.clip(R-165,0,None),76); rr=158-np.where(xr<38,xr,76-xr)
    Ls=np.stack([ndimage.map_coordinates(L4[...,c],[cy+rr*np.sin(th),cx+rr*np.cos(th)],order=1) for c in range(3)],-1)
    somon_maske=np.clip(ndimage.gaussian_filter(par,6)*1.6,0,1)*np.clip((250-R)/30,0,1)
    G=np.maximum(G,Ls*(somon_maske*min(1,1.4*t))[...,None])
    T=1-(1-G)*(1-np.clip(Pm,0,1))
    # 3) titanyum sariya: parlak beyaz/krem pikseller (dusuk doygunluk, yuksek parlaklik) sariya kayar, en merkez (r<16) beyaz kalir
    mxT=np.maximum(T.max(2),1e-3); beyazlik=np.clip((T.min(2)/mxT-0.70)/0.2,0,1)*np.clip((mxT-0.7)/0.2,0,1)*np.clip((R-16)/22,0,1)*(R<200)
    T=T*(1-(beyazlik*t)[...,None])+(SARI*mxT[...,None])*(beyazlik*t)[...,None]
    # 4) yildiz (kullanici: yangin gibi degil, yildiz isini gibi): merkezden cikan keskin, duz, uca dogru sivrilen isinlar.
    #    Baskin uzun yatay isin cifti + kisa capraz ve dikey isinlar; kenarlar net (gurultu yok), cevresinde yumusak parilti.
    def isin_kol(aci,boy,gen):                                                  # tek isin: kok genisligi gen, uca dogru 0
        ca,sa=np.cos(aci),np.sin(aci); u=dx*ca+dy*sa; v=np.abs(-dx*sa+dy*ca)
        w=gen*np.clip(1-u/boy,0,1)**1.15
        return np.clip(1-v/np.maximum(w,0.35),0,1)**1.6*(u>0)*(u<boy)
    kollar=[(0,560,30),(np.pi,560,30),                                          # uzun yatay
            (np.pi/2,190,16),(-np.pi/2,230,18),                                 # dikey (asagisi biraz uzun, fotograftaki gibi)
            (np.radians(-28),260,13),(np.radians(208),260,13),(np.radians(28),220,11),(np.radians(152),220,11),
            (np.radians(-62),150,9),(np.radians(242),150,9),(np.radians(62),130,8),(np.radians(118),130,8),
            (np.radians(-12),360,9),(np.radians(192),360,9),(np.radians(12),330,8),(np.radians(168),330,8)]
    yil=np.zeros_like(R)
    for ac,b_,g_ in kollar: yil=np.maximum(yil,isin_kol(ac,b_,g_))
    yil=np.maximum(yil,np.clip(1-R/70,0,1)**1.3)                               # merkez gobek
    cek=np.zeros_like(R)
    for ac,b_,g_ in kollar[:2]: cek=np.maximum(cek,isin_kol(ac,b_*0.9,g_*0.3))  # yatay isinin ince parlak omurgasi
    hale=ndimage.gaussian_filter(yil,18)*0.9+np.exp(-(R/120)**2)*0.35
    isin=np.clip(SARI*yil[...,None]*0.95+KREM*cek[...,None]*0.5+SARI*hale[...,None]*0.55,0,1)*t
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

#!/usr/bin/env python3
"""Efekt 9'u uc ayri parcaya boler (kaynak kareler degismez, yeni klasorler):
  vurus   : mobdaki skill (pembe patlama, gokten isin, yerde pembe halka, yatay parlama, yildiz, havadaki altin yapraklar) — mob zeminine bagli
  kesik   : karakterin onundeki sari kilic kesigi yayi — oyuncu ayagina bagli (kesik = oyuncu cevresindeki buyuk sari parca, y >= 500)
  altin   : oyuncunun ustundeki altin patlama — oyuncu ayagina bagli (ayni kareler)
Olcu: oyuncu boyu kayitta 270 px (bas ~760, ayak ~1027) -> butun parcalar karakter boyuna gore."""
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
K=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","efekt9")
B=json.load(open(os.path.join(K,"bilgi.json")))
BOY=270.0; MOB=(522,812); OYUNCU=(1130,1027)
def kaydet(ad,K_,x,y,capa):
    mx=np.stack(K_).max(3).max(0); ys,xs=np.nonzero(mx>8)
    a,b,c,d=max(0,xs.min()-6),max(0,ys.min()-6),min(mx.shape[1],xs.max()+7),min(mx.shape[0],ys.max()+7)
    od=os.path.join(K,"paket_"+ad); os.makedirs(od,exist_ok=True)
    for f in os.listdir(od): os.remove(os.path.join(od,f))
    son=max(i for i in range(len(K_)) if K_[i].max()>12)+1
    for n in range(son): Image.fromarray(np.clip(K_[n][b:d,a:c],0,255).round().astype(np.uint8)).save(os.path.join(od,"%s_%02d.png"%(ad,n)))
    X,Y,W,H=x+a,y+b,c-a,d-b
    return dict(kare=son,fps=30.0,kutu_ekran=[int(X),int(Y),int(W),int(H)],capa_ekran=list(capa),genislik_karakter=round(W/BOY,4),
                en_boy=round(H/W,4),pivot=[round((capa[0]-X)/W,4),round(1-(capa[1]-Y)/H,4)])
x,y,w,h=B["skill"]["kutu_ekran"]; V=[];C=[]
yy,xx=np.mgrid[0:h,0:w]
for n in range(B["skill"]["kare"]):
    E=np.asarray(Image.open(os.path.join(K,"skill","skill_%02d.png"%n)).convert("RGB"),dtype=np.float32)
    sari=(np.minimum(E[...,0],E[...,1])>1.4*E[...,2]+6)&(E.max(2)>20)
    bolge=(xx+x>820)&(yy+y>480)                                          # oyuncunun cevresi (yapraklar daha yukarida)
    l,nl=ndimage.label(ndimage.binary_closing(sari&bolge,np.ones((9,9))))
    m=np.zeros_like(sari)
    if nl:
        for i,sl in enumerate(ndimage.find_objects(l)):
            if (l[sl]==i+1).sum()>1500: m|=(l==i+1)
    m=ndimage.gaussian_filter(ndimage.binary_dilation(m,np.ones((11,11))).astype(np.float32),2.5)[...,None]
    # vurus: oyuncu bolgesinde (yapraklarin altinda) hicbir sey kalmasin — kesigin halesi dahil
    bol=ndimage.gaussian_filter(((xx+x>840)&(yy+y>500)).astype(np.float32),8)[...,None]
    Ck=E*np.maximum(m,bol)                                                # oyuncu bolgesindeki tum isik kesige ait (vurus orada sifir)
    # kesik: oyuncunun govdesindeki kucuk kirinti (sari olmayan) atilir
    gov=np.zeros((h,w),bool); gov[max(0,690-y):1050-y,max(0,1040-x):1245-x]=True     # oyuncu govdesi: kesik bunun ustunden/solundan gecer
    gw=ndimage.gaussian_filter(gov.astype(np.float32),6)[...,None]
    Ck=Ck*(1-gw)
    C.append(Ck); V.append(E*(1-np.maximum(m,bol)))
J={"karakter_boyu_px":BOY,"mob_zemini":list(MOB),"oyuncu_ayagi":list(OYUNCU)}
J["vurus"]=kaydet("vurus",V,x,y,MOB); J["kesik"]=kaydet("kesik",C,x,y,OYUNCU)
x,y,w,h=B["altin"]["kutu_ekran"]
import sys; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
A=[]
for n in range(B["altin"]["kare"]):
    E=np.asarray(Image.open(os.path.join(K,"altin","altin_%02d.png"%n)).convert("RGB"),dtype=np.float32)
    dolu=E.max(2)>3; delik=ndimage.binary_fill_holes(ndimage.binary_closing(dolu,np.ones((15,15))))&~dolu   # isim plakasi/can cubugu boslugu
    delik=ndimage.binary_dilation(delik,np.ones((5,5)))
    A.append(yumusak_doldur(E,delik,n=14,k=15) if delik.any() else E)
J["altin"]=kaydet("altin",A,x,y,OYUNCU)
json.dump(J,open(os.path.join(K,"paket_olculer.json"),"w"),indent=1)
for k in ("vurus","kesik","altin"): print(k,J[k])

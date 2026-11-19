#!/usr/bin/env python3
"""Efekt 10 — kare 3 (kullanici cizimi): titanyum beyaz kure ince bir mercek/goz bicimine kuculur (govde ~ 210x108 px,
uclari ince bant olarak yanlara uzanir ~ 300 px), etrafindaki ikinci katman (seftali/somon halka, r 80-170) %50 azalir.
Parantezler ve dis sis kare_01'deki gibi; bant bittikten sonra %50 opak sari cizgi devam eder.
Cikti: kareler/kare_03.png (+ _siyah/_beyaz), onizlemeler/efekt10_kare_01_02_03.png"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
GOVDE_X,GOVDE_Y,BANT_Y,BANT_X=105.0,54.0,36.0,170.0      # yanlar kalin (kare 2 gibi)
IKINCI_KAT=0.50; CIZGI_OPAK=0.50; SARI=np.array([0xF7,0xE6,0x45],np.float32)/255
a=np.asarray(Image.open(os.path.join(K,"kare_01.png")).convert("RGBA")).astype(np.float32)/255
L=a[...,:3]*a[...,3:4]; H,W=L.shape[:2]; cy,cx=(H-1)/2,(W-1)/2
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); dx,dy=xx-cx,yy-cy; R=np.hypot(dx,dy); ax=np.abs(dx)
# 1) parantez disinda ic bolge bosaltilir (ikinci katman asagida mercegin etrafina sarilacak)
mx=np.maximum(L.max(2),1e-3); sariyesil=np.clip((L[...,1]-0.80*L[...,0])/0.12+0.5,0,1)*np.clip((R-165)/10,0,1)
bos=np.clip((184-R)/30,0,1)*(1-sariyesil)
L=L*(1-bos)[...,None]
# 2) mercek bicimli titanyum beyaz: yari yukseklik profili h(x) -> govde (elips) + uca dogru incelen bant
govde=GOVDE_Y*np.sqrt(np.clip(1-(ax/GOVDE_X)**2,0,1))
bant=BANT_Y*(1-0.6*np.clip((ax-GOVDE_X*0.5)/(BANT_X-GOVDE_X*0.5),0,1)**0.8)*np.clip((BANT_X+10-ax)/20,0,1)   # kureden kalin cikar, paranteze dogru incelir
h=np.maximum(govde,np.maximum(bant,0.01))
h=ndimage.gaussian_filter1d(h,6,axis=1)                         # govde-bant gecisi yumusak (goz bicimi)
rg=np.random.default_rng(31)
def gur(sc,seed):
    z=np.random.default_rng(seed).standard_normal((H//sc+3,W//sc+3)).astype(np.float32)
    z=ndimage.zoom(ndimage.gaussian_filter(z,1.0),sc,order=3)[:H,:W]; return z/(z.std()+1e-6)
s_=np.abs(dy)/np.maximum(h,0.5)*(1+0.05*gur(12,5)+0.02*gur(5,6))        # 1 = kenar; hafif duzensiz
# renk: kare_01'in beyaz->sampanya->seftali radyal gecisi (orijinal L0'dan)
a0=np.asarray(Image.open(os.path.join(K,"kare_01.png")).convert("RGBA")).astype(np.float32)/255; L0=a0[...,:3]*a0[...,3:4]
rr=np.clip(76*s_,0,cx-1); G=np.stack([ndimage.map_coordinates(L0[...,c],[np.full_like(rr,cy),cx+rr],order=1) for c in range(3)],-1)
w=np.clip((1.45-s_)/0.75,0,1); w=w*w*(3-2*w); w=ndimage.gaussian_filter(w*(ax<BANT_X+25),4.0)[...,None]
G=np.stack([ndimage.gaussian_filter(G[...,c],2.0) for c in range(3)],-1)
# ikinci katman: kare_01'deki seftali/somon halka (beyaz kenari r~78'den r~172'ye, ~95 px) AYNI KALINLIKTA mercegin etrafina sarilir, %50
mask=np.hypot(dx/GOVDE_X,dy/GOVDE_Y)<1.0           # yalniz mercek govdesi (bant haric)
d=ndimage.distance_transform_edt(~mask)
KAL=48.0                                            # ikinci katman kalinligi (her yerde ayni)
req=112.0+d*(48.0/KAL)
th1=np.arctan2(dy,dx)
Hk=np.stack([ndimage.map_coordinates(L0[...,c],[cy+req*np.sin(th1),cx+req*np.cos(th1)],order=1) for c in range(3)],-1)
wk=np.clip((KAL+10-d)/26,0,1)*np.clip((d+6)/6,0,1)*(1-sariyesil)*np.clip((186-R)/10,0,1)
L=np.maximum(L,Hk*(wk*IKINCI_KAT)[...,None])
# renk (kare 2 gibi): yalniz merkez titanyum beyaz; etrafi kademeli olarak parantez sarisina (#FCFD8A, en fazla) doner
ALTIN=np.array([0xFC,0xFD,0x8A],np.float32)/255; ACIK=np.array([0xFE,0xFE,0xD2],np.float32)/255
q=np.hypot(dx/48.0,dy/34.0)
ys=np.clip((q-0.7)/2.2,0,1); ys=np.maximum(ys,np.clip((ax-GOVDE_X*0.4)/(BANT_X-GOVDE_X*0.4),0,1)); ys=ys*ys*(3-2*ys)
G=np.where(ys[...,None]<0.5, np.ones(3,np.float32)*(1-2*ys[...,None])+ACIK*2*ys[...,None], ACIK*(2-2*ys[...,None])+ALTIN*(2*ys[...,None]-1))
T=L*(1-w)+G*w
# 3) sari cizgi %50 (beyazin icinde gorunmez)
beyaz=ndimage.gaussian_filter(np.clip((T.min(2)-0.80)/0.15,0,1),2.0)
boy=np.clip(1-ax/(W*0.47),0,1)**0.8
cizgi=(np.exp(-(dy/1.6)**2)+0.35*np.exp(-(dy/5.0)**2))*boy*CIZGI_OPAK*(1-beyaz)
T=T*(1-cizgi[...,None])+SARI*cizgi[...,None]
al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(K,"kare_03.png"))
im=Image.open(os.path.join(K,"kare_03.png"))
for ad,zr in (("siyah",(0,0,0,255)),("beyaz",(255,255,255,255))):
    z=Image.new("RGBA",im.size,zr); z.alpha_composite(im); z.convert("RGB").save(os.path.join(K,"kare_03_%s.png"%ad))
o=Image.new("RGB",(W*3+40,H*2+20),(20,20,24))
for j,k in enumerate(("01","02","03")):
    for i,ad in enumerate(("beyaz","siyah")):
        o.paste(Image.open(os.path.join(K,"kare_%s_%s.png"%(k,ad))),(j*(W+20),i*(H+20)))
o.save(os.path.join(ONZ,"efekt10_kare_01_02_03.png")); print("tamam")

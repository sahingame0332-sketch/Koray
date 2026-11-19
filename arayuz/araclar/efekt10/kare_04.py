#!/usr/bin/env python3
"""Efekt 10 — kare 4 (yavas cekimde 00:11): kare 3 ile ayni yapi; merkez kure ve etrafindaki (mercek + bantlar + ikinci katman + alevler)
biraz azalmis ve tum uzunlugun 1/3'u kadar (OLC=0.5: 340 px -> 170 px); efekt boyu kareler_olcek.py'de kare 3'un %110'u.
(eski aciklama) kare 3 (kullanici cizimi): titanyum beyaz kure ince bir mercek/goz bicimine kuculur (govde ~ 210x108 px,
uclari ince bant olarak yanlara uzanir ~ 300 px), etrafindaki ikinci katman (seftali/somon halka, r 80-170) %50 azalir.
Parantezler ve dis sis kare_01'deki gibi; bant bittikten sonra %50 opak sari cizgi devam eder.
Cikti: kareler/kare_03.png (+ _siyah/_beyaz), onizlemeler/efekt10_kare_01_02_03.png"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
OLC=0.5; AZ=0.85                                      # merkez yapi olcegi (tum uzunlugun 1/3'u) ve azalma
GOVDE_X,GOVDE_Y=105.0*OLC,54.0*OLC
BANT_Y,BANT_X=GOVDE_Y*0.9,170.0          # bant: titanyum boyunda baslar, paranteze kadar uzanip kenara dogru incelir
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
bant=BANT_Y*(1-0.42*np.clip((ax-GOVDE_X*0.5)/(BANT_X-GOVDE_X*0.5),0,1)**0.8)*np.clip((BANT_X+10-ax)/20,0,1)   # kureden kalin cikar, paranteze dogru incelir
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
KAL=48.0*OLC                                            # ikinci katman kalinligi (her yerde ayni)
req=112.0+d*(48.0/KAL)
th1=np.arctan2(dy,dx)
Hk=np.stack([ndimage.map_coordinates(L0[...,c],[cy+req*np.sin(th1),cx+req*np.cos(th1)],order=1) for c in range(3)],-1)
wk=np.clip((KAL+10-d)/26,0,1)*np.clip((d+6)/6,0,1)*(1-sariyesil)*np.clip((186-R)/10,0,1)
L=np.maximum(L,Hk*(wk*IKINCI_KAT*AZ)[...,None])
# renk (kare 2 gibi): yalniz merkez titanyum beyaz; etrafi kademeli olarak parantez sarisina (#FCFD8A, en fazla) doner
ALTIN=np.array([0xFC,0xFD,0x8A],np.float32)/255; ACIK=np.array([0xFE,0xFE,0xD2],np.float32)/255
q=np.hypot(dx/(48.0*OLC),dy/(34.0*OLC))
ys=np.clip((q-0.7)/2.2,0,1); ys=np.maximum(ys,np.clip((ax-GOVDE_X*0.4)/(BANT_X-GOVDE_X*0.4),0,1)); ys=ys*ys*(3-2*ys)
G=np.where(ys[...,None]<0.5, np.ones(3,np.float32)*(1-2*ys[...,None])+ACIK*2*ys[...,None], ACIK*(2-2*ys[...,None])+ALTIN*(2*ys[...,None]-1))
w=w*AZ
T=L*(1-w)+G*w
# 3) sari cizgi %50 (beyazin icinde gorunmez)
beyaz=ndimage.gaussian_filter(np.clip((T.min(2)-0.80)/0.15,0,1),2.0)
boy=np.clip(1-ax/(W*0.47),0,1)**0.8
cizgi=(np.exp(-(dy/1.6)**2)+0.35*np.exp(-(dy/5.0)**2))*boy*CIZGI_OPAK*(1-beyaz)
T=T*(1-cizgi[...,None])+SARI*cizgi[...,None]
# 4) merkezin kenarina alev sizmalari: mercek govdesinin kenarindan disari, dalgali alev dilleri (ic sari-beyaz -> uc turuncu)
govm=np.hypot(dx/GOVDE_X,dy/GOVDE_Y)<1.0
dd=ndimage.distance_transform_edt(~govm)
th2=np.arctan2(dy,dx); NA=72
za=np.random.default_rng(77).random(NA).astype(np.float32)
ia=(th2+np.pi)/(2*np.pi)*NA; i0=np.floor(ia).astype(int)%NA; fa=ia-np.floor(ia); fa=fa*fa*(3-2*fa)
dil=za[i0]*(1-fa)+za[(i0+1)%NA]*fa                                  # her yonde farkli dil uzunlugu
uz=(10+34*dil**1.6)*OLC
kivri=gur(6,78)*4.0                                                  # alevin kivrilmasi
alev=np.clip(1-(dd+kivri)/uz,0,1)*(dd>0)*np.clip(1-np.abs(dy)/(GOVDE_Y*1.9),0,1)**0.3
damar=np.clip(0.55+0.45*np.sin(th2*38+gur(9,79)*2.5),0,1)            # dil dil ayrisma
alev=(alev**1.3)*(0.45+0.55*damar)*np.clip(1-np.abs(dx)/(GOVDE_X*1.25),0,1)**0.5
IC=np.array([0xFF,0xFB,0xC8],np.float32)/255; UC=np.array([0xFF,0xB0,0x55],np.float32)/255
u_=np.clip(dd/np.maximum(uz,1),0,1)[...,None]
alev_renk=IC*(1-u_)+UC*u_
T=1-(1-T)*(1-np.clip(alev_renk*alev[...,None]*0.95*AZ,0,1))
# 4b) ikinci katmanin (titanyum disindaki seftali/somon halka) dis kenarina da alev sizmalari: somon -> kizil turuncu uclar
halka_m=d<=KAL-6
dd2=ndimage.distance_transform_edt(~halka_m)
zb=np.random.default_rng(91).random(96).astype(np.float32); NB_=96
ib=(th2+np.pi)/(2*np.pi)*NB_; j0=np.floor(ib).astype(int)%NB_; fb=ib-np.floor(ib); fb=fb*fb*(3-2*fb)
dil2=zb[j0]*(1-fb)+zb[(j0+1)%NB_]*fb
uz2=(8+30*dil2**1.5)*OLC
alev2=np.clip(1-(dd2+gur(6,92)*4.0)/(uz2+10),0,1)*np.clip(dd2/10,0,1)
damar2=np.clip(0.5+0.5*np.sin(th2*46+gur(9,93)*2.5),0,1)
alev2=(alev2**1.3)*(0.4+0.6*damar2)*(1-sariyesil)*np.clip((186-R)/12,0,1)
IC2=np.array([0xF4,0xA8,0x96],np.float32)/255; UC2=np.array([0xE8,0x6A,0x40],np.float32)/255
u2=np.clip(dd2/np.maximum(uz2,1),0,1)[...,None]
T=1-(1-T)*(1-np.clip((IC2*(1-u2)+UC2*u2)*alev2[...,None]*0.75*AZ,0,1))
# 5) kullanicinin ust temizligi ve onun alt aynasi: maske bolgesi saydam
mk=np.asarray(Image.open(os.path.join(K,"kare_03_temizlik_maskesi.png")))>127
mk|=(np.abs(dy)>200)&(ax<175)                                           # ekran disina tasan kisim: ust/alt kapak disari dogru tamamen temiz
mk|=(R>148)&(R<182)&(sariyesil<0.3)&(np.abs(dy)>45)                     # bosluktaki ince halka cizgisi
mk=ndimage.binary_closing(mk,np.ones((9,9)))&(R>150)
yy_,xx_=np.mgrid[-6:7,-6:7]; mk=ndimage.binary_opening(mk,(yy_**2+xx_**2)<=36)    # tirtikli kenarlar yuvarlanir
mk=np.maximum(ndimage.gaussian_filter(mk.astype(np.float32),3.0),ndimage.gaussian_filter(mk.astype(np.float32),14.0)*(R>200))   # dis sisle kesik kenar yumusak
T=T*(1-mk)[...,None]
# 6) sol parantezin disi = sag parantezin disinin yatay aynasi (r>212, sol yari; eksen ve ic kenar yumusak)
mxs=np.clip(np.round(2*cx-xx).astype(int),0,W-1); yyi=yy.astype(int)
ws=np.clip((R-212)/14,0,1)*np.clip((-dx-20)/30,0,1)
T=T*(1-ws[...,None])+T[yyi,mxs]*ws[...,None]
# 7) bos kalan yerler (kullanici): kare 1-2'deki seftali-somon katman AYNI PIKSELLERIYLE (renk + doku birebir kare_01'den),
#    yalniz eski beyaz cekirdek yeri (r<100) ayni katmanin rengiyle iceri dogru tamamlanir; merkezin sekli bozulmaz (yalniz bos yerler)
th3=np.arctan2(dy,dx); rs3=np.where(R<100,100+(100-R)*0.25,R)
Lic3=np.stack([ndimage.gaussian_filter(ndimage.map_coordinates(L0[...,c],[cy+rs3*np.sin(th3),cx+rs3*np.cos(th3)],order=1),5) for c in range(3)],-1)
w3=np.clip((104-R)/8,0,1)[...,None]; Lk=L0*(1-w3)+Lic3*w3                         # kare_01 katmani (beyaz cekirdeksiz)
bos_yer=np.clip((Lk.max(2)*0.95-T.max(2))/0.12,0,1); bos_yer=ndimage.gaussian_filter(bos_yer,2.0)   # T, kare_01 katmanindan sonukse (bos/yari bos) doldur
bv=bos_yer*(1-sariyesil)*np.clip((186-R)/8,0,1)
T=np.maximum(T,Lk*bv[...,None])
al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(K,"kare_04.png"))
im=Image.open(os.path.join(K,"kare_04.png"))
for ad,zr in (("siyah",(0,0,0,255)),("beyaz",(255,255,255,255))):
    z=Image.new("RGBA",im.size,zr); z.alpha_composite(im); z.convert("RGB").save(os.path.join(K,"kare_04_%s.png"%ad))
o=Image.new("RGB",(W*2+20,H),(20,20,24))
for i,ad in enumerate(("beyaz","siyah")): o.paste(Image.open(os.path.join(K,"kare_04_%s.png"%ad)),(i*(W+20),0))
o.save(os.path.join(ONZ,"efekt10_kare_04.png")); print("tamam")

#!/usr/bin/env python3
"""Efekt 10 kure — REFERANSTAN PIKSEL PIKSEL: kullanicinin fotografi (= patlama_son_hali klibinin 11. karesi; HUD ile hizalandi:
foto(x,y) = video(x,y)*1.01 + (4,-28)). Efektsiz zemin B = klibin ilk 4 karesinin medyani (ayni hizalama).
Oyun isigi ekran (screen) karisimiyla ciziyor: foto = 1-(1-B)(1-E)  ->  E = 1-(1-foto)/(1-B)  (doyan beyaz cekirdek de dogru cikar).
Isigin onundeki mob parcalari / oyuncu / isim etiketi: efektin sag-sol ve ust-alt simetrisiyle (4 yonlu medyan) yalniz sapan yerlerde doldurulur.
Cikti: kaynak/efekt10/kure_ref/kure_ref.png (siyah fon), kure_ref_saydam.png (alfa = parlaklik), onizlemeler/efekt10_kure_ref*.png
Kullanim: kure_ref.py FOTO KARE_KLASORU (KLASOR/k_01..k_04.png = klibin ilk kareleri; klip depoya konmaz)"""
import os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kure_ref"); ONZ=os.path.join(B_,"..","..","onizlemeler")
SC,OX,OY=1.01,4,-28; CX,CY=638,440; RMAX=262
def hizala(p):
    A=np.asarray(Image.open(p).convert('RGB').resize((round(1440*SC),round(1080*SC)),Image.BICUBIC)).astype(np.float32)/255
    a=np.zeros((1080,1454,3),np.float32)
    for y in range(1080):
        sy=y-OY
        if 0<=sy<A.shape[0]: a[y,OX:][:1454-OX]=A[sy,:1454-OX]
    return a
foto=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32)/255
B=np.median([hizala(os.path.join(sys.argv[2],"k_%02d.png"%i)) for i in range(1,5)],0)       # ayni anin hemen oncesi: kamera ayni
E=np.clip(1-(1-foto)/np.maximum(1-B,0.02),0,1)
H,W=E.shape[:2]; yy,xx=np.mgrid[0:H,0:W]; R=np.hypot(xx-CX,yy-CY)
mx=np.clip(2*CX-xx,0,W-1); my=np.clip(2*CY-yy,0,H-1)
d4=np.stack([E,E[yy,mx],E[my,xx],E[my,mx]],0); med=np.median(d4,0)
sap=(np.abs(E-med).sum(2)>0.40)&(R<RMAX+20)
# bilinen ongorulen engeller: oyuncu + isim etiketi (video kare 11'deki yeri), mob parcalari (B'de yesil govde)
oy=((xx>690)&(xx<800)&(yy>470)&(yy<640))|((xx>690)&(xx<810)&(yy>445)&(yy<495))     # oyuncu govdesi + isim etiketi (dar)
yesil=(B[...,1]>B[...,0]+0.06)&(B[...,1]>B[...,2]+0.12)&(B.max(2)<0.55)
sap|=oy|(ndimage.binary_opening(yesil,np.ones((7,7)))&(R<RMAX+20))           # zemin karesinde mob govdesi olan yerler
sap=ndimage.binary_dilation(sap,np.ones((7,7)))
# doldurma: efekt halka yapili -> engelli pikseller ayni yaricapta, aci yonunde en yakin gercek piksellerden (kutupsal dogrusal ara deger)
NA,NR=1440,RMAX+40
tg=np.linspace(-np.pi,np.pi,NA,endpoint=False); rg_=np.arange(NR,dtype=np.float32)
PX=(CX+rg_[:,None]*np.cos(tg)[None,:]); PY=(CY+rg_[:,None]*np.sin(tg)[None,:])
pxi=np.clip(np.round(PX).astype(int),0,W-1); pyi=np.clip(np.round(PY).astype(int),0,H-1)
Pv=E[pyi,pxi]; Pm=sap[pyi,pxi]
Pf=Pv.copy()
for r_ in range(NR):
    ok=~Pm[r_]
    if ok.sum()>4 and (~ok).any():
        idx=np.where(ok)[0]; t=np.arange(NA)
        for c in range(3): Pf[r_,~ok,c]=np.interp(t[~ok],idx,Pv[r_,idx,c],period=NA)
# geri kartezyene
ai=((np.arctan2(yy-CY,xx-CX)+np.pi)/(2*np.pi)*NA).astype(int)%NA; ri=np.clip(R.astype(int),0,NR-1)
dol=Pf[ri,ai]
dol=np.stack([ndimage.gaussian_filter(dol[...,c],1.2) for c in range(3)],-1)
w=np.maximum(ndimage.gaussian_filter(sap.astype(np.float32),2.0),ndimage.gaussian_filter(oy.astype(np.float32),7)*1.6).clip(0,1)[...,None]; w=np.maximum(w,sap[...,None])
# oyuncu + isim etiketi kutusu: merkezin sol tarafi temiz -> yatay ayna (ayni yaricap ve dikey konum)
ay=E[yy,mx]; mor=(ay[...,0]>ay[...,1]+0.18)&(ay[...,2]>ay[...,1]+0.08)
oyd=np.where(mor[...,None],dol,0.5*ay+0.5*dol)
dol=np.where(oy[...,None],oyd,dol)
T=E*(1-w)+dol*w
# ust yari = alt yarinin dikey aynasi (kullanici: alt %50 dogru renkler); merkez cizgisinde 12 px yumusak gecis
ust=np.clip((CY+6-yy)/12,0,1)[...,None]
T=T*(1-ust)+T[my,xx]*ust
# turuncu gecis katmani (r 160-180, somon halka ile sari parantez arasi) kaldirildi: yumusak kenarli saydam
kald=1-np.clip((R-132)/6,0,1)*np.clip((182-R)/6,0,1)          # bos bant merkeze dogru 24 px (mevcut genisligin 6/5i) genisletildi: 136-180
T=T*kald[...,None]
# daire disi (isaretli bolge disi) yumusakca saydam
T=T*np.clip((RMAX+30-R)/45,0,1)[...,None]
os.makedirs(K,exist_ok=True)
x0,y0,x1,y1=CX-RMAX-40,CY-RMAX-40,CX+RMAX+40,CY+RMAX+40
k=lambda a: Image.fromarray((np.clip(a,0,1)*255).round().astype(np.uint8)).crop((x0,max(0,y0),x1,min(H,y1)))
k(T).save(os.path.join(K,"kure_ref.png"))
al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).crop((x0,max(0,y0),x1,min(H,y1))).save(os.path.join(K,"kure_ref_saydam.png"))
geri=1-(1-B)*(1-T)                                                            # ayni zemine geri bindirme (dogrulama)
fark=np.abs(geri-foto).mean(2); ic=(R<RMAX)&~sap
print("dogrulama: isaretli bolgede (engelsiz) ort. fark %.2f / 255, engelli piksel orani %.1f%%"%(fark[ic].mean()*255, sap[R<RMAX].mean()*100))
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","Roboto-Bold.ttf"),28)
ims=[(k(foto),"REFERANS (fotoğraf)"),(k(geri),"YENİ — aynı zeminde"),(k(T),"YENİ — siyah fonda (ışık katmanı)")]
w_=ims[0][0].width; out=Image.new("RGB",(3*w_+40,ims[0][0].height+56),(20,20,24)); d=ImageDraw.Draw(out)
for i,(im,t) in enumerate(ims): out.paste(im,(i*(w_+20),56)); d.text((i*(w_+20)+10,12),t,font=F,fill=(255,220,120))
out.save(os.path.join(ONZ,"efekt10_kure_ref.png"))

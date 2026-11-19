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
KARE=int(sys.argv[3]) if len(sys.argv)>3 else None                          # verilirse: klibin bu karesi islenir (animasyon)
SADE=len(sys.argv)>4 and sys.argv[4]=="sade"                                   # sari evre: halka/bant duzeltmeleri uygulanmaz
foto=hizala(os.path.join(sys.argv[2],"k_%02d.png"%(KARE+1))) if KARE is not None else np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32)/255
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
T0=T.copy()
if not SADE:
    # turuncu gecis katmani (r 160-180, somon halka ile sari parantez arasi) kaldirildi: yumusak kenarli saydam
    T0=T.copy()
    kald=1-np.clip((R-132)/6,0,1)*np.clip((192-R)/6,0,1)          # bos bant merkeze dogru 24 px (mevcut genisligin 6/5i) genisletildi: 136-180
    T=T*kald[...,None]
    # silinen bandin hemen disindaki en yakin renk (turuncu/pembe; G < 0.85 R) da silinir — sari/yesil parantez ve ic somon halka korunur
    tp=(T[...,1]<0.85*T[...,0])&(R>=178)&(R<235)
    tp=ndimage.binary_opening(tp,np.ones((3,3)))
    wt=np.clip(ndimage.gaussian_filter(tp.astype(np.float32),2.0)*1.5,0,1)
    T=T*(1-wt)[...,None]
    # eski (fotograftaki) parantez geri: silmelerde kaybolan kenarlari referansin kendi pikselleriyle doldur
    mx0=T0.max(2); doy0=(mx0-T0.min(2))/np.maximum(mx0,1e-3)
    Y=(T0[...,1]>=0.85*T0[...,0])&(doy0>0.18)&(mx0>0.2)&(R>165)&(R<275)
    Y=ndimage.binary_closing(ndimage.binary_opening(Y,np.ones((3,3))),np.ones((7,7)))
    lb_,n_=ndimage.label(Y)
    if n_:
        sz_=ndimage.sum(Y,lb_,range(1,n_+1)); Y=np.isin(lb_,1+np.where(sz_>800)[0])   # yalniz buyuk parantez govdeleri
    wy=np.clip(ndimage.gaussian_filter(Y.astype(np.float32),1.5)*1.3,0,1)[...,None]
    T=T*(1-wy)+np.maximum(T,T0)*wy
    # kenarlar: pruzlu girintiler kapanis ile doldurulur; yeni pikseller en yakin gercek parantez pikselinin rengini alir
    yy_d,xx_d=np.mgrid[-14:15,-14:15]; disk=(yy_d**2+xx_d**2)<=14**2
    Yc=ndimage.binary_closing(np.pad(Y,15),disk)[15:-15,15:-15]
    ek=Yc&~Y
    if ek.any():
        _,(iy,ix)=ndimage.distance_transform_edt(~Y,return_indices=True)
        kom=ndimage.gaussian_filter(T,(2,2,0))[iy,ix]
        we=np.clip(ndimage.gaussian_filter(ek.astype(np.float32),1.2)*1.4,0,1)[...,None]*Yc[...,None]
        T=T*(1-we)+np.maximum(T,kom)*we
    # kenar duzeltme (kutupsal): her parantez kendi merkez acisina gore (sag 0°, sol 180°) ±90° araliginda incelenir.
    # Aci basina ic/dis kenar olculur; ic kenar alt zarf, dis kenar ust zarfla duzgun yaya cekilir (girintiler dolar, cikintilar tiraslanir).
    # Uclar: parantezin aci araligi aynen kalir, son %10'da ic ve dis kenar birlesir -> uclar kalin ve sivri.
    Yk=Y|Yc; NB=720
    for merkez in (0.0,np.pi):
        phi=np.angle(np.exp(1j*(np.arctan2(yy-CY,xx-CX)-merkez)))
        yan=np.abs(phi)<np.pi/2
        sec=Yk&yan&(R>150)
        if sec.sum()<200: continue
        bi=np.clip(((phi+np.pi/2)/np.pi*NB).astype(int),0,NB-1)
        a_=bi[sec]; r_=R[sec]
        rin=np.full(NB,np.nan); rout=np.full(NB,np.nan)
        for k in np.unique(a_):
            rr=r_[a_==k]
            if len(rr)>=2: rin[k]=np.percentile(rr,2); rout[k]=np.percentile(rr,98)
        ok=~np.isnan(rin)
        if ok.sum()<20: continue
        lo,hi=np.where(ok)[0][[0,-1]]                                      # parantezin aci araligi (uctan uca)
        idx=np.where(ok)[0]
        ri=np.interp(np.arange(NB),idx,rin[idx]); ro=np.interp(np.arange(NB),idx,rout[idx])
        ri=ndimage.gaussian_filter1d(ndimage.minimum_filter1d(ri,31,mode="nearest"),8,mode="nearest")
        ro=ndimage.gaussian_filter1d(ndimage.maximum_filter1d(ro,31,mode="nearest"),8,mode="nearest")
        pos=np.clip((np.arange(NB)-lo)/max(hi-lo,1),0,1)
        uc=np.clip(np.minimum(pos,1-pos)/0.10,0,1)**0.7
        mid=(ri+ro)/2; ri2=mid-(mid-ri)*uc; ro2=mid+(ro-mid)*uc
        aralik=(bi>=lo)&(bi<=hi)&yan
        inside=aralik&(R>=ri2[bi])&(R<=ro2[bi])
        yeni=inside&~Yk
        if yeni.any():
            _,(iy2,ix2)=ndimage.distance_transform_edt(~Yk,return_indices=True)
            kom2=ndimage.gaussian_filter(T,(2,2,0))[iy2,ix2]
            w2=np.clip(ndimage.gaussian_filter(yeni.astype(np.float32),1.0)*1.5,0,1)[...,None]*inside[...,None]
            T=T*(1-w2)+np.maximum(T,kom2)*w2
        tasan=Yk&aralik&(R<ri2[bi]-1.5)&(R>ri2[bi]-40)&(uc[bi]>0.5)           # ic kenardan iceri tasan cikintilar; dis hale ve uclar korunur
        T=T*(1-np.clip(ndimage.gaussian_filter(tasan.astype(np.float32),1.0),0,1))[...,None]
# daire disi (isaretli bolge disi) yumusakca saydam
T=T*np.clip((RMAX+30-R)/45,0,1)[...,None]
os.makedirs(K,exist_ok=True)
if KARE is not None:
    x0,y0,x1,y1=CX-RMAX-40,CY-RMAX-40,CX+RMAX+40,CY+RMAX+40
    ad=os.path.join(K,"anim"); os.makedirs(ad,exist_ok=True)
    al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
    Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).crop((x0,max(0,y0),x1,min(H,y1))).save(os.path.join(ad,"kure_%02d.png"%KARE))
    print("kare",KARE,"tamam"); sys.exit(0)
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

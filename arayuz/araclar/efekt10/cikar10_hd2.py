#!/usr/bin/env python3
"""Efekt 10: kayit 21-39-19 (tablet 2266x1488, 60 kare/sn, TUM kareler; YAKIN kamera + kucuk alcak mob -> buyuk ve kapanmayan aura) — tam dongu: yapraklar + pembe aura -> yatay parlama -> sari yildiz patlamasi. Ayni ailenin skill isigi (kesik + altin yapraklar -> pembe aura -> yatay sari parlama).
Efekt 8 yontemi: E = O - P; P = efektsiz zemin, mob siluetinde hasar kirmizisina boyanmis zemin (R=0.60L+162, G=0.95L+5, B=0.75L, guc s olculur).
Kayitta 96. kareden sonra ekran kararir (kontrol merkezi): kanal kazanci duvar/cim bolgesinden olculup bolunur.
Kullanim: cikar10.py KLASOR (KLASOR/k_%04d.png, 60 kare/sn, 1'den; kayit depoya konmaz)"""
import os, sys, json, glob, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","efekt10","hd2")
KX,KY,KX1,KY1=600,130,2200,1100
MOB_ZEMIN=(1480,600); MOB_TEPE=380
ONCE=range(100,141,3); SONRA=range(244,262,3); EFEKT=range(144,193)
def kirmizi(L): return np.stack([0.60*L+162,0.95*L+5,0.75*L],-1)
def calis(k):
    fs=sorted(glob.glob(os.path.join(k,"k_*.png")))
    T=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)
    Bt=np.median([T(i) for i in ONCE],0)
    q=np.zeros(Bt.shape[:2],bool); q[150:450,800:1100]=True; q[1000:1300,1300:1700]=True; q&=(Bt.min(2)>8)&(Bt.max(2)<200)
    G={}
    def Y(i):
        O=T(i); G[i]=float(np.median(O[q][:,0]/Bt[q][:,0])); return O[KY:KY1,KX:KX1]
    Oc={}
    def zemin(i):
        """kararma ekranda uzamsal olarak yayiliyor: piksel basina kazanc haritasi (24 px blok medyani, ince isik cizgileri elenir)"""
        if G[i]>0.995: return Bt[KY:KY1,KX:KX1]
        O=T(i); Rt=O/np.maximum(Bt,6); h,w=Rt.shape[:2]; b=24
        bl=Rt[:h//b*b,:w//b*b].reshape(h//b,b,w//b,b,3).transpose(0,2,1,3,4).reshape(h//b,w//b,b*b,3)
        gm=np.median(bl,2); gm[...,2]=gm[...,1]; gm=ndimage.median_filter(gm,size=(5,5,1))
        gm=ndimage.zoom(gm,(h/gm.shape[0],w/gm.shape[1],1),order=1)
        gm=np.pad(gm,((0,h-gm.shape[0]),(0,w-gm.shape[1]),(0,0)),mode="edge")
        return (Bt*np.clip(gm,0.3,1.05))[KY:KY1,KX:KX1]
    Bo=Bt[KY:KY1,KX:KX1]; Bs=np.median([T(i) for i in SONRA],0)[KY:KY1,KX:KX1]
    rm=np.zeros(Bo.shape[:2],bool)
    for i in (148,150,152,154,168,170,172,174):
        O=Y(i); Bz=zemin(i); rm|=ndimage.binary_opening((O[...,0]-Bz[...,0]>45)&(O[...,0]>O[...,1]+70)&(O[...,2]<O[...,1]+5)&(O[...,2]>0.55*O[...,1])&(O[...,1]<0.45*O[...,0]),np.ones((3,3)))
    kut=np.zeros_like(rm); kut[300-KY:760-KY,1180-KX:1760-KX]=True; rm&=kut
    l,n=ndimage.label(rm); sz=ndimage.sum(rm,l,range(1,n+1)); rm=l==(1+np.argmax(sz))
    sik=np.zeros_like(rm)
    for i in (150,152,170,172):
        O=Y(i); sik|=((O[...,0]-Bo[...,0])>35)&(O[...,0]>O[...,1]+55)&(O[...,2]<O[...,1]+5)&(O[...,2]>0.55*O[...,1])&(O[...,1]<0.45*O[...,0])
    rm=ndimage.binary_closing(rm&ndimage.binary_dilation(sik,np.ones((3,3))),np.ones((3,3))); rmd=ndimage.binary_dilation(rm,np.ones((3,3)))
    Kr0=kirmizi(Bo.mean(2)); od=os.path.join(OUT,"skill"); os.makedirs(od,exist_ok=True)
    for f in os.listdir(od): os.remove(os.path.join(od,f))
    S=[]; K=[]
    for i in EFEKT:
        O=Y(i); Bo=zemin(i); Kr=kirmizi(Bo.mean(2))
        qq=rm&(Kr[...,0]-Bo[...,0]>40)&~((O[...,1]-Bo[...,1])>25)
        dK=(Kr-Bo)[qq]; dO=(O-Bo)[qq]
        s=float(np.clip((dK*dO).sum()/max((dK*dK).sum(),1e-6),0,1)) if qq.sum()>50 else 0.0; S.append(round(s,3))
        P=np.where(rm[...,None],Bo+s*(Kr-Bo),Bo)
        D=np.where(rmd[...,None],O-P,np.minimum(O-Bo,O-Bs))                       # oyuncu hareketi: iki zeminin kucugu
        w8=(np.clip((O.max(2)-242)/13.0,0,1)*(D.max(2)>60))[...,None]
        E=np.clip(w8*O+(1-w8)*D,0,255)
        Dp=np.clip(D,0,None); yesil=(Dp[...,1]>Dp[...,0]*1.3)&(Dp[...,1]>Dp[...,2]*1.6)
        artik=rmd&(((Dp[...,0]>2.2*Dp[...,1]+10)&(Dp[...,0]>2*Dp[...,2]+10))|((Dp[...,1]+Dp[...,2])>2.6*Dp[...,0]+20))
        E=E*(np.clip((Dp.max(2)-10)/16,0,1)*~yesil*~artik)[...,None]
        yab=(np.minimum(O-Bo,O-Bs).min(2)<-25)&~rmd
        m=ndimage.binary_dilation(yab,np.ones((5,5)))&(w8[...,0]<0.3)
        E=yumusak_doldur(E,m,n=10,k=11)
        mx=E.max(2); tut=ndimage.binary_opening(mx>10,np.ones((2,2)))|(mx>90)
        lb,nn=ndimage.label(tut)
        if nn: ss=ndimage.sum(mx>10,lb,range(1,nn+1)); tut=np.isin(lb,1+np.where(ss>=10)[0])
        E=ndimage.gaussian_filter(np.where(tut[...,None],E,0),[0.6,0.6,0]); E[860-KY:,1720-KX:]=0; E[:250-KY,1820-KX:]=0; K.append(E)   # sag-alt: skill dugmeleri (UI)
    K=np.stack(K); mx=K.max(3).max(0); ys,xs=np.nonzero(mx>8)
    x0,y0,x1,y1=max(0,xs.min()-6),max(0,ys.min()-6),min(K.shape[2],xs.max()+7),min(K.shape[1],ys.max()+7)
    for n,E in enumerate(K): Image.fromarray(np.clip(E[y0:y1,x0:x1],0,255).round().astype(np.uint8)).save(os.path.join(od,"skill_%02d.png"%n))
    boy=MOB_ZEMIN[1]-MOB_TEPE; X,Yy,W,H=KX+x0,KY+y0,x1-x0,y1-y0
    b=dict(kayit="21-39-19 tablet 2266x1488 (kareler 144-192, 60 kare/sn)",kaynak_kareler_60fps=[EFEKT[0],EFEKT[-1]+1],kare=len(K),fps=60.0,kutu_ekran=[int(X),int(Yy),int(W),int(H)],
           mob_zemin=MOB_ZEMIN,mob_boyu_px=boy,pivot=[round((MOB_ZEMIN[0]-X)/W,4),round(1-(MOB_ZEMIN[1]-Yy)/H,4)],kirmizi_gucu=S)
    np.save(os.path.join(OUT,"mob_maskesi.npy"),rm[y0:y1,x0:x1]); np.save(os.path.join(OUT,"zemin_kutu.npy"),Bt[KY:KY1,KX:KX1][y0:y1,x0:x1].astype(np.uint8)); json.dump(b,open(os.path.join(OUT,"bilgi.json"),"w"),indent=1); print(b)
if __name__=="__main__": calis(sys.argv[1])

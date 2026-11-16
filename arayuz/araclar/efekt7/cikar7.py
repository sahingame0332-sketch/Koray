#!/usr/bin/env python3
"""Kayit 14-01-51 -> iki efekt, her biri iki katman + hedefin kirmizilasma egrisi.
EFEKT1 "kesik_aura" (olay C, oyun zamani 2.76-3.40 sn): hedefte sari kesikler/kivilcimlar + hedefin ARKASINDA pembe-mor aura (gokkusagi kenar)
        + sonda yatay sari parlama.  EFEKT2 "yildiz" (olay B, 1.55-1.85 sn): hedefin ortasinda sari yildiz + hedef kirmizi.
Katmanlar: ARKA = hedef silueti disindaki isik (siluet ici komsudan doldurulur; Unity'de mobun arkasinda, mob ortsun),
           ON   = hedef silueti icindeki isik (mobun onunde).  Eklemeli: E = O - (zemin, kirmizi boyali hedef dahil).
Hedef kirmizisi eklemeli degil (boyama): hedef = lerp(zemin, K(L), s), K: ortak.kirmizi. s(t) her kare icin olculur.
Zemin: min(O - once, O - sonra) (karakter oynuyor). Galeri katmanlari (ipucu, sure kutusu) komsudan doldurulur.
Oyun zamani sure kutusundan; 30 kare/sn'ye en yakin benzersiz kareyle orneklenir."""
import os, sys, json, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
from ortak import *
from zaman import benzersiz
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","efekt7")
KX,KY,KX1,KY1=250,226,1660,1060
HEDEF_ZEMIN=(755,812); HEDEF_UST=230          # hedefin (Chain Scarecrow) zemin merkezi ve tepesi (ekran) -> boy 582 px
EFEKT={"kesik_aura":("C",2.76,3.40),"yildiz":("B",1.55,1.86)}
def kirp(A): return A[KY:KY1,KX:KX1]
def hedef_maskesi(t):
    """hedefin silueti: kirmizi boyandigi karelerin birlesimi"""
    m=np.zeros((1220,2712),bool)
    for ad in ("B","D"):
        E,o,s=OLAY[ad]; B=med(s)
        for i in E:
            O=Y(i); r=(O[...,0]-B[...,0]>45)&(O[...,0]>O[...,1]+70); m|=ndimage.binary_opening(r,np.ones((3,3)))
    l,n=ndimage.label(m); sz=ndimage.sum(m,l,range(1,n+1)); m=l==(1+np.argmax(sz))
    m=ndimage.binary_closing(m,np.ones((9,9))); m=ndimage.binary_fill_holes(m)
    return m
def kirmizi_gucu(O,B,hm):
    L=B.mean(2); K=kirmizi(L); den=K[...,0]-B[...,0]
    v=((O[...,0]-B[...,0])/np.maximum(den,20))[hm&(den>40)]
    return float(np.clip(np.quantile(v,0.3),0,1)) if len(v) else 0.0
def isik(O,Bo,Bs,hm,s):
    D=np.minimum(O-Bo,O-Bs)
    L=Bo.mean(2); P=Bo+s*(kirmizi(L)-Bo)                      # boyali hedef
    Dh=O-P; D=np.where(hm[...,None],Dh,D)
    w8=(np.clip((O.max(2)-242)/13.0,0,1)*(D.max(2)>60))[...,None]   # yalniz gercek doyma (O~255)
    E=np.clip(w8*O+(1-w8)*D,0,255)
    Dp=np.clip(D,0,None); mx=np.maximum(Dp.max(2),1e-3)
    # renk kapisi: sari (R,G >> B), pembe/mor (B ve R), beyaz; yesil baskin (karakter teni, cim) degil
    yesil=(Dp[...,1]>Dp[...,0]*1.3)&(Dp[...,1]>Dp[...,2]*1.6)   # limon sarisi isinlar (G~R) gecer
    kapi=np.clip((mx-18)/20,0,1)*(~yesil)
    yab=(np.minimum(O-Bo,O-Bs).min(2)<-25)&~hm                 # karakter hareketi (kararan)
    m=ndimage.binary_dilation(yab,np.ones((5,5)))&(w8[...,0]<0.3)
    E=E*kapi[...,None]
    om=ovr_maske(); E=yumusak_doldur(E,m|om,n=10,k=11)
    a,b,c,d=KARAKTER; E[b:d,a:c]=0
    return E
def temizle(E,esik=12):
    mx=E.max(2); tut=ndimage.binary_opening(mx>esik,np.ones((2,2)))|(mx>90)
    l,n=ndimage.label(tut)
    if n: s=ndimage.sum(mx>esik,l,range(1,n+1)); tut=np.isin(l,1+np.where(s>=10)[0])
    return ndimage.gaussian_filter(np.where(tut[...,None],E,0),[0.6,0.6,0])
def cikar():
    Z=json.load(open("zaman.json")); hm=hedef_maskesi(Z)
    hm_d=ndimage.binary_dilation(hm,np.ones((5,5)))
    np.save(os.path.join(OUT,"hedef_maskesi.npy") if os.path.isdir(OUT) else "hedef_maskesi.npy",hm)
    bilgi={}
    for ad,(olay,t0,t1) in EFEKT.items():
        E_,o,s=OLAY[olay]; Bo=med(o); Bs=med(s)
        uniq=benzersiz(list(range(E_[0]-12,E_[-1]+8)))
        tt=np.array([Z[i] for i in uniq])
        hedefler=np.arange(t0,t1,1/30.0); sec=[uniq[int(np.argmin(np.abs(tt-t)))] for t in hedefler]
        for kat in ("arka","on"):
            d=os.path.join(OUT,"%s_%s"%(ad,kat)); os.makedirs(d,exist_ok=True)
            for f in os.listdir(d): os.remove(os.path.join(d,f))
        S=[];AR=[];ON=[]
        for n,i in enumerate(sec):
            O=Y(i); sg=kirmizi_gucu(O,Bo,hm); S.append(round(sg,3))
            E=isik(O,Bo,Bs,hm,sg)
            on=np.where(hm_d[...,None],E,0)
            ar=yumusak_doldur(np.where(hm_d[...,None],0,E),hm_d,n=14,k=15)
            AR.append(temizle(kirp(ar))); ON.append(temizle(kirp(on)))
        for kat,K in (("arka",AR),("on",ON)):
            K=np.stack(K); mx=K.max(3).max(0); ys,xs=np.nonzero(mx>8)
            x0,y0,x1,y1=max(0,xs.min()-6),max(0,ys.min()-6),min(K.shape[2],xs.max()+7),min(K.shape[1],ys.max()+7)
            for n,k in enumerate(K): Image.fromarray(np.clip(k[y0:y1,x0:x1],0,255).astype(np.uint8)).save(os.path.join(OUT,"%s_%s"%(ad,kat),"%s_%s_%02d.png"%(ad,kat,n)))
            bilgi.setdefault(ad,{})[kat]=dict(kutu_ekran=[int(KX+x0),int(KY+y0),int(x1-x0),int(y1-y0)])
            print(ad,kat,bilgi[ad][kat]["kutu_ekran"],len(K),"kare")
        bilgi[ad].update(olay=olay,oyun_zamani=[t0,t1],kare=len(sec),fps=30.0,kaynak_kareler=sec,kirmizi_gucu=S,
                         hedef_zemin=list(HEDEF_ZEMIN),hedef_boyu_px=HEDEF_ZEMIN[1]-HEDEF_UST)
        print(ad,'kirmizi',S)
    json.dump(bilgi,open(os.path.join(OUT,"bilgi.json"),"w"),indent=1)
if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); cikar()

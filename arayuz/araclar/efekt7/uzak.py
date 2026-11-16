#!/usr/bin/env python3
"""Efekt 7 eki — uzak kayitlar (16-33-29 = a, 16-33-43 = b; gercek hizda 30 kare/sn, galeri katmani yok).
Efekt 7'nin kareleri DEGISTIRILMEZ. Uzak kayittan:
 (1) gercek zamanlama: her uzak kareye, olcekli efekt 7 karelerinden en iyi oturan (efekt, kare) secilir -> sira tablosu
 (2) hedef kirmizisinin gercek egrisi (uzak karede olculur)
 (3) "yapraklar": hedefin cevresine genis sacilan altin yaprak/kivilcim parcaciklari (yakin kayitta ekran disinda kalmisti)
     = uzak efekt - olcekli efekt 7, efekt 7'nin kapsami disinda kalan sari parcaciklar; hedef zeminine bagli, hedef boyuna gore olcu.
Kullanim: uzak.py KLASOR  (KLASOR/a/k_%04d.png ... kayitlarin 30 kare/sn kareleri; depoya konmaz)"""
import os, sys, json, glob, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
from ortak import kirmizi
B_=os.path.dirname(os.path.abspath(__file__)); K7=os.path.join(B_,"..","..","kaynak","efekt7")
BIL=json.load(open(os.path.join(K7,"bilgi.json"))); HM=np.load(os.path.join(K7,"hedef_maskesi.npy"))
YAKIN_ZEMIN=(755,812); YAKIN_BOY=582
# uzak kayit: hedef zemini (secim halkasi merkezi) + boy (zemin - mighfer tepesi), olculdu
KAYIT={"a":dict(zemin=(1038,698),boy=158,once=range(5,24),sonra=range(104,160),
                devir=[(24,60),(72,104)]),
       "b":None}
ARKA_KAT="arka"
def yakin_isik(ad,n):
    """efekt 7 karesi: arka + on toplam (yakin ekran koordinatinda), hedef silueti icinde arka yok (mob ortuyor)"""
    E=np.zeros((1220,2712,3),np.float32)
    for kat in (ARKA_KAT,"on"):
        x,y,w,h=BIL[ad][kat]["kutu_ekran"]
        A=np.asarray(Image.open(os.path.join(K7,"%s_%s"%(ad,kat),"%s_%s_%02d.png"%(ad,kat,n))).convert("RGB"),dtype=np.float32)
        if kat!="on": A=np.where(HM[y:y+h,x:x+w,None],0,A)
        E[y:y+h,x:x+w]+=A
    return E
def olcekle(A,k,kaynak,hedef,boyut=(1220,2712)):
    """A'yi kaynak noktasi etrafinda k ile olcekleyip hedef noktasina tasir"""
    H,W=boyut; yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
    sx=kaynak[0]+(xx-hedef[0])/k; sy=kaynak[1]+(yy-hedef[1])/k
    if A.ndim==2: return ndimage.map_coordinates(A,[sy,sx],order=1,cval=0)
    return np.stack([ndimage.map_coordinates(A[...,c],[sy,sx],order=1,cval=0) for c in range(A.shape[2])],-1)
def calis(klasor,ad="a"):
    cfg=KAYIT[ad]; fs=sorted(glob.glob(os.path.join(klasor,ad,"k_*.png")))
    Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)
    Bo=np.median([Y(i) for i in cfg["once"]],0); Bs=np.median([Y(i) for i in cfg["sonra"]],0)
    k=cfg["boy"]/YAKIN_BOY; Z=cfg["zemin"]
    hm=olcekle(HM.astype(np.float32),k,YAKIN_ZEMIN,Z)>0.5
    # uzak hedef maskesi: kirmizi karelerden (daha dogru)
    rm=np.zeros(Bo.shape[:2],bool)
    for a0,a1 in cfg["devir"]:
        for i in range(a0,a1):
            O=Y(i); rm|=(O[...,0]-Bo[...,0]>40)&(O[...,0]>O[...,1]+60)
    rm=ndimage.binary_opening(rm,np.ones((2,2))); l,n=ndimage.label(rm); s=ndimage.sum(rm,l,range(1,n+1)); rm=l==(1+np.argmax(s))
    rm=ndimage.binary_fill_holes(ndimage.binary_closing(rm,np.ones((5,5))))
    # aday kareler (olcekli, onceden)
    pen=(slice(Z[1]-260,Z[1]+60),slice(Z[0]-260,Z[0]+260))
    aday={}
    for e in ("kesik_aura","yildiz"):
        for n in range(BIL[e]["kare"]): aday[(e,n)]=olcekle(yakin_isik(e,n),k,YAKIN_ZEMIN,Z)[pen]
    L=Bo.mean(2); Kr=kirmizi(L)
    SIRA=[("kesik_aura",n) for n in range(BIL["kesik_aura"]["kare"])]+[("yildiz",n) for n in range(BIL["yildiz"]["kare"])]
    tablo=[]
    for a0,a1 in cfg["devir"]:
        C=[];S=[];ii=list(range(a0,a1))
        for i in ii:
            O=Y(i)
            v=((O[...,0]-Bo[...,0])/np.maximum(Kr[...,0]-Bo[...,0],20))[rm&(Kr[...,0]-Bo[...,0]>40)]
            s=float(np.clip(np.quantile(v,0.6),0,1)) if len(v) else 0.0; S.append(s)
            P=np.where(rm[...,None],Bo+s*(Kr-Bo),Bo); hed=np.clip(O-P,0,255)[pen]
            C.append([float(np.abs(hed).mean())]+[float(np.abs(hed-aday[q]).mean()) for q in SIRA])
        C=np.array(C)                         # sutun 0 = efekt yok
        # DTW: once "yok", sonra SIRA'da monoton ilerleme (kare tekrar/atlama serbest, en fazla 3 atlama), sonra "yok"
        T,M=C.shape; INF=1e9; dp=np.full((T,M),INF); bk=np.zeros((T,M),int)
        dp[0,0]=C[0,0]; dp[0,1]=C[0,1]
        for t in range(1,T):
            for m in range(M):
                if m==0: cands=[(dp[t-1,0],0)]
                else:
                    cands=[(dp[t-1,j],j) for j in range(max(0,m-4),m+1) if j<M]
                    if m>=1: cands.append((dp[t-1,0],0))
                v,j=min(cands); dp[t,m]=v+C[t,m]; bk[t,m]=j
        # bitis: son karede ya SIRA sonu ya da sonrasi "yok" -> son satirin en iyisi
        m=int(np.argmin(dp[-1])); yol=[m]
        for t in range(T-1,0,-1): m=bk[t,m]; yol.append(m)
        yol=yol[::-1]
        dev=[]
        for t,(i,m) in enumerate(zip(ii,yol)):
            e,n=("yok",-1) if m==0 else SIRA[m-1]
            dev.append(dict(kayit_kare=i,efekt=e,kare=n,kirmizi=round(S[t],3),fark=round(float(C[t,m]),2)))
        tablo.append(dev)
    json.dump(dict(kayit=ad,olcek=k,hedef_zemin=Z,hedef_boy=cfg["boy"],devirler=tablo),open(os.path.join(K7,"uzak_zamanlama_%s.json"%ad),"w"),indent=1)
    for dev in tablo: print([(d["kayit_kare"],d["efekt"][:5],d["kare"],d["kirmizi"]) for d in dev])
if __name__=="__main__": calis(sys.argv[1])

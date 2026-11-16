#!/usr/bin/env python3
"""Efekt 7 eki — uzak (gercek hizli) kayitlarla zamanlama + yapraklar katmani. Efekt 7 kareleri degismez; '_tum' kare dizileri
(yakin kayittaki tum benzersiz kareler, cikar7.py --tum) gercek zamana DTW ile eslenir.
Ozellikler (her kare): hedef kirmizisi s, pembe aura enerjisi, sari isik enerjisi (hedefe gore olcekli bolgede), her biri 0-1'e olcekli.
Cikti: kaynak/efekt7/uzak_<kayit>.json (devir basina: kayit karesi -> (efekt, tum kare), kirmizi s), yapraklar_<kayit>/ kareleri.
Kullanim: uzak2.py KLASOR [a|b]"""
import os, sys, json, glob, numpy as np
from PIL import Image
from scipy import ndimage
from ortak import kirmizi
from uzak import yakin_isik, olcekle, BIL, HM, K7, YAKIN_ZEMIN, YAKIN_BOY
KAYIT={"a":dict(zemin=(1038,698),boy=158,once=range(5,24),sonra=range(104,160),devir=[(24,62),(72,104)]),
       "b":dict(zemin=None,boy=None,once=None,sonra=None,devir=None)}
SIRA=[("kesik_aura_tum",n) for n in range(BIL["kesik_aura_tum"]["kare"])]+[("yildiz_tum",n) for n in range(BIL["yildiz_tum"]["kare"])]
def ozellik(E,s,hm):
    """E: eklemeli isik (hedef cevresi), s: kirmizi -> (s, pembe, sari)"""
    R,G,B=E[...,0],E[...,1],E[...,2]
    pem=np.clip(B-G,0,None)*(~hm); sar=np.clip(np.minimum(R,G)-B,0,None)
    return np.array([s,pem.sum(),sar.sum()],np.float64)
def yakin_ozellikleri():
    F=[]
    for e,n in SIRA:
        E=yakin_isik(e,n); F.append(ozellik(E,BIL[e]["kirmizi_gucu"][n],HM))
    return np.array(F)
def dtw(Fu,Fy):
    """Fu: uzak (T x 3, 0-1), Fy: yakin (M x 3); sutun -1 = efekt yok (ozellik 0). Monoton, atlama <= 6"""
    Fy=np.vstack([np.zeros(3),Fy]); T,M=len(Fu),len(Fy)
    C=np.array([[np.abs(Fu[t]-Fy[m]).sum() for m in range(M)] for t in range(T)])
    dp=np.full((T,M),1e9); bk=np.zeros((T,M),int); dp[0,0]=C[0,0]; dp[0,1]=C[0,1]
    for t in range(1,T):
        for m in range(M):
            c=[(dp[t-1,j],j) for j in range(max(0,m-6),m+1)]
            if m>0: c.append((dp[t-1,0],0))
            v,j=min(c); dp[t,m]=v+C[t,m]; bk[t,m]=j
    m=int(np.argmin(dp[-1])); yol=[m]
    for t in range(T-1,0,-1): m=bk[t,m]; yol.append(m)
    return yol[::-1]
def calis(klasor,ad):
    cfg=KAYIT[ad]; fs=sorted(glob.glob(os.path.join(klasor,ad,"k_*.png")))
    Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)
    Bo=np.median([Y(i) for i in cfg["once"]],0); Bs=np.median([Y(i) for i in cfg["sonra"]],0)
    k=cfg["boy"]/YAKIN_BOY; Z=cfg["zemin"]; hm=olcekle(HM.astype(np.float32),k,YAKIN_ZEMIN,Z)>0.5
    rm=np.zeros(Bo.shape[:2],bool)
    for a0,a1 in cfg["devir"]:
        for i in range(a0,a1): O=Y(i); rm|=(O[...,0]-Bo[...,0]>40)&(O[...,0]>O[...,1]+60)
    rm=ndimage.binary_opening(rm,np.ones((2,2))); l,n=ndimage.label(rm); sz=ndimage.sum(rm,l,range(1,n+1)); rm=l==(1+np.argmax(sz))
    rm=ndimage.binary_fill_holes(ndimage.binary_closing(rm,np.ones((5,5)))); np.save(os.path.join(K7,"uzak_hedef_%s.npy"%ad),rm)
    L=Bo.mean(2); Kr=kirmizi(L)
    pen=(slice(max(0,Z[1]-int(560*k)),Z[1]+int(120*k)),slice(Z[0]-int(700*k),Z[0]+int(700*k)))   # yakin kutuyla ayni bolge
    Fy=yakin_ozellikleri(); olc=Fy.max(0)+1e-6
    sonuc=[]
    for a0,a1 in cfg["devir"]:
        Fu=[];S=[];ii=list(range(a0,a1))
        for i in ii:
            O=Y(i); v=((O[...,0]-Bo[...,0])/np.maximum(Kr[...,0]-Bo[...,0],20))[rm&(Kr[...,0]-Bo[...,0]>40)]
            s=float(np.clip(np.quantile(v,0.6),0,1)) if len(v) else 0.0; S.append(s)
            P=np.where(rm[...,None],Bo+s*(Kr-Bo),Bo); D=np.clip(np.minimum(O-Bo,O-Bs-(P-Bo)),0,255)
            f=ozellik(D[pen],s,rm[pen]); f[1:]/=k*k; Fu.append(f)       # alan olcegi
        Fu=np.array(Fu)/olc; yol=dtw(Fu,Fy/olc)
        dev=[]
        for i,m,s in zip(ii,yol,S):
            e,n=("yok",-1) if m==0 else SIRA[m-1]; dev.append(dict(kayit_kare=i,efekt=e,kare=n,kirmizi=round(s,3)))
        sonuc.append(dev); print([(d["kayit_kare"],d["efekt"][:5],d["kare"],d["kirmizi"]) for d in dev])
    json.dump(dict(kayit=ad,olcek=k,hedef_zemin=Z,hedef_boy=cfg["boy"],devirler=sonuc),open(os.path.join(K7,"uzak_%s.json"%ad),"w"),indent=1)
if __name__=="__main__": calis(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else "a")

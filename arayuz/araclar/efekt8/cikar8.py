#!/usr/bin/env python3
"""Efekt 8: kayit 19-16-21 (tablet 2266x1488, gercek hiz, 60 -> 30 kare/sn). Ayni skill (kesik + aura -> yildiz) ucuncu bir acidan.
YALNIZ SKILL ISIGI cikarilir (mobun hasar kirmizisi haric): E = O - P, P = efektsiz zemin; mob siluetinde P kirmizi boyanmis zemin
(R = 0.60L+162, G = 0.95L+5, B = 0.75L; guc s her karede olculur). Oyuncu hareketi: min(O-Bonce, O-Bsonra); kararan / yesil artan dolgu.
Opak UI (etiketler, skill dugmeleri) zaten degismiyor -> E = 0.
Kullanim: cikar8.py KLASOR (KLASOR/k_%04d.png, 30 kare/sn; kayit depoya konmaz)"""
import os, sys, json, glob, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","kaynak","efekt8")
KX,KY,KX1,KY1=700,150,2266,1300
MOB_ZEMIN=(1508,917); MOB_TEPE=495; OYUNCU_AYAK=(1135,1050)
ONCE=range(30,58); SONRA=range(86,95); EFEKT=range(59,85)
def kirmizi(L): return np.stack([0.60*L+162,0.95*L+5,0.75*L],-1)
def calis(k):
    fs=sorted(glob.glob(os.path.join(k,"k_*.png")))
    Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB"),dtype=np.float32)[KY:KY1,KX:KX1]
    Bo=np.median([Y(i) for i in ONCE],0); Bs=np.median([Y(i) for i in SONRA],0)
    rm=np.zeros(Bo.shape[:2],bool)
    for i in EFEKT:
        O=Y(i); rm|=ndimage.binary_opening((O[...,0]-Bo[...,0]>45)&(O[...,0]>O[...,1]+70),np.ones((3,3)))
    kut=np.zeros_like(rm); kut[470-KY:960-KY,1380-KX:1700-KX]=True; rm&=kut          # yalniz mob (oyuncunun kirmizi kilici degil)
    l,n=ndimage.label(rm); sz=ndimage.sum(rm,l,range(1,n+1)); rm=l==(1+np.argmax(sz))
    # siki maske: mob tam kirmiziyken (kareler 79-81) kirmiziya donen pikseller; cim/cit maskeye girmesin
    sik=np.zeros_like(rm)
    for i in range(79,82):
        O=Y(i); sik|=((O[...,0]-Bo[...,0])>35)&(O[...,0]>O[...,1]+55)
    rm=ndimage.binary_closing(rm&ndimage.binary_dilation(sik,np.ones((3,3))),np.ones((3,3))); rmd=ndimage.binary_dilation(rm,np.ones((3,3)))
    Kr=kirmizi(Bo.mean(2)); os.makedirs(OUT,exist_ok=True)
    od=os.path.join(OUT,"skill"); os.makedirs(od,exist_ok=True)
    for f in os.listdir(od): os.remove(os.path.join(od,f))
    S=[]; K=[]
    for i in EFEKT:
        O=Y(i)
        # s: mob icinde, isiksiz piksellerde (sari/beyaz isik disarida) en kucuk kareler: O = B + s (K - B)
        q=rm&(Kr[...,0]-Bo[...,0]>40)&~((O[...,1]-Bo[...,1])>25)
        dK=(Kr-Bo)[q]; dO=(O-Bo)[q]
        s=float(np.clip((dK*dO).sum()/max((dK*dK).sum(),1e-6),0,1)) if q.sum()>50 else 0.0; S.append(round(s,3))
        P=np.where(rm[...,None],Bo+s*(Kr-Bo),Bo)
        D=np.where(rmd[...,None],O-P,np.minimum(O-Bo,O-Bs))
        w8=(np.clip((O.max(2)-242)/13.0,0,1)*(D.max(2)>60))[...,None]
        E=np.clip(w8*O+(1-w8)*D,0,255)
        Dp=np.clip(D,0,None); yesil=(Dp[...,1]>Dp[...,0]*1.3)&(Dp[...,1]>Dp[...,2]*1.6)
        # mob icinde: kirmizi boyama artigi (saf kirmizi ya da camgobegi denge) isik degil; yalniz sari/beyaz/pembe isik kalir
        artik=rmd&(((Dp[...,0]>2.2*Dp[...,1]+10)&(Dp[...,0]>2*Dp[...,2]+10))|((Dp[...,1]+Dp[...,2])>2.6*Dp[...,0]+20))
        E=E*(np.clip((Dp.max(2)-14)/18,0,1)*~yesil*~artik)[...,None]
        yab=(np.minimum(O-Bo,O-Bs).min(2)<-25)&~rmd
        m=ndimage.binary_dilation(yab,np.ones((5,5)))&(w8[...,0]<0.3)
        E=yumusak_doldur(E,m,n=10,k=11)
        mx=E.max(2); tut=ndimage.binary_opening(mx>12,np.ones((2,2)))|(mx>90)
        lb,nn=ndimage.label(tut)
        if nn: ss=ndimage.sum(mx>12,lb,range(1,nn+1)); tut=np.isin(lb,1+np.where(ss>=10)[0])
        E=ndimage.gaussian_filter(np.where(tut[...,None],E,0),[0.6,0.6,0]); K.append(E)
    K=np.stack(K); mx=K.max(3).max(0); ys,xs=np.nonzero(mx>8)
    x0,y0,x1,y1=max(0,xs.min()-6),max(0,ys.min()-6),min(K.shape[2],xs.max()+7),min(K.shape[1],ys.max()+7)
    for n,E in enumerate(K): Image.fromarray(np.clip(E[y0:y1,x0:x1],0,255).round().astype(np.uint8)).save(os.path.join(od,"skill_%02d.png"%n))
    boy=MOB_ZEMIN[1]-MOB_TEPE; X,Yy,W,H=KX+x0,KY+y0,x1-x0,y1-y0
    b=dict(kayit="19-16-21 tablet 2266x1488",kaynak_kareler=[EFEKT[0],EFEKT[-1]+1],kare=len(K),fps=30.0,kutu_ekran=[int(X),int(Yy),int(W),int(H)],
           mob_zemin=MOB_ZEMIN,mob_boyu_px=boy,genislik_mob_boyu=round(W/boy,4),en_boy=round(H/W,4),
           pivot=[round((MOB_ZEMIN[0]-X)/W,4),round(1-(MOB_ZEMIN[1]-Yy)/H,4)],kirmizi_gucu=S,oyuncu_ayak=OYUNCU_AYAK)
    json.dump(b,open(os.path.join(OUT,"bilgi.json"),"w"),indent=1); np.save(os.path.join(OUT,"mob_maskesi.npy"),rm)
    np.save(os.path.join(OUT,"zemin.npy"),Bo.astype(np.uint8)); print(b)
if __name__=="__main__": calis(sys.argv[1])

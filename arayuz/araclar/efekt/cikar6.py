#!/usr/bin/env python3
"""Altinci set: yakin dovus skill'leri Stroke / Stab / Stab2 (telefon kaydi 2712x1220, 30 kare/sn; kamera sabit).
Her skill iki katman: KARAKTER (kesik yaylari + kivilcimlar, karakterin ayagina bagli) ve HEDEF (gokten isin + vurus patlamasi
+ yildiz parlamasi, hedefin zeminine bagli). Toplam = O - B (eklemeli); B = once/sonra medyanlarinin ikisi: min(O-Bonce, O-Bsonra)
hareket eden solucani ve karakteri dusurur. Hedef secim halkasi (sari-beyaz, hedef secildiginde cikan UI isareti; efekt degil):
halkali-efektsiz karelerden maskesi cikarilip komsu isiktan doldurulur. Isin icin ayrisik model (isin_modeli). UI (hedef cubugu, etiketler, skill dugmeleri) bantlari doldurulur.
Kullanim: cikar6.py VIDEO   (kayit depoya konmaz; tam kare saklanmaz, yalniz efekt kareleri)"""
import os, sys, json, glob, subprocess, tempfile, atexit, shutil
import numpy as np
from PIL import Image
from scipy import ndimage
from cikar import OUT
from cikar2 import yumusak_doldur, dikey_doldur
KX,KY,KW,KH=560,0,1600,1140                     # calisma kutusu (alt cubuk y>=1140 disarida)
UI_DIKEY=[(1160,0,1600,138),                    # hedef cubugu "Worm" + Show Drops (yalniz hedef seciliyken)
          (1250,455,1468,558),                  # JustForFARM / xDarkPast + can cubugu (isinin onunde)
          (1205,352,1530,400),(1258,398,1415,442)]  # "Earth worm" yazisi + yaratik (isinin onunde)
UI_DOLGU=[(1772,690,2160,1080)]                  # skill dugmeleri (bekleme sayaci degisir)
GOVDE=(1378,715,120,175)                         # karakter govdesi (hareket araligi dahil) elipsi
#        ad,      once,          sonra,          aralik,          hedef (halka merkezi), halka (rx,ry), halka kareleri, halkasiz
SKILL=[("stroke", range(33,44),  range(80,95),   range(45,78),    (1307,983),  (138,131), (72,75),  range(80,95)),
       ("stab",   range(97,108), range(143,160), range(109,136),  (1175,1119), (164,117), (136,141),range(143,160)),
       ("stab2",  range(186,200),range(222,240), range(202,218),  None, None, None, None)]
AYAK=(1372,832); BOY=242                          # karakterin dinlenme ayagi (ekran) ve boyu (px) - olculdu
_G=[]; atexit.register(lambda: [shutil.rmtree(d,ignore_errors=True) for d in _G])
def kareler(video):
    d=tempfile.mkdtemp(); _G.append(d)
    subprocess.run(["ffmpeg","-v","error","-y","-i",video,"-vf","fps=30,crop=%d:%d:%d:%d"%(KW,KH,KX,KY),d+"/k_%04d.png"],check=True)
    return sorted(glob.glob(d+"/k_*.png"))
def Y(f): return np.asarray(Image.open(f).convert("RGB")).astype(np.float32)
def kutu_maske(L):
    m=np.zeros((KH,KW),bool)
    for a,b,c,d in L: m[max(0,b-KY):d-KY,max(0,a-KX):c-KX]=True
    return m
def temizle(E,esik=16,koru=None):
    mx=E.max(2)
    tut=ndimage.binary_opening(mx>esik,np.ones((2,2)))|(mx>110)
    l,n=ndimage.label(tut)
    if n:
        s=ndimage.sum(mx>esik,l,range(1,n+1)); tut=np.isin(l,1+np.where(s>=8)[0])
    if koru is not None: tut|=koru                                      # isin bulutu: esikle kesilmez (yumusak kenar)
    E=np.where(tut[...,None],E,0)
    return ndimage.gaussian_filter(E,[0.6,0.6,0])
def _doldur1(I,v):
    i=np.arange(len(I))
    if not v.any(): return np.ones_like(I)
    return np.interp(i,i[v],I[v])
def isin_modeli(Es,p,T,gecersiz,U0=300,esik=35.0):
    """Gokten inen isin: E(x,y) ~ I(y) * P(x - cizgi(y)) (cizgi boyunca ayrisik). Isinin altindaki zemin dokusu (agac govdesi, cim,
    doyan gok) modele girmez; modelin uzerinde kalan guclu artis (kivilcim, kesik) korunur. Patlamaya yaklasirken orijinale gecer."""
    ust=int(T[1]-KY-120); rows=np.arange(0,ust); U=np.arange(-U0,U0+1)
    X=(p[0]-KX+p[1]*(rows+KY))[:,None]+U[None,:]; Xi=np.clip(np.round(X).astype(int),0,KW-1)
    V=(~gecersiz[rows[:,None],Xi])&(X>=0)&(X<KW)
    gec=np.clip((ust-rows)/180.0,0,1)[:,None,None]                   # son 180 satirda orijinale yumusak gecis
    tah=rows<ust-180                                                  # I(y) yalniz patlamadan uzak satirlardan (yildiz/patlama karismasin)
    out=Es.copy()
    for n,E in enumerate(Es):
        S=E[rows[:,None],Xi]; I=np.ones(len(rows))
        cek=np.where(V[:,U0-15:U0+16],S[:,U0-15:U0+16].max(2),np.nan)[tah]
        if not np.isfinite(cek).any() or np.nanmedian(np.nanmean(cek,1))<25: continue   # bu karede isin yok: model kurulmaz
        for _ in range(3):
            Sm=np.where(V[...,None],S/np.maximum(I,1e-3)[:,None,None],np.nan); P=np.nan_to_num(np.nanmedian(Sm,0))
            P=ndimage.median_filter(P,size=(7,1))                          # tek sutunluk cukurlar (agac govdesi izi)
            P=np.clip(P-np.median(np.concatenate([P[:40],P[-40:]]),0),0,None)   # kenardaki gurultu tabani
            P*=np.clip((U0-np.abs(U))/80.0,0,1)[:,None]                      # kenarda yumusak sonum
            core=P.max(1)>0.3*max(P.max(),1)
            r=np.where(V[:,core,None],S[:,core]/np.maximum(P[core],1)[None],np.nan).reshape(len(rows),-1)
            ok=(np.isfinite(r).sum(1)>20)&tah; I=np.nanmedian(np.where(ok[:,None],r,0),1); I=_doldur1(np.nan_to_num(I),ok)
            I=np.clip(ndimage.gaussian_filter1d(I,12),0,3)
        if P.max()<20:                                                   # isin yok (sonmus): model kurulmaz
            continue
        M=I[:,None,None]*P[None]
        F=M+np.clip(S-M-esik,0,None)*V[...,None]                         # gecersiz (gok, UI) bolgede yalniz model
        F=gec*F+(1-gec)*S
        Z=out[n]; Z[rows[:,None],Xi]=F
    return out
def cikar(video):
    fs=kareler(video)
    yy,xx=np.mgrid[0:KH,0:KW]; gx,gy,rx,ry=GOVDE
    gov=ndimage.gaussian_filter(np.clip(1.15-np.hypot((xx+KX-gx)/rx,(yy+KY-gy)/ry),0,1),6)
    uid=kutu_maske(UI_DIKEY); uif=kutu_maske(UI_DOLGU)
    sonuc={}
    sec=set(sys.argv[2:])
    for ad,once,sonra,aralik,T,R,hk,hsiz in SKILL:
        if sec and ad not in sec: continue
        Bo=np.median(np.stack([Y(fs[i]) for i in once]),0); Bs=np.median(np.stack([Y(fs[i]) for i in sonra]),0)
        gok=None
        if T:
            rr=np.hypot((xx+KX-T[0])/R[0],(yy+KY-T[1])/R[1]); band=(rr>0.66)&(rr<1.30)
            Hs=np.median(np.stack([Y(fs[i]) for i in hsiz]),0)
            Ht=np.median(np.stack([Y(fs[i]) for i in range(*hk)]),0)-Hs        # halka sablonu (eklemeli yaklasim)
            Ht=np.where(band[...,None],np.clip(Ht,0,255),0)
            halka=ndimage.binary_dilation(ndimage.binary_opening(Ht.max(2)>15,np.ones((3,3))),np.ones((13,13)))  # halka pikselleri (+6 px)
            gok=ndimage.binary_dilation((Bo.mean(2)>140)&(yy<330),np.ones((5,5)))   # parlak gok / uzak zemin: eklemeli isik doyar
            yakin=(np.hypot(xx+KX-T[0],(yy+KY-T[1])*1.25)<300)&((yy+KY)>T[1]-280)
        Es=[]
        for i in aralik:
            O=Y(fs[i]); D=np.minimum(O-Bo,O-Bs)
            etk=(O[...,0]>150)&(O[...,1]<140)&(O[...,2]<140)&(O[...,0]-O[...,1]>75)&(O[...,0]-O[...,2]>70)   # kirmizi "Worm"/"Earth worm" etiketleri
            etk=ndimage.binary_dilation(etk,np.ones((7,7)))
            if T:
                etk|=halka                                                  # secim halkasi da efekt degil
                sol=(O[...,2]<0.33*O[...,0])&(O[...,1]<0.62*O[...,0])&(O[...,0]>90)&(O[...,0]<238)&yakin   # hedef solucanin turuncu govdesi
                etk|=ndimage.binary_dilation(ndimage.binary_opening(sol,np.ones((3,3))),np.ones((9,9)))
            w8=(np.clip((O.max(2)-215)/35.0,0,1)*(D.max(2)>40)*~etk)[...,None]  # doyan cekirdek: isigin kendi rengi
            E=np.clip(w8*O+(1-w8)*D,0,255)
            yab=(np.minimum(O-Bo,O-Bs).min(2)<-22)                                                             # karakter/solucan hareketi
            ok_=ndimage.binary_dilation((D[...,1]>D[...,2]+8)&(D[...,0]<0.75*D[...,1])&(D.max(2)>20),np.ones((15,15)))   # yesil hedef oku (koyu yesil; limon sarisi kesik degil)
            yab|=(O.max(2)<160)&(O[...,1]<0.6*O[...,0])&(O[...,2]<0.6*O[...,0])                               # kizil-kahve solucan govdesi
            m=(ndimage.binary_dilation(yab,np.ones((5,5)))|ok_)&(w8[...,0]<0.3)
            Dp=np.clip(D,0,None); mx=np.maximum(Dp.max(2),1e-3)
            kapi=np.clip((Dp[...,0]/mx-0.80)/0.08,0,1)*(Dp[...,2]<=Dp[...,0]+2)  # renk: kirmizi baskin ya da limon sarisi (R >= 0.8 G); mavi R'yi gecmez
            kapi=np.maximum(kapi,np.clip((Dp.min(2)-np.where(gov>0.3,999.0,60.0))/20.0,0,1))   # beyaz-mavimsi parlak cekirdek
            sicak=np.clip(((Dp[...,0]-Dp[...,2])/mx-0.15)/0.2,0,1)               # govdede: gri/beyaz zirh degil, sicak artis olmali
            kapi*=1-gov*(O.max(2)<235)*np.maximum(0.55,1-sicak)            # govde: hareket izi zayiflatilir
            E=E*kapi[...,None]
            E=yumusak_doldur(E,m|uif|uid|etk,n=10,k=11)                    # halka, etiketler, UI: komsu isiktan doldur (isin bantlari isin modelinde)
            E[:300,1430:]=0                                                # sag ust: uzak yaratik hareketi
            Es.append(E)
        Es=np.stack(Es)
        # hedef katman agirligi: isin cizgisi + vurus diski
        w=np.zeros((KH,KW),np.float32); cizgi=None; koru=None
        if T:
            S=Es.sum(0).sum(2); ys=np.arange(150,760,10); xs=[]
            for y in ys:
                lo=max(0,T[0]-KX-450); hi=T[0]-KX+150; r=ndimage.uniform_filter1d(S[y-5:y+5].sum(0),25)[lo:hi]; xs.append(lo+np.argmax(r)+KX)
            xs=np.array(xs,float); A=np.stack([np.ones_like(ys),ys],1).astype(float)
            for _ in range(3):
                p=np.linalg.lstsq(A,xs,rcond=None)[0]; e=np.abs(A@p-xs); k=e<max(15,np.quantile(e,.7)); A,xs,ys=A[k],xs[k],ys[k]
            cizgi=[float(p[0]),float(p[1])]
            xl=p[0]+p[1]*(yy+KY); dl=np.abs(xx+KX-xl)/np.sqrt(1+p[1]**2)
            wb=np.clip((310-dl)/60,0,1)*((yy+KY)<T[1]+40)              # isin bulutu (model genisligi +-300)
            wd=np.clip((300-np.hypot((xx+KX-T[0]),(yy+KY-T[1])*1.25))/80,0,1)
            w=np.maximum(wb,wd)
            Es=isin_modeli(Es,p,T,gok|uid|uif)
            koru=(dl<300)&((yy+KY)<T[1]-120)
        w=ndimage.gaussian_filter(w,4)[None,...,None]
        kat={"karakter":Es*(1-w),"hedef":Es*w} if T else {"karakter":Es}
        bilgi={}
        for kn,K in kat.items():
            K=np.stack([temizle(k,koru=koru if kn=="hedef" else None) for k in K]); mx=K.max(3).max(0)
            ys_,xs_=np.nonzero(mx>8); x0,x1,y0,y1=xs_.min()-6,xs_.max()+7,ys_.min()-6,ys_.max()+7
            x0,y0=max(0,x0),max(0,y0); x1,y1=min(KW,x1),min(KH,y1)
            od=os.path.join(OUT,"yakin_%s_%s"%(ad,kn)); os.makedirs(od,exist_ok=True)
            for f in glob.glob(od+"/*.png"): os.remove(f)
            for n,k in enumerate(K):
                Image.fromarray(np.clip(k[y0:y1,x0:x1],0,255).astype(np.uint8)).save(os.path.join(od,"%s_%s_%02d.png"%(ad,kn,n)))
            cap=AYAK if kn=="karakter" else T
            bilgi[kn]=dict(kutu_ekran=[int(x0+KX),int(y0+KY),int(x1-x0),int(y1-y0)],capa_ekran=list(cap),
                           pivot=[round((cap[0]-x0-KX)/(x1-x0),4),round(1-(cap[1]-y0-KY)/(y1-y0),4)],
                           genislik_karakter_boyu=round((x1-x0)/BOY,4),kare_sayisi=len(K),
                           parlaklik=[round(float(k.max(2).mean()),2) for k in K])
            print(ad,kn,bilgi[kn]["kutu_ekran"],"pivot",bilgi[kn]["pivot"],len(K),"kare")
        sonuc[ad]=dict(kaynak_kareler=[aralik[0],aralik[-1]+1],fps=30.0,karakter_ayak=list(AYAK),karakter_boyu_px=BOY,
                       hedef=list(T) if T else None,hedef_halka=list(R) if R else None,isin_cizgisi_x_eq_a_plus_b_y=cizgi,katmanlar=bilgi)
    p=os.path.join(OUT,"efekt_bilgisi.json"); r=json.load(open(p)) if os.path.exists(p) else {}
    r.update({"yakin_"+k:v for k,v in sonuc.items()}); json.dump(r,open(p,"w"),indent=1)
if __name__=="__main__": cikar(sys.argv[1])

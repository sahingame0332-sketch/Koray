#!/usr/bin/env python3
"""Ikinci efekt seti (2712 x 1220 telefon kayitlari): Fire Burst, Fire Blade, karaktere vurus (tam hali).
Yontem cikar.py ile ayni (eklemeli katman: E = clip(O - B, 0, 255)) + iki ek temizlik:
  * sabit katman: zemine gore degisen ama efekt suresince SABIT kalan pikseller (yeni beliren UI: "Open" dugmesi,
    ad etiketleri) -> komsulardan doldurulur;
  * sicak olmayan artik: ad/can cubugu kaymasi, yaratik hareketi, cim dokusunun alt-piksel kaymasi -> silinir.
Kullanim: cikar2.py VIDEO_A VIDEO_B   (a: 09-51-10, b: 09-56-57 kaydi; depoya konmaz)"""
import os, sys, json, subprocess, tempfile, glob
import numpy as np
from PIL import Image
from scipy import ndimage
from cikar import doldur, OUT
def kareler(video,kutu,secim):
    x,y,w,h=kutu
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg","-v","error","-y","-i",video,"-vf","crop=%d:%d:%d:%d"%(w,h,x,y),"-vsync","0",d+"/k_%04d.png"],check=True)
        fs=sorted(glob.glob(d+"/k_*.png"))
        return {i:np.asarray(Image.open(fs[i]).convert("RGB")).astype(np.float32) for i in secim}
def temizle(E,esik=24):
    mx=E.max(2); sicak=(E[:,:,0]-E[:,:,2])>18
    tut=(sicak&(mx>esik))|(mx>150)                  # beyaz-sicak cekirdek ve beyaz girdap (Fire Blade) kalir
    tut=ndimage.binary_opening(tut,np.ones((2,2)))
    E=np.where(tut[...,None],E,0)
    E[:,:,1]=np.minimum(E[:,:,1],E[:,:,0])            # ates/vurus isigi: G <= R (yesil cim artigi kalmasin)
    return ndimage.gaussian_filter(E,[0.6,0.6,0])
def yumusak_doldur(E,m,n=14,k=17):
    """izotropik doldurma, genis yumusatma: kutu izi kalmasin"""
    if not (~m).any(): return E
    _,(iy,ix)=ndimage.distance_transform_edt(m,return_indices=True)
    F=E[iy,ix]
    for _ in range(n):
        Y=ndimage.uniform_filter(F,[k,k,0]); F=np.where(m[...,None],Y,E)
    return F
def dikey_doldur(E,m):
    """m icini sutun boyunca (ust/alt bilinen pikseller arasinda) dogrusal doldurur: isin ve halka gibi dikey
    surekliligi olan efektlerde etiket bantlarinin altini dogal kapatir"""
    F=E.copy(); H=E.shape[0]; y=np.arange(H)
    for x in np.where(m.any(0))[0]:
        b=~m[:,x]
        if not b.any(): continue
        for c in range(3): F[:,x,c]=np.interp(y,y[b],E[b,x,c])
    Y=ndimage.uniform_filter(F,[1,5,0])
    return np.where(m[...,None],Y,E)
def sira(ad,video,kutu,once,aralik,maskeler=(),siluet=None,fps_kayit=None,dikey=False,kes=None):
    secim=sorted(set(list(once)+list(aralik)))
    K=kareler(video,kutu,secim)
    B=np.median(np.stack([K[i] for i in once]),0)
    H,W=B.shape[:2]
    St=np.stack([K[i] for i in aralik])
    degisti=(np.abs(St-B).max(3)>25).mean(0)>0.9            # neredeyse her karede zeminden farkli
    sabit=(St.std(0).max(2)<6)                              # ve kendi icinde sabit -> UI katmani
    U=ndimage.binary_dilation(degisti&sabit,np.ones((5,5)))
    for (a,b,c,d) in maskeler: U[max(0,b-kutu[1]):d-kutu[1],max(0,a-kutu[0]):c-kutu[0]]=True
    os.makedirs(os.path.join(OUT,ad),exist_ok=True)
    for f in glob.glob(os.path.join(OUT,ad,"*.png")): os.remove(f)
    par=[]
    for n,i in enumerate(aralik):
        D=K[i]-B; E=np.clip(D,0,255); m=U.copy()
        S=np.zeros_like(m)
        for (a,b,c,d) in (siluet or ()):
            S[max(0,b-kutu[1]):d-kutu[1],max(0,a-kutu[0]):c-kutu[0]]=True
        if dikey: m|=S
        else:
            # silüet kutusunda yalniz isik olamayacak pikseller (kararan / sicak olmayan) doldurulur
            yanlis=(D.min(2)<-12)|((D[:,:,2]>D[:,:,0]+8)&(D.max(2)>20))
            m|=S&ndimage.binary_dilation(yanlis,np.ones((5,5)))
        m=ndimage.binary_dilation(m,np.ones((9,9)))     # etiket kenar artiklari dolguya karismasin
        if m.any(): E=dikey_doldur(E,m) if dikey else yumusak_doldur(E,m)
        # eklemeli isik zemini karartamaz: kararan pikseller onde hareket eden karakter/yaratik -> doldur
        yabanci=(D.min(2)<-20)|((D.max(2)>25)&((D[:,:,1]>D[:,:,0]+12)|(D[:,:,2]>D[:,:,0])))   # yesil/mavi: yaratik, cim
        k=ndimage.binary_dilation(yabanci,np.ones((7,7)))&~m
        if k.any() and (~k).any(): E=yumusak_doldur(E,k)
        # parlak isigin icinde kalan karanlik delikler (ortadaki karakter/beyaz cekirdek) -> doldur
        mx=E.max(2); delik=(ndimage.binary_fill_holes(mx>40)|(ndimage.uniform_filter(mx,61)>90))&(mx<=40)
        if delik.any(): E=yumusak_doldur(E,ndimage.binary_dilation(delik,np.ones((5,5))))
        if kes and i>=kes[0]:
            # baska efektin (oyuncuya vurus) baslangici: oyuncu cevresi yumusak kenarla silinir
            cx,cy,r=kes[1]-kutu[0],kes[2]-kutu[1],kes[3]; yy,xx=np.mgrid[:H,:W]
            a=np.clip((np.hypot(xx-cx,yy-cy)-r)/40.0,0,1); E=E*a[...,None]
        E=temizle(E)
        mx=E.max(2); delik=(ndimage.binary_fill_holes(mx>40)|(ndimage.uniform_filter(mx,61)>90))&(mx<=40)
        if delik.any(): E=yumusak_doldur(E,ndimage.binary_dilation(delik,np.ones((5,5))))   # temizlik sonrasi kalan delik
        Image.fromarray(np.clip(E,0,255).astype(np.uint8)).save(os.path.join(OUT,ad,"%s_%02d.png"%(ad,n)))
        par.append(round(float(E.max(2).mean()),2))
    fr=fps_kayit or 72.0
    adim=aralik[1]-aralik[0]
    return dict(kare_sayisi=len(par),fps=round(fr/adim,1),ekran_kutu=list(kutu),kaynak_kareler=[aralik[0],aralik[-1]+1,adim],
                once=list(once),ortalama_parlaklik=par,kaynak="telefon 2712x1220")
if __name__=="__main__":
    va,vb=sys.argv[1],sys.argv[2]
    p=os.path.join(OUT,"efekt_bilgisi.json"); r=json.load(open(p)) if os.path.exists(p) else {}
    # kayit ~72 kare/sn (372 kare / 5.14 sn); 2 karede bir -> ~36 kare/sn
    # UI etiketleri efektin ONUNDE cizilir -> maskelenip doldurulur; karakter siluetleri de (efektin onunde duruyor)
    r["fire_burst"]=sira("fire_burst",vb,(800,200,900,760),range(66,69),list(range(69,141,2)),
                         maskeler=[(1258,488,1448,566)],siluet=[(1305,620,1465,815)],
                         kes=(104,1385,720,150))
    r["fire_blade"]=sira("fire_blade",va,(1080,0,560,820),range(224,228),list(range(228,266,2)),
                         maskeler=[(1080,55,1640,270),(1255,490,1465,566)],siluet=[(1190,500,1310,700),(1305,600,1420,800)],dikey=True)
    r["vurus_tam"]=sira("vurus_tam",va,(1130,450,470,430),range(140,158,3),list(range(160,196,2)),
                        maskeler=[(1255,488,1462,570)],siluet=[(1305,605,1440,800)])
    json.dump(r,open(p,"w"),indent=1)
    for k in ("fire_burst","fire_blade","vurus_tam"): print(k,r[k]["kare_sayisi"],"kare",r[k]["fps"],"fps",r[k]["ekran_kutu"])

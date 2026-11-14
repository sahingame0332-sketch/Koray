#!/usr/bin/env python3
"""Ucuncu efekt: skill sirasinda karakterin ALTINDA olusan sari-turuncu ates havuzu (2712x1220 kayit, 19-30-28).
Kayit degisken kare hizli (~67 kare/sn); 30 kare/sn'ye yeniden orneklenir. Kamera 30fps kare 67'de durur:
efektin ilk ~0.2 sn'si kamera kayarken -> cikarilamaz (efekt zaten acik halde baslar; kurucuda 0.15 sn acilis eklenir).
Zemin B = efekt bittikten sonraki karelerin medyani (116-131; ayni kamera). E = clip(O - B), eklemeli.
Temizlik: ad etiketi ve karakter silueti (efektin ONUNDE) doldurulur; kararan / sicak olmayan artiklar silinir.
Kullanim: cikar3.py VIDEO   (kayit depoya konmaz)"""
import os, sys, json, glob, subprocess, tempfile
import numpy as np
from PIL import Image
from scipy import ndimage
from cikar import OUT
from cikar2 import temizle, yumusak_doldur
KUTU=(1100,460,560,420)            # x,y,w,h (ekran)
ARALIK=range(67,106); ONCE=range(116,132)
ETIKET=(1300,534,1414,562); SILUET=(1303,563,1420,718)
def main(video):
    x,y,w,h=KUTU
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg","-v","error","-y","-i",video,"-vf","fps=30,crop=%d:%d:%d:%d"%(w,h,x,y),d+"/k_%04d.png"],check=True)
        fs=sorted(glob.glob(d+"/k_*.png"))
        Y=lambda i: np.asarray(Image.open(fs[i]).convert("RGB")).astype(float)
        B=np.median(np.stack([Y(i) for i in ONCE]),0)
        ad="ates_havuzu"; od=os.path.join(OUT,ad); os.makedirs(od,exist_ok=True)
        for f in glob.glob(od+"/*.png"): os.remove(f)
        m0=np.zeros((h,w),bool)
        for (a,b,c,e) in (ETIKET,SILUET): m0[b-y:e-y,a-x:c-x]=True
        m0=ndimage.binary_dilation(m0,np.ones((7,7)))
        # karakter silueti: orijinalde karakter isigin icinden goruluyor (efekt karakterin ustunde zayif) ->
        # dolgu orada yumusak kenarla zayiflatilir (ham O-B artisi siluette cevreyle ~ayni, 0.8-1.4x; ama doygun dolgu karakteri silerdi -> %40 zayiflatma, gozle)
        a,b,c,e=SILUET; yy,xx=np.mgrid[0:h,0:w]; sil=np.clip(1.15-np.hypot((xx-((a+c)/2-x))/((c-a)/2),(yy-((b+e)/2-y))/((e-b)/2)),0,1); sil=ndimage.gaussian_filter(sil,10)   # yumusak elips
        par=[]
        for n,i in enumerate(ARALIK):
            O=Y(i); D=O-B
            # doyma: parlak cekirdekte orijinal 255'e dayaniyor, O-B bilgiyi kaybeder (sari zeminde mavimsi kalir).
            # Eklemeli isik orada zaten zemini beyaza tasir -> E = O (isigin kendi rengi) ile harmanla.
            w=np.clip((O.max(2)-215)/35.0,0,1)[...,None]
            E=np.clip(w*O+(1-w)*D,0,255)
            yab=((D.min(2)<-20)|((D.max(2)>25)&(D[...,2]>D[...,0]+5)))&(w[...,0]<0.2)      # kararan / mavi-yesil: efekt degil
            k=ndimage.binary_dilation(yab,np.ones((7,7)))|m0
            E=yumusak_doldur(E,k)
            E=temizle(E,esik=22)
            E=E*(1-0.35*sil[...,None])
            mx=E.max(2); delik=(ndimage.binary_fill_holes(mx>40)|(ndimage.uniform_filter(mx,61)>90))&(mx<=40)
            if delik.any(): E=yumusak_doldur(E,ndimage.binary_dilation(delik,np.ones((5,5))))
            Image.fromarray(np.clip(E,0,255).astype(np.uint8)).save(os.path.join(od,"%s_%02d.png"%(ad,n)))
            par.append(round(float(E.max(2).mean()),2))
    p=os.path.join(OUT,"efekt_bilgisi.json"); r=json.load(open(p)) if os.path.exists(p) else {}
    r[ad]=dict(kare_sayisi=len(par),fps=30.0,ekran_kutu=list(KUTU),kaynak_kareler=[ARALIK[0],ARALIK[-1]+1,1],once=list(ONCE),
               ortalama_parlaklik=par,kaynak="telefon 2712x1220, 30 kare/sn'ye orneklendi",ayak=[1360,712],karakter_boyu_px=150)
    json.dump(r,open(p,"w"),indent=1); print(ad,len(par),"kare",par[:3],"...",par[-3:])
if __name__=="__main__": main(sys.argv[1])

#!/usr/bin/env python3
"""Besinci set: karakterin kendine uyguladigi skill efektleri (9 telefon kaydi, 2712x1220, 30 kare/sn'ye orneklenir).
Her efekt: O - B eklemeli; B = efekt oncesi karelerin medyani (kamera sabit).
Temizlik: cast cubugu ("<skill> 1,5 sec") kutusu ve karakterin hareketi (kararan / yesil artan pikseller) komsu isiktan doldurulur.
Kullanim: cikar5.py KLASOR   (KLASOR: v1.mp4 .. v9.mp4; kayitlar depoya konmaz)"""
import os, sys, json, glob, subprocess, tempfile
import numpy as np
from PIL import Image
from scipy import ndimage
from cikar import OUT
from cikar2 import yumusak_doldur, dikey_doldur
KUTU=(1000,150,720,860)                       # x,y,w,h  (karakter (1370, ayak 835), boy ~265 px)
CAST=(1250,740,1462,796)                      # cast cubugu + yazilari
ETIKET=(1205,452,1500,553)                    # "JustForFARM" / "xDarkPast" + can cubugu: efektin ONUNDE (isin arkasindan gecer)
# renk imzalari (O-B artisinin yonu; olculdu): altin, turuncu, kirmizi, pembe; beyaz cekirdek ayrica
ALTIN=[(1,1,.33),(1,.67,.33),(1,1,0)]; TURUNCU=[(1,.5,0),(1,.25,0),(1,.67,.33)]; KIRMIZI=[(1,0,0),(1,.25,.25),(1,.45,.45)]          # (1,.6,.6) gri zirhi da kabul ediyordu (cos .97)
PEMBE=[(.67,.33,1),(1,.33,1),(.8,.5,1),(.67,0,1)]; MAVI_BEYAZ=[(.67,.67,1),(1,1,1)]   # pembe: (.67,.67,1) gri ile cos .98 -> cikarildi
RENK={"dokum_yildizlari":ALTIN+TURUNCU,"hide":ALTIN+TURUNCU,"light_feet":ALTIN,"kedi_gozu":KIRMIZI,"evade":ALTIN,
      "safety":TURUNCU+ALTIN[1:2],"cure":ALTIN+MAVI_BEYAZ+[(1,.67,.67)],"magic_shield":PEMBE}
BEYAZ_ESIK={"cure":45,"kedi_gozu":40,"light_feet":60}                         # beyaz isik: tum kanallar en az bu kadar artmali (cure isini, goz efektinin acik cizgileri, light feet cekirdegi)
GOVDE=(1370,700,92,150)                        # karakter govdesi elipsi (merkez x,y, yaricap x,y): doku hareketi burada
GOVDE_ZAYIF={"dokum_yildizlari":0.8,"hide":0.6,"evade":0.75,"safety":0.75,"cure":0.3,"light_feet":0.3,"kedi_gozu":1.0,"magic_shield":0.3}
#        ad,             video, once (bg),   aralik (efekt)
EFEKT=[("dokum_yildizlari","v4",range(0,40), range(44,86)),
       ("hide",           "v1",range(0,24), range(26,90)),
       ("light_feet",     "v2",range(0,50), range(56,146)),
       ("kedi_gozu",      "v4",range(0,40), range(104,174)),
       ("evade",          "v5",range(0,30), range(32,104)),
       ("safety",         "v6",range(0,48), range(50,142)),
       ("cure",           "v8",range(0,36), range(82,132)),
       ("magic_shield",   "v9",range(0,48), range(50,130))]
import atexit, shutil
_GECICI=[]
atexit.register(lambda: [shutil.rmtree(d,ignore_errors=True) for d in _GECICI])
def kareler(video):
    x,y,w,h=KUTU; d=tempfile.mkdtemp(); _GECICI.append(d)               # cikista silinir (disk dolmasin)
    subprocess.run(["ffmpeg","-v","error","-y","-i",video,"-vf","fps=30,crop=%d:%d:%d:%d"%(w,h,x,y),d+"/k_%04d.png"],check=True)
    return d,sorted(glob.glob(d+"/k_*.png"))
def Y(f): return np.asarray(Image.open(f).convert("RGB")).astype(np.float32)
def temizle(E,esik=18):
    mx=E.max(2)
    tut=ndimage.binary_opening(mx>esik,np.ones((2,2)))|(mx>120)
    l,n=ndimage.label(tut)
    if n:
        s=ndimage.sum(mx>esik,l,range(1,n+1)); tut=np.isin(l,1+np.where(s>=6)[0])
    E=np.where(tut[...,None],E,0)
    return ndimage.gaussian_filter(E,[0.6,0.6,0])
def cikar(klasor):
    x,y,w,h=KUTU; bilgi={}; cache={}
    cast=np.zeros((h,w),bool); cast[CAST[1]-y:CAST[3]-y,CAST[0]-x:CAST[2]-x]=True
    etk=np.zeros((h,w),bool); etk[ETIKET[1]-y:ETIKET[3]-y,ETIKET[0]-x:ETIKET[2]-x]=True
    yy,xx=np.mgrid[0:h,0:w]; gx,gy,rx,ry=GOVDE
    gov=np.clip(1.15-np.hypot((xx+x-gx)/rx,(yy+y-gy)/ry),0,1); gov=ndimage.gaussian_filter(gov,6)
    for ad,v,once,aralik in EFEKT:
        if v not in cache: cache[v]=kareler(os.path.join(klasor,v+".mp4"))
        fs=cache[v][1]
        B=np.median(np.stack([Y(fs[i]) for i in once]),0)
        od=os.path.join(OUT,ad); os.makedirs(od,exist_ok=True)
        for f in glob.glob(od+"/*.png"): os.remove(f)
        par=[]; kutu=[w,h,0,0]
        for n,i in enumerate(aralik):
            O=Y(fs[i]); D=O-B
            w8=(np.clip((O.max(2)-215)/35.0,0,1)*(D.max(2)>40))[...,None]   # doyan cekirdek (ve gercekten artmis): isigin kendi rengi
            E=np.clip(w8*O+(1-w8)*D,0,255)
            yab=(D.min(2)<-22)|((D[...,1]>D[...,0]+10)&(D[...,1]>D[...,2]+10)&(D.max(2)>20))   # karakter hareketi / yesil ten
            m=ndimage.binary_dilation(yab,np.ones((5,5)))&(w8[...,0]<0.3)
            m|=cast
            # renk kapisi: artisin yonu efektin imzasina benzemeyen pikseller (karakterin gri zirhi, yesil-sari ten) atilir
            Dp=np.clip(D,0,None); nn=Dp/np.maximum(np.linalg.norm(Dp,axis=2,keepdims=True),1e-3)
            cosm=np.max([nn@ (np.array(r)/np.linalg.norm(r)) for r in RENK[ad]],0)
            kapi=np.clip((cosm-0.95)/0.03,0,1)
            if ad in BEYAZ_ESIK:
                esik=np.where(gov>0.5,90.0,BEYAZ_ESIK[ad])
                kapi=np.maximum(kapi,np.clip((Dp.min(2)-esik)/20.0,0,1))
            kapi=np.maximum(kapi,w8[...,0]*(cosm>(0.85 if ad in BEYAZ_ESIK else 0.95)))   # doyan cekirdek de efekt renginde olmali (beyaz kumas degil)
            gz=GOVDE_ZAYIF[ad]
            kapi*=1-gz*gov*((O.max(2)<235) if gz<1 else 1)          # govde: parlak cekirdek disindaki artis zayiflatilir (1.0: govdede efekt yok)
            E=E*kapi[...,None]
            E=yumusak_doldur(E,m,n=10,k=11)
            E=dikey_doldur(E,etk)                                    # etiket bandi: isin/sutun dikey surekli -> ust/alttan
            E[:40]=0; E[:140,460:]=0                                 # uzak yaratik etiketleri (ust serit, sag ust)
            E=temizle(E)
            Image.fromarray(np.clip(E,0,255).astype(np.uint8)).save(os.path.join(od,"%s_%02d.png"%(ad,n)))
            par.append(round(float(E.max(2).mean()),2))
            ys,xs=np.nonzero(E.max(2)>20)
            if len(xs): kutu=[min(kutu[0],xs.min()),min(kutu[1],ys.min()),max(kutu[2],xs.max()),max(kutu[3],ys.max())]
        bilgi[ad]=dict(video=v,kaynak_kareler=[aralik[0],aralik[-1]+1],once=[once[0],once[-1]+1],kare_sayisi=len(par),fps=30.0,
                       ekran_kutu=list(KUTU),efekt_kutusu_ekran=[int(x+kutu[0]),int(y+kutu[1]),int(kutu[2]-kutu[0]+1),int(kutu[3]-kutu[1]+1)],
                       ortalama_parlaklik=par,karakter_ayak=[1370,835],karakter_boyu_px=265)
        print(ad,len(par),"kare, efekt kutusu",bilgi[ad]["efekt_kutusu_ekran"])
    p=os.path.join(OUT,"efekt_bilgisi.json"); r=json.load(open(p)) if os.path.exists(p) else {}
    r.update({"kendi_"+k:v for k,v in bilgi.items()}); json.dump(r,open(p,"w"),indent=1)
if __name__=="__main__": cikar(sys.argv[1])

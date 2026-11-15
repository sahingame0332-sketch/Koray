#!/usr/bin/env python3
"""Shadow Hunter vurusu: beyaz cizgi-roman patlamasi (kare 123-128) + gokten inen turuncu isin (129-160) + pembe duman.
Eklemeli kareler E = O - B (B = vurus oncesi 100-118 ve sonrasi 172-199 medyanlari; ikisine gore artisin kucugu), 2 karede bir -> 30 kare/sn.
Renk kapisi: beyaz / turuncu / kirmizi / pembe disindaki artislar (kivranan Worm'un kahverengi hareketi) atilir; "Worm" etiketi doldurulur.
Sol ustteki karakter paneli isinin ust kismini ortuyor (y < ~262): o bolgede isin yok (kayitta gorunmuyor).
Kullanim: cikar_vurus.py KARE_KLASORU"""
import os, sys, glob, json, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","efekt"))
from cikar2 import yumusak_doldur
B_=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(B_,"..","..","kaynak","ok","vurus"); os.makedirs(OUT,exist_ok=True)
fs=sorted(glob.glob(sys.argv[1]+'/k_*.png'))
KUTU=(0,262,520,260)                         # x,y,w,h (panelin alti)
x,y,w,h=KUTU
Y=lambda i: np.asarray(Image.open(fs[i]).convert('RGB')).astype(np.float32)[y:y+h,x:x+w]
B=np.median(np.stack([Y(i) for i in range(100,119)]),0)
B2=np.median(np.stack([Y(i) for i in range(172,200)]),0)          # vurus sonrasi: Worm ve secim halkasi yeni yerinde
# halka ve Worm her iki zeminde de var: artis = iki zemine gore artislarin kucugu (yalniz efekt ikisinde de yok)
RENK=[(1,1,1),(1,.9,.8),(1,.55,.2),(1,.35,.1),(1,.25,.25),(1,.5,.7),(1,.6,.5)]
RENK=[np.array(r)/np.linalg.norm(r) for r in RENK]
etiket=np.zeros((h,w),bool); etiket[330-y:372-y,125-x:235-x]=True
for f in glob.glob(OUT+"/*.png"): os.remove(f)
W=np.array([248.,248.,244.])                                   # patlama beyazi (olculen ~ 203,204,192 cimin ustunde, yari saydam)
ARALIK=list(range(122,168,2))
def ham(i):
    O=Y(i); D=np.minimum(O-B,O-B2); return O,D
# secim halkasi: yalniz efektsiz zeminlerde (vurus oncesi ve sonrasi) gorunen acik sari-beyaz ince elips -> iki konumun birlesimi
def halka_bul(Z):
    m=(Z.max(2)>165)&(Z[...,1]>130)&(Z[...,0]-Z[...,2]<120)
    m[:380-y]=False                                                 # halka yerde (y >= 380)
    return m
halka=halka_bul(B)|halka_bul(B2)
for i in range(158,168,2):                                          # son kareler: isin sonmus, artis = yalniz halka (titresip kayan)
    O,D=ham(i); hm=np.clip(D,0,None).max(2)>30; hm[:405-y]=False; halka|=hm
halka=ndimage.binary_dilation(halka,np.ones((9,9)))
par=[]
for n,i in enumerate(ARALIK):
    O,D=ham(i); Dp=np.clip(D,0,None)
    # 1) beyaz patlama: ORTUCU (alfa) — O = (1-a)B + a*W
    V=W-B; a=np.clip((D*V).sum(2)/np.maximum((V*V).sum(2),400),0,1)
    nn=Dp/np.maximum(np.linalg.norm(Dp,axis=2,keepdims=True),1e-3)
    beyazlik=np.clip((O.min(2)-130)/50.0,0,1)*np.clip(1-(O.max(2)-O.min(2)-25)/40.0,0,1)   # acik ve renksiz
    a=a*beyazlik
    # 2) turuncu isin / pembe duman / kivilcim: EKLEMELI
    cosm=np.max([nn@r for r in RENK[2:]],0)
    kapi=np.clip((cosm-0.93)/0.04,0,1)*np.clip((Dp.max(2)-25)/25,0,1)
    E=Dp*kapi[...,None]*(1-a[...,None])
    m=halka|ndimage.binary_dilation(etiket&(O.max(2)>150),np.ones((3,3)))
    E=yumusak_doldur(E,m,n=8,k=9); a=yumusak_doldur(a[...,None],m,n=8,k=9)[...,0]
    E=ndimage.gaussian_filter(E,[0.5,0.5,0]); a=ndimage.gaussian_filter(a,0.5)
    C=np.clip(a[...,None]*W+E,0,255)                                # on-carpimli renk; Unity: Blend One OneMinusSrcAlpha
    Image.fromarray(np.dstack([C,a*255]).astype(np.uint8),"RGBA").save(os.path.join(OUT,"vurus_%02d.png"%n))
    par.append(round(float(C.max(2).mean()),2))
json.dump(dict(kutu=list(KUTU),kaynak_kareler=[122,168,2],fps=30,kare_sayisi=len(par),vurus_merkezi_ekran=[250,350],karisim="on-carpimli: rgb = a*beyaz + isik, alfa = beyaz patlamanin ortuculugu",
               ortalama_parlaklik=par),open(os.path.join(OUT,"..","vurus_olculer.json"),"w"),indent=1)
print(len(par),"kare",par)

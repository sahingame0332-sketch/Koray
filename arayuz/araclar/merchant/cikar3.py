#!/usr/bin/env python3
"""Alici gorunumu (a_cubuk.jpg, a_pencere.jpg — 2712x1220): mor yuva cerceveleri + ornek ikonlar.
Mor cerceve = dolu yuva cercevesinin disinda ~3 px mor kenar; hangi esyalarda ciktigi bilinmiyor (bu karelerde +1 silahlar)."""
import json
from scipy import ndimage
from ortak import *
KAYIT={}
def yaz(ad,a,**b): kaydet(ad,a); KAYIT[ad]=dict(w=int(a.shape[1]),h=int(a.shape[0]),**b)
def halka(kare,kutu,dis,ic):
    """Cerceve = dis dikdortgen ile ic dikdortgen arasindaki koyu olmayan pikseller ("+N" etiketinin acik moru haric)."""
    x,y,w,h=kutu; a=Y(kare)[y:y+h,x:x+w]
    etiket=(a[:,:,1]>105)&(a[:,:,0]>a[:,:,1]+35)&(a[:,:,2]>a[:,:,1]+35)       # #CA89E2 dolayi
    m=(a.max(2)>48)&~ndimage.binary_dilation(etiket,np.ones((3,3)))
    bolge=np.zeros((h,w),bool); bolge[dis[1]:dis[3],dis[0]:dis[2]]=True; bolge[ic[1]:ic[3],ic[0]:ic[2]]=False
    m&=bolge
    al=ndimage.gaussian_filter(ndimage.binary_closing(m,np.ones((3,3))).astype(float),0.6)
    return np.dstack([a,np.clip(al*1.7,0,1)*255])
TZ=(955,241)                                   # tezgah cubugu sprite basi (alti alt-sablonla eslestirildi)
yaz("yuva_mor_tezgah",halka("a_cubuk",(TZ[0]+27+86,TZ[1]+9,86,88),(9,4,86,86),(17,12,77,78)))
yaz("yuva_mor_mp_ust",halka("a_pencere",(975,229,117,114),(1,1,116,113),(13,12,104,102)))
PU=(974.7,120.31,228.8,121.17); PE=(967.8,103.64,588.9,104.4)
def ikon(ad,kare,x,y,w,h,etiket=None,sayac=None):
    a=Y(kare)[y:y+h,x:x+w].copy()
    if etiket:        # "+N": mor pikseller (siyah zemin ustunde) siyaha
        x0,y0,x1,y1=etiket; s=a[y0:y1,x0:x1]; m=(s[:,:,0]>s[:,:,1]+25)&(s[:,:,2]>s[:,:,1]+25)&(s.max(2)>60)
        m=ndimage.binary_dilation(m,np.ones((5,5))); s[m]=0
    if sayac:         # adet rakami: beyaz + koyu dis hat (koyu zemin ustunde) siyaha
        x0,y0,x1,y1=sayac; s=a[y0:y1,x0:x1]; m=(s.min(2)>150)
        m=ndimage.binary_dilation(m,np.ones((7,7))); s[m]=0
    yaz(ad,np.dstack([a,np.full(a.shape[:2],255.0)]))
# mor cerceveli yuvada ikon alani 12 px icerde (93 x 90); "+N" etiketi siyah zemin ustunde -> siyaha boyanir
def ikon_mor(ad,x,y):
    a=Y("a_pencere")[y+12:y+114-12,x+12:x+117-12].copy()
    s=a[0:30,52:]; m=(s[:,:,1]>80)&(s[:,:,0]>s[:,:,1]+25)&(s[:,:,2]>s[:,:,1]+25); s[ndimage.binary_dilation(m,np.ones((5,5)))]=0
    yaz(ad,np.dstack([a,np.full(a.shape[:2],255.0)]))
ikon_mor("ikon_yay",975,229); ikon_mor("ikon_balta",975,350)
ex=int(round(PE[0]+PE[1]*5)); ey=int(round(PE[2]))
ikon("ikon_parsomen_sureli_3","a_pencere",ex+8,ey+8,88,86)     # adet rakami "3" ikonun ustunde: temizlenemedi, pikselde kaldi
p=os.path.join(OUT,"..","sprite_bilgisi.json"); j=json.load(open(p)); j.update(KAYIT); json.dump(j,open(p,"w"),indent=1,ensure_ascii=False)
print(list(KAYIT))

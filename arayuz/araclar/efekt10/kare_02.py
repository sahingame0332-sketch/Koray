#!/usr/bin/env python3
"""Efekt 10 — kare 2 (kullanici cizimine gore: mercek bicimli beyaz + yatay bant) (yavas cekimde 00:04, gercek hizda ~0.27 sn): kare_01 uzerine
  1) titanyum beyaz kure yanlara dogru genisler: cekirdek (r~76, kenar r~94) yatayda 1.35x, dikeyde 1.05x elips olur ve
     bir sonraki katmana (seftali/somon halka) tasar; kenar yumusak (ayni beyaz->sampanya->seftali gecisi korunur)
  2) ortada yatay, ince, hafif saydam sari cizgi (%50 opaklik), uclara dogru incelir
Cikti: kareler/kare_02.png (+ _siyah/_beyaz), onizlemeler/efekt10_kare_01_02.png (yan yana)"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
YX,YY=1.35,1.05                      # beyaz kurenin yatay/dikey genisleme orani
CIZGI_OPAK=0.50; SARI=np.array([0xF7,0xE6,0x45],np.float32)/255
a=np.asarray(Image.open(os.path.join(K,"kare_01.png")).convert("RGBA")).astype(np.float32)/255
L=a[...,:3]*a[...,3:4]; H,W=L.shape[:2]; cy,cx=(H-1)/2,(W-1)/2
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); dx,dy=xx-cx,yy-cy
# 1) beyaz kure (kullanici cizimi): yanlara genisleyen mercek/goz bicimi + iki yandan disari uzanan yatay bant.
#    Bicim alani s: elips (yari genislik 150, yari yukseklik 96) ile yatay bant (yari kalinlik 16, uzunluk 245) yumusak birlesimi.
#    s=1 kenar; renk kare_01'in kendi radyal gecisinden (beyaz -> sampanya -> seftali) ayni aci yonunde orneklenir.
EA,EB,BK,BU=121.5,79.2,15.0,200.0          # titanyum beyaz 1/10 kucuk
el=np.hypot(dx/EA,dy/EB)
# bant: ortada ince, parantezle birlestigi yerde (|dx| ~ 175-215) kalinlasir, sonra yumusakca biter
ax=np.abs(dx)
kalin=2.4-1.95*np.clip((ax-EA*0.75)/(BU-EA*0.75),0,1)**0.8         # kureden cikan taraf kalin, paranteze dogru incelir
bt=np.maximum(np.abs(dy)/(BK*kalin),ax/(BU+12))+np.clip((ax-BU+5)/20,0,None)   # bant parantezden once biter; devaminda sari cizgi
k=0.12; s_=-k*np.log(np.exp(-el/k)+np.exp(-bt/k))                 # yumusak min (birlesim)
# duzensizlik: kenara organik dalga + ince puruz (acisal + 2B gurultu)
rg=np.random.default_rng(12)
def gur(sc,seed):
    z=np.random.default_rng(seed).standard_normal((H//sc+3,W//sc+3)).astype(np.float32)
    z=ndimage.zoom(ndimage.gaussian_filter(z,1.0),sc,order=3)[:H,:W]; return z/(z.std()+1e-6)
th0=np.arctan2(dy,dx); na=48
za=ndimage.gaussian_filter1d(rg.standard_normal(na).astype(np.float32),1.2,mode="wrap"); za/=za.std()
ia=((th0+np.pi)/(2*np.pi)*na); i0=np.floor(ia).astype(int)%na; fa=ia-np.floor(ia)
dalga=za[i0]*(1-fa)+za[(i0+1)%na]*fa
s_=s_*(1+0.045*dalga+0.03*gur(14,3)+0.012*gur(5,4))
th=np.arctan2(dy,dx); R0=80.0
sx=cx+np.cos(th)*R0*s_; sy=cy+np.sin(th)*R0*s_
G=np.stack([ndimage.map_coordinates(L[...,c],[sy,sx],order=1) for c in range(3)],-1)
w=np.clip((1.45-s_)/0.75,0,1); w=w*w*(3-2*w); w=ndimage.gaussian_filter(w,6.0)[...,None]      # genis, yumusak kenar
G=np.stack([ndimage.gaussian_filter(G[...,c],2.0) for c in range(3)],-1)
T=L*(1-w)+np.maximum(L,G)*w
# 2) yatay sari cizgi, %50 opaklik
uz=W*0.47
boy=np.clip(1-np.abs(dx)/uz,0,1)**0.8
beyaz=np.clip((T.min(2)-0.80)/0.15,0,1); beyaz=ndimage.gaussian_filter(beyaz,2.0)   # titanyum beyaz bolge
cizgi=(np.exp(-(dy/1.6)**2)+0.35*np.exp(-(dy/5.0)**2))*boy*CIZGI_OPAK*(1-beyaz)        # beyazin icinde gorunmez
T=T*(1-cizgi[...,None])+SARI*cizgi[...,None]+T*cizgi[...,None]*0  # cizgi alttakinin uzerine %50 opak
T=np.maximum(T,np.clip(SARI*cizgi[...,None],0,1))
al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(K,"kare_02.png"))
im=Image.open(os.path.join(K,"kare_02.png"))
for ad,zr in (("siyah",(0,0,0,255)),("beyaz",(255,255,255,255))):
    z=Image.new("RGBA",im.size,zr); z.alpha_composite(im); z.convert("RGB").save(os.path.join(K,"kare_02_%s.png"%ad))
o=Image.new("RGB",(W*2+20,H*2+20),(20,20,24))
for j,k in enumerate(("01","02")):
    for i,ad in enumerate(("beyaz","siyah")):
        o.paste(Image.open(os.path.join(K,"kare_%s_%s.png"%(k,ad))),(j*(W+20),i*(H+20)))
o.save(os.path.join(ONZ,"efekt10_kare_01_02.png")); print("tamam")

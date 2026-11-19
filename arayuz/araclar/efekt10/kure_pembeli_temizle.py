#!/usr/bin/env python3
"""Pembeli surumde (kure_ref_saydam_pembeli.png) mor/macenta lekeleri temizler (mob ve etiket artigi; ust-alt ortada).
Leke: B, G'den belirgin buyuk (mor-macenta). Lekeli pikseller ayni yaricapta, aci yonunde en yakin temiz piksellerden doldurulur
(efekt halka yapili). Cikti: kure_ref_saydam_pembeli_temiz.png + onizlemeler/efekt10_kure_pembeli_temiz.png"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kure_ref"); ONZ=os.path.join(B_,"..","..","onizlemeler")
a=np.asarray(Image.open(os.path.join(K,"kure_ref_saydam_pembeli.png")).convert("RGBA")).astype(np.float32)/255
L=a[...,:3]*a[...,3:4]                                                         # isik (on-carpimli)
H,W=L.shape[:2]; cy,cx=(H-1)/2,(W-1)/2
yy,xx=np.mgrid[0:H,0:W]; R=np.hypot(xx-cx,yy-cy); A=np.arctan2(yy-cy,xx-cx)
r,g,b=L[...,0],L[...,1],L[...,2]; mx=np.maximum(L.max(2),1e-3)
mor=((b-g)/mx>0.10)&((r-g)/mx>0.15)&(L.max(2)>0.05)
mor=ndimage.binary_opening(mor,np.ones((2,2)))
lb,n=ndimage.label(ndimage.binary_dilation(mor,np.ones((5,5))))
if n:
    sz=ndimage.sum(mor,lb,range(1,n+1)); mor=np.isin(lb,1+np.where(sz>=6)[0])
leke=ndimage.binary_dilation(mor,np.ones((7,7)))
# kutupsal doldurma
NA=1440; NR=int(R.max())+2
tg=np.linspace(-np.pi,np.pi,NA,endpoint=False); rg=np.arange(NR)
PX=np.clip(np.round(cx+rg[:,None]*np.cos(tg)[None]).astype(int),0,W-1); PY=np.clip(np.round(cy+rg[:,None]*np.sin(tg)[None]).astype(int),0,H-1)
Pv=L[PY,PX]; Pm=leke[PY,PX]; Pf=Pv.copy(); t=np.arange(NA)
for k in range(NR):
    ok=~Pm[k]
    if (~ok).any() and ok.sum()>4:
        i=np.where(ok)[0]
        for c in range(3): Pf[k,~ok,c]=np.interp(t[~ok],i,Pv[k,i,c],period=NA)
ai=((A+np.pi)/(2*np.pi)*NA).astype(int)%NA; ri=np.clip(R.astype(int),0,NR-1)
dol=np.stack([ndimage.gaussian_filter(Pf[ri,ai][...,c],1.0) for c in range(3)],-1)
w=np.maximum(ndimage.gaussian_filter(leke.astype(np.float32),2.0),leke)[...,None]
T=L*(1-w)+dol*w
al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(K,"kure_ref_saydam_pembeli_temiz.png"))
im=Image.open(os.path.join(K,"kure_ref_saydam_pembeli_temiz.png"))
bz=Image.new("RGBA",im.size,(255,255,255,255)); bz.alpha_composite(im); sz_=Image.new("RGBA",im.size,(0,0,0,255)); sz_.alpha_composite(im)
o=Image.new("RGB",(im.width*2+20,im.height),(20,20,24)); o.paste(bz.convert("RGB"),(0,0)); o.paste(sz_.convert("RGB"),(im.width+20,0))
o.save(os.path.join(ONZ,"efekt10_kure_pembeli_temiz.png"))
m=Image.fromarray((leke*255).astype(np.uint8)); m.save("/tmp/claude-0/-home-user-Koray/7667fcb8-b488-59d0-b1d8-f55ffb36b68a/scratchpad/eski/leke.png")
print("leke piksel:",int(leke.sum()))

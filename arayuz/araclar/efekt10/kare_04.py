#!/usr/bin/env python3
"""Efekt 10 — kare 4 (kullanici fotografi): ortada yuvarlak titanyum beyaz (~100x84 px); onun etrafi PARANTEZE KADAR beyazdan sariya
donmus isik (mercek bicimli parlak cekirdek ~230x124, uclari yanlara bant olarak uzanir ~330); ikinci katman (seftali/somon) yok,
yalniz soluk buharlari (dalgali, parcali) kalir. Parantezler ve dis sis kare_01'deki gibi.
Cikti: kareler/kare_04.png (+ _siyah/_beyaz), onizlemeler/efekt10_kareler.png (1-4 yan yana)"""
import os, numpy as np
from PIL import Image
from scipy import ndimage
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","efekt10","kareler"); ONZ=os.path.join(B_,"..","..","onizlemeler")
BEYAZ_RX,BEYAZ_RY=50.0,42.0; MER_X,MER_Y,BANT_Y,BANT_X=115.0,62.0,10.0,168.0
SARI=np.array([0xF8,0xE9,0x5A],np.float32)/255; ACIK=np.array([0xFF,0xF8,0xC8],np.float32)/255
a=np.asarray(Image.open(os.path.join(K,"kare_01.png")).convert("RGBA")).astype(np.float32)/255
L0=a[...,:3]*a[...,3:4]; H,W=L0.shape[:2]; cy,cx=(H-1)/2,(W-1)/2
yy,xx=np.mgrid[0:H,0:W].astype(np.float32); dx,dy=xx-cx,yy-cy; R=np.hypot(dx,dy); ax=np.abs(dx)
def gur(sc,seed):
    z=np.random.default_rng(seed).standard_normal((H//sc+3,W//sc+3)).astype(np.float32)
    z=ndimage.zoom(ndimage.gaussian_filter(z,1.0),sc,order=3)[:H,:W]; return z/(z.std()+1e-6)
sariyesil=np.clip((L0[...,1]-0.80*L0[...,0])/0.12+0.5,0,1)*np.clip((R-165)/10,0,1)
ic=np.clip((186-R)/14,0,1)*(1-sariyesil)                         # parantezin ici
# taban: kare_01, parantez ici bosaltilir
T=L0*(1-ic)[...,None]
# sari isik: parantezin icini dolduran, merkeze dogru beyazlasan sari (merceğin icinde daha parlak)
gov=MER_Y*np.sqrt(np.clip(1-(ax/MER_X)**2,0,1))
bant=BANT_Y*np.clip(1-np.clip((ax-MER_X*0.6)/(BANT_X-MER_X*0.6),0,1),0,1)**0.7*(ax<BANT_X)
h=ndimage.gaussian_filter1d(np.maximum(gov,np.maximum(bant,0.01)),6,axis=1)
sm=np.abs(dy)/np.maximum(h,0.5)*(1+0.05*gur(12,9))               # mercek: 1 = kenar
mer=np.clip((1.5-sm)/0.9,0,1); mer=mer*mer*(3-2*mer)
genel=np.clip((196-R)/34,0,1); genel=genel*genel*(3-2*genel)*(1-sariyesil)     # paranteze kadar sari, yumusak sinir
sar_op=np.clip(genel*(0.86+0.12*np.clip(1-R/190,0,1))+0.5*mer,0,1)
renk=SARI[None,None,:]*(1-mer[...,None])+ACIK[None,None,:]*mer[...,None]
T=T*(1-sar_op[...,None])+renk*sar_op[...,None]
# buharlar: ikinci katmanin soluk, dalgali parcalari — sarinin uzerinde ekran karisimiyla (yalniz pembe ton ekler)
buh=np.clip(0.4+0.7*ndimage.gaussian_filter(gur(16,7),2),0,1)**2*np.clip((R-75)/30,0,1)*np.clip((185-R)/30,0,1)*(1-mer)
pembe=L0*np.array([1.0,0.62,0.60],np.float32)
T=1-(1-T)*(1-np.clip(pembe*(buh*0.45)[...,None],0,1))
# titanyum beyaz yuvarlak cekirdek (hafif duzensiz, yumusak kenar)
eb=np.hypot(dx/BEYAZ_RX,dy/BEYAZ_RY)*(1+0.04*gur(10,10))
wb=np.clip((1.18-eb)/0.30,0,1); wb=wb*wb*(3-2*wb)
T=T*(1-wb[...,None])+np.ones(3,np.float32)*wb[...,None]
T=np.clip(T,0,1); al=T.max(2); rgb=np.where(al[...,None]>1e-4,T/np.maximum(al,1e-4)[...,None],0)
Image.fromarray(np.dstack([(rgb*255).round(),(al*255).round()]).astype(np.uint8)).save(os.path.join(K,"kare_04.png"))
im=Image.open(os.path.join(K,"kare_04.png"))
for ad,zr in (("siyah",(0,0,0,255)),("beyaz",(255,255,255,255))):
    z=Image.new("RGBA",im.size,zr); z.alpha_composite(im); z.convert("RGB").save(os.path.join(K,"kare_04_%s.png"%ad))
o=Image.new("RGB",(W*4+60,H*2+20),(20,20,24))
for j,k in enumerate(("01","02","03","04")):
    for i,ad in enumerate(("beyaz","siyah")):
        o.paste(Image.open(os.path.join(K,"kare_%s_%s.png"%(k,ad))),(j*(W+20),i*(H+20)))
o.save(os.path.join(ONZ,"efekt10_kareler.png")); print("tamam")

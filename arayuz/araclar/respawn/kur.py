#!/usr/bin/env python3
"""Respawn benzetimi. Pencereli olmayan kare yok: (1) ayni kare, pencere ici arka sahne O/(1-a) ile geri kestirilip
siyah(0.92)+sprite yeniden bindirilir -> orijinalle karsilastirma; (2) baska bir sahnede (genie g_once) ayni konumda.
Cikti: onizlemeler/respawn_onizleme.png"""
import os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","respawn")
REF=os.path.join(B_,"..","..","referans_gorseller")
J=json.load(open(os.path.join(K,"olculer.json"))); a=J["alfa"]
O=np.asarray(Image.open(os.path.join(REF,"respawn","respawn.jpg")).convert("RGB")).astype(float)
sp=Image.open(os.path.join(K,"respawn_pencere.png"))
sx,sy=J["sprite"][:2]; x,y,w,h=J["dis_kutu"]
def bindir(sahne):
    S=sahne.copy(); S[y:y+h,x:x+w]*=(1-a); im=Image.fromarray(np.clip(S,0,255).astype(np.uint8)).convert("RGBA"); im.alpha_composite(sp,(sx,sy)); return im.convert("RGB")
B=O.copy(); ic=O[y:y+h,x:x+w]; B[y:y+h,x:x+w]=np.clip(ndi:=ic,0,255)
from scipy import ndimage
taban=ndimage.grey_opening(ic.max(2),size=(21,21))[...,None]*np.ones(3)
B[y:y+h,x:x+w]=np.clip(np.minimum(ic,taban+2)/(1-a),0,255)          # yazi/cerceve disindaki sizinti -> sahne
yeni=bindir(B)
kut=(1900,560,2712,1100)
o1=Image.fromarray(O.astype(np.uint8)).crop(kut); n1=yeni.crop(kut)
fark=np.abs(np.asarray(o1).astype(float)-np.asarray(n1).astype(float)).mean()
G=np.asarray(Image.open(os.path.join(REF,"genie","g_once.jpg")).convert("RGB")).astype(float)
g1=bindir(G).crop(kut)
FT=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf"),22)
W=o1.width; c=Image.new("RGB",(W*3+40,o1.height+44),(24,24,28)); d=ImageDraw.Draw(c)
d.text((6,8),"ORİJİNAL",font=FT,fill=(255,220,120)); d.text((W+26,8),"YENİ (siyah %.2f + sprite)  ort. fark %.1f/255"%(a,fark),font=FT,fill=(140,230,140))
d.text((2*W+46,8),"YENİ — başka sahnede",font=FT,fill=(140,230,140))
c.paste(o1,(0,44)); c.paste(n1,(W+20,44)); c.paste(g1,(2*W+40,44))
c.save(os.path.join(B_,"..","..","onizlemeler","respawn_onizleme.png")); print("fark %.2f"%fark, c.size)

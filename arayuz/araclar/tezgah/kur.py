#!/usr/bin/env python3
"""Tezgah onizlemesi: (1) orijinal kare, (2) ayni kare uzerine sprite, (3) baska bir sahnede (respawn karesi) ayni olcekle.
Cikti: onizlemeler/tezgah_onizleme.png"""
import os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","tezgah"); REF=os.path.join(B_,"..","..","referans_gorseller")
J=json.load(open(os.path.join(K,"olculer.json"))); sp=Image.open(os.path.join(K,"tezgah.png"))
O=Image.open(os.path.join(REF,"tezgah","tezgah.jpg")).convert("RGBA"); x,y=J["ekran_kutu"][:2]
N=O.copy(); N.alpha_composite(sp,(x,y))
fark=np.abs(np.asarray(O.convert("RGB")).astype(float)-np.asarray(N.convert("RGB")).astype(float))[y:y+sp.height,x:x+sp.width].mean()
S=Image.open(os.path.join(REF,"respawn","respawn.jpg")).convert("RGBA"); S.alpha_composite(sp,(1000,560))
kut=(1200,560,1900,1100); kut2=(760,420,1460,960)
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf"),22)
a,b,c=O.crop(kut).convert("RGB"),N.crop(kut).convert("RGB"),S.crop(kut2).convert("RGB")
w,h=a.size; o=Image.new("RGB",(w*3+40,h+40),(24,24,28)); d=ImageDraw.Draw(o)
for i,(im,t) in enumerate(((a,"ORİJİNAL"),(b,"YENİ (sprite aynı yerde, fark %.1f/255)"%fark),(c,"YENİ — başka sahnede"))):
    o.paste(im,(i*(w+20),40)); d.text((i*(w+20)+6,8),t,font=F,fill=(255,220,120))
o.save(os.path.join(B_,"..","..","onizlemeler","tezgah_onizleme.png")); print("fark %.2f"%fark,o.size)

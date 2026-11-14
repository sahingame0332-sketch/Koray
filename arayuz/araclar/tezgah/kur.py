#!/usr/bin/env python3
"""Tezgah onizlemesi: on ve yan gorunus — orijinal / ayni yerde sprite / baska sahnede.  Cikti: onizlemeler/tezgah_onizleme.png"""
import os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","tezgah"); REF=os.path.join(B_,"..","..","referans_gorseller")
J=json.load(open(os.path.join(K,"olculer.json")))
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf"),22)
satir=[]
for ad,dosya,spr,kut,sx,kut2 in (("ÖN","tezgah.jpg","tezgah.png",(1200,560,1900,1100),(1000,560),(760,420,1460,960)),
                                 ("YAN","tezgah_yan.jpg","tezgah_yan.png",(860,330,1560,870),(1060,600),(820,460,1520,1000))):
    sp=Image.open(os.path.join(K,spr)); O=Image.open(os.path.join(REF,"tezgah",dosya)).convert("RGBA")
    x,y=J["on" if ad=="ÖN" else "yan"]["ekran_kutu"][:2]; N=O.copy(); N.alpha_composite(sp,(x,y))
    fk=np.abs(np.asarray(O.convert("RGB")).astype(float)-np.asarray(N.convert("RGB")).astype(float))[y:y+sp.height,x:x+sp.width].mean()
    S=Image.open(os.path.join(REF,"respawn","respawn.jpg")).convert("RGBA"); S.alpha_composite(sp,sx)
    a,b,c=O.crop(kut).convert("RGB"),N.crop(kut).convert("RGB"),S.crop(kut2).convert("RGB"); w,h=a.size
    o=Image.new("RGB",(w*3+40,h+40),(24,24,28)); d=ImageDraw.Draw(o)
    for i,(im,t) in enumerate(((a,ad+" — ORİJİNAL"),(b,ad+" — YENİ aynı yerde (fark %.1f)"%fk),(c,ad+" — YENİ başka sahnede"))):
        o.paste(im,(i*(w+20),40)); d.text((i*(w+20)+6,8),t,font=F,fill=(255,220,120))
    satir.append(o)
z=Image.new("RGB",(satir[0].width,satir[0].height*2+16),(24,24,28)); z.paste(satir[0],(0,0)); z.paste(satir[1],(0,satir[0].height+16))
z.save(os.path.join(B_,"..","..","onizlemeler","tezgah_onizleme.png")); print(z.size)

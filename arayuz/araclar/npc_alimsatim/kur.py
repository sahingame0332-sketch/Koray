#!/usr/bin/env python3
"""Kurucunun benzetimi: 4 durum (Buy Item Count / Need Money / Sell Item Count / Earn Money).
Zemin: pencere ici arkadan sizan isik (<=20) aynen birakilir (alfa 0.97 siyah bunu verir), ustune krom + yazilar.
Cikti: onizlemeler/npc_alimsatim_onizleme.png"""
import os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","npc_alimsatim"); REF=os.path.join(B_,"..","..","referans_gorseller","npc_alimsatim")
J=json.load(open(os.path.join(K,"olculer.json"))); Y_=J["yazi"]
SB=os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf")
def H(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def aralikli(d,t,f,s,cx,cy,renk):
    w=sum(f.getlength(c) for c in t)+s*(len(t)-1); b=f.getbbox("H"); x=cx-w/2; y=cy-(b[1]+b[3])/2
    for c in t: d.text((x,y),c,font=f,fill=renk); x+=f.getlength(c)+s
def kur(k,ad,satir,sayi):
    O=np.asarray(Image.open(os.path.join(REF,k+".jpg")).convert("RGB")).astype(float)
    x,y,w,h=J["ic"]; S=O.copy(); ic=S[y:y+h,x:x+w]; S[y:y+h,x:x+w]=np.minimum(ic,20)          # yalniz sizinti
    im=Image.fromarray(S.astype(np.uint8)).convert("RGBA"); sx,sy=J["sprite"][:2]
    im.alpha_composite(Image.open(os.path.join(K,"pencere.png")),(sx,sy))
    if sayi is not None: im.alpha_composite(Image.open(os.path.join(K,"giris_kutusu.png")),tuple(J["giris"][:2]))
    d=ImageDraw.Draw(im); f=ImageFont.truetype(SB,Y_["punto"])
    aralikli(d,ad,f,Y_["harf_araligi"],*Y_["baslik_merkez"],H(Y_["renk"])); aralikli(d,satir,f,Y_["harf_araligi"],*Y_["satir2_merkez"],H(Y_["renk"]))
    if sayi is not None:
        fs=ImageFont.truetype(SB,Y_["sayi"]["punto"]); b=fs.getbbox(sayi); d.text((Y_["sayi"]["sol"]-b[0],Y_["sayi"]["merkez_y"]-(b[1]+b[3])/2),sayi,font=fs,fill=H(Y_["sayi"]["renk"]))
    kut=(1640,520,2310,815); o=Image.fromarray(O.astype(np.uint8)).crop(kut); n=im.convert("RGB").crop(kut)
    return o,n,np.abs(np.asarray(o).astype(float)-np.asarray(n).astype(float)).mean()
DUR=[("al_adet","Holy water","Buy Item Count:","1"),("al_para","Holy water","Need Money : 70",None),
     ("sat_adet","Holy water","Sell Item Count:","3"),("sat_para","Holy water","Earn Money : 33",None)]
F=ImageFont.truetype(SB,22); sat=[]
for k,a,s,n in DUR:
    o,y,fk=kur(k,a,s,n); c=Image.new("RGB",(o.width*2+20,o.height+36),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((6,6),"%s — sol ORİJİNAL · sağ YENİ  (ort. fark %.1f/255)"%(s,fk),font=F,fill=(255,220,120)); c.paste(o,(0,36)); c.paste(y,(o.width+20,36)); sat.append(c); print(k,round(fk,2))
o=Image.new("RGB",(sat[0].width*2+20,sat[0].height*2+20),(24,24,28))
for i,s in enumerate(sat): o.paste(s,((i%2)*(s.width+20),(i//2)*(s.height+20)))
o.save(os.path.join(B_,"..","..","onizlemeler","npc_alimsatim_onizleme.png")); print(o.size)

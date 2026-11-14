#!/usr/bin/env python3
"""Kurucunun Python benzetimi: ayni sprite + koordinat + font/punto ile yeniden kurar, orijinalle yan yana.
Cikti: onizlemeler/genie_onizleme.png"""
import json, numpy as np
from PIL import Image, ImageDraw, ImageFont
from ortak import *
KF=os.path.join(B_,"..","..","kaynak","char_info","fonts")
SB=os.path.join(KF,"RobotoSlab-Bold.ttf"); SR="/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Regular.otf"
ONZ=os.path.join(B_,"..","..","onizlemeler")
def sp(ad): return Image.open(os.path.join(OUT,ad+".png")).convert("RGBA")
def yazi(im,t,font,p,renk,cx,cy,hiza="orta",x0=None,dis=None):
    f=ImageFont.truetype(font,p); d=ImageDraw.Draw(im); b=d.textbbox((0,0),t,font=f)
    x=(cx-(b[0]+b[2])/2) if hiza=="orta" else (x0-b[0]); y=cy-(b[1]+b[3])/2
    if dis:
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx or dy: d.text((x+dx,y+dy),t,font=f,fill=dis)
    d.text((x,y),t,font=f,fill=renk)
# Olculen yazilar (punto.py): font, punto, renk, merkez / sol kenar
PANEL_YAZI=[("Time Left : 244 Minute(s)",SR,18,(0xFF,0xFC,0xEA),2502,137.5,"orta",None,(40,20,0)),
            ("Ares - 1",SB,21,(0xAF,0xEB,0x9F),2500.5,170,"orta",None,None),
            ("CR : 01:18:08",SB,23,(0xDC,0xF1,0x9E),None,214,"sol",2393,None),
            ("Channel 2",SB,23,(0xEE,0xF4,0xEF),None,266.5,"sol",2393,None)]
def panel(im):
    pj=json.load(open(os.path.join(OUT,"..","panel_olculer.json"))); x,y,w,h=pj["panel"]
    im.alpha_composite(sp("genie_panel"),(x,y))
    for t,f,p,r,cx,cy,hz,x0,dis in PANEL_YAZI: yazi(im,t,f,p,r,cx,cy,hz,x0,dis)
def pencere(im,degerler=(40,70,80,50),onaylar=(False,False,True,False)):
    pj=json.load(open(os.path.join(OUT,"..","pencere_olculer.json")))
    x,y,w,h=pj["zemin"]; a=np.asarray(im).astype(float); a[y:y+h,x:x+w,:3]*=(1-pj["alfa"]); im.paste(Image.fromarray(a.astype(np.uint8)))
    sx,sy=pj["sprite"][:2]; im.alpha_composite(sp("aa_pencere"),(sx,sy))
    top=sp("aa_topuz"); en=[45,100,100,100]
    for k,v in enumerate(degerler):
        p=v/en[k]; cx=363.5+p*405; ty=pj["topuzlar"][k][1]
        im.alpha_composite(top,(int(round(cx-top.width/2)),ty))
        yazi(im,("%d" if k==0 else "%%%d")%v,SB,24,(0xD2,0xA7,0x76),818,pj["iz"]["y"][k]+7)
    im.alpha_composite(sp("aa_etiketler"),(sx,sy))
    on=sp("aa_onay"); ox,oy=pj["onay"][:2]
    for k,(bx,by,bw,bh) in enumerate(pj["kutular"]):
        if onaylar[k]: im.alpha_composite(on,(ox+bx-612,oy+by-1036))
ROZET_DY=0
def aktif(im):
    kj=json.load(open(os.path.join(OUT,"..","kilit_olculer.json"))); k=sp("genie_kilit")
    for (x,y) in kj["merkezler"]: im.alpha_composite(k,(x-k.width//2,y-k.height//2))
    r=kj["rozet"]; cx,cy=r["merkez"]; cy+=ROZET_DY; ro=sp("genie_rozet"); im.alpha_composite(ro,(cx-ro.width//2,cy-ro.height//2))
def F(ad): return Image.open(os.path.join(REF,ad+".jpg")).convert("RGBA")
P=[]; fark={}
# 1) panel
o=F("g_once"); n=F("g_once"); panel(n); kut=(2300,45,2672,300)
P.append(("Knight Genie paneli",o.crop(kut),n.crop(kut),2.0))
# 2) pencere
o=F("g_pencere"); n=F("g_once"); pencere(n); kut=(262,30,898,1192)
P.append(("AUTO ATTACK SETTINGS",o.crop(kut),n.crop(kut),1.0))
# 3) aktif: kilitler (ayni HUD) + rozet (baska sahne -> g_aktif uzerine degil, g_once uzerine)
o=F("g_aktif"); n=F("g_once"); ROZET_DY=384-470; aktif(n); kut=(1180,220,2560,1000)   # rozet ad etiketine gore: g_once etiketi y~384, g_aktif y~470; kut=(1180,220,2560,1000)
P.append(("Genie aktif: GENIE rozeti + skill kilitleri",o.crop(kut),n.crop(kut),0.62))
for ad,a,b,_ in P:
    A=np.asarray(a.convert("RGB")).astype(float); Bb=np.asarray(b.convert("RGB")).astype(float); fark[ad]=round(float(np.abs(A-Bb).mean()),2)
print(fark)
FT=ImageFont.truetype(SB,24); sat=[]
for ad,a,b,s in P:
    a=a.resize((int(a.width*s),int(a.height*s))); b=b.resize(a.size)
    c=Image.new("RGB",(a.width*2+30,a.height+44),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((8,8),"%s — sol: ORİJİNAL · sağ: YENİ (kurucu benzetimi)"%ad,font=FT,fill=(255,220,120))
    c.paste(a.convert("RGB"),(0,44)); c.paste(b.convert("RGB"),(a.width+30,44)); sat.append(c)
W=sum(s.width for s in sat[:2])+20; H=max(sat[0].height,sat[1].height)+sat[2].height+20
o=Image.new("RGB",(max(W,sat[2].width),H),(24,24,28))
o.paste(sat[1],(0,0)); o.paste(sat[0],(sat[1].width+20,0)); o.paste(sat[2],(sat[1].width+20,sat[0].height+20))
o.save(os.path.join(ONZ,"genie_onizleme.png")); print(o.size)

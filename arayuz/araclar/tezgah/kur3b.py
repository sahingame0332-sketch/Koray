#!/usr/bin/env python3
"""3B tezgahin yazilim benzetimi (dik izdusum kamera, ressam algoritmasi) — Unity'deki mesh ile ayni olculer/UV.
(1) on fotografin kamerasi, (2) yan fotografin kamerasi, (3) iki yeni aci. Orijinallerle yan yana.
Olculer (karakter boyu 1.8 birim icin, metre): W 0.78, D 0.40, on yukseklik 0.59, arka yukseklik 0.99 (tahta 45 derece one egik).
Cikti: onizlemeler/tezgah3b_onizleme.png"""
import os, math, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
B_=os.path.dirname(os.path.abspath(__file__)); K=os.path.join(B_,"..","..","kaynak","tezgah","3b"); R=os.path.join(B_,"..","..","referans_gorseller")
OL=json.load(open(os.path.join(K,"olculer.json"))) if os.path.exists(os.path.join(K,"olculer.json")) else None
W,D,HF,HB=0.78,0.42,0.59,0.99
T={k:Image.open(os.path.join(K,k+".png")).convert("RGBA") for k in ("ust","on","yan")}
x0,x1,z0,z1=-W/2,W/2,-D/2,D/2
# (doku, [kose(x,y,z) ile uv sol-ust/sag-ust/sag-alt/sol-alt sirasi], normal, ayna)
YUZLER=[("on",[(x0,HF,z1),(x1,HF,z1),(x1,0,z1),(x0,0,z1)],(0,0,1),False),
        ("ust",[(x0,HB,z0),(x1,HB,z0),(x1,HF,z1),(x0,HF,z1)],(0,math.cos(math.atan2(HB-HF,D)),math.sin(math.atan2(HB-HF,D))),False),
        ("yan",[(x0,HB,z0),(x0,HF,z1),(x0,0,z1),(x0,0,z0)],(-1,0,0),False),          # sol yan: arka solda, on sagda
        ("yan",[(x1,HF,z1),(x1,HB,z0),(x1,0,z0),(x1,0,z1)],(1,0,0),True),            # sag yan: ayna
        ("yan",[(x1,HB,z0),(x0,HB,z0),(x0,0,z0),(x1,0,z0)],(0,0,-1),False)]          # arka (fotograf yok)
def homografi(src,dst):
    A=[];b=[]
    for (x,y),(u,v) in zip(src,dst): A+=[[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]; b+=[u,v]
    return np.linalg.solve(np.array(A,float),np.array(b,float))
def ciz(boyut,merkez,s,yaw,pitch):
    cy,sy=math.cos(math.radians(yaw)),math.sin(math.radians(yaw)); cp,sp=math.cos(math.radians(pitch)),math.sin(math.radians(pitch))
    def proj(p):
        x,y,z=p; xr=x*cy+z*sy; zr=-x*sy+z*cy
        return (merkez[0]+xr*s, merkez[1]-(y*cp-zr*sp)*s, zr*cp+y*sp)
    vd=(-sy*cp*0+0,0,0)
    kam=np.array([sy*cp, sp, cy*cp])                    # kameraya dogru birim vektor (dunya)
    out=Image.new("RGBA",boyut,(0,0,0,0)); sira=[]
    for ad,P,n,ayna in YUZLER:
        if np.dot(n,kam)<=0.02: continue
        q=[proj(p) for p in P]; sira.append((np.mean([c[2] for c in q]),ad,q,ayna))
    for _,ad,q,ayna in sorted(sira):
        t=T[ad].transpose(Image.FLIP_LEFT_RIGHT) if ayna else T[ad]; w,h=t.size
        c=homografi([(a,b) for a,b,_ in q],[(0,0),(w,0),(w,h),(0,h)])
        katman=t.transform(boyut,Image.PERSPECTIVE,tuple(c),Image.BICUBIC)
        m=Image.new("L",boyut,0); ImageDraw.Draw(m).polygon([(a,b) for a,b,_ in q],fill=255)
        out.paste(katman,(0,0),m)
    return out
F=ImageFont.truetype(os.path.join(B_,"..","..","kaynak","char_info","fonts","RobotoSlab-Bold.ttf"),20)
on=Image.open(os.path.join(R,"tezgah","tezgah.jpg")).convert("RGBA"); yan=Image.open(os.path.join(R,"tezgah","tezgah_yan.jpg")).convert("RGBA")
pan=[]
# 1) on fotografin kamerasi: karakter 427 px -> s = 427/1.8*cos(pitch)^-1 ... olcek 270 px/m, pitch 28, yaw 22 (sol yuz gorunur)
bos=Image.open(os.path.join(R,"respawn","respawn.jpg")).convert("RGBA")
for ad,arka,kut,s,yaw,pitch in (("ÖN kamera",on,(1440,640,1840,1080),285,-22,29),("YAN kamera",yan,(1020,400,1340,740),230,-66,30)):
    o=arka.crop(kut).convert("RGB"); w,h=o.size
    # yeni model ayni olcek ve kamerayla, bos cim uzerinde (orijinal tezgahin ustune cizmek karistiriyordu)
    yeni=Image.alpha_composite(bos.crop((900,520,900+w,520+h)),ciz((w,h),(w*0.5,h*0.86),s,yaw,pitch)).convert("RGB")
    pan.append((ad+" — ORİJİNAL",o)); pan.append((ad+" — 3B",yeni))
for ad,yaw,pitch in (("arkadan sağ",140,30),("üstten",30,55)):
    im=Image.alpha_composite(bos,ciz(bos.size,(1100,850),270,yaw,pitch)).crop((900,520,1300,960)).convert("RGB"); pan.append(("3B — "+ad,im))
H=max(p[1].height for p in pan); Wt=sum(p[1].width for p in pan)+10*len(pan)
c=Image.new("RGB",(Wt,H+34),(24,24,28)); d=ImageDraw.Draw(c); x=0
for t,im in pan: c.paste(im,(x,34)); d.text((x+4,6),t,font=F,fill=(255,220,120)); x+=im.width+10
c.save(os.path.join(B_,"..","..","onizlemeler","tezgah3b_onizleme.png")); print(c.size)

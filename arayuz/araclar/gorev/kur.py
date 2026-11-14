#!/usr/bin/env python3
"""Kurucunun benzetimi: q_open sahnesi + siyah zemin (olculen alfa) + taban + parcalar + yazilar  <->  orijinal.
"?" rozeti: q_once rozetsiz zemin yok -> merdivenin rozet disindaki satir medyani ustune.  Cikti: onizlemeler/gorev_onizleme.png"""
from ortak import *
from PIL import ImageDraw, ImageFont
LS="/usr/share/fonts/truetype/liberation/"; FB=LS+"LiberationSans-Bold.ttf"; FR=LS+"LiberationSans-Regular.ttf"
ONZ=os.path.join(B_,"..","..","onizlemeler")
PJ=json.load(open(os.path.join(OUT,"..","pencere_olculer.json"))); KJ=json.load(open(os.path.join(OUT,"..","krom_olculer.json")))
def sp(ad): return Image.open(os.path.join(OUT,ad+".png")).convert("RGBA")
def yazi(im,t,font,p,renk,x=None,y=None,cx=None,cy=None,sag=None,alt=None,golge=True):
    f=ImageFont.truetype(font,p); d=ImageDraw.Draw(im); b=d.textbbox((0,0),t,font=f)
    if cx is not None: x=cx-(b[0]+b[2])/2
    elif sag is not None: x=sag-b[2]
    else: x=x-b[0]
    if cy is not None: y=cy-(b[1]+b[3])/2
    elif alt is not None: y=alt-b[3]
    else: y=y-b[1]
    if golge:                                                    # beyaz yazilarin koyu dis hatti (Unity: Outline 1 px)
        for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(1,1)): d.text((x+dx,y+dy),t,font=f,fill=(0,0,0,200))
    d.text((x,y),t,font=f,fill=renk)
def H(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def zemin(im,kutu,a):
    x,y,w,h=kutu; A=np.asarray(im).astype(float); A[y:y+h,x:x+w,:3]*=(1-a); return Image.fromarray(A.astype(np.uint8))
def liste(im):
    p=PJ["liste"]; im=zemin(im,p["zemin"],KJ["liste"]["alfa"]); x,y=p["sprite"][:2]
    im.alpha_composite(sp("liste_pencere"),(x,y))
    cx,cy,r=p["portre"]; im.alpha_composite(sp("portre"),(cx-r,cy-r))
    yazi(im,"Test NPC Description.",FB,16,H(p["aciklama_renk"]),x=p["aciklama"][0],y=p["aciklama"][1],golge=False)
    sx,sy,sw,sh=p["satir"]; im.alpha_composite(sp("gorev_satiri"),(sx,sy))
    yazi(im,"Starter Weapon&Armor",FB,22,H("#F6E1E1"),cx=p["satir_yazi_merkez"][0],cy=p["satir_yazi_merkez"][1])
    return im
ODUL=["Rapt Bow(+2)","Stiletto(+2)","Stiletto(+2)","Silan Pauldron","Silan Pad","Silan Helmet","Silan Gauntlet","Silan Boots"]
def detay(im):
    p=PJ["detay"]; im=zemin(im,p["zemin"],KJ["detay"]["alfa"]); x,y=p["sprite"][:2]
    im.alpha_composite(sp("detay_pencere"),(x,y))
    cx,cy,r=p["portre"]; im.alpha_composite(sp("portre"),(cx-r,cy-r))
    yazi(im,"Starter Weapon&Armor",FB,19,H("#EEDADA"),cx=p["baslik_merkez"][0],cy=p["baslik_merkez"][1])
    yazi(im,"Kill: 20x Orc Watcher",FB,16,H(p["aciklama_renk"]),x=p["aciklama"][0],y=p["aciklama"][1],golge=False)
    hx,hy=p["hedef"][:2]; im.alpha_composite(sp("hedef_satiri"),(hx,hy))
    ix,iy=p["hedef_ikon"][:2]; im.alpha_composite(sp("ikon_hedef"),(ix,iy))
    yazi(im,"Hunt: Shilan",FB,16,H("#EAD8D8"),x=1185,y=514); yazi(im,"Shilan öldür.",FB,16,H("#EAD7D7"),x=1185,y=545)
    yazi(im,"25",FB,18,H("#EED8D4"),sag=p["sayi_sag_alt"][0],alt=p["sayi_sag_alt"][1])
    ox,oy=p["odul"][:2]; ax,ay=p["odul_adim"]
    for i,ad in enumerate(ODUL):
        c,r_=i%2,i//2; X=ox+c*ax; Yy=oy+r_*ay
        im.alpha_composite(sp("odul_yuvasi"),(X,Yy)); im.alpha_composite(sp("ikon_odul_%d"%(i+1)),(X+13,Yy+15))
        yazi(im,ad,FB,16,H("#E9D6D6"),x=X+67,y=Yy+19)
    yazi(im,"Accepted",FB,21,H("#F0DDDE"),cx=p["kabul_yazi_merkez"][0],cy=p["kabul_yazi_merkez"][1])
    return im
def F(ad): return Image.open(os.path.join(REF,ad+".jpg")).convert("RGBA")
P=[]
n=liste(F("q_open")); P.append(("QuestList",F("q_liste").crop((1030,360,1690,850)),n.crop((1030,360,1690,850)),1.0))
n=detay(F("q_open")); P.append(("Görev detayı",F("q_detay").crop((1045,165,1655,1015)),n.crop((1045,165,1655,1015)),1.0))
# rozet
O=Y("q_once"); bg=np.repeat(np.median(O[0:350,700:790],1)[:,None,:],350,1)
Rz=np.asarray(sp("soru_rozeti")).astype(float); yeni=np.clip(bg*(1-Rz[:,:,3:]/255)+Rz[:,:,:3],0,255)
P.append(('"?" rozeti (zemin: merdiven satırı)',F("q_once").crop((810,0,1160,350)),Image.fromarray(yeni.astype(np.uint8)).convert("RGBA"),1.0))
fark={a:round(float(np.abs(np.asarray(o.convert("RGB")).astype(float)-np.asarray(y.convert("RGB")).astype(float)).mean()),2) for a,o,y,_ in P}
print(fark)
FT=ImageFont.truetype("/home/user/Koray/arayuz/kaynak/char_info/fonts/RobotoSlab-Bold.ttf",22); sat=[]
for ad,a,b,s in P:
    c=Image.new("RGB",(a.width*2+20,a.height+40),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((6,6),"%s — sol: ORİJİNAL · sağ: YENİ"%ad,font=FT,fill=(255,220,120)); c.paste(a.convert("RGB"),(0,40)); c.paste(b.convert("RGB"),(a.width+20,40)); sat.append(c)
W=sat[0].width+sat[1].width+20; Hh=max(sat[1].height,sat[0].height+sat[2].height+20)
o=Image.new("RGB",(W,Hh),(24,24,28)); o.paste(sat[1],(0,0)); o.paste(sat[0],(sat[1].width+20,0)); o.paste(sat[2],(sat[1].width+20,sat[0].height+20))
o.save(os.path.join(ONZ,"gorev_onizleme.png")); print(o.size)

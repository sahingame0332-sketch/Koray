#!/usr/bin/env python3
"""Unity kurucusunun (OlymposOyunIciBuilder.cs) Python benzetimi.
Ayni sprite'lar + ayni koordinatlar + ayni punto ile her ogeyi yeniden kurar ve
orijinal kareyle yan yana koyar.  Cikti: arayuz/onizlemeler/oyun_ici_*.png"""
import os, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
B=os.path.dirname(os.path.abspath(__file__))
REF=os.path.join(B,"..","..","referans_gorseller","oyun_ici"); S=os.path.join(B,"..","..","kaynak","oyun_ici","sprites")
KF=os.path.join(B,"..","..","kaynak","char_info","fonts"); ONZ=os.path.join(B,"..","..","onizlemeler")
FONT={"RB":KF+"/Roboto-Bold.ttf","RR":KF+"/Roboto-Regular.ttf","SB":KF+"/RobotoSlab-Bold.ttf",
      "SR":"/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Regular.otf",
      "DB":"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"}
_f={}
def fnt(k,p):
    if (k,p) not in _f: _f[(k,p)]=ImageFont.truetype(FONT[k],p)
    return _f[(k,p)]
def kare(ad): return Image.open(os.path.join(REF,ad+".jpg")).convert("RGBA")
def spr(ad): return Image.open(os.path.join(S,ad+".png")).convert("RGBA")
class Tuval:
    def __init__(self,im): self.im=im; self.d=ImageDraw.Draw(self.im,"RGBA")
    def kutu(self,x,y,w,h,renk,alfa):
        self.im.alpha_composite(Image.new("RGBA",(int(w),int(h)),tuple(renk)+(int(round(alfa*255)),)),(int(x),int(y)))
    def spr(self,ad,x,y,w=None,h=None):
        s=spr(ad) if isinstance(ad,str) else ad
        if w: s=s.resize((int(w),int(h)),Image.LANCZOS)
        self.im.alpha_composite(s,(int(round(x)),int(round(y))))
    def yaz(self,t,x,y,f,p,renk,hiza="sol",dis=1,disrenk=(0,0,0,255)):
        """(x,y): murek kutusunun sol-ust (sol), ust-orta (orta) ya da sag-ust (sag) noktasi."""
        fo=fnt(f,p); l,tp,r,b=fo.getbbox(t); w=r-l
        if hiza=="orta": x-=w/2.0
        elif hiza=="sag": x-=w
        self.d.text((x-l,y-tp),t,font=fo,fill=renk,stroke_width=dis,stroke_fill=disrenk)
        return w
def daire_ikon(ikon,cap):
    i=spr(ikon).resize((cap,cap),Image.LANCZOS); m=spr("slot_maske").resize((cap,cap),Image.LANCZOS)
    a=np.asarray(i).copy(); a[:,:,3]=np.asarray(m)[:,:,3]; return Image.fromarray(a,"RGBA")
PEMBE=(255,230,232,255); BEYAZ=(255,255,255,255)

# ---------------------------------------------------------------- 1) esya eylem penceresi
def esya_penceresi(t,x0,y0,ad,tur,aciklama,ikon):
    t.kutu(x0,y0,663,313,(0,0,0),0.92)
    t.spr(ikon,x0+9,y0+9); t.spr("ikon_cerceve",x0+2,y0+2)
    w=t.yaz(ad,x0+113,y0+11,"RB",36,PEMBE,dis=0)
    t.yaz(tur,x0+113,y0+50,"RB",27,(252,209,0,255),dis=0)
    sag=113+w+20                                   # icerik genisligi = ad + 20
    t.kutu(x0+11,y0+236,sag-11,1,(65,52,46),1.0)
    t.yaz(aciklama,x0+(12+sag)/2.0,y0+177,"RB",27,PEMBE,"orta",dis=0)
    for a,x in (("btn_use_self",11),("btn_use_target",173),("btn_equip",334),("btn_close_kirmizi",496)):
        t.spr(a,x0+x,y0+248)
def panel_esya():
    t=Tuval(kare("v1_once")); esya_penceresi(t,1360,740,"Scroll of 500HP Up(L)","Store Item","Increases HP by 500.","ikon_hp_scroll")
    k=(1300,700,2090,1100); return kare("v1_popup_hp").crop(k), t.im.crop(k)

# ---------------------------------------------------------------- 2) buff cubugu + menu
def buff(t,x,y,ikon,sure):
    t.spr(ikon,x+3,y+3,58,58); t.spr("buff_cerceve",x,y)
    t.yaz(sure,x+32,y+41,"RB",27,PEMBE,"orta",1)
def panel_buff():
    t=Tuval(kare("v1_buffsiz"))
    sag=2309
    for i,ik in enumerate(("ikon_hp_scroll","ikon_hiz_iksiri","ikon_zirh_scroll")): buff(t,sag-64-66*(2-i),56,ik,"59m")
    cx=2245+32                                    # secilen ikonun merkezi
    t.spr("menu_ok",cx-15,120); t.spr("btn_remove",cx-97,136); t.spr("btn_menu_close",cx-97,206)
    k=(2090,30,2400,290); return kare("v1_remove").crop(k), t.im.crop(k)

# ---------------------------------------------------------------- 3) hizli slotlar + hedef iptal
def slot(t,cx,cy,ikon=None,adet=None):
    if ikon:
        t.spr(daire_ikon(ikon,146),cx-73,cy-73)
    else:
        m=np.asarray(spr("slot_maske")).copy().astype(float); m[:,:,:3]=0; m[:,:,3]*=0.88
        t.spr(Image.fromarray(m.astype(np.uint8),"RGBA"),cx-72,cy-72)
    t.spr("slot_halka",cx-82,cy-82)
    if adet is not None: t.yaz(str(adet),cx,cy+40,"RB",31,BEYAZ,"orta",1)
def panel_slot():
    t=Tuval(kare("v2_hedef"))
    slot(t,2085,781,"ikon_hiz_iksiri",2); slot(t,2235,634,"ikon_zirh_scroll",3); slot(t,2431,638,"ikon_hp_scroll",4)
    slot(t,2193,452); slot(t,2030,595)
    t.spr("btn_hedef_iptal",2503,784)
    k=(1930,360,2712,1000); return kare("v2_hedef").crop(k), t.im.crop(k)

# ---------------------------------------------------------------- 4) hedef cubugu + Show Drops
def panel_hedef():
    t=Tuval(kare("v1_buffsiz"))
    t.yaz("Kecoon fighter",1370,64,"DB",30,(254,83,86,255),"orta",2,(70,12,14,255))
    t.spr("hedef_cubuk",1178,96)
    t.yaz("Lv.12",1190,111,"DB",16,(142,225,58,255),"sol",1,(20,50,10,255))
    t.spr("btn_show_drops",1298,134)
    k=(1150,40,1610,200); return kare("v2_hedef").crop(k), t.im.crop(k)

# ---------------------------------------------------------------- 5) Drop List Search
DX,DY=176,82
def drop_slot(t,i,ikon,oran,renk=BEYAZ):
    c,r=i%5,i//5; x=DX+64+115*c; y=DY+703+111*r
    t.spr(ikon,x+7,y+7); t.spr("drop_slot_dolu",x,y)
    fo=fnt("SB",19); l,tp,rr,b=fo.getbbox(oran); w=rr-l
    t.kutu(x+97-w-3,y+75,w+5,23,(0,0,0),1.0)
    t.yaz(oran,x+97,y+79,"SB",19,renk,"sag",0)
def drop_penceresi(t,sayfa,slotlar,ust_sayfa="0/0"):
    t.kutu(DX+6,DY+8,683,1107,(0,0,0),0.89)
    t.spr("drop_krom",DX,DY); t.spr("onay_isareti",DX+28,DY+74); t.spr("drop_yer_tutucu",DX+150,DY+256)
    t.yaz(ust_sayfa,DX+350.5,DY+657,"SR",32,(227,177,112,255),"orta",0)
    t.yaz(sayfa,DX+352.5,DY+1061,"SR",32,(227,177,112,255),"orta",0)
    for i,(ik,o,rk) in enumerate(slotlar): drop_slot(t,i,ik,o,rk)
def panel_drop1():
    t=Tuval(kare("v2_hedef"))
    drop_penceresi(t,"1/1",[("drop_grup","Middle",BEYAZ),("drop_grup","Middle",BEYAZ),("drop_ornek_0","Low",(250,232,0,255))])
    k=(150,60,900,1220); return kare("v2_drop_bos").crop(k), t.im.crop(k)
def ipucu(t,x0,y0):
    t.kutu(x0,y0,484,621,(0,0,0),0.93)
    t.spr("drop_ornek_temiz",x0+12,y0+12); t.spr("ikon_cerceve",x0+5,y0+5)
    M=(202,137,231,255)
    t.yaz("Quilted Pauldron(+3)",x0+115,y0+11,"RB",36,M,dis=0); t.yaz("Upgrade Item",x0+115,y0+50,"RB",27,M,dis=0)
    w=t.yaz("Drop Rate :",x0+13,y0+139,"RB",32,(255,16,0,255)); t.yaz("Middle",x0+183,y0+138,"RB",32,PEMBE)
    for y in (194,355,543): t.kutu(x0+12,y0+y,458,1,(64,58,55),1.0)
    t.yaz("Defense Ability : 28",x0+12,y0+230,"RB",29,PEMBE)
    t.yaz("Health Bonus : 4",x0+12,y0+269,"RB",29,(150,192,25,255))
    t.yaz("Required Strenght : 66",x0+13,y0+307,"RB",29,(254,0,1,255))
    t.yaz("(Warrior Item)",x0+242,y0+389,"RB",27,(254,0,1,255),"orta")
    t.yaz("Item Grade : Low Class",x0+242,y0+422,"RB",27,(128,195,102,255),"orta")
    t.yaz("The pauldron worn by",x0+242,y0+453,"RB",27,PEMBE,"orta")
    t.yaz("novice warriors.",x0+242,y0+484,"RB",27,PEMBE,"orta")
    t.spr("btn_close_kirmizi",x0+12,y0+556)
def panel_drop2():
    t=Tuval(kare("v2_hedef"))
    sira=[1,2,3,4,5,1,2,3,4,5,6,7,3,8,9]
    drop_penceresi(t,"1/2",[("drop_ornek_%d"%i,"Middle",BEYAZ) for i in sira])
    ipucu(t,591,499)
    k=(150,60,1100,1220); return kare("v2_drop_ipucu").crop(k), t.im.crop(k)

# ---------------------------------------------------------------- 6) Save Skill Slot Stat
def panel_save():
    t=Tuval(kare("foto_saveslot")); SX,SY=1196,110
    # benzetim icin pencerenin altindaki orijinali ortmek gerek: once ayni yeri cimle doldur
    cim=kare("v1_once").crop((300,560,300+526,560+1056-400)).resize((526,1056))
    t.im.paste(cim,(SX,SY))
    t.kutu(SX+12,SY+68,498,986,(0,0,0),0.95)
    t.spr("saveslot_krom",SX,SY)
    durum=["Fire:41 - Ice:23\nLightning:0 - Master:0","- Empty -","- Empty -","- Empty -"]
    for k,dr in enumerate(durum):
        sat=dr.split("\n"); y0=SY+85+245*k+122-(len(sat)-1)*21
        for i,sx in enumerate(sat): t.yaz(sx,SX+262,y0+i*42-14,"SB",29,BEYAZ,"orta",1)
    kk=(1180,100,1740,1180); return kare("foto_saveslot").crop(kk), t.im.crop(kk)

def yan_yana(ad,o,y,olcek=1.0,baslik=""):
    if olcek!=1.0:
        o=o.resize((int(o.width*olcek),int(o.height*olcek)),Image.LANCZOS); y=y.resize(o.size,Image.LANCZOS)
    W=o.width*2+30; H=o.height+64
    c=Image.new("RGB",(W,H),(24,24,28)); d=ImageDraw.Draw(c)
    d.text((10,8),baslik,font=fnt("RB",24),fill=(255,220,120))
    d.text((10,36),"ORİJİNAL",font=fnt("RB",18),fill=(200,200,200)); d.text((o.width+30,36),"YENİ (Unity kurulumunun benzetimi)",font=fnt("RB",18),fill=(140,230,140))
    c.paste(o.convert("RGB"),(10,60)); c.paste(y.convert("RGB"),(o.width+20,60))
    c.save(os.path.join(ONZ,ad+".png")); return c
if __name__=="__main__":
    os.makedirs(ONZ,exist_ok=True)
    P=[("oyun_ici_1_esya_penceresi",panel_esya,1.0,"1a · Envanterden scroll basma — eşya penceresi"),
       ("oyun_ici_2_buff_sil",panel_buff,2.0,"1c · Basılan scrollu silme — buff ikonu + Remove / Close"),
       ("oyun_ici_3_slot_iptal",panel_slot,1.0,"1b · Skill bardan scroll basma  +  4 · Hedef iptal (X)"),
       ("oyun_ici_4_hedef",panel_hedef,1.6,"3a · Hedef çubuğu + Show Drops"),
       ("oyun_ici_5_drop",panel_drop1,0.8,"3b · Drop List Search — açılış"),
       ("oyun_ici_6_drop_ipucu",panel_drop2,0.8,"3c · Drop List Search — grup içi + eşya ipucu"),
       ("oyun_ici_7_save_slot",panel_save,0.8,"2 · Save Skill Slot Stat")]
    for ad,fn,olc,bas in P:
        o,y=fn(); c=yan_yana(ad,o,y,olc,bas); print(ad,c.size)

#!/usr/bin/env python3
"""Oyun ici yazilarin fontu + puntosu: referans karedeki murek maskesi ile aday fontun
rasterini karsilastirir (IoU). Dis hat (outline) murek kutusunu ~2 px buyuttugu icin
esik, yazinin kendi renginin cekirdegini secer."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
B=os.path.dirname(os.path.abspath(__file__)); REF=os.path.join(B,"..","..","referans_gorseller","oyun_ici")
KF=os.path.join(B,"..","..","kaynak","char_info","fonts")
ADAY={"Roboto-Bold":KF+"/Roboto-Bold.ttf","Roboto-Regular":KF+"/Roboto-Regular.ttf",
      "RobotoSlab-Bold":KF+"/RobotoSlab-Bold.ttf","RobotoSlab-Regular":"/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Regular.otf"}
def murek(m):
    ys,xs=np.nonzero(m)
    return None if len(xs)<10 else m[ys.min():ys.max()+1,xs.min():xs.max()+1]
def ciz(t,yol,p):
    f=ImageFont.truetype(yol,p); im=Image.new("L",(1800,260),0)
    ImageDraw.Draw(im).text((40,40),t,font=f,fill=255); return murek(np.asarray(im)>128)
def iou(a,b):
    h,w=max(a.shape[0],b.shape[0]),max(a.shape[1],b.shape[1])
    A=np.zeros((h,w),bool);Bm=np.zeros((h,w),bool)
    A[:a.shape[0],:a.shape[1]]=a;Bm[:b.shape[0],:b.shape[1]]=b
    return (A&Bm).sum()/max(1,(A|Bm).sum())
def hedef(kare,kutu,renk,tol):
    a=np.asarray(Image.open(os.path.join(REF,kare+".jpg")).convert("RGB")).astype(float)[kutu[1]:kutu[3],kutu[0]:kutu[2]]
    return murek(np.abs(a-np.array(renk,float)).max(2)<tol)
def olc(ad,metin,kare,kutu,renk,tol=70,fontlar=None):
    h=hedef(kare,kutu,renk,tol)
    if h is None: print("%-22s olculemedi"%ad); return
    r=[]
    for f in (fontlar or ADAY):
        en=(0,0)
        for p in range(10,64):
            m=ciz(metin,ADAY[f],p)
            if m is None: continue
            v=iou(h,m)
            if v>en[0]: en=(v,p)
        r.append((en[0],en[1],f))
    r.sort(reverse=True)
    print("%-22s %-24s murek %3dx%-3d | "%(ad,"'"+metin+"'",h.shape[1],h.shape[0])+"  ".join("%s %d (%.2f)"%(f,p,v) for v,p,f in r[:3]))
if __name__=="__main__":
    W=(245,235,235)
    olc("esya adi","Scroll of 500HP Up(L)","v1_popup_hp",(1360+108,740+6,1360+480,740+46),W)
    olc("esya turu","Store Item","v1_popup_hp",(1360+108,740+46,1360+260,740+80),(250,200,10),80)
    olc("esya aciklama","Increases HP by 500.","v1_popup_hp",(1360+110,740+170,1360+400,740+208),W)
    olc("buff suresi","59m","v1_buff3",(2182,92,2242,120),W,60)
    olc("slot adedi","4","v1_slotlar",(2400,670,2460,715),W,60)
    olc("hedef adi","Kecoon fighter","v2_hedef",(1230,58,1510,94),(235,70,80),70)
    olc("hedef seviye","Lv.12","v2_hedef",(1186,106,1240,128),(120,240,60),90)
    olc("drop etiket","Middle","v2_drop_izgara",(176+64+30,82+703+72,176+64+100,82+703+100),W,60)
    olc("drop sayfa","1/2","v2_drop_izgara",(176+320,82+1052,176+386,82+1096),(235,190,120),70)
    olc("ipucu adi","Quilted Pauldron(+3)","v2_drop_ipucu",(591+110,499+6,591+470,499+46),(200,110,235),80)
    olc("ipucu turu","Upgrade Item","v2_drop_ipucu",(591+110,499+44,591+300,499+80),(200,110,235),80)
    olc("ipucu drop","Drop Rate :","v2_drop_ipucu",(591+8,499+132,591+178,499+172),(240,30,30),90)
    olc("ipucu stat","Defense Ability : 28","v2_drop_ipucu",(591+8,499+224,591+280,499+262),W)
    olc("ipucu aciklama","The pauldron worn by","v2_drop_ipucu",(591+90,499+448,591+400,499+482),W)
    olc("save durum","- Empty -","foto_saveslot",(1196+190,110+425,1196+370,110+475),W)
    olc("save durum 2","Fire:41 - Ice:23","foto_saveslot",(1196+160,110+165,1196+400,110+203),W)

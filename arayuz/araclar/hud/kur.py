#!/usr/bin/env python3
"""Olculen degerlerden HUD'i yeniden kurar (onizleme)."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
S="/home/user/Koray/arayuz/kaynak/hud/sprites"
F="/home/user/Koray/arayuz/kaynak/char_info/fonts/RobotoSlab-Bold.ttf"
W,H=2266,1488
tuval=Image.open("dunya.png").convert("RGBA")
d=ImageDraw.Draw(tuval,"RGBA")
_f={}
def fnt(p):
    if p not in _f: _f[p]=ImageFont.truetype(F,p)
    return _f[p]
def spr(ad,x,y,alfa=255):
    im=Image.open(os.path.join(S,ad+".png")).convert("RGBA")
    if alfa<255:
        a=np.asarray(im).astype(float); a[:,:,3]*=alfa/255.0
        im=Image.fromarray(a.astype(np.uint8),"RGBA")
    tuval.alpha_composite(im,(x,y))
def kutu(x,y,w,h,renk,alfa):
    o=Image.new("RGBA",(w,h),tuple(renk)+(int(alfa*255),)); tuval.alpha_composite(o,(x,y))
def yaz(t,x,y,p,renk,hiza="sol",golge=2,orta_y=True):
    f=fnt(p); l,t_,r,b=f.getbbox(t); gw,gh=r-l,b-t_
    if hiza=="orta": x-=gw//2
    elif hiza=="sag": x-=gw
    if orta_y: y-=gh//2+t_
    if golge:
        d.text((x,y),t,font=f,fill=(0,0,0,210),stroke_width=golge,stroke_fill=(0,0,0,210))
    d.text((x,y),t,font=f,fill=renk)

# ---------------- sol ust ----------------
spr("durum_plaka",0,0)      # cubuklar dahil (dolu hal)
yaz("419/419",245,31,31,(255,255,255,255),"orta")
yaz("1162/1162",245,73,31,(255,255,255,255),"orta")
yaz("Exp. %0,07",245,113,22,(255,255,255,255),"orta")
yaz("xMegaTon",72,146,27,(243,255,230,255),"sol")
yaz("41",420,146,40,(239,195,129,255),"sag")
yaz("1526,490",330,192,33,(220,255,170,255),"orta")
for i,t in enumerate(("FPS: 59","MS: 8","T: 23:44")):
    yaz(t,2,180+i*22,22,(255,255,255,255),"sol",2)
spr("btn_m",459,3); spr("btn_p",557,3); spr("btn_c",459,96)
# ---------------- gorev ----------------
spr("gorev_parsomen",2,272)
yaz("(15)",29,390,24,(230,230,230,255),"orta")
for i,(t,c) in enumerate([("Hunt :KOBOLD",(224,230,176,255)),("KOBOLD",(255,229,229,255)),
                          ("Hunt :BUGBE...",(224,230,176,255)),("BUGBEAR",(255,229,229,255))]):
    yaz(t,78,293+i*39,28 if i%2 else 30,c,"sol",2)
for i in (0,1):
    yaz("(0/10)",258,332+i*78,24,(56,230,0,255),"sol",2)
# ---------------- sag ust ----------------
spr("pim_ust",1908,0); spr("pim_alt",1908,74)
spr("sagust_dugmeler",1942,0)
spr("cubuk_timeleft_yazisiz",1942,74)
yaz("Time Left : 540 Minute(s)",2104,86,21,(255,255,255,255),"orta",1)
spr("panel_diez_yazisiz",1942,99)
yaz("Diez - 1",2104,120,25,(183,254,148,255),"orta",1)
spr("panel_cr_yazisiz",1942,144)
yaz("CR : 00:15:35",2104,167,25,(234,255,136,255),"orta",1)
spr("panel_aktif_etkinlik_yazisiz",1944,195)
yaz("Active Events",2105,216,25,(255,255,255,255),"orta",1)
spr("panel_kanal_yazisiz",1946,244)
yaz("Channel 1",2106,268,25,(254,254,254,255),"orta",1)
# ---------------- kamera ----------------
for ad,cx,cy in (("kam_kamera",1981,346),("kam_asagi",2069,348),("kam_yukari",2160,346),
                 ("kam_dondur",2068,435),("kam_goz",2161,436)):
    spr(ad,cx-44,cy-44)
# ---------------- beceri carki ----------------
for ad,cx,cy in (("bec_kendine",1875,859),("bec_bos_1",1745,974),("bec_ates",1909,1005),
                 ("bec_kosu",2066,1009),("bec_buz",1634,1115),("bec_alev",1788,1124),
                 ("bec_bos_2",1631,1274),("bec_bos_3",1788,1277)):
    spr(ad,cx-67,cy-67)
spr("merkez_saldiri",1976-109,1180-109)
spr("hedef_yakin",2155-62,1110-62); spr("hedef_uzak",2139-62,1256-62)
spr("ok_sol",2004-50,828-50); spr("ok_sag",2141-50,828-50)
yaz("1",2072,828,30,(255,255,255,255),"orta",2)
# ---------------- sohbet ----------------
kutu(7,922,806,56,(140,126,112),0.84)
spr("bildirim_kelebek",6,922)
yaz("Acele Edin, %10 Bonus Cash Kampanyası Başladı! Üstelik 5.000 ve",58,936,21,(255,255,255,255),"sol",1)
yaz("üzeri Cash satın alan ilk 1.000 oyuncuya ekstra 500 Cash hediye!…",58,964,21,(255,255,255,255),"sol",1)
spr("bildirim_baglanti",722,928); spr("bildirim_kapat",766,924)
SEK=[("ALL CHAT",3,153,"sekme_secili_yazisiz"),("SHOUT",164,151,"sekme_normal_yazisiz"),
     ("PARTY",321,152,"sekme_normal_yazisiz"),("CLAN",478,152,"sekme_normal_yazisiz"),
     ("NOTICES",635,177,"sekme_notices_yazisiz")]
for t,x,w,s in SEK:
    spr(s,x,978); yaz(t,x+w//2,1001,18,(247,247,247,255),"orta",1)
kutu(7,1028,804,290,(0,0,0),0.46)
kutu(813,1028,554,290,(0,0,0),0.46)
spr("tutamac",760,1036); spr("tutamac",1322,1036)
SOL=[("_BreeZeQueeN_ has obtained Wrath of Erenion -",(242,214,110,255)),
     ("> Green Treasure Chest",(255,255,255,255)),
     ("RelaxPikachU59 : 6 EAGLEEEE SELLLLLLLL",(255,255,255,255)),
     ("RelaxPikachU59 : 6 EAGLEEEE SELLLLLLLL",(255,255,255,255)),
     ("ACİLLLL",(255,255,255,255))]
for i,(t,c) in enumerate(SOL): yaz(t,36,1083+i*49,31,c,"sol",2)
SAG=[("5 SP Used",(230,40,40,255)),("5 SP Recovered",(130,140,250,255)),
     ("Using - Rush",(240,200,40,255)),("5 SP Used",(230,40,40,255)),
     ("5 SP Recovered",(130,140,250,255))]
for i,(t,c) in enumerate(SAG): yaz(t,845,1083+i*47,31,c,"sol",2)
kutu(7,1325,770,54,(0,0,0),0.40)
yaz("Enter text...",30,1352,24,(195,195,195,255),"sol",1)
spr("giris_ok",778,1333); spr("giris_beyaz_kutu",818,1329)
spr("panel_information_yazisiz",868,1331)
yaz("Information",982,1350,24,(224,201,200,255),"orta",1)
# ---------------- alt bar ----------------
spr("alt_bar_tam",0,1407)
tuval.convert("RGB").save("hud_kurulum.png")
print("hud_kurulum.png yazildi")

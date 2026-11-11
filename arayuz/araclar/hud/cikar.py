#!/usr/bin/env python3
"""HUD sprite'larini orijinal ekran goruntulerinden keser."""
import os, json, numpy as np
from PIL import Image
P="/home/user/Koray/arayuz/referans_gorseller/hud_ekranlar/hud_%02d.png"
OUT="/home/user/Koray/arayuz/kaynak/hud/sprites"
os.makedirs(OUT,exist_ok=True)
IM={k:Image.open(P%k).convert("RGB") for k in (1,2,3,4)}

def kes(ad,x,y,w,h,kare=1):
    im=IM[kare].crop((x,y,x+w,y+h)); im.save(os.path.join(OUT,ad+".png")); return (ad,x,y,w,h)

def daire(ad,cx,cy,d,kare=1,yumusat=2.0):
    """Dairesel buton: disi saydam alfa maskesi ile kesilir."""
    r=d/2.0; x0,y0=int(round(cx-r)),int(round(cy-r)); n=int(round(d))
    im=IM[kare].crop((x0,y0,x0+n,y0+n)).convert("RGBA")
    a=np.asarray(im).astype(float)
    yy,xx=np.mgrid[0:n,0:n]; dist=np.sqrt((xx-(n-1)/2)**2+(yy-(n-1)/2)**2)
    al=np.clip((r-dist)/yumusat+0.5,0,1)*255
    a[:,:,3]=al
    Image.fromarray(a.astype(np.uint8),"RGBA").save(os.path.join(OUT,ad+".png"))
    return (ad,x0,y0,n,n)

kayit=[]
A=kayit.append
# --- sol ust ---
A(kes("durum_plaka",0,0,452,240))
A(kes("hp_dolgu",69,13,353,36))
A(kes("mp_dolgu",69,56,353,34))
A(kes("btn_m",459,3,82,82)); A(kes("btn_p",557,3,82,82)); A(kes("btn_c",459,96,82,82))
A(kes("gorev_parsomen",2,272,54,110))
# --- sag ust ---
A(kes("sagust_dugmeler",1942,0,324,74))
A(kes("cubuk_timeleft",1942,74,324,25))
A(kes("panel_diez",1942,99,324,45))
A(kes("panel_cr",1942,144,324,46))
A(kes("panel_aktif_etkinlik",1944,195,322,43))
A(kes("panel_kanal",1946,244,320,48))
A(kes("pim_ust",1908,0,32,68)); A(kes("pim_alt",1908,74,32,69))
# --- kamera dugmeleri (cap 88) ---
for ad,cx,cy in (("kam_kamera",1981,346),("kam_asagi",2069,348),("kam_yukari",2160,346),
                 ("kam_dondur",2068,435),("kam_goz",2161,436)):
    A(daire(ad,cx,cy,88))
# --- beceri carki ---
for ad,cx,cy in (("bec_kendine",1875,859),("bec_bos_1",1745,974),("bec_ates",1909,1005),
                 ("bec_kosu",2066,1009),("bec_buz",1634,1115),("bec_alev",1788,1124),
                 ("bec_bos_2",1631,1274),("bec_bos_3",1788,1277)):
    A(daire(ad,cx,cy,134))
A(daire("ok_sol",2004,828,100)); A(daire("ok_sag",2141,828,100))
A(daire("merkez_saldiri",1976,1180,218))
A(daire("hedef_yakin",2155,1110,124)); A(daire("hedef_uzak",2139,1256,124))
# --- sohbet ---
A(kes("sekme_secili",3,978,153,48))
A(kes("sekme_normal",164,978,151,48))
A(kes("sekme_notices",635,978,177,48))
A(kes("bildirim_kelebek",6,922,46,56))
A(kes("bildirim_baglanti",722,928,42,44))
A(kes("bildirim_kapat",766,924,46,50))
A(kes("giris_ok",778,1333,35,37))
A(kes("giris_beyaz_kutu",818,1329,47,44))
A(kes("panel_information",868,1331,265,38))
A(kes("tutamac",760,1036,38,30))     # yeniden boyutlandirma tutamagi
# --- alt bar ---
A(kes("alt_bar_tam",0,1407,2266,81))
A(kes("alt_bar_buton",750,1417,98,52))
json.dump([{"ad":a,"x":x,"y":y,"w":w,"h":h} for a,x,y,w,h in kayit],
          open(os.path.join(OUT,"..","sprite_kutulari.json"),"w"),indent=1,ensure_ascii=False)
print("%d sprite yazildi"%len(kayit))

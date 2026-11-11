#!/usr/bin/env python3
"""OLYMPOS-KO oyun ici pencereler: sprite cikarimi (2712x1220 referans kareler).

Yontem
  * Yari saydam siyah zeminli pencereler (esya penceresi, Drop List, ipucu):
    ayni sahnenin pencereli/penceresiz kareleri var.  O = K (+) siyah(a) (+) B.
    Zemin katkisi cikarilir  R = O - (1-a)*B ;  R~0 -> saf zemin (krom alfasi 0).
    Krom siyaha karsi cozulur: alfa = clip((max(R)-t0)/(T-t0)), RGB = R/alfa.
    Boylece krom, Unity'deki siyah zemin Image'inin ustunde orijinali birebir verir.
  * Dunyanin ustune dogrudan cizilen opak ogeler (Remove/Close, ok): once/sonra
    farki alfa maskesi olur, renk dogrudan orijinalden.
  * Save Skill Slot Stat: tek fotograf var; zemin ~siyah oldugundan parlaklikla ayrilir.
"""
import os, json, numpy as np
from PIL import Image
BURADA=os.path.dirname(os.path.abspath(__file__))
REF=os.path.join(BURADA,"..","..","referans_gorseller","oyun_ici")
OUT=os.path.join(BURADA,"..","..","kaynak","oyun_ici","sprites")
os.makedirs(OUT,exist_ok=True)
_c={}
def Y(ad):
    if ad not in _c: _c[ad]=np.asarray(Image.open(os.path.join(REF,ad+".jpg")).convert("RGB")).astype(float)
    return _c[ad]
KAYIT={}
def yaz(ad,rgba,**bilgi):
    rgba=np.clip(rgba,0,255).astype(np.uint8)
    Image.fromarray(rgba,"RGBA").save(os.path.join(OUT,ad+".png"))
    KAYIT[ad]=dict(w=int(rgba.shape[1]),h=int(rgba.shape[0]),**bilgi)
def krom(once,sonra,kutu,a,T=60.0,t0=5.0):
    x0,y0,x1,y1=kutu
    R=np.clip(Y(sonra)[y0:y1,x0:x1]-(1-a)*Y(once)[y0:y1,x0:x1],0,255)
    al=np.clip((R.max(2)-t0)/(T-t0),0,1)
    rgb=np.where(al[...,None]>0,np.clip(R/np.maximum(al[...,None],1e-3),0,255),0)
    return np.dstack([rgb,al*255])
def degisen(once,sonra,kutu,e0=8.0,e1=30.0):
    x0,y0,x1,y1=kutu
    O=Y(sonra)[y0:y1,x0:x1]; B=Y(once)[y0:y1,x0:x1]
    al=np.clip((np.abs(O-B).max(2)-e0)/(e1-e0),0,1)
    return np.dstack([O,al*255])
def opak(kare,kutu):
    x0,y0,x1,y1=kutu; O=Y(kare)[y0:y1,x0:x1]
    return np.dstack([O,np.full(O.shape[:2],255.0)])
def daire(kare,cx,cy,d,yumusat=1.5):
    r=d/2.0; n=int(round(d)); x0=int(round(cx-r)); y0=int(round(cy-r))
    O=Y(kare)[y0:y0+n,x0:x0+n]
    yy,xx=np.mgrid[0:n,0:n]; dist=np.sqrt((xx-(n-1)/2.0)**2+(yy-(n-1)/2.0)**2)
    return np.dstack([O,np.clip((r-dist)/yumusat+0.5,0,1)*255]),(x0,y0)

# ====================== 1) ESYA EYLEM PENCERESI ======================
PX,PY,PW,PH=1360,740,663,313
K=krom("v1_once","v1_popup_hp",(PX,PY,PX+PW,PY+PH),0.92)
for ad,(x,y,w,h) in {"btn_use_self":(11,248,155,62),"btn_use_target":(173,248,155,62),
                     "btn_equip":(334,248,156,62),"btn_close_kirmizi":(496,248,155,62)}.items():
    yaz(ad,K[y:y+h,x:x+w],pencere="esya",x=x,y=y)
cer=K[2:105,2:105].copy(); cer[7:96,7:96,3]=0          # ic: ikon alani 89x89
yaz("ikon_cerceve",cer,pencere="esya",x=2,y=2,ic=[7,7,89,89])
for ad,kare,(ox,oy) in (("ikon_hp_scroll","v1_popup_hp",(1360,740)),("ikon_hiz_iksiri","v1_popup_hiz2",(1255,740)),
                        ("ikon_zirh_scroll","v1_popup_armor",(1150,741))):
    yaz(ad,opak(kare,(ox+9,oy+9,ox+98,oy+98)))

# ====================== 2) BUFF CUBUGU + REMOVE/CLOSE ======================
b=opak("v1_buff3",(2179,56,2243,120))                     # ortadaki ikon (hiz iksiri) cercevesi
c=b.copy(); c[3:61,3:61,3]=0
c[61:64,:,:3]=c[2::-1,:,:3]                               # alt kenar yazi altinda: ust kenarin aynasi
yaz("buff_cerceve",c,ic=[3,3,58,58])
yaz("menu_ok",degisen("v1_buff3","v1_remove",(2262,120,2292,138)),x=2262,y=120)
from scipy import ndimage
def dolu(a):
    """Fark maskesindeki delikleri doldurur (dugme govdesi opak)."""
    m=ndimage.binary_fill_holes(ndimage.binary_closing(a[:,:,3]>90,np.ones((5,5))))
    a=a.copy(); a[:,:,3]=np.where(m,255,a[:,:,3]); return a
yaz("btn_remove",dolu(degisen("v1_buff3","v1_remove",(2180,136,2374,202))),x=2180,y=136)
yaz("btn_menu_close",dolu(degisen("v1_buff3","v1_remove",(2180,206,2374,270))),x=2180,y=206)

# ====================== 3) HIZLI SLOT + HEDEF IPTAL ======================
h,(sx,sy)=daire("v2_hedef",2193,452,164)
yy,xx=np.mgrid[0:164,0:164]; dist=np.sqrt((xx-81.5)**2+(yy-81.5)**2)
ic=dist<70.0
h[:,:,3]=np.where(ic,0,h[:,:,3])                          # ic bosluk: ayri siyah disk (alfa olculdu)
h[:,:,3]=np.where((dist>=70)&(dist<73),h[:,:,3]*(dist-70)/3.0,h[:,:,3])
yaz("slot_halka",h,merkez=[2193,452],cap=164,ic_cap=144)
m=np.zeros((144,144,4)); yy,xx=np.mgrid[0:144,0:144]; dist=np.sqrt((xx-71.5)**2+(yy-71.5)**2)
m[:,:,:3]=255; m[:,:,3]=np.clip((72-dist)/1.5+0.5,0,1)*255
yaz("slot_maske",m)
x,(ox,oy)=daire("v2_hedef",2573,854,140)
yaz("btn_hedef_iptal",x,x=ox,y=oy)

# ====================== 4) HEDEF CUBUGU + SHOW DROPS ======================
x0,y0,x1,y1=1178,96,1582,137
O=Y("v2_hedef")[y0:y1,x0:x1]; ust=Y("v2_hedef")[y0-3:y0,x0:x1].mean(0); alt=Y("v2_hedef")[y1:y1+2,x0:x1].mean(0)
t=((np.arange(y1-y0)+0.5)/(y1-y0))[:,None,None]
Bt=ust[None]*(1-t)+alt[None]*t                             # gokyuzu duz: dikey ara degerleme
# gokyuzu/ufuk aydinlik (G>170), cubuk koyu kirmizi: alfa yesil kanaldan
al=np.clip((172.0-O[:,:,1])/45.0,0,1)
al[:2,:]=0; al[40:,:]=0; al[:,:5]=0; al[:,402:]=0
from scipy import ndimage as _nd
al=np.where(_nd.binary_fill_holes(al>0.5),1.0,al)          # parlak yansima seridi cubugun parcasi
cub=np.dstack([O,al*255])
# Lv yazisi dinamik: yesil pikselleri ayni satirin kirmizisiyla doldur
R_,G_,B_=cub[:,:,0],cub[:,:,1],cub[:,:,2]
yesil=(G_>R_+15)
yesil[:, :6]=False; yesil[:,70:]=False
for yy_ in range(cub.shape[0]):
    if yesil[yy_].any(): cub[yy_,6:70,:3]=np.median(cub[yy_,74:110,:3],axis=0)
yaz("hedef_cubuk",cub,x=x0,y=y0)
yaz("btn_show_drops",opak("v2_hedef",(1298,134,1450,188)),x=1298,y=134)

# ====================== 5) DROP LIST SEARCH ======================
DX,DY,DW,DH=176,82,698,1116
D=krom("v2_hedef","v2_drop_bos",(DX,DY,DX+DW,DY+DH),0.89)
dis=degisen("v2_hedef","v2_drop_bos",(DX,DY,DX+DW,DY+DH),10,36)
zemin=np.zeros((DH,DW),bool); zemin[8:1115,6:689]=True       # siyah zeminin kapladigi alan
D=np.where(zemin[...,None],D,dis)
def temizle(x,y,w,h): D[y:y+h,x:x+w,3]=0
# onay isareti (Monster kutusu) ayri sprite
tik=D[74:152,28:104].copy()
beyaz=(tik[:,:,:3].min(2)>150)
tik[:,:,3]=np.where(beyaz,tik[:,:,3],0)
from scipy import ndimage
tik[:,:,3]=ndimage.gaussian_filter(np.where(beyaz,255.0,0.0),0.6)
tik[:,:,:3]=255
yaz("onay_isareti",tik,x=28,y=74)
bos_kutu=D[160:224,32:96].copy()                             # Item Name'in bos kutusu
temizle(28,74,76,82); D[84:148,32:96]=bos_kutu               # Monster kutusu: isaretsiz
# yer tutucu yazi ayri sprite
yaz("drop_yer_tutucu",D[256:292,150:556].copy(),x=150,y=256); temizle(150,256,406,36)
# sayfa yazilari dinamik
temizle(318,648,66,42); temizle(322,1052,62,44)
# ilk uc slotun icerigi -> bos slot
dolu_cer=D[703:806,64:167].copy(); dolu_cer[7:96,7:96,3]=0      # esyali slotun acik renkli cercevesi
yaz("drop_slot_dolu",dolu_cer,ic=[7,7,89,89])
bos=D[703:806,409:512].copy()
grup=D[703+7:703+96,64+7:64+96].copy(); ornek=D[703+7:703+96,294+7:294+96].copy()
for sx_ in (64,179,294): D[703:806,sx_:sx_+103]=bos
yaz("drop_krom",D,ekran=[DX,DY])
def ikon_yaz(ad,a):
    a=a.copy(); a[:,:,3]=255
    a[68:89,26:89,:3]=0            # oran etiketi kutusu: Unity'de Text + siyah zemin ayni yere gelir
    yaz(ad,a)
ikon_yaz("drop_grup",opak("v2_drop_bos",(DX+64+7,DY+703+7,DX+64+96,DY+703+96)))
ikon_yaz("drop_ornek_0",opak("v2_drop_bos",(DX+294+7,DY+703+7,DX+294+96,DY+703+96)))
# 2. sayfadaki ornek ikonlar (grup acildiginda)
# ipucundaki ikon etiketsiz (temiz): ayni esya icin onu kullan
yaz("drop_ornek_temiz",opak("v2_drop_ipucu",(591+12,499+12,591+101,499+101)))
for i,(c,r) in enumerate(((0,0),(1,0),(2,0),(3,0),(4,0),(0,2),(1,2),(3,2),(4,2))):
    sx_=DX+64+115*c+7; sy_=DY+703+111*r+7
    ikon_yaz("drop_ornek_%d"%(i+1),opak("v2_drop_izgara",(sx_,sy_,sx_+89,sy_+89)))

# ipucu (drop esyasi): Close dugmesi + ikon
TX,TY,TW,TH=591,499,484,621
T_=krom("v2_drop_izgara","v2_drop_ipucu",(TX,TY,TX+TW,TY+TH),0.93)
Image.fromarray(np.clip(T_,0,255).astype(np.uint8),"RGBA").save(os.path.join(OUT,"..","_ipucu_ham.png"))

# ====================== 6) SAVE SKILL SLOT STAT ======================
SX,SY,SW,SH=1196,110,526,1068
F=Y("foto_saveslot")[SY:SY+SH,SX:SX+SW]
R=np.clip(F-7.0,0,255); al=np.clip((R.max(2)-12)/(60-12.0),0,1)
Sk=np.dstack([np.where(al[...,None]>0,np.clip(R/np.maximum(al[...,None],1e-3),0,255),0),al*255])
# pencere disi (dunya) temizligi: govde cercevesi x 13..508, alt cerceve y 1044..1052; baslik cubugu daha genis
Sk[70:,:12,3]=0; Sk[70:,510:,3]=0; Sk[1054:,:,3]=0; Sk[:10,:455,3]=0
ROW0,PITCH=85,245
sablon=Sk[ROW0+2*PITCH+2:ROW0+2*PITCH+240,60:505].copy()   # 3. satir: arkadan sizan hayalet yok
for k in (1,3): Sk[ROW0+k*PITCH+2:ROW0+k*PITCH+240,60:505]=sablon
for k in range(4): Sk[ROW0+k*PITCH+82:ROW0+k*PITCH+167,18:505,3]=0   # durum yazisi dinamik
yaz("saveslot_krom",Sk[:1056],ekran=[SX,SY],satir0=ROW0,adim=PITCH)
json.dump(KAYIT,open(os.path.join(OUT,"..","sprite_bilgisi.json"),"w"),indent=1,ensure_ascii=False)
print("%d sprite"%len(KAYIT))

#!/usr/bin/env python3
"""Adet giris penceresi + sure cubuklu satin alma onayi (tablet goruntuleri, 2266x1488, kayipsiz PNG).
Tablet duzeni telefon duzeninin 1.0405 kati: sprite'lar tablet cozunurlugunde saklanir, kurucu 1/1.0405 ile yerlestirir."""
import os, json, numpy as np
from PIL import Image
from scipy import ndimage
B=os.path.dirname(os.path.abspath(__file__)); REF=os.path.join(B,"..","..","referans_gorseller","merchant"); OUT=os.path.join(B,"..","..","kaynak","merchant","sprites")
OLCEK=1.0405
def Y(n): return np.asarray(Image.open(os.path.join(REF,n+".png")).convert("RGB")).astype(float)
def mat(R,t0=8.0,T=60.0):
    R=np.clip(R,0,255); al=np.clip((R.max(2)-t0)/(T-t0),0,1)
    return np.dstack([np.where(al[...,None]>0,np.clip(R/np.maximum(al[...,None],1e-3),0,255),0),al*255])
KAYIT={}
def yaz(ad,a,**b):
    Image.fromarray(np.clip(a,0,255).astype(np.uint8),"RGBA").save(os.path.join(OUT,ad+".png")); KAYIT[ad]=dict(w=int(a.shape[1]),h=int(a.shape[0]),**b)
def satir_doldur(a,x0,y0,x1,y1,serit=10):
    n=x1-x0; t=((np.arange(n)+0.5)/n)[:,None]
    for y in range(y0,y1):
        L=np.median(a[y,x0-serit:x0],axis=0); R=np.median(a[y,x1:x1+serit],axis=0); a[y,x0:x1]=L*(1-t)+R*t

# ===================== ADET PENCERESI  (cerceve 1170..1909 x 325..867) =====================
A=Y("t_adet"); AX,AY,AW,AH=1170,325,740,543
k=A[AY:AY+AH,AX:AX+AW].copy()
satir_doldur(k,205,372,305,420)                       # "20" silinir (alan ici duz koyu gri)
k=mat(k,t0=14.0,T=60.0)                               # t0=14: arkadan sizan yuva izleri (<=10) zemine gider
yaz("adet_krom",k,tablet=[AX,AY],olcek=OLCEK)

# ===================== SATIN ALMA ONAYI  (cerceve 864..1440 x 416..945) =====================
S=Y("t_satinal"); SX,SY,SW,SH=864,416,577,530
ham=S[SY:SY+SH,SX:SX+SW].copy()
# dugmeler ayri: Cancel zemini (yazisi silinmis) her iki dugmede kullanilir; OK'nin soluk hali = ayni zemin x0.56 (olculdu)
bx,by,bw,bh=1196-SX,853-SY,156,64
zemin=ham[by:by+bh,bx:bx+bw].copy(); satir_doldur(zemin,16,14,143,50,serit=7)
yaz("btn_onay_zemin",mat(zemin,t0=4.0,T=30.0),tablet=[1196,853])
def yazi(kutu,renk=(224,201,201),alt=95.0,ust=205.0):
    x0,y0,x1,y1=kutu; c=S[y0:y1,x0:x1]; al=np.clip((c.max(2)-alt)/(ust-alt),0,1)
    o=np.zeros(c.shape[:2]+(4,)); o[:,:,:3]=renk; o[:,:,3]=al*255; return o
yaz("yazi_ok",yazi((1026,872,1092,900)),tablet=[1026,872])
yaz("yazi_cancel",yazi((1210,872,1340,900),alt=125.0),tablet=[1210,872])
# ikon cercevesi
ix,iy,iw,ih=1102-SX,439-SY,98,96
c=mat(ham[iy:iy+ih,ix:ix+iw].copy(),t0=6.0,T=50.0); c[7:-7,7:-7,3]=0
yaz("onay_ikon_cerceve",c,goreli=[ix,iy],ic=[7,7,iw-14,ih-14])
# sure cubugu: oluk (dolgu ve sayi silinmis) + dolgu
ox,oy,ow,oh=922-SX,560-SY,460,24
oluk=ham[oy:oy+oh,ox:ox+ow].copy()
bos=oluk[:,340:380].copy()                             # bos kismin isaretsiz temiz parcasi
for x in range(4,300): oluk[:,x]=bos[:,(x-4)%40]
oluk[:,:4]=oluk[:,::-1][:,:4]                          # sol uc = sag ucun aynasi
yaz("sure_oluk",mat(oluk,t0=4.0,T=40.0),goreli=[ox,oy])
dol=S[563:580,930:1130].copy()
yaz("sure_dolgu",np.dstack([dol,np.full(dol.shape[:2],255.0)]),goreli=[924-SX,563-SY],ic_genislik=455)
# govde: dinamik ogeler cikarilir
k=mat(ham,t0=6.0,T=50.0)
k[iy-2:iy+ih+2,ix-2:ix+iw+2,3]=0                       # ikon + cerceve (ayri)
k[oy-2:oy+oh+2,ox-4:ox+ow+4,3]=0                       # sure cubugu (ayri)
k[280:386,20:557,3]=0                                  # "[Price: ...] Will you buy this item? / Please double check the price" (Text)
k[by-4:by+bh+4,100:500,3]=0                            # dugmeler (ayri)
yaz("onay_krom",k,tablet=[SX,SY],olcek=OLCEK)
p=os.path.join(OUT,"..","sprite_bilgisi.json"); j=json.load(open(p)); j.update(KAYIT); json.dump(j,open(p,"w"),indent=1,ensure_ascii=False)
for a,v in KAYIT.items(): print("%-18s %dx%d"%(a,v["w"],v["h"]))

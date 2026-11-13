#!/usr/bin/env python3
"""Alici gorunumunun benzetimi: baska oyuncunun tezgah cubugu (satici adi + mor cerceveli yuvalar) ve dolu Merchant penceresi.
Tek kare oldugu icin orijinal ogenin yeri once ayni karedeki cim parcasiyla kapatilir, sonra yeniden cizilir."""
import kur
from kur import *
kur.FONT["DB"]="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def yuva_e(t,x,y,w,h,e,dolu,mor,ic,mor_ic,punto,etiket_sag,etiket_ust):
    """e=(ikon, adet, yukseltme, mor_mu). ic / mor_ic: ikon kutusu (x,y,w,h) yuva icinde."""
    if e is None: return
    k=mor_ic if e[3] else ic
    t.spr(e[0],x+k[0],y+k[1],k[2],k[3]); t.spr(mor if e[3] else dolu,x,y)
    if e[2]:                                       # etiket orijinalde Roboto Bold'dan biraz kalin: 1 px ayni renkte dis hat
        for dx in (0,1): t.yaz("+%d"%e[2],x+etiket_sag+dx,y+etiket_ust,"RB",punto,(202,137,226,255),"sag")
    if e[1]>1: t.yaz(str(e[1]),x+w-11,y+h-8-int(h*0.27*0.80),"RB",int(round(h*0.27)),PEMBE,"sag",1)
def cubuk(t,x0,y0,ad,liste):
    for i in range(4): t.kutu(x0+35+86*i,y0+17,70,72,(0,0,0),0.87)
    t.spr("tezgah_krom",x0,y0)
    for i,e in enumerate(liste[:4]): yuva_e(t,x0+27+86*i,y0+9,86,88,e,"yuva_dolu_tezgah","yuva_mor_tezgah",(8,8,70,72),(16,12,62,66),31,78,13)
    t.yaz(ad,x0+197.5,y0-35,"DB",30,BEYAZ,"orta",2)
def pencere(t,ad,tezgah,altin,envanter):
    t.kutu(952,172,770,905,(0,0,0),0.89); t.kutu(958,122,762,48,(0,0,0),0.89); t.spr("mpencere_krom",*E("mpencere_krom"))
    t.yaz(ad+" Merchant",1335.5,131,"SR",33,ALTIN,"orta"); t.yaz(altin,1618,538,"RB",36,BEYAZ,"sag")
    for i,e in enumerate(tezgah): yuva_e(t,int(round(PU[0]+PU[1]*(i%6))),int(round(PU[2]+PU[3]*(i//6))),117,114,e,"yuva_dolu_mp_ust","yuva_mor_mp_ust",(8,8,101,98),(12,12,93,90),25,110,11)
    for i,e in enumerate(envanter): yuva_e(t,int(round(PE[0]+PE[1]*(i%7))),int(round(PE[2]+PE[3]*(i//7))),104,102,e,"yuva_dolu_mp_env","yuva_dolu_mp_env",(8,8,88,86),(8,8,88,86),28,94,11)
def cimle(im,kutu,kaynak=(560,430,300,180)):
    p=im.crop((kaynak[0],kaynak[1],kaynak[0]+kaynak[2],kaynak[1]+kaynak[3])); x0,y0,x1,y1=kutu
    for y in range(y0,y1,kaynak[3]):
        for x in range(x0,x1,kaynak[2]): im.paste(p.crop((0,0,min(kaynak[2],x1-x),min(kaynak[3],y1-y))),(x,y))
YAY=("ikon_yay",1,1,True); BALTA=("ikon_balta",1,1,True)
if __name__=="__main__":
    o=kare("a_cubuk"); y=o.copy(); cimle(y,(935,190,1385,405)); t=Tuval(y); cubuk(t,955,241,"Itccc",[YAY]*4)
    k=(900,170,1420,430); a=yan_yana("merchant_15_alici_cubuk",o.crop(k),y.crop(k),1.6,"Başka oyuncunun tezgâhı: satıcı adı + mor çerçeveli yuvalar"); print(a.size)
    o=kare("a_pencere"); y=o.copy(); cimle(y,(930,105,1745,1095)); t=Tuval(y)
    env=[None]*5+[("ikon_parsomen_sureli_3",1,0,False)]
    pencere(t,"Itccc",[YAY]*6+[BALTA]*4+[YAY]*2,"9,322",env)
    k=(900,90,1780,1110); b=yan_yana("merchant_16_alici_pencere",o.crop(k),y.crop(k),0.8,"Itccc Merchant — alıcının gördüğü pencere"); print(b.size)
    c=Image.new("RGB",(max(a.width,b.width),a.height+b.height+10),(24,24,28)); c.paste(a,(0,0)); c.paste(b,(0,a.height+10)); c.save(os.path.join(ONZ,"merchant_alici_onizleme.png")); print(c.size)

#!/usr/bin/env python3
"""Merchant / Slave Merchant / esya bilgi penceresi sprite cikarimi (2712x1220 kareler).
Yontem oyun_ici/cikar.py ile ayni: krom siyaha karsi cozulur (ayri siyah zemin Image'inin ustunde
orijinali verir); pencere disi, cim siniflandirmasi ya da once/sonra farkiyla saydamlastirilir;
dolu yuvalar ayni pencerenin bos yuva sablonuyla degistirilir; degisen yazilar silinir."""
import json
from scipy import ndimage
from ortak import *; from maske import *
os.makedirs(OUT,exist_ok=True)
KAYIT={}
def yaz(ad,rgba,**b):
    kaydet(ad,rgba); KAYIT[ad]=dict(w=int(rgba.shape[1]),h=int(rgba.shape[0]),**b)
def sikistir(m,kutu,oran=0.2):
    """maskenin govdesini (satir/sutun kaplama > oran) bulur; (x,y,w,h) mutlak"""
    col=(m>0.5).mean(0); row=(m>0.5).mean(1)
    xs=np.where(col>oran)[0]; ys=np.where(row>oran)[0]
    return kutu[0]+xs.min(),kutu[1]+ys.min(),xs.max()-xs.min()+1,ys.max()-ys.min()+1
def pencere(kare,kaba,maske,once=None,a=0.95,t0=8.0,pay=(0,0,14,14)):
    """kaba kutuda maske -> govde kutusu (+pay: sol,ust,sag,alt; kose susleri icin) -> RGBA, kutu"""
    x,y,w,h=sikistir(maske,kaba); x-=pay[0]; y-=pay[1]; w+=pay[0]+pay[2]; h+=pay[1]+pay[3]
    k=krom(kare,(x,y,w,h),once,a,t0=t0)
    mx=x-kaba[0]; my=y-kaba[1]; M=np.zeros((h,w))
    sub=maske[max(my,0):my+h,max(mx,0):mx+w]; M[max(-my,0):max(-my,0)+sub.shape[0],max(-mx,0):max(-mx,0)+sub.shape[1]]=sub
    k[:,:,3]*=M
    return k,(x,y,w,h)
def yuva_doldur(k,kutu,kare,sablon,konumlar,once=None,a=0.95,t0=8.0):
    """sablon=(x,y,w,h) mutlak bos yuva; konumlar: mutlak (x,y) listesi"""
    T=krom(kare,sablon,once,a,t0=t0)
    for (X,Yy) in konumlar:
        lx,ly=int(round(X))-kutu[0],int(round(Yy))-kutu[1]; k[ly:ly+sablon[3],lx:lx+sablon[2]]=T
def ikonlar(on,kare,x0,px,y0,py,liste,ic=(8,8,87,85)):
    for (c,r,ad) in liste:
        X=int(round(x0+px*c))+ic[0]; Yy=int(round(y0+py*r))+ic[1]
        yaz(on+ad,opak(kare,(X,Yy,ic[2],ic[3])))

# ============================================================ 1) KOMUT MENUSU
KM=(2290,105,400,1020)
m=fark_maskesi("m_once","m_menu",KM,esik=12)
m[:, :2322-KM[0]]=0; m[:,2636-KM[0]:]=0
yy,xx=np.mgrid[0:KM[3],0:KM[2]]; daire=np.hypot(xx-(2489-KM[0]),yy-(153-KM[1]))<41
m[:160-KM[1]]=np.where(daire[:160-KM[1]],1.0,0.0)            # cercevenin ustunde yalniz kapatma dugmesi
m=np.maximum(m,daire*1.0)
k,kb=pencere("m_menu",KM,m,once="m_once",a=0.94,pay=(0,48,0,0)); yaz("menu_krom",k,ekran=list(kb),dugme=[2344,211,276,64,116])

# ============================================================ 2) CREATE A MERCHANT
KC=(1540,26,830,900); m=cim_disi("m_create",KC)
m[:, :1573-KC[0]]=0; m[:,2350-KC[0]:]=0
m[140-KC[1]:, :1584-KC[0]]=0                                   # govdenin solundaki skill bar artiklari
k,kb=pencere("m_create",KC,m,pay=(11,0,0,0))
CU=(1637.0,111.0,163.0,110.0); CE=(1613.8,99.67,414.0,100.9)
yuva_doldur(k,kb,"m_create",(1859,163,102,100),[(CU[0]+CU[1]*c,CU[2]+CU[3]*r) for r in range(2) for c in range(6)])
yuva_doldur(k,kb,"m_create",(2112,717,103,101),[(CE[0]+CE[1]*c,CE[2]+CE[3]*r) for r in range(4) for c in range(7)])
yaz("create_krom",k,ekran=list(kb),ust=CU,env=CE)
# deneme ikonlari (envanter): sayac rakamlari ikonla birlikte geldi
# yalniz bindirmesiz (sayac / +N etiketi olmayan) ikonlar; sayac ve "+N" oyunda yuvanin ustune ayri cizilir
ENV=[(5,0,"eldiven"),(6,0,"yuzuk"),(0,1,"asa"),(2,1,"zirh"),(3,1,"bilezik"),(4,1,"kupe"),(6,1,"pantolon"),(1,2,"sopa")]
ikonlar("ikon_","m_create",CE[0],CE[1],CE[2],CE[3],ENV)

# ============================================================ 3) FIYAT DIYALOGU
KF=(1605,208,711,522); k=krom("m_fiyat0",KF)
# "0" yer tutucusu dinamik: ayni satirin sag komsusuyla doldur
k[352:402,200:255]=k[352:402,262:317]
yaz("fiyat_krom",k,ekran=list(KF))

# ============================================================ 4) TEZGAH CUBUGU
KT=(1130,500,460,230); m=cim_disi("m_tezgah",KT)
k,kb=pencere("m_tezgah",KT,m,pay=(4,0,4,4))
mavi=(k[:14,:,2]>k[:14,:,0]+30); k[:14,:,3]=np.where(mavi,0,k[:14,:,3])   # ustteki oyuncu adi artigi
yuva_doldur(k,kb,"m_tezgah",(1272,560,86,88),[(1186,560)])
yaz("tezgah_krom",k,ekran=list(kb),yuva=[1186,86,560])

# ============================================================ 5) MERCHANT PENCERESI
KP=(920,90,830,1010); m=cim_disi("m_pencere2",KP)
m[:, :945-KP[0]]=0; m[:,1745-KP[0]:]=0
k,kb=pencere("m_pencere2",KP,m,once="m_tezgah",a=0.89,pay=(0,0,0,0))
PU=(974.7,120.31,228.8,121.17); PE=(967.8,103.64,588.9,104.4)
# ust izgara bolgesi: arka plan artiklari (kayan skill bar) -> zemin temiz
k[220-kb[1]:470-kb[1],960-kb[0]:1710-kb[0],3]=0
k[582-kb[1]:1012-kb[1],960-kb[0]:1705-kb[0],3]=0
yuva_doldur(k,kb,"m_pencere2",(1095,229,117,114),[(PU[0]+PU[1]*c,PU[2]+PU[3]*r) for r in range(2) for c in range(6)],"m_tezgah",0.89)
yuva_doldur(k,kb,"m_pencere2",(1486,798,104,102),[(PE[0]+PE[1]*c,PE[2]+PE[3]*r) for r in range(4) for c in range(7)],"m_tezgah",0.89)
# altin miktari dinamik; dokunma izi (gri daire) baska kareden
k[525-kb[1]:575-kb[1],1470-kb[0]:1650-kb[0],3]=0
p=krom("m_pencere_ipucu",(1530,1010,110,75),"m_tezgah",0.89); k[1010-kb[1]:1085-kb[1],1530-kb[0]:1640-kb[0]]=p
# baslik yazisi dinamik ("<ad> Merchant"): cubugun sol temiz parcasinin aynasiyla doldur
by0,by1=120-kb[1],170-kb[1]; sx0,sx1=1000-kb[0],1100-kb[0]; tx0,tx1=1100-kb[0],1580-kb[0]
parca=k[by0:by1,sx0:sx1].copy(); n=sx1-sx0; x=tx0; ters=True
while x<tx1:
    w=min(n,tx1-x); k[by0:by1,x:x+w]=(parca[:,::-1] if ters else parca)[:,:w]; x+=w; ters=not ters
yaz("mpencere_krom",k,ekran=list(kb),ust=PU,env=PE)

# ============================================================ 6) SLAVE MERCHANT
KS=(1440,70,1010,1060); m=fark_maskesi("s_sonra","s_pencere2",KS,esik=10)
k,kb=pencere("s_pencere2",KS,m,once="s_sonra",a=0.95,t0=14.0,pay=(0,0,0,0))
SATIR=(1460,294,946,96)             # liste satiri (cerceve + icerik)
# baslik alani: arkadan sizan gok/yazi artiklari -> yalniz bilinen ogeler ve parlak pikseller kalir
ust=k[:285-kb[1]]; parlak=ust[:,:,:3].max(2)*ust[:,:,3]/255>70
kutular=[(1478,256,1682,318),(1792,256,2050,318),(2193,256,2414,318),(2228,120,2300,194),(2310,118,2392,200)]
tut=np.zeros(parlak.shape,bool)
for (a0,b0,a1,b1) in kutular: tut[b0-kb[1]:b1-kb[1],a0-kb[0]:a1-kb[0]]=True
tut[:12]=True; tut[:,:12]=True; tut[:,-22:]=True                 # dis cerceve
ust[:,:,3]=np.where(tut|ndimage.binary_dilation(parlak,np.ones((3,3))),ust[:,:,3],0)
lx,ly=SATIR[0]-kb[0],SATIR[1]-kb[1]
satir=k[ly:ly+SATIR[3],lx:lx+SATIR[2]].copy()
k[ly:ly+SATIR[3],lx:lx+SATIR[2],3]=0                      # satir ayri sprite
k[ly+SATIR[3]:1030-kb[1],lx:lx+SATIR[2],3]=0              # liste alani: arkadan sizan yazilar
yaz("slave_krom",k,ekran=list(kb),satir=list(SATIR))
# satir cercevesi: icerik (ikon, sayac, durum yazisi) silinir -> yalniz cizgiler
ic=satir[9:88,4:936]; ic[:,:,3]=0
yaz("slave_satir",satir)
yaz("ikon_short_bow_kucuk",opak("s_pencere2",(1517,309,70,68)))
c=krom("s_pencere2",(1512,304,80,78),"s_sonra",0.95,t0=14.0); c[6:72,6:74,3]=0
yaz("slave_ikon_cerceve",c)

# ============================================================ dolu yuva cerceveleri (esyali yuvanin kenari daha acik)
def dolu(ad,kare,kutu,once=None,a=0.95,pay=8):
    c=krom(kare,kutu,once,a); c[pay:-pay,pay:-pay,3]=0; yaz(ad,c)
dolu("yuva_dolu_create_ust","m_create_dolu",(1637,163,102,100))
dolu("yuva_dolu_create_env","m_create",(int(round(CE[0]+CE[1]*5)),414,103,101))
dolu("yuva_dolu_mp_ust","m_pencere2",(975,229,117,114),"m_tezgah",0.89)
dolu("yuva_dolu_mp_env","m_pencere2",(int(round(PE[0]+PE[1]*5)),589,104,102),"m_tezgah",0.89)
dolu("yuva_dolu_tezgah","m_tezgah",(1186,560,86,88))

# ============================================================ 7) ESYA BILGI PENCERESI PARCALARI
EQ=(1727,507); UN=(1816,507); RM=(1270,196)
yaz("btn_equip",mat(Y("f_equip")[EQ[1]+548:EQ[1]+610,EQ[0]+12:EQ[0]+167]),x=12)
yaz("btn_unequip",mat(Y("f_unequip")[UN[1]+548:UN[1]+610,UN[0]+12:UN[0]+167]),x=12)
yaz("btn_close",mat(Y("f_equip")[EQ[1]+548:EQ[1]+610,EQ[0]+173:EQ[0]+328]),x=173)
yaz("btn_remove",krom("m_ipucu_b",(RM[0]+12,RM[1]+652,155,62)),x=12)
c=mat(Y("f_equip")[EQ[1]+5:EQ[1]+108,EQ[0]+5:EQ[0]+108]); c[7:96,7:96,3]=0
yaz("ikon_cerceve",c,ic=[7,7,89,89])
yaz("ikon_silan_boots",opak("f_equip",(EQ[0]+12,EQ[1]+12,89,89)))
yaz("ikon_knife",opak("f_npc",(1426+12,197+12,89,89)))
yaz("ikon_short_bow",opak("m_ipucu_b",(1270+13,196+13,87,87)))

json.dump(KAYIT,open(os.path.join(OUT,"..","sprite_bilgisi.json"),"w"),indent=1,ensure_ascii=False,default=lambda o: o.item() if hasattr(o,"item") else list(o))
for a,v in KAYIT.items():
    if "ekran" in v: print("%-16s ekran %s  %dx%d"%(a,v["ekran"],v["w"],v["h"]))
print(len(KAYIT),"sprite")

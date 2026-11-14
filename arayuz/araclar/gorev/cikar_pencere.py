#!/usr/bin/env python3
"""QuestList + gorev detayi: ham kromdan (cikar_krom.py) parcalar.
Taban pencerelerden degisen her sey cikarilir; tekrar eden ogeler ayri sprite olur:
  liste_pencere, detay_pencere (taban) · portre (NPC resmi, dairesel) · gorev_satiri (QuestList girisi, 9-dilim)
  hedef_satiri (Objectives satiri) · odul_yuvasi (Rewards hucresi) · ornek ikonlar (hedef + 8 odul)."""
from ortak import *
from scipy import ndimage
LI=oku("_ham_liste"); DE=oku("_ham_detay")
LS=(1040,372); DS=(1052,172)
def bol(K,o,x0,y0,x1,y1): return K[y0-o[1]:y1-o[1],x0-o[0]:x1-o[0]]
def sil(K,o,x0,y0,x1,y1): K[y0-o[1]:y1-o[1],x0-o[0]:x1-o[0],3]=0
def satir_medyan(K,o,bx0,by0,bx1,by1,yx0,yy0,yx1,yy1):
    """(yx..) yazi kutusunu, (bx..) zemin kutusunun ayni satirlarindaki yazisiz piksellerin medyaniyla doldurur."""
    for y in range(yy0,yy1):
        r=K[y-o[1],bx0-o[0]:bx1-o[0]]; m=np.ones(len(r),bool); m[yx0-bx0:yx1-bx0]=False
        K[y-o[1],yx0-o[0]:yx1-o[0]]=np.median(r[m],0)
def ayna_doldur(K,o,bx0,bx1,yx0,yy0,yx1,yy1):
    """Baslik tasi dokusu: yazi kutusunu ayni satirin solundan aynalayarak (genie panel yontemi)."""
    w=yx1-yx0; kaynak=list(range(yx0-1,bx0,-1))+list(range(yx1,bx1))
    for i,x in enumerate(range(yx0,yx1)):
        k=kaynak[i%len(kaynak)]
        K[yy0-o[1]:yy1-o[1],x-o[0]]=K[yy0-o[1]:yy1-o[1],k-o[0]]
def ping(a,b,n):
    """a..b araligini ileri-geri tarayan n uzunlukta sutun dizisi (dikis yok)"""
    s=list(range(a,b))+list(range(b-1,a-1,-1)); return [s[i%len(s)] for i in range(n)]
def doku_doldur(K,o,kx0,kx1,yx0,yy0,yx1,yy1):
    """Yazi kutusunu ayni satirlarin [kx0,kx1) temiz sutunlarindan ileri-geri kopyalar."""
    for x,k in zip(range(yx0,yx1),ping(kx0,kx1,yx1-yx0)):
        K[yy0-o[1]:yy1-o[1],x-o[0]]=K[yy0-o[1]:yy1-o[1],k-o[0]]
def opak(K,O,o,x0,y0,x1,y1):
    b=K[y0-o[1]:y1-o[1],x0-o[0]:x1-o[0]]; m=b[:,:,3]>40
    b[m,:3]=O[y0:y1,x0:x1][m]; b[m,3]=255
def govde(K,o,x0,y0,x1,y1,istisna):
    """Pencere ici duz siyah zemin: bilinen ogeler disinda kalan her sey (arkadaki sahnenin hareket izleri) saydam."""
    b=K[y0-o[1]:y1-o[1],x0-o[0]:x1-o[0]]; keep=np.zeros(b.shape[:2],bool)
    yy,xx=np.mgrid[y0:y1,x0:x1]
    for e in istisna:
        if len(e)==3: keep|=np.hypot(xx-e[0],yy-e[1])<=e[2]
        else: keep|=(xx>=e[0])&(xx<e[2])&(yy>=e[1])&(yy<e[3])
    b[~keep,3]=0
def disari(K,o,ic,istisna):
    """Pencere kutusu disi: yalniz X dugmesi ve kose susleri."""
    H,W=K.shape[:2]; yy,xx=np.mgrid[o[1]:o[1]+H,o[0]:o[0]+W]
    m=(xx>=ic[0])&(xx<ic[2])&(yy>=ic[1])&(yy<ic[3])
    for e in istisna: m|=(xx>=e[0])&(xx<e[2])&(yy>=e[1])&(yy<e[3])
    K[~m,3]=0
def daire(K,o,cx,cy,r):
    n=2*r; p=bol(K,o,cx-r,cy-r,cx+r,cy+r).copy(); yy,xx=np.mgrid[0:n,0:n]; d=np.hypot(xx-r+0.5,yy-r+0.5)
    p[:,:,3]=np.clip((r-d)/1.5+0.5,0,1)*255; return p,d
# ---------------- portre (liste; ayni resim detayda da) ----------------
PR=63
p,d=daire(LI,LS,1181,567,PR)
p[:,:,:3]=bol(Y("q_liste")[...,],(0,0),1181-PR,567-PR,1181+PR,567+PR)       # opak resim: renk dogrudan orijinal
yaz("portre",p)
for K,o,cy in ((LI,LS,567),(DE,DS,358)):
    yy,xx=np.mgrid[cy-PR-2:cy+PR+2,1181-PR-2:1181+PR+2]; m=np.hypot(xx-1181,yy-cy)<PR-0.5
    blk=K[cy-PR-2-o[1]:cy+PR+2-o[1],1181-PR-2-o[0]:1181+PR+2-o[0]]; blk[m,3]=0
# ---------------- QuestList ----------------
OL=Y("q_liste"); ODt=Y("q_detay")
opak(LI,OL,LS,1050,388,1634,470)                                         # baslik tasi
disari(LI,LS,(1056,388,1622,829),[(1040,385,1060,470),(1615,385,1640,470),(1575,780,1600,842)])
govde(LI,LS,1062,470,1616,824,[(1181,567,73),(1250,507,1575,633),(1122,694,1590,776)])
# aciklama kutusu: arkadaki karakterin izi + yazi -> kutunun medyan rengi/alfasi (yari saydam gri, olculdu)
kl=bol(LI,LS,1252,509,1573,632); kl[:]=np.median(kl[(kl[:,:,3]>100)&(kl[:,:,3]<200)],0)
g=bol(LI,LS,1122,694,1590,776).copy()
gi=g[:,:,:]; gi[729-694-3:747-694+4,1236-1122-4:1475-1122+5,3]=0       # yazi -> zemin (saydam)
yaz("gorev_satiri",g)
sil(LI,LS,1122,694,1590,776)
yaz("liste_pencere",LI)
# ---------------- detay ----------------
opak(DE,ODt,DS,1062,183,1640,255)                                        # baslik tasi
disari(DE,DS,(1070,187,1629,998),[(1056,186,1072,255),(1575,175,1648,255),(1590,940,1648,1012)])
govde(DE,DS,1076,255,1622,996,[(1181,358,73),(1252,296,1576,470),(1095,452,1232,486),(1095,594,1232,628),(1117,496,1592,574),
                               (1128,638,1584,940),(1150,954,1566,999)])
doku_doldur(DE,DS,1100,1215,1222,203,1447,233)                           # baslik yazisi
# aciklama kutusu: arkadaki sahne izleri (ad etiketi, hedef cubugu) + yazi -> kutunun medyan rengi/alfasi
kut=bol(DE,DS,1254,298,1574,468)
temiz=kut[(kut[:,:,3]>40)&(kut[:,:,3]<90)]; med=np.median(temiz,0)
kut[:]=med
yaz("_detay_kutu_bilgi",np.full((2,2,4),med))
h=bol(DE,DS,1117,496,1592,574).copy()
h[512-496:558-496,1132-1117:1178-1117,3]=0                              # ikon ici
h[510-496:562-496,1183-1117:1290-1117,3]=0                              # iki satir yazi
yaz("hedef_satiri",h); sil(DE,DS,1117,496,1592,574)
o=bol(DE,DS,1128,638,1356,712).copy()
o[653-638:698-638,1141-1128:1188-1128,3]=0                              # ikon ici
o[652-638:680-638,1192-1128:1348-1128,3]=0                              # ad
yaz("odul_yuvasi",o); sil(DE,DS,1128,638,1584,940)
for x,k in zip(range(1218,1334),ping(1470,1504,116)):                    # "Accepted" -> Close dugmesinin yazisiz sutunlari (ayni dugme)
    DE[958-DS[1]:996-DS[1],x-DS[0]]=DE[958-DS[1]:996-DS[1],k-DS[0]]
yaz("detay_pencere",DE)
# ---------------- ornek ikonlar (prefab ornegi) ----------------
OD=Y("q_detay")
ik=OD[512:558,1132:1178].copy(); m=np.zeros(ik.shape[:2],bool); m[27:46,22:46]=True        # "25" -> komsu doldurma
_,(iy,ix)=ndimage.distance_transform_edt(m,return_indices=True); ik=ik[iy,ix]
yaz("ikon_hedef",np.dstack([ik,np.full(ik.shape[:2],255.)]))
for r in range(4):
    for c in range(2):
        x=1141+229*c; y=653+76*r; ik=OD[y:y+45,x:x+47]
        yaz("ikon_odul_%d"%(r*2+c+1),np.dstack([ik,np.full(ik.shape[:2],255.)]))
json.dump(dict(liste=dict(sprite=[1040,372,642,470],zemin=[1056,388,566,441],portre=[1181,567,PR],kapat=[1580,390,62,62],
                          aciklama=[1272,516],aciklama_renk="#DD9344",satir=[1122,694,468,82],satir_yazi_merkez=[1355.5,738]),
               detay=dict(sprite=[1052,172,596,840],zemin=[1070,187,559,811],portre=[1181,358,PR],kapat=[1582,183,62,62],
                          baslik_merkez=[1334.5,218],aciklama=[1259,306],aciklama_renk="#E09869",
                          hedef=[1117,496,475,78],hedef_ikon=[1132,512,46,46],hedef_yazi=[[1185,514],[1185,545]],sayi_sag_alt=[1177,558],
                          odul=[1128,638,228,74],odul_adim=[229,76],odul_ikon=[13,15,47,45],odul_yazi=[67,19],
                          kabul=[1153,958,203,37],kabul_yazi_merkez=[1275,980.5],kapat_dugme=[1362,958,150,37])),
          open(os.path.join(OUT,"..","pencere_olculer.json"),"w"),indent=1)
print("tamam")

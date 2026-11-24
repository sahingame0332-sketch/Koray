"""ITEM UPGRADE penceresi: katman cozumu + dinamik iceriklerin temizlenmesi. Calisma klasoru: item.jpg, secim.jpg"""
import numpy as np, json, sys
from PIL import Image
from scipy import ndimage
import ortak as Ot
B=Ot.yukle('secim'); O=Ot.yukle('item'); K=Ot.kirli_maske(B); H,W=B.shape[:2]
X0,Y0,X1,Y1=1165,150,2020,1385
U=np.zeros((H,W),bool); U[252:1322,1189:2001]=True
op=np.zeros((H,W),bool); op[171:252,1174:2019]=True
op[398:517,1266:1390]=True; op[396:517,1813:1938]=True          # buyuk yuvalar (Need Coins / Upgrade Rate): opak
G=np.zeros((H,W),int)
def r(g,x0,y0,x1,y1,ic=4): G[y0+ic:y1-ic,x0+ic:x1-ic]=g
r(1,1210,265,1998,689,3)                                   # ust panel
INV_X=[1227,1337,1446,1555,1665,1774,1884]; INV_Y=[912,1019,1125,1232]
for x in INV_X:
    for y in INV_Y: r(2,x,y,x+92,y+93)                     # envanter yuvalari
Y9X=[1452,1555,1658]; Y9Y=[320,430,540]
for x in Y9X:
    for y in Y9Y: r(3,x,y,x+93,y+93)                       # 3x3 yuvalar
r(4,1241,570,1418,623); r(4,1787,570,1965,623)            # deger kutulari
r(5,1722,826,2002,869,1)                                   # para cubugu ici (govdeden saydam)
a,C,s=Ot.coz(O,B,U,K,op,G)
for g,v in s.items(): print('grup',g,'alfa',v[0],'renk',v[1],'n',v[2])
np.savez('item_coz.npz',a=a,C=C,U=U,G=G)
R=Ot.bilesim(a,C,B,U); sl=np.s_[Y0:Y1,X0:X1]
print('fark',np.abs(R[sl]-O[sl]).mean().round(2))
c=np.concatenate([a[sl][...,None].repeat(3,2)*255, np.abs(R[sl]-O[sl])*8],1)
Image.fromarray(c.clip(0,255).astype(np.uint8)).resize((c.shape[1]//2,c.shape[0]//2)).save('a_kirli.png')
a0=a.copy(); C0=C.copy()
# dinamik icerik: envanter ikonlari -> bos yuva (sablon: 6. sutun 1. satir), deger kutusu yazilari, para
Ot.yuva_kopyala(a,C,(INV_X[5]-4,INV_Y[0]-4),[(x-4,y-4) for x in INV_X for y in INV_Y],100,101)
Ot.yazi_sil(a,C,1245,574,1414,619); Ot.yazi_sil(a,C,1791,574,1961,619)
Ot.yazi_sil(a,C,1780,826,1990,866,32); Ot.yazi_sil(a,C,1780,862,1990,874,150)
sl=np.s_[Y0:Y1,X0:X1]
np.savez('item_coz.npz',a=a,C=C,U=U,G=G)
spr=np.dstack([C,a*255])[sl]
Image.fromarray(spr.clip(0,255).astype(np.uint8),'RGBA').save('item_sprite.png')
# onizleme icin arka plan: kirli bolgelerde gercek arka plan, O'dan geri cozulur (govde: B = O/T0)
Bt=B.copy(); deg=(a!=a0)|(C!=C0).any(-1); kk=K&U&(a<0.9)&~deg
Bt[kk]=np.clip((O[kk]-a[kk][:,None]*C[kk])/((1-a[kk][:,None])*Ot.T0),0,255)
kd=K&U&deg
if kd.any():
    _,(iy,ix)=ndimage.distance_transform_edt(kd,return_indices=True); Bt[kd]=Bt[iy[kd],ix[kd]]
np.save('arka_item.npy',Bt)
R=Ot.bilesim(a,C,Bt,U)
Image.fromarray(R[sl].clip(0,255).astype(np.uint8)).save('item_yeni_bos.png')

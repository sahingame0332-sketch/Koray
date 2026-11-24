"""ITEM / ACCESSORY / FAST UPGRADE pencereleri: katman cozumu (arka plan = Select Upgrade goruntusu, ayni kamera),
dinamik iceriklerin silinmesi (envanter ikonlari -> bos yuva, deger kutusu yazilari, para), sprite + onizleme.
Kullanim (calisma klasorunde secim.jpg + <ad>.jpg): pencere.py item|aksesuar|hizli"""
import numpy as np, json, sys
from PIL import Image
from scipy import ndimage
import ortak as Ot
CFG={
 'item':dict(kutu=(1165,150,2022,1385),U=(1189,252,2001,1322),baslik=(1174,171,2019,252),
     inv_x=[1227,1337,1446,1555,1665,1774,1884],inv_y=[912,1019,1125,1232],yuva=(92,93),
     sil=[(1245,574,1414,619,40),(1791,574,1961,619,40),(1780,826,1990,866,32),(1780,862,1990,874,150)],
     para=(1785,826,1990,868), degerler=[(1241,570,1418,623),(1787,570,1965,623)]),
 'aksesuar':dict(kutu=(1170,150,2022,1385),U=(1192,252,2004,1322),baslik=(1180,160,2020,250),
     inv_x=[1227,1337,1446,1555,1665,1774,1884],inv_y=[912,1019,1126,1232],yuva=(92,93),
     sil=[(1245,600,1414,645,40),(1805,600,1962,645,40),(1780,828,1990,868,32),(1780,864,1990,876,150)],
     para=(1785,828,1990,870), degerler=[(1240,597,1417,650),(1796,597,1973,650)],
     opak=[(1256,304,1384,428),(1256,433,1384,557),(1823,371,1950,496)]),
 'hizli':dict(kutu=(1160,150,2022,1395),U=(1182,252,2006,1352),baslik=(1166,172,2021,250),
     inv_x=[1218,1328,1439,1550,1660,1771,1882],inv_y=[922,1030,1137,1245],yuva=(92,93),
     sil=[(1780,838,1990,878,32),(1780,874,1990,886,150)],
     para=(1785,838,1990,880), degerler=[(1432,637,1786,676)]),
}
ad=sys.argv[1]; c=CFG[ad]
B=Ot.yukle('secim'); O=Ot.yukle(ad); K=Ot.kirli_maske(B); H,W=B.shape[:2]
U=np.zeros((H,W),bool); x0,y0,x1,y1=c['U']; U[y0:y1,x0:x1]=True
op=np.zeros((H,W),bool); x0,y0,x1,y1=c['baslik']; op[y0:y1,x0:x1]=True
for x0,y0,x1,y1 in c.get('opak',[]): op[y0:y1,x0:x1]=True
a,C,s=Ot.coz(O,B,U,K,op)
a0=a.copy(); C0=C.copy()
w,h=c['yuva']; X,Y=c['inv_x'],c['inv_y']
Ot.yuva_hizali(a,C,(X[5]-3,Y[0]-3),[(x-3,y-3) for x in X for y in Y if (x,y)!=(X[5],Y[0])],w+6,h+6)
for x0,y0,x1,y1,e in c['sil']: Ot.yazi_sil(a,C,x0,y0,x1,y1,e)
X0,Y0,X1,Y1=c['kutu']; sl=np.s_[Y0:Y1,X0:X1]
deg=(a!=a0)|(C!=C0).any(-1); kk=K&U&(a<0.9)&~deg
Bt=B.copy(); Bt[kk]=np.clip((O[kk]-a[kk][:,None]*C[kk])/((1-a[kk][:,None])*Ot.T0),0,255)
kd=K&U&deg
if kd.any():
    _,(iy,ix)=ndimage.distance_transform_edt(kd,return_indices=True); Bt[kd]=Bt[iy[kd],ix[kd]]
np.savez_compressed(ad+'_coz.npz',a=a[sl],C=C[sl],U=U[sl],arka=Bt[sl],O=O[sl])
Image.fromarray(np.dstack([C,a*255])[sl].clip(0,255).astype(np.uint8),'RGBA').save(ad+'_sprite.png')
R=Ot.bilesim(a0,C0,Bt,U)
print(ad,'yeniden bilesim farki',np.abs(R[sl]-O[sl]).mean().round(2))
Image.fromarray(Ot.bilesim(a,C,Bt,U)[sl].clip(0,255).astype(np.uint8)).save(ad+'_yeni_bos.png')
json.dump({k:(v if not isinstance(v,tuple) else list(v)) for k,v in c.items()},open(ad+'_cfg.json','w'))

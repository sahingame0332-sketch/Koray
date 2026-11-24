"""Kutu olculeri + bolge saydamliklari (tasarim gruplari). Cikti <ad>_olcu.json ve ekrana tablo."""
import numpy as np, json, sys
from PIL import Image
import ortak as Ot
B=Ot.yukle('secim'); K=Ot.kirli_maske(B)
UR={'item':(1189,252,2001,1324),'aksesuar':(1192,252,2004,1324),'hizli':(1182,252,2006,1354)}
for ad,(x0,y0,x1,y1) in UR.items():
    O=Ot.yukle(ad); H,W=O.shape[:2]; U=np.zeros((H,W),bool); U[y0:y1,x0:x1]=True
    kt=Ot.kutular(O,U)
    tab=B*Ot.T0; lum=O.mean(-1); tl=tab.mean(-1)
    def oran(m):
        t=m&~K&(lum<=0.6*tl+22)
        if t.sum()<50: return None
        k=np.polyfit(tl[t],lum[t],1)[0]; c0=np.median(lum[t]-k*tl[t])
        return dict(alfa_ek=round(1-float(np.clip(k,0,1)),3),toplam_gecirgenlik=round(float(np.clip(k,0,1))*Ot.T0,4),sabit=round(float(c0),1),n=int(t.sum()))
    tur={}
    for (x,y,w,h) in kt:
        if w>150: t='deger_kutusu'
        elif y>880: t='envanter_yuvasi'
        elif w>95: t='buyuk_yuva'
        else: t='kucuk_yuva'
        tur.setdefault(t,[]).append([int(x),int(y),int(w),int(h)])
    sonuc={}
    for t,L in tur.items():
        m=np.zeros((H,W),bool)
        for x,y,w,h in L: m[y+3:y+h-3,x+3:x+w-3]=True
        sonuc[t]=dict(kutular=L,saydamlik=oran(m))
    # govde: U icinde kutu/panel olmayan, govde gecirgenligi dogrudan
    t=U&~K&(lum<0.6*tl+22); g=U.copy()
    for L in tur.values():
        for x,y,w,h in L: g[y-4:y+h+4,x-4:x+w+4]=False
    m=g&t&(B.mean(-1)>40); r=O.mean(-1)[m]/B.mean(-1)[m]
    print(ad,'govde gecirgenlik (medyan, panel dahil karisik)',np.round(np.percentile(r,[25,50]),3))
    for t_,v in sonuc.items(): print(' ',ad,t_,len(v['kutular']),'adet; ilk',v['kutular'][0],'saydamlik',v['saydamlik'])
    json.dump(sonuc,open(ad+'_olcu.json','w'),indent=1)

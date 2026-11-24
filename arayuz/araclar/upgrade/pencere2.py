"""ITEM / ACCESSORY / FAST UPGRADE — tasarim gruplu katman cozumu (2. surum).
Kutular gri kenar cizgilerinden otomatik bulunur (ortak.kutular); saydamlik her tasarim bolgesi icin birlikte olculur:
  govde (siyah Image alfa 1-T0), panel(ler), kucuk yuvalar, deger kutulari, envanter yuvalari; buyuk yuvalar + krom opak.
Kullanim: pencere2.py item|aksesuar|hizli   (calisma klasoru: secim.jpg + <ad>.jpg)"""
import numpy as np, json, sys
from PIL import Image
from scipy import ndimage
import ortak as Ot
CFG={
 'item':dict(kutu=(1165,150,2022,1385),U=(1189,252,2001,1324),baslik=(1174,171,2019,252),
     paneller=[(1212,270,1993,680)], opak=[(1266,398,1390,517),(1813,396,1938,517)],
     cubuk=(1722,826,2002,869), sil=[(1780,826,1990,866,32),(1780,862,1990,874,150)]),
 'aksesuar':dict(kutu=(1170,150,2022,1385),U=(1192,252,2004,1324),baslik=(1180,160,2020,250),
     paneller=[(1212,271,1437,680),(1440,271,1773,680),(1777,271,1993,680)],
     opak=[(1256,304,1384,428),(1256,433,1384,557),(1823,371,1950,496)],
     cubuk=(1722,828,2002,871), sil=[(1780,828,1990,868,32),(1780,864,1990,876,150)]),
 'hizli':dict(kutu=(1160,150,2022,1395),U=(1182,252,2006,1354),baslik=(1166,172,2021,250),
     paneller=[], opak=[], cubuk=(1722,838,2002,881), sil=[(1780,838,1990,878,32),(1780,874,1990,886,150)]),
}
ad=sys.argv[1]; c=CFG[ad]
B=Ot.yukle('secim'); O=Ot.yukle(ad); K=Ot.kirli_maske(B); H,W=B.shape[:2]
U=np.zeros((H,W),bool); x0,y0,x1,y1=c['U']; U[y0:y1,x0:x1]=True
op=np.zeros((H,W),bool); x0,y0,x1,y1=c['baslik']; op[y0:y1,x0:x1]=True
for x0,y0,x1,y1 in c['opak']: op[y0:y1,x0:x1]=True
kt=Ot.kutular(O,U)
kucuk=[k for k in kt if k[2]<150 and k[1]<880]; deger=[k for k in kt if k[2]>=150]; env=[k for k in kt if k[1]>=880]
# envanter izgarasi: bulunan (bos) yuvalarin x / y kumelerinden 7 x 4
def kume(v,ara):
    v=sorted(v); g=[[v[0]]]
    for q in v[1:]:
        (g[-1].append(q) if q-g[-1][-1]<ara else g.append([q]))
    return [int(round(np.median(t))) for t in g]
gx=kume([k[0] for k in env],20); gy=kume([k[1] for k in env],20)
if len(gy)==3: gy=gy+[gy[-1]+(gy[-1]-gy[-2])]
ew=int(np.median([k[2] for k in env])); eh=int(np.median([k[3] for k in env]))
G=np.zeros((H,W),int)
def r(g,x,y,w,h,i=2): G[y+i:y+h-i,x+i:x+w-i]=g
for i,(x0,y0,x1,y1) in enumerate(c['paneller']): G[y0:y1,x0:x1]=1+i
for k in kucuk: r(10,*k)
for k in deger: r(11,*k)
for x in gx:
    for y in gy: r(12,x,y,ew,eh)
x0,y0,x1,y1=c['cubuk']; G[y0:y1,x0:x1]=np.where(G[y0:y1,x0:x1]==0,13,G[y0:y1,x0:x1])
a,C,s=Ot.coz(O,B,U,K,op,G)
AD={1:'panel',2:'panel orta',3:'panel sag',10:'kucuk yuva',11:'deger kutusu',12:'envanter yuvasi',13:'para cubugu'}
olcu={}
for g,v in sorted(s.items()):
    if g<10000: olcu[AD.get(g,str(g))]=dict(ek_alfa=v[0],renk=v[1],n=v[2],toplam_gecirgenlik=round((1-v[0])*Ot.T0,4))
for k,v in olcu.items(): print(ad,k,v)
a0=a.copy(); C0=C.copy()
# ikonlu yuvalar: bos sablon (bulunan ilk bos yuva, cerceve dahil +4) ile degistirilir; bos yuvalara dokunulmaz
def dolu(x,y):
    ic=O[y+4:y+eh-4,x+4:x+ew-4]; kr=O[y-4:y+eh+4,x-4:x+ew+4]
    sat=ic.max(-1)-ic.min(-1); kenar_altin=np.percentile((kr[...,0]-kr[...,2]),97)>45
    return np.percentile(ic.mean(-1),99)>60 or np.percentile(sat,99)>40 or kenar_altin
hucre=[(x,y) for y in gy for x in gx]
bosh=[(x,y) for x,y in hucre if not dolu(x,y)]
sx,sy=min(bosh,key=lambda p:O[p[1]+4:p[1]+eh-4,p[0]+4:p[0]+ew-4].std())
Ta=a[sy-4:sy+eh+4,sx-4:sx+ew+4].copy(); Tc=C[sy-4:sy+eh+4,sx-4:sx+ew+4].copy()
print(ad,'envanter',len(gx),'x',len(gy),'bos',len(bosh),'sablon',(sx,sy))
hh,ww=Ta.shape; halka=np.zeros((hh,ww),bool); halka[:7]=halka[-7:]=True; halka[:,:7]=halka[:,-7:]=True
Tl=Tc.mean(-1)
for x,y in hucre:
    if (x,y) in bosh: continue
    en=None
    for dy in range(-4,5):
        for dx in range(-4,5):
            R=O[y-4+dy:y-4+dy+hh,x-4+dx:x-4+dx+ww].mean(-1); kr=O[y-4+dy:y-4+dy+hh,x-4+dx:x-4+dx+ww]
            gri=(kr.max(-1)-kr.min(-1))<35                   # altin vurgu piksellerini sayma
            e=np.median(np.abs(R-Tl)[halka&gri])
            if en is None or e<en[0]: en=(e,dx,dy)
    _,dx,dy=en
    a[y-4+dy:y-4+dy+hh,x-4+dx:x-4+dx+ww]=Ta; C[y-4+dy:y-4+dy+hh,x-4+dx:x-4+dx+ww]=Tc
for x,y,w,h in deger: Ot.yazi_sil(a,C,x+3,y+3,x+w-3,y+h-3,40)
for x0,y0,x1,y1,e in c['sil']: Ot.yazi_sil(a,C,x0,y0,x1,y1,e)
X0,Y0,X1,Y1=c['kutu']; sl=np.s_[Y0:Y1,X0:X1]
deg=(a!=a0)|(C!=C0).any(-1); kk=K&U&(a<0.9)&~deg
Bt=B.copy(); Bt[kk]=np.clip((O[kk]-a[kk][:,None]*C[kk])/((1-a[kk][:,None])*Ot.T0),0,255)
kd=K&U&deg
if kd.any():
    _,(iy,ix)=ndimage.distance_transform_edt(kd,return_indices=True); Bt[kd]=Bt[iy[kd],ix[kd]]
np.savez_compressed(ad+'_coz.npz',a=a[sl],C=C[sl],U=U[sl],arka=Bt[sl],O=O[sl])
Image.fromarray(np.dstack([C,a*255])[sl].clip(0,255).astype(np.uint8),'RGBA').save(ad+'_sprite.png')
print(ad,'yeniden bilesim farki',np.abs(Ot.bilesim(a0,C0,Bt,U)[sl]-O[sl]).mean().round(2))
rel=lambda k:[int(k[0]-X0),int(k[1]-Y0),int(k[2]),int(k[3])]
json.dump(dict(kutu=list(c['kutu']),U=list(c['U']),govde_alfa=round(1-Ot.T0,3),saydamlik=olcu,
    kucuk_yuvalar=[rel(k) for k in kucuk],deger_kutulari=[rel(k) for k in deger],
    envanter=dict(x=[x-X0 for x in gx],y=[y-Y0 for y in gy],w=ew,h=eh)),open(ad+'_cfg.json','w'),indent=1)

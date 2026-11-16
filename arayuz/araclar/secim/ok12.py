import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw
z=np.load('ok_ornek2.npz'); Es,Bs,bads=z['E'],z['B'],z['bad']; K,Hc,Wc=Es.shape[:3]; V=~bads
_,_,_,_,cx,yuc,Yb,Yalt,hb,sw,t,_,_=np.load('ok_meta.npy')
A_K,A_D=0.85,0.47
S=4; im=Image.new('L',(Wc*S,Hc*S),0)
ImageDraw.Draw(im).polygon([(x*S,y*S) for x,y in [(cx,yuc),(cx+hb,Yb),(cx+sw,Yb),(cx+sw,Yalt),(cx-sw,Yalt),(cx-sw,Yb),(cx-hb,Yb)]],fill=255)
dt4=ndimage.distance_transform_edt(np.asarray(im)>127)/S
dt4=dt4-ndimage.distance_transform_edt(np.asarray(im)<=127)/S   # isaretli uzaklik
dt=dt4.reshape(Hc,S,Wc,S).mean((1,3))                      # 4x4 ortalama: kenar merdivensiz
yy=np.repeat(np.arange(Hc)[:,None],Wc,1)
O=Es+Bs
# alfa profili dt'ye gore: kenar 0..3 rampasi, krem 3..16 (A_K), gecis 16..20, dolgu A_D
def alfa_dt(d):
    return np.interp(d,[-0.5,1.5,4,15,19.5],[0,0.15,A_K,A_K,A_D])
al=alfa_dt(dt)
Pk=O-(1-al)[None,...,None]*Bs                     # her ornekte on-carpimli renk
Pm=np.where(V[...,None]&(yy<205)[None,...,None],Pk,np.nan)   # alt kisimda karakter ortusu cok: renk ustten
# krem/kenar (dt<19.5): dt kutularina gore medyan
P=np.zeros((Hc,Wc,3))
kb=np.arange(0,20,0.5)
for b0 in kb:
    m=(dt>b0)&(dt<=b0+0.5)
    if m.any():
        v=Pm[:,m].reshape(-1,3); v=v[np.isfinite(v).all(1)]
        if len(v): P[m]=np.median(v,0)
# dolgu (dt>19.5): satira gore medyan (dikey renk gecisi); y>=205 icin son olculen satirlar uzatilir
ic=dt>19.5; prof=np.full((Hc,3),np.nan)
for y in range(Hc):
    m=ic[y]
    if m.any() and y<205:
        v=Pm[:,y,m].reshape(-1,3); v=v[np.isfinite(v).all(1)]
        if len(v)>10: prof[y]=np.median(v,0)
ok=np.isfinite(prof[:,0]); ys=np.arange(Hc)
prof=np.stack([np.interp(ys,ys[ok],ndimage.gaussian_filter1d(prof[ok,c],3)) for c in range(3)],1)
P[ic]=prof[yy[ic]]
# dolgu-krem gecisi yumusak
w=np.clip((dt-17)/3,0,1)[...,None]; P=np.where(ic[...,None]|(w>0),w*np.repeat(prof[:,None],Wc,1)+(1-w)*P,P)
P=np.clip(P,0,255); P=np.minimum(P,al[...,None]*255+0.5)
P=(P+P[:,::-1])/2; al=(al+al[:,::-1])/2
for y in (60,100,140,180,200): print('dolgu satir',y,np.round(prof[y]/A_D))
print('krem (dt 9-12) renk', np.round(P[(dt>9)&(dt<12)].mean(0)/A_K))
for k in (0,2,4):
    Op=P+(1-al[...,None])*Bs[k]; m=V[k]&(al>0.05)&(yy<205)
    print('ornek',k//2,'ok ici ort fark',round(float(np.abs(O[k]-Op)[m].mean()),2))
ys_,xs_=np.nonzero(al>0.004); y0,y1,x0,x1=ys_.min()-2,ys_.max()+3,xs_.min()-2,xs_.max()+3
Image.fromarray(np.dstack([P,al*255])[y0:y1,x0:x1].round().astype(np.uint8),'RGBA').save('ok_doku.png')
np.save('ok_meta2.npy',np.array([x0,y0,x1-x0,y1-y0,cx,yuc,Yb,Yalt,hb,sw]))
c=[]
for k in (0,2,4):
    Op=P+(1-al[...,None])*Bs[k]; c.append(np.concatenate([O[k],Op],1)[y0:y1])
Image.fromarray(np.clip(np.concatenate(c,1),0,255).astype(np.uint8)).resize((Wc*6*2,(y1-y0)*2)).save('ok_kars.png')
print('doku',x1-x0,y1-y0)

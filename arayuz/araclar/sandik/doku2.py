import numpy as np, json
from PIL import Image
from scipy import ndimage
from geo import proj, R
from mesh import N
U=json.load(open('uydu.json')); D,HB,HL=U['sekil']; a=D/2; L=1.0
CAM={int(k):v for k,v in U['kam'].items()}
AC=json.load(open('acik.json')); CAM[1]=AC['kam']; ACI=AC['aci']
crop={1:(780,590,960,800),2:(755,455,895,575),3:(670,500,805,620),4:(860,340,970,425)}
IMG={i:np.asarray(Image.open('s%d.jpg'%i).convert('RGB'),dtype=np.float32) for i in crop}
MS={}
for i,(x0,y0,x1,y1) in crop.items():
    M=np.zeros((1220,2712),bool); m=np.load('m1t.npy' if i==1 else 'm%d.npy'%i)
    M[y0:y0+m.shape[0],x0:x0+m.shape[1]]=ndimage.binary_erosion(m,np.ones((3,3))); MS[i]=M
PX=320
def yuzey(pts,nrm,goruntuler,sekil):
    """pts/nrm (H,W,3) -> en iyi bakan goruntuden ornek; gecersiz pikseller NaN"""
    H,W=sekil; best=np.full((H,W),-1.0); out=np.full((H,W,3),np.nan)
    for i in goruntuler:
        P=CAM[i]; q=proj(pts.reshape(-1,3),P); g=(R(P[0],P[1],P[2])@nrm.reshape(-1,3).T)[2]
        if P[3]<0: pass
        x,y=q[:,0],q[:,1]; ok=(x>=0)&(x<2711)&(y>=0)&(y<1219)
        ok[ok]&=MS[i][y[ok].astype(int),x[ok].astype(int)]
        ok&=g>0.15
        c=np.stack([ndimage.map_coordinates(IMG[i][...,k],[y,x],order=1) for k in range(3)],-1)
        g=g.reshape(H,W); ok=ok.reshape(H,W); c=c.reshape(H,W,3)
        sec=ok&(g>best); out[sec]=c[sec]; best[sec]=g[sec]
    return out
def doldur(T):
    bad=~np.isfinite(T).all(2)
    if bad.all() or not bad.any(): return np.nan_to_num(T)
    _,(iy,ix)=ndimage.distance_transform_edt(bad,return_indices=True); return T[iy,ix]
def kaydet(ad,T,alfa=None):
    T=np.clip(T,0,255); A=np.full(T.shape[:2],255.) if alfa is None else alfa*255
    Image.fromarray(np.dstack([T,A]).astype(np.uint8),'RGBA').save('t_%s.png'%ad); print(ad,T.shape[1],T.shape[0],'eksik %',round(100*np.mean(~np.isfinite(T).all(2)) if False else 0,1))
def izgara(W,H): v,u=np.mgrid[0:H,0:W]+0.5; return u/W, 1-v/H     # v: 1 ust satir
# on (z=+a): u=x, v=y/HB
W,H=int(L*PX),int(HB*PX); u,v=izgara(W,H)
p=np.stack([u*L,v*HB,np.full_like(u,a)],-1); n=np.broadcast_to([0,0,1.],p.shape)
T=yuzey(p,n,[2],(H,W)); print('on eksik',np.isnan(T[...,0]).mean().round(3)); kaydet('on',doldur(T))
# arka (z=-a): u=0 -> x=L
p=np.stack([(1-u)*L,v*HB,np.full_like(u,-a)],-1); n=np.broadcast_to([0,0,-1.],p.shape)
T=yuzey(p,n,[4],(H,W)); print('arka eksik',np.isnan(T[...,0]).mean().round(3)); kaydet('arka',doldur(T))
# uc (x=L): u=0 -> z=+a ; v=y/(HB+HL); kemer disi saydam
W,H=int(D*PX),int((HB+HL)*PX); u,v=izgara(W,H); z=a-u*D; y=v*(HB+HL)
p=np.stack([np.full_like(u,L),y,z],-1); n=np.broadcast_to([1,0,0.],p.shape)
T=yuzey(p,n,[3],(H,W)); ic=(y<=HB)|((z/a)**2+((y-HB)/HL)**2<=1)
print('uc eksik (ic)',np.isnan(T[...,0])[ic].mean().round(3))
kaydet('uc',doldur(T),ndimage.gaussian_filter(ic.astype(float),0.8))
# kapak dis: u=x, v=k/N -> phi=v*pi (v=1 arka dikis)
W,H=int(L*PX),int(np.pi*0.5*(a+HL)*PX); u,v=izgara(W,H); phi=v*np.pi
p=np.stack([u*L,HB+HL*np.sin(phi),a*np.cos(phi)],-1)
n=np.stack([np.zeros_like(u),np.sin(phi)/HL,np.cos(phi)/a],-1); n/=np.linalg.norm(n,axis=-1,keepdims=True)
T=yuzey(p,n,[2],(H,W)); eks=np.isnan(T[...,0]); print('kapak eksik',eks.mean().round(3))
T=np.where(eks[...,None],T[::-1],T)          # on/arka simetri
print('kapak eksik (ayna sonrasi)',np.isnan(T[...,0]).mean().round(3)); kaydet('kapak',doldur(T))
# acik: govde ustu (y=HB duzlemi), kapak ici (acik kapak, s1 kamerasi)
W,H=int(L*PX),int(D*PX); u,v=izgara(W,H)
p=np.stack([u*L,np.full_like(u,HB),-a+(1-v)*D],-1); n=np.broadcast_to([0,1,0.],p.shape)
T=yuzey(p,n,[1],(H,W)); print('ust_acik eksik',np.isnan(T[...,0]).mean().round(3)); kaydet('ust_acik',doldur(T))
W,H=int(L*PX),int(np.pi*0.5*(a+HL)*PX); u,v=izgara(W,H); phi=v*np.pi
yy,zz=HL*np.sin(phi),a*np.cos(phi)+a; c,s=np.cos(ACI),np.sin(ACI)
p=np.stack([u*L,HB+yy*c+zz*s,-a+(-yy*s+zz*c)],-1)
n0=np.stack([np.zeros_like(u),-np.sin(phi)/HL,-np.cos(phi)/a],-1); n0/=np.linalg.norm(n0,axis=-1,keepdims=True)
n=np.stack([n0[...,0],n0[...,1]*c+n0[...,2]*s,-n0[...,1]*s+n0[...,2]*c],-1)
T=yuzey(p,n,[1],(H,W)); print('kapak_ic eksik',np.isnan(T[...,0]).mean().round(3)); kaydet('kapak_ic',doldur(T))
json.dump({'L':L,'D':D,'HB':HB,'HL':HL,'aci_derece':float(np.degrees(ACI))},open('olcu.json','w'))

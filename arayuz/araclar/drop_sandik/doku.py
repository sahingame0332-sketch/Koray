"""Geri izdusum ile dokular: her yuzey noktasi uydurulan kameralarla goruntulere izdusurulur, en dik bakan gecerli
goruntuden orneklenir. Calisma klasoru: d*.png, kirp.json, m_*.npy, uydu.json -> t_*.png, olcu.json"""
import numpy as np, json
from PIL import Image
from scipy import ndimage
from geo import proj, R
from mesh import kesit
U=json.load(open('uydu.json')); D,HB,HL,h1,c=U['sekil']; a=D/2; L=1.0; n=(h1,c)
CAM=U['kam']; K=json.load(open('kirp.json'))
IMG={}; MS={}
for k,(i,(x0,y0,x1,y1)) in K.items():
    if i not in IMG: IMG[i]=np.asarray(Image.open('d%d.png'%i).convert('RGB'),dtype=np.float32)
    H,W=IMG[i].shape[:2]; M=np.zeros((H,W),bool); m=np.load('m_%s.npy'%k)
    M[y0:y0+m.shape[0],x0:x0+m.shape[1]]=ndimage.binary_erosion(m,np.ones((5,5))); MS[k]=M
PX=256
def yuzey(pts,nrm,gor,sekil,min_g=0.2):
    H,W=sekil; best=np.full((H,W),-1.0); out=np.full((H,W,3),np.nan); kim=np.full((H,W),'',object)
    for k in gor:
        P=CAM[k]; I=IMG[K[k][0]]; q=proj(pts.reshape(-1,3),P); g=(R(P[0],P[1],P[2])@nrm.reshape(-1,3).T)[2]
        x,y=q[:,0],q[:,1]; ok=(x>=0)&(x<I.shape[1]-1)&(y>=0)&(y<I.shape[0]-1)
        ok[ok]&=MS[k][y[ok].astype(int),x[ok].astype(int)]; ok&=g>min_g
        col=np.stack([ndimage.map_coordinates(I[...,j],[y,x],order=1) for j in range(3)],-1)
        g=g.reshape(H,W); ok=ok.reshape(H,W); col=col.reshape(H,W,3)
        sec=ok&(g>best); out[sec]=col[sec]; best[sec]=g[sec]; kim[sec]=k
    return out,kim
def doldur(T):
    bad=~np.isfinite(T).all(2)
    if bad.all() or not bad.any(): return np.nan_to_num(T)
    _,(iy,ix)=ndimage.distance_transform_edt(bad,return_indices=True); return T[iy,ix]
def kaydet(ad,T,alfa=None):
    T=np.clip(T,0,255); A=np.full(T.shape[:2],255.) if alfa is None else alfa*255
    Image.fromarray(np.dstack([T,A]).astype(np.uint8),'RGBA').save('t_%s.png'%ad)
def izgara(W,H): v,u=np.mgrid[0:H,0:W]+0.5; return u/W, 1-v/H
def rapor(ad,T,kim): print(ad,'eksik',np.isnan(T[...,0]).mean().round(3),{k:int((kim==k).sum()) for k in set(kim.ravel()) if k})
if __name__=="__main__":
    import sys
    GOR={'on':['g'],'arka':['f'],'uc':['d'],'kapak':['b']}
    # on (z=+a)
    W,H=int(L*PX),int(HB*PX); u,v=izgara(W,H)
    p=np.stack([u*L,v*HB,np.full_like(u,a)],-1); T,kim=yuzey(p,np.broadcast_to([0,0,1.],p.shape),GOR['on'],(H,W)); rapor('on',T,kim); kaydet('on',doldur(T))
    p=np.stack([(1-u)*L,v*HB,np.full_like(u,-a)],-1); T,kim=yuzey(p,np.broadcast_to([0,0,-1.],p.shape),GOR['arka'],(H,W)); rapor('arka',T,kim); kaydet('arka',doldur(T))
    # uc (x=L): u=0 -> z=+a ; v=y/(HB+HL); kemer disi saydam
    W,H=int(D*PX),int((HB+HL)*PX); u,v=izgara(W,H); z=a-u*D; y=v*(HB+HL)
    p=np.stack([np.full_like(u,L),y,z],-1); T,kim=yuzey(p,np.broadcast_to([1,0,0.],p.shape),GOR['uc'],(H,W))
    # kemer ici: kesit cokgeni
    ph=np.linspace(0,np.pi,400); kz,ky=kesit(ph,a,HL,n)
    from PIL import ImageDraw
    mi=Image.new('L',(W,H),0); px=lambda zz,yy:((a-zz)/D*W,(1-yy/(HB+HL))*H)
    ImageDraw.Draw(mi).polygon([px(zz,yy+HB) for zz,yy in zip(kz,ky)]+[px(-a,0),px(a,0)],fill=255)
    ic=np.asarray(mi)>127
    rapor('uc',T,kim); kaydet('uc',doldur(T),ndimage.gaussian_filter(ic.astype(float),0.7))
    # kapak dis: u=x, v=k/N (yay uzunlugu orani) ; normal kesit tegetinden
    W,H=int(L*PX),int(1.4*(a+HL)*PX); u,v=izgara(W,H); phi=v*np.pi
    kz,ky=kesit(phi,a,HL,n); e=1e-3; kz2,ky2=kesit(np.clip(phi+e,0,np.pi),a,HL,n); kz1,ky1=kesit(np.clip(phi-e,0,np.pi),a,HL,n)
    tz,ty=kz2-kz1,ky2-ky1; nz,ny=ty,-tz; nn=np.hypot(nz,ny)+1e-12
    p=np.stack([u*L,HB+ky,kz],-1); nr=np.stack([np.zeros_like(u),ny/nn,nz/nn],-1)
    T,kim=yuzey(p,nr,GOR['kapak'],(H,W)); rapor('kapak',T,kim)
    eks=np.isnan(T[...,0]); T=np.where(eks[...,None],T[::-1],T); kaydet('kapak',doldur(T))
    np.save('kapak_kim.npy',kim)
    json.dump({'L':L,'D':D,'HB':HB,'HL':HL,'h1':h1,'c':c},open('olcu.json','w'))
    # ---- acik durum (gorunum c): govde ustu (y=HB duzlemi: kenar + altin) ve kapak ici
    if 'c' in CAM:
        ACI=U['aci']
        W,H=int(L*PX),int(D*PX); u,v=izgara(W,H)
        p=np.stack([u*L,np.full_like(u,HB),-a+(1-v)*D],-1)
        T,kim=yuzey(p,np.broadcast_to([0,1,0.],p.shape),['c'],(H,W),0.05); rapor('ust_acik',T,kim); kaydet('ust_acik',doldur(T))
        # kapak agzi: yerel y=HB duzlemi, u=x, v: 0 -> z=+a ; donmus konumda c'den orneklenir
        W,H=int(L*PX),int(D*PX); u,v=izgara(W,H); co,s=np.cos(ACI),np.sin(ACI)
        zl=a-v*D+a; yl=np.full_like(u,0.004)
        p=np.stack([u*L,HB+yl*co+zl*s,-a+(-yl*s+zl*co)],-1)
        nr=np.broadcast_to([0,-co+0*s,s*1.0],p.shape)            # yerel -y normalinin donmus hali: (0,-cos,sin)
        T,kim=yuzey(p,np.ascontiguousarray(nr),['c'],(H,W),0.05); rapor('kapak_taban',T,kim); T=doldur(T)
        lum=T.mean(-1); al=ndimage.gaussian_filter((lum>34).astype(float),1.0)
        bb=ndimage.binary_erosion(lum>34,np.ones((3,3)),border_value=1); 
        kaydet('kapak_taban',T,al); karanlik=np.median(T[lum<25],0); print('kapak ici renk',karanlik.round(1))
        Image.fromarray(np.tile(karanlik,(8,8,1)).clip(0,255).astype(np.uint8)).save('t_kapak_ic.png')
        if False:
          W,H=int(L*PX),int(1.4*(a+HL)*PX); u,v=izgara(W,H); phi=v*np.pi
          kz,ky=kesit(phi,a-0.012,HL-0.012,n); kz2,ky2=kesit(np.clip(phi+1e-3,0,np.pi),a,HL,n); kz1,ky1=kesit(np.clip(phi-1e-3,0,np.pi),a,HL,n)
          tz,ty=kz2-kz1,ky2-ky1; nz,ny=-ty,tz; nn=np.hypot(nz,ny)+1e-12; nz,ny=nz/nn,ny/nn   # ice bakan normal
          co,s=np.cos(ACI),np.sin(ACI); yy,zz=ky,kz+a
          p=np.stack([u*L,HB+yy*co+zz*s,-a+(-yy*s+zz*co)],-1)
          nr=np.stack([np.zeros_like(u),ny*co+nz*s,-ny*s+nz*co],-1)
          T,kim=yuzey(p,nr,['c'],(H,W),0.05); rapor('kapak_ic',T,kim); kaydet('kapak_ic',doldur(T))

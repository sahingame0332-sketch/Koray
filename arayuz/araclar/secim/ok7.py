import numpy as np
from PIL import Image
from scipy import ndimage
z=np.load('ok_ornek.npz'); Es,Bs,bads=z['E'].copy(),z['B'].copy(),z['bad'].copy()
K=len(Es); Hc,Wc=Es.shape[1:3]
ref=np.where(bads[0][...,None],np.nan,Es[0]).sum(2)
def warp(I,dx,dy,dth,o=1):
    ty,tx=np.mgrid[0:Hc,0:Wc]+0.5; c=np.radians(dth); cx,cy=100,150
    sx=cx+(tx-cx)*np.cos(c)-(ty-cy)*np.sin(c)+dx; sy=cy+(tx-cx)*np.sin(c)+(ty-cy)*np.cos(c)+dy
    return np.stack([ndimage.map_coordinates(I[...,k],[sy,sx],order=o,cval=0) for k in range(I.shape[2])],-1)
for k in range(2,K):
    b=(-2,0,0,0)
    for dth in np.arange(-4,4.5,1):
        for dx in range(-7,8):
            for dy in range(-7,8):
                Ew=warp(Es[k],dx,dy,dth); bw=warp(bads[k][...,None].astype(float),dx,dy,dth,0)[...,0]>0.5
                m=~bw&np.isfinite(ref)&(ref>-50); m[200:]=False
                c=np.corrcoef(Ew.sum(2)[m],ref[m])[0,1]
                if c>b[0]: b=(c,dx,dy,dth)
    print(k,np.round(b,3))
    Es[k]=warp(Es[k],*b[1:]); Bs[k]=warp(Bs[k],*b[1:]); bads[k]=warp(bads[k][...,None].astype(float),*b[1:],o=0)[...,0]>0.5
np.savez('ok_ornek2.npz',E=Es,B=Bs,bad=bads)

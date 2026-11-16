import numpy as np
from scipy import ndimage
p=np.load('rect.npy'); YH,S=p[0],p[1]; R0=p[6]; CX=1356.
PXU=256/1.35/R0           # doku pikseli / zemin birimi (halka dokusuyla ayni olcek)
def zemine(u,v): return (u-CX)/(v-YH), S/(v-YH)
def ekrana(X,D): return CX+X*S/D, YH+S/D
def ac(I,merkez_uv,W,H):
    X0,D0=zemine(*merkez_uv)
    ty,tx=np.mgrid[0:H,0:W]+0.5
    X=X0+(tx-W/2)/PXU; D=D0-(ty-H/2)/PXU
    u,v=ekrana(X,D)
    return np.stack([ndimage.map_coordinates(I[...,c],[v,u],order=1) for c in range(I.shape[2])],-1),u,v

"""Zemin duzlemini yukaridan gorunuse cevirir (igne deligi kamera, egim phi, odak f piksel).
Kamera yuksekligi 1 birim.  Zemin noktasi (X, Z):  zc = Z*cos(phi) + sin(phi),  yc = cos(phi) - Z*sin(phi)
  x = cx + f*X/zc ,  y = cy + f*yc/zc      (ufuk: y_h = cy - f*tan(phi))"""
import numpy as np
from PIL import Image
def yukle(p): return np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
def izdusum(X,Z,f,phi,cx,cy):
    zc=Z*np.cos(phi)+np.sin(phi); yc=np.cos(phi)-Z*np.sin(phi)
    return cx+f*X/zc, cy+f*yc/zc
def geri(x,y,f,phi,cx,cy):
    """goruntu noktasi -> zemin (X,Z)"""
    v=(y-cy)/f                      # yc/zc
    Z=(np.cos(phi)-v*np.sin(phi))/(v*np.cos(phi)+np.sin(phi))
    zc=Z*np.cos(phi)+np.sin(phi)
    return (x-cx)/f*zc, Z
def ornekle(img,x,y):
    H,W=img.shape[:2]
    x0=np.floor(x).astype(int); y0=np.floor(y).astype(int)
    ok=(x0>=0)&(x0<W-1)&(y0>=0)&(y0<H-1)
    x0c=np.clip(x0,0,W-2); y0c=np.clip(y0,0,H-2); fx=(x-x0c)[...,None]; fy=(y-y0c)[...,None]
    a=img[y0c,x0c]*(1-fx)*(1-fy)+img[y0c,x0c+1]*fx*(1-fy)+img[y0c+1,x0c]*(1-fx)*fy+img[y0c+1,x0c+1]*fx*fy
    return a,ok
def duzelt(img,f,phi,X0,X1,Z0,Z1,ppu,cx=None,cy=None):
    """zemin dikdortgeni [X0,X1]x[Z0,Z1] -> ppu piksel/birim yukaridan gorunus (ust satir = uzak)"""
    H,W=img.shape[:2]; cx=W/2 if cx is None else cx; cy=H/2 if cy is None else cy
    nx=int((X1-X0)*ppu); nz=int((Z1-Z0)*ppu)
    Xs=X0+(np.arange(nx)+0.5)/ppu; Zs=Z1-(np.arange(nz)+0.5)/ppu
    X,Z=np.meshgrid(Xs,Zs)
    x,y=izdusum(X,Z,f,phi,cx,cy)
    return ornekle(img,x,y)

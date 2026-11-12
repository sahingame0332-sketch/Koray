"""Pencere bicim maskeleri."""
import numpy as np
from scipy import ndimage
from ortak import *
def cim_disi(kare,kutu,tohum=None):
    """Kutu kenarindan baslayip cim benzeri piksellerden (yesil baskin) gecerek disariyi bulur; kalan = pencere."""
    x,y,w,h=kutu; a=Y(kare)[y:y+h,x:x+w]; R,G,Bl=a[:,:,0],a[:,:,1],a[:,:,2]
    cim=(G>Bl*1.6)&(G>R*0.9)&(a.max(2)>20)
    cim=ndimage.binary_dilation(cim,np.ones((3,3)))
    lab,n=ndimage.label(cim)
    kenar=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    dis=np.isin(lab,list(kenar))
    ic=~dis
    ic=ndimage.binary_opening(ic,np.ones((7,7)))
    lab,n=ndimage.label(ic)
    if n>1:
        s=ndimage.sum(ic,lab,range(1,n+1)); ic=lab==(1+int(np.argmax(s)))
    ic=ndimage.binary_fill_holes(ic)
    return ndimage.gaussian_filter(ic.astype(float),0.8)
def fark_maskesi(once,sonra,kutu,esik=12):
    x,y,w,h=kutu; d=np.abs(Y(sonra)[y:y+h,x:x+w]-Y(once)[y:y+h,x:x+w]).max(2)>esik
    d=ndimage.binary_closing(d,np.ones((9,9))); d=ndimage.binary_opening(d,np.ones((5,5)))
    lab,n=ndimage.label(d)
    if n>1:
        s=ndimage.sum(d,lab,range(1,n+1)); d=lab==(1+int(np.argmax(s)))
    d=ndimage.binary_fill_holes(d)
    return ndimage.gaussian_filter(d.astype(float),0.8)

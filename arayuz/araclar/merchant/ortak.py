"""Merchant isi icin ortak yardimcilar."""
import os, numpy as np
from PIL import Image
B=os.path.dirname(os.path.abspath(__file__))
REF=os.path.join(B,"..","..","referans_gorseller","merchant")
OUT=os.path.join(B,"..","..","kaynak","merchant","sprites")
_c={}
def Y(ad):
    if ad not in _c: _c[ad]=np.asarray(Image.open(os.path.join(REF,ad+".jpg")).convert("RGB")).astype(float)
    return _c[ad]
def mat(R,t0=8.0,T=60.0):
    """Siyaha karsi cozme: alfa = clip((max-t0)/(T-t0)), RGB = R/alfa. Siyah zemin Image'inin ustunde R'yi geri verir."""
    R=np.clip(R,0,255); al=np.clip((R.max(2)-t0)/(T-t0),0,1)
    rgb=np.where(al[...,None]>0,np.clip(R/np.maximum(al[...,None],1e-3),0,255),0)
    return np.dstack([rgb,al*255])
def krom(sonra,kutu,once=None,a=0.95,t0=8.0,T=60.0):
    """kutu=(x,y,w,h). once verilirse zemin katkisi cikarilir: R = O-(1-a)*B ; verilmezse R = O (zemin ~siyah)."""
    x,y,w,h=kutu; O=Y(sonra)[y:y+h,x:x+w]
    if once is not None: O=O-(1-a)*Y(once)[y:y+h,x:x+w]
    return mat(O,t0,T)
def opak(kare,kutu):
    x,y,w,h=kutu; O=Y(kare)[y:y+h,x:x+w]; return np.dstack([O,np.full(O.shape[:2],255.0)])
def degisen(once,sonra,kutu,e0=8.0,e1=30.0):
    x,y,w,h=kutu; O=Y(sonra)[y:y+h,x:x+w]; Bk=Y(once)[y:y+h,x:x+w]
    return np.dstack([O,np.clip((np.abs(O-Bk).max(2)-e0)/(e1-e0),0,1)*255])
def kaydet(ad,rgba): Image.fromarray(np.clip(rgba,0,255).astype(np.uint8),"RGBA").save(os.path.join(OUT,ad+".png"))
def dama(rgba,k=12):
    a=np.asarray(rgba,float); H,W=a.shape[:2]; ch=(np.indices((H,W)).sum(0)//k)%2
    bg=np.where(ch[...,None]==0,np.array([70,150,70]),np.array([40,100,40])).astype(float); al=a[:,:,3:4]/255
    return Image.fromarray((a[:,:,:3]*al+bg*(1-al)).astype(np.uint8))

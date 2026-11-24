"""Power Up Store ortak: goruntuler, sRGB<->lineer, olculen saydamliklar (oyun LINEER uzayda karistiriyor)."""
import numpy as np
from PIL import Image
X0,Y0,X1,Y1=272,0,2409,1220            # magaza (oyun alani) — telefon 2712x1220, iki yanda siyah bant
T_KART=0.30; T_ANA=0.185                # kart ici gecirgenlik (lineer): kategori / ana sayfa
ORTU_A=0.24; ORTU_G=0.24               # basari ortusu: lineer alfa, lineer gri (sRGB ~135)
def yukle(i): return np.asarray(Image.open('s%02d.jpg'%i).convert('RGB'),float)
def lin(v): v=np.clip(v,0,255)/255; return np.where(v<=0.04045,v/12.92,((v+0.055)/1.055)**2.4)
def srgb(l): l=np.clip(l,0,1); return 255*np.where(l<=0.0031308,l*12.92,1.055*l**(1/2.4)-0.055)
def kaydet(ad,rgb,a=None):
    a=np.full(rgb.shape[:2],1.0) if a is None else a
    Image.fromarray(np.dstack([np.clip(rgb,0,255),np.clip(a,0,1)*255]).astype(np.uint8),'RGBA').save(ad)
def ustune(alt,rgb,a,x,y):
    """lineer uzayda alfa karisimi (oyundaki gibi); alt: sRGB tam ekran"""
    h,w=a.shape; sl=np.s_[y:y+h,x:x+w]
    alt[sl]=srgb(lin(rgb)*a[...,None]+lin(alt[sl])*(1-a[...,None]))

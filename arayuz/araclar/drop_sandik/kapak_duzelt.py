"""Kapak dokusunda gumus bantlar satir satir egri cikiyor (izdusum hatasi). Her satirda 4 bandin merkezini bulup
satiri parcali dogrusal olarak bantlar dik ve medyan konumda olacak sekilde yeniden orneklenir."""
import numpy as np
from PIL import Image
from scipy import ndimage
I=np.asarray(Image.open('t_kapak.png').convert('RGB'),dtype=np.float32); H,W=I.shape[:2]
sat=I.max(-1)-I.min(-1); gum=(sat<38).astype(float)
gum=ndimage.uniform_filter1d(gum,5,axis=1)>0.5
x0,x1=int(0.12*W),int(0.88*W); NB=2; mer=np.full((H,NB),np.nan)
for y in range(H):
    l,n=ndimage.label(gum[y,x0:x1])
    if n<NB: continue
    sl=ndimage.find_objects(l); boy=np.array([s[0].stop-s[0].start for s in sl])
    sec=np.sort(np.argsort(boy)[-NB:])
    if boy[sec].min()<6: continue
    mer[y]=[x0+(sl[j][0].start+sl[j][0].stop)/2 for j in sec]
iyi=np.isfinite(mer).all(1); print('bant bulunan satir',iyi.mean().round(2))
hedef=np.median(mer[iyi],0); print('hedef',hedef.round(1))
yy=np.arange(H)
for j in range(NB): mer[:,j]=np.interp(yy,yy[iyi],ndimage.median_filter(mer[iyi,j],9))
O=np.zeros_like(I); xt=np.arange(W)+0.5
for y in range(H):
    xs=np.interp(xt,np.r_[0,hedef,W],np.r_[0,mer[y],W])
    for c in range(3): O[y,:,c]=np.interp(xs-0.5,np.arange(W),I[y,:,c])
Image.fromarray(O.clip(0,255).astype(np.uint8)).save('t_kapak.png')
np.save('kapak_bant.npy',hedef/W)

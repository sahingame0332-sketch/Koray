import numpy as np
from PIL import Image
from scipy import ndimage
z=np.load('ok_ornek2.npz'); Es,Bs,bads=z['E'],z['B'],z['bad']; K,Hc,Wc=Es.shape[:3]
V=~bads; Em=np.where(V[...,None],Es,np.nan)
med=np.nanmedian(Em,0)
# sekil: ok govdesi (yesil ya da krem artis)
sek=np.nan_to_num((med[...,1]>8)|(med.min(2)>20))
sek=ndimage.binary_closing(sek,np.ones((5,5))); sek=ndimage.binary_opening(sek,np.ones((3,3)))
l,n=ndimage.label(sek); s=ndimage.sum(sek,l,range(1,n+1)); sek=l==(1+np.argmax(s)); sek=ndimage.binary_fill_holes(sek)
sek=sek|sek[:,::-1]                       # simetri
krem=np.nan_to_num(med.min(2)>35)&sek; krem=ndimage.binary_opening(krem,np.ones((2,2)))
dolgu=sek&~ndimage.binary_dilation(krem,np.ones((3,3)))&ndimage.binary_erosion(sek,np.ones((9,9)))
# bolge basina ortak a: E = P - aB, P yavas degisir -> her pikselde ornek ortalamasindan sapmalar
def bolge_a(m):
    X=[];Y=[]
    for k in range(K):
        mk=m&V[k]
        X.append((Bs[k]-np.nanmean(np.where(V[...,None],Bs,np.nan),0))[mk]); Y.append((Es[k]-np.nanmean(Em,0))[mk])
    X=np.concatenate(X).ravel(); Y=np.concatenate(Y).ravel(); ok=np.isfinite(X)&np.isfinite(Y)
    return float(np.clip(-np.sum(X[ok]*Y[ok])/np.sum(X[ok]**2),0,1)), ok.sum()
a_d,nd=bolge_a(dolgu); a_k,nk=bolge_a(krem)
print('alfa dolgu',round(a_d,3),nd,'krem',round(a_k,3),nk)
np.save('ok_sekil.npy',np.stack([sek,krem,dolgu]))
np.save('ok_alfa.npy',np.array([a_d,a_k]))

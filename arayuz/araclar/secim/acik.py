import numpy as np, glob
from PIL import Image
from scipy import ndimage
fs=sorted(glob.glob('G/k_*.png'))
a=lambda i: np.asarray(Image.open(fs[i]).convert('RGB'),dtype=np.float32)
med=lambda r: np.median([a(i) for i in r],0)
p=np.load('rect.npy'); yh,s,a1,b1,a2,b2,r=p; cx=1356.
O=med(range(72,75)); B=med(range(76,80))
N=512; R=1.35*r
ty,tx=np.mgrid[0:N,0:N]+0.5
X=a1+(tx-N/2)/(N/2)*R; D=b1-(ty-N/2)/(N/2)*R
u=cx+X*s/D; v=yh+s/D
def samp(I): return np.stack([ndimage.map_coordinates(I[...,c],[v,u],order=1) for c in range(3)],-1)
Or,Br=samp(O),samp(B)
np.save('Or.npy',Or); np.save('Br.npy',Br); np.save('uv.npy',np.stack([u,v]))
Image.fromarray(np.concatenate([Or,Br,np.clip(Or-Br+128,0,255)],1).astype(np.uint8)).save('acik.png')

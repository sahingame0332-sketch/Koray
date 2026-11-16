import numpy as np
from PIL import Image
from scipy import ndimage
M=np.load('radyal_model.npy'); rc,A,P=M[:,0],M[:,1],M[:,2:]
res=np.load('res.npy'); bad=np.load('bad.npy'); N=512; c=N/2; K=1.35; px=N/2/K
yy,xx=np.mgrid[0:N,0:N]+0.5; r=np.hypot(xx-c,yy-c)/px; th=np.degrees(np.arctan2(-(yy-c),xx-c))
# 4x ust ornekleme ile radyal profil (kenar yumusak)
def prof(rr):
    a=np.interp(rr,rc,np.clip(A,0,1),left=0,right=0); p=np.stack([np.interp(rr,rc,np.clip(P[:,k],0,None),left=0,right=0) for k in range(3)],-1)
    return a,p
S=4; y4,x4=np.mgrid[0:N*S,0:N*S]+0.5; r4=np.hypot(x4/S-c,y4/S-c)/px
a4,p4=prof(r4); al=a4.reshape(N,S,N,S).mean((1,3)); rgb=p4.reshape(N,S,N,S,3).mean((1,3))
rgb=np.minimum(rgb,al[...,None]*255+np.where(al[...,None]<0.5,120,0))   # ince mor isima eklemeli kalabilir
# isaret sablonu (45 derece, sag ust): kalintinin pozitif, parlak kismi
win=(r>0.72)&(r<0.98)&(np.abs(((th-45.2)+180)%360-180)<13)&~bad
lum=res.mean(2); sab=np.where((win&(np.clip(res,0,None).max(2)>10))[...,None],np.clip(res,0,None),0)
sab=ndimage.gaussian_filter(sab,[0.5,0.5,0])
print('isaret pikseli',int((sab.max(2)>10).sum()))
def dondur(I,deg):
    return np.stack([ndimage.rotate(I[...,k],deg,reshape=False,order=1) for k in range(3)],-1)
isa=np.zeros_like(rgb)
for hedef in (45.2,165.2,285.2):
    isa+=dondur(sab,hedef-45.2)
rgb=np.clip(rgb+isa,0,255)
rgb=ndimage.gaussian_filter(rgb,[0.6,0.6,0]); al=ndimage.gaussian_filter(al,0.6)
Image.fromarray(np.dstack([rgb,al*255]).round().astype(np.uint8),'RGBA').save('halka_doku.png')
# gorunum: siyah/cim ustunde
B=np.load('Br.npy'); O=np.load('Or.npy')
rec=rgb+(1-al[...,None])*B
m=(r>0.6)&(r<1.2)&~bad
print('halka (gecerli) ort fark',round(float(np.abs(rec-O)[m].mean()),2))
Image.fromarray(np.clip(np.concatenate([O,rec,rgb+(1-al[...,None])*40],1),0,255).astype(np.uint8)).save('halka_kars.png')

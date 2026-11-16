import numpy as np
from PIL import Image
from scipy import ndimage
Or=np.load('Or.npy'); Br=np.load('Br.npy'); bad=np.load('bad.npy'); N=512; c=N/2; K=1.35; px=N/2/K
E=Or-Br; Es=E.sum(2)
def ridge(lo,hi):
    th=[];rr=[]
    for deg in np.arange(0,360,1.0):
        t=np.radians(deg); rs=np.arange(lo,hi,0.002)*px; x=c+rs*np.cos(t); y=c-rs*np.sin(t)
        if ndimage.map_coordinates(bad.astype(float),[y,x],order=0).any(): continue
        v=ndimage.map_coordinates(Es,[y,x],order=1); k=np.argmax(v)
        if 0<k<len(v)-1:
            d=(v[k-1]-v[k+1])/(2*(v[k-1]-2*v[k]+v[k+1])+1e-9); th.append(t); rr.append((rs[k]+d*0.002*px)/px)
    th=np.array(th); rr=np.array(rr)
    F=lambda t: np.stack([np.ones_like(t),np.cos(t),np.sin(t),np.cos(2*t),np.sin(2*t)],1)
    w=np.ones(len(th))
    for _ in range(5):
        cf=np.linalg.lstsq(F(th)*w[:,None],rr*w,rcond=None)[0]; e=np.abs(F(th)@cf-rr); w=1/np.maximum(e,0.004)
    print('ridge',lo,hi,len(th),np.round(cf,4),'rms',round(float(np.sqrt(np.median(e**2))),4))
    return lambda t: F(np.atleast_1d(t))@cf
Ro=ridge(0.9,1.1); Ri=ridge(0.72,0.88)
yy,xx=np.mgrid[0:N,0:N]+0.5; t=np.arctan2(-(yy-c),xx-c); r=np.hypot(xx-c,yy-c)/px
ro=Ro(t.ravel()).reshape(N,N); ri=Ri(t.ravel()).reshape(N,N)
RI=float(np.median(ri/ro))*1.0; print('ic/dis',RI)
# normalize: ri->RI, ro->1 ; disinda dis olcekle, icinde ic olcekle
rho=np.where(r>=ro, r/ro, np.where(r<=ri, r*RI/ri, RI+(r-ri)/(ro-ri)*(1-RI)))
step=0.004; bins=np.arange(0.5,1.3,step); A=[];P=[]
for b0 in bins:
    m=(rho>=b0)&(rho<b0+step)&~bad
    e=E[m]; bb=Br[m]; w=np.ones(len(e))
    if len(e)<20: A.append(0.0); P.append(np.zeros(3)); continue
    for it in range(6):
        bm=(bb*w[:,None]).sum(0)/w.sum(); em=(e*w[:,None]).sum(0)/w.sum()
        a=-(((bb-bm)*(e-em))*w[:,None]).sum()/max((((bb-bm)**2)*w[:,None]).sum(),1e-6)
        a=float(np.clip(a,0,1)); p=em+a*bm
        res=np.abs(e-(p-a*bb)).sum(1); w=1/np.maximum(res,3)
    A.append(a); P.append(p)
A=np.array(A); P=np.array(P); rc=bins+step/2
A=ndimage.gaussian_filter1d(A,0.7); P=ndimage.gaussian_filter1d(P,0.7,axis=0)
np.save('radyal_model.npy',np.concatenate([rc[:,None],A[:,None],P],1)); np.save('RI.npy',RI)
a_=np.interp(rho,rc,A,left=0,right=0); P_=np.stack([np.interp(rho,rc,P[:,k],left=0,right=0) for k in range(3)],-1)
pred=P_-a_[...,None]*Br; res=np.where(bad[...,None],0,E-pred)
print('ort |res| r 0.6-1.2:',float(np.abs(res)[(r>0.6)&(r<1.2)&~bad].mean()))
np.save('res.npy',res); np.save('rho.npy',rho)
Image.fromarray(np.concatenate([np.clip(Br+pred,0,255),Or,np.clip(res*2+128,0,255)],1).astype(np.uint8)).save('model.png')
for r0 in np.arange(0.70,1.16,0.02): i=np.argmin(abs(rc-r0)); print(round(r0,2), round(A[i],3), np.round(P[i],1))

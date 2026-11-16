import numpy as np
from scipy import optimize, ndimage
E1=np.load('E1.npy'); E2=np.load('E2.npy')
def pts(E,ylim):
    m=(E[...,0]>90)&(E[...,1]>60)&(E[...,2]<0.75*E[...,0])&(E[...,1]<=E[...,0]+5)
    m[:ylim]=False; m[1138:]=False
    m=ndimage.binary_opening(m,np.ones((3,3)))
    l,n=ndimage.label(m); s=ndimage.sum(m,l,range(1,n+1)); m=np.isin(l,1+np.where(s>300)[0])
    y,x=np.nonzero(m); return x.astype(float),y.astype(float)
P1=pts(E1,820); P2=pts(E2,960); cx=1356.
def g(yh,s,P): return (P[0]-cx)/(P[1]-yh), s/(P[1]-yh)
def res(p):
    yh,s,a1,b1,a2,b2,r=p; o=[]
    for P,(a,b) in ((P1,(a1,b1)),(P2,(a2,b2))):
        X,D=g(yh,s,P); o.append(np.hypot(X-a,D-b)/r-1)
    return np.concatenate(o)
best=None
for yh in [0,150,260,400,550]:
  for s in [300,700,1000,1500,2500]:
    X1,D1=g(yh,s,P1); X2,D2=g(yh,s,P2)
    p0=[yh,s,X1.mean(),D1.mean(),X2.mean(),D2.mean(),(X1.max()-X1.min())/2]
    try: r=optimize.least_squares(res,p0,loss='soft_l1',f_scale=0.03,bounds=([-2000,10,-5,-50,-5,-50,1e-3],[950,1e5,5,50,5,50,5]))
    except Exception as e: continue
    if best is None or r.cost<best.cost: best=r
yh,s=best.x[:2]; print('yh',yh,'s',s,'cost',best.cost,'med|res|',np.median(np.abs(best.fun)))
print(best.x)
np.save('rect.npy',best.x)

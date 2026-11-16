import numpy as np
from scipy import optimize, ndimage
from scipy.spatial import cKDTree
exec(open('rectfit.py').read().split('cx=1356.')[0])
cx=1356.
P1=(P1[0][::4],P1[1][::4]); P2=(P2[0][::2],P2[1][::2])
t=np.linspace(0,2*np.pi,720,endpoint=False)
def proj(yh,s,a,b,r):
    X=a+r*np.cos(t); D=b+r*np.sin(t); D=np.maximum(D,1e-6)
    return cx+X*s/D, yh+s/D
def res(p):
    yh,s,a1,b1,a2,b2,r=p; o=[]
    for P,(a,b) in ((P1,(a1,b1)),(P2,(a2,b2))):
        u,v=proj(yh,s,a,b,r); d,_=cKDTree(np.stack([u,v],1)).query(np.stack(P,1)); o.append(d)
    return np.concatenate(o)
best=None
for yh in [100,261,400]:
  for s in [600,1200,2000]:
    def g(P): return (P[0]-cx)/(P[1]-yh), s/(P[1]-yh)
    X1,D1=g((np.array([1307.]),np.array([983.]))); X2,D2=g((np.array([1175.]),np.array([1119.])))
    r0=150/(983-yh)
    p0=[yh,s,X1[0],D1[0],X2[0],D2[0],r0]
    r=optimize.least_squares(res,p0,loss='soft_l1',f_scale=6,x_scale='jac')
    print(yh,s,'->',np.round(r.x[:2],1),round(float(np.median(r.fun)),2))
    if best is None or r.cost<best.cost: best=r
print(best.x); np.save('rect.npy',best.x)

"""Kameralar sabit, oval kapakli sekil (D,HB,HL,us) siluet ortusmesiyle yeniden uydurulur."""
import numpy as np, json
from scipy import optimize
import uydur as U
J=json.load(open('uydu.json')); KAP=['g','a','b','f','d']
def f(x):
    sh=[x[0],x[1],x[2],x[3],0]
    return -np.mean([U.iou(sh,J['kam'][k],k) for k in KAP])
x0=np.array([J['sekil'][0],J['sekil'][1],J['sekil'][2],2.4])
for us in (2.0,2.4,3.0):
    x0[3]=us; print('us',us,-f(x0))
r=optimize.minimize(f,x0,method='Powell',options={'xtol':1e-3,'ftol':1e-6}); x=r.x
print('D HB HL us',x.round(3),'iou',-r.fun,[round(U.iou([*x,0],J['kam'][k],k),3) for k in KAP])
J['sekil']=[*map(float,x),0.0]; json.dump(J,open('uydu.json','w'))

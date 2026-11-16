import numpy as np,json
from scipy import optimize
import uydur as S
from nokta_uydur import noktalar
from geo import proj
x=np.concatenate([[0.876,0.386,0.377]]+[S.K[i] for i in (2,3,4)])
x0j=json.load(open('uydu_sil.json'))
x=np.concatenate([x0j['sekil']]+[x0j['kam'][str(i)] for i in (2,3,4)])
def nok(x):
    D,HB,HL=x[:3]; r=[]
    for k,(i,pp) in enumerate(noktalar(D,HB,HL).items()):
        P=x[3+6*k:9+6*k]; q=proj(np.array([p for p,_ in pp]),P)[:,:2]; r.append((q-np.array([o for _,o in pp])).ravel())
    return np.sqrt(np.mean(np.concatenate(r)**2))
def f(x):
    sil=np.mean([S.iou(x[:3],x[3+6*k:9+6*k],i) for k,i in enumerate((2,3,4))])
    return -sil+0.02*nok(x)
print('bas iou/nok',-f(x)-0, nok(x))
r=optimize.minimize(f,x,method='Powell',options={'maxiter':8000,'xtol':1e-3,'ftol':1e-6})
x=r.x
print('D HB HL',np.round(x[:3],3),'nokta rms',round(nok(x),2),'iou',[round(S.iou(x[:3],x[3+6*k:9+6*k],i),3) for k,i in enumerate((2,3,4))])
for k,i in enumerate((2,3,4)): print(i,np.round(np.degrees(x[3+6*k:6+6*k]),1),np.round(x[6+6*k:9+6*k],1))
json.dump({'sekil':list(x[:3]),'kam':{i:list(x[3+6*k:9+6*k]) for k,i in enumerate((2,3,4))}},open('uydu.json','w'))

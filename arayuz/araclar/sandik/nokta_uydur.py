import numpy as np,json
from scipy import optimize
from geo import proj
K={int(k):v for k,v in json.load(open('kam.json')).items()}
def noktalar(D,HB,HL):
    a=D/2
    return {2:[((0,HB,a),(792.5,535.8)),((1,HB,a),(868.3,510)),((1,0,a),(876.7,531.7)),((0,0,a),(802.5,558.3)),((0,HB,-a),(767.5,495.8))],
            3:[((1,HB,a),(728.3,585.2)),((1,HB,-a),(783.3,558.3)),((1,0,-a),(793.3,578.3)),((1,0,a),(735,606.7)),((1,HB+HL,0),(753,541.2))],
            4:[((1,HB,-a),(875.7,389.3)),((0,HB,-a),(937.9,389.3)),((0,0,-a),(938.5,410)),((1,0,-a),(881,410)),((0,0,a),(946,404)),((0,HB,a),(950,387))]}
if __name__=="__main__":
    def f(x):
        D,HB,HL=x[:3]; r=[]
        for k,(i,pp) in enumerate(noktalar(D,HB,HL).items()):
            P=x[3+6*k:9+6*k]; q=proj(np.array([p for p,_ in pp]),P)[:,:2]; r.append((q-np.array([o for _,o in pp])).ravel())
        return np.concatenate(r)
    x0=np.concatenate([[0.86,0.41,0.5]]+[K[i] for i in (2,3,4)])
    r=optimize.least_squares(f,x0)
    print('D HB HL',np.round(r.x[:3],3),'rms px',round(float(np.sqrt(np.mean(r.fun**2))),2)); print(np.round(r.fun.reshape(-1,2),1).tolist())
    for k,i in enumerate((2,3,4)): print(i,np.round(np.degrees(r.x[3+6*k:6+6*k]),1),np.round(r.x[6+6*k:9+6*k],1))
    json.dump({'sekil':list(r.x[:3]),'kam':{i:list(r.x[3+6*k:9+6*k]) for k,i in enumerate((2,3,4))}},open('uydu.json','w'))
    
import numpy as np,json
from PIL import Image, ImageDraw
from scipy import optimize
from mesh import sandik; from geo import proj
K={int(k):v for k,v in json.load(open('kam.json')).items()}
crop={2:(755,455,895,575),3:(670,500,805,620),4:(860,340,970,425)}
M={i:np.load('m%d.npy'%i) for i in crop}
def siluet(sh,P,boyut):
    D,HB,HL=sh; im=Image.new('L',boyut,0); dr=ImageDraw.Draw(im)
    for ad,T in sandik(1.0,D,HB,HL):
        for tri,_ in T:
            q=proj(np.array(tri),P); dr.polygon([(float(x),float(y)) for x,y,_ in q],fill=255)
    return np.asarray(im)>127
def iou(sh,P,i):
    x0,y0,x1,y1=crop[i]; P=list(P); P[4]-=x0; P[5]-=y0
    r=siluet(sh,P,(x1-x0,y1-y0)); m=M[i]; return (r&m).sum()/(r|m).sum()
if __name__=="__main__":
    x=np.concatenate([[0.88,0.41,0.38]]+[K[i] for i in (2,3,4)])
    def f(x):
        sh=x[:3]; return -np.mean([iou(sh,x[3+6*k:9+6*k],i) for k,i in enumerate((2,3,4))])
    print('baslangic',-f(x))
    sc=np.concatenate([[0.05,0.03,0.05]]+[[0.05,0.05,0.05,3,1.5,1.5]]*3)
    r=optimize.minimize(f,x,method='Powell',options={'maxiter':6000,'xtol':1e-3,'ftol':1e-5})
    print('son',-r.fun,'D HB HL',np.round(r.x[:3],3))
    for k,i in enumerate((2,3,4)): print(i,round(iou(r.x[:3],r.x[3+6*k:9+6*k],i),3),np.round(np.degrees(r.x[3+6*k:6+6*k]),1),np.round(r.x[6+6*k:9+6*k],1))
    json.dump({'sekil':list(r.x[:3]),'kam':{i:list(r.x[3+6*k:9+6*k]) for k,i in enumerate((2,3,4))}},open('uydu.json','w'))
    
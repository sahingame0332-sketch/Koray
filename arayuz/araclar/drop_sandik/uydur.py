"""Siluet uydurma: sekil (D,HB,HL,n; L=1) + her goruntu icin ortografik kamera. Calisma klasoru: kirp.json, m_*.npy"""
import numpy as np, json, sys
from PIL import Image, ImageDraw
from scipy import optimize
from mesh import sandik; from geo import proj
K=json.load(open('kirp.json')); KAP=[k for k in 'abdefg']
M={k:np.load('m_%s.npy'%k) for k in K}
def siluet(sh,P,boyut,acik=False,aci=0):
    D,HB,HL,n=sh; im=Image.new('L',boyut,0); dr=ImageDraw.Draw(im)
    for ad,T in sandik(1.0,D,HB,HL,n,acik,aci):
        for tri,_ in T:
            q=proj(np.array(tri),P); dr.polygon([(float(x),float(y)) for x,y,_ in q],fill=255)
    return np.asarray(im)>127
def iou(sh,P,k,acik=False,aci=0):
    m=M[k]; r=siluet(sh,P,(m.shape[1],m.shape[0]),acik,aci); return (r&m).sum()/(r|m).sum()
def ilk_kamera(sh,k,acik=False,aci=0):
    m=M[k]; ys,xs=np.nonzero(m); cx,cy=xs.mean(),ys.mean(); w=np.ptp(xs)
    best=(-1,None)
    for yaw in np.radians(np.arange(-180,180,20)):
        for pitch in np.radians([10,25,40,55,70]):
            for roll in np.radians([-30,0,30]):
                P=[yaw,pitch,roll,1,0,0]; q=proj(np.array([[0,0,0],[1,0,0],[0,.6,0],[1,.6,0],[0,0,.8],[1,0,.8]])-[.5,.3,.4],P)
                s=w/max(np.ptp(q[:,0]),1e-3); P=[yaw,pitch,roll,s,cx,cy]
                c=proj(np.array([[0.5,0.35,0]]),P)[0]; P[4]+=cx-c[0]; P[5]+=cy-c[1]
                v=iou(sh,P,k,acik,aci)
                if v>best[0]: best=(v,P)
    P=best[1]
    r=optimize.minimize(lambda P:-iou(sh,P,k,acik,aci),P,method='Powell',options={'xtol':1e-3,'ftol':1e-5,'maxiter':3000})
    return list(r.x),-r.fun
if __name__=="__main__":
    sh=[0.85,0.39,0.41,2.0]; kam={}
    for k in KAP:
        kam[k],v=ilk_kamera(sh,k); print(k,round(v,3),np.round(np.degrees(kam[k][:3]),1),flush=True)
    x=np.concatenate([sh]+[kam[k] for k in KAP])
    f=lambda x:-np.mean([iou(x[:4],x[4+6*j:10+6*j],k) for j,k in enumerate(KAP)])
    for tur in range(2):
        r=optimize.minimize(f,x,method='Powell',options={'maxiter':20000,'xtol':1e-3,'ftol':1e-6}); x=r.x
        print('tur',tur,-r.fun,'D HB HL n',np.round(x[:4],3),flush=True)
    for j,k in enumerate(KAP): print(k,round(iou(x[:4],x[4+6*j:10+6*j],k),3),np.round(np.degrees(x[4+6*j:7+6*j]),1),np.round(x[7+6*j:10+6*j],1))
    json.dump({'sekil':list(x[:4]),'kam':{k:list(x[4+6*j:10+6*j]) for j,k in enumerate(KAP)}},open('uydu.json','w'))

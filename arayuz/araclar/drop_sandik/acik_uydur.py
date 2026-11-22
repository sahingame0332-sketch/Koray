"""Acik sandik (gorunum c): kamera + kapak acisi. Kapak on-taban kenari mentese (y=HB, z=-a) etrafinda doner."""
import numpy as np, json
from scipy import optimize
from PIL import Image, ImageDraw
from geo import proj
from mesh import sandik
U=json.load(open('uydu.json')); D,HB,HL,h1,c=U['sekil']; a=D/2; n=(h1,c)
K=json.load(open('kirp.json')); M=np.load('m_c.npy'); i,(x0,y0,x1,y1)=K['c']
def noktalar(aci,ters):
    s,co=np.sin(aci),np.cos(aci); lf=lambda x:(x,HB+2*a*s,-a+2*a*co)
    X0,X1=(1,0) if ters else (0,1)
    return [(X0,HB,a),(X1,HB,a),(X1,HB,-a),(X0,HB,-a),(X0,0,a),(X1,0,a),lf(X1),lf(X0)]
OBS=np.array([(860,387),(957,282),(852,232),(757,332),(872,432),(965,380),(757,127),(647,232)],float)
def iou(P,aci):
    im=Image.new('L',(M.shape[1],M.shape[0]),0); dr=ImageDraw.Draw(im); P=list(P); P[4]-=x0; P[5]-=y0
    for ad,T in sandik(1.0,D,HB,HL,n,True,aci):
        for tri,_ in T:
            q=proj(np.array(tri),P); dr.polygon([(float(x),float(y)) for x,y,_ in q],fill=255)
    r=np.asarray(im)>127; return (r&M).sum()/(r|M).sum()
best=None
for ters in (False,True):
    for y0_ in np.radians(np.arange(-180,180,30)):
        for p0 in np.radians([20,40,60,75]):
            for ac in np.radians([100,130,160]):
                f=lambda Q:(proj(np.array(noktalar(Q[6],ters)),Q[:6])[:,:2]-OBS).ravel()
                r=optimize.least_squares(f,[y0_,p0,0,180,860,300,ac],bounds=([-7,0,-0.9,20,0,0,1.2],[7,1.55,0.9,2000,3000,3000,3.2]))
                if best is None or r.cost<best[0].cost: best=(r,ters)
r,ters=best; Q=r.x; print('ters',ters,'rms',np.sqrt(np.mean(r.fun**2)).round(2),'acilar',np.degrees(Q[:3]).round(1),'kapak',np.degrees(Q[6]).round(1))
f2=lambda Q:-iou(Q[:6],Q[6])+0.01*np.sqrt(np.mean((proj(np.array(noktalar(Q[6],ters)),Q[:6])[:,:2]-OBS)**2))
r2=optimize.minimize(f2,Q,method='Powell',options={'xtol':1e-3,'ftol':1e-5,'maxiter':4000}); Q=r2.x
print('iou',round(iou(Q[:6],Q[6]),3),'kapak',np.degrees(Q[6]).round(1),'acilar',np.degrees(Q[:3]).round(1))
U['kam']['c']=list(Q[:6]); U['aci']=float(Q[6]); U['acik_ters']=bool(ters); json.dump(U,open('uydu.json','w'))

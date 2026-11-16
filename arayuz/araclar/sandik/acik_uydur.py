import numpy as np,json
from PIL import Image, ImageDraw
from scipy import optimize
from mesh import sandik; from geo import proj, kamera
U=json.load(open('uydu.json')); D,HB,HL=U['sekil']; a=D/2
P0,e=kamera([(0,HB,-a),(1,HB,-a),(1,HB,a),(0,HB,a)],[(850,664),(912,701),(860,773),(794,720)],(75,855,715))
print('s1 kamera',np.round(np.degrees(P0[:3]),1),np.round(P0[3:],1),'hata',round(e,2))
x0,y0,x1,y1=(780,590,960,800)
m=np.load('m1.npy'); 
# s1 maskesinde sari cim parcalari: kenardaki ince seyleri at
from scipy import ndimage
m=ndimage.binary_opening(m,np.ones((7,7)))
def sil(P,aci):
    P=list(P); P[4]-=x0; P[5]-=y0
    im=Image.new('L',(x1-x0,y1-y0),0); dr=ImageDraw.Draw(im)
    for ad,T in sandik(1.0,D,HB,HL,acik=True,aci=aci):
        for tri,_ in T:
            q=proj(np.array(tri),P); dr.polygon([(float(x),float(y)) for x,y,_ in q],fill=255)
    return np.asarray(im)>127
def f(x):
    r=sil(x[1:],x[0]); return -(r&m).sum()/(r|m).sum()
best=None
for ac in np.radians([90,100,110,120,130]):
    r=optimize.minimize(f,np.concatenate([[ac],P0]),method='Powell',options={'maxiter':3000,'xtol':1e-3,'ftol':1e-5})
    print(round(np.degrees(r.x[0]),1),round(-r.fun,3))
    if best is None or r.fun<best.fun: best=r
print('aci',np.degrees(best.x[0]),'iou',-best.fun, np.round(np.degrees(best.x[1:4]),1), np.round(best.x[4:],1))
json.dump({'aci':best.x[0],'kam':list(best.x[1:])},open('acik.json','w'))
np.save('m1t.npy',m)

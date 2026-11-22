"""Nokta + siluet ortak uydurma: sekil (D,HB,HL,h1,c; L=1) + her goruntu icin ortografik kamera.
Calisma klasoru: kirp.json, m_*.npy. Noktalar goruntu pikseli (tam kare koordinati)."""
import numpy as np, json
from PIL import Image, ImageDraw
from scipy import optimize
from mesh import sandik; from geo import proj
K=json.load(open('kirp.json')); M={k:np.load('m_%s.npy'%k) for k in K}
# model noktalari: x 0..1 (onden bakinca soldan saga), y yukari, z +on (kilitli yuz)
def NOK(D,HB,HL):
    a=D/2
    return {'F00':(0,0,a),'F10':(1,0,a),'F01':(0,HB,a),'F11':(1,HB,a),
            'B00':(0,0,-a),'B10':(1,0,-a),'B01':(0,HB,-a),'B11':(1,HB,-a),'K':(0.5,HB*0.42,a),'A1':(1,HB+HL,0)}
P2={'g':{'F00':(675,740),'F10':(794,733),'F01':(667,681),'F11':(799,675),'B10':(805,728),'K':(737,713)},
    'a':{'F01':(789,156),'F11':(960,155),'F00':(811,221),'F10':(957,217),'K':(886,196)},
    'b':{'F01':(528,622),'F11':(728,623),'F00':(565,663),'F10':(730,658),'K':(643,645)},
    'f':{'B11':(1579,820),'B01':(1737,821),'B10':(1584,887),'B00':(1730,893),'F10':(1562,868),'A1':(1565,738)},
    'd':{'F00':(1550,555),'B00':(1675,612),'F01':(1568,512),'B01':(1705,570)}}
KAP=list(P2)
def siluet(sh,P,boyut):
    im=Image.new('L',boyut,0); dr=ImageDraw.Draw(im)
    for ad,T in sandik(1.0,sh[0],sh[1],sh[2],(sh[3],sh[4])):
        for tri,_ in T:
            q=proj(np.array(tri),P); dr.polygon([(float(x),float(y)) for x,y,_ in q],fill=255)
    return np.asarray(im)>127
def iou(sh,P,k):
    i,(x0,y0,x1,y1)=K[k]; m=M[k]; P=list(P); P[4]-=x0; P[5]-=y0
    r=siluet(sh,P,(m.shape[1],m.shape[0])); return (r&m).sum()/(r|m).sum()
def nok_hata(sh,P,k):
    N=NOK(*sh[:3]); ad=list(P2[k]); q=proj(np.array([N[a] for a in ad]),P)[:,:2]
    return q-np.array([P2[k][a] for a in ad])
def kamera(sh,k):
    best=None; ad=list(P2[k]); obs=np.array([P2[k][a] for a in ad],float); c=obs.mean(0)
    for y0 in np.radians(np.arange(-180,180,30)):
        for p0 in np.radians([10,30,50,70]):
            for r0 in np.radians([-30,0,30]):
                r=optimize.least_squares(lambda P:nok_hata(sh,P,k).ravel(),[y0,p0,r0,150,c[0],c[1]])
                if best is None or r.cost<best.cost: best=r
    return best.x
if __name__=="__main__":
    sh=np.array([0.80,0.36,0.40,0.35,0.55])
    kam={k:kamera(sh,k) for k in KAP}
    for k in KAP: print(k,'nokta rms',np.sqrt(np.mean(nok_hata(sh,kam[k],k)**2)).round(2),'iou',round(iou(sh,kam[k],k),3),np.round(np.degrees(kam[k][:3]),1),flush=True)
    x=np.concatenate([sh]+[kam[k] for k in KAP])
    def f(x):
        sh=x[:5]; t=0
        for j,k in enumerate(KAP):
            P=x[5+6*j:11+6*j]; t+=-iou(sh,P,k)+0.01*np.sqrt(np.mean(nok_hata(sh,P,k)**2))
        return t/len(KAP)
    print('bas',f(x),flush=True)
    for tur in range(3):
        r=optimize.minimize(f,x,method='Powell',options={'maxiter':30000,'xtol':1e-4,'ftol':1e-7}); x=r.x
        print('tur',tur,r.fun,'D HB HL h1 c',np.round(x[:5],3),flush=True)
    for j,k in enumerate(KAP):
        P=x[5+6*j:11+6*j]; print(k,'iou',round(iou(x[:5],P,k),3),'nokta',np.sqrt(np.mean(nok_hata(x[:5],P,k)**2)).round(2),np.round(np.degrees(P[:3]),1),np.round(P[3:],1))
    json.dump({'sekil':list(x[:5]),'kam':{k:list(x[5+6*j:11+6*j]) for j,k in enumerate(KAP)}},open('uydu.json','w'))

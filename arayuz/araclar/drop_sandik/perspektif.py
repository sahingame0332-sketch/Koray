"""Oyun kamerasi gibi igne delikli (perspektif) kamera: ortografik uydurmadan baslar, ortak odak F ve her goruntu
icin poz (yaw,pitch,roll,TX,TY,TZ) siluet + nokta amaciyla uydurulur. Asal nokta ekran merkezi."""
import numpy as np, json, sys
from scipy import optimize
import uydur as U
from geo import ort2pin
J=json.load(open('uydu.json')); sh=J['sekil']; KAP=['g','a','b','f','d']
CX,CY=2266/2,1488/2
def poz(k,F):
    P0=ort2pin(J['kam'][k],F,CX,CY); x=np.array(P0[:6])
    f=lambda x:U.amac(sh,[*x,F,CX,CY],k)
    r=optimize.minimize(f,x,method='Powell',options={'xtol':1e-3,'ftol':1e-6,'maxiter':6000})
    return [*r.x,F,CX,CY],r.fun
sonuc={}
for F in [float(v) for v in sys.argv[1:]] or [1100.,1500.,2200.,4000.]:
    kam={}; top=0
    for k in KAP: kam[k],v=poz(k,F); top+=v
    print('F',F,'ort amac',round(top/len(KAP),4),[round(U.iou(sh,kam[k],k),3) for k in KAP],flush=True)
    sonuc[F]=(top,kam)
F=min(sonuc,key=lambda f:sonuc[f][0]); print('secilen F',F)
J2=dict(J); J2['kam']=dict(J['kam']); J2['kam'].update(sonuc[F][1]); J2['F']=F; J2['kam_orto']=J['kam']
json.dump(J2,open('uydu_p.json','w'))

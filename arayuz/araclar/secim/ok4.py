import numpy as np, glob
from PIL import Image
from scipy import ndimage
from zemin import *
fs=sorted(glob.glob('G/k_*.png'))
a=lambda i: np.asarray(Image.open(fs[i]).convert('RGB'),dtype=np.float32)
med=lambda r: np.median([a(i) for i in r],0)
B200=med(range(196,201))
ORN=[("stab",med(range(136,140)),med(range(141,146)),(1330,850)),
     ("stroke",med(range(72,76)),med(range(76,80)),(1330,830)),
     ("s220",a(220),B200,(1300,840)),("s228",a(228),B200,(1320,835)),("s231",a(231),B200,(1320,835))]
W=H=360; out=[]
for ad,O,B,C in ORN:
    Or,_,_=ac(O,C,W,H); Br,_,_=ac(B,C,W,H); E=Or-Br
    etk=(Or[...,0]>150)&(Or[...,0]-Or[...,1]>70)|(Br[...,0]>150)&(Br[...,0]-Br[...,1]>70)
    _,uu,vv=ac(O,C,W,H); Xg,Dg=zemine(uu,vv); p=np.load('rect.npy'); rr=np.hypot(Xg-p[2],Dg-p[3])/p[6]
    hal=((rr>0.6)&(rr<1.3)) if ad=='stroke' else np.zeros_like(rr,bool)
    _hal=(E[...,0]>100)&(E[...,2]<0.75*E[...,0])&(E[...,1]>60)&(E[...,1]<=E[...,0]+5)   # secim halkasi (stroke)
    kar=((E[...,2]>E[...,1]+8)&(E.max(2)>20))|(E.min(2)<-18)
    bad=ndimage.binary_dilation(etk,np.ones((5,5)))|ndimage.binary_dilation(ndimage.binary_opening(kar,np.ones((2,2))),np.ones((5,5)))|hal
    np.savez('orn_%s.npz'%ad,E=E,B=Br,bad=bad)
    v=np.clip(E+128,0,255).astype(np.uint8); v[bad]=[255,0,255]; out.append(v)
Image.fromarray(np.concatenate(out,1)).resize((5*300,300)).save('orn.png')

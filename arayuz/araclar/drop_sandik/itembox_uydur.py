"""ItemBox 360 kaydindan (48 kare, 7.5 derece/kare) sekil: kutu govde + super-elips kapak; igne delikli kamera
(egim, uzaklik, odak) + donus baslangici, siluet ortusmesiyle. -> itembox.json"""
import numpy as np, json, glob
from PIL import Image, ImageDraw
from scipy import ndimage, optimize
from mesh import sandik; from geo import proj
bg=np.array([24,32,42.])
def maske(i):
    f=np.asarray(Image.open('ib_%02d.png'%i).convert('RGB'),float); m=np.zeros(f.shape[:2],bool)
    a=f[60:392]; mm=(np.abs(a-bg).sum(-1)>30)&(a[...,0]-a[...,2]>-4)
    mm=ndimage.binary_opening(mm,np.ones((3,3))); l,n=ndimage.label(mm); s=ndimage.sum(mm,l,range(1,n+1)); mm=l==1+np.argmax(s)
    m[60:392]=ndimage.binary_fill_holes(ndimage.binary_closing(mm,np.ones((5,5)))); return m
KARE=[43,1,7,13,19,25,31,37]
M={i:maske(i) for i in KARE}
def kam(x,i):
    yaw0,pitch,TZ,F,cx,cy,ty=x[5:12]
    yaw=yaw0+np.radians(7.5)*((i-43)%48)
    return [yaw,pitch,0,0,ty,TZ,F,cx,cy]
def siluet(sh,P,boyut):
    im=Image.new('L',boyut,0); dr=ImageDraw.Draw(im)
    for ad,T in sandik(1.0,sh[0],sh[1],sh[2],(sh[3],0),o=sh[4]):
        for tri,_ in T:
            q=proj(np.array(tri)-[0.5,0,0],P); dr.polygon([(float(a),float(b)) for a,b,_ in q],fill=255)
    return np.asarray(im)>127
def iou(x,i):
    r=siluet(x[:5],kam(x,i),(420,430)); m=M[i]; return (r&m).sum()/(r|m).sum()
def f(x): return -np.mean([iou(x,i) for i in KARE])
if __name__=="__main__":
    # baslangic: on kare 43 -> yaw ~0 (kilit kameraya)
    x0=json.load(open('itembox.json'))['x']; x=np.array(x0[:3]+[2.3,0.06]+x0[4:])
    r=optimize.minimize(f,x,method='Powell',options={'maxiter':20000,'xtol':1e-4,'ftol':1e-7}); x=r.x
    r=optimize.minimize(f,x,method='Powell',options={'maxiter':20000,'xtol':1e-4,'ftol':1e-7}); x=r.x
    print('iou',-r.fun,[round(iou(x,i),3) for i in KARE])
    print('D HB HL us o',x[:5].round(3),'yaw0',np.degrees(x[5]).round(1),'egim',np.degrees(x[6]).round(1),'TZ F',x[7:9].round(1),'c',x[9:12].round(1))
    json.dump({'x':list(map(float,x)),'sekil':list(map(float,x[:5]))},open('itembox.json','w'))

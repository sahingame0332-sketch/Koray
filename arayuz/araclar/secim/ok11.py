import numpy as np
from scipy import ndimage
z=np.load('ok_ornek2.npz'); Es,Bs,bads=z['E'],z['B'],z['bad']; K,Hc,Wc=Es.shape[:3]; V=~bads
x0,y0,w,h,cx,yuc,Yb,Yalt,hb,sw,t,_,_=np.load('ok_meta.npy')
from PIL import Image, ImageDraw
S=4; im=Image.new('L',(Wc*S,Hc*S),0)
ImageDraw.Draw(im).polygon([(x*S,y*S) for x,y in [(cx,yuc),(cx+hb,Yb),(cx+sw,Yb),(cx+sw,Yalt),(cx-sw,Yalt),(cx-sw,Yb),(cx-hb,Yb)]],fill=255)
dt=(ndimage.distance_transform_edt(np.asarray(im)>127)/S)[S//2::S,S//2::S]
icb=dt>t+2.5; krb=(dt>2.5)&(dt<t-2.5)
def reg(m):
    # E_k = P(x) - a B_k  -> ornekler arasi sapmalarla a
    Bm=np.where(V[...,None],Bs,np.nan); Em=np.where(V[...,None],Es,np.nan)
    dB=(Bm-np.nanmean(Bm,0))[:,m]; dE=(Em-np.nanmean(Em,0))[:,m]
    ok=np.isfinite(dB)&np.isfinite(dE)&(np.isfinite(Bm[:,m]).sum(0)>=3)[None]
    return float(-np.sum(dB[ok]*dE[ok])/max(np.sum(dB[ok]**2),1e-6)), int(ok.sum())
for nm,M in (('dolgu',icb),('krem',krb)):
    for ya,yb_ in ((40,90),(90,130),(130,170),(170,210),(210,252)):
        m=M.copy(); m[:ya]=False; m[yb_:]=False
        if m.sum()<30: continue
        print(nm,ya,yb_,reg(m))
print('--- ince')
ys=[];As=[];Ws=[]
for ya in range(60,250,12):
    m=icb.copy(); m[:ya]=False; m[ya+12:]=False
    if m.sum()<30: continue
    a,n=reg(m); ys.append(ya+6); As.append(a); Ws.append(n); print(ya+6,round(a,3),n)
ka=[]
for ya in range(40,250,15):
    m=krb.copy(); m[:ya]=False; m[ya+15:]=False
    if m.sum()<30: continue
    a,n=reg(m); ka.append(a); print('krem',ya,round(a,3),n)
np.save('ok_alfa_satir.npy',np.array([ys,As,Ws]))

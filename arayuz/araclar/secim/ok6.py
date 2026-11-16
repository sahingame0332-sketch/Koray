import numpy as np
from PIL import Image
from scipy import ndimage
# doku pikselinde elle olculen noktalar: uc, iki kanat (diken) ucu
KP={"stab":[(137.5,275),(111,149),(246,202.5)],"s220":[(117.5,257.5),(137.5,135),(249,220)],"s228":[(92.5,267.5),(107.5,142.5),(222.5,230)]}
# kanonik (y yukari, ok yukari bakar): uc (0,107), kanatlar (+-72.6,0); kanonik doku: Wc x Hc, merkez kanat ortasi
Wc,Hc=200,280; OX,OY=100,150     # kanat ortasinin doku yeri (y asagi)
def sim(src,dst):
    A=[];b=[]
    for (x,y),(u,v) in zip(src,dst): A+= [[x,-y,1,0],[y,x,0,1]]; b+=[u,v]
    p=np.linalg.lstsq(np.array(A,float),np.array(b,float),rcond=None)[0]; return p
CAN=None
ornek=[]
for ad,(T,L,R) in KP.items():
    T,L,R=map(np.array,(T,L,R)); M=(L+R)/2
    # sol/sag: uc yonune gore capraz carpim
    d=T-M; 
    if d[0]*(L-M)[1]-d[1]*(L-M)[0] < 0: L,R=R,L
    h=np.linalg.norm(d); w=np.linalg.norm(R-L)/2
    print(ad,'uc boyu',round(h,1),'yari genislik',round(w,1))
    if CAN is None: CAN=(h,w)
    h,w=CAN
    # kanonik (doku, y asagi) noktalari: uc (OX, OY-h), sol kanat (OX-w,OY), sag (OX+w,OY)
    dst=[(OX,OY-h),(OX-w,OY),(OX+w,OY)]
    # kanonik -> kaynak benzerlik
    best=None
    for LL,RR in ((L,R),(R,L)):
        p=sim(dst,[tuple(T),tuple(LL),tuple(RR)])
        e=sum(np.hypot(p[0]*a-p[1]*b+p[2]-c,p[1]*a+p[0]*b+p[3]-d) for (a,b),(c,d) in zip(dst,[T,LL,RR]))
        if best is None or e<best[0]: best=(e,p)
    p=best[1]; print('  hiza artigi',round(best[0],2),'olcek',round(np.hypot(p[0],p[1]),3))
    ty,tx=np.mgrid[0:Hc,0:Wc]+0.5
    sx=p[0]*tx-p[1]*ty+p[2]; sy=p[1]*tx+p[0]*ty+p[3]
    z=np.load('orn_%s.npz'%ad)
    g=lambda I,o=1: np.stack([ndimage.map_coordinates(I[...,c],[sy,sx],order=o,cval=0) for c in range(I.shape[2])],-1)
    E=g(z['E']); B=g(z['B']); bad=g(z['bad'][...,None].astype(float),0)[...,0]>0.5
    ornek.append((E,B,bad)); ornek.append((E[:,::-1],B[:,::-1],bad[:,::-1]))   # ayna
np.save('ok_kanon.npy',np.array([[OX,OY,CAN[0],CAN[1]]]))
Es=np.stack([o[0] for o in ornek]); Bs=np.stack([o[1] for o in ornek]); bads=np.stack([o[2] for o in ornek])
np.savez('ok_ornek.npz',E=Es,B=Bs,bad=bads)
gec=(~bads).sum(0); print('kapsanmayan piksel (ok govdesi icinde sonra bakilacak):',int((gec==0).sum()))
Em=np.where(bads[...,None],np.nan,Es); med=np.nanmedian(Em,0)
v=np.clip(np.nan_to_num(med,nan=-128)+128,0,255).astype(np.uint8)
row=np.concatenate([np.clip(np.where(b[...,None],-128,e)+128,0,255).astype(np.uint8) for e,_,b in ornek],1)
Image.fromarray(np.concatenate([row,np.concatenate([v]+[np.zeros_like(v)]*5,1)],0)).save('kanon.png')

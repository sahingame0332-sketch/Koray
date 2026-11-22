import numpy as np
from geo import R, proj
def ciz(S,dokular,P,boyut,arka=None):
    """S: [(doku,[(3 nokta,3 uv)])], P kamera (yaw,pitch,roll,s,tx,ty); orthografik; z-buffer"""
    Wd,Hd=boyut; img=np.zeros((Hd,Wd,4),np.float32) if arka is None else np.dstack([arka,np.full(arka.shape[:2],255.)]).astype(np.float32)
    zb=np.full((Hd,Wd),-1e9); Rm=R(P[0],P[1],P[2])
    for ad,T in S:
        tex=dokular[ad]; th,tw=tex.shape[:2]
        for tri,uv in T:
            pq=proj(np.array(tri,float),P); X,Y,Z=pq[:,0],pq[:,1],pq[:,2]
            ar=(X[1]-X[0])*(Y[2]-Y[0])-(X[2]-X[0])*(Y[1]-Y[0])
            if ar*np.sign(P[3])>=0 if False else abs(ar)<1e-9: continue
            pass                                     # ayiklama yok: z-tampon yeterli (kapali govde)
            x0,x1=int(max(0,np.floor(X.min()))),int(min(Wd-1,np.ceil(X.max()))); y0,y1=int(max(0,np.floor(Y.min()))),int(min(Hd-1,np.ceil(Y.max())))
            if x1<x0 or y1<y0: continue
            yy,xx=np.mgrid[y0:y1+1,x0:x1+1]+0.5
            w0=((X[1]-xx)*(Y[2]-yy)-(X[2]-xx)*(Y[1]-yy))/ar; w1=((X[2]-xx)*(Y[0]-yy)-(X[0]-xx)*(Y[2]-yy))/ar; w2=1-w0-w1
            m=(w0>=-1e-4)&(w1>=-1e-4)&(w2>=-1e-4)
            z=w0*Z[0]+w1*Z[1]+w2*Z[2]; sub=zb[y0:y1+1,x0:x1+1]; m&=z>sub
            if not m.any(): continue
            u=w0*uv[0][0]+w1*uv[1][0]+w2*uv[2][0]; v=w0*uv[0][1]+w1*uv[1][1]+w2*uv[2][1]
            tx=np.clip(u*(tw-1),0,tw-1).astype(int); ty=np.clip((1-v)*(th-1),0,th-1).astype(int)
            c=tex[ty,tx]; al=c[...,3:4]/255.
            m&=al[...,0]>0.5
            reg=img[y0:y1+1,x0:x1+1]
            reg[m,:3]=c[m,:3]; reg[m,3]=255; sub[m]=z[m]
    return img

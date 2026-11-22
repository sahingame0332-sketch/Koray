import numpy as np
from scipy import optimize
L,D,HB,HL=1.0,0.86,0.41,0.58
a=D/2
def R(yaw,pitch,roll):
    cy,sy=np.cos(yaw),np.sin(yaw); cp,sp=np.cos(pitch),np.sin(pitch); cr,sr=np.cos(roll),np.sin(roll)
    Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]); Rx=np.array([[1,0,0],[0,cp,-sp],[0,sp,cp]]); Rz=np.array([[cr,-sr,0],[sr,cr,0],[0,0,1]])
    return Rz@Rx@Ry
def proj(p,P):
    yaw,pitch,roll,s,tx,ty=P; q=(R(yaw,pitch,roll)@np.asarray(p,float).T).T
    return np.stack([tx+s*q[:,0], ty-s*q[:,1], q[:,2]],1)   # z: kameraya dogru (+ yakin)
def kamera(P3,P2,ilk):
    f=lambda P: (proj(P3,P)[:,:2]-np.asarray(P2)).ravel()
    best=None
    for y0 in np.radians(np.arange(-180,180,30)):
        for p0 in np.radians([15,35,55]):
            r=optimize.least_squares(f,[y0,p0,0,ilk[0],ilk[1],ilk[2]])
            if r.x[1]>0 and r.x[1]<1.5 and (best is None or r.cost<best.cost): best=r
    return best.x, np.sqrt(np.mean(best.fun**2))
# koseler (x 0..L soldan, y yukari, z +on): on yuz = z=+a, arka z=-a, uc x=0 (sol uc) / x=L
ON=[(0,HB,a),(L,HB,a),(L,0,a),(0,0,a)]
ARKA=[(L,HB,-a),(0,HB,-a),(0,0,-a),(L,0,-a)]        # arkadan bakinca sol-ust = x=L
UC0=[(0,HB,-a),(0,HB,a),(0,0,a),(0,0,-a)]          # x=0 ucu, disaridan bakinca sol = arka
UC1=[(L,HB,a),(L,HB,-a),(L,0,-a),(L,0,a)]

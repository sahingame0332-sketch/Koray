import numpy as np
from scipy import optimize
def R(yaw,pitch,roll):
    cy,sy=np.cos(yaw),np.sin(yaw); cp,sp=np.cos(pitch),np.sin(pitch); cr,sr=np.cos(roll),np.sin(roll)
    Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]); Rx=np.array([[1,0,0],[0,cp,-sp],[0,sp,cp]]); Rz=np.array([[cr,-sr,0],[sr,cr,0],[0,0,1]])
    return Rz@Rx@Ry
def proj(p,P):
    """P 6'li: ortografik (yaw,pitch,roll,s,tx,ty).
    P 9'lu: igne delikli (yaw,pitch,roll,TX,TY,TZ,F,cx,cy): q=R p + (TX,TY,0); derinlik Z=TZ-q_z;
    x=cx+F*q_x/Z, y=cy-F*q_y/Z. Donen 3. sutun: kameraya yakinlik (buyuk = yakin)."""
    q=(R(P[0],P[1],P[2])@np.asarray(p,float).T).T
    if len(P)==6: return np.stack([P[4]+P[3]*q[:,0], P[5]-P[3]*q[:,1], q[:,2]],1)
    Z=P[5]-q[:,2]; return np.stack([P[7]+P[6]*(q[:,0]+P[3])/Z, P[8]-P[6]*(q[:,1]+P[4])/Z, -Z],1)
def kaydir(P,x0,y0):
    P=list(P)
    if len(P)==6: P[4]-=x0; P[5]-=y0
    else: P[7]-=x0; P[8]-=y0
    return P
def ort2pin(P,F,cx,cy,TZ=None):
    """ortografik -> igne delikli baslangic: ayni olcek modelin merkezinde"""
    yaw,pitch,roll,s,tx,ty=P; TZ=TZ or F/s
    return [yaw,pitch,roll,(tx-cx)*TZ/F,(cy-ty)*TZ/F,TZ,F,cx,cy]

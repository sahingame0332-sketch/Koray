import numpy as np
N=24
def kubbe(L,D,HB,HL,ic=False):
    a=D/2; T=[]
    for k in range(N):
        p0,p1=np.pi*k/N,np.pi*(k+1)/N
        e=0.012 if ic else 0.0                       # ic yuzey: kalinlik kadar iceride (z catismasi olmasin)
        P=lambda x,p:(x,HB+(HL-e)*np.sin(p),(a-e)*np.cos(p))
        q=[P(0,p0),P(L,p0),P(L,p1),P(0,p1)]; uv=[(0,k/N),(1,k/N),(1,(k+1)/N),(0,(k+1)/N)]
        tri=[(0,1,2),(0,2,3)] if not ic else [(0,2,1),(0,3,2)]
        for t in tri: T.append(([q[i] for i in t],[uv[i] for i in t]))
    return T
def kapak_uc(L,D,HB,HL,x,sol_on):
    """kemer kapagi (x=0 ya da L): yelpaze; uv t_uc: u = (z on->arka) , v alttan"""
    a=D/2; H=HB+HL; T=[]; c=(x,HB,0.0)
    for k in range(N):
        p0,p1=np.pi*k/N,np.pi*(k+1)/N
        A=(x,HB+HL*np.sin(p0),a*np.cos(p0)); B=(x,HB+HL*np.sin(p1),a*np.cos(p1))
        f=lambda p:((a-p[2])/D if sol_on else (p[2]+a)/D, p[1]/H)
        tri=[c,A,B] if x>0 else [c,B,A]
        T.append((tri,[f(p) for p in tri]))
    return T
def kutu_yuz(q,uv=((0,1),(1,1),(1,0),(0,0))):
    return [([q[0],q[1],q[2]],[uv[0],uv[1],uv[2]]),([q[0],q[2],q[3]],[uv[0],uv[2],uv[3]])]
def govde(L,D,HB,HL,acik=False):
    a=D/2; H=HB+HL; vb=HB/H; S=[]
    S.append(("on",kutu_yuz([(0,HB,a),(L,HB,a),(L,0,a),(0,0,a)])))
    S.append(("arka",kutu_yuz([(L,HB,-a),(0,HB,-a),(0,0,-a),(L,0,-a)])))
    S.append(("uc",kutu_yuz([(L,HB,a),(L,HB,-a),(L,0,-a),(L,0,a)],((0,vb),(1,vb),(1,0),(0,0)))))
    S.append(("uc",kutu_yuz([(0,HB,-a),(0,HB,a),(0,0,a),(0,0,-a)],((1,vb),(0,vb),(0,0),(1,0)))))
    if acik: S.append(("ust_acik",kutu_yuz([(0,HB,-a),(L,HB,-a),(L,HB,a),(0,HB,a)])))
    return S
def kapak(L,D,HB,HL,aci=0.0,ic_doku=True):
    """aci: arka mentese (y=HB, z=-a) etrafinda acilma (radyan)"""
    a=D/2; H=HB+HL; vb=HB/H
    S=[("kapak",kubbe(L,D,HB,HL))]
    if ic_doku: S.append(("kapak_ic",kubbe(L,D,HB,HL,ic=True)))
    u1=kapak_uc(L,D,HB,HL,L,True); u0=kapak_uc(L,D,HB,HL,0.0,False)
    S.append(("uc",u1+u0))
    if aci:
        c,s=np.cos(aci),np.sin(aci)
        def rot(p):
            y,z=p[1]-HB,p[2]+a; return (p[0],HB+y*c+z*s,-a+(-y*s+z*c))
        S=[(n,[([rot(p) for p in t],uv) for t,uv in T]) for n,T in S]
    return S
def sandik(L,D,HB,HL,acik=False,aci=np.radians(110)):
    return govde(L,D,HB,HL,acik)+kapak(L,D,HB,HL,aci if acik else 0.0,ic_doku=acik)

"""Drop sandigi geometrisi: govde kutusu L x D x HB + super-elips kubbe kapak (yukseklik HL, us n; n=2 elips)."""
import numpy as np
N=40
def kesit(phi,a,HL,n):
    """Kapak kesiti: cokgen (on taban -> dik yan -> pah -> duz tepe -> ... arka taban).
    n=(h1,c): dik yanin yuksekligi (HL orani), duz tepenin yari genisligi (a orani). phi 0..pi -> yay uzunlugu orani."""
    h1,c=n
    P=np.array([(a,0),(a,h1*HL),(c*a,HL),(-c*a,HL),(-a,h1*HL),(-a,0)],float)
    sl=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))]; t=np.asarray(phi)/np.pi*sl[-1]
    return np.interp(t,sl,P[:,0]), np.interp(t,sl,P[:,1])
def kubbe(L,D,HB,HL,n,ic=False):
    a=D/2; T=[]; e=0.012 if ic else 0.0
    for k in range(N):
        p0,p1=np.pi*k/N,np.pi*(k+1)/N
        def P(x,p):
            z,y=kesit(p,a-e,HL-e,n); return (x,HB+y,z)
        q=[P(0,p0),P(L,p0),P(L,p1),P(0,p1)]; uv=[(0,k/N),(1,k/N),(1,(k+1)/N),(0,(k+1)/N)]
        tri=[(0,1,2),(0,2,3)] if not ic else [(0,2,1),(0,3,2)]
        for t in tri: T.append(([q[i] for i in t],[uv[i] for i in t]))
    return T
def kapak_uc(L,D,HB,HL,n,x,sol_on):
    a=D/2; H=HB+HL; T=[]; c=(x,HB,0.0)
    for k in range(N):
        p0,p1=np.pi*k/N,np.pi*(k+1)/N
        z0,y0=kesit(p0,a,HL,n); z1,y1=kesit(p1,a,HL,n)
        A=(x,HB+y0,z0); B=(x,HB+y1,z1)
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
def kapak(L,D,HB,HL,n,aci=0.0,ic_doku=True):
    a=D/2
    S=[("kapak",kubbe(L,D,HB,HL,n))]
    if ic_doku:
        S.append(("kapak_ic",kubbe(L,D,HB,HL,n,ic=True)))
        # kapak agzi (taban duzlemi): kenar cercevesi opak, ici saydam (ic kubbe gorunur); kapaliyken govdenin icinde kalir
        e=0.004
        S.append(("kapak_taban",kutu_yuz([(0,HB+e,a),(L,HB+e,a),(L,HB+e,-a),(0,HB+e,-a)],((0,0),(1,0),(1,1),(0,1)))))
    S.append(("uc",kapak_uc(L,D,HB,HL,n,L,True)+kapak_uc(L,D,HB,HL,n,0.0,False)))
    if aci:
        c,s=np.cos(aci),np.sin(aci)
        def rot(p):
            y,z=p[1]-HB,p[2]+a; return (p[0],HB+y*c+z*s,-a+(-y*s+z*c))
        S=[(nm,[([rot(p) for p in t],uv) for t,uv in T]) for nm,T in S]
    return S
def sandik(L,D,HB,HL,n,acik=False,aci=np.radians(110)):
    return govde(L,D,HB,HL,acik)+kapak(L,D,HB,HL,n,aci if acik else 0.0,ic_doku=acik)

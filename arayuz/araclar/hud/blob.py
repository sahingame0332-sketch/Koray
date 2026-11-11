import numpy as np
from PIL import Image
from collections import deque
P="/home/user/Koray/arayuz/referans_gorseller/hud_ekranlar/hud_%02d.png"
def etiket(m):
    H,W=m.shape; lab=np.zeros((H,W),np.int32); n=0
    for y in range(H):
        for x in range(W):
            if m[y,x] and lab[y,x]==0:
                n+=1; q=deque([(y,x)]); lab[y,x]=n
                while q:
                    cy,cx=q.popleft()
                    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny,nx=cy+dy,cx+dx
                        if 0<=ny<H and 0<=nx<W and m[ny,nx] and lab[ny,nx]==0:
                            lab[ny,nx]=n; q.append((ny,nx))
    return lab,n
def kapat(m,k=7):
    import numpy as np
    pad=k//2
    def dil(a):
        o=np.zeros_like(a)
        for dy in range(-pad,pad+1):
            for dx in range(-pad,pad+1):
                o|=np.roll(np.roll(a,dy,0),dx,1)
        return o
    def ero(a): return ~dil(~a)
    return ero(dil(m))
def doldur(m):
    # disaridan erisilemeyen delikleri doldur
    H,W=m.shape; dis=np.zeros_like(m); q=deque()
    for x in range(W):
        for y in (0,H-1):
            if not m[y,x] and not dis[y,x]: dis[y,x]=True;q.append((y,x))
    for y in range(H):
        for x in (0,W-1):
            if not m[y,x] and not dis[y,x]: dis[y,x]=True;q.append((y,x))
    while q:
        cy,cx=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=cy+dy,cx+dx
            if 0<=ny<H and 0<=nx<W and not m[ny,nx] and not dis[ny,nx]:
                dis[ny,nx]=True;q.append((ny,nx))
    return m|~dis
def bul(n,x0,y0,x1,y1,esik=95,minalan=1500):
    a=np.asarray(Image.open(P%n).convert("RGB")).astype(int)
    s=a[y0:y1,x0:x1].mean(2)
    m=doldur(kapat(s<esik,9))
    lab,k=etiket(m)
    out=[]
    for i in range(1,k+1):
        ys,xs=np.where(lab==i)
        if len(ys)<minalan: continue
        out.append((x0+xs.min(),y0+ys.min(),xs.max()-xs.min()+1,ys.max()-ys.min()+1,len(ys)))
    for o in sorted(out,key=lambda t:(t[1]//40,t[0])):
        print("x=%4d y=%4d w=%3d h=%3d alan=%6d  merkez=(%d,%d)"%(o+(o[0]+o[2]//2,o[1]+o[3]//2)))

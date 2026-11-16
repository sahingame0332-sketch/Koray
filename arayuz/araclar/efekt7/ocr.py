import numpy as np, glob, json
from PIL import Image
fs=sorted(glob.glob('G/k_*.png'))
def kes(i):
    a=np.asarray(Image.open(fs[i]).convert('L').crop((1160,920,1360,980)),dtype=np.float32)
    return a<110          # koyu rakamlar
def bolut(m):
    col=m.any(0); seg=[]; x=0
    while x<len(col):
        if col[x]:
            s=x
            while x<len(col) and col[x]: x+=1
            seg.append((s,x))
        x+=1
    return seg
if __name__=='__main__':
    for i in (160,166,190,200,230,262,420,600):
        m=kes(i); print(i,bolut(m))
SL=[(108,133),(144,169),(168,193)]
def hucre(m,s): return m[:,s[0]:s[1]].astype(np.float32)
def sablon():
    bil={160:"107",166:"121",190:"124",200:"129",230:"143",262:"171",420:"285",600:"352"}
    T={}
    for i,t in bil.items():
        m=kes(i)
        for s,ch in zip(SL,t): T.setdefault(ch,[]).append(hucre(m,s))
    return {k:np.mean(v,0) for k,v in T.items()}
def oku(i,T):
    m=kes(i); out=""; skor=[]
    for s in SL:
        h=hucre(m,s); d={k:np.abs(h-v).mean() for k,v in T.items()}; k=min(d,key=d.get); out+=k; skor.append(round(d[k],3))
    return int(out[0])+int(out[1:])/100.0, max(skor)

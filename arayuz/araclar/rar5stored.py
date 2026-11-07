import sys
def vint(b,i):
    r=0;s=0
    while True:
        c=b[i];i+=1;r|=(c&0x7f)<<s;s+=7
        if not c&0x80: return r,i
d=open(sys.argv[1],'rb').read();out=sys.argv[2]
i=8
while i<len(d):
    i+=4;sz,i=vint(d,i);start=i
    typ,i=vint(d,i);fl,i=vint(d,i);dsz=0
    if fl&1: _,i=vint(d,i)
    if fl&2: dsz,i=vint(d,i)
    if typ==2 and dsz>1000000:
        data=d[start+sz:start+sz+dsz];open(out,'wb').write(data);print(data[:4])
    if typ==5: break
    i=start+sz+dsz

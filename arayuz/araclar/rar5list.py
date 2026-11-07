import sys
def vint(b,i):
    r=0;s=0
    while True:
        c=b[i];i+=1;r|=(c&0x7f)<<s;s+=7
        if not c&0x80: return r,i
d=open(sys.argv[1],'rb').read()
i=8
while i<len(d):
    hs=i;i+=4
    sz,i=vint(d,i);start=i
    typ,i=vint(d,i);fl,i=vint(d,i)
    ext=dsz=0
    if fl&1: ext,i=vint(d,i)
    if fl&2: dsz,i=vint(d,i)
    if typ==2:
        ff,i=vint(d,i);us,i=vint(d,i);at,i=vint(d,i)
        if ff&2: i+=4
        if ff&4: i+=4
        ci,i=vint(d,i);hos,i=vint(d,i);nl,i=vint(d,i)
        name=d[i:i+nl].decode('utf8','replace')
        print(name,'packed',dsz,'unp',us,'method',(ci>>7)&7,'solid',(ci>>6)&1,'dir',ff&1, 'enc' if ext and b'\x01' else '')
    if typ==5: break
    i=start+sz+dsz

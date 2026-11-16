import numpy as np,json
from PIL import Image, ImageDraw, ImageFont
from mesh import sandik; from ciz import ciz
U=json.load(open('uydu.json')); D,HB,HL=U['sekil']; AC=json.load(open('acik.json'))
TON=np.array([0.41,0.40,0.45])     # acik durumda yan yuzler + kapak disi (s1'den olculdu)
def dokular(acik):
    d={k:np.asarray(Image.open('t_%s.png'%k).convert('RGBA')).astype(np.float32) for k in ('on','arka','uc','kapak','ust_acik','kapak_ic')}
    if acik:
        for k in ('on','arka','uc','kapak'): d[k][...,:3]*=TON
    return d
crop={1:(780,590,960,800),2:(755,455,895,575),3:(670,500,805,620),4:(860,340,970,425)}
cams={**{int(k):v for k,v in U['kam'].items()},1:AC['kam']}
F=ImageFont.truetype('/home/user/Koray/arayuz/kaynak/char_info/fonts/Roboto-Bold.ttf',20)
Z=3; pan=[]
cim=np.asarray(Image.open('s4.jpg').convert('RGB')).astype(np.float32)[540:780,1480:1720]   # bos cim
for i,(x0,y0,x1,y1) in crop.items():
    P=list(cams[i]); P[4]-=x0; P[5]-=y0
    O=np.asarray(Image.open('s%d.jpg'%i).convert('RGB')).astype(np.float32)[y0:y1,x0:x1]
    im=ciz(sandik(1.0,D,HB,HL,acik=(i==1),aci=AC['aci']),dokular(i==1),P,(x1-x0,y1-y0))
    r=im[...,3]>0; arka=cim[:y1-y0,:x1-x0]; v=arka.copy(); v[r]=im[r,:3]
    ad='AÇIK' if i==1 else 'KAPALI'
    pan.append(('%s — ORİJİNAL (%d)'%(ad,i),O)); pan.append(('%s — 3B MODEL'%ad,v))
# yeni acilar
for ad,acik,yaw,pitch in (('KAPALI arkadan',False,200,40),('AÇIK yandan',True,-60,35),('AÇIK önden',True,0,30)):
    P=[np.radians(yaw),np.radians(pitch),0,80,90,120]
    im=ciz(sandik(1.0,D,HB,HL,acik=acik,aci=AC['aci']),dokular(acik),P,(180,180)); r=im[...,3]>0
    v=cim[:180,:180].copy(); v[r]=im[r,:3]; pan.append(('3B — '+ad,v))
H=max(p[1].shape[0] for p in pan)*Z; W=sum(p[1].shape[1]*Z+8 for p in pan)
c=Image.new('RGB',(W,H+34),(24,24,28)); d=ImageDraw.Draw(c); x=0
for t,a in pan:
    im=Image.fromarray(a.astype(np.uint8)).resize((a.shape[1]*Z,a.shape[0]*Z),Image.LANCZOS); c.paste(im,(x,34)); d.text((x+4,6),t,font=F,fill=(255,220,120)); x+=im.width+8
# iki satira bol
w2=W//2+300; ust=c.crop((0,0,w2,H+34)); alt=c.crop((w2,0,W,H+34))
o=Image.new('RGB',(max(ust.width,alt.width),2*(H+34)+8),(24,24,28)); o.paste(ust,(0,0)); o.paste(alt,(0,H+42))
o.save('/home/user/Koray/arayuz/onizlemeler/sandik_onizleme.png'); print(o.size)

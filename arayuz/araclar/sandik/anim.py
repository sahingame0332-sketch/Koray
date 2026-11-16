import numpy as np,json,os,subprocess,tempfile,shutil
from PIL import Image, ImageDraw, ImageFont
from mesh import sandik; from ciz import ciz
U=json.load(open('uydu.json')); D,HB,HL=U['sekil']; AC=json.load(open('acik.json')); ACI=AC['aci']
TON=np.array([0.41,0.40,0.45])
base={k:np.asarray(Image.open('t_%s.png'%k).convert('RGBA')).astype(np.float32) for k in ('on','arka','uc','kapak','ust_acik','kapak_ic')}
def dok(t):
    d={k:v.copy() for k,v in base.items()}
    for k in ('on','arka','uc','kapak'): d[k][...,:3]*=(1-t)+t*TON
    return d
cim=np.asarray(Image.open('s3.jpg').convert('RGB').crop((1424,244,1604,424)).resize((360,360),Image.BICUBIC)).astype(np.float32)   # bos cim
F=ImageFont.truetype('/home/user/Koray/arayuz/kaynak/char_info/fonts/Roboto-Bold.ttf',22)
d=tempfile.mkdtemp(); n=0
def kare(yaw,aci_t,ton,yazi):
    global n
    P=[np.radians(yaw),np.radians(40),0,150,180,235]
    im=ciz(sandik(1.0,D,HB,HL,acik=aci_t>0,aci=ACI*aci_t),dok(ton),P,(360,360)); r=im[...,3]>0
    v=cim.copy(); v[r]=im[r,:3]
    o=Image.fromarray(v.astype(np.uint8)).resize((720,720),Image.LANCZOS); dr=ImageDraw.Draw(o)
    dr.rectangle((0,0,720,36),fill=(24,24,28)); dr.text((10,6),yazi,font=F,fill=(255,220,120))
    o.save(os.path.join(d,'a_%04d.png'%n)); n+=1
for k in range(90): kare(k*4,0,0,'KAPALI — 360° dönüş')
for k in range(15): kare(0,0,0,'KAPALI')
for k in range(10): t=(k+1)/10; kare(0,t,t,'AÇILIYOR (0.3 sn)')
for k in range(90): kare(k*4,1,1,'AÇIK — 360° dönüş (kapak 115.5°)')
for k in range(15): kare(0,1,1,'AÇIK')
O='/home/user/Koray/arayuz/onizlemeler/'
subprocess.run(['ffmpeg','-v','error','-y','-framerate','30','-i',d+'/a_%04d.png','-vf','format=yuv420p','-c:v','libx264','-crf','18',O+'sandik_animasyon.mp4'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-framerate','30','-i',d+'/a_%04d.png','-vf','fps=15,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=160[p];[b][p]paletteuse=dither=bayer',O+'sandik_animasyon.gif'],check=True)
shutil.rmtree(d); print(n,'kare')

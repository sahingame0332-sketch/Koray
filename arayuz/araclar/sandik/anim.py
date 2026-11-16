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
K=json.load(open('uydu.json'))['kam']['2']; YAW=np.degrees(K[0]); PIT=np.degrees(K[1]); ROLL=K[2]
def kare2(aci_t,ton,yazi):
    global n
    P=[np.radians(YAW),np.radians(PIT),ROLL,130,175,250]
    if aci_t<0: r=np.zeros((360,360),bool); im=np.zeros((360,360,4))
    else:
        im=ciz(sandik(1.0,D,HB,HL,acik=aci_t>0,aci=ACI*aci_t),dok(ton),P,(360,360)); r=im[...,3]>0
    v=cim.copy(); v[r]=im[r,:3]
    o=Image.fromarray(v.astype(np.uint8)).resize((720,720),Image.LANCZOS); dr=ImageDraw.Draw(o)
    dr.rectangle((0,0,720,36),fill=(24,24,28)); dr.text((10,6),yazi,font=F,fill=(255,220,120))
    o.save(os.path.join(d,'a_%04d.png'%n)); n+=1
for k in range(20): kare2(-1,0,'Mob öldü')
for k in range(75): kare2(0,0,'Sandık düştü — yerinde SABİT, kapalı')
for k in range(10): t=(k+1)/10; kare2(t,t,'Açılıyor (0.3 sn, varsayım)')
for k in range(75): kare2(1,1,'Açık — SABİT (Collect All penceresi açıkken)')
O='/home/user/Koray/arayuz/onizlemeler/'
subprocess.run(['ffmpeg','-v','error','-y','-framerate','30','-i',d+'/a_%04d.png','-vf','format=yuv420p','-c:v','libx264','-crf','18',O+'sandik_animasyon.mp4'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-framerate','30','-i',d+'/a_%04d.png','-vf','fps=15,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=160[p];[b][p]paletteuse=dither=bayer',O+'sandik_animasyon.gif'],check=True)
shutil.rmtree(d); print(n,'kare')

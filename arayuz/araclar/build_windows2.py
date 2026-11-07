import numpy as np
from PIL import Image, ImageDraw
SC=4
def rr(W,H,rects):
    m=Image.new('L',(W*SC,H*SC),0);d=ImageDraw.Draw(m)
    for x0,y0,x1,y1,r in rects: d.rounded_rectangle((x0*SC,y0*SC,(x1+1)*SC-1,(y1+1)*SC-1),radius=r*SC,fill=255)
    return np.array(m.resize((W,H),Image.LANCZOS)).astype(np.float32)/255
# ---------- SAVE STAT PRESET (mat / opak) ----------
o=np.array(Image.open('preset_orig.png').convert('RGB'));H,W=o.shape[:2]
out=o.copy()
for k in (1,2,3):                       # slot 2-4 <- temiz slot 1 (hayalet izleri yok)
    out[45+103*k:148+103*k,6:291]=o[45:148,6:291]
    out[45+103*k:65+103*k,7:30]=o[45+103*k:65+103*k,7:30]   # kendi numara rozeti
al=np.zeros((H,W),np.float32)
al=np.maximum(al,rr(W,H,[(3,8,295,40,3)]))      # başlık çubuğu
al[41:462,6:291]=1                               # gövde (mat)
x0,y0,x1,y1=3,8,296,462
rgba=np.dstack([out,(al*255).astype(np.uint8)])[y0:y1,x0:x1]
Image.fromarray(rgba).save('save_stat_preset.png')
# ---------- STAT BUTONLARI (saydam zemin) ----------
o=np.array(Image.open('stats_orig.png').convert('RGB')).astype(np.float32);H,W=o.shape[:2]
X0,Y0,X1,Y1=2,0,198,242
alpha=np.zeros((H,W),np.float32);col=np.zeros_like(o)
alpha[Y0:Y1+1,X0:X1+1]=0.85                       # yarı saydam siyah zemin
fr=np.zeros((H,W),bool);fr[Y0:Y1+1,X0:X1+1]=True;fr[Y0+3:Y1-2,X0+3:X1-2]=False
alpha[fr]=1;col[fr]=o[fr]                          # çerçeve opak
btn=rr(W,H,[(23,22,185,59,3),(23,65,185,102,3),(23,108,185,145,3),(23,151,185,188,3),(23,194,185,231,3)])
alpha=np.maximum(alpha,btn);col=col*(1-btn[...,None])+o*btn[...,None]
rgba=np.dstack([col.astype(np.uint8),(alpha*255).astype(np.uint8)])[Y0:Y1+1,X0:X1+1]
Image.fromarray(rgba).save('stat_buttons.png')
print('ok')

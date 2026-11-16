import numpy as np
from PIL import Image
from scipy import ndimage
K={1:(780,590,960,800),2:(755,455,895,575),3:(670,500,805,620),4:(860,340,970,425),5:(690,425,820,535)}
out=[]
for i,(x0,y0,x1,y1) in K.items():
    I=np.asarray(Image.open('s%d.jpg'%i).convert('RGB'),dtype=np.float32)[y0:y1,x0:x1]
    R,G,B=I[...,0],I[...,1],I[...,2]
    cim=(G>=R-4)&(G>B+12)            # cim: yesil baskin
    m=~cim
    m=ndimage.binary_opening(m,np.ones((3,3)))
    l,n=ndimage.label(m); s=ndimage.sum(m,l,range(1,n+1)); m=l==(1+np.argmax(s))
    m=ndimage.binary_fill_holes(ndimage.binary_closing(m,np.ones((5,5))))
    np.save('m%d.npy'%i,m)
    v=I.copy(); v[~m]*=0.25
    out.append(Image.fromarray(v.astype(np.uint8)).resize(((x1-x0)*3,(y1-y0)*3)))
W=sum(o.width for o in out); c=Image.new('RGB',(W,max(o.height for o in out)))
x=0
for o in out: c.paste(o,(x,0)); x+=o.width
c.save('maske.png')

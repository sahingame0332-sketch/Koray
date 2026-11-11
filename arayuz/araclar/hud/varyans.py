import numpy as np
from PIL import Image
P="/home/user/Koray/arayuz/referans_gorseller/hud_ekranlar/hud_%02d.png"
ims=[np.asarray(Image.open(P%i).convert("RGB")).astype(np.int16) for i in range(1,5)]
st=np.stack(ims)                      # 4,H,W,3
rng=(st.max(0)-st.min(0)).max(2)      # H,W  kanal bazinda en buyuk fark
H,W=rng.shape
print("boyut",W,H)
# statik = tum karelerde ayni (HUD kromu), degisken = oyun dunyasi veya dinamik yazi
statik=(rng<=10)
print("statik piksel orani %.3f"%statik.mean())
Image.fromarray((statik*255).astype(np.uint8)).save("statik_maske.png")
# satir/sutun profilleri: HUD bloklarini bulmak icin
rs=statik.mean(1); cs=statik.mean(0)
np.save("statik.npy",statik)
for name,prof in (("satir",rs),("sutun",cs)):
    print("---",name)
    step=max(1,len(prof)//60)
    for i in range(0,len(prof),step):
        v=prof[i:i+step].mean()
        print("%5d %.2f %s"%(i,v,"#"*int(v*50)))

#!/usr/bin/env python3
"""Orijinal gorseldeki yazinin hangi fonta ait oldugunu olcerek siralar.

Her etiketi her aday fontla 13-28 punto arasinda rasterize eder, yazi kutusunu
orijinalinkiyle hizalar ve en iyi ortusmeyi (IoU) alir. Punto etkisini disarida
biraktigi icin sonuc fontun kendi sekil benzerligini gosterir.

Kullanim:
  python3 font_kimligi.py ORIJINAL.jpg [font.ttf ...]
Font verilmezse sistemdeki yaygin adaylar + depodaki fontlar denenir.
"""
import json, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ESIK = 150
BURADA = pathlib.Path(__file__).parent
DEPO = BURADA.parent.parent

VARSAYILAN = [
    DEPO / "unity_kaynak/Assets/OlymposCharacter1298/Fonts/RobotoSlab-Bold.ttf",
    DEPO / "unity_kaynak/Assets/OlymposCharacter1298/Fonts/Roboto-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
]

def kutu(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def ciz(metin, yol, punto):
    f = ImageFont.truetype(str(yol), punto)
    im = Image.new("L", (700, 140), 0)
    ImageDraw.Draw(im).text((20, 20), metin, font=f, fill=255)
    return kutu(np.asarray(im) > 128)

def iou(a, b):
    h, w = max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1])
    A = np.zeros((h, w), bool); B = np.zeros((h, w), bool)
    A[:a.shape[0], :a.shape[1]] = a; B[:b.shape[0], :b.shape[1]] = b
    en_iyi = 0.0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            Bs = np.roll(np.roll(B, dy, 0), dx, 1)
            u = np.logical_or(A, Bs).sum()
            if u:
                en_iyi = max(en_iyi, np.logical_and(A, Bs).sum() / u)
    return en_iyi

def main(argv):
    if len(argv) < 2:
        print(__doc__); return 1
    orig = np.asarray(Image.open(argv[1]).convert("L")).astype(np.int16)
    fontlar = [pathlib.Path(p) for p in (argv[2:] or VARSAYILAN)]
    fontlar = [f for f in fontlar if pathlib.Path(f).exists()]
    bolgeler = json.loads((BURADA / "bolgeler.json").read_text())["bolgeler"]

    sonuc = {}
    for f in fontlar:
        puanlar, puntolar = [], {}
        for ad, b in bolgeler.items():
            x0, y0, x1, y1 = b["kutu"]
            hedef = kutu(orig[y0:y1, x0:x1] > ESIK)
            if hedef is None:
                continue
            en_iyi, en_punto = 0.0, None
            for punto in range(13, 29):
                m = ciz(b.get("metin", ad), f, punto)
                if m is None:
                    continue
                v = iou(hedef, m)
                if v > en_iyi:
                    en_iyi, en_punto = v, punto
            puanlar.append(en_iyi); puntolar[ad] = (en_punto, en_iyi)
        sonuc[f.name] = (float(np.mean(puanlar)), puntolar)

    print("SIRALAMA (yuksek = orijinale daha benzer sekil):")
    for i, (ad, (ort, _)) in enumerate(sorted(sonuc.items(), key=lambda r: -r[1][0]), 1):
        print("  %d. %-28s %.3f" % (i, ad, ort))
    en = max(sonuc.items(), key=lambda r: r[1][0])
    print("\n'%s' icin etiket basina en iyi punto:" % en[0])
    for ad, (punto, v) in en[1][1].items():
        print("  %-20s punto %-3s IoU %.3f" % (ad, punto, v))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

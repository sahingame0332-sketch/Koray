#!/usr/bin/env python3
"""Yukseltme sunaginin dokularini uretir (ozgun, prosedurel, dikissiz).

Cikti: unity/Assets/Resources/Props/UpgradeAltar/stone.png, energy_noise.png

Dikissizlik: rastgele gurultu frekans uzayinda suzulur; FFT periyodik oldugu
icin sonuc kendiliginden doseme (tile) yapar.

Gerekli: pip install pillow numpy
"""
import os

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "unity", "Assets", "Resources", "Props", "UpgradeAltar")


def spectral_noise(n, power, seed, lo=1.0):
    rng = np.random.RandomState(seed)
    f = np.fft.fft2(rng.randn(n, n))
    fx = np.fft.fftfreq(n) * n
    k = np.hypot(*np.meshgrid(fx, fx))
    k[0, 0] = 1.0
    f *= (k >= lo) / k ** power
    a = np.real(np.fft.ifft2(f))
    a -= a.min()
    return a / a.max()


def save(arr, name):
    os.makedirs(OUT, exist_ok=True)
    img = Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8))
    path = os.path.join(OUT, name)
    img.convert("RGB").save(path, optimize=True)
    print("yazildi:", os.path.relpath(path, ROOT), img.size)


def stone(n=256):
    base = spectral_noise(n, 1.6, 7)
    grain = spectral_noise(n, 0.6, 8, lo=12)
    veins = 1.0 - np.clip(np.abs(spectral_noise(n, 1.9, 9) - 0.5) * 14, 0, 1)  # ince catlaklar
    v = 0.58 + (base - 0.5) * 0.45 + (grain - 0.5) * 0.22 - veins * 0.22
    # hafif sicak gri
    save(np.stack([v * 1.03, v * 1.0, v * 0.94], -1), "stone.png")


def energy(n=256):
    a = spectral_noise(n, 1.9, 21, lo=2)
    wisps = 1.0 - np.clip(np.abs(a - 0.5) * 5.0, 0, 1)   # sirt cizgileri -> duman telleri
    v = wisps ** 1.6 * 0.85 + spectral_noise(n, 1.4, 22) * 0.15
    save(np.stack([v, v, v], -1), "energy_noise.png")


if __name__ == "__main__":
    stone()
    energy()

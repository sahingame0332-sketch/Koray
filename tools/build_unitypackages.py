#!/usr/bin/env python3
"""Unity paketlerini (.unitypackage) uretir.

Cikti: unity/ResistBuffEffect.unitypackage, unity/UpgradeAltar.unitypackage
Unity'de: Assets > Import Package > Custom Package...

Ayrica her dosyanin yanina sabit GUID'li .meta yazar; boylece paketi ice
aktarmakla unity/Assets klasorunu kopyalamak ayni GUID'leri verir.

Kullanim: python3 tools/build_unitypackages.py
"""
import hashlib
import io
import os
import tarfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITY = os.path.join(ROOT, "unity")
SHARED_VFX = [
    "Assets/Resources/VFX/ResistBuff/KorayAdditive.shader",
    "Assets/Resources/VFX/ResistBuff/hoop.png",
    "Assets/Resources/VFX/ResistBuff/glow.png",
]
PACKAGES = {
    "ResistBuffEffect.unitypackage": SHARED_VFX + [
        "Assets/Scripts/VFX/ResistBuffEffect.cs",
        "Assets/Scripts/Editor/ResistBuffEffectMenu.cs",
        "Assets/Resources/VFX/ResistBuff/rune_circle.png",
        "Assets/Resources/VFX/ResistBuff/spark.png",
    ],
    # Sunak, halka ve parilti icin resist efektinin iki dokusunu ve shader'ini paylasir;
    # GUID'ler ayni oldugundan iki paket birlikte ice aktarilabilir.
    "UpgradeAltar.unitypackage": SHARED_VFX + [
        "Assets/Scripts/Props/UpgradeAltar.cs",
        "Assets/Scripts/Editor/UpgradeAltarMenu.cs",
        "Assets/Resources/Props/UpgradeAltar/KorayVertexColor.shader",
        "Assets/Resources/Props/UpgradeAltar/KorayEnergySwirl.shader",
        "Assets/Resources/Props/UpgradeAltar/stone.png",
        "Assets/Resources/Props/UpgradeAltar/energy_noise.png",
    ],
}


def add(tar, name, data):
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mode = 0o644
    tar.addfile(info, io.BytesIO(data))


def build(name, files):
    out = os.path.join(UNITY, name)
    with tarfile.open(out, "w:gz") as tar:
        for path in files:
            guid = hashlib.md5(("koray:" + path).encode()).hexdigest()
            meta = ("fileFormatVersion: 2\nguid: %s\n" % guid).encode()
            src = os.path.join(UNITY, path)
            with open(src + ".meta", "wb") as f:
                f.write(meta)
            with open(src, "rb") as f:
                add(tar, guid + "/asset", f.read())
            add(tar, guid + "/asset.meta", meta)
            add(tar, guid + "/pathname", path.encode())
    print("yazildi:", os.path.relpath(out, ROOT), os.path.getsize(out), "bayt,", len(files), "dosya")


def main():
    for name, files in PACKAGES.items():
        build(name, files)


if __name__ == "__main__":
    main()

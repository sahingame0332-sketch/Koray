#!/bin/sh
# Unity kodunu Unity kurmadan derleme kontrolunden gecirir.
#
# Gerekli: mono-mcs  (apt-get install -y mono-mcs)
#
# NE YAPAR: unity/Assets/Scripts altindaki butun .cs dosyalarini minimal bir
# UnityEngine saplamasiyla birlikte derler. Sozdizimi ve tip hatalarini yakalar.
#
# NE YAPMAZ: calisma zamani davranisini test etmez, Unity'ye ozgu seyleri
# (serilestirme, Inspector, prefab baglantilari) dogrulamaz. Bunlar icin
# projeyi Unity'de acman gerekir.

set -e
cd "$(dirname "$0")/../.."
ROOT=$(pwd)

if ! command -v mcs > /dev/null 2>&1; then
    echo "HATA: mcs bulunamadi. Kurulum: apt-get install -y mono-mcs"
    exit 1
fi

OUT=$(mktemp -d)
trap 'rm -rf "$OUT"' EXIT

echo "Derleniyor: unity/Assets/Scripts/**/*.cs + UnityEngine saplamasi"
echo

# -define:UNITY_EDITOR  -> OnValidate gibi editor-only kod da derlenir
mcs -target:library \
    -out:"$OUT/Koray.dll" \
    -define:UNITY_EDITOR \
    -warnaserror+ \
    -warn:4 \
    -nowarn:0169,0414,0649 \
    "$ROOT/tools/unity-compile-check/UnityEngineStub.cs" \
    $(find "$ROOT/unity/Assets/Scripts" -name '*.cs')

echo "DERLEME BASARILI -- sozdizimi ve tip hatasi yok"
echo

# --run verilirse dogrulama kosumunu da derle ve calistir
if [ "$1" = "--run" ]; then
    mcs -target:exe \
        -out:"$OUT/harness.exe" \
        -define:UNITY_EDITOR \
        -nowarn:0169,0414,0649 \
        "$ROOT/tools/unity-compile-check/UnityEngineStub.cs" \
        "$ROOT/tools/unity-compile-check/HoldRepeatHarness.cs" \
        $(find "$ROOT/unity/Assets/Scripts" -name '*.cs')
    mono "$OUT/harness.exe"
fi

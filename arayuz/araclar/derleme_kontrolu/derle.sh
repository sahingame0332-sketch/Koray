#!/usr/bin/env bash
# OLYMPOS betiklerini Unity olmadan derleyip söz dizimi / tip hatalarını yakalar.
# Gerekli: mono-devel (mcs).  Kullanım: arayuz/araclar/derleme_kontrolu/derle.sh
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
assets="$here/../../unity_kaynak/Assets"
out="$(mktemp -d)"

if ! command -v mcs >/dev/null; then
  echo "mcs bulunamadı. Kurulum: apt-get install -y mono-devel" >&2
  exit 1
fi

mapfile -t sources < <(find "$assets" -name '*.cs' | sort)
printf 'Derlenen betikler:\n'; printf '  %s\n' "${sources[@]#$assets/}"

mcs -target:library -out:"$out/olympos_check.dll" -langversion:7.2 \
    "$here/UnityStubs.cs" "$here/EditorStubs.cs" "${sources[@]}"

echo "Derleme tamam: 0 hata. ($out/olympos_check.dll)"

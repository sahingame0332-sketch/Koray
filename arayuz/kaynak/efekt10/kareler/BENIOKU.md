# Efekt 10 — pembe patlama kareleri (onaylı)

| Kare | Dosya | Açıklama |
|---|---|---|
| 1 | `kare_01.png` (saydam, 604×604) | Patlamanın ilk çıkış karesi — kullanıcı onayı (19 Kasım 2026). Referans fotoğraftan çıkarılan ışık katmanı; mor lekeler temizlendi, somon-pembe halka sol parçadan tüm çevreye uygulandı, tepe/dip turuncu iz giderildi. |

Önizleme: `kare_01_siyah.png`, `kare_01_beyaz.png`. Üretim zinciri: `araclar/efekt10/kure_ref.py` → `kure_pembeli_temizle.py` → `kure_halka_kopyala.py`.
Merkez görüntünün tam ortasında; ışık katmanı ön-çarpımsız RGBA (alfa = parlaklık), Unity'de eklemeli (Blend One One / SrcAlpha One) kullanılır.

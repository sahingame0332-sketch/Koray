# 10 · Skill ve hasar efektleri (Pillar of Fire, karaktere vuruş, cast çubuğu, hasar mesajları)

Kaynak: kullanıcının 4 sn'lik kaydı (2266 × 1488, 60 kare/sn, HEVC). Kayıt sol üstte yüz kamerası içerdiği için
**depoya konmadı**; yalnız çıkarılan efekt kareleri (`kaynak/efekt/`) ve ölçümler var.
Paket: `unity_paketleri/OlymposEfekt1298.unitypackage` (tek başına) · önizleme: `onizlemeler/efekt_onizleme.png`.
Araçlar: `araclar/efekt/cikar.py VIDEO` (kareler), `kur.py VIDEO` (doğrulama görseli).

## Yöntem
- Kamera sabit: efektsiz karelerde zemin farkı < 0.3 / 255 (196. kareden sonra kayıt ekranı kararıyor).
- Efekt **eklemeli ışık**: efekt bölgesinde 148 971 piksel parlıyor, 4 606 kararıyor (kararanlar efektin önündeki karakter/mob).
  Bu yüzden kare = `clip(O − B, 0, 255)`, B = efekt öncesi karelerin medyanı. Unity'de `Blend One One` ile aynı zemine eklenince
  orijinal geri gelir: ortalama mutlak fark **3.7** (ateş sütunu) ve **4.2** (vuruş) / 255.
- UI etiketleri (ad, can çubuğu) ve efektin önündeki karakter bölgesi en yakın piksel + yumuşatma ile dolduruldu;
  ısınmayan sönük artıklar (mob animasyonu) silindi.

## Ölçümler
| Efekt | Kayıtta | Kare | Boyut (px) | Pivot (hedef noktası) | Genişlik |
|---|---|---|---|---|---|
| Pillar of Fire (moba) | kare 110–160 (1.83–2.67 sn) | 26 @ 30 fps | 500 × 710 | mobun ayağı (0.40, 0.155) | 4.5 karakter boyu |
| Karaktere vuruş | kare 178–194 (2.97–3.23 sn) | 9 @ 30 fps | 450 × 420 | karakter gövdesi (0.573, 0.452) | 4.1 karakter boyu |

- Karakter ekranda ~110 px (kurucu `karakterBoyu = 1.8` ile çarpar).
- Ateş sütunu: ilk 0.1 sn dışa saçılan ince kıvılcım çizgileri → 0.2–0.4 sn en geniş turuncu-sarı alev (genişlik ~470 px) →
  incelen kırmızı çekirdekli dikey sütun → 0.85 sn'de sönük kalıntı.
- Vuruş: ilk 2 kare sarı yuvarlak ışıma (yarıçap ~120 px) + zeminde dikdörtgen ışık lekesi (oyunun dinamik ışığı),
  sonra kırmızı-turuncu halka ve dışa sivri ışınlar (yarıçap ~90 px). Sonu kayıtta yok.
- **Cast çubuğu** (tablet koordinatı): siyah (1032,1002) 205 × 12; yeşil dolum 8 px, dikey ton
  `#437731 → #5CB938 → #3D8222`; skill adı Roboto Bold 15 `#FDE1E2` mürekkep üstü 986; kalan süre "0,2 sec"
  Roboto Bold 17 `#E3DF73`; ekran ortasının 266 px altında. Kurucu telefon düzenine 1/1.0405 ile çevirir.
- **Hasar:** ekranda uçan sayı yok. Information paneli (Roboto Slab Bold 31, satır ~30 px):
  kırmızı `#F80001` "… is inflicted with N HP damage." ve "N SP Used"; beyaz "… received N damage";
  sarı `#FCE600` "Using - Pillar Of Fire". Hedefin can çubuğu azalır (bkz. 06 hedef çubuğu).

## Sınırlar
Düz kare dizisi (parçacık sistemi değil) · karakter önündeki şerit tahmini · vuruşun sönüşü kayıtta yok ·
Unity'de ve URP'de denenmedi, shader burada derlenemedi.

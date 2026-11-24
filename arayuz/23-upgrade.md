# 23 · Upgrade pencereleri (Select · Item · Accessory · Fast)

Kaynak: kullanıcının 5 tablet ekran görüntüsü (2266 × 1488): Select Upgrade menüsü, ITEM UPGRADE (boş + dolu), ACCESSORY UPGRADE,
FAST UPGRADE +1…+5. Paketler (her biri tek başına): `OlymposSelectUpgrade1298`, `OlymposItemUpgrade1298`, `OlymposAccessoryUpgrade1298`,
`OlymposFastUpgrade1298` (sınıflar `Olympos<Ad>Penceresi`, `Olympos<Ad>HarfAraligi`, `Olympos<Ad>Builder`). Araçlar `araclar/upgrade/`,
sprite + ölçüler `kaynak/upgrade/`, önizlemeler `onizlemeler/upgrade_*_onizleme.png`.

## Yöntem
- Select / Item / Accessory / Fast görüntüleri **aynı kamera**: pencere dışı pikseller birebir aynı (fark 0.0). Select görüntüsünde
  yükseltme pencerelerinin arkası açık → her piksel için arka plan B biliniyor. Kirli yerler (Select menüsü, skill çarkı, NPC, şimşek/altıgen
  efekt) maskelenip bölgenin temiz pikselleriyle ölçülür (`ortak.kirli_maske`).
- Model: `O = a·C + (1−a)·(B·T0)` — T0 = gövde geçirgenliği (siyah Image), a/C sprite. Her **tasarım bölgesinde** (panel, yuva türü, değer
  kutusu, para çubuğu) temiz piksellerle `O = k·(B·T0) + c` doğrusu → a = 1−k (`ortak.coz`, `pencere2.py`). a > 0.85 bölgeler opak, orijinal piksel.
- Kutular gri kenar çizgisinden otomatik (`ortak.kutular`): iç dikdörtgenler. Envanter ızgarası bunların x/y kümelerinden.
- Dinamik içerik silindi: envanter ikonları → hizalı boş yuva (kenar halkasıyla ±4 px arama), değer kutusu yazıları, para.

## Ölçüler (kaynak pikseli)
| | Item | Accessory | Fast |
|---|---|---|---|
| Sprite | (1165,150) 857×1235 | (1170,150) 852×1235 | (1160,150) 862×1245 |
| Gövde alfa | 0.895 | 0.895 | 0.895 |
| Panel | 0.967 | sol opak · orta 0.959 · sağ 0.995 | — |
| Küçük yuvalar | 3×3, 86×87, 0.993 | 3 adet 86×88, 0.988 | 5×3, 86×89, **0.94** |
| Büyük yuvalar | 2, opak | 3, opak | — |
| Değer kutuları | 2 × 172×45, opak | 2 × 172×45, opak | Need Coins çubuğu |
| Envanter | 7×4, iç 88×90 | 7×4, 88×90 | 7×4, 89×91 |
| Para çubuğu | gövde (0.895) | gövde | gövde |

Select Upgrade: (1846,335) 420×497, gövde alfa **0.93** (sol kenar, `saydamlik.py`; arkası hiçbir görüntüde açık değil).
Sol alttaki sarı parşömen pencerenin üstüne çizilen NPC ikonu — sprite'a alınmadı.

Yazılar (sabitler sprite'ta): Need Coins değeri Roboto Slab **Regular 27**; Upgrade Rate "%100,0" Regular **39 +1.5**; para "5,042,580"
Roboto Slab **Bold 34 +1** (dolu Item görüntüsünden ölçüldü, IoU 0.65 / 0.81 / 0.77).

## Unity
Ortak 2712×1220 Canvas'a **yüksekliğe göre 1220/1488 = 0.8199** ölçek, sağ-orta çapalı (kaynaktaki sağ boşluk korunur).
Unity'de denenmedi. Varsayım: tablet ve telefon arayüzü ekran yüksekliğiyle ölçekleniyor (Item Remove düğmesi 55 px ↔ burada 64·0.82 = 52.5).

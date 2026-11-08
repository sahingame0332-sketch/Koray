# NPC dükkân penceresi — videolardan çıkarım

Tarih: 8 Kasım 2026 · Kaynak: `NPCler.zip` içindeki 5 oynanış videosu

## Kaynak

| video | NPC | çözünürlük | sayfa |
|---|---|---|---|
| WA0021 | **Ruber[Healing potion]** | 720 × 480 | 1/1 |
| WA0022 | **Tyroon[Armor]** | 720 × 480 | 1/3 |
| WA0023 | **Caspy[Accessory]** | 1088 × 720 | 1/5 |
| WA0024 | **Pallus[Arms]** | 1088 × 720 | 1/4 |
| WA0025 | **Yasbal[Sundries]** | 1088 × 720 | 1/1 |

**Beşi de aynı pencere.** Yalnızca başlık (`NPCAdı[Kategori]`) ve ürün listesi değişiyor.
Bu yüzden tek bir `OlymposNpcShopWindow` + NPC başına veri yeterli.

## Kare ortalamasıyla temizleme

Videolar WhatsApp'tan geçmiş, H.264 gürültüsü ağır. Pencere sabit, arka plan hareketli
olduğu için: aynı içeriği gösteren kareler toplanıp medyana yakınlığa göre elenir ve
ortalanır. Gürültü kare sayısının kareköküyle azalır.

96–120 kare ortalandığında başlık, ızgara ve düğmeler net okunur hâle geliyor
(bkz. `onizlemeler/` içindeki karşılaştırma). **Ama ortalama gürültüyü siler,
çözünürlük eklemez.** Pencere 1088'lik videoda 362 px; ekran görüntüsünde aynı pencere
~754 px olurdu. Yani bu sprite diğer pencerelerin yarı çözünürlüğünde.

## Ölçülen geometri (1088 × 720 video koordinatı)

Pencere: **x 563–924, y 93–445 → 362 × 352**

| öğe | konum | boyut |
|---|---|---|
| Başlık çubuğu (X dahil) | 563, 93 | 362 × 42 |
| Kapat (X) | 886, 96 | 32 × 34 |
| Ürün slotu `[c,r]` | 589 + 54,2·c · 138 + 49·r | 42 × 42 |
| Izgara | 6 sütun × 4 satır = **24 slot/sayfa** | — |
| Sayfa ◀ | 672, 336 | 32 × 28 |
| Sayfa ▶ | 786, 336 | 32 × 28 |
| Sayfa yazısı | 712, 334 | 66 × 32 |
| "Multiple Selling" onay kutusu | 577, 381 | 25 × 24 |
| "Sell selected items." | 781, 378 | 133 × 27 |
| "Total Amount :" | 576, 412 | 100 × 20 |
| Para ikonu | 779, 426 | 18 × 15 |
| Tutar yazısı | 812, 420 | 98 × 26 |

**Zemin alfası 0,93** — üç videodan kenar ölçümüyle (Caspy 0,915 · Yasbal 0,946 ·
Pallus 0,970, medyan 0,93). Yöntem: `araclar/saydamlik_olcumu/saydamlik.py`.

**Puntolar** (mürekkep yüksekliğinden): başlık **23** · sayfa **14** ·
"Multiple Selling" **13** · "Sell selected items." **10** · "Total Amount :" **12** ·
tutar **11**.

## Sprite üretimi

`kaynak/npc_dukkan/npc_dukkan_krom.png` (362 × 352, RGBA):

- Ürün ikonları silindi: Caspy 5/5 sayfasında boş olan 2. satır, dolu 1. satırın üzerine
  birebir kopyalandı.
- Başlık yazısı silindi: çubuğun süs deseni periyodik (ölçüm: **23 px**); yazısız sol
  parçadan iki periyotluk dilim faz korunarak döşendi.
- Sayfa numarası ve tutar silindi (yan taraftaki boş zeminden örneklenerek).
- Alfa: çerçeve + başlık çubuğu + 24 slot + oklar + onay kutusu + düğme + para ikonu opak;
  etiket yazıları parlaklıktan anahtarlandı; gerisi saydam.

## Mekanikler

Videolardan doğrudan gözlendi:

1. NPC'ye basınca **Open** düğmesi çıkıyor, ona basınca dükkân açılıyor.
2. Izgaradaki ürüne basınca **ipucu kutusu**: ikon + ad · kalite satırı ("Regular Item",
   "Item Grade: Low Class") · kırmızı **Buy Price** · stat satırları ("Strength Bonus : 2",
   "Attack Power : 14", "Required Intelligence : 40") · açıklama.
3. **Satın alma onayı**: ürün adı + "Rest Money" (kalan para) + Confirm / Cancel.
4. **Satış adedi**: "Sell Dna Count" + sayı alanı + Confirm / Cancel.
5. **Multiple Selling** işaretlenince çoklu seçim; seçilenler "Sell selected items." ile satılır.
6. Sayfa okları `n/m` göstergesiyle.

**Çıkarım (kesin değil):** "Total Amount" oyuncunun parası. Gerekçe: satın alma sonrası
azalıyor (Tyroon 136.200 → 135.780). Farklıysa `SetPlayerMoney` yerine kendi değeriniz yazılır.

## Paket

`unity_paketleri/OlymposNpcShop1298.unitypackage` — menü: `OLYMPOS > 1298 > NPC Dükkân
Penceresi Oluştur`. Bileşenler: `OlymposNpcShopWindow`, `OlymposItemTooltip`,
`OlymposShopDialog`, veri yapısı `OlymposShopItem`.

İpucu kutusu ve diyalogların zemini koddan kuruluyor (ölçülen renklerle) — orijinalde de
süssüz koyu panel. Ürün ikonları paketin parçası değil: oyunun kendi item sprite'ları
`OlymposShopItem.icon` alanına verilir.

## Açık kalanlar

- Tam çözünürlüklü ekran görüntüsü gelirse sprite değişir, yerleşim ve kod aynı kalır.
- Ürün listeleri (5 NPC'nin tüm sayfaları) henüz çıkarılmadı; videolarda yalnızca bazı
  sayfalar görünüyor.
- Unity'de hiç denenmedi (ortamda Unity yok).

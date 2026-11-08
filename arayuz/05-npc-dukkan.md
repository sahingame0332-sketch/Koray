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

---

# GÜNCELLEME — tam çözünürlüklü ekran görüntüleri (8 Kasım 2026)

Kullanıcı 30 adet 2266 × 1488 ekran görüntüsü gönderdi (beş NPC + diyaloglar + ipuçları).
Yukarıdaki video tabanlı ölçümlerin yerini bunlar aldı. **Videodan çıkan iki şey yanlıştı:**

1. **Pencere boyutu.** Videoda 362 × 352 ölçmüştüm; gerçek boyut **750 × 1156**.
   Videoda pencerenin alt yarısını kaçırmışım: oyuncunun envanter ızgarası da
   aynı çerçevenin içinde.
2. **Onay diyaloğunun metni.** Videoda "Rest Money" okumuştum; aslı **"Need Money"**.

## Düzeltilmiş ölçüler (ekran koordinatı, pencere kökü 1167,193)

| öğe | konum | boyut |
|---|---|---|
| Pencere | 1167, 193 | **750 × 1156** |
| Başlık çubuğu (X dahil) | 1167, 193 | 750 × 74 |
| Kapat (X) | 1832, 195 | 72 × 72 |
| Dükkân slotu `[c,r]` | 1223 + 112,2·c · 286 + 101·r | 86 × 87 |
| Dükkân ızgarası | 6 × 4 = **24 slot/sayfa** | — |
| Sayfa ◀ / ▶ | 1397 / 1634, 692 | 65 × 50 |
| Sayfa yazısı | 1490, 688 | 100 × 58 |
| "Multiple Selling" kutusu | 1199, 786 | 45 × 45 |
| "Sell selected items." | 1619, 784 | 275 × 50 |
| "Total Amount :" | 1202, 854 | 192 × 28 |
| Para ikonu | 1610, 876 | 46 × 40 |
| Tutar yazısı | 1700, 870 | 200 × 52 |
| **Envanter slotu** `[c,r]` | 1209 + 98,2·c · 941 + 98·r | 86 × 90 |
| Envanter ızgarası | 7 × 4 = **28 slot** | — |
| Diyalog paneli | 1224, 672 | 642 × 254 (adet modunda 317) |
| Confirm / Cancel | 1339 / 1554, 837 | 195 × 45 |
| İpucu Close düğmesi | — | 157 × 58 |

Puntolar: başlık **47** · sayfa **34** · "Multiple Selling" **29** ·
"Sell selected items." **22** · "Total Amount :" **25** · tutar **26** · diyalog **30**.

## Saydamlık

| panel | geçirgenlik | alfa |
|---|---:|---:|
| Pencere | 0,035 – 0,073 | **0,96** |
| İpucu kutusu | ~0,08 | **0,92** |
| Diyalog | 0,058 – 0,078 | **0,93** |

Diyalogunki projedeki en güvenilir alfa ölçümü: diyaloğun arkasından sızan
"Multiple Selling", "Sell selected items.", "Total Amount :" ve tutar yazıları,
aynı sayfanın temiz karesiyle piksel piksel oranlandı (n = 731…3634, dört ölçüm
0,922–0,942 arasında). Burada arka planın ne olduğu **biliniyor**, dolayısıyla
kenar yöntemindeki "arka plan çerçeve boyunca aynı" varsayımına gerek yok.

## Videoda görünmeyen mekanikler

Tam çözünürlük, renk kurallarını ortaya çıkardı:

- **Buy Price rengi paraya bağlı.** Oyuncunun parası 63.261. Pearl Earring 64.000 →
  **kırmızı**; Holy water 70, Fabric Coat 392, Calling Friend Scroll 10.000 → **sarı**.
  Platinum bar 1.000.000.000 → kırmızı. Kural: yetmiyorsa kırmızı, yetiyorsa sarı.
- **Ad ve kalite satırı kaliteye göre renkleniyor:** Regular beyaz, Magic mavi,
  Upgrade mor.
- **Karşılanmayan şart kırmızı.** Oyuncu 41. seviye Mage; "Quilted Pauldron(+1)"
  ipucunda "Defense Ability : 20" beyaz ama "Required Strenght : 62" kırmızı.
- **Sınıf satırı** oyuncunun sınıfı değilse kırmızı: "(Warrior Item)", "(Priest Item)".
- **Derece satırı yeşil:** "Item Grade : Low Class".
- **İpucunda Close düğmesi var** (videoda seçemiyordum).
- **Satın alma iki adımlı:** yığılabilir üründe önce "Buy Item Count:" sayı alanı,
  sonra "Need Money : N" onayı.
- **Satış onayı ayrı metin:** "Earn Money : 106".
- İpucu ve diyalog **içerikle birlikte boyut değiştiriyor** → sabit sprite değil,
  9-slice çerçeve + otomatik yerleşim.

## Sprite'lar

`kaynak/npc_dukkan/`: `npc_dukkan_krom.png` (750 × 1156, RGBA),
`diyalog_cerceve.png` (9-slice altın çerçeve, içi saydam),
`btn_close.png`, `btn_confirm.png`, `btn_cancel.png`.

Krom üretimi: dükkân ızgarasının boş 2. satırı 1. satırın üzerine, envanterin boş
3. satırı dolu satırların üzerine kopyalandı; başlık yazısı çubuğun süs deseni
(periyot **47 px**) faz korunarak döşenerek silindi; sayfa numarası ve tutar yan
zeminden örneklenerek temizlendi.

## Doğrulama

Kurucunun üreteceği yerleşim Python'da simüle edilip orijinalle karşılaştırıldı
(`onizlemeler/cmp_npc_dukkan.png`). Simülasyon gerçek bir hata yakaladı: slot
zeminleri kromda opak olduğu için ikonlar kromun **üstünde** oluşturulmalı —
kurucudaki sıra buna göre düzeltildi.

# 24 · Power Up Store (tek paket)

Kaynak: 12 telefon ekran görüntüsü (2712 × 1220): Main Page, Power-UP (2 sayfa), Premiums, Scrolls (2 sayfa), Special, Package, paket içeriği,
Cash Code sayfası, satın alma ayrıntısı (Teleport Scroll), satın alma başarılı. Paket `unity_paketleri/OlymposPowerUpStore1298.unitypackage`
(sınıflar `OlymposPowerUp*`, menü `OLYMPOS > 1298 > Power Up Store Oluştur`). Araçlar `araclar/powerup/`, sprite + ölçüler `kaynak/powerup/`,
önizlemeler `onizlemeler/powerup_*_onizleme.png` (12 ekranda ortalama fark 0.4–3.9 / 255).

## Ölçümler
- Mağaza arka planı bütün sayfalarda piksel piksel aynı → kart / örtü saydamlığı doğrudan ölçüldü.
- **Lineer karışım:** kart içi lineer uzayda O = t·B (sabit ≈ 0, üç kanal eşit); sRGB'de kanallar ayrışıyor. Kategori t = 0.30, Main Page t = 0.185.
- Başarı örtüsü: lineer O = 0.76·B + 0.058 → gri 0.24 (sRGB ~135), alfa 0.24. Açılır pencerelerin içi opak (arka plan katsayısı ≈ 0).
- Mağaza zemini Package sayfasından; sütun 1 satır 1 kartının altı lineer geri çözüldü (B = O / 0.30), ikon/yazı/düğme izleri rötuşlandı (oyunda o konumda hep kart var).
- Kartlar: kategori çerçeve 288 × 289 (sprite 292 × 315, düğme 146 × 66), Main Page 292 × 291 (sprite 294 × 315, düğme 244 × 59).
- Yazılar (`punto.py`): fiyat Liberation Sans Bold 31 +1.5 (IoU 0.84), ad Roboto Bold 22 (0.70), Cash LB 37 (0.91), ayrıntı başlığı LB 29 +0.5,
  adet LB 36 +1.5, açıklama Roboto Bold 33, ayrıntı fiyatı LB 37, başarı mesajı LB 30, yer tutucu LB 29 +0.5.
- Fiyat ≤ Cash → sarı #FDDE24 ve vurgulu Purchase (Teleport Scroll, fiyat 0). Main Page için vurgulu düğme görüntüsü yok (yalnız renk değişir).
- Fiyat yazısı para ikonunun sağından sabit aralıkla, sola yaslı (uzun fiyatlarda ikon kaymaz).
- Cash Code'daki üçüncü taraf logosu alınmadı (boş yuva). Orijinal yazım hataları korundu: "Puchase", "Succcessfully".
- Unity'de denenmedi.

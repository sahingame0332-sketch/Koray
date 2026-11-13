# 09 · Merchant, Slave Merchant, Equip / UnEquip, eşya bilgi penceresi

Kaynak: `Merchant.zip` (13,9 s) ve `Slave_Merchant.zip` (8,3 s) videoları — 2712 × 1220, H.265 — ve üç ekran görüntüsü
(Equip, UnEquip, NPC dükkânı eşya bilgisi).
Paket: `unity_paketleri/OlymposMerchant1298.unitypackage` · kaynak: `unity_kaynak/Assets/OlymposMerchant1298/`
Önizleme: `onizlemeler/merchant_onizleme.png` (orijinal ↔ yeni, 12 panel).

## Yöntem (`araclar/merchant/`)
| Adım | Araç | Not |
|---|---|---|
| Sabit kareler | `oyun_ici/medyan.py` | 19 an; referanslar `referans_gorseller/merchant/` (JPEG q92, 4:4:4) |
| Krom ayırma | `cikar.py`, `ortak.py` | krom siyaha karşı çözülür (ayrı siyah zemin Image'ının üstünde orijinali verir) |
| Pencere dışı | `maske.py` | çim sınıflandırması (kenardan taşma) ya da önce/sonra farkı |
| Yuvalar | `cikar.py` | ızgaralar halka şablonu eşleştirmesiyle oturtuldu; dolu yuvalar aynı pencerenin boş yuvasıyla değiştirildi; **dolu yuvanın açık renkli çerçevesi** ayrı sprite |
| Font / punto | `punto.py` | mürekkep genişliği + IoU |
| Doğrulama | `kur.py` | kurucunun benzetimi → `onizlemeler/merchant_*.png` |

## Saydamlıklar (ölçüldü)
| Öğe | Alfa | Ölçüm |
|---|---|---|
| Komut menüsü zemini | **0.94** | önce/sonra oranı 0.93–0.95 (iki video) |
| Create a Merchant zemini | **0.95** | zemin/çim oranı 0.945; yuva içi 0.95–0.97 |
| Fiyat diyaloğu zemini | **0.97** | önce/sonra 0.968 |
| Tezgâh çubuğu yuva içi | **0.87** | önce/sonra 0.87–0.88 |
| "<ad> Merchant" zemini | **0.89** | zemin/çim 0.891 (yuva içi 0.945) |
| Slave Merchant zemini | **0.95** | önce/sonra 0.948 |
| Eşya bilgi penceresi | **0.93** | üç örnek 0.92–0.96 |

## Ölçüler (ekran pikseli, 2712 × 1220)
- **Komut menüsü** (2322,97) 314×1015 — düğmeler x=2336, y=207+116k, 290×62 (8 adet); kapat merkezi (2489,153).
- **Create a Merchant** (1573,51) 756×851 — tezgâh 6×2: x=1637+111c, y=163+110r, 102×100 · envanter 7×4: x=1613.8+99.67c,
  y=414+100.9r, 103×101 · OK (1792,841) 157×57 · CANCEL (1981,841) 160×57.
- **Fiyat diyaloğu** (1605,208) 711×522 — sayı: eğik, `#EBDFCD`, punto 46, mürekkep solu x=1819, üst y=566 ·
  OK (1751,645) 200×63 · CANCEL (1967,645) 202×63. Uyarı metni (TR + EN) orijinal piksellerden.
- **Tezgâh çubuğu** (1159,551) 404×168 — 4 yuva x=1186+86i, y=560, 86×88 · OPEN (1182,655) 179×60 · WHISPER (1361,655) 178×60.
- **"<ad> Merchant"** (945,113) 785×987 — başlık Roboto Slab Regular 33 `#DDA96A`, merkez x=1335.5 · para Roboto Bold 36 beyaz,
  sağ kenar x=1618, üst y=538 · tezgâh 6×2: x=974.7+120.31c, y=228.8+121.17r, 117×114 · envanter 7×4: x=967.8+103.64c,
  y=588.9+104.4r, 104×102 · OK (1155,1033) 163×56 · Cancel (1352,1033) 157×56.
- **Slave Merchant** (1444,90) 1002×1027 — satır (1460,294+92i) 946×96: ikon (57,15) 70×68, sayaç x=169 (Slab Bold 26),
  durum merkezi x=465.5 (Slab Bold 28) · yenile (2228,120) · kapat (2310,118) · CLAIM COINS (2193,256) 221×62 ·
  Close Slave Merchant (1710,1038) 431×70.
- **Yuva bindirmeleri:** "+N" yükseltme etiketi sağ üstte mor `#CA89E2` (punto ≈ yuva yüksekliği × 0.33); adet sağ altta
  (× 0.27, dış hatlı). İkonun kendisinde yoklar — bilgi penceresindeki ikon etiketsizdir.

## Eşya bilgi penceresi (tek yerleşim, altı kullanım)
Altı örnekte (Equip, UnEquip, NPC, tezgâh kurulumu, Merchant penceresi, tezgâh çubuğu) ikon çerçevesi ve Close düğmesi
şablon eşleştirmesiyle bulundu; hepsi aynı kurala uyuyor (±2 px):

| Öğe | Değer |
|---|---|
| İkon çerçevesi / ikon | (5,5) 103² / (12,12) 89² |
| Ad · tür | x=115 · Roboto Bold 36 / 27 · üst y=13 / 50 |
| Fiyat satırı (varsa) | x=12, üst y=139, Roboto Bold 32 — `Buy Price :` `#FBD20C`, `Purchase Price :` `#B42A99` |
| 1. ayırıcı | y=147 (fiyatsız) / 194 (fiyatlı) |
| Statlar | ilki ayırıcı + 36, adım 38.7, Roboto Bold 29 — beyaz `#FFE7E9`, bonus `#98BF2A`, zehir `#81C267`, kırmızı `#FE0001` |
| 2. ayırıcı | son stat + 48 |
| Ortalı blok | ilki ayırıcı + 35, adım 31.5, Roboto Bold 27: **[sınıf]** · **[boş satır + cins]** · derece `#88C273` · açıklama |
| 3. ayırıcı · düğmeler | son satır + 59 · + 13 · 155×62, x=12 ve 173 |
| Genişlik · yükseklik | en sağdaki mürekkep + 33 (en az 346) · düğme y + 65 |
| Konum | sağ-üst köşe = yuva merkezi + (−34, −17); alt kenar ekran altından 100 px yukarıda kalır |

Doğrulanan yükseklikler: Equip/UnEquip 613 · NPC 678 · tezgâh kurulumu 717 · Merchant penceresi 717 · tezgâh çubuğu 668.
Sınıf satırı sınıf uyuyorsa beyaz ("(Magician Item)"), uymuyorsa kırmızı ("(Rogue Item)").

| Kullanım | Fiyat satırı | Düğmeler |
|---|---|---|
| Envanter eşyası | — | Equip · Close |
| Kuşanılmış eşya | — | UnEquip · Close |
| NPC dükkânı | Buy Price (sarı) | Close |
| Create a Merchant tezgâhı | Purchase Price (mor) | Remove · Close |
| "<ad> Merchant" penceresi | Purchase Price (mor) | Close |
| Tezgâh çubuğu yuvası | — | Close |

## Çalışma mantığı (videolardan)
1. **Commands** → komut menüsü. **OPEN MERCHANT** → Create a Merchant.
2. Envanterde eşyaya dokun → fiyat diyaloğu (alan "0" ile açılır, cihazın sayı klavyesi gelir, yazılan değer "99,999"
   biçiminde görünür) → OK → eşya envanterden çıkıp ilk boş tezgâh yuvasına geçer.
3. Tezgâhtaki eşyaya dokun → bilgi penceresi (Purchase Price, Remove / Close).
4. OK → pencere kapanır, karakterin üstünde **tezgâh çubuğu** belirir (ilk 4 eşya + OPEN / WHISPER).
5. OPEN → "xMegaTon Merchant" penceresi (tezgâh + para + envanter, OK / Cancel); eşyaya dokun → bilgi (Close).
6. Tezgâh çubuğundaki yuvaya dokun → fiyatsız bilgi penceresi.
7. **SLAVE MERCHANT** → durum penceresi: satır başına ikon, "1/0", "Not sold yet."; bilgi satırına
   `Slave Expire Time : 07Hour:59Minute`. İki video arasında tezgâh kapatılmış: bilgi satırında `Merchant Items Received`.
8. **Equip / UnEquip:** Silan Boots kuşanılınca HP 419→434, MP 1162→1177 (eşyadaki "Bonus HP : 15", "Bonus MP : 15").

## Ek: toplu eşya koyma (adet) ve süre çubuklu satın alma onayı
Kaynak: iki tablet ekran görüntüsü, **2266 × 1488, kayıpsız PNG** (`referans_gorseller/merchant/t_adet.png`, `t_satinal.png`).
Tablet düzeni telefon düzeninin **1.0405** katı (diyalog genişliği 740 ↔ 711; pencere şablonu eşleştirmesi 1.04–1.05).
Sprite'lar tablet çözünürlüğünde saklanır; kurucu ölçüleri `T(v) = v / 1.0405` ile telefon birimine çevirir.
Araçlar: `araclar/merchant/cikar2.py` (sprite), `kur2.py` (benzetim → `onizlemeler/merchant_adet_satinal_onizleme.png`).

**Adet penceresi** — tablet (1170,325) 740×543 → 711×522; Create a Merchant içinde fiyat diyaloğuyla **aynı yerde**.
- Zemin alfası **0.94**: diyalogun ardındaki yuva kenarlarının kontrastı 8.4, görünen yuvalarınki 146.5 → geçirgenlik 0.057.
- Başlık "Please enter the quantity of the item." Roboto Bold 27–28, `#FF8787`; uyarı metni (TR + EN) Roboto Slab — hepsi orijinal piksel.
- Alan: yuvarlak uçlu, (137,358) 462×72, içi opak `#1B1917`; sayı eğik, `#D6D6D6`, punto 46, mürekkep solu x=219, üst y=377.
- OK (154,457) 204×65 · CANCEL (380,457) 207×65.

**Satın alma onayı** — tablet (864,416) 577×530 → 554×509; Merchant penceresine göre (153,179).
- Zemin **mat**: aynı ölçümle geçirgenlik 0.003–0.008 → alfa 0.99.
- İkon çerçevesi (238,23) 98×96, ikon (245,30) 84×82, "+N" mor `#CA89E2` punto 29.
- Süre çubuğu: oluk (58,144) 460×24, dolgu (60,147) 455×17 turuncu `#E18E0F` (üstten alta açılan ton); sayaç dolgunun ucunda,
  Roboto Bold 19, `#FFE6E6`, dış hatlı. Karede dolgu %49, sayaç "2".
- Sarı iki satır (`#EBE680`, "Itemin Gradesini ve Fiyatını Kontrol Edin." / "Check the Grade and Price of the Item.") ve
  pembe başlık (`#FF8787`, "Please enter the item's price.") orijinal piksel.
- Fiyat yazısı Text: Roboto Bold 27, `#D9C3C3`, fiyat `#FFD300`; ortalı (merkez x=295.5), 470 genişlikte sarar, satır adımı 31,
  ilk satırın mürekkep üstü y=288 → "[Price: 99,999,999 ] Will you buy this" / "item?" / "Please double check the price".
- Düğmeler (115,437) ve (332,437), 156×64. **OK soluk:** zemini Cancel'ın 0.56 katı (gövde 26/32/39 ↔ 56/66/78), yazısı aynı
  parlaklıkta → zemin + yazı ayrı sprite; kapalıyken yalnız zemin 0.56'ya iner.
- Aynı karedeki bilgi penceresinde fiyat **kırmızı** `#FF0000` (para 174,472 < 99,999,999). Sahibinin baktığı videoda
  (para 523,455, fiyat 99,999) mordu → kural: para yetmiyorsa kırmızı.

**Akış:** yığınlı eşyaya dokun → adet → fiyat (tek eşyanın) → girilen adet tezgâha geçer, kalan envanterde kalır; Remove / CANCEL /
Close Slave Merchant'ta yığın geri birleşir. Merchant penceresinde eşyaya dokun → bilgi; aynı eşyaya yeniden dokun → onay;
çubuk dolunca OK açılır → eşya envantere geçer, para düşer.

**Ayrı paketler:** kullanıcı isteğiyle iki pencere tek başına da verildi — `OlymposAdetPenceresi1298.unitypackage`
(`OlymposAdetPenceresi`, `Ac(adet)`, `onOnay(int)`) ve `OlymposSatinAlmaOnayi1298.unitypackage` (`OlymposSatinAlmaPenceresi`,
`Ac(ikon, yukseltme, fiyat)`, `onOnay(long)`). Sınıf adları Merchant paketindekilerden farklı; birlikte içe aktarılabilir.
İkisi de `acilistaGoster` ile ekran görüntüsündeki örnek değerlerle açık gelir.

**Bu ekteki varsayımlar:** onayın ikinci dokunuşla açılması · bekleme süresi 4 sn · sayacın kalan saniye oluşu · OK'nin süre dolunca
açılması · yığında tutarın fiyat × adet oluşu · adet alanının yığının tamamıyla açılması · çubuğun boş kısmındaki iki küçük işaretin
(x=316 ve 396) anlamı (piksel olarak korundu).

## Ek: alıcı görünümü — başka oyuncunun tezgâhı
Kaynak: iki telefon ekran görüntüsü, 2712 × 1220 (`referans_gorseller/merchant/a_cubuk.jpg`, `a_pencere.jpg`).
Paket: **`unity_paketleri/OlymposMerchantAlici1298.unitypackage`** (tek başına; kullanıcı ayrı paket istedi).
Araçlar: `araclar/merchant/cikar3.py`, `kur3.py` → `onizlemeler/merchant_alici_onizleme.png`.

- Tezgâh çubuğu ve pencere, sahibinin gördüğüyle **aynı sprite ve ölçülerde** (çubuk altı alt-şablonla eşleştirildi: (955,241);
  pencere (945,113) — önceki konumla aynı).
- **Satıcı adı** çubuğun üstünde: DejaVu Sans Bold 30 (IoU 0.56; Roboto 0.37), beyaz, siyah dış hat; mürekkep üstü çubuğun
  35 px yukarısında, merkez çubuk merkezinin 4.5 px solunda.
- **Mor çerçeve:** gümüş çerçevenin dışında ~3 px mor kenar (`#AF66A5` dolayı). Mor çerçeveli yuvada ikon alanı küçülüyor:
  çubukta (16,12) 62×66 (gümüşte (8,8) 70×72), pencerede (12,12) 93×90 (gümüşte (8,8) 101×98).
  Bu karelerde +1 silahlar mor; önceki videodaki +5 yay gümüştü → **kural bilinmiyor**, eşya başına işaretlenir.
- **"+N" etiketi** (`#CA89E2`): çubukta mürekkep x 43..77, y 13..34 → Roboto Bold 31; pencere üst yuvalarında x 77..109, y 11..28 →
  Roboto Bold **25**. Gümüş çerçeveli +5 ile aynı yerde. Orijinal biraz daha kalın → aynı renkte ince dış hat.
  (Merchant paketinin kurucusu üst yuvalarda 0.33 × yükseklik = 38 kullanıyor; doğrusu 25 — o pakette düzeltilmedi.)
- Para "9,322" Roboto Bold 36, sağ kenar x=1618–1620: sağa yaslı (önceki ölçümle aynı).
- Alıcının envanterindeki süreli parşömenin adet rakamı ikonun pikselinde kaldı (temizlenemedi).
- Tezgâh sancağı (çubuğun yanındaki kırmızı-mavi bayrak) oyun dünyasındaki 3B nesne; arayüz değil.

## Varsayımlar (videoda yok)
Satılmış eşyanın durum yazısı · CLAIM COINS'in etkisi · 8'den fazla satır · slave süresinin başlangıcı
ve 8 saat oluşu · tezgâh yokken SLAVE MERCHANT, tezgâh açıkken OPEN MERCHANT · 0 fiyat ve boş tezgâh · sınıfı uymayan
eşyanın kuşanılamaması · Merchant penceresinde OK ile Cancel farkı · fiyat alanının eğik fontu.
Hepsi kodda "varsayım" yorumuyla işaretli.

## Doğrulama
- Mono `mcs`: tüm paketler birlikte **0 hata, 0 uyarı**.
- Paket ↔ `unity_kaynak`: 66 girdi, 60 dosya, GUID + SHA-256 **0 sorun**; kurucudaki sprite kutuları sprite boyutlarıyla eşleşiyor
  (tablet kaynaklı 8 sprite 1.0405 oranında küçültülerek gösterilir).
- Equip / UnEquip / NPC panellerinde tek kare olduğu için benzetim, orijinal kutunun yeri düz siyaha boyanarak çizildi.
- **Unity'de import denenmedi.**

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

## Varsayımlar (videoda yok)
Satın alma akışı · satılmış eşyanın durum yazısı · CLAIM COINS'in etkisi · 8'den fazla satır · slave süresinin başlangıcı
ve 8 saat oluşu · tezgâh yokken SLAVE MERCHANT, tezgâh açıkken OPEN MERCHANT · 0 fiyat ve boş tezgâh · sınıfı uymayan
eşyanın kuşanılamaması · Merchant penceresinde OK ile Cancel farkı · fiyat alanının eğik fontu.
Hepsi kodda "varsayım" yorumuyla işaretli.

## Doğrulama
- Mono `mcs`: tüm paketler birlikte **0 hata, 0 uyarı**.
- Paket ↔ `unity_kaynak`: 56 girdi, 50 dosya, GUID + SHA-256 **0 sorun**; kurucudaki 18 sprite kutusu sprite boyutlarıyla eşleşiyor.
- Equip / UnEquip / NPC panellerinde tek kare olduğu için benzetim, orijinal kutunun yeri düz siyaha boyanarak çizildi.
- **Unity'de import denenmedi.**

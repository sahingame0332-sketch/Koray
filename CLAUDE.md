# OLYMPOS-KO · 1298 Mobil Arayüz — Claude Code proje bağlamı

Bu depo, claude.ai'daki "OLYMPOS arayüz" sohbetinin devamıdır. Arayüz çalışmasının tamamı `arayuz/` altındadır;
sohbetin adım adım kaydı: `arayuz/00-sohbet-ozeti.md`. Kullanıcıyla **Türkçe** konuş.

Deponun geri kalanı aynı oyunun altyapı tarafıdır (veri modeli, içerik üretimi, APK analizi) — bkz. `README.md` ve `docs/`.
Arayüz işi ile altyapı işi aynı oyunun iki yüzü: `docs/03-icerik-uretim-rehberi.md` içindeki UI ekran envanteri bu pencerelerle eşleşir.

## Proje
- Oyun: **OLYMPOS-KO**, Knight Online **1298** istemcisi tarzında bir **mobil** oyun, **Unity** ile geliştiriliyor.
- Görev: kullanıcının gönderdiği oyun arayüzü ekran görüntülerini **birebir** Unity'ye aktarılabilir pencerelere çevirmek.
- Kullanıcının referans arşivi (`ara_yüz_görselleri.rar`, kendi bilgisayarında): `01_Onizlemeler`, `02_Unity_Gorselleri`,
  `03_Hazir_Paketler` (`1298_Mobil_Arayuz_Unity_Hazir`, NPC pencereleri, Moradon referansı), `04_1298_Font_Referanslari`
  (UIF font kayıtları CSV: 3.698 kayıt; çoğunluk Arial, sonra Gulim). Proje tercihi başlık/etiket fontu: **Roboto Slab Bold**.

## Kullanıcının çalışma tarzı ve kuralları (önemli)
1. **Birebir.** Yazılar, fontlar, renkler, çerçeveler, buton zeminleri **orijinal görselden alınır**; yeniden çizilmez/tasarlanmaz.
   Yöntem: ilgili parçayı orijinalden kes → üstündeki yazıyı sil (aynı satırdaki gerçek dokudan örnekleyerek doldur) → yazısız sprite.
   Küçük, oyun içi boyuttaki görsellerde yazılar da orijinal piksellerden korunur.
2. **Önce görsel.** Dosya/doküman/paket yapmadan önce sonucu **görsel olarak** göster (orijinal ↔ yeni yan yana).
   Kullanıcı onaylayınca ("Süpersin… Unity editöre aktarabileceğim şekilde dosya haline getir") Unity paketine geç.
3. **Saydamlık.** Pencere iç zemini **düz siyah** (kahverengi doku YOK) ve **yarı saydam**;
   oyun dünyası arkadan hafifçe görünür. Unity'de ayrı bir siyah Image + Inspector'da `backgroundAlpha` ile ayarlanır.
   Pencere dışında kalan oyun sahnesi parçaları **tamamen saydam**. Kutular/butonlar **opak**.
   Alfa değerleri **orijinal ekran görüntülerinden ölçüldü** (bkz. `arayuz/04-saydamlik.md`), varsayılmadı:
   Character **0.92** · Ana menü **0.92** · Stat butonları **0.92** · OPTIONS dış alan **0.95**.
   İSTİSNA: **Save Stat Preset** **mat** (ölçüm: alfa 0.99) ve **OPTIONS içerik paneli** opak (kendi siyah zemini var).
   Yeni pencerede alfa tahmin edilmez: `araclar/saydamlik_olcumu/saydamlik.py` ile ölçülür.
4. Kullanıcı "Dur" derse hemen dur, durumu kısaca söyle, bekle.

## Teslim edilenler
| Paket | Pencere | Boyut (px) | Zemin |
|---|---|---|---|
| `arayuz/unity_paketleri/OlymposCharacter1298.unitypackage` | Character › CHAR INFO sekmesi | 654 × 1030 | yarı saydam siyah **0.92** |
| `arayuz/unity_paketleri/OlymposStatWindows1298.unitypackage` | SAVE STAT PRESET | 293 × 454 | mat |
| (aynı paket) | Stat butonları STR/HP/DEX/INT/MP | 197 × 243 | yarı saydam siyah **0.92** |
| `arayuz/unity_paketleri/OlymposCharacter1298.unitypackage` | Character › CLAN ve FRIENDS sekmeleri | 654 × 1030 | yarı saydam **0.92** |
| `arayuz/unity_paketleri/OlymposMenuOptions1298.unitypackage` | Ana menü paneli | 321 × 989 | yarı saydam **0.92** |
| (aynı paket) | OPTIONS (11 sayfa) | 854 × 1171 | dış **0.95**, içerik paneli opak |
| `arayuz/unity_paketleri/OlymposNpcShop1298.unitypackage` | NPC dükkânı + diyalog + ipucu | 750 × 1156 | yarı saydam (bkz. `arayuz/05-npc-dukkan.md`) |
| `arayuz/unity_paketleri/OlymposOyunIci1298.unitypackage` | Oyun içi: eşya penceresi, buff çubuğu + Remove, hızlı slotlar, Save Skill Slot, hedef + Show Drops + Drop List, hedef iptal X | 2712 × 1220 ekran (kendi Canvas'ı) | 0.92 / 0.89 / 0.93 / 0.95, slot içi 0.88 (bkz. `arayuz/06-oyun-ici.md`) |
| `arayuz/unity_paketleri/OlymposZemin1298.unitypackage` | Zemin: 5 döşenebilir doku, kontrol + renk haritası örnekleri, `Olympos/Zemin1298` shader, ortam rengi | 256² / 128² | — (bkz. `arayuz/08-zemin.md`) |
| `arayuz/unity_paketleri/OlymposMerchant1298.unitypackage` | Komut menüsü, Create a Merchant + fiyat diyaloğu, tezgâh çubuğu, "<ad> Merchant", Slave Merchant, adet girişi (toplu eşya), süre çubuklu satın alma onayı, eşya bilgi penceresi (Equip / UnEquip / Remove / Buy Price / Purchase Price) | 2712 × 1220 ekran (OyunIci ile ortak Canvas) | 0.94 / 0.95 / 0.97 / 0.89 / 0.95 / 0.93, tezgâh yuvası 0.87 (bkz. `arayuz/09-merchant.md`) |
| `arayuz/unity_paketleri/OlymposAdetPenceresi1298.unitypackage` | Adet girişi penceresi — tek başına (Merchant paketindekinin bağımsız kopyası; sınıf `OlymposAdetPenceresi`) | 711 × 522 | yarı saydam **0.94** |
| `arayuz/unity_paketleri/OlymposSatinAlmaOnayi1298.unitypackage` | Süre çubuklu satın alma onayı — tek başına (sınıf `OlymposSatinAlmaPenceresi`) | 554 × 509 | mat (0.99) |
| `arayuz/unity_paketleri/OlymposMerchantAlici1298.unitypackage` | Merchant alıcı görünümü — tek başına: satıcı adlı tezgâh çubuğu (mor çerçeveli yuvalar) + "<ad> Merchant" penceresi (sınıflar `OlymposSatici*`) | 404 × 168 / 785 × 987 | yuva 0.87 / **0.89** |

Kaynaklar `arayuz/unity_kaynak/Assets/...` (meta dosyalarıyla). Unity menüsü:
`OLYMPOS > 1298 > Character Penceresi Oluştur` (CHAR INFO + CLAN + FRIENDS sekmeleriyle birlikte),
`… > Save Stat Preset Penceresi Oluştur`, `… > Stat Butonları Penceresi Oluştur`,
`… > Ana Menü Paneli Oluştur`, `… > OPTIONS Penceresi Oluştur`.
`… > NPC Dükkân Penceresi Oluştur`, `… > Oyun İçi (Scroll · Skill Slot · Drops · Hedef) Oluştur`
(sonuncusu 2712×1220 referanslı ayrı bir Canvas kurar; diğerleri 1920×1080).
`… > Zemin Malzemeleri Oluştur` (arayüz değil: malzemeler + deneme zemini; namespace `Olympos.Zemin`).
`… > Merchant (Tezgâh · Slave · Equip · Eşya Bilgisi) Oluştur` (OyunIci'nin 2712×1220 Canvas'ını paylaşır).
`… > Adet Penceresi Oluştur`, `… > Satın Alma Onayı Penceresi Oluştur`, `… > Merchant Alıcı Görünümü Oluştur` (tek başına paketler; aynı Canvas).
Kurucular: doku import ayarları (Sprite, sıkıştırmasız, mipmap yok, 9-slice kenarlar) → hiyerarşiyi **sol-üst piksel
koordinatlarıyla** kurar → `Prefabs/` altına prefab → sahnedeki Canvas'a ekler (yoksa 1920×1080, match=1 Canvas + EventSystem).
UI sistemi: **uGUI + legacy `UnityEngine.UI.Text`** (TMP kullanılmadı). Namespace `Olympos.UI` / `Olympos.UI.EditorTools`.

**Doğrulama durumu:** Yerleşim Python/Chrome ile simüle edilip orijinalle karşılaştırıldı.
Claude Code'a devirden sonra Mono (`mcs`) kurulup betikler **derlendi: 0 hata, 0 uyarı**; paketlerin arşiv yapısı,
GUID'leri ve dosya içerikleri `unity_kaynak/` ile birebir eşleşiyor. Font kalibrasyonundan sonra ölçülen
31 yazı bölgesinde orijinale örtüşme 0.478 → **0.627** (31/31 iyileşti). **Unity'de import hâlâ denenmedi** (ortamda Unity yok).
Ayrıntı: `arayuz/01-dogrulama.md` (derleme/paket) ve `arayuz/02-font-kalibrasyonu.md` (font/punto).
Kontroller: `arayuz/araclar/derleme_kontrolu/derle.sh`, `arayuz/araclar/font_kalibrasyonu/olc.py`.

## Char Info (654×1030) ölçüleri
Renkler: etiket beyaz `#F4F4F4`, isim `#F2E79C`, turuncu etiket (Exp/NP/Attack/Defence) `#E2B47C`, değer tan `#DCB98A`,
stat puanı yeşil `#A6DC3C`, Stat Reset turuncu `#D98A34`, kutu kenarı tan `#DFC5AE`.
Sprite'lar (`arayuz/unity_kaynak/Assets/OlymposCharacter1298/Resources/OlymposCharacter1298/`): `window_frame` (bronz çerçeve 9px, içi saydam), `tabs_strip` (637×92 @ 9,8;
orijinal doku, CHAR INFO altın alt çizgisi dahil), `label_button` (9-slice L18 B8 R8 T8), `value_box` (9-slice 6),
`btn_preset`/`btn_reset` (145×45), `race_human` (57×57 @ 64,116, dairesel alfa).
Sekmeler: CHAR INFO (15,10,200,82) · QUESTS (224,10,128,82) · CLAN (365,10,156,82) · FRIENDS (525,10,120,82).
Diğer tüm koordinatlar `OlymposCharacterWindowBuilder.cs` içinde.
Font: **Roboto Slab Bold v2.002** artık pakette (`Fonts/RobotoSlab-Bold.ttf`, her iki pakette de).
Puntolar bu fonta göre ölçülerek kalibre edildi — sekme 21, etiket 21, HUMAN 20, isim 25, Magician 22,
stat adı 21, stat değeri 25, direnç adı 19, direnç değeri 23, buton 22. Değiştirmeden önce
`arayuz/02-font-kalibrasyonu.md` oku; puntolar fonta bağlı, font değişirse yeniden ölçülmeli.

## Stat pencereleri ölçüleri
- Save Stat Preset: orijinal 299×479'dan (3,8)-(296,462) kesildi. Slot aralığı **103 px**; slot 2–4 temiz **slot 1**'den üretildi
  (orijinalde 2. ve 3. slotta arkadaki stat penceresinin hayalet izleri vardı), numara rozetleri her slotun kendisinden.
  Tıklama alanları (sprite koordinatı): Kapat (246,3,28,28); slot k için Save (49,107+103k,95,25), Activate (148,107+103k,95,25);
  "- Empty -" örtüsü/metni (74,80+103k,146,16) → `SetSlotStatus(slot, text)`.
- Stat butonları: orijinal 202×251'den (2,0)-(198,242). Çerçeve 3 px. Butonlar x=21, w=163, h=38, y = 22/65/108/151/194.
  `stat_buttons_frame.png` = çerçeve + butonlar, içi saydam; siyah zemin ayrı Image.
- Butonlar: görünmez Image + ColorTint (normal α0, hover α0.12, basılı α0.35, disabled α0.45 siyah).

## Araçlar (`arayuz/araclar/`)
- `rar5list.py` / `rar5stored.py`: RAR5 başlık okuyucu; arşivdeki sıkıştırılmamış (stored) ZIP'i çıkarır (ortamda unrar yoktu).
- `mkunitypkg.py <klasör> <çıktı.unitypackage> <çıktı.zip>`: `Assets/` altındakilere yoldan türetilen sabit GUID'li minimal
  `.meta` yazar, `.unitypackage` (tar.gz: guid/asset, asset.meta, pathname) ve zip üretir.
- `build_windows2.py`: Save Stat Preset + stat butonları sprite'larını orijinallerden üretir (`preset_orig.png`, `stats_orig.png` bekler).
- `derleme_kontrolu/derle.sh`: Unity olmadan tüm `.cs` dosyalarını Mono ile derler (Unity API taslakları yanında).
- `font_kalibrasyonu/`: `font_kimligi.py` (orijinaldeki yazı hangi fonta ait — adayları ölçüp sıralar),
  `olc.py` (önizleme ↔ orijinal bölge bölge örtüşme), `bolgeler.json` (Char Info'daki 31 yazı bölgesi).
  Yeni pencere birebir yapılırken punto bunlarla seçilir, gözle değil.
- `oyun_ici/`: `medyan.py` (video karelerinin medyanı), `cikar.py` (pencereli/penceresiz kare farkıyla krom ayırma),
  `punto.py` (font + punto), `kur.py` (kurucunun benzetimi → `onizlemeler/oyun_ici_*.png`). `hud/`: yarım HUD işinin araçları.
- `merchant/`: `cikar.py` (krom + maske + yuva şablonu), `maske.py`, `punto.py`, `kur.py` (benzetim → `onizlemeler/merchant_*.png`).
  `cikar2.py` / `kur2.py`: tablet görüntülerinden adet ve satın alma onayı pencereleri (ölçek 1.0405).
  `cikar3.py` / `kur3.py`: alıcı görünümü (mor çerçeveler, satıcı adı).
- `zemin/`: `duzelt.py` (zemin düzlemini yukarıdan görünüşe çevirir), `zemin.py` (karo + renk ölçümü),
  `haritalar.py` (kontrol/renk haritası örnekleri), `onizle.py` (aynı kamerayla yeniden çizim → `onizlemeler/zemin_onizleme.png`).
- Char Info sprite çıkarımı (OpenCV inpaint + aynı satırdan doku örnekleme) sohbet içinde satır içi yapıldı; sonuçlar
  `arayuz/kaynak/char_info/sprites/`. HTML önizleme: `arayuz/kaynak/char_info/unity_preview.html` (sprite'larla, Moradon arka planı üzerinde).

## Sıradaki olası işler
- **Yarım iş:** oyun içi HUD (durum plakası, sohbet, alt bar, beceri çarkı…). Tablet ölçümleri `arayuz/07-hud-taslak.md` içinde;
  karar: HUD **telefon karelerinden (2712×1220)** kurulacak ki OyunIci/Merchant ile aynı Canvas'a otursun. Başlangıç:
  `araclar/hud_telefon/ortak.py` (çim taşması maskesi `cim_disi` — tamamı çim olan `m_once` karesinde bütün HUD öğelerini ayırıyor).
  Önizleme/paket yok.
- Kullanıcı son isteklerde her görseli **ayrı paket** olarak istedi ("ayrı paket olarak hazırla"): yeni pencereler tek başına,
  çakışmayan sınıf adlarıyla paketlenmeli. Merchant paketindeki "+N" puntosu üst yuvalarda 38; ölçülen 25 (bkz. 09 eki) — düzeltilebilir.
- Merchant paketi teslim edildi (`arayuz/09-merchant.md`, adet + satın alma onayı eki dâhil). Hâlâ varsayım: onayın nasıl
  açıldığı, bekleme süresi, satılmış eşyanın Slave Merchant'taki durumu — kayıt gelirse gerçek davranışla değiştirilmeli.
- Zemin paketi teslim edildi (`arayuz/08-zemin.md`); kullanıcı Unity'de deneyince shader derleme çıktısı ve
  karo ölçeği/en-boy rötuşu gerekebilir (görüş açısı 60° varsayıldı).
- Kullanıcının Unity'de ilk import sonucunu almak, Console çıktısındaki hataları düzeltmek.
  (Beklenen tek uyarı: Unity 2023.1+ için eskimiş `FindObjectOfType` — hata değil.)
  Aynı denemede puntoların Unity'de de tutup tutmadığına bakılmalı (±1 rötuş gerekebilir).
- Üç pencerenin ölçeklerini birbirine oranlamak (Char Info daha büyük bir ekran görüntüsünden geldi).
- OPTIONS sayfalarındaki onay kutuları ve kaydırıcıları etkileşimli hâle getirmek
  (şu an sayfa görselinin parçası; her iki durum da kaynak ekranlarda mevcut).
- QUESTS sekmesi — ekran görüntüsü gelince, aynı yöntemle.
- Kullanıcının göndereceği yeni pencereler.

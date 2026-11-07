# Roboto Slab Bold: font temini ve punto kalibrasyonu

Tarih: 7 Kasım 2026

Devir notundaki bilinen tek görsel fark şuydu: *"Roboto Slab bu ortamda yoktu (ağ kapalı);
önizlemelerde DejaVu Serif, Unity'de Roboto Bold yedeği."* Bu belge o farkın nasıl kapatıldığını
ve yol boyunca çıkan ters sonucu anlatır.

## 1. Font temin edildi

Claude Code ortamında ağ var. **Roboto Slab Bold v2.002** Google Fonts üzerinden indirildi:
102 KB, 938 glif, Latin + Türkçe karakterlerin tamamı mevcut.

Kopyalandığı yerler (dördü de bit düzeyinde aynı):
- `unity_kaynak/Assets/OlymposCharacter1298/Fonts/RobotoSlab-Bold.ttf`
- `unity_kaynak/Assets/OlymposStatWindows1298/Fonts/RobotoSlab-Bold.ttf`
- `kaynak/char_info/fonts/RobotoSlab-Bold.ttf` (HTML önizleme)
- iki `.unitypackage` içinde

Kurucular fontu zaten `LoadFont("RobotoSlab-Bold.ttf") ?? LoadFont("Roboto-Bold.ttf")` ile
arıyordu; dosya yerine konduğu için kod değişmeden Roboto Slab'ı kullanıyor ve "font bulunamadı"
uyarısı artık çıkmıyor.

**Lisans:** Roboto Slab, Google Fonts ailesi olarak Apache 2.0 veya SIL OFL 1.1 ile dağıtılıyor;
ikisi de ticari bir oyuna gömmeye izin verir. Hangisi olduğu bu ortamdan kesinleştirilemedi
(GitHub'a erişim kapalı). Hukuken önemliyse teyit edilmeli.

## 2. Düz font değişimi işe yaramadı

Fontu takıp ölçtüğümüzde sonuç **daha kötü** çıktı: en iyi hizalamada ortalama örtüşme
Roboto Slab ile 0.378, DejaVu Serif ile 0.476.

Sebep: önizlemedeki punto değerleri DejaVu'nun metriklerine göre elle ayarlanmıştı. Roboto Slab
aynı puntoda daha küçük çiziyor, dolayısıyla yazılar orijinalin altında kalıyordu. Yani ölçüm
fontu değil, fonta uymayan puntoyu cezalandırıyordu.

## 3. Font kimliği ayrıca test edildi

Puntonun etkisini dışarıda bırakmak için her etiket, her aday fontla 13–28 punto arasında
rasterize edilip en iyi eşleşme alındı (`araclar/font_kalibrasyonu/font_kimligi.py`):

| font | şekil örtüşmesi |
|---|---|
| **Roboto Slab Bold v2.002** | **0.602** |
| Roboto Bold | 0.588 |
| Liberation Sans Bold (Arial metrikleri) | 0.520 |
| Liberation Serif Bold | 0.493 |
| FreeSerif Bold | 0.482 |
| DejaVu Sans Bold | 0.468 |
| DejaVu Serif Bold | 0.418 |

Roboto Slab açık ara önde. Tercih doğruydu; sorun puntodaydı.

## 4. Puntolar kalibre edildi

Her metin grubu için punto taraması yapıldı (önizleme HTML'i render → `olc.py` ile ölçüm),
tepe noktası seçildi. Gruplar ayrı bölgelerde olduğu için bağımsız tarandı.

| grup | nerede | eski | yeni |
|---|---|---:|---:|
| `tab` | CHAR INFO / QUESTS / CLAN / FRIENDS | 20 | **21** |
| `lbl` | Level, Job, HP/MP Point, Exp/NP Points, Attack, Defence, Your Stat Points, Resistance | 19 | **21** |
| `human` | HUMAN | 19 | **20** |
| `name` | karakter adı | 25 | 25 |
| `job` | Magician (Job kutusu) | 19 | **22** |
| `statk` | STR / DEX / INT / HP / MP | 19 | **21** |
| `statv` | stat değerleri (50, 70, 112, 52, 255) | 21 | **25** |
| `resk` | Flame / Poison / Glacier / Lightning Resist. | 18 | **19** |
| `resv` | direnç değerleri | 21 | **23** |
| `btn` | Stat Preset / Stat Reset | 21 | **22** |

Her grupta tepe noktası doğrulandı: bir üstü ve bir altı daha düşük puan veriyor. `lbl` için
22 ve 23 de denendi (0.451 ve 0.401), `statv` için 27'ye kadar çıkıldı (tepe 25'te).

`statv`'nin `statk`'tan dört punto büyük olması tuhaf görünüyor ama orijinal görselde de öyle:
stat değerleri etiketlerinden gözle görülür biçimde büyük.

## 5. Sonuç

| | eski (DejaVu) | yeni (Roboto Slab kalibre) |
|---|---:|---:|
| ortalama örtüşme (31 bölge) | 0.478 | **0.627** |
| iyileşen bölge | — | **31 / 31** |
| kötüleşen bölge | — | **0** |

Grup bazında: `statk` 0.547→0.750, `human` 0.467→0.710, `resk` 0.540→0.669, `tab` 0.505→0.639,
`job` 0.410→0.638, `lbl` 0.462→0.608, `statv` 0.455→0.570, `name` 0.419→0.545, `btn` 0.316→0.394.

Tekrar üretmek için:

```bash
cd arayuz/araclar/font_kalibrasyonu
python3 font_kimligi.py ../../referans_gorseller/CharInfo_Orijinal.jpg
python3 olc.py ../../referans_gorseller/CharInfo_Orijinal.jpg \
    ../../onizlemeler/OLYMPOS_CharInfo_Unity_Onizleme_ESKI_dejavu.png \
    ../../onizlemeler/OLYMPOS_CharInfo_Unity_Onizleme.png
```

Görsel karşılaştırma: `onizlemeler/cmp_font_kalibrasyon.png` (ve `_ust` / `_alt` 2× yakın planlar).

## 6. Açık kalan

- **Unity'de doğrulanmadı.** Puntolar Chromium render'ı üzerinden ölçüldü; Unity'nin uGUI
  `Text` rasterleştiricisi tıpatıp aynı değil. İlk import'ta ±1 punto rötuş gerekebilir.
- `btn` grubu en düşük puanlı (0.394). Stat Reset'in turuncu yazısı turuncumsu buton zemini
  üzerinde olduğu için eşikleme yazıyı zemin dokusundan tam ayıramıyor; rakam olduğundan
  düşük, görsel olarak fark belirgin değil.
- Stat pencerelerinde yazılar orijinal piksellerden geldiği için font etkilemiyor; Roboto Slab
  yalnızca `SetSlotStatus()` ile yazılan metinde kullanılıyor.

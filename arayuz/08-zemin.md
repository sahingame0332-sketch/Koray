# 08 · Zemin dokuları, renk haritası, renk/sıcaklık

İstek: "sadece zemin grafikleri — haritalardaki renk haritası ve zemin dokuları, renk ve sıcaklık; Unity'de kullanacağım kodlar."
Paket: `unity_paketleri/OlymposZemin1298.unitypackage` · kaynak: `unity_kaynak/Assets/OlymposZemin1298/`
Önizleme: `onizlemeler/zemin_onizleme.png` · ham ölçümler: `kaynak/zemin/zemin_olcumleri.json`

## Yöntem (`araclar/zemin/`)
1. **Perspektif düzeltme** (`duzelt.py`): zemin düz kabul edilir, iğne deliği kamera. Dikey görüş açısı **60°**
   (Unity varsayılanı; kum dokusunun en/boy oranı bu değerde 1.00 çıktı — f=1300 px). Ufuk satırı sahne başına:
   hud_01 **232** (doku ölçeğinin satırla büyümesinden 192–260 arası iki tahmin), hud_03 **480** ve hud_04 **470**
   (yol çizgilerinin kaçış noktası / zeminin bittiği satır), v2 videosu **150**.
   Doğrulama: Moradon'da düzeltilmiş görüntüde yol şeritlerinin kenarları paralel çıktı.
2. **Karo** (`zemin.py`): kameraya en yakın temiz bölgeden kare kesilir; büyük ölçekli açık/koyu dalga ayrılır
   (`karo / alçak_geçiren × ortalama`); sol/üst 1/8'lik bant karonun **gerçek devamıyla** harmanlanır → ek yersiz döşenir.
3. **Renk**: ortalama sRGB → XYZ → xy → ilintili renk sıcaklığı (McCamy), Lab, doygunluk.
4. **Doğrulama** (`onizle.py`): karolar aynı kamerayla aynı ekran bölgesine yeniden çizilip orijinalle yan yana kondu.

## Zemin ölçümleri

| Doku | Kaynak | Ort. renk | Renk sıcaklığı | Lab | Doygunluk | Karo | Karo kenarı |
|---|---|---|---|---|---|---|---|
| `zemin_kum` | hud_01 (Diez) | `#B48F57` | **3505 K** | 61.6 / 6.8 / 34.6 | 0.51 | 256² | 5.6 karakter boyu |
| `zemin_tas_doseme` | hud_04 (Moradon) | `#837E6A` | **5133 K** | 52.8 / −1.6 / 11.8 | 0.20 | 256² | 5.2 |
| `zemin_tas_tugla` | hud_04 | `#716C5A` | **5080 K** | 45.5 / −1.2 / 10.9 | 0.21 | 128² | 2.2 |
| `zemin_tas_arnavut` | hud_03 | `#7D7762` | **5022 K** | 50.1 / −1.8 / 12.8 | 0.22 | 128² | 3.1 |
| `zemin_cim` | v2 videosu (kır) | `#31380E` | **4484 K** | 22.1 / −10.2 / 24.4 | 0.75 | 256² | 4.5 |

"Karakter boyu" ölçek birimidir: karakterin ekrandaki boyundan o sahnenin kamera yüksekliğine oranlandı
(0.206 / 0.271 / 0.294 / 0.191 kamera yüksekliği; ±%10). Kurucu `KarakterBoyu = 1.8` ile çarpar.

Moradon yolu **üç dokunun yan yana şeritleridir**: iri döşeme | örgü tuğla (**3.5 karakter boyu** genişlik, iki karede
0.86 ve 0.83 birim) | arnavut kaldırımı.

## Gök ve uzak renk

| Sahne | Gök | Uzak renk (görüş mesafesinin sonu) |
|---|---|---|
| Moradon | `#ADC6D6` (8819 K) | `#D0EA84` limon (4868 K) |
| Kale (Diez) | `#AEC7D7` | `#C0D47E` |
| Kır | `#BFCDDB` (7979 K) | `#B2C7D4` |

Zeminde **kademeli sis ölçülmedi**: Moradon yolunda y=550…640 satır ortalamaları sabit (125,120,99). Uzak nesneler
görüş mesafesinin sonunda tek düz renge dönüyor (kalede limon renkli lamba direği silueti). Görüş mesafesinin kendisi
ekrandan ölçülemedi.

## Renk haritası
- `renk_haritasi_kum.png`: kumun büyük ölçekli dalgası, ortalamaya oranla **0.85 – 1.10** (std 0.054), 7.8 karakter boyu
  kenarlı alandan. Gri 0.5 = değişiklik yok; shader ×2 çarpar.
- `kontrol_kum_cim.png`: hud_01'deki kum → çim geçişi (R kum, G çim; alanın %16'sı çim), 12.2 karakter boyu kenar.
- `kontrol_moradon_yol.png`: ölçülen şerit düzeni (örnek; 32 karakter boyu genişlik).
Haritanın tamamının renk haritası ekran görüntülerinden çıkarılamaz — yalnızca görünen parçalar örnek olarak verildi.

## Unity tarafı
- `Olympos/Zemin1298` shader: ışıksız; 4 katman, dünya XZ ile döşeme, kontrol haritası, renk haritası (×2), `_Renk`.
- `OlymposZeminPaleti`: tablodaki sabitler + `KelvindenRenk`, `SicaklikCarpani`.
- `OlymposOrtamRengi`: ön ayarlar (Moradon / Kale / Kır) → kamera arka planı, sis rengi; `sicaklikKaymasiK`, `parlaklik`.
- Menü: `OLYMPOS > 1298 > Zemin Malzemeleri Oluştur` → 7 malzeme + deneme sahnesi.

## Sınırlar
- Görüş açısı varsayım (60°); taş dokularda bu değerle en/boy ≈0.7–0.8 çıktı (doku yönlü olabilir ya da ufuk ±30 px
  kaymış olabilir) → taşlarda en-boy belirsizliği ≈ ±%25, kumda ≈ ±%10.
- Dokunun gerçek tekrar periyodu bulunamadı (otokorelasyon tepeleri 0.1–0.19, kararsız); karolar kırpma + kenar harmanıdır.
- Çözünürlük kaynakla sınırlı; tuğla/arnavut 128².
- Renkler oyunun ışığı dâhil ekran değerleridir.
- Shader bu ortamda derlenemedi; C# betikleri Mono ile derlendi (0 hata). Unity'de ve URP'de denenmedi.

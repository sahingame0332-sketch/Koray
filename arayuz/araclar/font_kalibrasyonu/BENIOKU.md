# Font kalibrasyon araçları

Bir pencereyi "birebir" yaparken fontu ve puntoyu gözle seçmek yanıltıcı oluyor. Bu iki araç
kararı ölçüme bağlar.

**Ölçüt:** orijinal ekran görüntüsündeki açık renkli yazı pikselleri ile önizlemedeki yazı
piksellerinin örtüşme oranı (IoU). Bölge ±6 px kaydırılarak en iyi hizalama aranır, böylece
1–2 piksellik konum farkı fontun şekil benzerliğini maskelemez. 1.0 = birebir.

## `font_kimligi.py` — hangi font?

```bash
python3 font_kimligi.py ../../referans_gorseller/CharInfo_Orijinal.jpg
```

Her etiketi her aday fontla 13–28 punto arasında rasterize eder, en iyi puntoyu alır ve
fontları sıralar. Punto etkisini dışarıda bıraktığı için sonuç fontun kendi şekil
benzerliğini gösterir. Çıktının ikinci kısmı, kazanan font için etiket başına en uygun
puntoyu verir — kalibrasyonun başlangıç noktası budur.

## `olc.py` — önizleme ne kadar tutuyor?

```bash
python3 olc.py ../../referans_gorseller/CharInfo_Orijinal.jpg eski.png yeni.png
```

İki (veya daha fazla) önizlemeyi aynı orijinale karşı bölge bölge karşılaştırır, grup
ortalamalarını verir. Punto değiştirip yeniden render ettikten sonra bununla doğrulanır.

## `bolgeler.json`

Char Info penceresindeki 31 yazı bölgesi: `kutu` orijinaldeki piksel sınırları, `metin`
o kutudaki gerçek yazı, `grup` aynı puntoyu paylaşan metinler (`tab`, `lbl`, `statk`,
`statv`, `resk`, `resv`, `btn`, `human`, `name`, `job`). Yeni pencere kalibre edilirken
bu dosyanın aynı biçimde bir eşi hazırlanır.

## Punto taraması

Önizleme HTML'i (`kaynak/char_info/unity_preview.html`) punto değerlerini `:root` içinde
CSS değişkeni olarak tutar (`--fs-tab`, `--fs-lbl`, …). Tarama, bu değişkenleri geçersiz
kılan bir `<style>` enjekte edip Chromium ile render etmek ve her render'ı `olc.py` ile
ölçmekten ibarettir. Gruplar ayrı bölgelerde olduğu için her grup bağımsız taranabilir.

Not: Chromium ile Unity'nin uGUI yazı rasterleştiricisi tıpatıp aynı değil. Buradan çıkan
punto Unity'de ±1 rötuş isteyebilir.

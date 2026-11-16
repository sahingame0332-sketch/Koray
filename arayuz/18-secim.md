# 18 — Seçim efektleri: hedef seçim halkası + yön oku

Paket `unity_paketleri/OlymposSecim1298.unitypackage` (namespace `Olympos.Secim`; sınıflar `OlymposSecimHalkasi`, `OlymposYonOku`,
`OlymposSecimYoneticisi`, ortak taban `OlymposSecimZeminDortgeni`; shader `Olympos/Secim Zemin`; menü `OLYMPOS > 1298 > Seçim Halkası + Yön Oku Oluştur`).
Kaynak: telefon kaydı 14-31-04 (2712 × 1220; depoya konmadı) + kullanıcının ekran görüntüsü (pakette `Referans/`).
Önizleme: `onizlemeler/secim_onizleme.png` (orijinal kare ↔ efektsiz zemin + doku, kameranın perspektifiyle geri yansıtılmış).
Araçlar `araclar/secim/` (sıra: `rectfit2.py` → `acik.py` → `model2.py` → `halka_doku.py`; `ok4.py` → `ok6.py` → `ok7.py` → `ok8.py`/`ok11.py` → `ok12.py`; `yansit.py`).

## Davranış (kayıttan)
- Halka ve ok hedef seçilince birlikte çıkıyor; hedef bırakılınca aynı karede (Stroke 75→76, Stab 140→141) birlikte kayboluyor.
- Halka dönmüyor/atmıyor. Mob (solucan) halkanın önünde çiziliyor → yer decalı. Ok karakterin ayağından hedefe bakıyor, yere yapışık.

## Kamera-zemin modeli
Yer düzlemi için u − cx = X·(v − yh)·…, v = yh + s/D (cx = 1356). İki seçim halkasının (aynı mob → aynı yarıçap) noktalarına
görüntüde uzaklık en küçüklenerek: **yh = −353, s = 1621** (9 farklı başlangıçtan aynı sonuç; Stroke halkasına ortanca sapma 5 px).
Stab halkası (alt çubuğa yakın, eğimli zemin) tam oturmadı; dokular Stroke halkası ve ok örneklerinden. `araclar/secim/kamera_zemin.npy`.

## Halka
- Yukarıdan görünüşe açılan halka (512², kenar = 1.35 × yarıçap) dairesel: dış/iç sırtların açıya göre Fourier (2. derece) uyumuyla
  normalleştirildi (rms 0.0016 yarıçap). İç çizgi / dış çekirdek = 0.817.
- Saydamlık: her yarıçap halkasında çim dokusu değişkenliğinden E = P − a·B regresyonu (ağırlıklı): dış çekirdek a 0.95,
  iç çizgi 0.94, aradaki sıcak dolgu ~0.3, mor ışıma a≈0 (eklemeli), iç tül 0.1–0.25. Doku ön-çarpımlı.
- İşaretler: radyal modelden artık; sağ-üst örnek (45°) alınıp 165° ve 285°'ye döndürüldü (kayıtta ~158° ve ~−72°).
- Boyut: yarıçap = 0.399 × karakter boyu (eğik bakış düzeltmeli: karakter 243 px, ayakta ışın yükselişi 46.8°).
- Doğrulama: geri yansıtılmış halka ↔ orijinal ort. fark **12.8**/255 (solucan ve etiket önde bırakılarak).

## Yön oku
- 5 örnek (Stab 136–139, Stab2 220/228/231; Stroke halkanın altında kaldı, kullanılmadı), elle ölçülen uç + iki kanat noktasıyla benzerlik
  dönüşümü (uç boyu 107–110 px, yarı genişlik 70–73 px), sonra ±7 px / ±4° ince hizalama (korelasyon 0.93–0.96), aynayla ikiye katlandı.
- Şekil ölçülen kenar doğrularından: bas eğimi 0.626, kanat yarı genişliği 75.5, sap yarı genişliği 43, kenar kalınlığı 13.5 px; kenar yumuşaklığı ölçülen profile göre.
- Saydamlık satır satır regresyon: krem kenar **0.85**, dolgu **0.47**; renk: kenar (202,190,102), dolgu uçta (248,244,85) → kuyrukta (55,97,16).
- Ok içindeki ort. fark (örnek başına) 11.8–14.5/255. Boyut: 0.328 × 0.488 karakter boyu; karakter noktası (0.497, 0.262).
- Sınır: kuyruk ucu tüm örneklerde bacak altında (kenar düz uzatıldı), uç "Worm" yazısı altında (ayna + 5 örnekle tamamlandı).

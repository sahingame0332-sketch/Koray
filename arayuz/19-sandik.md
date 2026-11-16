# 19 — Mob ölünce düşen sandık (kapalı + açık)

Paket `unity_paketleri/OlymposSandik1298.unitypackage` (namespace `Olympos.Sandik`; sınıflar `OlymposSandik` (3B), `OlymposSandik2B`;
shader'lar `Olympos/Sandik 3B`, `Olympos/Sandik Sprite`; menü `OLYMPOS > 1298 > Sandık (Açık · Kapalı) Oluştur`).
Kaynak: kullanıcının 5 ekran görüntüsü (2712 × 1220), pakette `Referans/`. Önizleme `onizlemeler/sandik_onizleme.png`
(orijinal ↔ 3B model aynı kamerayla + yeni açılar). Araçlar `araclar/sandik/` (ekran görüntüleri scratch'te `s1..s5.jpg` olarak beklenir).

## Yöntem
1. `maske.py`: sandık / çim ayrımı (yeşil baskın = çim) → siluet maskeleri.
2. Şekil: gövde kutusu L × D × HB + yarı elips kubbe kapak (yükseklik HL, uzunluk ekseni boyunca) + kemerli uç kapakları.
   `ortak_uydur.py`: 3 kapalı görüntüde (2, 3, 4) ortografik kamera (yaw, pitch, roll, ölçek, öteleme) + şekil birlikte —
   amaç siluet örtüşmesi (+ elle okunan köşe noktalarına küçük ağırlık). Sonuç **D 0.848, HB 0.389, HL 0.414** (L = 1),
   örtüşme 0.921 / 0.932 / 0.924; kameralar pitch 43° / 42° / 18°.
   Not: yalnız köşe noktalarıyla uydurma ortografik belirsizlik yüzünden bozuldu (pitch 3°); yalnız siluetle HL 0.377 çıktı — ortak amaç seçildi.
3. `acik_uydur.py`: açık görüntüde (1, neredeyse tepeden, pitch 56°) kamera + kapak açısı → **115.5°** (örtüşme 0.87).
4. `doku2.py`: her yüz noktası uydurulan kameralarla görüntüye izdüşürülüp örneklenir (en dik bakan görüntü; maske dışı geçersiz):
   ön (görüntü 2, kilit), arka (4), uç (3; kemer dışı alfa), kapak (2; görünmeyen arka yamaç = ön yamacın aynası),
   açık üst yüzey ve kapak içi (1).
5. Açık görüntüde gölgeli yüzler (uç, kapak dışı) modelden koyu: oran (0.41, 0.40, ~0.45) → açık durum tonu.

## Davranış
- Kullanıcı: sandık mob öldükten sonra düştüğü yerde **sabit** kalır (dönmez, zıplamaz). `OlymposSandik` kendi kendine hiçbir hareket yapmaz;
  yalnız `Dus(konum, yon)` ile yerleşir, `Ac()` ile kapak açılır. Önizleme videosu oyundaki gibi sabit kamerayla (görüntü 2'nin açısı).

## Boyut
Uzunluk = 0.24 × karakter boyu: görüntü 2'de sandık 77.6 px/L, eğik kamera (43°) ile karakterin izdüşüm boyu ~220 px (çömelmiş,
ayakta ~×1.1); görüntü 1'de aynı derinlikte benzer oran. Tahmin ±%15 (Inspector `uzunlukKarakter`).

## Sınırlar
- Alt yüz ve arka yamaç görünmüyor; açık sandığın içi altın yüzeyi (derinlik yok).
- Açılma animasyonu (0.3 sn) ve açılmanın ne zaman olduğu varsayım (görüntülerde açılış anı yok; "Collect All" penceresiyle birlikte açık görünüyor).
- Doku çözünürlüğü kaynak kadar (sandık ekranda ~80 px): 320 px/L dokular büyütülmüş görüntüdür.

# OLYMPOS-KO — Mobil Grafik ve Performans Yol Haritası

> Tarih: 28 Kasım 2026 · Hedef: MykoMobile düzeyinde **akıcı (60 FPS) ve net** görüntü, orta seviye Android telefonda.

## 0. Bu belge neye dayanıyor

| Kaynak | Kesinlik |
|---|---|
| MykoMobile APK analizi (`02-apk-analizi.md`, `arayuz/21-hazir-paket-kaynaklari.md`): Unity 2021.3.45f2, IL2CPP, URP, GLES 3.0 zorunlu; Bakery, Mesh Combine Studio, Advanced Culling System, TerrainToMesh, Lux URP, Stylized Water 2, TCP2, Polygon Arsenal… | **Ölçüldü** (APK'daki assembly / ad alanı adları) |
| Ekran görüntüsü ölçümleri (`arayuz/24-powerup-store.md`): oyun saydamlığı **lineer** uzayda karıştırıyor; telefon görüntüleri ekranın doğal çözünürlüğünde (2712 × 1220); arayüzde sıkıştırma izi yok | **Ölçüldü** |
| Bütçe rakamları (çizim komutu, üçgen, doku belleği), aşama süreleri | **Öneri** — Unity'nin mobil rehberleri ve sektör pratiği; OLYMPOS-KO sahnelerinde ölçülüp düzeltilmeli |
| Revenger Mobile | **İncelenmedi.** APK gelirse aynı yöntemle bakılır |

Temel fikir: MykoMobile motoru sıfırdan optimize etmedi. Mobilde performansın kaybedildiği beş yerin — **arazi, çizim komutu sayısı, görünmeyen nesneler, gerçek zamanlı ışık/gölge, efektler** — her birine hazır ve kanıtlanmış bir çözüm koydu. Üstüne Knight Online 1298'in zaten düşük poligonlu dünyasını modern ışıkla süsledi. Bu belge aynı yolu, mümkün olan yerde ücretsiz alternatiflerle, sırayla anlatır.

---

## 1. Aşama 0 — Proje kurulumu (1 hafta)

Sonradan değiştirmesi en pahalı kararlar. **İlk gün** yapılır.

| Ayar | Değer | Neden |
|---|---|---|
| Unity sürümü | **Unity 6 LTS** | 2021 LTS'in desteği bitti; Unity 6'da URP mobil iyileştirmeleri (Forward+, GPU Resident Drawer, Render Graph) var |
| Render hattı | **URP**, mobil profil | MykoMobile'ın da kullandığı hafif hat |
| Renk uzayı | **Linear** | MykoMobile lineer çalışıyor (ölçtük). Saydamlık/ışık geçişleri doğal görünür. Arayüz paketlerimizin saydamlık değerleri de buna göre (`OlymposPowerUpRenk`) |
| Betik arka ucu | **IL2CPP**, ARM64 | Hızlı yerel kod; Play Store zaten 64-bit istiyor |
| Grafik API | **Vulkan** önce, **OpenGL ES 3.0** yedek | Vulkan'da CPU yükü düşük; GLES 3.0 en düşük destek (MykoMobile ile aynı) |
| Hedef kare hızı | `Application.targetFrameRate = 60`, ayarlarda 30 seçeneği | Pil / ısınma için |
| Kalite seviyeleri | **3 seviye**: Düşük / Orta / Yüksek (Bölüm 8) | Cihaz sınıfına göre otomatik seçim |
| Doku sıkıştırma (Android) | **ASTC** (sahne 6×6, karakter 5×5, arayüz 4×4 ya da sıkıştırmasız) | Kalite / bellek dengesi en iyi format |
| Arayüz Canvas | Referans **2712 × 1220**, match = yükseklik | Bütün arayüz paketlerimiz bu Canvas'a göre (`CLAUDE.md`) |

**Tamamlanma ölçütü:** Boş bir sahne hedef telefonda 60 FPS, Frame Debugger'da yalnız beklenen geçişler var.

---

## 2. Aşama 1 — Arazi ve zemin (2–3 hafta)

Zeminin akıcılığı MykoMobile'ın en belirgin farkı; sebebi **Unity Terrain kullanmamaları** (APK'da TerrainToMesh var).

1. **Tasarım:** Haritayı Unity Terrain ile çizin (heightmap, boyama). Terrain yalnız düzenleme aracı olarak kalır.
2. **Çevirme:** Bitince Terrain'i **mesh'e çevirin**.
   - Ücretli: Amazing Assets *TerrainToMesh* (MykoMobile'ın kullandığı).
   - Ücretsiz: heightmap'i kendi betiğinizle LOD'lu mesh parçalarına bölmek (64 × 64 m parçalar).
3. **Zemin shader'ı:** Katman başına bir doku + **kontrol haritası (splatmap)** + **renk haritası**, tek geçişte. Bunun ilk sürümü zaten hazır: `arayuz/unity_paketleri/OlymposZemin1298.unitypackage` (`Olympos/Zemin1298` shader, 5 döşenebilir doku, ölçülmüş renk/sıcaklık). URP'ye uyarlaması bu aşamada yapılır.
4. **Parça ve LOD:** Her arazi parçasına 3 LOD (tam / ½ / ¼ üçgen), uzak parçalar düşük LOD.
5. **Çim:** GPU instancing ile çizilen çim kümeleri, rüzgâr vertex shader'da.
   - Ücretli: Lux URP Essentials (MykoMobile).
   - Ücretsiz: URP Shader Graph ile basit rüzgâr + instancing.
   - Çim yoğunluğu kalite seviyesine bağlı (Düşük: kapalı).

**Bütçe (öneri):** Görünen arazi ≤ 60 bin üçgen, zemin ≤ 8 çizim komutu, zemin dokuları toplam ≤ 32 MB.

---

## 3. Aşama 2 — Işık ve gölge (2 hafta)

Mobilde gerçek zamanlı gölge pahalıdır. MykoMobile ışığı **önceden pişiriyor** (Bakery).

| Konu | Uygulama |
|---|---|
| Ortam ışığı | **Önceden pişirilmiş lightmap** (statik nesneler, zemin). Ücretli: Bakery; ücretsiz: Unity Progressive GPU Lightmapper |
| Hareketli nesneler | **Light Probe**'lar (karakter / mob pişmiş ışığı alır) |
| Güneş gölgesi | Yalnız **karakter ve moblar** için, 1 kademe (cascade), kısa mesafe (≈25 m), 1024 px gölge haritası; Düşük seviyede **blob gölge** (karakter altına yarı saydam daire) |
| Ek ışıklar | Gerçek zamanlı nokta ışık ≤ 2 (skill efektleri için), geri kalanı pişmiş |
| Son işlem (post-process) | Yalnız **renk düzenleme (LUT) + hafif bloom**. SSAO, derinlik bulanıklığı, hareket bulanıklığı **kapalı** |
| Sis | URP doğrusal sis, uzak LOD geçişlerini gizler |

**Tamamlanma ölçütü:** Şehir sahnesinde gölge geçişi ≤ 2 ms (Orta seviye cihaz).

---

## 4. Aşama 3 — Çizim komutu ve görünürlük (2 hafta)

Mobilde akıcılığın asıl anahtarı **çizim komutu (draw call / SetPass) sayısı**.

1. **Statik birleştirme:** Aynı malzemeli statik nesneleri birleştirin. Ücretli: Mesh Combine Studio (MykoMobile); ücretsiz: Unity Static Batching + kendi birleştirme betiği.
2. **Doku atlası:** Bina / sahne nesnelerini az sayıda atlas dokuda toplayın (malzeme sayısı ↓ → birleştirme ↑).
3. **SRP Batcher** açık; mümkünse **GPU Resident Drawer** (Unity 6).
4. **Görünmeyeni çizmeme:** Unity Occlusion Culling (pişirilmiş) + kamera uzaklık sınırları. Ücretli: Advanced Culling System (MykoMobile).
5. **LOD Group:** Bina 3 LOD, ağaç 3 LOD + en uzakta billboard.
6. **Kamera:** KO tarzı sabit eğik kamera → görüş uzaklığı küçük tutulur (ör. 120 m), ufuk sisle kapanır.

**Bütçe (öneri, Orta seviye):** SetPass ≤ 60, çizim komutu ≤ 150, sahnede görünen toplam ≤ 250 bin üçgen.

---

## 5. Aşama 4 — Karakter ve moblar (sürekli)

KO'nun asıl avantajı: **düşük poligonlu dünya**. Görsel kaliteyi poligondan değil ışık ve shader'dan alın.

| Öğe | Bütçe (öneri) |
|---|---|
| Oyuncu karakteri | 6–10 bin üçgen, 1 malzeme, 1024² doku (ASTC 5×5), ≤ 40 kemik |
| Mob | 2–6 bin üçgen, 512–1024² doku |
| Ekrandaki karakter | 30+ kişide otomatik LOD ve animasyon güncelleme seyreltmesi (uzaktakiler daha seyrek) |
| Kumaş / pelerin | Yalnız yakındaki oyuncularda (Magica Cloth 2 ya da kemik zinciri); uzakta kapalı |
| Shader | Stilize aydınlatma (ücretli: Toony Colors Pro 2 — MykoMobile; ücretsiz: Shader Graph) |
| Animasyon | **GPU skinning**, Animator'da "Cull Update Transforms" |

---

## 6. Aşama 5 — Efektler (sürekli)

Efekt paketlerimiz hazır (`CLAUDE.md` — Efekt 7/8/9, Manes Of Fire, Kendi Skill, Yakın Skill, Ok…). Kayıtlardan çıkarılmış **kare dizisi + eklemeli shader** yöntemi mobilde ucuzdur; bunu koruyun.

1. Efekt dokuları **doku atlasında** (tek malzeme), ASTC 6×6.
2. **Overdraw:** Ekranı kaplayan büyük eklemeli kareler en pahalı şeydir. Büyük efektlerde kare boyutunu küçük tutun, boş kenarları kırpın.
3. Parçacık sınırı: efekt başına ≤ 50, ekranda ≤ 400; uzaktaki efektlerde yarı yoğunluk.
4. **Havuzlama (pooling):** Efektleri yaratıp yok etmek yerine yeniden kullanın.
5. Düşük seviyede ikincil katmanları (ön/arka ikinci katman, kıvılcım) kapatın.

---

## 7. Aşama 6 — Arayüz netliği (sürekli; büyük kısmı hazır)

Netliğin büyük kısmı arayüzden gelir. Bu tarafta **40+ paket teslim edildi** (`CLAUDE.md` — Teslim edilenler).

1. Arayüz her zaman **ekranın tam çözünürlüğünde** çizilir. Sahne gerekirse düşük çözünürlükte çizilir (URP **Render Scale** 0.85–0.9), arayüz etkilenmez.
2. Arayüz dokuları: **sıkıştırmasız** ya da ASTC 4×4, **mipmap kapalı**, filtre bilinear (paket kurucularımız zaten böyle ayarlıyor).
3. **Sprite Atlas:** Pencere başına bir atlas → pencere = 1–3 çizim komutu.
4. Canvas'ı böl: sık değişen öğeler (HP/MP çubukları, sayılar) ayrı Canvas'ta; statik pencereler ayrı. Böylece her karede bütün arayüz yeniden kurulmaz.
5. Yazı: şu an legacy `Text` + ölçülmüş fontlar. Uzun vadede **TextMeshPro**'ya geçiş (MykoMobile TMP kullanıyor) — keskin yazı, her boyutta. Geçişte puntolar yeniden ölçülmeli (`arayuz/02-font-kalibrasyonu.md`).
6. Saydamlık değerleri ekranlardan **ölçüldü**, tahmin edilmez (`arayuz/04-saydamlik.md`); renk uzayı Linear olduğu için değerler birebir tutar.

---

## 8. Kalite seviyeleri

| Ayar | Düşük | Orta | Yüksek |
|---|---|---|---|
| Render Scale (sahne) | 0.75 | 0.9 | 1.0 |
| Gölge | Blob | 1 kademe, 1024 px, 20 m | 1 kademe, 2048 px, 35 m |
| Çim | Kapalı | Yarım yoğunluk | Tam |
| Bloom | Kapalı | Açık | Açık |
| Efekt ikincil katmanları | Kapalı | Açık | Açık |
| Görüş mesafesi | 80 m | 120 m | 160 m |
| Hedef FPS | 30 | 60 | 60 |

İlk açılışta GPU adı / bellek / kısa bir kıyaslama ile seviye **otomatik** seçilir; oyuncu değiştirebilir.

---

## 9. Ölçüm ve doğrulama (her aşamanın sonunda)

| Araç | Neye bakılır |
|---|---|
| Unity Profiler (cihazda, Development Build) | Kare süresi: 60 FPS için ≤ 16.6 ms; CPU ana iş parçacığı ve render iş parçacığı ayrı |
| Frame Debugger | Çizim komutu / SetPass sayısı, gereksiz geçişler |
| Memory Profiler | Doku belleği; toplam bellek ≤ 1.2 GB (Orta) |
| Android GPU Inspector / Snapdragon Profiler | Overdraw, GPU süresi, ısınma |
| 15 dakikalık test | Isınma sonrası FPS düşüşü ≤ %10 |

**Test cihazları (öneri):** 1 düşük (ör. Mali-G52 sınıfı), 1 orta (Adreno 6xx / Mali-G68), 1 üst segment telefon + 1 tablet. Her aşama sonunda aynı şehir sahnesinde aynı rotayla ölçülür ve sonuç bu belgeye eklenir.

---

## 10. Paket seçimi — ücretli ve ücretsiz

| İhtiyaç | MykoMobile'ın kullandığı (ücretli) | Ücretsiz / kendi yapımı alternatif |
|---|---|---|
| Arazi → mesh | Amazing Assets TerrainToMesh | Heightmap → parçalı mesh betiği |
| Pişmiş ışık | Bakery | Unity Progressive GPU Lightmapper |
| Nesne birleştirme | Mesh Combine Studio | Static Batching + birleştirme betiği |
| Görünürlük | Advanced Culling System | Unity Occlusion Culling |
| Çim / rüzgâr | Lux URP Essentials | Shader Graph + GPU instancing |
| Su | Stylized Water 2 | Shader Graph (basit stilize su) |
| Karakter shader'ı | Toony Colors Pro 2 | Shader Graph |
| Kumaş | Magica Cloth 2 | Kemik zinciri (basit yay fiziği) |
| Efekt | Polygon Arsenal, Hovl Studio, All In 1 Vfx | **Kendi kayıtlarımızdan çıkardığımız paketler** (hazır) |

Ücretli paketler süreyi kısaltır ama şart değil. Satın alınacaksa öncelik sırası (etkiye göre): **TerrainToMesh → Bakery → Mesh Combine Studio**. Hepsi Unity Asset Store'dan, proje adına lisanslanmalı.

---

## 11. Zaman çizelgesi (öneri, 1 grafik/teknik geliştirici)

| Hafta | İş |
|---|---|
| 1 | Aşama 0 — proje kurulumu, kalite seviyeleri iskeleti |
| 2–4 | Aşama 1 — arazi → mesh, zemin shader'ı (URP), çim |
| 5–6 | Aşama 2 — pişmiş ışık, light probe, karakter gölgesi |
| 7–8 | Aşama 3 — birleştirme, atlas, culling, LOD |
| 9 | Aşama 6 — arayüz atlasları, Canvas bölme, paketlerin Unity'de denenmesi |
| 10 | İlk tam ölçüm turu (Bölüm 9), düzeltmeler |
| Sürekli | Aşama 4 (karakter/mob) ve Aşama 5 (efekt) içerik geldikçe bütçeyle |

---

## 12. Riskler

| Risk | Önlem |
|---|---|
| Unity'de henüz denenmemiş arayüz / efekt paketleri | Aşama 6'da hepsi bir test sahnesinde içe aktarılır, Console hataları giderilir |
| Gamma projede saydamlıkların sapması | Proje **Linear** açılır; paketlerdeki renk uzayı yardımcısı Gamma'da da yaklaşık değer verir |
| Ucuz telefonlarda ısınma | Düşük seviye + 30 FPS sınırı, efekt ikincil katmanları kapalı |
| Telif | MykoMobile / Knight Online varlıkları ve kodu kullanılmaz; yalnız **yöntem** taklit edilir. Lisanssız stok görseller kopyalanmaz (`CLAUDE.md`) |

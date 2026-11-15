# 16 · Yerdeki Merchant tezgâhı (3B nesnenin görüntüsü)

Kaynak: tek telefon ekran görüntüsü `referans_gorseller/tezgah/tezgah.jpg` (pakette `Referans/`). Paket `unity_paketleri/OlymposTezgah1298.unitypackage`
(namespace `Olympos.Tezgah`, sınıf `OlymposTezgah`, shader `Olympos/Tezgah Sprite`). Araçlar `araclar/tezgah/cikar.py`, `kur.py`; önizleme `onizlemeler/tezgah_onizleme.png`.

- Tezgâh çubuğu (OPEN/WHISPER) daha önce teslim edildi (Merchant / MerchantAlici); bu paket yerdeki nesne.
- Kesim: çim olmayan pikseller (olive-yeşil ve koyu yeşil eşiği) → en büyük parça → dış bükey zarf (siluet dış bükey) → 4× örnekle yumuşak kenar.
  Ekranda (1504,704) 251 × 330. Aynı yere bindirince fark 0.0 (kesim kayıpsız); başka sahnede (respawn karesi) gösterildi.
- Boyut: karakter 427 px (ayak 1045) → yükseklik 0.773, genişlik 0.588 karakter boyu. Pivot alt orta (0.54, 0).
- Sınır: 3B model yok; görüntü tek açıdan (kameraya dönük dörtgen). Unity'de denenmedi.

## Ek — yan görünüş
Kullanıcının ikinci görüntüsü (`referans_gorseller/tezgah/tezgah_yan.jpg`): tezgâh yandan, sancak ön yüzden sarkıyor, altında kırmızı perde.
Kesim aynı yöntem + maskeyle kesişim (sancak sandıktan taştığı için siluet dış bükey değil): (1081,453) 193 × 246.
Karakter 332 px → yükseklik 0.741 karakter boyu (ön görünüşle tutarlı: 0.773). Oynatıcı kamera açısına göre ÖN / YAN / YAN-ayna seçer (`onAcisi` 50°).
Önizleme `onizlemeler/tezgah_onizleme.png` iki satır (ön + yan); aynı yerde fark 0.0.

## Ek 2 — 3B tezgâh (kullanıcı: "2B olmuş, 3B yap")
- Geometri iki fotoğraftan çıkarıldı: alçak sandık + öne eğik teşhir tahtası. Ön kamerada (ölçek 285 px/m, eğim 29°, yaw −22°) üst izdüşüm ~145 px
  ve ön yüz ~140 px; yatay ön yüz 211 px → W 0.78, ön H 0.59 m; derinlik 0.42, arka H 0.99 (tahta ~44°).
- Yüz köşeleri elle ölçüldü (`araclar/tezgah/cikar3b.py`), homografiyle düz dokuya açıldı. `kur3b.py` aynı mesh/UV'yi yazılımla çizer → `onizlemeler/tezgah3b_onizleme.png`.
- Unity: `OlymposTezgah3B` (5 alt-mesh: üst, ön, sol, sağ-ayna, arka), menü `OLYMPOS > 1298 > Merchant Tezgahı 3B Oluştur`.
- Belirsiz: yan fotoğrafta görünen yüzlerin hangisi olduğu (sol yan + arka mı?) tek görüntüden kesin değil; ön kamera tutuyor, yan kamera
  yaklaşık. Arka yüz fotoğrafı yok (yan doku kullanıldı). Üstteki eşyalar düz dokuda (kabartma yok).

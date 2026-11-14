# 16 · Yerdeki Merchant tezgâhı (3B nesnenin görüntüsü)

Kaynak: tek telefon ekran görüntüsü `referans_gorseller/tezgah/tezgah.jpg` (pakette `Referans/`). Paket `unity_paketleri/OlymposTezgah1298.unitypackage`
(namespace `Olympos.Tezgah`, sınıf `OlymposTezgah`, shader `Olympos/Tezgah Sprite`). Araçlar `araclar/tezgah/cikar.py`, `kur.py`; önizleme `onizlemeler/tezgah_onizleme.png`.

- Tezgâh çubuğu (OPEN/WHISPER) daha önce teslim edildi (Merchant / MerchantAlici); bu paket yerdeki nesne.
- Kesim: çim olmayan pikseller (olive-yeşil ve koyu yeşil eşiği) → en büyük parça → dış bükey zarf (siluet dış bükey) → 4× örnekle yumuşak kenar.
  Ekranda (1504,704) 251 × 330. Aynı yere bindirince fark 0.0 (kesim kayıpsız); başka sahnede (respawn karesi) gösterildi.
- Boyut: karakter 427 px (ayak 1045) → yükseklik 0.773, genişlik 0.588 karakter boyu. Pivot alt orta (0.54, 0).
- Sınır: 3B model yok; görüntü tek açıdan (kameraya dönük dörtgen). Unity'de denenmedi.

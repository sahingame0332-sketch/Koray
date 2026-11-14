# 13 · Respawn penceresi (karakter ölünce)

Kaynak: tek telefon ekran görüntüsü (2712 × 1220) `referans_gorseller/respawn/respawn.jpg` — pakette de var (`Referans/respawn_referans.jpg`).
Paket: `unity_paketleri/OlymposRespawn1298.unitypackage` (sınıf `OlymposRespawnPenceresi`). Önizleme `onizlemeler/respawn_onizleme.png`.
Araçlar `araclar/respawn/`: `cikar.py`, `punto.py`, `kur.py`.

- Dış kutu (1985,645)–(2685,1031) = 700 × 386; koyu dış çizgi 1985–1987, tan çerçeve 1988–1990 (üst 649–652, alt 1026–1029).
- **Saydamlık 0.92:** pencerenin olmadığı kare yok; pencere içi üst şerit / hemen üstündeki çim oranı 0.081, 0.091,
  sağ kenar iç/dış 0.067 (arkada kırmızı skill ikonu olan şerit hariç) → 1 − 0.080 = 0.92.
- Krom: pencere içinde sızan sahne = yerel karanlık taban (gri açma 21 px), yazılar parlak çekirdeğin 2 px çevresi;
  çerçeve ve Confirm düğmesi opak, renk orijinal.
- Yazılar (sprite'ta, orijinal piksel): "Respawn" `#EDF522`, büyük harf 19 px; mesaj beyaz, 2 satır, büyük harf 20 px, geniş harf aralığı;
  "Confirm" `#FAEFEF` 17 px. Font Roboto Slab Bold (~28 / ~24 punto, +1.8 px aralık) — legacy Text harf aralığı veremediği için yazılar sprite'ta.
- Doğrulama: aynı karede sahne geri kestirilip siyah 0.92 + sprite bindirildi → ortalama fark 1.0/255 (kendi içinde tutarlılık; başka sahnede de gösterildi).
- Varsayım: pencerenin konumu ekranın sağ altı (kayıttaki gibi); kapatma düğmesi yok, yalnız Confirm. Unity'de denenmedi.

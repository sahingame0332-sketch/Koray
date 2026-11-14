# 15 · NPC alım-satım penceresi (adet + ücret onayı)

Kaynak: 4 telefon ekran görüntüsü (2712 × 1220), `referans_gorseller/npc_alimsatim/` (pakette `Referans/`):
`al_adet` (Buy Item Count: + kutu "1"), `al_para` (Need Money : 70), `sat_adet` (Sell Item Count: + kutu "3"), `sat_para` (Earn Money : 33).
Paket `unity_paketleri/OlymposAlimSatim1298.unitypackage` (sınıflar `OlymposAlimSatim*`). Araçlar `araclar/npc_alimsatim/` (`cikar.py`, `punto.py`, `aralik.py`, `kur.py`).
Önizleme `onizlemeler/npc_alimsatim_onizleme.png` — 4 durumda ortalama fark 2.3 / 2.5 / 3.4 / 2.7 (255 üzerinden).

- Dış kutu (1665,542)–(2281,794) = 616 × 252; iç (1669,546) 607 × 244. Confirm (1765,693) 186×50, Cancel (1971,693) 188×50.
- **Saydamlık 0.97:** pencerenin kapalı hâli yok. Arkadaki dükkân öğeleri kenardan dışarı taşıyor: "Total Amount" yazısı dışarıda 255, içeride 19;
  "Sell selected items" düğme zemini dışarıda 68, içeride 1.7 → b = 19·(a/255)^1.84 (Genie/Görev ile aynı doğrusal olmayan ilişki) → orta tonda %3 geçiyor.
- Yazılar: Roboto Slab Bold **25 + 2 px harf aralığı** (IoU 0.73–0.76; aralıksız en iyisi 28 ama genişlik/yükseklik tutmuyor), `#EBEBEB`.
  Legacy Text harf aralığı veremediği için `OlymposAlimSatimHarfAraligi` (BaseMeshEffect) eklendi. Sayı Roboto Slab Bold 26 `#F0DCDC`.
- Fiyat: 1 Holy water = 70 (alım), 3 tane = 33 (satış, birim 11) — kayıttaki değerler deneme örneği.
- Varsayım: tekli eşyada adet sormadan doğrudan ücret ekranı (UcretleAc). Unity'de denenmedi.

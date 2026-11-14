# 14 · Alevli run halkası (skill sırasında karakterin altında)

İstek: gönderilen rün dairesi görseli "videodaki gibi" karakterin altında alevli efekt olsun.
**Kaynak görsel kullanılmadı:** dreamstime stok vektörü (filigranlı, lisans alınmamış). Bunun yerine aynı türde **özgün** bir daire
`araclar/rune/ciz.py` ile çizildi (uydurma rün alfabesi, heksagram, güneş/hilal/alev sembolleri, 8 kollu yıldız) — kompozisyon farklı.

Paket: `unity_paketleri/OlymposRuneEfekt1298.unitypackage` · önizleme `onizlemeler/rune_onizleme.png` (sahne üzerinde zaman serisi),
`rune_onizleme_tek.png` (üstten). Benzetim `araclar/rune/kur.py` shader ile aynı formülleri kullanır.

| Parametre | Değer |
|---|---|
| Çap | **1.6 × karakter boyu** (karakterBoyu 1.8 → 2.88 birim; kayıt karesinde karakter 110 px → 176 px; perspektif basıklık 0.47) |
| Dönüş | dış +0.04 tur/sn, iç −0.064 tur/sn |
| Alev dilleri | dış halka (r 0.93) ve heksagram çemberi (r 0.62) üzerinde dışa akan gürültü |
| Alev duvarı | silindir, yükseklik **0.12 × çap** (alevler yere yakın), 2 katman yukarı akan gürültü; yer alev dilleri güçlendirildi |
| Zarf | açılış 0.25 sn (0.6→1 büyüme), yanma `sure` (2 sn), sönüş 0.5 sn |
| Renk | çekirdek `#FFC761`, alev `#FF5C0A`, kor `#CC1400`; eklemeli |

Not: kullanıcının sahne karesinde (yeşil çim) efektin kendisi görünmüyordu; konum/boyut karakterin ayağına göre seçildi.
Unity'de denenmedi.

Revizyon (kullanıcı isteği): alevler yere yatırıldı (duvar 0.55 → 0.12), çap 2.0 → 1.6 karakter boyu. Önizleme `onizlemeler/rune_karakter*.png` (kayıttaki xDarKPasT).

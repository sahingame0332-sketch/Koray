# Unity olmadan derleme kontrolü

`derle.sh`, `arayuz/unity_kaynak/Assets/` altındaki tüm `.cs` dosyalarını Mono `mcs` ile
derler. Unity kurulu olmadığı için `UnityStubs.cs` ve `EditorStubs.cs` içinde, bu betiklerin
kullandığı Unity API üyelerinin **boş karşılıkları** tanımlı — davranış taklit edilmez,
yalnızca derleyicinin tipleri çözebilmesi sağlanır.

Yakaladığı hatalar: söz dizimi, isim çözümleme (ör. `Object` ad çakışması), tip uyuşmazlığı,
jenerik kısıtları, eksik `using`, erişilemeyen üye.

Yakalamadığı: gerçek Unity imzalarıyla farklılık, Unity çalışma zamanı davranışı, prefab/
serileştirme sorunları. Ayrıntılı sınır notu: `arayuz/01-dogrulama.md`.

Yeni bir Unity API'si kullanıldığında taslaklara karşılığını eklemek gerekir.

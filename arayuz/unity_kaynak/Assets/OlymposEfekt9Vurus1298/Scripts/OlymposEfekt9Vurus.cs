// OLYMPOS-KO · 1298 efekt 9 — mobdaki skill vurusu: havada pembe-beyaz patlama, gokten turuncu-kirmizi isin, yerde pembe halka + yatay sari parlama, sonda sari yildiz; havaya sacilan altin yapraklar.
// Kayit 20-27-52 (tablet, gercek hiz) -> 26 kare, 30 kare/sn (0.87 sn); eklemeli, renk/sicaklik degistirilmedi.
// Baglanti: mobun zemin noktasi (secim halkasi merkezi). Boyut karakter boyuna gore (kayitta 270 px): genislik 4.115 x boy, yuk./gen. 0.728, pivot (0.470, 0.169).
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Efekt9Vurus
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 9/vurus")]
    public class OlymposEfekt9Vurus : MonoBehaviour
    {
        public OlymposEfekt9VurusKatman katman;
        public bool denemeDongusu = false;
        public Transform denemeNokta;
        public float denemeAraligi = 0.8f;
        public UnityEvent onBitti = new UnityEvent();
        float bitis = -1f;

        void Start() { if (denemeDongusu) Oyna(denemeNokta != null ? denemeNokta : transform); }

        public void Oyna(Transform nokta)
        {
            if (katman == null) return;
            katman.Oyna(nokta);
            bitis = Time.time + katman.Sure;
        }

        void Update()
        {
            if (bitis < 0f || Time.time < bitis) return;
            bitis = -1f; onBitti.Invoke();
            if (denemeDongusu) Invoke("Tekrar", denemeAraligi);
        }

        void Tekrar() { Oyna(denemeNokta != null ? denemeNokta : transform); }
    }
}

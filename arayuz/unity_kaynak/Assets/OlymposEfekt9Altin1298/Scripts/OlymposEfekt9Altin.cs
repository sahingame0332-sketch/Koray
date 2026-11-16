// OLYMPOS-KO · 1298 efekt 9 — karakterin ustunde altin patlama: beyaz cekirdek, sari-altin halka ve runler, disi turuncu; cevresinde sicak isilti.
// Kayit 20-27-52 (tablet, gercek hiz) -> 10 kare, 30 kare/sn (0.33 sn); eklemeli, renk/sicaklik degistirilmedi.
// Baglanti: karakterin ayagi. Boyut karakter boyuna gore (kayitta 270 px): genislik 2.122 x boy, yuk./gen. 0.811, pivot (0.515, 0.073).
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Efekt9Altin
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 9/altin")]
    public class OlymposEfekt9Altin : MonoBehaviour
    {
        public OlymposEfekt9AltinKatman katman;
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

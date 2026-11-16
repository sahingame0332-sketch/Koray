// OLYMPOS-KO · 1298 efekt 9 — karakterin onundeki sari kilic kesigi yayi (kayitta hedef karakterin SOLUNDA; hedef saga dusunce otomatik ayna).
// Kayit 20-27-52 (tablet, gercek hiz) -> 10 kare, 30 kare/sn (0.33 sn); eklemeli, renk/sicaklik degistirilmedi.
// Baglanti: karakterin ayagi. Boyut karakter boyuna gore (kayitta 270 px): genislik 2.630 x boy, yuk./gen. 0.610, pivot (0.413, -0.155).
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Efekt9Kesik
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 9/kesik")]
    public class OlymposEfekt9Kesik : MonoBehaviour
    {
        public OlymposEfekt9KesikKatman katman;
        public bool denemeDongusu = false;
        public Transform denemeNokta;
        public float denemeAraligi = 0.8f;
        public UnityEvent onBitti = new UnityEvent();
        float bitis = -1f;

        void Start() { if (denemeDongusu) Oyna(denemeNokta != null ? denemeNokta : transform); }

        public void Oyna(Transform nokta, Transform hedef = null)
        {
            if (katman == null) return;
            katman.hedef = hedef;
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

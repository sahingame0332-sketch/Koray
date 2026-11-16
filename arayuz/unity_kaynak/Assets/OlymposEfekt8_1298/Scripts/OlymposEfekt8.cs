// OLYMPOS-KO · 1298 efekt 8 — YALNIZ SKILL EFEKTI (kayit 19-16-21, tablet, gercek hiz). Mobun kirmizilasmasi ayri paket (OlymposMobHasar1298).
// Sira (26 kare, 30 kare/sn, 0.87 sn): oyuncunun onunde sari kilic kesikleri + havaya sacilan altin yaprak/kivilcimlar -> mobun arkasinda
// pembe-mor aura (gokkusagi kenar) -> yatay sari parlama -> mobun ustunde sari yildiz patlamasi.
// Iki katman: ARKA (mobun arkasi, mob orter) + ON (mobun silueti ustundeki isik). Ikisi de mobun zemin noktasina bagli.
// Kullanim: efekt.Oyna(mob.transform);
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Efekt8
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 8/Efekt 8")]
    public class OlymposEfekt8 : MonoBehaviour
    {
        public string skillAdi = "efekt8";
        public OlymposEfekt8Katman arka, on;
        public bool denemeDongusu = false;
        public Transform hedefDeneme;
        public float denemeAraligi = 0.8f;
        public UnityEvent onBitti = new UnityEvent();
        float bitis = -1f;

        public float Sure { get { return Mathf.Max(arka != null ? arka.Sure : 0f, on != null ? on.Sure : 0f); } }

        void Start() { if (denemeDongusu) Oyna(hedefDeneme != null ? hedefDeneme : transform); }

        public void Oyna(Transform mob)
        {
            if (arka != null) arka.Oyna(mob);
            if (on != null) on.Oyna(mob);
            bitis = Time.time + Sure;
        }

        void Update()
        {
            if (bitis < 0f || Time.time < bitis) return;
            bitis = -1f; onBitti.Invoke();
            if (denemeDongusu) Invoke("Tekrar", denemeAraligi);
        }

        void Tekrar() { Oyna(hedefDeneme != null ? hedefDeneme : transform); }
    }
}

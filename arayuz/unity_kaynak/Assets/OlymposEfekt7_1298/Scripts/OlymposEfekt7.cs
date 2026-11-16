// OLYMPOS-KO · efekt 7: bir skill efekti = arka katman (mobun arkasi) + on katman (mobun onu) + hasar kirmizisi egrisi.
//   "kesik_aura": sari kesikler/kivilcimlar + mobun arkasinda pembe-mor aura (gokkusagi kenar) + yatay sari parlama; 20 kare (0.67 sn)
//   "yildiz":     mobun ortasinda sari yildiz patlamasi + mob ~0.15 sn kirmizi; 10 kare (0.33 sn)
// Kullanim: efekt.Oyna(mob.transform);  (mob.transform = mobun zemin noktasi)
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Efekt7
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 7/Efekt 7")]
    public class OlymposEfekt7 : MonoBehaviour
    {
        public string skillAdi = "";
        public OlymposEfekt7Katman arka, on;
        public OlymposEfekt7HasarRengi hasarRengi;
        [Tooltip("Mobun kirmizilik gucu, kare basina (30 kare/sn; kayittan olculdu).")]
        public float[] kirmiziEgrisi = new float[0];
        [Tooltip("Denemede surekli tekrar (hedefDeneme ile).")]
        public bool denemeDongusu = false;
        public Transform hedefDeneme;
        public float denemeAraligi = 0.8f;
        public UnityEvent onBitti = new UnityEvent();

        float bitis = -1f;

        public float Sure { get { return Mathf.Max(arka != null ? arka.Sure : 0f, on != null ? on.Sure : 0f); } }

        void Start() { if (denemeDongusu) Oyna(hedefDeneme != null ? hedefDeneme : transform); }

        public void Oyna(Transform hedef)
        {
            if (arka != null) arka.Oyna(hedef);
            if (on != null) on.Oyna(hedef);
            if (hasarRengi != null) hasarRengi.Oyna(hedef, kirmiziEgrisi);
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

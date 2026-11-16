// OLYMPOS-KO · efekt 7 HASAR (vurus) efekti — mobun uzerinde: arka katman (mobun arkasi) + on katman. Karakterin kilic yayi ayri paket (OlymposEfekt7Karakter1298), mob kirmizisi ayri paket (OlymposMobHasar1298).
//   "kesik_aura": mobda sari kivilcimlar + mobun arkasinda pembe-mor aura + yatay sari parlama; 20 kare (0.67 sn)
//   "yildiz":     mobun ortasinda sari yildiz patlamasi; 10 kare (0.33 sn)
// Kullanim: efekt.Oyna(mob.transform);
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Efekt7Hasar
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 7 Hasar/Efekt")]
    public class OlymposEfekt7Hasar : MonoBehaviour
    {
        public string skillAdi = "";
        public OlymposEfekt7HasarKatman arka, on;
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

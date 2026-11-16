// OLYMPOS-KO · efekt 7 skill isiklari (hasar rengi YOK — o ayri paket: OlymposMobHasar1298): arka katman (mobun arkasi) + on katman.
//   "kesik_aura": sari kesikler/kivilcimlar + mobun arkasinda pembe-mor aura + yatay sari parlama; 20 kare (0.67 sn)
//   "yildiz":     mobun ortasinda sari yildiz patlamasi; 10 kare (0.33 sn)
// Kullanim: efekt.Oyna(mob.transform);
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Efekt7Skill
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 7 Skill/Efekt")]
    public class OlymposEfekt7Skill : MonoBehaviour
    {
        public string skillAdi = "";
        public OlymposEfekt7SkillKatman arka, on;
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

// OLYMPOS-KO · bir yakin dovus skill'inin tum efekti: karakter katmani + (varsa) hedef katmani, ayni anda baslar.
// Kayitta: Stroke 33 kare (1.10 sn), Stab 27 kare (0.90 sn), Stab2 16 kare (0.53 sn; yalniz karakter katmani).
// Kullanim: efekt.Oyna(karakter.transform, hedef.transform);   hedef null ise hedef katmani karakterin ayaginda oynar.
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.YakinSkill
{
    [AddComponentMenu("OLYMPOS/1298/Yakin Skill/Yakin Skill Efekti")]
    public class OlymposYakinSkillEfekti : MonoBehaviour
    {
        public string skillAdi = "";
        public OlymposYakinSkillKatmani karakterKatmani;
        public OlymposYakinSkillKatmani hedefKatmani;
        [Tooltip("Denemede: baslangicta karakter = bu nesnenin kendisi, hedef = hedefDeneme ile surekli oynat.")]
        public bool denemeDongusu = false;
        public Transform hedefDeneme;
        public UnityEvent onBitti = new UnityEvent();

        float bitis = -1f;

        public float Sure
        {
            get
            {
                float s = 0f;
                if (karakterKatmani != null) s = Mathf.Max(s, karakterKatmani.Sure);
                if (hedefKatmani != null) s = Mathf.Max(s, hedefKatmani.Sure);
                return s;
            }
        }

        void Start() { if (denemeDongusu) Oyna(transform, hedefDeneme); }

        public void Oyna(Transform karakter, Transform hedef)
        {
            if (karakterKatmani != null) karakterKatmani.Oyna(karakter);
            if (hedefKatmani != null) hedefKatmani.Oyna(hedef != null ? hedef : karakter);
            bitis = Time.time + Sure;
        }

        public void Durdur()
        {
            if (karakterKatmani != null) karakterKatmani.Durdur();
            if (hedefKatmani != null) hedefKatmani.Durdur();
            bitis = -1f;
        }

        void Update()
        {
            if (bitis < 0f || Time.time < bitis) return;
            bitis = -1f; onBitti.Invoke();
            if (denemeDongusu) Oyna(transform, hedefDeneme);
        }
    }
}

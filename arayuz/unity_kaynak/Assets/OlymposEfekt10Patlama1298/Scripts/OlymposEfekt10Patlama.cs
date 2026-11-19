// OLYMPOS-KO · 1298 efekt 10 — pembe patlama (cekirdek): pembe kure + titanyum cekirdek + sari-yesil parantezler -> cekirdek sikisir, yanlara genisler
// -> parantezler disari acilip seftali-somon soyutlasir, titanyum sariya doner, yildiz isinlari parlar ve soner.
// Kullanici tarifiyle kare kare cizildi: 39 kare, 60 kare/sn = 0.65 sn; eklemeli. Baglanti: mobun merkezi (gogus hizasi).
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Efekt10Patlama
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 10/patlama")]
    public class OlymposEfekt10Patlama : MonoBehaviour
    {
        public OlymposEfekt10PatlamaKatman katman;
        public bool denemeDongusu = false;
        public Transform denemeNokta;
        public float denemeAraligi = 0.6f;
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

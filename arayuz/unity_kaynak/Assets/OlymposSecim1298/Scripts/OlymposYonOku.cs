// OLYMPOS-KO · 1298 yon oku — karakterin ayaginda, yere yapisik yesil ok (krem kenar), secili hedefe dogru doner.
// Kayittan 5 ornek (farkli yonler) yukaridan gorunuse duzeltilip hizalandi, ok simetrik oldugu icin aynayla tamamlandi.
// Olculen: kenar alfa 0.85, dolgu alfa 0.47 (dolgu ucta sari-yesil -> kuyrukta koyu yesil), kenar kalinligi 13.5 px.
// Doku 156 x 232 px; genislik 0.328 x karakter boyu, uzunluk 0.488 x boy; karakter noktasi dokuda (0.497, 0.262), ok ucu 0.355 x boy ileride.
using UnityEngine;

namespace Olympos.Secim
{
    [AddComponentMenu("OLYMPOS/1298/Secim/Yon Oku")]
    public class OlymposYonOku : OlymposSecimZeminDortgeni
    {
        public Transform karakter;
        public Transform hedef;
        [Header("Boyut (olculen)")]
        public float karakterBoyu = 1.8f;
        public float genislikKarakter = 0.328f;
        public float uzunlukKarakter = 0.488f;
        [Tooltip("Karakterin dokudaki yeri (x soldan, y kuyruktan).")]
        public Vector2 pivot = new Vector2(0.497f, 0.262f);

        void Awake() { Kur(); if (hedef == null) Gizle(); }
        void OnValidate() { if (GetComponent<MeshFilter>() != null) Kur(); }
        void Kur() { MeshKur(karakterBoyu * genislikKarakter, karakterBoyu * uzunlukKarakter, pivot); }

        public void Goster(Transform kim, Transform neye) { karakter = kim; hedef = neye; Goster(); LateUpdate(); }
        public void Birak() { hedef = null; Gizle(); }

        void LateUpdate()
        {
            if (karakter == null || hedef == null) return;
            Vector3 yon = hedef.position - karakter.position; yon.y = 0f;
            Yerlestir(karakter.position, yon);
        }
    }
}

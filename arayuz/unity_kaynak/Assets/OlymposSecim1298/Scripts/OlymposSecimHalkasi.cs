// OLYMPOS-KO · 1298 hedef secim halkasi — secilen mobun altinda, yere yapisik (dis sari halka + ic beyaz-mor cizgi + 3 sari ucgen isaret).
// Kayittan (14-31-04, 2712x1220) olculdu, yukaridan gorunuse duzeltildi: doku 512 x 512, halka yaricapi dokuda 189.6 px (dis sari cekirdek),
// dokunun yarisi = 1.35 x halka yaricapi. Halka yaricapi = 0.399 x karakter boyu (Worm icin). Doku on-carpimli (bkz. shader).
// Halka kayitta donmuyor ve atmiyor (sabit). Isaretler kayitta kameraya gore sag-ust, sol, alt; burada dunyaya gore sabit (donmeyiOlcek ile ayarlanir).
using UnityEngine;

namespace Olympos.Secim
{
    [AddComponentMenu("OLYMPOS/1298/Secim/Secim Halkasi")]
    public class OlymposSecimHalkasi : OlymposSecimZeminDortgeni
    {
        public Transform hedef;
        [Header("Boyut (olculen)")]
        public float karakterBoyu = 1.8f;
        [Tooltip("Halka (dis sari cekirdek) yaricapi / karakter boyu. Worm: 0.399. Buyuk moblarda arttirin.")]
        public float yaricapKarakter = 0.399f;
        [Tooltip("Doku yarisi / halka yaricapi (olculen 1.35).")]
        public float dokuPayi = 1.35f;
        [Tooltip("Isaretlerin dunya Y ekseni etrafinda donusu (derece).")]
        public float isaretAcisi = 0f;

        float sonBoy = -1f;

        void Awake() { Kur(); if (hedef == null) Gizle(); }
        void OnValidate() { if (GetComponent<MeshFilter>() != null) Kur(); }

        void Kur()
        {
            float d = 2f * karakterBoyu * yaricapKarakter * dokuPayi;
            MeshKur(d, d, new Vector2(0.5f, 0.5f)); sonBoy = d;
        }

        public void Sec(Transform yeniHedef) { hedef = yeniHedef; Goster(); LateUpdate(); }
        public void Birak() { hedef = null; Gizle(); }

        void LateUpdate()
        {
            if (hedef == null) return;
            if (!Mathf.Approximately(sonBoy, 2f * karakterBoyu * yaricapKarakter * dokuPayi)) Kur();
            Yerlestir(hedef.position, Quaternion.Euler(0, isaretAcisi, 0) * Vector3.forward);
        }
    }
}

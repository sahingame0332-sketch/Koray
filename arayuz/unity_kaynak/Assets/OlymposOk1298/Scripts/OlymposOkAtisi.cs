// OLYMPOS-KO · 1298 Shadow Hunter oku — atis (kayittan olculdu, telefon 2712x1220, 60 kare/sn).
// Ucus: yaydan cikis -> hedefe DUZ cizgi (olculen yay sapmasi kirisin %0.16'si: yok sayildi), sabit hiz,
//       kayitta 0.483 sn (29 kare). Ok her an ucus yonune hizali, kendi ekseni etrafinda kameraya doner (eksenel billboard).
// Gorsel: Textures/ok.png 160 x 19 — opak krem ucgen bas (golgeli taban) + incelen krem-sari isik izi; uc sagda.
//         Uzunluk 0.533 karakter boyu (kayitta yaydan cikarken 160 px, karakter ~300 px).
// Cikis noktasi: atanin ayagindan 0.77 karakter boyu yukari (yay eli). Varis: hedefin govdesi (hedefYuksekligi).
// Vurus: OlymposOkVurusu (beyaz patlama + gokten turuncu isin + pembe duman, 23 kare 30 kare/sn).
// Kullanim: okAtisi.At(okcu.transform, hedef.transform);
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Ok
{
    [AddComponentMenu("OLYMPOS/1298/Ok/Ok Atisi")]
    public class OlymposOkAtisi : MonoBehaviour
    {
        [Header("Gorsel")]
        public Material okMalzemesi;
        public OlymposOkVurusu vurusSablonu;

        [Header("Olcu (olculen)")]
        public float karakterBoyu = 1.8f;
        [Tooltip("Ok uzunlugu / karakter boyu (160 / 300 px).")]
        public float okUzunlukKarakter = 0.533f;
        [Tooltip("Ok yuksekligi / uzunlugu (19 / 160 px).")]
        public float okEnBoy = 0.119f;
        [Tooltip("Cikis yuksekligi / karakter boyu (yay eli; kayitta 0.77).")]
        public float cikisYuksekligi = 0.77f;
        [Tooltip("Hedefte okun saplandigi yukseklik (dunya birimi; kayittaki Worm icin govde ~0.25).")]
        public float hedefYuksekligi = 0.25f;

        [Header("Ucus")]
        [Tooltip("Acik: her atis ayni surede varir (kayitta 0.483 sn). Kapali: sabit hiz.")]
        public bool sabitSure = true;
        public float ucusSuresi = 0.483f;
        [Tooltip("sabitSure kapaliyken dunya birimi / sn.")]
        public float hiz = 25f;
        [Tooltip("Yay yuksekligi / mesafe (kayitta ~0.002; duz).")]
        public float yayOrani = 0f;
        public Camera kamera;

        public UnityEvent onVurdu = new UnityEvent();

        public void At(Transform atan, Transform hedef)
        {
            if (atan == null || hedef == null) return;
            var go = new GameObject("Ok", typeof(MeshFilter), typeof(MeshRenderer));
            var mr = go.GetComponent<MeshRenderer>(); mr.sharedMaterial = okMalzemesi;
            mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            var u = go.AddComponent<OlymposOkUcusu>();
            float L = karakterBoyu * okUzunlukKarakter;
            u.Kur(this, atan.position + Vector3.up * (karakterBoyu * cikisYuksekligi), hedef, L, L * okEnBoy);
        }

        internal void Vurdu(Vector3 nokta, Transform hedef)
        {
            if (vurusSablonu != null)
            {
                var v = Object.Instantiate(vurusSablonu, nokta, Quaternion.identity);
                v.gameObject.SetActive(true); v.kamera = kamera; v.karakterBoyu = karakterBoyu; v.hedef = hedef; v.Oyna();
            }
            onVurdu.Invoke();
        }
    }
}

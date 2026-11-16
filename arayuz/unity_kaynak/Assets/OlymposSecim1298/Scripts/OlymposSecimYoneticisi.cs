// OLYMPOS-KO · secim efektleri yoneticisi: hedef secilince mobun altinda halka + karakterin ayaginda hedefe donuk ok.
// Kayitta ikisi birlikte cikiyor ve hedef birakilinca ayni karede birlikte kayboluyor.
// Kullanim: secim.Sec(karakter.transform, mob.transform);  secim.Birak();
using UnityEngine;

namespace Olympos.Secim
{
    [AddComponentMenu("OLYMPOS/1298/Secim/Secim Yoneticisi")]
    public class OlymposSecimYoneticisi : MonoBehaviour
    {
        public OlymposSecimHalkasi halka;
        public OlymposYonOku ok;
        [Tooltip("Denemede baslangicta bu ikisiyle sec.")]
        public Transform denemeKarakter, denemeHedef;

        void Start() { if (denemeKarakter != null && denemeHedef != null) Sec(denemeKarakter, denemeHedef); }

        public void Sec(Transform karakter, Transform hedef)
        {
            if (halka != null) halka.Sec(hedef);
            if (ok != null) ok.Goster(karakter, hedef);
        }

        public void Birak()
        {
            if (halka != null) halka.Birak();
            if (ok != null) ok.Birak();
        }
    }
}

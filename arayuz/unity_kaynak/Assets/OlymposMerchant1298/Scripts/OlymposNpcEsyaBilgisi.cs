// OLYMPOS-KO · 1298 NPC dukkani esya bilgisi: dukkan yuvasina eklenir; dokununca "Buy Price" satirli
// bilgi penceresi acilir (yalniz Close dugmesi). Olculen ornek: Knife(+1), Buy Price : 3,188.
using UnityEngine;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/Merchant/NPC Esya Bilgisi")]
    public class OlymposNpcEsyaBilgisi : MonoBehaviour
    {
        public OlymposTicariYuva yuva;
        public OlymposEsyaBilgiPenceresi bilgi;
        public OlymposTicariEsya esya = new OlymposTicariEsya();

        void Awake()
        {
            if (yuva != null) yuva.onTiklandi.AddListener(delegate (int i) { Goster(); });
        }

        void Start() { if (yuva != null) yuva.Goster(esya); }

        public void Goster()
        {
            if (bilgi != null && esya != null) bilgi.GosterNpc(esya, yuva != null ? (RectTransform)yuva.transform : null);
        }
    }
}

// OLYMPOS-KO · 1298 Power Up Store — urun karti (kategori ya da Main Page duzeni).
// Kart sprite'i = cerceve + Purchase dugmesi (opak); ic ayri siyah Image (lineer gecirgenlik: kategori 0.30, Main Page 0.185).
// Fiyat: Cash yetiyorsa sari #FDDE24 + vurgulu dugme (orijinal: 0 fiyatli Teleport Scroll), yetmiyorsa kirmizi #F94922.
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/Power Up Store/Urun Karti")]
    public class OlymposPowerUpKart : MonoBehaviour
    {
        public Image ic;
        [Range(0f, 1f)] public float icGecirgenlikLineer = 0.30f;
        public Image ikon;
        public Text rozet;
        public Text adText;
        public Text fiyatText;
        public Image uygunDugme;
        public Button purchaseButton;

        public OlymposPowerUpUrun Urun { get; private set; }

        void OnEnable() { IcUygula(); }
        void OnValidate() { IcUygula(); }
        void IcUygula() { if (ic != null) ic.color = new Color(0f, 0f, 0f, OlymposPowerUpRenk.SiyahAlfa(icGecirgenlikLineer)); }

        public void Ayarla(OlymposPowerUpUrun u, long cash)
        {
            Urun = u;
            if (ikon != null) { ikon.sprite = u.ikon; ikon.enabled = u.ikon != null; }
            if (rozet != null) rozet.text = u.adet > 0 ? u.adet.ToString() : "";
            if (adText != null) adText.text = u.ad;
            bool yeter = u.fiyat <= cash;
            if (fiyatText != null) { fiyatText.text = OlymposPowerUpRenk.Para(u.fiyat); fiyatText.color = yeter ? OlymposPowerUpRenk.FiyatYeter : OlymposPowerUpRenk.FiyatYetmez; }
            if (uygunDugme != null) uygunDugme.enabled = yeter;
            IcUygula();
        }
    }
}

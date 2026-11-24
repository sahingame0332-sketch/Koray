// OLYMPOS-KO · 1298 Power Up Store — acilir pencereler: satin alma ayrintisi, paket icerigi, basari bildirimi, Cash Code sayfasi.
// Icleri opak (olculdu: arkadaki magaza hic gorunmuyor). Orijinal yazim korundu: dugmede "Puchase", mesajda "Purchase Succcessfully".
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/Power Up Store/Satin Alma Ayrintisi")]
    public class OlymposPowerUpAyrinti : MonoBehaviour
    {
        public Text baslikText, adetText, aciklamaText, fiyatText;
        public Image ikon;
        public Button eksiButton, artiButton, purchaseButton, closeButton;
        public int enCokAdet = 9999;
        public OlymposPowerUpSatinAlmaOlayi onSatinAl = new OlymposPowerUpSatinAlmaOlayi();
        OlymposPowerUpUrun urun; int adet = 1; long cash;

        void Awake()
        {
            if (eksiButton != null) eksiButton.onClick.AddListener(() => SetAdet(adet - 1));
            if (artiButton != null) artiButton.onClick.AddListener(() => SetAdet(adet + 1));
            if (purchaseButton != null) purchaseButton.onClick.AddListener(SatinAl);
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            if (urun == null) gameObject.SetActive(false);
        }

        public void Ac(OlymposPowerUpUrun u, long mevcutCash)
        {
            urun = u; cash = mevcutCash; adet = 1;
            if (baslikText != null) baslikText.text = u.ad;
            if (ikon != null) { ikon.sprite = u.ikon; ikon.enabled = u.ikon != null; }
            if (aciklamaText != null) aciklamaText.text = string.IsNullOrEmpty(u.aciklama) ? u.ad + "." : u.aciklama;
            gameObject.SetActive(true); transform.SetAsLastSibling();
            SetAdet(1);
        }

        public void SetAdet(int n)
        {
            adet = Mathf.Clamp(n, 1, enCokAdet);
            if (adetText != null) adetText.text = "(" + adet + ")";
            long toplam = urun != null ? (long)urun.fiyat * adet : 0;
            if (fiyatText != null) { fiyatText.text = OlymposPowerUpRenk.Para(toplam); fiyatText.color = toplam <= cash ? OlymposPowerUpRenk.FiyatYeter : OlymposPowerUpRenk.FiyatYetmez; }
        }

        void SatinAl() { var u = urun; int n = adet; Kapat(); if (u != null) onSatinAl.Invoke(u, n); }
        public void Kapat() { gameObject.SetActive(false); }
    }

    [AddComponentMenu("OLYMPOS/1298/Power Up Store/Paket Icerigi")]
    public class OlymposPowerUpPaketIcerik : MonoBehaviour
    {
        public Button closeButton;
        [Tooltip("Paketin iceriginin konacagi alan (orijinalde bos gorundu)")] public RectTransform icerikAlani;
        public OlymposPowerUpUrun Urun { get; private set; }
        public UnityEvent onAcildi = new UnityEvent();
        void Awake() { if (closeButton != null) closeButton.onClick.AddListener(Kapat); if (Urun == null) gameObject.SetActive(false); }
        public void Ac(OlymposPowerUpUrun u) { Urun = u; gameObject.SetActive(true); transform.SetAsLastSibling(); onAcildi.Invoke(); }
        public void Kapat() { gameObject.SetActive(false); }
    }

    [AddComponentMenu("OLYMPOS/1298/Power Up Store/Basari Bildirimi")]
    public class OlymposPowerUpBasari : MonoBehaviour
    {
        [Tooltip("Tam ekran gri ortu (olculdu: lineer gri 0.24, alfa 0.24)")] public Image ortu;
        public Text mesajText;
        public string varsayilanMesaj = "Purchase Succcessfully";
        public Button okButton;
        public UnityEvent onOk = new UnityEvent();
        bool acik;
        void Awake() { if (okButton != null) okButton.onClick.AddListener(Kapat); OrtuUygula(); if (!acik) gameObject.SetActive(false); }
        void OnValidate() { OrtuUygula(); }
        void OrtuUygula() { if (ortu != null) ortu.color = OlymposPowerUpRenk.GriOrtu(); }
        public void Ac(string mesaj = null)
        {
            acik = true; if (mesajText != null) mesajText.text = string.IsNullOrEmpty(mesaj) ? varsayilanMesaj : mesaj;
            OrtuUygula(); gameObject.SetActive(true); transform.SetAsLastSibling();
        }
        public void Kapat() { acik = false; gameObject.SetActive(false); onOk.Invoke(); }
    }

    [AddComponentMenu("OLYMPOS/1298/Power Up Store/Cash Code Sayfasi")]
    public class OlymposPowerUpCashCode : MonoBehaviour
    {
        public InputField kodAlani;
        public Button useButton, closeButton;
        [Tooltip("E-pin satici logosu icin bos yuva (orijinaldeki ucuncu taraf logosu kopyalanmadi)")] public Image logo;
        public OlymposPowerUpKodOlayi onKod = new OlymposPowerUpKodOlayi();
        bool acik;
        void Awake()
        {
            if (useButton != null) useButton.onClick.AddListener(() => { if (kodAlani != null && !string.IsNullOrEmpty(kodAlani.text)) onKod.Invoke(kodAlani.text.Trim()); });
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            if (logo != null) logo.enabled = logo.sprite != null;
            if (!acik) gameObject.SetActive(false);
        }
        public void Ac() { acik = true; if (kodAlani != null) kodAlani.text = ""; gameObject.SetActive(true); transform.SetAsLastSibling(); }
        public void Kapat() { acik = false; gameObject.SetActive(false); }
    }
}

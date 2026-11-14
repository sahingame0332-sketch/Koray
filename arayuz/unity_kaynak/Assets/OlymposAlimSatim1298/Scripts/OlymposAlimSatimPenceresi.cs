// OLYMPOS-KO · 1298 NPC alim-satim penceresi — TEK BASINA paket (OlymposAlimSatim1298)
// Dukkanda esyaya dokununca acilir. Dort durum (hepsi ayni pencere, 616 x 252):
//   AlimAdedi  : "<esya>" / "Buy Item Count:"  + sayi kutusu        SatisAdedi : "<esya>" / "Sell Item Count:" + sayi kutusu
//   AlimParasi : "<esya>" / "Need Money : N"                        SatisParasi: "<esya>" / "Earn Money : N"
// Kayittaki akis: adet gir -> Confirm -> ucret ("Need/Earn Money") -> Confirm -> islem. Cancel her adimda kapatir.
// Zemin duz siyah alfa 0.97 (olculdu), cerceve + Confirm/Cancel opak (orijinal piksel). Yazilar Roboto Slab Bold 25, +2 px aralik, #EBEBEB.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    public enum OlymposAlimSatimDurumu { AlimAdedi, AlimParasi, SatisAdedi, SatisParasi }
    [Serializable] public class OlymposAlimSatimOlayi : UnityEvent<bool, int, int> { }   // (alim mi, adet, toplam para)

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Alim Satim/Alim Satim Penceresi")]
    public class OlymposAlimSatimPenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.97f;

        [Header("Parcalar")]
        public Text esyaText;
        public Text satirText;
        public GameObject girisKutusu;
        public InputField adetField;
        public Button confirmButton;
        public Button cancelButton;

        [Header("Yazilar (orijinal)")]
        public string alimAdetYazisi = "Buy Item Count:";
        public string satisAdetYazisi = "Sell Item Count:";
        public string alimParaBicimi = "Need Money : {0}";
        public string satisParaBicimi = "Earn Money : {0}";

        [Header("Deneme")]
        public bool acilistaGoster = true;
        public OlymposAlimSatimDurumu denemeDurumu = OlymposAlimSatimDurumu.AlimAdedi;
        public string denemeEsya = "Holy water";

        [Header("Olaylar")]
        [Tooltip("Ucret ekraninda Confirm: (alim mi, adet, toplam para).")]
        public OlymposAlimSatimOlayi onOnay = new OlymposAlimSatimOlayi();
        public UnityEvent onIptal = new UnityEvent();

        OlymposAlimSatimDurumu durum;
        string esya; int birimFiyat; int enCok = 1; int adet = 1;

        public OlymposAlimSatimDurumu Durum { get { return durum; } }

        void Awake()
        {
            if (confirmButton != null) confirmButton.onClick.AddListener(Onayla);
            if (cancelButton != null) cancelButton.onClick.AddListener(Iptal);
            ZeminiUygula();
        }

        void Start()
        {
            if (!acilistaGoster) { gameObject.SetActive(false); return; }
            bool alim = denemeDurumu == OlymposAlimSatimDurumu.AlimAdedi || denemeDurumu == OlymposAlimSatimDurumu.AlimParasi;
            Ac(alim, denemeEsya, alim ? 70 : 11, alim ? 9999 : 3);
            if (denemeDurumu == OlymposAlimSatimDurumu.AlimParasi || denemeDurumu == OlymposAlimSatimDurumu.SatisParasi) Onayla();
        }

        void OnValidate() { ZeminiUygula(); }
        void ZeminiUygula() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        /// <summary>Alim (true) ya da satis (false) icin adet ekraniyla acar. enCokAdet: satista elde olan, alimda sinir.</summary>
        public void Ac(bool alim, string esyaAdi, int birimFiyati, int enCokAdet)
        {
            esya = esyaAdi; birimFiyat = Mathf.Max(0, birimFiyati); enCok = Mathf.Max(1, enCokAdet);
            adet = alim ? 1 : enCok;                                // kayit: alimda 1, satista eldeki adet (3) hazir gelir
            gameObject.SetActive(true); transform.SetAsLastSibling();
            Goster(alim ? OlymposAlimSatimDurumu.AlimAdedi : OlymposAlimSatimDurumu.SatisAdedi);
        }

        /// <summary>Adet sormadan dogrudan ucret ekrani (tekli esya).</summary>
        public void UcretleAc(bool alim, string esyaAdi, int toplamPara)
        {
            esya = esyaAdi; adet = 1; birimFiyat = toplamPara; enCok = 1;
            gameObject.SetActive(true); transform.SetAsLastSibling();
            Goster(alim ? OlymposAlimSatimDurumu.AlimParasi : OlymposAlimSatimDurumu.SatisParasi);
        }

        void Goster(OlymposAlimSatimDurumu d)
        {
            durum = d;
            bool adetModu = d == OlymposAlimSatimDurumu.AlimAdedi || d == OlymposAlimSatimDurumu.SatisAdedi;
            if (esyaText != null) esyaText.text = esya;
            if (satirText != null)
            {
                switch (d)
                {
                    case OlymposAlimSatimDurumu.AlimAdedi: satirText.text = alimAdetYazisi; break;
                    case OlymposAlimSatimDurumu.SatisAdedi: satirText.text = satisAdetYazisi; break;
                    case OlymposAlimSatimDurumu.AlimParasi: satirText.text = string.Format(alimParaBicimi, adet * birimFiyat); break;
                    default: satirText.text = string.Format(satisParaBicimi, adet * birimFiyat); break;
                }
            }
            if (girisKutusu != null) girisKutusu.SetActive(adetModu);
            if (adetModu && adetField != null) adetField.text = adet.ToString();
        }

        int GirilenAdet()
        {
            int v; if (adetField == null || !int.TryParse(adetField.text, out v)) v = 1;
            return Mathf.Clamp(v, 1, enCok);
        }

        public void Onayla()
        {
            switch (durum)
            {
                case OlymposAlimSatimDurumu.AlimAdedi: adet = GirilenAdet(); Goster(OlymposAlimSatimDurumu.AlimParasi); break;
                case OlymposAlimSatimDurumu.SatisAdedi: adet = GirilenAdet(); Goster(OlymposAlimSatimDurumu.SatisParasi); break;
                default:
                    bool alim = durum == OlymposAlimSatimDurumu.AlimParasi;
                    gameObject.SetActive(false);
                    onOnay.Invoke(alim, adet, adet * birimFiyat);
                    break;
            }
        }

        public void Iptal() { gameObject.SetActive(false); onIptal.Invoke(); }
    }
}

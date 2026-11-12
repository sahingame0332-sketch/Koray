// OLYMPOS-KO · 1298 "<ad> Merchant" penceresi (785 x 987, zemin alfa 0.89) — tezgah cubugundaki OPEN ile acilir
// Ustte 6 x 2 tezgah, ortada bakanin parasi, altta 7 x 4 envanter, OK / Cancel.
// Tezgahtaki esyaya dokun -> bilgi penceresi ("Purchase Price", yalniz Close; para yetmiyorsa fiyat kirmizi).
// Ayni esyaya bilgi penceresi acikken yeniden dokun -> sure cubuklu satin alma onayi (bilgi penceresi acik kalir;
// ekran goruntusunde ikisi birlikte gorunuyor — ikinci dokunusla acildigi varsayimdir).
// Onayda OK -> SatinAl(): para yeterse esya bakanin envanterine gecer; fiyat TEK esya icindir, yiginda adetle carpilir (varsayim).
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Merchant Penceresi")]
    public class OlymposMerchantPenceresi : MonoBehaviour
    {
        public Image background;
        public Image titleBackground;
        [Range(0f, 1f)] public float backgroundAlpha = 0.89f;
        public Text titleText;
        public Text goldText;
        public OlymposTicariYuva[] tezgahYuvalari = new OlymposTicariYuva[12];
        public OlymposTicariYuva[] envanterYuvalari = new OlymposTicariYuva[28];
        public Button okButton;
        public Button cancelButton;
        public OlymposEsyaBilgiPenceresi bilgi;
        public OlymposSatinAlmaOnayi satinAlmaOnayi;
        [Tooltip("Baslik: \"<ad>\" + bu ek. Olculen: \" Merchant\"")]
        public string baslikEki = " Merchant";

        public UnityEvent onClosed = new UnityEvent();
        [Tooltip("SatinAl() basarili olunca (satin alinan esya).")]
        public OlymposTicariEsyaOlayi onSatinAlindi = new OlymposTicariEsyaOlayi();
        [Tooltip("Satin almada odenen tutar: oyun parayi dusurur.")]
        public OlymposSayiOlayi onOdendi = new OlymposSayiOlayi();
        [Tooltip("Onayda OK'ye basildi ama para yetmedi (esya).")]
        public OlymposTicariEsyaOlayi onParaYetmedi = new OlymposTicariEsyaOlayi();

        OlymposTicariEsya[] tezgah;
        List<OlymposTicariEsya> envanter;
        long para;
        int sonDokunulan = -1;

        void Awake()
        {
            for (int i = 0; i < tezgahYuvalari.Length; i++)
                if (tezgahYuvalari[i] != null) { tezgahYuvalari[i].sira = i; tezgahYuvalari[i].onTiklandi.AddListener(Dokun); }
            if (okButton != null) okButton.onClick.AddListener(Kapat);
            if (cancelButton != null) cancelButton.onClick.AddListener(Kapat);
            if (satinAlmaOnayi != null) satinAlmaOnayi.onOnay.AddListener(OnayVerildi);
            ZeminiUygula();
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            var c = new Color(0f, 0f, 0f, backgroundAlpha);
            if (background != null) background.color = c;
            if (titleBackground != null) titleBackground.color = c;
        }

        public void Ac(string saticiAdi, OlymposTicariEsya[] tezgahEsyalari, List<OlymposTicariEsya> bakaninEnvanteri, long bakaninParasi)
        {
            tezgah = tezgahEsyalari; envanter = bakaninEnvanteri;
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            if (titleText != null) titleText.text = saticiAdi + baslikEki;
            sonDokunulan = -1;
            if (satinAlmaOnayi != null) satinAlmaOnayi.Kapat();
            ParaYaz(bakaninParasi);
            Ciz();
        }

        public void ParaYaz(long yeniPara) { para = yeniPara; if (goldText != null) goldText.text = OlymposTicariBicim.Para(yeniPara); }

        void Ciz()
        {
            for (int i = 0; i < tezgahYuvalari.Length; i++)
                if (tezgahYuvalari[i] != null) tezgahYuvalari[i].Goster(tezgah != null && i < tezgah.Length ? tezgah[i] : null);
            for (int i = 0; i < envanterYuvalari.Length; i++)
                if (envanterYuvalari[i] != null) envanterYuvalari[i].Goster(envanter != null && i < envanter.Count ? envanter[i] : null);
        }

        void Dokun(int i)
        {
            if (tezgah == null || i < 0 || i >= tezgah.Length || tezgah[i] == null) return;
            bool bilgiAcik = bilgi != null && bilgi.gameObject.activeSelf && bilgi.Esya == tezgah[i];
            if (satinAlmaOnayi != null && sonDokunulan == i && (bilgi == null || bilgiAcik))
            {
                satinAlmaOnayi.Ac(tezgah[i], tezgah[i].tezgahFiyati);
                return;
            }
            sonDokunulan = i;
            if (bilgi != null) bilgi.GosterTezgah(tezgah[i], (RectTransform)tezgahYuvalari[i].transform, para);
        }

        void OnayVerildi(OlymposTicariEsya e)
        {
            int i = tezgah != null ? System.Array.IndexOf(tezgah, e) : -1;
            if (i < 0) return;
            if (bilgi != null) bilgi.Kapat();
            if (SatinAl(i, para) < 0) onParaYetmedi.Invoke(e);
        }

        public void Kapat()
        {
            if (!gameObject.activeSelf) return;
            if (bilgi != null) bilgi.Kapat();
            if (satinAlmaOnayi != null) satinAlmaOnayi.Kapat();
            gameObject.SetActive(false);
            onClosed.Invoke();
        }

        /// <summary>Tezgahtaki esyayi satin alir: para yeterse esya bakanin envanterine gecer. Donus: odenen tutar (basarisizsa -1).</summary>
        public long SatinAl(int tezgahSirasi, long bakaninParasi)
        {
            if (tezgah == null || envanter == null || tezgahSirasi < 0 || tezgahSirasi >= tezgah.Length) return -1;
            var e = tezgah[tezgahSirasi];
            if (e == null) return -1;
            long fiyat = e.tezgahFiyati * Mathf.Max(1, e.adet);
            if (fiyat > bakaninParasi) return -1;
            tezgah[tezgahSirasi] = null; e.tezgahFiyati = 0;
            bool kondu = false;
            if (!string.IsNullOrEmpty(e.id))
                for (int i = 0; i < envanter.Count && !kondu; i++)
                    if (envanter[i] != null && envanter[i].id == e.id && (envanter[i].adet > 1 || e.adet > 1)) { envanter[i].adet += e.adet; kondu = true; }
            for (int i = 0; i < envanter.Count && !kondu; i++) if (envanter[i] == null) { envanter[i] = e; kondu = true; }
            if (!kondu) envanter.Add(e);
            sonDokunulan = -1;
            ParaYaz(bakaninParasi - fiyat);
            Ciz();
            onOdendi.Invoke(fiyat);
            onSatinAlindi.Invoke(e);
            return fiyat;
        }
    }
}

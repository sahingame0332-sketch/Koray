// OLYMPOS-KO · 1298 "<ad> Merchant" penceresi (785 x 987, zemin alfa 0.89) — tezgah cubugundaki OPEN ile acilir
// Ustte 6 x 2 tezgah, ortada bakanin parasi, altta 7 x 4 envanter, OK / Cancel.
// Tezgahtaki esyaya dokun -> bilgi penceresi ("Purchase Price", yalniz Close).
// Video yalniz tezgah SAHIBININ kendi tezgahina bakisini gosteriyor; satin alma adimi goruntulenmedi.
// SatinAl() bu yuzden arayuzu olmayan bir API'dir (oyun kendi onayindan sonra cagirir).
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
        [Tooltip("Baslik: \"<ad>\" + bu ek. Olculen: \" Merchant\"")]
        public string baslikEki = " Merchant";

        public UnityEvent onClosed = new UnityEvent();
        [Tooltip("SatinAl() basarili olunca (satin alinan esya).")]
        public OlymposTicariEsyaOlayi onSatinAlindi = new OlymposTicariEsyaOlayi();

        OlymposTicariEsya[] tezgah;
        List<OlymposTicariEsya> envanter;

        void Awake()
        {
            for (int i = 0; i < tezgahYuvalari.Length; i++)
                if (tezgahYuvalari[i] != null) { tezgahYuvalari[i].sira = i; tezgahYuvalari[i].onTiklandi.AddListener(Dokun); }
            if (okButton != null) okButton.onClick.AddListener(Kapat);
            if (cancelButton != null) cancelButton.onClick.AddListener(Kapat);
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
            ParaYaz(bakaninParasi);
            Ciz();
        }

        public void ParaYaz(long para) { if (goldText != null) goldText.text = OlymposTicariBicim.Para(para); }

        void Ciz()
        {
            for (int i = 0; i < tezgahYuvalari.Length; i++)
                if (tezgahYuvalari[i] != null) tezgahYuvalari[i].Goster(tezgah != null && i < tezgah.Length ? tezgah[i] : null);
            for (int i = 0; i < envanterYuvalari.Length; i++)
                if (envanterYuvalari[i] != null) envanterYuvalari[i].Goster(envanter != null && i < envanter.Count ? envanter[i] : null);
        }

        void Dokun(int i)
        {
            if (bilgi == null || tezgah == null || i < 0 || i >= tezgah.Length || tezgah[i] == null) return;
            bilgi.GosterTezgah(tezgah[i], (RectTransform)tezgahYuvalari[i].transform);
        }

        public void Kapat()
        {
            if (!gameObject.activeSelf) return;
            if (bilgi != null) bilgi.Kapat();
            gameObject.SetActive(false);
            onClosed.Invoke();
        }

        /// <summary>Tezgahtaki esyayi satin alir: para yeterse esya bakanin envanterine gecer. Donus: odenen tutar (basarisizsa -1).</summary>
        public long SatinAl(int tezgahSirasi, long bakaninParasi)
        {
            if (tezgah == null || envanter == null || tezgahSirasi < 0 || tezgahSirasi >= tezgah.Length) return -1;
            var e = tezgah[tezgahSirasi];
            if (e == null || e.tezgahFiyati > bakaninParasi) return -1;
            long fiyat = e.tezgahFiyati;
            tezgah[tezgahSirasi] = null; e.tezgahFiyati = 0;
            bool kondu = false;
            for (int i = 0; i < envanter.Count && !kondu; i++) if (envanter[i] == null) { envanter[i] = e; kondu = true; }
            if (!kondu) envanter.Add(e);
            ParaYaz(bakaninParasi - fiyat);
            Ciz();
            onSatinAlindi.Invoke(e);
            return fiyat;
        }
    }
}

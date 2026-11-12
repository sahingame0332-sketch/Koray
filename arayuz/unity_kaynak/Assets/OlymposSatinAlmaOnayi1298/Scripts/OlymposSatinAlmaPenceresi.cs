// OLYMPOS-KO · 1298 sure cubuklu satin alma onayi — TEK BASINA paket
// Merchant tezgahindan esya alirken acilir. 554 x 509; zemin MAT siyah (olcum: alfa 0.99).
// Ustte esya ikonu ve "+N"; turuncu sure cubugu + sayac; sari uyari ("Itemin Gradesini ve Fiyatini Kontrol Edin."),
// pembe baslik, "[Price: 99,999,999 ] Will you buy this item?" (fiyat sari) + "Please double check the price"; OK / Cancel.
// Ekran goruntusunde cubuk yari dolu, sayac "2", OK soluk (zemini Cancel'in 0.56 kati): OK, cubuk dolana kadar basilamaz.
// Toplam sure tek kareden olculemez — varsayilan 4 sn; Inspector'dan degisir.
// Kullanim:  pencere.Ac(ikon, yukseltme, fiyat);  pencere.onOnay -> fiyat ;  pencere.onIptal
// Cerceve, sari uyari, pembe baslik ve dugme yazilari orijinal piksellerdendir. Olculer: arayuz/09-merchant.md (ek bolum).
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposSatinAlmaOlayi : UnityEvent<long> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Satin Alma Onayi Penceresi")]
    public class OlymposSatinAlmaPenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.99f;

        [Header("Esya")]
        public Image iconImage;
        public Text upgradeText;

        [Header("Sure cubugu")]
        [Tooltip("Dolgu (Image.Type = Filled, yatay, soldan).")]
        public Image fillImage;
        public Text countdownText;
        [Tooltip("Dolgunun tam genisligi (px). Sayac dolgunun ucunu izler.")]
        public float dolguGenisligi = 437f;
        [Tooltip("OK'nin acilmasi icin beklenen sure (sn). Tek kareden olculemedi: varsayim (cubuk %49 iken sayac \"2\").")]
        public float beklemeSuresi = 4f;

        [Header("Yazi")]
        public Text messageText;
        [Tooltip("{0}: fiyat. Olculen: \"[Price: 99,999,999 ] Will you buy this item?\" + alt satir.")]
        public string mesajBicimi = "[Price: <color=#FFD300>{0}</color> ] Will you buy this item?\nPlease double check the price";

        [Header("Dugmeler")]
        public Button okButton;
        public Button cancelButton;

        [Header("Deneme")]
        [Tooltip("Isaretliyse sahne baslarken pencere ekran goruntusundeki ornekle acik gelir (Short Bow +5, 99,999,999).")]
        public bool acilistaGoster = true;
        public Sprite denemeIkonu;
        public int denemeYukseltme = 5;
        public long denemeFiyati = 99999999;

        [Header("Olaylar")]
        [Tooltip("Sure dolduktan sonra OK: onaylanan fiyat.")]
        public OlymposSatinAlmaOlayi onOnay = new OlymposSatinAlmaOlayi();
        public UnityEvent onIptal = new UnityEvent();

        long fiyat;
        float gecen;

        void Awake()
        {
            if (okButton != null) okButton.onClick.AddListener(Onayla);
            if (cancelButton != null) cancelButton.onClick.AddListener(Iptal);
            ZeminiUygula();
        }

        void Start()
        {
            if (acilistaGoster) Ac(denemeIkonu, denemeYukseltme, denemeFiyati); else gameObject.SetActive(false);
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        /// <summary>99999999 -> "99,999,999"</summary>
        public static string Para(long v)
        {
            string s = Math.Abs(v).ToString();
            var sb = new System.Text.StringBuilder();
            for (int i = 0; i < s.Length; i++)
            {
                if (i > 0 && (s.Length - i) % 3 == 0) sb.Append(',');
                sb.Append(s[i]);
            }
            return (v < 0 ? "-" : "") + sb;
        }

        /// <summary>Pencereyi acar ve sureyi bastan baslatir. yukseltme 0 ise "+N" yazilmaz.</summary>
        public void Ac(Sprite ikon, int yukseltme, long esyaFiyati)
        {
            fiyat = esyaFiyati;
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            if (iconImage != null) { iconImage.sprite = ikon; iconImage.enabled = ikon != null; }
            if (upgradeText != null)
            {
                upgradeText.gameObject.SetActive(yukseltme > 0);
                upgradeText.text = "+" + yukseltme;
            }
            if (messageText != null) messageText.text = string.Format(mesajBicimi, Para(esyaFiyati));
            gecen = 0f;
            Guncelle();
        }

        /// <summary>Kalan bekleme (sn).</summary>
        public float Kalan { get { return Mathf.Max(0f, beklemeSuresi - gecen); } }

        void Update()
        {
            if (gecen >= beklemeSuresi) return;
            gecen += Time.unscaledDeltaTime;
            Guncelle();
        }

        void Guncelle()
        {
            float oran = beklemeSuresi <= 0f ? 1f : Mathf.Clamp01(gecen / beklemeSuresi);
            bool bitti = oran >= 1f;
            if (fillImage != null) fillImage.fillAmount = oran;
            if (countdownText != null)
            {
                countdownText.gameObject.SetActive(!bitti);
                countdownText.text = Mathf.Max(0, Mathf.RoundToInt(beklemeSuresi - gecen)).ToString();
                if (fillImage != null)
                {
                    var rt = countdownText.rectTransform;
                    rt.anchoredPosition = new Vector2(fillImage.rectTransform.anchoredPosition.x + dolguGenisligi * oran, rt.anchoredPosition.y);
                }
            }
            if (okButton != null) okButton.interactable = bitti;      // kapaliyken yalniz dugme zemini 0.56'ya kararir (olculdu)
        }

        void Onayla()
        {
            if (gecen < beklemeSuresi) return;
            gameObject.SetActive(false);
            onOnay.Invoke(fiyat);
        }

        void Iptal()
        {
            gameObject.SetActive(false);
            onIptal.Invoke();
        }

        public void Kapat() { gameObject.SetActive(false); }
    }
}

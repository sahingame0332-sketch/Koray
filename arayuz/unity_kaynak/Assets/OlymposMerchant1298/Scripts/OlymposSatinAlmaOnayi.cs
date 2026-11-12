// OLYMPOS-KO · 1298 satin alma onayi (sure cubuklu) — "<ad> Merchant" penceresinde tezgahtaki esya icin
// 554 x 509 (tablet goruntusunde 577 x 530); zemin MAT siyah (olcum: alfa 0.99).
// Ustte esya ikonu ve "+N", altinda turuncu sure cubugu ve sayac; "Itemin Gradesini ve Fiyatini Kontrol Edin." uyarisi;
// "[Price: 99,999,999 ] Will you buy this item?" (fiyat sari) + "Please double check the price"; OK / Cancel.
// Ekran goruntusunde cubuk yari dolu, sayac "2", OK dugmesi soluk (zemini Cancel'in 0.56 kati), Cancel parlak:
// OK, cubuk dolana kadar basilamaz. Toplam sure tek kareden olculemez — varsayilan 4 sn (cubuk %49 iken "2").
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Satin Alma Onayi")]
    public class OlymposSatinAlmaOnayi : MonoBehaviour
    {
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
        [Tooltip("OK'nin acilmasi icin beklenen sure (sn). Tek kareden olculemedi: varsayim.")]
        public float beklemeSuresi = 4f;

        [Header("Yazi")]
        public Text messageText;
        [Tooltip("{0}: fiyat. Olculen: \"[Price: 99,999,999 ] Will you buy this item?\" + alt satir.")]
        public string mesajBicimi = "[Price: <color=#FFD300>{0}</color> ] Will you buy this item?\nPlease double check the price";

        [Header("Dugmeler")]
        public Button okButton;
        public Button cancelButton;

        public OlymposTicariEsyaOlayi onOnay = new OlymposTicariEsyaOlayi();
        public UnityEvent onIptal = new UnityEvent();

        public OlymposTicariEsya Esya { get; private set; }
        float gecen;

        void Awake()
        {
            if (okButton != null) okButton.onClick.AddListener(Onayla);
            if (cancelButton != null) cancelButton.onClick.AddListener(Iptal);
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void OnValidate() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        public void Ac(OlymposTicariEsya e, long fiyat)
        {
            if (e == null) return;
            Esya = e;
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            if (iconImage != null) { iconImage.sprite = e.ikon; iconImage.enabled = e.ikon != null; }
            if (upgradeText != null)
            {
                upgradeText.gameObject.SetActive(e.yukseltme > 0);
                upgradeText.text = "+" + e.yukseltme;
            }
            if (messageText != null) messageText.text = string.Format(mesajBicimi, OlymposTicariBicim.Para(fiyat));
            gecen = 0f;
            Guncelle();
        }

        void Update()
        {
            if (gecen >= beklemeSuresi) return;
            gecen += Time.unscaledDeltaTime;
            Guncelle();
        }

        void Guncelle()
        {
            float oran = beklemeSuresi <= 0f ? 1f : Mathf.Clamp01(gecen / beklemeSuresi);
            if (fillImage != null) fillImage.fillAmount = oran;
            bool bitti = oran >= 1f;
            if (countdownText != null)
            {
                countdownText.gameObject.SetActive(!bitti);
                countdownText.text = Mathf.Max(0, Mathf.RoundToInt(beklemeSuresi - gecen)).ToString();
                var rt = countdownText.rectTransform;
                rt.anchoredPosition = new Vector2(fillImage != null ? fillImage.rectTransform.anchoredPosition.x + dolguGenisligi * oran : rt.anchoredPosition.x,
                                                  rt.anchoredPosition.y);
            }
            if (okButton != null) okButton.interactable = bitti;
        }

        void Onayla()
        {
            if (gecen < beklemeSuresi) return;
            var e = Esya;
            gameObject.SetActive(false);
            if (e != null) onOnay.Invoke(e);
        }

        void Iptal() { Kapat(); onIptal.Invoke(); }

        public void Kapat() { gameObject.SetActive(false); }
    }
}

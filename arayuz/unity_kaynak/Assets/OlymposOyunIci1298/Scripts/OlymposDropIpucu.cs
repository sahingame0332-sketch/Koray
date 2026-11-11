// OLYMPOS-KO · 1298 drop esyasi ipucu (zemin siyah, alfa 0.93)
// Yerlesim icerikle buyur; araliklar orijinal kareden olculdu (484 x 621 ornek kutu).
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Drop Ipucu")]
    public class OlymposDropIpucu : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.93f;

        [Header("Icerik")]
        public Image iconImage;
        public Text nameText;
        public Text typeText;
        public Text dropRateLabel;
        public Text dropRateValue;
        public Text[] statTexts = new Text[0];
        public Text classText;
        public Text gradeText;
        public Text descriptionText;
        public RectTransform[] separators = new RectTransform[3];
        public Button closeButton;

        [Header("Renkler (olculen)")]
        public Color beyaz = new Color32(0xFF, 0xE7, 0xE9, 0xFF);
        public Color yesil = new Color32(0x96, 0xC0, 0x19, 0xFF);
        public Color kirmizi = new Color32(0xFE, 0x00, 0x01, 0xFF);

        [Header("Araliklar (olculen, px)")]
        public float statBaslangic = 241f;      // ilk stat satirinin merkezi
        public float statAdim = 38.5f;
        public float ortaBlokAdim = 31f;
        public float enAzGenislik = 300f;

        void Awake()
        {
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        public void Kapat() { gameObject.SetActive(false); }

        static void SatirY(Text t, float merkezY)
        {
            var rt = t.rectTransform;
            rt.anchoredPosition = new Vector2(rt.anchoredPosition.x, -(merkezY - rt.sizeDelta.y * 0.5f));
        }

        /// <summary>Ipucunu doldurur ve (solUstX, solUstY) ust nesne koordinatina yerlestirir.</summary>
        public void Goster(OlymposDropGirdisi d, Vector2 solUst)
        {
            if (d == null) return;
            gameObject.SetActive(true);
            transform.SetAsLastSibling();

            if (iconImage != null) { iconImage.sprite = d.ikon; iconImage.enabled = d.ikon != null; }
            nameText.text = d.ad; nameText.color = d.adRengi;
            typeText.text = d.turSatiri; typeText.color = d.adRengi;
            dropRateValue.text = d.oran;
            var dr = dropRateValue.rectTransform;
            dr.anchoredPosition = new Vector2(dropRateLabel.rectTransform.anchoredPosition.x + dropRateLabel.preferredWidth + 12f,
                                              dr.anchoredPosition.y);

            // genislik: en genis satir. Olculen: ayirici sagi = ad sagi + 19, kutu = ayirici sagi + 14
            float icerik = nameText.rectTransform.anchoredPosition.x + nameText.preferredWidth;
            icerik = Mathf.Max(icerik, typeText.rectTransform.anchoredPosition.x + typeText.preferredWidth);
            icerik = Mathf.Max(icerik, dr.anchoredPosition.x + dropRateValue.preferredWidth);

            int n = d.statlar != null ? d.statlar.Length : 0;
            float y = statBaslangic;
            for (int i = 0; i < statTexts.Length; i++)
            {
                var t = statTexts[i];
                if (t == null) continue;
                bool acik = i < n;
                t.gameObject.SetActive(acik);
                if (!acik) continue;
                t.text = d.statlar[i].metin;
                t.color = d.statlar[i].renk == OlymposSatirRengi.Yesil ? yesil
                        : d.statlar[i].renk == OlymposSatirRengi.Kirmizi ? kirmizi : beyaz;
                SatirY(t, y); y += statAdim;
                icerik = Mathf.Max(icerik, t.rectTransform.anchoredPosition.x + t.preferredWidth);
            }
            float genislik = Mathf.Max(enAzGenislik, icerik + 33f);
            float ayiriciGen = genislik - 26f;

            // 2. ayirici: son stat merkezinden 37 px asagi (stat yoksa 1. ayiricinin 30 px alti)
            float a2 = n > 0 ? (y - statAdim) + 37f : 194f + 30f;
            // ortali blok
            float oy = a2 + 46f;
            Text[] orta = { classText, gradeText };
            string[] ortaMetin = { d.sinifSatiri, d.dereceSatiri };
            for (int i = 0; i < orta.Length; i++)
            {
                if (orta[i] == null) continue;
                bool acik = !string.IsNullOrEmpty(ortaMetin[i]);
                orta[i].gameObject.SetActive(acik);
                if (!acik) continue;
                orta[i].text = ortaMetin[i];
                OrtaSatir(orta[i], oy, genislik); oy += ortaBlokAdim;
            }
            float aciklamaAlt = oy - ortaBlokAdim * 0.5f;
            if (descriptionText != null)
            {
                bool acik = !string.IsNullOrEmpty(d.aciklama);
                descriptionText.gameObject.SetActive(acik);
                if (acik)
                {
                    descriptionText.text = d.aciklama;
                    var rt = descriptionText.rectTransform;
                    rt.sizeDelta = new Vector2(ayiriciGen, rt.sizeDelta.y);
                    float h = descriptionText.preferredHeight;
                    rt.sizeDelta = new Vector2(ayiriciGen, h);
                    rt.anchoredPosition = new Vector2(12f, -(oy - ortaBlokAdim * 0.5f));
                    aciklamaAlt = oy - ortaBlokAdim * 0.5f + h;
                }
            }
            float a3 = aciklamaAlt + 33f;
            float dugmeY = a3 + 13f;

            float[] ay = { 194f, a2, a3 };
            for (int i = 0; i < separators.Length && i < 3; i++)
            {
                if (separators[i] == null) continue;
                separators[i].anchoredPosition = new Vector2(12f, -ay[i]);
                separators[i].sizeDelta = new Vector2(ayiriciGen, separators[i].sizeDelta.y);
            }
            if (closeButton != null)
            {
                var rt = (RectTransform)closeButton.transform;
                rt.anchoredPosition = new Vector2(12f, -dugmeY);
            }

            var kendi = (RectTransform)transform;
            kendi.sizeDelta = new Vector2(genislik, dugmeY + 62f + 3f);
            // ekrandan tasmasin
            var ust = kendi.parent as RectTransform;
            if (ust != null)
            {
                float maxX = ust.rect.width - genislik, maxY = ust.rect.height - kendi.sizeDelta.y;
                solUst = new Vector2(Mathf.Clamp(solUst.x, 0f, Mathf.Max(0f, maxX)), Mathf.Clamp(solUst.y, 0f, Mathf.Max(0f, maxY)));
            }
            kendi.anchoredPosition = new Vector2(solUst.x, -solUst.y);
        }

        static void OrtaSatir(Text t, float merkezY, float genislik)
        {
            var rt = t.rectTransform;
            rt.sizeDelta = new Vector2(genislik, rt.sizeDelta.y);
            rt.anchoredPosition = new Vector2(0f, -(merkezY - rt.sizeDelta.y * 0.5f));
        }
    }
}

// OLYMPOS-KO · 1298 esya eylem penceresi (envanterde esyaya dokununca acilan kutu)
// 663 x 313 · zemin siyah, alfa 0.92 (pencereli/penceresiz kare farkindan olculdu)
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposEsyaOlayi : UnityEvent<OlymposEsya> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Oyun Ici/Esya Penceresi")]
    public class OlymposEsyaPenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.92f;

        [Header("Icerik")]
        public Image iconImage;
        public Text nameText;
        public Text typeText;
        public Text descriptionText;
        public RectTransform separator;

        [Header("Dugmeler")]
        public Button useSelfButton;
        public Button useTargetButton;
        public Button equipButton;
        public Button closeButton;

        [Header("Yerlesim (olculen)")]
        [Tooltip("Icerik genisligi = adin sag ucu + bu deger. Ayirici cizgi ve aciklamanin ortalanmasi buna gore.")]
        public float adSonrasiBosluk = 20f;
        [Tooltip("Pencerenin sag-ust kosesinin, dokunulan yuvanin merkezine gore konumu.")]
        public Vector2 yuvaOfseti = new Vector2(-32f, 14f);

        [Header("Olaylar")]
        public OlymposEsyaOlayi onUseSelf = new OlymposEsyaOlayi();
        public OlymposEsyaOlayi onUseTarget = new OlymposEsyaOlayi();
        public OlymposEsyaOlayi onEquip = new OlymposEsyaOlayi();
        public UnityEvent onClosed = new UnityEvent();

        public OlymposEsya Esya { get; private set; }

        void Awake()
        {
            if (useSelfButton != null) useSelfButton.onClick.AddListener(delegate { Sec(onUseSelf); });
            if (useTargetButton != null) useTargetButton.onClick.AddListener(delegate { Sec(onUseTarget); });
            if (equipButton != null) equipButton.onClick.AddListener(delegate { Sec(onEquip); });
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        /// <summary>Pencereyi esyanin bilgileriyle doldurup acar. yuva verilirse pencere onun yanina gelir.</summary>
        public void Goster(OlymposEsya esya, RectTransform yuva)
        {
            if (esya == null) return;
            Esya = esya;
            if (iconImage != null) { iconImage.sprite = esya.ikon; iconImage.enabled = esya.ikon != null; }
            if (nameText != null) nameText.text = esya.ad;
            if (typeText != null) typeText.text = esya.turSatiri;
            if (descriptionText != null) descriptionText.text = esya.aciklama;
            if (useSelfButton != null) useSelfButton.interactable = esya.kendineKullanilir && esya.adet > 0;
            if (useTargetButton != null) useTargetButton.interactable = esya.hedefeKullanilir && esya.adet > 0;
            if (equipButton != null) equipButton.interactable = esya.kusanilir;
            gameObject.SetActive(true);
            Yerlestir();
            if (yuva != null) YuvaninYaninaTasi(yuva);
            transform.SetAsLastSibling();
        }

        // Olculen kural: ayirici cizgi x=11'den adin sag ucu + 20'ye kadar; aciklama bu genislikte ortali.
        void Yerlestir()
        {
            if (nameText == null) return;
            float adSol = nameText.rectTransform.anchoredPosition.x;
            float sag = adSol + nameText.preferredWidth + adSonrasiBosluk;
            var kendi = (RectTransform)transform;
            sag = Mathf.Clamp(sag, 200f, kendi.sizeDelta.x - 12f);
            if (separator != null)
                separator.sizeDelta = new Vector2(sag - separator.anchoredPosition.x, separator.sizeDelta.y);
            if (descriptionText != null)
            {
                var rt = descriptionText.rectTransform;
                rt.anchoredPosition = new Vector2(12f, rt.anchoredPosition.y);
                rt.sizeDelta = new Vector2(sag - 12f, rt.sizeDelta.y);
            }
        }

        void YuvaninYaninaTasi(RectTransform yuva)
        {
            var kendi = (RectTransform)transform;
            var ust = kendi.parent as RectTransform;
            if (ust == null) return;
            // yuvanin merkezi -> ust nesnenin yerel uzayi
            Vector3 dunya = yuva.TransformPoint(new Vector3(
                (0.5f - yuva.pivot.x) * yuva.rect.width, (0.5f - yuva.pivot.y) * yuva.rect.height, 0f));
            Vector3 yerel = ust.InverseTransformPoint(dunya);
            float w = kendi.sizeDelta.x, h = kendi.sizeDelta.y;
            // pencerenin sag-ust kosesi = yuva merkezi + ofset
            float sagX = yerel.x + yuvaOfseti.x, ustY = yerel.y + yuvaOfseti.y;
            float solX = sagX - w, altY = ustY - h;
            Rect r = ust.rect;
            if (solX < r.xMin) solX = r.xMin;
            if (solX + w > r.xMax) solX = r.xMax - w;
            if (altY < r.yMin) altY = r.yMin;
            if (altY + h > r.yMax) altY = r.yMax - h;
            kendi.anchorMin = kendi.anchorMax = new Vector2(0.5f, 0.5f);
            kendi.pivot = new Vector2(0f, 0f);
            kendi.anchoredPosition = new Vector2(solX - r.center.x, altY - r.center.y);
        }

        void Sec(OlymposEsyaOlayi olay)
        {
            var e = Esya;
            Kapat();                       // oyunda dugmeye basinca pencere kapanir
            if (e != null) olay.Invoke(e);
        }

        public void Kapat()
        {
            if (!gameObject.activeSelf) return;
            gameObject.SetActive(false);
            onClosed.Invoke();
        }
    }
}

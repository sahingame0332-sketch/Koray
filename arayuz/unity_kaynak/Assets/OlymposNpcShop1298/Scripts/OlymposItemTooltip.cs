// OLYMPOS-KO · 1298 ürün ipucu kutusu
// Oyundaki sırayla: ikon + ad · kalite satırı · Buy Price (kırmızı) · stat satırları · açıklama.
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    public class OlymposItemTooltip : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.85f;

        [Header("Parçalar")]
        public Image iconImage;
        public Text nameText;
        public Text gradeText;
        public Text priceText;
        public Text statsText;
        public Text descriptionText;

        [Header("Yerleşim")]
        [Tooltip("Kutunun imlece/slota göre kaydırması (sol-üst piksel).")]
        public Vector2 offset = new Vector2(8f, 8f);

        // Orijinal ipucundan ölçülen renkler
        static readonly Color Ad      = new Color32(0xF2, 0xF2, 0xF2, 0xFF);
        static readonly Color Kalite  = new Color32(0xA8, 0xA8, 0xA8, 0xFF);
        static readonly Color Fiyat   = new Color32(0xE0, 0x30, 0x30, 0xFF);
        static readonly Color Stat    = new Color32(0xD8, 0xC0, 0x90, 0xFF);
        static readonly Color Aciklama= new Color32(0xE6, 0xE6, 0xE6, 0xFF);

        void OnValidate() { ApplyBackgroundAlpha(); }

        public void ApplyBackgroundAlpha()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void Awake() { ApplyBackgroundAlpha(); Hide(); }

        public void Show(OlymposShopItem item, Vector2 anchoredPos)
        {
            if (iconImage != null) { iconImage.sprite = item.icon; iconImage.enabled = item.icon != null; }
            Yaz(nameText, item.name, Ad);
            Yaz(gradeText, item.gradeLine, Kalite);
            Yaz(priceText, item.buyPrice > 0 ? "Buy Price : " + OlymposNpcShopWindow.Num(item.buyPrice) : null, Fiyat);
            Yaz(statsText, item.statLines != null && item.statLines.Length > 0
                           ? string.Join("\n", item.statLines) : null, Stat);
            Yaz(descriptionText, item.description, Aciklama);

            var rt = transform as RectTransform;
            if (rt != null) rt.anchoredPosition = new Vector2(anchoredPos.x + offset.x, anchoredPos.y - offset.y);
            gameObject.SetActive(true);
        }

        public void Hide() { gameObject.SetActive(false); }

        static void Yaz(Text t, string v, Color c)
        {
            if (t == null) return;
            bool var_ = !string.IsNullOrEmpty(v);
            t.gameObject.SetActive(var_);
            if (var_) { t.text = v; t.color = c; }
        }
    }
}

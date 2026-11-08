// OLYMPOS-KO · 1298 ürün ipucu kutusu
// Sıra (ekran görüntülerinden): ikon + ad · kalite satırı · Buy Price · stat satırları ·
// sınıf satırı · derece satırı · açıklama · Close düğmesi.
// Renkler orijinalden ölçüldü; Buy Price para yetmiyorsa kırmızı, yetiyorsa sarı olur.
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    public class OlymposItemTooltip : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)]
        [Tooltip("Varsayılan 0.92: orijinalden ölçüldü. Ayrıntı: arayuz/05-npc-dukkan.md")]
        public float backgroundAlpha = 0.92f;

        [Header("Parçalar")]
        public Image iconImage;
        public Text nameText;
        public Text gradeTypeText;      // "Regular Item" / "Magic Item" / "Upgrade Item"
        public Text priceText;          // "Buy Price : 560"
        public Text statsText;          // karşılanan stat satırları
        public Text statsRedText;       // karşılanmayan satırlar (kırmızı)
        public Text classText;          // "(Warrior Item)"
        public Text itemGradeText;      // "Item Grade : Low Class"
        public Text descriptionText;
        public Button closeButton;

        [Header("Yerleşim")]
        public Vector2 offset = new Vector2(16f, 16f);

        public UnityEvent onClose = new UnityEvent();

        // Orijinalden ölçülen renkler
        static readonly Color Beyaz    = new Color32(0xF2, 0xF2, 0xF2, 0xFF);   // Regular ad + açıklama
        static readonly Color Mavi     = new Color32(0x4A, 0x7C, 0xFF, 0xFF);   // Magic Item
        static readonly Color Mor      = new Color32(0xCC, 0x55, 0xEE, 0xFF);   // Upgrade Item
        static readonly Color Sari     = new Color32(0xF2, 0xC4, 0x1E, 0xFF);   // yeterli para
        static readonly Color Kirmizi  = new Color32(0xEE, 0x22, 0x22, 0xFF);   // yetersiz para / şart
        static readonly Color StatBeyaz= new Color32(0xEE, 0xEE, 0xEE, 0xFF);
        static readonly Color Yesil    = new Color32(0x4C, 0xDD, 0x4C, 0xFF);   // "Item Grade : ..."

        void OnValidate() { ApplyBackgroundAlpha(); }

        public void ApplyBackgroundAlpha()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void Awake()
        {
            ApplyBackgroundAlpha();
            if (closeButton != null)
                closeButton.onClick.AddListener(() => { onClose.Invoke(); Hide(); });
            Hide();
        }

        public static Color KaliteRengi(OlymposItemKalite k)
        {
            switch (k)
            {
                case OlymposItemKalite.Magic:   return Mavi;
                case OlymposItemKalite.Upgrade: return Mor;
                default:                        return Beyaz;
            }
        }

        /// <summary>İpucunu doldurup gösterir. oyuncuParasi, Buy Price'ın rengini belirler.</summary>
        public void Show(OlymposShopItem item, long oyuncuParasi, Vector2 anchoredPos)
        {
            Color kr = KaliteRengi(item.kalite);
            Yaz(nameText, item.name, kr);
            Yaz(gradeTypeText, item.KaliteMetni, kr);

            bool parasiYetiyor = oyuncuParasi >= item.buyPrice;
            Yaz(priceText, item.buyPrice > 0 ? "Buy Price : " + OlymposNpcShopWindow.Num(item.buyPrice) : null,
                parasiYetiyor ? Sari : Kirmizi);

            // Stat satirlari iki gruba ayrilir: karsilanan (beyaz) ve karsilanmayan (kirmizi)
            string normal = "", red = "";
            if (item.statLines != null)
                foreach (var s in item.statLines)
                {
                    if (string.IsNullOrEmpty(s.metin)) continue;
                    if (s.karsilanmiyor) red += (red.Length > 0 ? "\n" : "") + s.metin;
                    else                 normal += (normal.Length > 0 ? "\n" : "") + s.metin;
                }
            Yaz(statsText, normal, StatBeyaz);
            Yaz(statsRedText, red, Kirmizi);

            Yaz(classText, item.classLine, item.classLineKirmizi ? Kirmizi : StatBeyaz);
            Yaz(itemGradeText, item.gradeLine, Yesil);
            Yaz(descriptionText, item.description, Beyaz);

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

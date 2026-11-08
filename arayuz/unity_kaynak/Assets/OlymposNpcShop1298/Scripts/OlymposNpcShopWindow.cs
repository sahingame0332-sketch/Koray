// OLYMPOS-KO · 1298 NPC dükkân penceresi (Tyroon / Ruber / Yasbal / Pallus / Caspy ortak)
// Beş NPC ayrı pencere değil: aynı pencere, farklı başlık ve ürün listesi.
// Görsel orijinal oynanış videolarından çıkarıldı; ölçüler arayuz/05-npc-dukkan.md
using System;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    public class OlymposNpcShopWindow : MonoBehaviour
    {
        public const int Sutun = 6, Satir = 4;
        public const int SayfaBasiSlot = Sutun * Satir;   // 24

        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)]
        [Tooltip("1 = tamamen siyah, 0 = tamamen saydam. Varsayılan 0.93: videodan ölçüldü " +
                 "(geçirgenlik t≈0.07). Ayrıntı: arayuz/04-saydamlik.md")]
        public float backgroundAlpha = 0.93f;

        [Header("Başlık")]
        public Text titleText;
        public Button closeButton;
        [Tooltip("X'e basılınca pencere gizlensin mi?")]
        public bool closeHidesWindow = true;

        [Header("Ürün ızgarası (6 x 4)")]
        public Image[] slotIcons = new Image[SayfaBasiSlot];
        public Button[] slotButtons = new Button[SayfaBasiSlot];
        [Tooltip("Çoklu satışta seçili slotun üzerine çıkan çerçeve.")]
        public Image[] slotSelection = new Image[SayfaBasiSlot];

        [Header("Sayfa")]
        public Button prevPageButton;
        public Button nextPageButton;
        public Text pageText;

        [Header("Satış")]
        public Button multipleSellingButton;
        [Tooltip("Onay kutusunun içindeki işaret; açık/kapalı olarak gösterilir.")]
        public Image multipleSellingCheck;
        public Button sellSelectedButton;
        public Text totalAmountText;

        [Header("Yan pencereler")]
        public OlymposItemTooltip tooltip;
        public OlymposShopDialog dialog;

        [Header("İçerik")]
        public string npcName = "Caspy";
        public string category = "Accessory";
        public List<OlymposShopItem> items = new List<OlymposShopItem>();

        [Serializable] public class SlotEvent : UnityEvent<int> { }
        [Serializable] public class AlimEvent : UnityEvent<int, int> { }   // ürün indeksi, adet

        /// <summary>Bir ürüne basıldı (listedeki genel indeks).</summary>
        public SlotEvent onItemClicked = new SlotEvent();
        /// <summary>Satın alma onaylandı: (ürün indeksi, adet).</summary>
        public AlimEvent onBuyConfirmed = new AlimEvent();
        /// <summary>"Sell selected items." ile satış istendi.</summary>
        public UnityEvent onSellSelected = new UnityEvent();
        public SlotEvent onPageChanged = new SlotEvent();
        public UnityEvent onClose = new UnityEvent();

        int sayfa;
        bool cokluSatis;
        long oyuncuParasi;
        readonly HashSet<int> secili = new HashSet<int>();

        public int Sayfa { get { return sayfa; } }
        public int SayfaSayisi { get { return Mathf.Max(1, Mathf.CeilToInt(items.Count / (float)SayfaBasiSlot)); } }
        public bool CokluSatis { get { return cokluSatis; } }
        /// <summary>Çoklu satışta seçili olan ürünlerin listedeki indeksleri.</summary>
        public IEnumerable<int> SeciliUrunler { get { return secili; } }

        void OnValidate() { ApplyBackgroundAlpha(); }

        public void ApplyBackgroundAlpha()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void Awake()
        {
            ApplyBackgroundAlpha();
            for (int i = 0; i < SayfaBasiSlot; i++)
            {
                int yerel = i;
                if (slotButtons != null && i < slotButtons.Length && slotButtons[i] != null)
                    slotButtons[i].onClick.AddListener(() => SlotaBasildi(yerel));
            }
            if (prevPageButton != null) prevPageButton.onClick.AddListener(() => SayfaGit(sayfa - 1));
            if (nextPageButton != null) nextPageButton.onClick.AddListener(() => SayfaGit(sayfa + 1));
            if (multipleSellingButton != null) multipleSellingButton.onClick.AddListener(() => SetMultipleSelling(!cokluSatis));
            if (sellSelectedButton != null) sellSelectedButton.onClick.AddListener(() => onSellSelected.Invoke());
            if (closeButton != null)
                closeButton.onClick.AddListener(() =>
                {
                    onClose.Invoke();
                    if (closeHidesWindow) gameObject.SetActive(false);
                });
            if (dialog != null) dialog.onConfirm.AddListener(DiyalogOnaylandi);
            SetMultipleSelling(false);
            Yenile();
        }

        // ------------------------------------------------------------------
        /// <summary>Dükkânı doldurur ve ilk sayfaya döner.</summary>
        public void SetShop(string ad, string kategori, IEnumerable<OlymposShopItem> urunler)
        {
            npcName = ad; category = kategori;
            items.Clear();
            if (urunler != null) items.AddRange(urunler);
            sayfa = 0; secili.Clear();
            Yenile();
        }

        /// <summary>"Total Amount" satırında gösterilen oyuncu parası.</summary>
        public void SetPlayerMoney(long para)
        {
            oyuncuParasi = para;
            if (totalAmountText != null) totalAmountText.text = Num(para);
        }

        public void SetMultipleSelling(bool acik)
        {
            cokluSatis = acik;
            if (multipleSellingCheck != null) multipleSellingCheck.enabled = acik;
            if (!acik) secili.Clear();
            SecimleriYenile();
        }

        public void SayfaGit(int yeni)
        {
            int n = SayfaSayisi;
            sayfa = Mathf.Clamp(yeni, 0, n - 1);
            Yenile();
            onPageChanged.Invoke(sayfa);
        }

        // ------------------------------------------------------------------
        void SlotaBasildi(int yerel)
        {
            int genel = sayfa * SayfaBasiSlot + yerel;
            if (genel < 0 || genel >= items.Count) return;
            var urun = items[genel];
            if (urun.Bos) return;

            if (cokluSatis)
            {
                if (!secili.Remove(genel)) secili.Add(genel);
                SecimleriYenile();
            }
            else if (tooltip != null)
            {
                var rt = slotButtons[yerel].transform as RectTransform;
                tooltip.Show(urun, rt != null ? rt.anchoredPosition : Vector2.zero);
            }
            onItemClicked.Invoke(genel);
        }

        /// <summary>Satın alma onay diyaloğunu açar (oyun mantığı çağırır).</summary>
        public void ShowBuyConfirm(int genelIndeks)
        {
            if (dialog == null || genelIndeks < 0 || genelIndeks >= items.Count) return;
            bekleyen = genelIndeks;
            var u = items[genelIndeks];
            dialog.ShowBuy(u.name, oyuncuParasi - u.buyPrice);
        }

        /// <summary>Satış adedi diyaloğunu açar.</summary>
        public void ShowSellCount(int genelIndeks, int enCokAdet)
        {
            if (dialog == null || genelIndeks < 0 || genelIndeks >= items.Count) return;
            bekleyen = genelIndeks;
            dialog.ShowSellCount(items[genelIndeks].name, enCokAdet);
        }

        int bekleyen = -1;
        void DiyalogOnaylandi(int adet)
        {
            if (bekleyen < 0) return;
            onBuyConfirmed.Invoke(bekleyen, adet);
            bekleyen = -1;
        }

        // ------------------------------------------------------------------
        void Yenile()
        {
            if (titleText != null) titleText.text = npcName + "[" + category + "]";
            if (pageText != null) pageText.text = (sayfa + 1) + "/" + SayfaSayisi;
            for (int i = 0; i < SayfaBasiSlot; i++)
            {
                int genel = sayfa * SayfaBasiSlot + i;
                var u = (genel >= 0 && genel < items.Count) ? items[genel] : new OlymposShopItem();
                if (slotIcons != null && i < slotIcons.Length && slotIcons[i] != null)
                {
                    slotIcons[i].sprite = u.icon;
                    slotIcons[i].enabled = u.icon != null;
                }
            }
            SecimleriYenile();
            if (tooltip != null) tooltip.Hide();
        }

        void SecimleriYenile()
        {
            for (int i = 0; i < SayfaBasiSlot; i++)
            {
                if (slotSelection == null || i >= slotSelection.Length || slotSelection[i] == null) continue;
                int genel = sayfa * SayfaBasiSlot + i;
                slotSelection[i].enabled = cokluSatis && secili.Contains(genel);
            }
        }

        /// <summary>1673 -> "1,673" (dükkân penceresinde sayılar virgülle ayrılır).</summary>
        public static string Num(long value)
        {
            bool neg = value < 0;
            string s = (neg ? -value : value).ToString();
            var sb = new StringBuilder();
            int first = s.Length % 3; if (first == 0) first = 3;
            sb.Append(s, 0, first);
            for (int i = first; i < s.Length; i += 3) { sb.Append(','); sb.Append(s, i, 3); }
            return neg ? "-" + sb : sb.ToString();
        }
    }
}

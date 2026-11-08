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
        public const int EnvSutun = 7, EnvSatir = 4;
        public const int EnvanterSlot = EnvSutun * EnvSatir;   // 28

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
        [Tooltip("Çoklu satışta seçili slotu işaretlemek için — OYUNDA BÖYLE BİR VURGU YOK. " +
                 "Kurucu doldurmaz; kendi geri bildiriminizi isterseniz buraya bağlayın.")]
        public Image[] slotSelection = new Image[SayfaBasiSlot];

        [Header("Envanter ızgarası (7 x 4) — oyuncunun çantası, satış buradan yapılır")]
        public Image[] invIcons = new Image[EnvanterSlot];
        public Button[] invButtons = new Button[EnvanterSlot];
        [Tooltip("Oyunda seçim vurgusu yok; kurucu doldurmaz.")]
        public Image[] invSelection = new Image[EnvanterSlot];
        public Text[] invCounts = new Text[EnvanterSlot];

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
        [Tooltip("NPC'nin sattığı ürünler; 24'erli sayfalara bölünür.")]
        public List<OlymposShopItem> items = new List<OlymposShopItem>();
        [Tooltip("Oyuncunun çantası (28 slot). Satış bu listeden yapılır.")]
        public List<OlymposShopItem> inventory = new List<OlymposShopItem>();

        [Serializable] public class SlotEvent : UnityEvent<int> { }
        [Serializable] public class AlimEvent : UnityEvent<int, int> { }   // ürün indeksi, adet

        /// <summary>Bir ürüne basıldı (listedeki genel indeks).</summary>
        public SlotEvent onItemClicked = new SlotEvent();
        /// <summary>Satın alma onaylandı: (ürün indeksi, adet).</summary>
        public AlimEvent onBuyConfirmed = new AlimEvent();
        /// <summary>"Sell selected items." ile satış istendi.</summary>
        public UnityEvent onSellSelected = new UnityEvent();
        /// <summary>Envanterdeki bir ürüne basıldı (envanter indeksi).</summary>
        public SlotEvent onInventoryClicked = new SlotEvent();
        /// <summary>Satış onaylandı: (envanter indeksi, adet).</summary>
        public AlimEvent onSellConfirmed = new AlimEvent();
        public SlotEvent onPageChanged = new SlotEvent();
        public UnityEvent onClose = new UnityEvent();

        int sayfa;
        bool cokluSatis;
        long oyuncuParasi;
        readonly HashSet<int> secili = new HashSet<int>();
        readonly HashSet<int> seciliEnvanter = new HashSet<int>();

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
            for (int i = 0; i < EnvanterSlot; i++)
            {
                int yerel = i;
                if (invButtons != null && i < invButtons.Length && invButtons[i] != null)
                    invButtons[i].onClick.AddListener(() => EnvanterSlotunaBasildi(yerel));
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
            if (!acik) { secili.Clear(); seciliEnvanter.Clear(); }
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
                tooltip.Show(urun, oyuncuParasi, rt != null ? rt.anchoredPosition : Vector2.zero);
            }
            onItemClicked.Invoke(genel);
        }

        /// <summary>
        /// Satın alma akışı: yığılabilir üründe önce "Buy Item Count:", sonra "Need Money"
        /// onayı; tek parçalık üründe doğrudan onay.
        /// </summary>
        public void ShowBuyConfirm(int genelIndeks)
        {
            if (dialog == null || genelIndeks < 0 || genelIndeks >= items.Count) return;
            bekleyen = genelIndeks; bekleyenEnvanter = false;
            var u = items[genelIndeks];
            if (u.stackSize > 1) dialog.ShowBuyCount(u.name, u.stackSize);
            else                 dialog.ShowBuyConfirm(u.name, u.buyPrice);
        }

        /// <summary>Satış onayı: "Earn Money : N".</summary>
        public void ShowSellConfirm(int envanterIndeksi)
        {
            if (dialog == null || envanterIndeksi < 0 || envanterIndeksi >= inventory.Count) return;
            bekleyen = envanterIndeksi; bekleyenEnvanter = true;
            var u = inventory[envanterIndeksi];
            dialog.ShowSellConfirm(u.name, u.SatisFiyati);
        }

        int bekleyen = -1;
        bool bekleyenEnvanter;

        void DiyalogOnaylandi(int adet)
        {
            if (bekleyen < 0) return;
            if (bekleyenEnvanter) { onSellConfirmed.Invoke(bekleyen, adet); bekleyen = -1; return; }

            // "Buy Item Count:" onaylandiysa ikinci adim: "Need Money" onayi
            if (dialog != null && dialog.Mod == OlymposDiyalogModu.AdetSor)
            {
                var u = items[bekleyen];
                bekleyenAdet = adet;
                dialog.ShowBuyConfirm(u.name, u.buyPrice * adet);
                return;
            }
            onBuyConfirmed.Invoke(bekleyen, bekleyenAdet > 0 ? bekleyenAdet : adet);
            bekleyen = -1; bekleyenAdet = 0;
        }
        int bekleyenAdet;

        void EnvanterSlotunaBasildi(int i)
        {
            if (i < 0 || i >= inventory.Count) return;
            var u = inventory[i];
            if (u.Bos) return;
            if (cokluSatis)
            {
                if (!seciliEnvanter.Remove(i)) seciliEnvanter.Add(i);
                SecimleriYenile();
            }
            else if (tooltip != null)
            {
                var rt = invButtons[i].transform as RectTransform;
                tooltip.Show(u, oyuncuParasi, rt != null ? rt.anchoredPosition : Vector2.zero);
            }
            onInventoryClicked.Invoke(i);
        }

        /// <summary>Envanteri doldurur.</summary>
        public void SetInventory(IEnumerable<OlymposShopItem> urunler)
        {
            inventory.Clear();
            if (urunler != null) inventory.AddRange(urunler);
            EnvanteriYenile();
        }

        void EnvanteriYenile()
        {
            for (int i = 0; i < EnvanterSlot; i++)
            {
                var u = (i < inventory.Count) ? inventory[i] : new OlymposShopItem();
                if (invIcons != null && i < invIcons.Length && invIcons[i] != null)
                {
                    invIcons[i].sprite = u.icon;
                    invIcons[i].enabled = u.icon != null;
                }
                if (invCounts != null && i < invCounts.Length && invCounts[i] != null)
                {
                    bool goster = !u.Bos && u.stackSize > 1;
                    invCounts[i].gameObject.SetActive(goster);
                    if (goster) invCounts[i].text = u.stackSize.ToString();
                }
            }
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
            EnvanteriYenile();
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
            for (int i = 0; i < EnvanterSlot; i++)
            {
                if (invSelection == null || i >= invSelection.Length || invSelection[i] == null) continue;
                invSelection[i].enabled = cokluSatis && seciliEnvanter.Contains(i);
            }
        }

        /// <summary>Çoklu satışta seçili envanter slotları.</summary>
        public IEnumerable<int> SeciliEnvanterSlotlari { get { return seciliEnvanter; } }

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

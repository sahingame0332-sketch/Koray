// OLYMPOS-KO · 1298 ACCESSORY UPGRADE penceresi — TEK BASINA paket (OlymposAccessoryUpgrade1298). Olculer: arayuz/23-upgrade.md
// Govde duz siyah alfa 0.895 (olculdu); panel / yuva saydamliklari sprite'in alfasinda. Krom + dugmeler opak (orijinal piksel).
using System;
using System.Globalization;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/AccessoryUpgrade/AccessoryUpgrade Penceresi")]
    public class OlymposAccessoryUpgradePenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.895f;

        [Header("Yazilar")]
        public Text needCoinsText;
        public Text upgradeRateText;
        public Text paraText;

        [Header("Dugmeler")]
        public Button upgradeButton;
        public Button cancelButton;
        public Button previewButton;
        public Button closeButton;

        [Header("Yuvalar (ikon Image'lari; bos yuva = devre disi)")]
        public Image[] upgradeYuvalari = new Image[0];
        public Image[] envanterYuvalari = new Image[0];
        public Text[] envanterAdetleri = new Text[0];

        [Header("Deneme")]
        public bool acilistaGoster = true;
        public long denemePara = 5042580;

        [Header("Olaylar")]
        public UnityEvent onUpgrade = new UnityEvent();
        public UnityEvent onCancel = new UnityEvent();
        public UnityEvent onPreview = new UnityEvent();
        public UnityEvent onClose = new UnityEvent();

        void Awake()
        {
            if (upgradeButton != null) upgradeButton.onClick.AddListener(() => onUpgrade.Invoke());
            if (cancelButton != null) cancelButton.onClick.AddListener(() => onCancel.Invoke());
            if (previewButton != null) previewButton.onClick.AddListener(() => onPreview.Invoke());
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }

        void Start()
        {
            if (!acilistaGoster) { gameObject.SetActive(false); return; }
            Ac(denemePara);
        }

        void OnValidate() { ZeminiUygula(); }
        void ZeminiUygula() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        /// <summary>Pencereyi acar; degerler "-" ile baslar (orijinaldeki gibi).</summary>
        public void Ac(long para)
        {
            gameObject.SetActive(true); transform.SetAsLastSibling();
            SetNeedCoins("-"); SetUpgradeRate("-"); SetPara(para);
            for (int i = 0; i < upgradeYuvalari.Length; i++) SetUpgradeYuvasi(i, null);
        }

        public void Kapat() { gameObject.SetActive(false); onClose.Invoke(); }

        public void SetNeedCoins(string metin) { if (needCoinsText != null) needCoinsText.text = metin; }
        public void SetUpgradeRate(string metin) { if (upgradeRateText != null) upgradeRateText.text = metin; }
        /// <summary>Oran: 100 -> "%100,0" (orijinal bicim).</summary>
        public void SetUpgradeRate(float yuzde) { SetUpgradeRate("%" + yuzde.ToString("0.0", CultureInfo.GetCultureInfo("tr-TR"))); }
        /// <summary>Para: 5042580 -> "5,042,580".</summary>
        public void SetPara(long para) { if (paraText != null) paraText.text = para.ToString("#,0", CultureInfo.InvariantCulture); }

        public void SetUpgradeYuvasi(int i, Sprite ikon)
        {
            if (i < 0 || i >= upgradeYuvalari.Length || upgradeYuvalari[i] == null) return;
            upgradeYuvalari[i].sprite = ikon; upgradeYuvalari[i].enabled = ikon != null;
        }

        public void SetEnvanter(int i, Sprite ikon, int adet)
        {
            if (i < 0 || i >= envanterYuvalari.Length || envanterYuvalari[i] == null) return;
            envanterYuvalari[i].sprite = ikon; envanterYuvalari[i].enabled = ikon != null;
            if (i < envanterAdetleri.Length && envanterAdetleri[i] != null) envanterAdetleri[i].text = (ikon != null && adet > 1) ? adet.ToString() : "";
        }
    }
}

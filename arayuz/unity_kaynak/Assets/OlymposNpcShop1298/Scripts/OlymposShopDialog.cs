// OLYMPOS-KO · 1298 dükkân diyalogları
// İki kullanım: satın alma onayı (ürün adı + Rest Money) ve satış adedi (Sell Dna Count).
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    public class OlymposShopDialog : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.95f;

        [Header("Parçalar")]
        public Text titleText;      // ürün adı
        public Text infoText;       // "Rest Money : 904" ya da "Sell Dna Count"
        public InputField countField;   // yalnızca adet modunda görünür
        public Button confirmButton;
        public Button cancelButton;

        [Serializable] public class OnayEvent : UnityEvent<int> { }
        /// <summary>Confirm'e basıldı; parametre adet (onay modunda 1).</summary>
        public OnayEvent onConfirm = new OnayEvent();
        public UnityEvent onCancel = new UnityEvent();

        int enCok = 1;

        void OnValidate() { ApplyBackgroundAlpha(); }
        public void ApplyBackgroundAlpha()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void Awake()
        {
            ApplyBackgroundAlpha();
            if (confirmButton != null) confirmButton.onClick.AddListener(Onayla);
            if (cancelButton != null) cancelButton.onClick.AddListener(() => { onCancel.Invoke(); Hide(); });
            Hide();
        }

        /// <summary>Satın alma onayı: ürün adı + kalan para.</summary>
        public void ShowBuy(string urunAdi, long kalanPara)
        {
            Kur(urunAdi, "Rest Money : " + OlymposNpcShopWindow.Num(kalanPara), false, 1);
        }

        /// <summary>Satış adedi: sayı alanı açılır.</summary>
        public void ShowSellCount(string urunAdi, int enCokAdet)
        {
            Kur(urunAdi, "Sell Dna Count", true, enCokAdet);
        }

        void Kur(string baslik, string bilgi, bool adetAlani, int enCokAdet)
        {
            enCok = Mathf.Max(1, enCokAdet);
            if (titleText != null) titleText.text = baslik ?? "";
            if (infoText != null) infoText.text = bilgi ?? "";
            if (countField != null)
            {
                countField.gameObject.SetActive(adetAlani);
                if (adetAlani) countField.text = "1";
            }
            gameObject.SetActive(true);
        }

        void Onayla()
        {
            int adet = 1;
            if (countField != null && countField.gameObject.activeSelf)
            {
                int.TryParse(countField.text, out adet);
                adet = Mathf.Clamp(adet, 1, enCok);
            }
            onConfirm.Invoke(adet);
            Hide();
        }

        public void Hide() { gameObject.SetActive(false); }
    }
}

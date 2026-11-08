// OLYMPOS-KO · 1298 dükkân diyaloğu
// Ekran görüntülerinde üç mod var:
//   satın alma onayı : ürün adı + "Need Money : 560"
//   satış onayı      : ürün adı + "Earn Money : 106"
//   adet sorma       : ürün adı + "Buy Item Count:" + sayı alanı
// Üçünde de altta Confirm / Cancel.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    public enum OlymposDiyalogModu { SatinAlmaOnayi = 0, SatisOnayi = 1, AdetSor = 2 }

    [DisallowMultipleComponent]
    public class OlymposShopDialog : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)]
        [Tooltip("Varsayılan 0.93: diyaloğun arkasından sızan yazılar ölçülerek bulundu " +
                 "(geçirgenlik t≈0.07). Ayrıntı: arayuz/05-npc-dukkan.md")]
        public float backgroundAlpha = 0.93f;
        [Tooltip("Altın çerçeve (9-slice); içi saydam, zemini background doldurur.")]
        public Image frame;

        [Header("Parçalar")]
        public Text titleText;
        public Text infoText;
        public InputField countField;
        public Button confirmButton;
        public Button cancelButton;

        [Header("Ölçü")]
        [Tooltip("Adet alanı kapalıyken ve açıkken panelin yüksekliği (orijinalden: 254 / 317).")]
        public float heightCompact = 254f;
        public float heightWithCount = 317f;

        [Serializable] public class OnayEvent : UnityEvent<int> { }
        /// <summary>Confirm'e basıldı; parametre adet (onay modlarında 1).</summary>
        public OnayEvent onConfirm = new OnayEvent();
        public UnityEvent onCancel = new UnityEvent();

        int enCok = 1;
        OlymposDiyalogModu mod;
        public OlymposDiyalogModu Mod { get { return mod; } }

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

        public void ShowBuyConfirm(string urunAdi, long gerekenPara)
        {
            Kur(OlymposDiyalogModu.SatinAlmaOnayi, urunAdi,
                "Need Money : " + OlymposNpcShopWindow.Num(gerekenPara), 1);
        }

        public void ShowSellConfirm(string urunAdi, long kazanilacak)
        {
            Kur(OlymposDiyalogModu.SatisOnayi, urunAdi,
                "Earn Money : " + OlymposNpcShopWindow.Num(kazanilacak), 1);
        }

        public void ShowBuyCount(string urunAdi, int enCokAdet)
        {
            Kur(OlymposDiyalogModu.AdetSor, urunAdi, "Buy Item Count:", enCokAdet);
        }

        void Kur(OlymposDiyalogModu m, string baslik, string bilgi, int enCokAdet)
        {
            mod = m;
            enCok = Mathf.Max(1, enCokAdet);
            bool adet = (m == OlymposDiyalogModu.AdetSor);
            if (titleText != null) titleText.text = baslik ?? "";
            if (infoText != null) infoText.text = bilgi ?? "";
            if (countField != null)
            {
                countField.gameObject.SetActive(adet);
                if (adet) countField.text = "1";
            }
            var rt = transform as RectTransform;
            if (rt != null)
                rt.sizeDelta = new Vector2(rt.sizeDelta.x, adet ? heightWithCount : heightCompact);
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

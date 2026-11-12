// OLYMPOS-KO · 1298 fiyat girisi ("Please enter the item's price.") — 711 x 522, zemin alfa 0.97
// Alana dokununca cihazin sayi klavyesi acilir; yazilan sayi binlik ayiricili gosterilir ("99,999").
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Fiyat Diyalogu")]
    public class OlymposFiyatDiyalogu : MonoBehaviour
    {
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.97f;
        public InputField priceField;
        public Button okButton;
        public Button cancelButton;
        [Tooltip("Girilebilecek en yuksek fiyat.")]
        public long enCokFiyat = 9999999999L;

        public OlymposSayiOlayi onOnay = new OlymposSayiOlayi();
        public UnityEvent onIptal = new UnityEvent();

        bool bicimleniyor;

        void Awake()
        {
            if (okButton != null) okButton.onClick.AddListener(Onayla);
            if (cancelButton != null) cancelButton.onClick.AddListener(Iptal);
            if (priceField != null) priceField.onValueChanged.AddListener(Bicimle);
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void OnValidate() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        public long Fiyat { get { return priceField != null ? OlymposTicariBicim.ParaOku(priceField.text) : 0; } }

        public void Ac()
        {
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            if (priceField != null) priceField.text = "0";     // oyunda alan "0" ile acilir
        }

        void Bicimle(string s)
        {
            if (bicimleniyor || priceField == null) return;
            long v = OlymposTicariBicim.ParaOku(s);
            if (v > enCokFiyat) v = enCokFiyat;
            string yeni = OlymposTicariBicim.Para(v);
            if (yeni == s) return;
            bicimleniyor = true;
            priceField.text = yeni;
            priceField.caretPosition = yeni.Length;
            bicimleniyor = false;
        }

        void Onayla()
        {
            long v = Fiyat;
            gameObject.SetActive(false);
            onOnay.Invoke(v);
        }

        void Iptal()
        {
            gameObject.SetActive(false);
            onIptal.Invoke();
        }
    }
}

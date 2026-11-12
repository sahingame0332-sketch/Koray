// OLYMPOS-KO · 1298 adet girisi ("Please enter the quantity of the item.") — toplu esya koyma
// Create a Merchant'ta yiginli (adedi 1'den buyuk) esyaya dokununca fiyat diyalogundan ONCE acilir.
// 711 x 522 (tablet goruntusunde 740 x 543, olcek 1.0405); zemin siyah, alfa 0.94 (arkadan gorunen yuva kenarlarindan olculdu).
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Adet Diyalogu")]
    public class OlymposAdetDiyalogu : MonoBehaviour
    {
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.94f;
        public InputField countField;
        public Button okButton;
        public Button cancelButton;

        public OlymposSayiOlayi onOnay = new OlymposSayiOlayi();
        public UnityEvent onIptal = new UnityEvent();

        int enCok = 1;
        bool duzeltiliyor;

        void Awake()
        {
            if (okButton != null) okButton.onClick.AddListener(Onayla);
            if (cancelButton != null) cancelButton.onClick.AddListener(Iptal);
            if (countField != null) countField.onValueChanged.AddListener(Duzelt);
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void OnValidate() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        public int Adet
        {
            get
            {
                long v = countField != null ? OlymposTicariBicim.ParaOku(countField.text) : 0;
                return (int)(v < 1 ? 1 : (v > enCok ? enCok : v));
            }
        }

        /// <summary>enCokAdet: yigindaki adet. Alan bu degerle acilir (olculen ornek: 20'lik yiginda "20"; varsayim).</summary>
        public void Ac(int enCokAdet)
        {
            enCok = Mathf.Max(1, enCokAdet);
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            if (countField != null) countField.text = enCok.ToString();
        }

        // yalniz rakam; yigindan fazlasi yazilamaz
        void Duzelt(string s)
        {
            if (duzeltiliyor || countField == null || string.IsNullOrEmpty(s)) return;
            long v = OlymposTicariBicim.ParaOku(s);
            if (v > enCok) v = enCok;
            string yeni = v.ToString();
            if (yeni == s) return;
            duzeltiliyor = true;
            countField.text = yeni;
            countField.caretPosition = yeni.Length;
            duzeltiliyor = false;
        }

        void Onayla()
        {
            int n = Adet;
            gameObject.SetActive(false);
            onOnay.Invoke(n);
        }

        void Iptal()
        {
            gameObject.SetActive(false);
            onIptal.Invoke();
        }
    }
}

// OLYMPOS-KO · 1298 Item Remove penceresi — TEK BASINA paket (OlymposItemRemove1298)
// Envanterde esyayi silmek isteyince acilir: "Item Remove" / "Do You want remove this Item?" / "<esya>" / "Count:<n>" + OK / Cancel.
// Pencere 696 x 382 (2712x1220 ekranda (1067,470)). Zemin duz siyah alfa 0.92 (olculdu), cerceve + OK/Cancel opak (orijinal piksel).
// Yazilar Roboto Slab Bold 28, +2 px harf araligi; baslik #F3FB1E, digerleri #FFFFFF, ortali.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposItemRemoveOlayi : UnityEvent<string, int> { }   // (esya adi, adet)

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Item Remove/Item Remove Penceresi")]
    public class OlymposItemRemovePenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.92f;

        [Header("Parcalar")]
        public Text baslikText;
        public Text soruText;
        public Text esyaText;
        public Text adetText;
        public Button okButton;
        public Button cancelButton;

        [Header("Yazilar (orijinal)")]
        public string baslik = "Item Remove";
        public string soru = "Do You want remove this Item?";
        public string adetBicimi = "Count:{0}";

        [Header("Deneme")]
        public bool acilistaGoster = true;
        public string denemeEsya = "Wood Staff(+7)";
        public int denemeAdet = 1;

        [Header("Olaylar")]
        [Tooltip("OK: (esya adi, adet).")]
        public OlymposItemRemoveOlayi onOnay = new OlymposItemRemoveOlayi();
        public UnityEvent onIptal = new UnityEvent();

        string esya; int adet = 1;

        void Awake()
        {
            if (okButton != null) okButton.onClick.AddListener(Onayla);
            if (cancelButton != null) cancelButton.onClick.AddListener(Iptal);
            ZeminiUygula();
        }

        void Start()
        {
            if (!acilistaGoster) { gameObject.SetActive(false); return; }
            Ac(denemeEsya, denemeAdet);
        }

        void OnValidate() { ZeminiUygula(); }
        void ZeminiUygula() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        /// <summary>Pencereyi esya adi ve adetle acar.</summary>
        public void Ac(string esyaAdi, int esyaAdedi)
        {
            esya = esyaAdi; adet = Mathf.Max(1, esyaAdedi);
            if (baslikText != null) baslikText.text = baslik;
            if (soruText != null) soruText.text = soru;
            if (esyaText != null) esyaText.text = esya;
            if (adetText != null) adetText.text = string.Format(adetBicimi, adet);
            gameObject.SetActive(true); transform.SetAsLastSibling();
        }

        public void Onayla() { gameObject.SetActive(false); onOnay.Invoke(esya, adet); }
        public void Iptal() { gameObject.SetActive(false); onIptal.Invoke(); }
    }
}

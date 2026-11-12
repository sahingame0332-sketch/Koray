// OLYMPOS-KO · 1298 adet girisi penceresi ("Please enter the quantity of the item.") — TEK BASINA paket
// Merchant'a toplu (yiginli) esya koyarken acilir. 711 x 522; zemin siyah, alfa 0.94 (olculdu).
// Baslik, iki dildeki uyari, alan cercevesi ve OK / CANCEL orijinal piksellerdendir; yalniz sayi Text'tir.
// Kullanim:  pencere.Ac(yigindakiAdet);  pencere.onOnay  -> girilen adet (1..yigin) ;  pencere.onIptal
// Olculer: depoda arayuz/09-merchant.md (ek bolum).  OlymposMerchant1298 paketiyle birlikte de kullanilabilir (adlar cakismaz).
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposAdetOlayi : UnityEvent<int> { }

    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Adet Penceresi")]
    public class OlymposAdetPenceresi : MonoBehaviour
    {
        [Header("Zemin")]
        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.94f;

        [Header("Parcalar")]
        public InputField countField;
        public Button okButton;
        public Button cancelButton;

        [Header("Deneme")]
        [Tooltip("Isaretliyse sahne baslarken pencere bu adetle acik gelir (ekran goruntusundeki ornek: 20).")]
        public bool acilistaGoster = true;
        public int denemeAdedi = 20;

        [Header("Olaylar")]
        [Tooltip("OK: girilen adet (1 ile yigin arasi).")]
        public OlymposAdetOlayi onOnay = new OlymposAdetOlayi();
        public UnityEvent onIptal = new UnityEvent();

        int enCok = 1;
        bool duzeltiliyor;

        void Awake()
        {
            if (okButton != null) okButton.onClick.AddListener(Onayla);
            if (cancelButton != null) cancelButton.onClick.AddListener(Iptal);
            if (countField != null) countField.onValueChanged.AddListener(Duzelt);
            ZeminiUygula();
        }

        void Start()
        {
            if (acilistaGoster) Ac(denemeAdedi); else gameObject.SetActive(false);
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        static int Oku(string s)
        {
            long v = 0;
            if (s != null)
                for (int i = 0; i < s.Length; i++)
                    if (s[i] >= '0' && s[i] <= '9' && v < 100000000L) v = v * 10 + (s[i] - '0');
            return (int)v;
        }

        /// <summary>Alandaki gecerli adet (1..yigin).</summary>
        public int Adet
        {
            get { int v = countField != null ? Oku(countField.text) : 1; return v < 1 ? 1 : (v > enCok ? enCok : v); }
        }

        /// <summary>Pencereyi acar. Alan yigindaki adetle dolu gelir (olculen ornek: 20'lik yiginda "20"; varsayim).</summary>
        public void Ac(int yigindakiAdet)
        {
            enCok = Mathf.Max(1, yigindakiAdet);
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            if (countField != null) countField.text = enCok.ToString();
        }

        // yalniz rakam; yigindan fazlasi yazilamaz
        void Duzelt(string s)
        {
            if (duzeltiliyor || countField == null || string.IsNullOrEmpty(s)) return;
            int v = Oku(s);
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

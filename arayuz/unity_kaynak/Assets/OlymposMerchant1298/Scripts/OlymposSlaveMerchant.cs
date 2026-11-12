// OLYMPOS-KO · 1298 "Slave Merchant" penceresi (1002 x 1027, zemin alfa 0.95)
// Tezgahtaki her esya icin bir satir:  ikon · "adet/satilan" (ornek 1/0) · durum ("Not sold yet.")
// Ust sag: yenile dugmesi ve kapatma (X).  CLAIM COINS: satislardan biriken parayi alir.
// "Close Slave Merchant": tezgahi kapatir, satilmayan esyalar envantere doner ("Merchant Items Received").
// Pencere acilinca bilgi satirina "Slave Expire Time : 07Hour:59Minute" yazilir (kalan sure).
// Videoda tek satir ve hic satis yok: satilmis esyanin durum yazisi ve 8'den fazla satirin gosterimi varsayimdir.
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Slave Merchant")]
    public class OlymposSlaveMerchant : MonoBehaviour
    {
        [Serializable]
        public class Satir
        {
            public GameObject kok;
            public Image ikon;
            public Text yukseltmeText;
            public Text sayacText;
            public Text durumText;
        }

        public Image background;
        [Range(0f, 1f)] public float backgroundAlpha = 0.95f;
        public Satir[] satirlar = new Satir[0];
        public Button refreshButton;
        public Button closeButton;
        public Button claimCoinsButton;
        public Button closeSlaveButton;

        [Header("Yazilar")]
        public string satilmadiMetni = "Not sold yet.";
        [Tooltip("Videoda gorulmedi (varsayim).")]
        public string satildiMetni = "Sold.";
        [Tooltip("{0} saat, {1} dakika. Olculen: Slave Expire Time : 07Hour:59Minute")]
        public string sureBicimi = "Slave Expire Time : {0:00}Hour:{1:00}Minute";
        public string esyalarAlindiMetni = "Merchant Items Received";

        [Header("Sure")]
        [Tooltip("Slave merchant'in toplam suresi (saat). Olculen: acilistan kisa sure sonra 07:59 -> 8 saat.")]
        public float toplamSaat = 8f;

        [Header("Olaylar")]
        public OlymposMetinOlayi onBilgi = new OlymposMetinOlayi();
        public UnityEvent onYenile = new UnityEvent();
        [Tooltip("CLAIM COINS: alinan para.")]
        public OlymposSayiOlayi onParaAlindi = new OlymposSayiOlayi();
        [Tooltip("Close Slave Merchant: tezgah kapatilmali, esyalar envantere donmeli.")]
        public UnityEvent onSlaveKapatildi = new UnityEvent();
        public UnityEvent onClosed = new UnityEvent();

        OlymposTicariEsya[] tezgah;
        int[] satilan = new int[0];
        long alinabilirPara;
        float bitis = -1f;        // Time.unscaledTime cinsinden

        void Awake()
        {
            if (refreshButton != null) refreshButton.onClick.AddListener(delegate { Ciz(); onYenile.Invoke(); });
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            if (claimCoinsButton != null) claimCoinsButton.onClick.AddListener(ParayiAl);
            if (closeSlaveButton != null) closeSlaveButton.onClick.AddListener(SlaveKapat);
            if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha);
        }

        void OnValidate() { if (background != null) background.color = new Color(0f, 0f, 0f, backgroundAlpha); }

        public bool Aktif { get { return tezgah != null && bitis > 0f; } }
        public long AlinabilirPara { get { return alinabilirPara; } }

        /// <summary>Tezgah acildiginda cagrilir: sureyi baslatir.</summary>
        public void Baslat(OlymposTicariEsya[] tezgahEsyalari)
        {
            tezgah = tezgahEsyalari;
            satilan = new int[tezgah != null ? tezgah.Length : 0];
            alinabilirPara = 0;
            bitis = Time.unscaledTime + toplamSaat * 3600f;
        }

        /// <summary>Bir satis oldugunda oyun cagirir (tezgah sirasi, adet).</summary>
        public void SatisKaydet(int tezgahSirasi, int adet)
        {
            if (tezgah == null || tezgahSirasi < 0 || tezgahSirasi >= tezgah.Length || tezgah[tezgahSirasi] == null) return;
            satilan[tezgahSirasi] += adet;
            alinabilirPara += tezgah[tezgahSirasi].tezgahFiyati * adet;
            if (gameObject.activeSelf) Ciz();
        }

        public string SureMetni()
        {
            float kalan = Mathf.Max(0f, bitis - Time.unscaledTime);
            int dk = Mathf.FloorToInt(kalan / 60f);
            return string.Format(sureBicimi, dk / 60, dk % 60);
        }

        public void Ac()
        {
            if (!Aktif) return;                 // tezgah yokken pencere acilmaz (varsayim)
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            Ciz();
            onBilgi.Invoke(SureMetni());
        }

        void Ciz()
        {
            int k = 0;
            for (int i = 0; i < satirlar.Length; i++)
            {
                var s = satirlar[i];
                if (s == null || s.kok == null) continue;
                OlymposTicariEsya e = null; int sira = -1;
                while (tezgah != null && k < tezgah.Length && e == null) { sira = k; e = tezgah[k++]; }
                s.kok.SetActive(e != null);
                if (e == null) continue;
                if (s.ikon != null) { s.ikon.sprite = e.ikon; s.ikon.enabled = e.ikon != null; }
                if (s.yukseltmeText != null)
                {
                    s.yukseltmeText.gameObject.SetActive(e.yukseltme > 0);
                    s.yukseltmeText.text = "+" + e.yukseltme;
                }
                if (s.sayacText != null) s.sayacText.text = e.adet + "/" + satilan[sira];
                if (s.durumText != null) s.durumText.text = satilan[sira] > 0 ? satildiMetni : satilmadiMetni;
            }
        }

        void ParayiAl()
        {
            if (alinabilirPara <= 0) return;
            long p = alinabilirPara; alinabilirPara = 0;
            onParaAlindi.Invoke(p);
        }

        void SlaveKapat()
        {
            tezgah = null; bitis = -1f;
            gameObject.SetActive(false);
            onSlaveKapatildi.Invoke();
            onBilgi.Invoke(esyalarAlindiMetni);
            onClosed.Invoke();
        }

        public void Kapat()
        {
            if (!gameObject.activeSelf) return;
            gameObject.SetActive(false);
            onClosed.Invoke();
        }

        /// <summary>Tezgah baska yoldan kapandiysa (sure doldu vb.) durumu sifirlar.</summary>
        public void Sifirla() { tezgah = null; bitis = -1f; if (gameObject.activeSelf) Kapat(); }
    }
}

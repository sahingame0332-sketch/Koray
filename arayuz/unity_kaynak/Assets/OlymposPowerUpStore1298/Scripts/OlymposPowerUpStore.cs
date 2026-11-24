// OLYMPOS-KO · 1298 Power Up Store — ana pencere (OlymposPowerUpStore1298). Olculer: arayuz/24-powerup-store.md
// Oyun alaninin tamami (2137 x 1220, telefon 2712 x 1220 ekranin ortasi). Zemin opak (orijinal resim), 6 sekme (normal / secili sprite),
// kartlar 5 sutun; kategori: sutun 335.33 px, satir 462 px; Main Page: 347.4 / 439. Gorunen 2 satir, fazlasi dikey kaydirma (tutamak 9-dilim).
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Power Up Store/Power Up Store")]
    public class OlymposPowerUpStore : MonoBehaviour
    {
        [Header("Sekmeler (Main Page, Power-UP, Premiums, Scrolls, Special, Package)")]
        public Image[] sekmeler = new Image[6];
        public Sprite[] sekmeNormal = new Sprite[6];
        public Sprite[] sekmeSecili = new Sprite[6];
        public Button[] sekmeButonlari = new Button[6];

        [Header("Liste")]
        public ScrollRect liste;
        public RectTransform icerik;
        public OlymposPowerUpKart kartSablonu;
        public OlymposPowerUpKart anaKartSablonu;
        public Vector2 kategoriBaslangic = new Vector2(20f, 13f);
        public Vector2 kategoriAralik = new Vector2(335.33f, 462f);
        public Vector2 anaBaslangic = new Vector2(21f, 32f);
        public Vector2 anaAralik = new Vector2(347.4f, 439f);
        public int sutun = 5;
        public float gorunurYukseklik = 840f;

        [Header("Ust cubuk")]
        public Text cashText;
        public InputField arama;
        public GameObject aramaOrtusu;
        public Button closeButton, refundButton, buyCashButton;

        [Header("Acilir pencereler")]
        public OlymposPowerUpAyrinti ayrinti;
        public OlymposPowerUpPaketIcerik paketIcerik;
        public OlymposPowerUpBasari basari;
        public OlymposPowerUpCashCode cashCode;

        [Header("Veri")]
        public long cash;
        public List<OlymposPowerUpUrun> urunler = new List<OlymposPowerUpUrun>();
        public bool acilistaGoster = true;

        [Header("Olaylar")]
        public OlymposPowerUpSatinAlmaOlayi onSatinAl = new OlymposPowerUpSatinAlmaOlayi();
        public UnityEvent onRefund = new UnityEvent();
        public UnityEvent onClose = new UnityEvent();

        readonly List<OlymposPowerUpKart> kartlar = new List<OlymposPowerUpKart>();
        OlymposPowerUpKategori secili = OlymposPowerUpKategori.MainPage;

        void Awake()
        {
            for (int i = 0; i < sekmeButonlari.Length; i++)
            {
                int k = i;
                if (sekmeButonlari[i] != null) sekmeButonlari[i].onClick.AddListener(() => SekmeSec((OlymposPowerUpKategori)k));
            }
            if (closeButton != null) closeButton.onClick.AddListener(Kapat);
            if (refundButton != null) refundButton.onClick.AddListener(() => onRefund.Invoke());
            if (buyCashButton != null) buyCashButton.onClick.AddListener(() => { if (cashCode != null) cashCode.Ac(); });
            if (arama != null) arama.onValueChanged.AddListener(s => { if (aramaOrtusu != null) aramaOrtusu.SetActive(!string.IsNullOrEmpty(s)); Yenile(); });
            if (ayrinti != null) ayrinti.onSatinAl.AddListener((u, n) => onSatinAl.Invoke(u, n));
            if (kartSablonu != null) kartSablonu.gameObject.SetActive(false);
            if (anaKartSablonu != null) anaKartSablonu.gameObject.SetActive(false);
        }

        void Start()
        {
            if (!acilistaGoster) { gameObject.SetActive(false); return; }
            Ac();
        }

        public void Ac() { gameObject.SetActive(true); transform.SetAsLastSibling(); SetCash(cash); SekmeSec(OlymposPowerUpKategori.MainPage); }
        public void Kapat() { gameObject.SetActive(false); onClose.Invoke(); }

        public void SetCash(long v) { cash = v; if (cashText != null) cashText.text = OlymposPowerUpRenk.Para(v); Yenile(); }

        public void SekmeSec(OlymposPowerUpKategori k)
        {
            secili = k;
            for (int i = 0; i < sekmeler.Length; i++)
                if (sekmeler[i] != null) sekmeler[i].sprite = i == (int)k ? sekmeSecili[i] : sekmeNormal[i];
            Yenile();
            if (liste != null) liste.verticalNormalizedPosition = 1f;
        }

        /// <summary>Satin alma basarili bildirimi (sunucu onayindan sonra cagirin).</summary>
        public void Basarili(string mesaj = null) { if (basari != null) basari.Ac(mesaj); }

        public void Yenile()
        {
            foreach (var k in kartlar) if (k != null) Destroy(k.gameObject);
            kartlar.Clear();
            if (icerik == null) return;
            string ara = arama != null ? arama.text : "";
            bool aramada = !string.IsNullOrEmpty(ara);
            bool ana = secili == OlymposPowerUpKategori.MainPage && !aramada;
            var sablon = ana ? anaKartSablonu : kartSablonu;
            if (sablon == null) return;
            Vector2 bas = ana ? anaBaslangic : kategoriBaslangic, ar = ana ? anaAralik : kategoriAralik;
            int n = 0;
            foreach (var u in urunler)
            {
                if (u == null) continue;
                bool uygun = aramada ? u.ad.ToLowerInvariant().Contains(ara.ToLowerInvariant())
                                     : (ana ? u.anaSayfada : u.kategori == secili);
                if (!uygun) continue;
                var kart = Instantiate(sablon, icerik);
                kart.gameObject.SetActive(true);
                var rt = (RectTransform)kart.transform;
                rt.anchorMin = rt.anchorMax = new Vector2(0f, 1f); rt.pivot = new Vector2(0f, 1f);
                rt.anchoredPosition = new Vector2(bas.x + (n % sutun) * ar.x, -(bas.y + (n / sutun) * ar.y));
                kart.Ayarla(u, cash);
                var urun = u;
                if (kart.purchaseButton != null) kart.purchaseButton.onClick.AddListener(() => KartaTiklandi(urun));
                kartlar.Add(kart);
                n++;
            }
            int satir = (n + sutun - 1) / sutun;
            icerik.sizeDelta = new Vector2(icerik.sizeDelta.x, gorunurYukseklik + Mathf.Max(0, satir - 2) * ar.y);
        }

        void KartaTiklandi(OlymposPowerUpUrun u)
        {
            if (u.paket) { if (paketIcerik != null) paketIcerik.Ac(u); }
            else if (ayrinti != null) ayrinti.Ac(u, cash);
        }
    }
}

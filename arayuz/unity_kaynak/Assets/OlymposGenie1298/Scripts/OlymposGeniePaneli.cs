// OLYMPOS-KO · 1298 Knight Genie paneli (sag ust) — TEK BASINA paket (OlymposGenie1298)
// Panel: Baslat (>) · Durdur (kare) · Ayarlar (asagi ok) + "Knight Genie" logosu, Time Left cubugu, sunucu, CR sayaci, kanal.
// Dugmeler, cubuklar ve logo orijinal piksellerden; degisen yazilar Text (olculen font/punto/renk, bkz. arayuz/11-genie.md).
// Genie calisirken: Time Left dakika dakika azalir, karakterin ustunde GENIE rozeti gorunur, hizli slot ikonlarinin
// ustune yari saydam asma kilit biner (kilitHedefleri). Durdurunca hepsi kalkar.
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Genie/Genie Paneli")]
    public class OlymposGeniePaneli : MonoBehaviour
    {
        [Header("Dugmeler")]
        public Button baslatButton;
        public Button durdurButton;
        public Button ayarButton;

        [Header("Yazilar")]
        public Text sureText;
        public Text sunucuText;
        public Text crText;
        public Text kanalText;
        [Tooltip("Orijinal: \"Time Left : 244 Minute(s)\"")]
        public string sureBicimi = "Time Left : {0} Minute(s)";
        public string sunucu = "Ares - 1";
        public int kanal = 2;

        [Header("Sure")]
        [Tooltip("Kalan genie suresi (dakika). Genie calisirken her gercek dakikada 1 azalir.")]
        public int kalanDakika = 244;
        [Tooltip("CR geri sayimi (saniye). Kayitlarda 01:20:05 -> 01:19:45 diye geri sayiyor.")]
        public float crSaniye = 1 * 3600 + 18 * 60 + 8;

        [Header("Bagli parcalar")]
        public OlymposGenieAyarPenceresi ayarPenceresi;
        public OlymposGenieRozeti rozet;
        [Tooltip("Genie calisirken ustune kilit binecek hizli slot ikonlari (RectTransform). Bos olabilir.")]
        public List<RectTransform> kilitHedefleri = new List<RectTransform>();
        public Sprite kilitSprite;
        [Tooltip("Kilit / ikon cap orani (olculen: 96 px kilit katmani, ~118 px ikon).")]
        public float kilitOrani = 96f / 118f;

        [Header("Olaylar")]
        public UnityEvent onBaslat = new UnityEvent();
        public UnityEvent onDurdur = new UnityEvent();
        public UnityEvent onSureBitti = new UnityEvent();

        public bool Aktif { get; private set; }
        float dakikaSayac;
        readonly List<GameObject> kilitler = new List<GameObject>();

        void Awake()
        {
            if (baslatButton != null) baslatButton.onClick.AddListener(Baslat);
            if (durdurButton != null) durdurButton.onClick.AddListener(Durdur);
            if (ayarButton != null) ayarButton.onClick.AddListener(AyarlariAcKapat);
            Yenile();
        }

        void Start()
        {
            if (rozet != null) rozet.Goster(false);
            if (ayarPenceresi != null && ayarPenceresi.gameObject.activeSelf && !ayarPenceresi.acilistaGoster) ayarPenceresi.Kapat();
        }

        void Update()
        {
            if (crSaniye > 0f) { crSaniye = Mathf.Max(0f, crSaniye - Time.unscaledDeltaTime); CrYaz(); }
            if (!Aktif) return;
            dakikaSayac += Time.unscaledDeltaTime;
            if (dakikaSayac >= 60f)
            {
                dakikaSayac -= 60f;
                kalanDakika = Mathf.Max(0, kalanDakika - 1);
                SureYaz();
                if (kalanDakika == 0) { Durdur(); onSureBitti.Invoke(); }
            }
        }

        public void Baslat()
        {
            if (Aktif || kalanDakika <= 0) return;
            Aktif = true; dakikaSayac = 0f;
            if (rozet != null) rozet.Goster(true);
            KilitleriKur(true);
            onBaslat.Invoke();
        }

        public void Durdur()
        {
            if (!Aktif) return;
            Aktif = false;
            if (rozet != null) rozet.Goster(false);
            KilitleriKur(false);
            onDurdur.Invoke();
        }

        public void AyarlariAcKapat()
        {
            if (ayarPenceresi == null) return;
            if (ayarPenceresi.gameObject.activeSelf) ayarPenceresi.Kapat(); else ayarPenceresi.Ac();
        }

        public void SureEkle(int dakika) { kalanDakika = Mathf.Max(0, kalanDakika + dakika); SureYaz(); }

        public void Yenile() { SureYaz(); CrYaz(); if (sunucuText != null) sunucuText.text = sunucu; if (kanalText != null) kanalText.text = "Channel " + kanal; }

        void SureYaz() { if (sureText != null) sureText.text = string.Format(sureBicimi, kalanDakika); }

        void CrYaz()
        {
            if (crText == null) return;
            var t = TimeSpan.FromSeconds(Mathf.CeilToInt(crSaniye));
            crText.text = string.Format("CR : {0:00}:{1:00}:{2:00}", (int)t.TotalHours, t.Minutes, t.Seconds);
        }

        void KilitleriKur(bool ac)
        {
            foreach (var k in kilitler) if (k != null) Destroy(k);
            kilitler.Clear();
            if (!ac || kilitSprite == null) return;
            foreach (var h in kilitHedefleri)
            {
                if (h == null) continue;
                var go = new GameObject("GenieKilit", typeof(RectTransform));
                var rt = (RectTransform)go.transform;
                rt.SetParent(h, false);
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
                float d = Mathf.Min(h.rect.width, h.rect.height) * kilitOrani;
                rt.sizeDelta = new Vector2(d, d); rt.anchoredPosition = Vector2.zero;
                var im = go.AddComponent<Image>(); im.sprite = kilitSprite; im.raycastTarget = false;
                kilitler.Add(go);
            }
        }
    }
}

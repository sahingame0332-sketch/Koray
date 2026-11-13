// OLYMPOS-KO · 1298 Merchant — alici gorunumu · "<ad> Merchant" penceresi
// 785 x 987; zemin siyah, alfa 0.89 (olculdu). Ustte 6 x 2 tezgah yuvasi, ortada alicinin parasi, altta 7 x 4 envanteri, OK / Cancel.
// Tezgah yuvasina dokununca onTezgahEsyasi(sira) gonderilir: bilgi penceresi / satin alma onayi oyunun isidir
// (hazirlari: OlymposMerchant1298 ve OlymposSatinAlmaOnayi1298 paketleri).
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant Alici/Merchant Penceresi")]
    public class OlymposSaticiPenceresi : MonoBehaviour
    {
        public const int TezgahYuvasi = 12, EnvanterYuvasi = 28;

        [Header("Zemin")]
        public Image background;
        public Image titleBackground;
        [Range(0f, 1f)] public float backgroundAlpha = 0.89f;

        [Header("Parcalar")]
        public Text titleText;
        public Text goldText;
        public OlymposSaticiYuvasi[] tezgahYuvalari = new OlymposSaticiYuvasi[TezgahYuvasi];
        public OlymposSaticiYuvasi[] envanterYuvalari = new OlymposSaticiYuvasi[EnvanterYuvasi];
        public Button okButton;
        public Button cancelButton;
        [Tooltip("Baslik: \"<ad>\" + bu ek. Olculen: \" Merchant\"")]
        public string baslikEki = " Merchant";

        [Header("Alici (bakan oyuncu)")]
        public long para = 9322;
        [Tooltip("Alicinin envanteri, yuva sirasiyla (7 x 4). Bos yuva: bos kayit.")]
        public List<OlymposSaticiEsyasi> envanter = new List<OlymposSaticiEsyasi>();

        [Header("Olaylar")]
        [Tooltip("Tezgahtaki esyaya dokunuldu (tezgah sirasi).")]
        public OlymposSaticiSiraOlayi onTezgahEsyasi = new OlymposSaticiSiraOlayi();
        [Tooltip("Alicinin envanterindeki esyaya dokunuldu (yuva sirasi).")]
        public OlymposSaticiSiraOlayi onEnvanterEsyasi = new OlymposSaticiSiraOlayi();
        public UnityEvent onKapandi = new UnityEvent();

        List<OlymposSaticiEsyasi> tezgah = new List<OlymposSaticiEsyasi>();
        string saticiAdi = "";

        void Awake()
        {
            for (int i = 0; i < tezgahYuvalari.Length; i++)
                if (tezgahYuvalari[i] != null) { tezgahYuvalari[i].sira = i; tezgahYuvalari[i].onTiklandi.AddListener(delegate (int s) { onTezgahEsyasi.Invoke(s); }); }
            for (int i = 0; i < envanterYuvalari.Length; i++)
                if (envanterYuvalari[i] != null) { envanterYuvalari[i].sira = i; envanterYuvalari[i].onTiklandi.AddListener(delegate (int s) { onEnvanterEsyasi.Invoke(s); }); }
            if (okButton != null) okButton.onClick.AddListener(Kapat);
            if (cancelButton != null) cancelButton.onClick.AddListener(Kapat);
            ZeminiUygula();
        }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            var c = new Color(0f, 0f, 0f, backgroundAlpha);
            if (background != null) background.color = c;
            if (titleBackground != null) titleBackground.color = c;
        }

        /// <summary>99999 -> "99,999"</summary>
        public static string Para(long v)
        {
            string s = Math.Abs(v).ToString();
            var sb = new System.Text.StringBuilder();
            for (int i = 0; i < s.Length; i++)
            {
                if (i > 0 && (s.Length - i) % 3 == 0) sb.Append(',');
                sb.Append(s[i]);
            }
            return (v < 0 ? "-" : "") + sb;
        }

        public OlymposSaticiEsyasi TezgahEsyasi(int sira) { return sira >= 0 && sira < tezgah.Count ? tezgah[sira] : null; }

        public void Ac(string ad, List<OlymposSaticiEsyasi> tezgahEsyalari)
        {
            saticiAdi = ad; tezgah = tezgahEsyalari ?? new List<OlymposSaticiEsyasi>();
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            Yenile();
        }

        /// <summary>Para, tezgah ya da envanter degistiginde cagirin.</summary>
        public void Yenile()
        {
            if (titleText != null) titleText.text = saticiAdi + baslikEki;
            if (goldText != null) goldText.text = Para(para);
            for (int i = 0; i < tezgahYuvalari.Length; i++)
                if (tezgahYuvalari[i] != null) tezgahYuvalari[i].Goster(i < tezgah.Count ? tezgah[i] : null);
            for (int i = 0; i < envanterYuvalari.Length; i++)
                if (envanterYuvalari[i] != null) envanterYuvalari[i].Goster(i < envanter.Count ? envanter[i] : null);
        }

        public void Kapat()
        {
            if (!gameObject.activeSelf) return;
            gameObject.SetActive(false);
            onKapandi.Invoke();
        }
    }
}

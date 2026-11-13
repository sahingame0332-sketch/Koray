// OLYMPOS-KO · 1298 Merchant — alici gorunumu · tezgah cubugu
// Tezgah acmis oyuncunun ustunde durur: satici adi (beyaz, dis hatli), 4 yuva (tezgahin ilk 4 esyasi), OPEN / WHISPER.
// 404 x 168; bos yuva zemini siyah, alfa 0.87 (olculdu). OPEN -> "<ad> Merchant" penceresi.
// Oyunda her saticinin ustunde bir cubuk olur: prefab'i cogaltip takipNoktasi'na o oyuncunun bas ustu noktasini verin.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant Alici/Tezgah Cubugu")]
    public class OlymposSaticiCubugu : MonoBehaviour
    {
        [Header("Satici")]
        public string saticiAdi = "Itccc";
        [Tooltip("Tezgahtaki esyalar (en cok 12). Cubuk ilk 4'unu gosterir.")]
        public List<OlymposSaticiEsyasi> tezgah = new List<OlymposSaticiEsyasi>();

        [Header("Parcalar")]
        public Text adText;
        public OlymposSaticiYuvasi[] yuvalar = new OlymposSaticiYuvasi[4];
        public Image[] yuvaZeminleri = new Image[4];
        [Range(0f, 1f)] public float yuvaAlpha = 0.87f;
        public Button openButton;
        public Button whisperButton;
        [Tooltip("OPEN ile acilacak pencere.")]
        public OlymposSaticiPenceresi pencere;

        [Header("Oyuncuyu izleme (istege bagli)")]
        [Tooltip("Doluysa cubuk her karede bu noktanin ekran konumuna tasinir (saticinin bas ustu).")]
        public Transform takipNoktasi;
        public Camera kamera;
        [Tooltip("Cubugun alt-orta noktasinin, takip noktasinin ekran konumuna gore kaymasi (px).")]
        public Vector2 takipKaymasi = new Vector2(0f, 20f);

        [Header("Olaylar")]
        public UnityEvent onOpen = new UnityEvent();
        [Tooltip("WHISPER: satici adi.")]
        public OlymposSaticiAdOlayi onWhisper = new OlymposSaticiAdOlayi();
        [Tooltip("Cubuktaki yuvaya dokunuldu (tezgah sirasi).")]
        public OlymposSaticiSiraOlayi onYuvaSecildi = new OlymposSaticiSiraOlayi();

        void Awake()
        {
            for (int i = 0; i < yuvalar.Length; i++)
                if (yuvalar[i] != null) { yuvalar[i].sira = i; yuvalar[i].onTiklandi.AddListener(delegate (int s) { onYuvaSecildi.Invoke(s); }); }
            if (openButton != null) openButton.onClick.AddListener(Ac);
            if (whisperButton != null) whisperButton.onClick.AddListener(delegate { onWhisper.Invoke(saticiAdi); });
            ZeminiUygula();
        }

        void Start() { Yenile(); }

        void OnValidate() { ZeminiUygula(); }

        void ZeminiUygula()
        {
            for (int i = 0; i < yuvaZeminleri.Length; i++)
                if (yuvaZeminleri[i] != null) yuvaZeminleri[i].color = new Color(0f, 0f, 0f, yuvaAlpha);
        }

        void LateUpdate()
        {
            if (takipNoktasi == null) return;
            var k = kamera != null ? kamera : Camera.main;
            if (k == null) return;
            Vector3 e = k.WorldToScreenPoint(takipNoktasi.position);
            var rt = (RectTransform)transform;
            rt.position = new Vector3(e.x + takipKaymasi.x, e.y + takipKaymasi.y + rt.rect.height * 0.5f * rt.lossyScale.y, 0f);
        }

        /// <summary>Saticiyi ve tezgahini degistirir.</summary>
        public void Goster(string ad, List<OlymposSaticiEsyasi> esyalar)
        {
            saticiAdi = ad; tezgah = esyalar ?? new List<OlymposSaticiEsyasi>();
            gameObject.SetActive(true);
            Yenile();
        }

        public void Yenile()
        {
            if (adText != null) adText.text = saticiAdi;
            int k = 0;
            for (int i = 0; i < yuvalar.Length; i++)
            {
                OlymposSaticiEsyasi e = null;
                while (k < tezgah.Count && e == null) { var a = tezgah[k++]; if (a != null && !a.Bos) e = a; }
                if (yuvalar[i] != null) yuvalar[i].Goster(e);
            }
        }

        void Ac()
        {
            onOpen.Invoke();
            if (pencere != null) pencere.Ac(saticiAdi, tezgah);
        }
    }
}

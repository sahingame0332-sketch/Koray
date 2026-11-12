// OLYMPOS-KO · 1298 tezgah cubugu: Merchant acikken karakterin ustunde duran 4 yuvalik cerceve + OPEN / WHISPER
// Yuvalar tezgahtaki ilk 4 esyayi gosterir (bos yuva zemini siyah, alfa 0.87).
// Yuvaya dokun -> esya bilgisi (fiyatsiz, yalniz Close). OPEN -> "<ad> Merchant" penceresi. WHISPER -> ozel mesaj.
// Oyunda cubuk karakteri izler: konumu her karede karakterin ekran konumuna tasiyin (bkz. takipNoktasi).
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Merchant/Tezgah Cubugu")]
    public class OlymposTezgahCubugu : MonoBehaviour
    {
        public OlymposTicariYuva[] yuvalar = new OlymposTicariYuva[4];
        public Image[] yuvaZeminleri = new Image[4];
        [Range(0f, 1f)] public float yuvaAlpha = 0.87f;
        public Button openButton;
        public Button whisperButton;
        public OlymposEsyaBilgiPenceresi bilgi;

        [Header("Karakteri izleme (istege bagli)")]
        [Tooltip("Doluysa cubuk her karede bu noktanin ekran konumuna tasinir (karakterin basinin ustu).")]
        public Transform takipNoktasi;
        public Camera kamera;
        [Tooltip("Cubugun orta-alt noktasinin, takip noktasinin ekran konumuna gore kaymasi (px).")]
        public Vector2 takipKaymasi = new Vector2(0f, 20f);

        public UnityEvent onOpen = new UnityEvent();
        public UnityEvent onWhisper = new UnityEvent();

        OlymposTicariEsya[] tezgah;

        void Awake()
        {
            for (int i = 0; i < yuvalar.Length; i++)
                if (yuvalar[i] != null) { yuvalar[i].sira = i; yuvalar[i].onTiklandi.AddListener(Dokun); }
            if (openButton != null) openButton.onClick.AddListener(delegate { onOpen.Invoke(); });
            if (whisperButton != null) whisperButton.onClick.AddListener(delegate { onWhisper.Invoke(); });
            ZeminiUygula();
        }

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

        public void Goster(OlymposTicariEsya[] tezgahEsyalari)
        {
            tezgah = tezgahEsyalari;
            gameObject.SetActive(true);
            int k = 0;
            for (int i = 0; i < yuvalar.Length; i++)
            {
                OlymposTicariEsya e = null;
                while (tezgah != null && k < tezgah.Length && e == null) e = tezgah[k++];
                if (yuvalar[i] != null) yuvalar[i].Goster(e);
            }
        }

        public void Gizle()
        {
            if (bilgi != null) bilgi.Kapat();
            gameObject.SetActive(false);
        }

        void Dokun(int i)
        {
            if (bilgi == null || i < 0 || i >= yuvalar.Length || yuvalar[i] == null || yuvalar[i].Esya == null) return;
            bilgi.GosterFiyatsiz(yuvalar[i].Esya, (RectTransform)yuvalar[i].transform);
        }
    }
}

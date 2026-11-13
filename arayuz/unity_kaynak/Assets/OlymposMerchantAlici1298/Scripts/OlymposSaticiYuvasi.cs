// OLYMPOS-KO · 1298 Merchant — alici gorunumu · esya yuvasi
// Ikon + cerceve (gumus ya da mor) + "+N" + adet. Mor cerceveli yuvada ikon alani daha kucuktur (olculdu).
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/Merchant Alici/Esya Yuvasi")]
    public class OlymposSaticiYuvasi : MonoBehaviour
    {
        public int sira;
        public Image ikon;
        [Tooltip("Esyali yuvanin gumus cercevesi.")]
        public Image doluCerceve;
        [Tooltip("Mor cerceve (gumus cercevenin disinda ~3 px mor kenar).")]
        public Image morCerceve;
        public Text yukseltmeText;
        public Text adetText;
        public Button dugme;
        [Tooltip("Ikon kutusu (x, y, genislik, yukseklik; yuvanin sol-ustune gore): gumus cercevede / mor cercevede.")]
        public Vector4 normalIkonKutusu = new Vector4(8, 8, 70, 72);
        public Vector4 morIkonKutusu = new Vector4(16, 12, 62, 66);

        public OlymposSaticiSiraOlayi onTiklandi = new OlymposSaticiSiraOlayi();
        public OlymposSaticiEsyasi Esya { get; private set; }

        void Awake()
        {
            if (dugme != null) dugme.onClick.AddListener(delegate { onTiklandi.Invoke(sira); });
        }

        public void Goster(OlymposSaticiEsyasi e)
        {
            bool dolu = e != null && !e.Bos;
            Esya = dolu ? e : null;
            bool mor = dolu && e.morCerceve && morCerceve != null;
            if (ikon != null)
            {
                ikon.sprite = dolu ? e.ikon : null;
                ikon.enabled = dolu && e.ikon != null;
                Vector4 k = mor ? morIkonKutusu : normalIkonKutusu;
                var rt = ikon.rectTransform;
                rt.anchoredPosition = new Vector2(k.x, -k.y);
                rt.sizeDelta = new Vector2(k.z, k.w);
            }
            if (doluCerceve != null) doluCerceve.enabled = dolu && !mor;
            if (morCerceve != null) morCerceve.enabled = mor;
            if (yukseltmeText != null)
            {
                bool g = dolu && e.yukseltme > 0;
                yukseltmeText.gameObject.SetActive(g);
                if (g) yukseltmeText.text = "+" + e.yukseltme;
            }
            if (adetText != null)
            {
                bool g = dolu && e.adet > 1;
                adetText.gameObject.SetActive(g);
                if (g) adetText.text = e.adet.ToString();
            }
            if (dugme != null) dugme.interactable = dolu;
        }
    }
}

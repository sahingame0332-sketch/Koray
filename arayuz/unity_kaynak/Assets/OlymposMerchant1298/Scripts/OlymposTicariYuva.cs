// OLYMPOS-KO · 1298 esya yuvasi: ikon + dolu cercevesi + adet + "+N" yukseltme etiketi
using System;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable] public class OlymposYuvaOlayi : UnityEvent<int> { }

    [AddComponentMenu("OLYMPOS/1298/Merchant/Esya Yuvasi")]
    public class OlymposTicariYuva : MonoBehaviour
    {
        public int sira;
        public Image ikon;
        [Tooltip("Esyali yuvanin acik renkli cercevesi (orijinalde dolu yuvanin kenari daha parlak).")]
        public Image doluCerceve;
        public Text adetText;
        public Text yukseltmeText;
        public Button dugme;
        public OlymposYuvaOlayi onTiklandi = new OlymposYuvaOlayi();

        public OlymposTicariEsya Esya { get; private set; }

        void Awake()
        {
            if (dugme != null) dugme.onClick.AddListener(delegate { onTiklandi.Invoke(sira); });
        }

        public void Goster(OlymposTicariEsya e)
        {
            Esya = e;
            bool dolu = e != null;
            if (ikon != null) { ikon.sprite = dolu ? e.ikon : null; ikon.enabled = dolu && e.ikon != null; }
            if (doluCerceve != null) doluCerceve.enabled = dolu;
            if (adetText != null)
            {
                bool g = dolu && e.adet > 1;
                adetText.gameObject.SetActive(g);
                if (g) adetText.text = e.adet.ToString();
            }
            if (yukseltmeText != null)
            {
                bool g = dolu && e.yukseltme > 0;
                yukseltmeText.gameObject.SetActive(g);
                if (g) yukseltmeText.text = "+" + e.yukseltme;
            }
        }
    }
}

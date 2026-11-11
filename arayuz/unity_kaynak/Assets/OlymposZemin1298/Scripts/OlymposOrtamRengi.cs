// OLYMPOS-KO · 1298 ortam rengi: gok rengi, gorus mesafesi sonundaki duz renk ve zemin sicakligi.
// Olculen degerler (arayuz/08-zemin.md):
//   Moradon  gok #ADC6D6   uzak #D0EA84 (limon)      Kale  gok #AEC7D7  uzak #C0D47E      Kir  gok #BFCDDB  uzak #B2C7D4
// Zeminde mesafeyle KADEMELI solma olculmedi (Moradon yolunda renk ufka kadar sabit); uzak nesneler
// gorus mesafesinin sonunda tek duz renge donuyor. Bu yuzden sis varsayilan olarak dar bir aralikta (%90-%100) acilir.
using UnityEngine;

namespace Olympos.Zemin
{
    public enum OlymposOrtamOnAyari { Moradon, Kale, Kir, Ozel }

    [ExecuteAlways]
    [DisallowMultipleComponent]
    [AddComponentMenu("OLYMPOS/1298/Zemin/Ortam Rengi")]
    public class OlymposOrtamRengi : MonoBehaviour
    {
        [Header("On ayar (olculen renkler)")]
        public OlymposOrtamOnAyari onAyar = OlymposOrtamOnAyari.Moradon;
        public Color gokRengi = new Color32(0xAD, 0xC6, 0xD6, 0xFF);
        public Color uzakRenk = new Color32(0xD0, 0xEA, 0x84, 0xFF);

        [Header("Kamera")]
        [Tooltip("Bos birakilirsa Camera.main kullanilir. Arka plan duz gok rengine boyanir.")]
        public Camera kamera;
        public bool kamerayiBoya = true;

        [Header("Uzak renk (sis)")]
        public bool sisKullan = true;
        [Tooltip("Gorus mesafesi (dunya birimi). Ekrandan olculemedi: kendi haritaniza gore ayarlayin.")]
        public float gorusMesafesi = 180f;
        [Tooltip("Sisin basladigi yer, gorus mesafesinin orani. Olculen davranis: keskin gecis (0.9).")]
        [Range(0f, 0.99f)] public float sisBaslangicOrani = 0.9f;

        [Header("Zemin sicakligi")]
        [Tooltip("Rengi kaydirilacak zemin malzemeleri (Olympos/Zemin1298).")]
        public Material[] zeminMalzemeleri = new Material[0];
        [Tooltip("0 = olculen renk. Arti: daha sicak (sari-turuncu), eksi: daha soguk (mavi). Kelvin farki.")]
        [Range(-3000f, 3000f)] public float sicaklikKaymasiK = 0f;
        [Tooltip("Zemin parlakligi carpani. 1 = olculen.")]
        [Range(0.5f, 1.5f)] public float parlaklik = 1f;

        static readonly int RenkId = Shader.PropertyToID("_Renk");

        void OnEnable() { Uygula(); }
        void OnValidate() { OnAyariYukle(); Uygula(); }

        void OnAyariYukle()
        {
            switch (onAyar)
            {
                case OlymposOrtamOnAyari.Moradon:
                    gokRengi = new Color32(0xAD, 0xC6, 0xD6, 0xFF); uzakRenk = new Color32(0xD0, 0xEA, 0x84, 0xFF); break;
                case OlymposOrtamOnAyari.Kale:
                    gokRengi = new Color32(0xAE, 0xC7, 0xD7, 0xFF); uzakRenk = new Color32(0xC0, 0xD4, 0x7E, 0xFF); break;
                case OlymposOrtamOnAyari.Kir:
                    gokRengi = new Color32(0xBF, 0xCD, 0xDB, 0xFF); uzakRenk = new Color32(0xB2, 0xC7, 0xD4, 0xFF); break;
            }
        }

        public void OnAyarSec(OlymposOrtamOnAyari yeni) { onAyar = yeni; OnAyariYukle(); Uygula(); }

        public void Uygula()
        {
            var k = kamera != null ? kamera : Camera.main;
            if (kamerayiBoya && k != null)
            {
                k.clearFlags = CameraClearFlags.SolidColor;
                k.backgroundColor = gokRengi;
            }
            RenderSettings.fog = sisKullan;
            if (sisKullan)
            {
                RenderSettings.fogMode = FogMode.Linear;
                RenderSettings.fogColor = uzakRenk;
                RenderSettings.fogEndDistance = Mathf.Max(1f, gorusMesafesi);
                RenderSettings.fogStartDistance = RenderSettings.fogEndDistance * sisBaslangicOrani;
            }
            // 6600 K notr kabul edilir; kayma kadar sicak/soguk carpan
            Color c = OlymposZeminPaleti.SicaklikCarpani(6600f, 6600f - sicaklikKaymasiK) * parlaklik;
            c.a = 1f;
            for (int i = 0; i < zeminMalzemeleri.Length; i++)
                if (zeminMalzemeleri[i] != null && zeminMalzemeleri[i].HasProperty(RenkId)) zeminMalzemeleri[i].SetColor(RenkId, c);
        }
    }
}

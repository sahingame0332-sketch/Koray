// OLYMPOS-KO · 1298 zemin olcumleri (ekran goruntulerinden) — arayuz/08-zemin.md
// Renkler ekranda olculen sRGB ortalamalaridir; "sicaklik" bu rengin ilintili renk sicakligidir (McCamy),
// sahnedeki isigin sicakligi degil.
using UnityEngine;

namespace Olympos.Zemin
{
    public enum OlymposZeminTuru { Kum, TasDoseme, TasTugla, TasArnavut, Cim }

    public static class OlymposZeminPaleti
    {
        public struct Olcum
        {
            public string doku;            // Textures/ altindaki dosya adi (uzantisiz)
            public Color32 renk;           // ortalama renk
            public int sicaklikK;          // ilintili renk sicakligi
            public float karoKarakterBoyu; // karonun bir kenari, karakter boyu cinsinden
            public Olcum(string d, Color32 r, int k, float b) { doku = d; renk = r; sicaklikK = k; karoKarakterBoyu = b; }
        }

        public static readonly Olcum Kum        = new Olcum("zemin_kum",         new Color32(0xB4, 0x8F, 0x57, 0xFF), 3505, 5.6f);
        public static readonly Olcum TasDoseme  = new Olcum("zemin_tas_doseme",  new Color32(0x83, 0x7E, 0x6A, 0xFF), 5133, 5.2f);
        public static readonly Olcum TasTugla   = new Olcum("zemin_tas_tugla",   new Color32(0x71, 0x6C, 0x5A, 0xFF), 5080, 2.2f);
        public static readonly Olcum TasArnavut = new Olcum("zemin_tas_arnavut", new Color32(0x7D, 0x77, 0x62, 0xFF), 5022, 3.1f);
        public static readonly Olcum Cim        = new Olcum("zemin_cim",         new Color32(0x31, 0x38, 0x0E, 0xFF), 4484, 4.5f);

        public static Olcum Al(OlymposZeminTuru t)
        {
            switch (t)
            {
                case OlymposZeminTuru.Kum: return Kum;
                case OlymposZeminTuru.TasDoseme: return TasDoseme;
                case OlymposZeminTuru.TasTugla: return TasTugla;
                case OlymposZeminTuru.TasArnavut: return TasArnavut;
                default: return Cim;
            }
        }

        /// <summary>Karonun dunya birimindeki kenari. karakterBoyu: sizin karakterinizin Unity birimindeki boyu.</summary>
        public static float KaroBoyu(OlymposZeminTuru t, float karakterBoyu) { return Al(t).karoKarakterBoyu * karakterBoyu; }

        /// <summary>Kara cisim renk sicakligi -> RGB carpani (Tanner Helland yaklasimi, 1000-40000 K). 6600 K ~ beyaz.</summary>
        public static Color KelvindenRenk(float kelvin)
        {
            float t = Mathf.Clamp(kelvin, 1000f, 40000f) / 100f;
            float r, g, b;
            if (t <= 66f)
            {
                r = 255f;
                g = 99.4708025861f * Mathf.Log(t) - 161.1195681661f;
                b = t <= 19f ? 0f : 138.5177312231f * Mathf.Log(t - 10f) - 305.0447927307f;
            }
            else
            {
                r = 329.698727446f * Mathf.Pow(t - 60f, -0.1332047592f);
                g = 288.1221695283f * Mathf.Pow(t - 60f, -0.0755148492f);
                b = 255f;
            }
            return new Color(Mathf.Clamp01(r / 255f), Mathf.Clamp01(g / 255f), Mathf.Clamp01(b / 255f), 1f);
        }

        /// <summary>Rengi "olculenK" sicakligindan "hedefK" sicakligina kaydiran carpan (en buyuk kanal 1 olacak sekilde).</summary>
        public static Color SicaklikCarpani(float olculenK, float hedefK)
        {
            Color a = KelvindenRenk(olculenK), h = KelvindenRenk(hedefK);
            float r = h.r / Mathf.Max(a.r, 0.001f), g = h.g / Mathf.Max(a.g, 0.001f), b = h.b / Mathf.Max(a.b, 0.001f);
            float m = Mathf.Max(r, Mathf.Max(g, b));
            return new Color(r / m, g / m, b / m, 1f);
        }
    }
}

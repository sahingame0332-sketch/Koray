// OLYMPOS-KO · 1298 Power Up Store — veri tipleri ve renk uzayi yardimcisi (OlymposPowerUpStore1298).
// Olculdu: oyun saydamligi LINEER isik uzayinda karistiriyor (kart karartmasi lineer uzayda uc kanalda esit, sRGB'de degil).
using System;
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.UI
{
    public enum OlymposPowerUpKategori { MainPage = 0, PowerUP = 1, Premiums = 2, Scrolls = 3, Special = 4, Package = 5 }

    [Serializable]
    public class OlymposPowerUpUrun
    {
        public string ad = "Teleport Scroll";
        public Sprite ikon;
        [Tooltip("Ikonun sag altindaki sayi (orijinalde 1 de yaziliyor)")] public int adet = 1;
        public int fiyat;
        [TextArea] public string aciklama = "";
        public OlymposPowerUpKategori kategori = OlymposPowerUpKategori.Scrolls;
        [Tooltip("Main Page'de de gosterilsin")] public bool anaSayfada;
        [Tooltip("Paket: Purchase -> paket icerik penceresi")] public bool paket;
    }

    [Serializable] public class OlymposPowerUpSatinAlmaOlayi : UnityEvent<OlymposPowerUpUrun, int> { }   // (urun, adet)
    [Serializable] public class OlymposPowerUpKodOlayi : UnityEvent<string> { }

    public static class OlymposPowerUpRenk
    {
        /// <summary>Olculen lineer gecirgenlikten (siyah orttu) projenin renk uzayina gore Image alfasi.</summary>
        public static float SiyahAlfa(float gecirgenlikLineer)
        {
            float t = Mathf.Clamp01(gecirgenlikLineer);
            return QualitySettings.activeColorSpace == ColorSpace.Linear ? 1f - t : 1f - Mathf.Pow(t, 1f / 2.2f);
        }
        /// <summary>Basari ortusu: lineer uzayda gri 0.24, alfa 0.24 (sRGB gri ~135). Gamma projede en yakin sRGB karsiligi.</summary>
        public static Color GriOrtu()
        {
            return QualitySettings.activeColorSpace == ColorSpace.Linear ? new Color(135f / 255f, 135f / 255f, 135f / 255f, 0.24f)
                                                                         : new Color(129f / 255f, 129f / 255f, 129f / 255f, 0.45f);
        }
        public static readonly Color FiyatYetmez = new Color(0xF9 / 255f, 0x49 / 255f, 0x22 / 255f);
        public static readonly Color FiyatYeter = new Color(0xFD / 255f, 0xDE / 255f, 0x24 / 255f);
        public static string Para(long v) { return v.ToString("#,0", System.Globalization.CultureInfo.GetCultureInfo("tr-TR")); }  // 1.000
    }
}

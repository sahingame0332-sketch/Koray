// OLYMPOS-KO · 1298 Merchant / ekipman — ortak veri tipleri
// Olculer ve davranis: arayuz/09-merchant.md
using System;
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.UI
{
    public enum OlymposBilgiRengi { Beyaz, Bonus, Zehir, Kirmizi }

    [Serializable]
    public struct OlymposBilgiSatiri
    {
        public string metin;
        [Tooltip("Beyaz: normal · Bonus: sari-yesil (#98BF2A) · Zehir: yesil (#81C267) · Kirmizi: karsilanmayan gereksinim")]
        public OlymposBilgiRengi renk;
        public OlymposBilgiSatiri(string m, OlymposBilgiRengi r) { metin = m; renk = r; }
    }

    /// <summary>Envanterde, tezgahta ya da ekipmanda duran bir esya.</summary>
    [Serializable]
    public class OlymposTicariEsya
    {
        public string id;
        [Tooltip("Ornek: Short Bow(+5)")]
        public string ad;
        [Tooltip("Adin ve tur satirinin rengi. Olculen: normal #FFE7E9, Upgrade Item #CA89E7")]
        public Color adRengi = new Color32(0xFF, 0xE7, 0xE9, 0xFF);
        [Tooltip("Adin altindaki satir. Ornek: Upgrade Item · normal esyada \"-\"")]
        public string turSatiri = "-";
        public Sprite ikon;
        [Tooltip("Yigin adedi. 2 ve uzeri yuvanin sag altinda yazar.")]
        public int adet = 1;
        [Tooltip("Yukseltme seviyesi. 0'dan buyukse yuvanin sag ustunde mor \"+N\" yazar.")]
        public int yukseltme;
        public OlymposBilgiSatiri[] statlar = new OlymposBilgiSatiri[0];
        [Tooltip("Ornek: (Rogue Item). Bos birakilabilir.")]
        public string sinifSatiri;
        [Tooltip("Karakterin sinifi bu esyaya uygun mu? Uygun degilse sinif satiri kirmizi yazar.")]
        public bool sinifUygun = true;
        [Tooltip("Ornek: (Bow). Doluysa ustunde bir bos satirla yazilir.")]
        public string cinsSatiri;
        [Tooltip("Ornek: Item Grade : Low Class")]
        public string dereceSatiri;
        [TextArea(1, 4)] public string aciklama;
        [Tooltip("NPC dukkanindaki fiyat (Buy Price).")]
        public long npcFiyati;

        [Header("Ekipman")]
        public bool kusanilir;
        public int bonusHp;
        public int bonusMp;

        [NonSerialized] public long tezgahFiyati;      // Create a Merchant'ta girilen fiyat
    }

    [Serializable] public class OlymposTicariEsyaOlayi : UnityEvent<OlymposTicariEsya> { }
    [Serializable] public class OlymposMetinOlayi : UnityEvent<string> { }
    [Serializable] public class OlymposSayiOlayi : UnityEvent<long> { }

    public static class OlymposTicariBicim
    {
        /// <summary>99999 -> "99,999" (oyundaki binlik ayirici virgul).</summary>
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

        public static long ParaOku(string s)
        {
            long v = 0; bool var = false;
            if (s == null) return 0;
            for (int i = 0; i < s.Length; i++)
                if (s[i] >= '0' && s[i] <= '9') { if (v < 99999999999L) v = v * 10 + (s[i] - '0'); var = true; }
            return var ? v : 0;
        }
    }
}

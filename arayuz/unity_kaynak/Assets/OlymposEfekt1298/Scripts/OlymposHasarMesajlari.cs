// OLYMPOS-KO · 1298 hasar / skill mesajlari (Information paneli satirlari)
// Bu oyunda hasar EKRANDA SAYI OLARAK UCMUYOR: hasar Information panelinde yazili satirla, hedefin can cubugunun
// azalmasiyla ve vurus isiklariyla gosteriliyor (kayitta yuzen sayi yok). Renkler kayittan olculdu.
// Font: Roboto Slab Bold 31 (telefon duzeninde 30), satir adimi ~30 px.
using UnityEngine;

namespace Olympos.Efekt
{
    public static class OlymposHasarMesajlari
    {
        public static readonly Color Kirmizi = new Color32(0xF8, 0x00, 0x01, 0xFF);   // verilen hasar, SP kullanimi
        public static readonly Color Beyaz = new Color32(0xFF, 0xFF, 0xFF, 0xFF);     // toplam hasar ("received")
        public static readonly Color Sari = new Color32(0xFC, 0xE6, 0x00, 0xFF);      // "Using - <skill>"

        /// <summary>"Using - Pillar Of Fire" (sari)</summary>
        public static string Kullanim(string skill) { return Renkli("Using - " + skill, Sari); }
        /// <summary>"Kecoon captain is inflicted with 27 HP damage." (kirmizi)</summary>
        public static string Hasar(string hedef, int hp) { return Renkli(hedef + " is inflicted with " + hp + " HP damage.", Kirmizi); }
        /// <summary>"Kecoon captain received 199 damage" (beyaz)</summary>
        public static string Aldi(string hedef, int hasar) { return Renkli(hedef + " received " + hasar + " damage", Beyaz); }
        /// <summary>"160 SP Used" (kirmizi)</summary>
        public static string SpKullanildi(int sp) { return Renkli(sp + " SP Used", Kirmizi); }

        public static string Renkli(string metin, Color c)
        {
            return "<color=#" + ColorUtility.ToHtmlStringRGB(c) + ">" + metin + "</color>";
        }
    }
}

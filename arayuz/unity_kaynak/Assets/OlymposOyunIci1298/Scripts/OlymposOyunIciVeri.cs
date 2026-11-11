// OLYMPOS-KO · 1298 oyun ici — ortak veri tipleri
// Olculer ve davranis: arayuz/06-oyun-ici.md
using System;
using UnityEngine;

namespace Olympos.UI
{
    /// <summary>Envanterdeki bir esya (scroll, iksir...). Sayac calisma aninda degisir.</summary>
    [Serializable]
    public class OlymposEsya
    {
        [Tooltip("Benzersiz kimlik; hizli slotlar ve kayitlar bununla esler.")]
        public string id;
        [Tooltip("Pencerede gorunen ad. Ornek: Scroll of 500HP Up(L)")]
        public string ad;
        [Tooltip("Adin altindaki sari satir. Ornek: Store Item")]
        public string turSatiri = "Store Item";
        [TextArea(1, 3)] public string aciklama;
        public Sprite ikon;
        [Tooltip("Yigin adedi. Hizli slottaki rakam budur.")]
        public int adet = 1;
        [Tooltip("Bilgi satirinda 'Using - ...' sonrasinda yazan ad. Ornek: Hp Scroll 500(L)")]
        public string kullanimAdi;
        [Tooltip("Basildiginda eklenen etkinin suresi (saniye). 0 = etki ikonu eklenmez.")]
        public float buffSuresi = 3600f;
        public bool kendineKullanilir = true;
        public bool hedefeKullanilir = true;
        public bool kusanilir = false;
    }

    /// <summary>Drop listesindeki bir kutu: tek esya ya da icinde esyalar olan grup.</summary>
    [Serializable]
    public class OlymposDropGirdisi
    {
        public string ad;
        public Sprite ikon;
        [Tooltip("Kutu etiketi ve ipucundaki 'Drop Rate'. Olculen degerler: Middle, Low")]
        public string oran = "Middle";
        [Tooltip("Isaretliyse kutuya basinca icindekiler listelenir (GROUP ? kutusu).")]
        public bool grup;
        public OlymposDropGirdisi[] grupIcerigi;

        [Header("Ipucu")]
        public string turSatiri = "Upgrade Item";
        public Color adRengi = new Color32(0xCA, 0x89, 0xE7, 0xFF);
        public OlymposDropSatiri[] statlar;
        [Tooltip("Ornek: (Warrior Item) — kirmizi, ortali")]
        public string sinifSatiri;
        [Tooltip("Ornek: Item Grade : Low Class — yesil, ortali")]
        public string dereceSatiri;
        [TextArea(1, 3)] public string aciklama;
    }

    public enum OlymposSatirRengi { Beyaz, Yesil, Kirmizi }

    [Serializable]
    public struct OlymposDropSatiri
    {
        public string metin;
        public OlymposSatirRengi renk;
    }

    [Serializable]
    public class OlymposCanavarDrop
    {
        public string canavarAdi;
        public OlymposDropGirdisi[] droplar;
    }

    /// <summary>Save Skill Slot Stat'taki bir kayit.</summary>
    [Serializable]
    public class OlymposSkillKaydi
    {
        public bool dolu;
        public string[] slotEsyaIdleri;
        public string[] dalAdlari;
        public int[] dalPuanlari;
    }
}

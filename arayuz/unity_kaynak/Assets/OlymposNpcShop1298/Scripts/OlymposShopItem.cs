// OLYMPOS-KO · 1298 NPC dükkânı · ürün verisi
// Alanlar oyundaki ipucu kutusunun satırlarıyla birebir eşleşir.
using System;
using UnityEngine;

namespace Olympos.UI
{
    /// <summary>Ürün kalitesi. İpucundaki ad ve kalite satırının rengini belirler.</summary>
    public enum OlymposItemKalite
    {
        Regular = 0,   // beyaz  — "Regular Item"
        Magic   = 1,   // mavi   — "Magic Item"
        Upgrade = 2,   // mor    — "Upgrade Item"
    }

    /// <summary>İpucundaki tek bir stat satırı. Oyuncu şartı karşılamıyorsa kırmızı yazılır.</summary>
    [Serializable]
    public struct OlymposStatSatiri
    {
        public string metin;
        [Tooltip("true ise satır kırmızı yazılır (ör. karşılanmayan \"Required Strenght : 62\").")]
        public bool karsilanmiyor;

        public OlymposStatSatiri(string m, bool k = false) { metin = m; karsilanmiyor = k; }
    }

    [Serializable]
    public struct OlymposShopItem
    {
        public Sprite icon;
        public string name;
        public OlymposItemKalite kalite;

        [Tooltip("İpucunun kırmızı/sarı Buy Price satırı. Oyuncunun parası yetmiyorsa kırmızı olur.")]
        public long buyPrice;
        [Tooltip("Satışta kazanılacak tutar (Earn Money). 0 ise buyPrice kullanılır.")]
        public long sellPrice;

        public OlymposStatSatiri[] statLines;

        [Tooltip("Sınıf/tür satırı: \"(Staff)\", \"(Warrior Item)\", \"(Magician Item)\" …")]
        public string classLine;
        [Tooltip("true ise sınıf satırı kırmızı yazılır (ürün bu sınıfa ait değil).")]
        public bool classLineKirmizi;

        [Tooltip("Yeşil yazılan derece satırı: \"Item Grade : Low Class\".")]
        public string gradeLine;

        [TextArea(2, 4)] public string description;

        [Tooltip("Bir slotta yığılabilen adet. 1'den büyükse satın alırken \"Buy Item Count:\" diyaloğu açılır.")]
        public int stackSize;

        public bool Bos { get { return string.IsNullOrEmpty(name) && icon == null; } }
        public long SatisFiyati { get { return sellPrice > 0 ? sellPrice : buyPrice; } }

        /// <summary>Kalite satırının metni ("Regular Item" vb.).</summary>
        public string KaliteMetni
        {
            get
            {
                switch (kalite)
                {
                    case OlymposItemKalite.Magic:   return "Magic Item";
                    case OlymposItemKalite.Upgrade: return "Upgrade Item";
                    default:                        return "Regular Item";
                }
            }
        }
    }
}

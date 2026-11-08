// OLYMPOS-KO · 1298 NPC dükkânı · ürün verisi
using System;
using UnityEngine;

namespace Olympos.UI
{
    /// <summary>
    /// Dükkân ızgarasındaki bir ürün. Alanlar oyundaki ipucu kutusunun satırlarıyla birebir:
    /// ad · kalite satırı · Buy Price · stat satırları · açıklama.
    /// </summary>
    [Serializable]
    public struct OlymposShopItem
    {
        public Sprite icon;
        public string name;

        [Tooltip("İpucunun ikinci satırı: \"Regular Item\", \"Item Grade: Low Class\" vb.")]
        public string gradeLine;

        [Tooltip("İpucunda kırmızı yazılan satır. 0 ise Buy Price satırı gizlenir.")]
        public long buyPrice;

        [Tooltip("Satın alınınca oyuncudan düşecek miktar; 0 ise buyPrice kullanılır.")]
        public long sellPrice;

        [Tooltip("\"Strength Bonus : 2\", \"Attack Power : 14\", \"Required Strength : 46\" gibi satırlar.")]
        public string[] statLines;

        [TextArea(2, 5)]
        public string description;

        [Tooltip("Tek bir slotta yığılabilen adet. 1 ise satışta adet diyaloğu açılmaz.")]
        public int stackSize;

        public bool Bos { get { return string.IsNullOrEmpty(name) && icon == null; } }
    }
}

// OLYMPOS-KO · 1298 gorev verisi (QuestList + gorev detayi icin). Inspector'dan ya da koddan doldurulur.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace Olympos.UI
{
    [Serializable]
    public class OlymposGorevHedefi
    {
        public Sprite ikon;
        [Tooltip("Ust satir, orn. \"Hunt: Shilan\"")] public string baslik = "Hunt: Shilan";
        [Tooltip("Alt satir, orn. \"Shilan öldür.\"")] public string aciklama = "Shilan öldür.";
        [Tooltip("Ikonun sag altindaki sayi (orn. 25). 0 = gizli.")] public int sayi = 25;
    }

    [Serializable]
    public class OlymposGorevOdulu
    {
        public Sprite ikon;
        public string ad = "Rapt Bow(+2)";
    }

    [Serializable]
    public class OlymposGorev
    {
        public string ad = "Starter Weapon&Armor";
        [Tooltip("Detaydaki turuncu aciklama, orn. \"Kill: 20x Orc Watcher\"")] public string aciklama = "Kill: 20x Orc Watcher";
        public List<OlymposGorevHedefi> hedefler = new List<OlymposGorevHedefi>();
        [Tooltip("En cok 8 (2 sutun x 4 satir)")] public List<OlymposGorevOdulu> oduller = new List<OlymposGorevOdulu>();
        public bool kabulEdildi;
    }
}

// OLYMPOS-KO · 1298 Character penceresi (Char Info sekmesi)
// Bu bileşen, editör menüsünden oluşturulan prefab üzerinde bulunur.
// Değerleri koddan doldurmak için SetData(...) kullanın.
using System;
using System.Text;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Olympos.UI
{
    [Serializable]
    public struct OlymposCharacterData
    {
        public string name;
        public string race;
        public int level;
        public string job;
        public long hp, maxHp;
        public long mp, maxMp;
        public long exp, maxExp;
        public long np, maxNp;
        public int attack, defence;
        public int statPoints;
        public int str, dex, intel, hpStat, mpStat;
        public int flameResist, poisonResist, glacierResist, lightningResist;
    }

    [DisallowMultipleComponent]
    public class OlymposCharacterWindow : MonoBehaviour
    {
        [Header("Zemin")]
        [Tooltip("Pencerenin siyah zemini. Saydamlık backgroundAlpha ile ayarlanır.")]
        public Image background;
        [Range(0f, 1f)]
        [Tooltip("1 = tamamen siyah, 0 = tamamen saydam. Varsayılan 0.85: oyun dünyası arkadan hafifçe görünür.")]
        public float backgroundAlpha = 0.85f;

        [Header("Sekmeler")]
        public Button tabCharInfo;
        public Button tabQuests;
        public Button tabClan;
        public Button tabFriends;

        [Header("Kimlik")]
        public Image raceIcon;
        public Text raceText;
        public Text nameText;

        [Header("Temel")]
        public Text levelText;
        public Text jobText;
        public Text hpText;
        public Text mpText;
        public Text expText;
        public Text npText;
        public Text attackText;
        public Text defenceText;

        [Header("Statlar")]
        public Text statPointsText;
        public Text strText;
        public Text dexText;
        public Text intText;
        public Text hpStatText;
        public Text mpStatText;

        [Header("Dirençler")]
        public Text flameText;
        public Text poisonText;
        public Text glacierText;
        public Text lightningText;

        [Header("Butonlar")]
        public Button statPresetButton;
        public Button statResetButton;

        [Serializable] public class TabEvent : UnityEvent<int> { }
        /// <summary>0 = Char Info, 1 = Quests, 2 = Clan, 3 = Friends</summary>
        public TabEvent onTabSelected = new TabEvent();

        void OnValidate()
        {
            ApplyBackgroundAlpha();
        }

        public void ApplyBackgroundAlpha()
        {
            if (background == null) return;
            var c = background.color;
            c.r = 0f; c.g = 0f; c.b = 0f;
            c.a = backgroundAlpha;
            background.color = c;
        }

        void Awake()
        {
            ApplyBackgroundAlpha();
            Hook(tabCharInfo, 0);
            Hook(tabQuests, 1);
            Hook(tabClan, 2);
            Hook(tabFriends, 3);
        }

        void Hook(Button b, int index)
        {
            if (b != null) b.onClick.AddListener(() => onTabSelected.Invoke(index));
        }

        public void SetData(OlymposCharacterData d)
        {
            Set(nameText, d.name);
            Set(raceText, string.IsNullOrEmpty(d.race) ? null : d.race.ToUpperInvariant());
            Set(levelText, d.level.ToString());
            Set(jobText, d.job);
            Set(hpText, Num(d.hp) + " / " + Num(d.maxHp));
            Set(mpText, Num(d.mp) + " / " + Num(d.maxMp));
            Set(expText, Num(d.exp) + " / " + Num(d.maxExp));
            Set(npText, Num(d.np) + " / " + Num(d.maxNp));
            Set(attackText, d.attack.ToString());
            Set(defenceText, d.defence.ToString());
            Set(statPointsText, d.statPoints.ToString());
            Set(strText, d.str.ToString());
            Set(dexText, d.dex.ToString());
            Set(intText, d.intel.ToString());
            Set(hpStatText, d.hpStat.ToString());
            Set(mpStatText, d.mpStat.ToString());
            Set(flameText, d.flameResist.ToString());
            Set(poisonText, d.poisonResist.ToString());
            Set(glacierText, d.glacierResist.ToString());
            Set(lightningText, d.lightningResist.ToString());
        }

        static void Set(Text t, string v)
        {
            if (t != null && v != null) t.text = v;
        }

        /// <summary>1673 -> "1.673" (1298 istemcisindeki gibi nokta ile ayırır).</summary>
        public static string Num(long value)
        {
            bool neg = value < 0;
            string s = (neg ? -value : value).ToString();
            var sb = new StringBuilder();
            int first = s.Length % 3;
            if (first == 0) first = 3;
            sb.Append(s, 0, first);
            for (int i = first; i < s.Length; i += 3)
            {
                sb.Append('.');
                sb.Append(s, i, 3);
            }
            return neg ? "-" + sb : sb.ToString();
        }
    }
}

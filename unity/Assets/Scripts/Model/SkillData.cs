using System;
using System.Collections.Generic;
using UnityEngine;

namespace Koray.Model
{
    /// <summary>
    /// Bir becerinin tek bir etkisi.
    ///
    /// NEDEN DUZ SEMA (butun alanlar her kayitta var)
    ///   Unity'nin JsonUtility'si polimorfik tip okuyamaz: "kind" alanina
    ///   bakip farkli sinifa deserialize etme yetenegi yok. Alternatif
    ///   Newtonsoft.Json ile ozel converter yazmakti, ama bu ek paket
    ///   bagimliligi demek.
    ///
    ///   Cozum: butun etki alanlari tek sinifta, kullanilmayanlar 0 / "".
    ///   `kind` hangi alanlarin anlamli oldugunu soyler. Birkac yuz bayt
    ///   israf eder, karsiliginda sifir bagimlilik ve hizli okuma verir.
    ///
    /// kind degerleri:
    ///   damage, damage_over_time, heal, buff, debuff, control,
    ///   threat, movement, stealth, cleanse, revive
    ///
    /// ONEMLI: Buraya alan eklersen tools/generate_content.py icindeki
    /// UNITY_EFFECT_FIELDS sozlugune de ekle. Ureteç, semada tanimsiz bir
    /// alan gorurse hata verir -- sessizce yutmaz.
    /// </summary>
    [Serializable]
    public class SkillEffectData
    {
        public string kind = "";
        public string school = "";          // physical, magic, poison, ...
        public string attribute = "";       // armor, all_stats, ...
        public string effectName = "";      // root, dash, ...

        public int    baseValue;            // hasar / sifa taban degeri
        public int    tickDamage;           // sureli hasarda tik basina
        public float  weaponScale;          // silah hasarina carpan
        public int    magnitudePct;         // buff/debuff yuzdesi (negatif olabilir)
        public int    durationMs;
        public int    tickIntervalMs;
        public float  distanceM;            // hareket becerilerinde mesafe
        public float  multiplier;           // tehdit carpani
        public int    maxEffects;           // arindirmada kac etki temizlenir
        public int    hpPct;                // diriltmede HP yuzdesi
        public int    mpPct;
        public int    bonusBelowHpPct;      // infaz: hedef bu HP altindaysa
        public float  bonusMultiplier;      // ... hasar bu kadar katlanir

        public bool IsDamage
        {
            get { return kind == "damage" || kind == "damage_over_time"; }
        }

        public bool IsHeal { get { return kind == "heal"; } }

        /// <summary>Arayuzde gosterilecek kisa ozet.</summary>
        public string Describe()
        {
            switch (kind)
            {
                case "damage":
                    return string.Format("{0} hasar (silah x{1:0.##})", baseValue, weaponScale);
                case "damage_over_time":
                    return string.Format("{0} sn boyunca {1} hasar/{2:0.#} sn",
                        durationMs / 1000, tickDamage, tickIntervalMs / 1000f);
                case "heal":
                    return string.Format("{0} iyilestirme", baseValue);
                case "buff":
                    return string.Format("{0} +%{1}, {2} sn", attribute, magnitudePct, durationMs / 1000);
                case "debuff":
                    return string.Format("{0} %{1}, {2} sn", attribute, magnitudePct, durationMs / 1000);
                case "control":
                    return string.Format("{0}, {1:0.#} sn", effectName, durationMs / 1000f);
                case "threat":
                    return string.Format("tehdit x{0:0.#}, {1} sn", multiplier, durationMs / 1000);
                case "movement":
                    return string.Format("{0}, {1:0.#} m", effectName, distanceM);
                case "stealth":
                    return string.Format("gizlenme, {0} sn", durationMs / 1000);
                case "cleanse":
                    return string.Format("{0} etki temizle", maxEffects);
                case "revive":
                    return string.Format("dirilt (%{0} HP, %{1} MP)", hpPct, mpPct);
                default:
                    return kind;
            }
        }
    }

    /// <summary>
    /// Becerinin bir rank'i (kademesi). Sayilar rank'a gore degisir;
    /// isim, aciklama ve hedef tipi <see cref="SkillData"/> icinde tektir.
    /// </summary>
    [Serializable]
    public class SkillRankData
    {
        public int rank;
        public int reqLevel;
        public int mpCost;
        public int hpCost;
        public int castTimeMs;
        public int cooldownMs;
        public SkillEffectData[] effects = new SkillEffectData[0];

        public float CastTimeSeconds { get { return castTimeMs / 1000f; } }
        public float CooldownSeconds { get { return cooldownMs / 1000f; } }
    }

    /// <summary>Bir beceri tanimi ve butun rank'lari.</summary>
    [Serializable]
    public class SkillData
    {
        public int    id;
        public string code = "";
        public string displayName = "";
        public string description = "";
        public string className = "";       // warrior, rogue, mage, priest
        public string targetType = "";      // self, single_enemy, area_enemy, ...
        public int    reqLevel;

        /// <summary>Onkosul beceri id'si. 0 = onkosul yok (JsonUtility null tasimaz).</summary>
        public int    reqSkillId;

        public float  rangeM;
        public float  areaRadiusM;

        public SkillRankData[] ranks = new SkillRankData[0];

        public bool HasPrerequisite { get { return reqSkillId != 0; } }
        public bool IsAreaOfEffect  { get { return areaRadiusM > 0f; } }

        /// <summary>Verilen rank'i dondurur; yoksa null.</summary>
        public SkillRankData GetRank(int rank)
        {
            for (int i = 0; i < ranks.Length; i++)
            {
                if (ranks[i].rank == rank)
                    return ranks[i];
            }
            return null;
        }

        /// <summary>Karakterin seviyesiyle ogrenebilecegi en yuksek rank.</summary>
        public SkillRankData GetHighestRankForLevel(int characterLevel)
        {
            SkillRankData best = null;
            for (int i = 0; i < ranks.Length; i++)
            {
                if (ranks[i].reqLevel <= characterLevel &&
                    (best == null || ranks[i].rank > best.rank))
                {
                    best = ranks[i];
                }
            }
            return best;
        }
    }

    /// <summary>
    /// skills.json'un kok nesnesi.
    /// JsonUtility ust seviyede dizi okuyamaz, bu yuzden sarmalayici gerekir.
    /// </summary>
    [Serializable]
    public class SkillCatalogJson
    {
        public int    schemaVersion;
        public string generatedBy = "";
        public int    skillCount;
        public int    rankCount;
        public SkillData[] skills = new SkillData[0];
    }
}

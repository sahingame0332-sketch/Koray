// =============================================================================
//  Skill verisi dogrulama kosumu
// =============================================================================
//  unity/Assets/Resources/GameData/skills.json dosyasini GERCEK C# siniflarina
//  yukler ve ice bakar. Bu deliverable'in en buyuk riski alan adi / tip
//  uyusmazligiydi: JSON'da "baseValue" yazarken C#'ta "base_value" olsa
//  Unity sessizce 0 okur ve butun hasar degerleri sifir olur. Bu kosum tam
//  olarak onu yakalar.
// =============================================================================

using System;
using System.Collections.Generic;
using System.IO;
using Koray.Model;
using UnityEngine;

public static class SkillChecks
{
    private const string JsonPath = "unity/Assets/Resources/GameData/skills.json";

    public static bool Run()
    {
        Console.WriteLine("SKILL VERISI DOGRULAMASI");
        Console.WriteLine(new string('=', 66));
        Console.WriteLine();

        if (!File.Exists(JsonPath))
        {
            Console.WriteLine("SORUN: " + JsonPath + " yok.");
            Console.WriteLine("Uret: python3 tools/generate_content.py");
            return false;
        }

        string json = File.ReadAllText(JsonPath);

        // Resources.Load yolunu da test et (oyunun gercekte kullandigi yol)
        Resources.Registry[SkillDatabase.ResourcePath] = new TextAsset(json);

        bool allOk = true;

        // --- 1. Yukleme ---
        bool loaded = SkillDatabase.Load(force: true);
        Report("Resources'tan yukleme", loaded);
        allOk &= loaded;
        if (!loaded)
            return false;

        Console.WriteLine(string.Format("  sema surumu {0}, {1} beceri yuklendi",
            SkillDatabase.SchemaVersion, SkillDatabase.Count));
        Console.WriteLine();

        // --- 2. Alan baglama gercekten oldu mu? ---
        // En sinsi hata: JSON yuklenir ama alan adlari uyusmadigi icin
        // her sey 0 / "" kalir. Onu yakalamak icin somut deger kontrolu.
        Console.WriteLine("Alan baglama kontrolu:");
        SkillData sample = SkillDatabase.GetByCode("warrior_sert_vurus");
        bool found = sample != null;
        Report("  kod ile bulma (warrior_sert_vurus)", found);
        allOk &= found;

        if (found)
        {
            allOk &= Report("  displayName dolu", !string.IsNullOrEmpty(sample.displayName),
                            sample.displayName);
            allOk &= Report("  className dolu", sample.className == "warrior",
                            sample.className);
            allOk &= Report("  targetType dolu", !string.IsNullOrEmpty(sample.targetType),
                            sample.targetType);
            allOk &= Report("  reqLevel > 0", sample.reqLevel > 0,
                            sample.reqLevel.ToString());
            allOk &= Report("  rangeM > 0", sample.rangeM > 0f,
                            sample.rangeM.ToString("0.##"));
            allOk &= Report("  rank sayisi 5", sample.ranks.Length == 5,
                            sample.ranks.Length.ToString());

            if (sample.ranks.Length > 0)
            {
                SkillRankData r1 = sample.ranks[0];
                allOk &= Report("  rank1 mpCost > 0", r1.mpCost > 0, r1.mpCost.ToString());
                allOk &= Report("  rank1 cooldownMs > 0", r1.cooldownMs > 0,
                                r1.cooldownMs.ToString());
                allOk &= Report("  rank1 etki sayisi > 0", r1.effects.Length > 0,
                                r1.effects.Length.ToString());

                if (r1.effects.Length > 0)
                {
                    SkillEffectData e = r1.effects[0];
                    allOk &= Report("  etki kind dolu", e.kind == "damage", e.kind);
                    allOk &= Report("  etki baseValue > 0", e.baseValue > 0,
                                    e.baseValue.ToString());
                    allOk &= Report("  etki weaponScale > 0", e.weaponScale > 0f,
                                    e.weaponScale.ToString("0.###"));
                    allOk &= Report("  etki school dolu", e.school == "physical", e.school);
                }
            }
        }
        Console.WriteLine();

        // --- 3. Rank olceklemesi artan mi? ---
        Console.WriteLine("Rank olceklemesi (warrior_sert_vurus):");
        if (found)
        {
            Console.WriteLine("  rank  seviye   MP  bekleme  hasar  silah x");
            int prevDamage = 0;
            bool rising = true;
            foreach (SkillRankData r in sample.ranks)
            {
                int dmg = r.effects.Length > 0 ? r.effects[0].baseValue : 0;
                float ws = r.effects.Length > 0 ? r.effects[0].weaponScale : 0f;
                Console.WriteLine(string.Format(
                    "  {0,4}  {1,6}  {2,3}  {3,6:F2}s  {4,5}  {5,6:F3}",
                    r.rank, r.reqLevel, r.mpCost, r.CooldownSeconds, dmg, ws));
                if (dmg <= prevDamage)
                    rising = false;
                prevDamage = dmg;
            }
            allOk &= Report("  hasar rank ile artiyor", rising);
        }
        Console.WriteLine();

        // --- 4. Butun etki tipleri okunabiliyor mu? ---
        Console.WriteLine("Etki tipleri (Describe() ile):");
        var seen = new Dictionary<string, string>();
        foreach (SkillData s in SkillDatabase.All)
        {
            foreach (SkillRankData r in s.ranks)
            {
                foreach (SkillEffectData e in r.effects)
                {
                    if (!seen.ContainsKey(e.kind))
                        seen[e.kind] = s.displayName + ": " + e.Describe();
                }
            }
        }
        var kinds = new List<string>(seen.Keys);
        kinds.Sort();
        foreach (string k in kinds)
            Console.WriteLine(string.Format("  {0,-18} {1}", k, seen[k]));

        // Ureteç 11 etki tipi uretiyor
        allOk &= Report("11 etki tipi de mevcut", kinds.Count == 11,
                        kinds.Count.ToString());
        Console.WriteLine();

        // --- 5. Sinif dagilimi ---
        Console.WriteLine("Sinif dagilimi:");
        foreach (string cls in new[] { "warrior", "rogue", "mage", "priest" })
        {
            var list = SkillDatabase.GetForClass(cls);
            bool ok = list.Count == 10;
            Console.WriteLine(string.Format("  {0,-9} {1,2} beceri   {2}",
                cls, list.Count, ok ? "ok" : "SORUN"));
            allOk &= ok;

            // Seviye sirasinda mi?
            for (int i = 1; i < list.Count; i++)
            {
                if (list[i].reqLevel < list[i - 1].reqLevel)
                {
                    Console.WriteLine("    SORUN: seviye sirasi bozuk");
                    allOk = false;
                    break;
                }
            }
        }
        Console.WriteLine();

        // --- 6. Beceri agaci dogrulamasi ---
        List<string> problems = SkillDatabase.Validate();
        Report("Beceri agaci dogrulamasi (onkosul, dongu, rank sirasi)",
               problems.Count == 0,
               problems.Count == 0 ? "sorun yok" : problems.Count + " sorun");
        foreach (string p in problems)
            Console.WriteLine("    " + p);
        allOk &= problems.Count == 0;

        // --- 7. Seviyeye gore rank secimi ---
        Console.WriteLine();
        Console.WriteLine("GetHighestRankForLevel (warrior_sert_vurus):");
        if (found)
        {
            foreach (int lvl in new[] { 1, 2, 25, 50, 75, 100 })
            {
                SkillRankData r = sample.GetHighestRankForLevel(lvl);
                Console.WriteLine(string.Format("  seviye {0,3} -> {1}",
                    lvl, r == null ? "ogrenilemez" : "rank " + r.rank));
            }
            // Seviye 1'de ogrenilemez olmali (ilk rank seviye 2)
            allOk &= Report("  seviye 1'de ogrenilemez",
                            sample.GetHighestRankForLevel(1) == null);
            allOk &= Report("  seviye 100'de en yuksek rank",
                            sample.GetHighestRankForLevel(100) != null &&
                            sample.GetHighestRankForLevel(100).rank == 5);
        }

        return allOk;
    }

    private static bool Report(string label, bool ok, string detail = null)
    {
        Console.WriteLine(string.Format("{0,-46} {1}{2}",
            label, ok ? "ok" : "SORUN",
            string.IsNullOrEmpty(detail) ? "" : "   (" + detail + ")"));
        return ok;
    }
}

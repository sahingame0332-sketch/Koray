using System.Collections.Generic;
using UnityEngine;

namespace Koray.Model
{
    /// <summary>
    /// Calisma zamani beceri veritabani.
    ///
    /// KULLANIM
    ///   SkillDatabase.Load();                       // bir kez, oyun acilirken
    ///   SkillData s = SkillDatabase.GetByCode("warrior_sert_vurus");
    ///   foreach (var s in SkillDatabase.GetForClass("mage")) { ... }
    ///
    /// Veri `Resources/GameData/skills.json` dosyasindan okunur -- yani hicbir
    /// editor adimi gerekmez, Play'e basinca calisir. ScriptableObject asset'i
    /// isteyen (VFX/ikon baglamak icin) SkillImporter'i kullanir; o yol
    /// opsiyoneldir.
    ///
    /// NEDEN SUNUCU DEGIL ISTEMCI VERISI
    ///   Bu veri istemcide arayuz, onizleme, ikon ve VFX secimi icindir.
    ///   Hasarin GERCEK hesabi sunucuda yapilir (docs/01 Bolum 6.2). Istemci
    ///   "bu beceri 214 hasar verir" diye gosterir; sunucu ne verdigini
    ///   kendisi belirler. Ikisi ayrilirsa gosterilen sayi yanlis olur ama
    ///   oyun hilelenemez -- dogru odunlesme budur.
    /// </summary>
    public static class SkillDatabase
    {
        public const string ResourcePath = "GameData/skills";   // .json uzantisiz

        private static readonly Dictionary<int, SkillData> _byId =
            new Dictionary<int, SkillData>();
        private static readonly Dictionary<string, SkillData> _byCode =
            new Dictionary<string, SkillData>();
        private static readonly Dictionary<string, List<SkillData>> _byClass =
            new Dictionary<string, List<SkillData>>();

        private static SkillData[] _all = new SkillData[0];

        public static bool IsLoaded { get; private set; }
        public static int SchemaVersion { get; private set; }
        public static int Count { get { return _all.Length; } }
        public static SkillData[] All { get { return _all; } }

        /// <summary>
        /// Resources altindaki skills.json'u yukler. Tekrar cagrilmasi zararsiz.
        /// </summary>
        /// <returns>Yukleme basarili mi</returns>
        public static bool Load(bool force = false)
        {
            if (IsLoaded && !force)
                return true;

            TextAsset asset = Resources.Load<TextAsset>(ResourcePath);
            if (asset == null)
            {
                Debug.LogError(
                    "SkillDatabase: Resources/" + ResourcePath + ".json bulunamadi. " +
                    "Uret: python3 tools/generate_content.py");
                return false;
            }

            return LoadFromJson(asset.text);
        }

        /// <summary>
        /// Hazir JSON metninden yukler. Test ve sunucudan indirilen guncelleme
        /// icin ayri tutuldu.
        /// </summary>
        public static bool LoadFromJson(string json)
        {
            if (string.IsNullOrEmpty(json))
            {
                Debug.LogError("SkillDatabase: bos JSON");
                return false;
            }

            SkillCatalogJson catalog = JsonUtility.FromJson<SkillCatalogJson>(json);
            if (catalog == null || catalog.skills == null)
            {
                Debug.LogError("SkillDatabase: JSON ayristirilamadi");
                return false;
            }

            _byId.Clear();
            _byCode.Clear();
            _byClass.Clear();

            foreach (SkillData skill in catalog.skills)
            {
                if (skill == null)
                    continue;

                if (_byId.ContainsKey(skill.id))
                {
                    Debug.LogWarning("SkillDatabase: tekrarlanan id " + skill.id +
                                     " (" + skill.code + ") -- atlandi");
                    continue;
                }

                _byId[skill.id] = skill;

                if (!string.IsNullOrEmpty(skill.code))
                    _byCode[skill.code] = skill;

                List<SkillData> list;
                if (!_byClass.TryGetValue(skill.className, out list))
                {
                    list = new List<SkillData>();
                    _byClass[skill.className] = list;
                }
                list.Add(skill);
            }

            // Sinif listelerini seviyeye gore sirala -- arayuz boylece
            // ogrenme sirasini gosterebilir
            foreach (KeyValuePair<string, List<SkillData>> kv in _byClass)
                kv.Value.Sort((a, b) => a.reqLevel.CompareTo(b.reqLevel));

            _all = catalog.skills;
            SchemaVersion = catalog.schemaVersion;
            IsLoaded = true;
            return true;
        }

        public static SkillData GetById(int id)
        {
            SkillData s;
            return _byId.TryGetValue(id, out s) ? s : null;
        }

        public static SkillData GetByCode(string code)
        {
            if (string.IsNullOrEmpty(code))
                return null;

            SkillData s;
            return _byCode.TryGetValue(code, out s) ? s : null;
        }

        /// <summary>Bir sinifin becerileri, seviye sirasinda.</summary>
        public static IReadOnlyList<SkillData> GetForClass(string className)
        {
            List<SkillData> list;
            return _byClass.TryGetValue(className, out list)
                ? (IReadOnlyList<SkillData>)list
                : new List<SkillData>();
        }

        /// <summary>
        /// Beceri agacini dogrular: onkosul zincirleri mevcut mu, dongu var mi.
        /// Veri uretecinin hatasini yakalamak icin acilista bir kez cagir.
        /// </summary>
        public static List<string> Validate()
        {
            List<string> problems = new List<string>();

            foreach (SkillData skill in _all)
            {
                if (skill.ranks == null || skill.ranks.Length == 0)
                    problems.Add(skill.code + ": rank tanimi yok");

                if (skill.HasPrerequisite && GetById(skill.reqSkillId) == null)
                {
                    problems.Add(skill.code + ": onkosul beceri " +
                                 skill.reqSkillId + " bulunamadi");
                }

                // Onkosul zincirinde dongu var mi?
                int guard = 0;
                SkillData cursor = skill;
                while (cursor != null && cursor.HasPrerequisite)
                {
                    cursor = GetById(cursor.reqSkillId);
                    if (++guard > 64)
                    {
                        problems.Add(skill.code + ": onkosul zincirinde dongu");
                        break;
                    }
                }

                if (skill.ranks != null)
                {
                    for (int i = 1; i < skill.ranks.Length; i++)
                    {
                        if (skill.ranks[i].reqLevel < skill.ranks[i - 1].reqLevel)
                        {
                            problems.Add(skill.code + ": rank " + skill.ranks[i].rank +
                                         " seviye sarti onceki rank'tan dusuk");
                        }
                    }
                }
            }

            return problems;
        }
    }
}

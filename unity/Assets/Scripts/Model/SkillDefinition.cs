using UnityEngine;

namespace Koray.Model
{
    /// <summary>
    /// Becerinin Unity asset hali -- OPSIYONEL yol.
    ///
    /// SkillDatabase zaten JSON'dan okuyor ve oyun bunsuz calisir. Bu
    /// ScriptableObject'e sadece beceriye UNITY VARLIGI baglamak gerektiginde
    /// ihtiyac duyarsin: ikon, ses, VFX prefab'i, animasyon klibi. Bunlar
    /// JSON'da tutulamaz cunku Unity referansi gerektirir.
    ///
    /// Uretimi: Tools > Koray > Skill Asset'lerini Uret
    /// (Editor/SkillImporter.cs)
    ///
    /// Is akisi:
    ///   skills.json  --(importer)-->  SkillDefinition asset'leri
    ///                                  ^ sayilar her uretimde guncellenir
    ///                                  ^ ikon/VFX alanlari KORUNUR
    /// </summary>
    [CreateAssetMenu(fileName = "Skill", menuName = "Koray/Skill Definition")]
    public class SkillDefinition : ScriptableObject
    {
        [Header("Veri (skills.json'dan uretilir -- elle duzenlemeyin)")]
        [SerializeField] private SkillData _data = new SkillData();

        [Header("Unity varliklari (elle baglanir, uretimde KORUNUR)")]
        public Sprite Icon;
        public GameObject CastVfx;
        public GameObject ImpactVfx;
        public AudioClip CastSound;
        public string AnimationStateName = "";

        public SkillData Data { get { return _data; } }

        public int Id { get { return _data.id; } }
        public string Code { get { return _data.code; } }
        public string DisplayName { get { return _data.displayName; } }

        /// <summary>Importer tarafindan cagrilir. Varlik alanlarina dokunmaz.</summary>
        public void ApplyData(SkillData data)
        {
            _data = data;
        }
    }
}

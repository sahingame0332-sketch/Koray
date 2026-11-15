// OLYMPOS-KO · kendi skill efektleri kutuphanesi: skill adina gore efekti karakterin ayaginda oynatir.
// Kayittaki akis: cast suresi olan skill'lerde (Cat's/Lupine Eyes, Cure) once "dokum yildizlari", sonra skill efekti.
// Kullanim: kutuphane.Uygula("Cure Disease", karakter.transform, dokumluMu: true);
using System.Collections.Generic;
using UnityEngine;

namespace Olympos.KendiSkill
{
    [AddComponentMenu("OLYMPOS/1298/Kendi Skill/Kendi Skill Kutuphanesi")]
    public class OlymposKendiSkillKutuphanesi : MonoBehaviour
    {
        [System.Serializable]
        public class Kayit { public string skill; public OlymposKendiSkillEfekti efekt; }

        public OlymposKendiSkillEfekti dokumYildizlari;
        public List<Kayit> skiller = new List<Kayit>();

        public OlymposKendiSkillEfekti Bul(string skill)
        {
            foreach (var k in skiller) if (k != null && k.efekt != null && string.Equals(k.skill, skill, System.StringComparison.OrdinalIgnoreCase)) return k.efekt;
            return null;
        }

        /// <summary>Skill efektini oynatir. dokumlu: once dokum yildizlari (kayitta ~1.4 sn), bitince skill efekti.</summary>
        public void Uygula(string skill, Transform karakter, bool dokumlu)
        {
            var e = Bul(skill); if (e == null) { Debug.LogWarning("[OLYMPOS] Efekt yok: " + skill); return; }
            if (dokumlu && dokumYildizlari != null)
            {
                dokumYildizlari.onBitti.RemoveAllListeners();
                dokumYildizlari.onBitti.AddListener(() => e.Oyna(karakter));
                dokumYildizlari.Oyna(karakter);
            }
            else e.Oyna(karakter);
        }
    }
}

// OLYMPOS-KO · yakin dovus skill efektleri kutuphanesi: skill adina gore (Information panelindeki "Using - <ad>") efekti oynatir.
// Kullanim: kutuphane.Uygula("Stab", karakter.transform, hedef.transform);
using System.Collections.Generic;
using UnityEngine;

namespace Olympos.YakinSkill
{
    [AddComponentMenu("OLYMPOS/1298/Yakin Skill/Yakin Skill Kutuphanesi")]
    public class OlymposYakinSkillKutuphanesi : MonoBehaviour
    {
        public List<OlymposYakinSkillEfekti> efektler = new List<OlymposYakinSkillEfekti>();

        public OlymposYakinSkillEfekti Bul(string skill)
        {
            foreach (var e in efektler) if (e != null && string.Equals(e.skillAdi, skill, System.StringComparison.OrdinalIgnoreCase)) return e;
            return null;
        }

        public void Uygula(string skill, Transform karakter, Transform hedef)
        {
            var e = Bul(skill); if (e == null) { Debug.LogWarning("[OLYMPOS] Yakin skill efekti yok: " + skill); return; }
            e.Oyna(karakter, hedef);
        }
    }
}

// OLYMPOS-KO · efekt 7 kutuphanesi: skill adina gore oynatir. Varsayilan adlar "kesik_aura", "yildiz"
// (videoda skill adlari gorunmuyordu; Inspector'dan oyundaki skill adlarini yazin).
using System.Collections.Generic;
using UnityEngine;

namespace Olympos.Efekt7Skill
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 7 Skill/Kutuphane")]
    public class OlymposEfekt7SkillKutuphanesi : MonoBehaviour
    {
        public List<OlymposEfekt7Skill> efektler = new List<OlymposEfekt7Skill>();

        public OlymposEfekt7Skill Bul(string skill)
        {
            foreach (var e in efektler) if (e != null && string.Equals(e.skillAdi, skill, System.StringComparison.OrdinalIgnoreCase)) return e;
            return null;
        }

        public void Uygula(string skill, Transform hedef)
        {
            var e = Bul(skill); if (e == null) { Debug.LogWarning("[OLYMPOS] Efekt 7 skill yok: " + skill); return; }
            e.Oyna(hedef);
        }
    }
}

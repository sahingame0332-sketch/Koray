// OLYMPOS-KO · efekt 7 kutuphanesi: skill adina gore oynatir. Varsayilan adlar "kesik_aura", "yildiz"
// (videoda skill adlari gorunmuyordu; Inspector'dan oyundaki skill adlarini yazin).
using System.Collections.Generic;
using UnityEngine;

namespace Olympos.Efekt7
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 7/Efekt 7 Kutuphanesi")]
    public class OlymposEfekt7Kutuphanesi : MonoBehaviour
    {
        public List<OlymposEfekt7> efektler = new List<OlymposEfekt7>();

        public OlymposEfekt7 Bul(string skill)
        {
            foreach (var e in efektler) if (e != null && string.Equals(e.skillAdi, skill, System.StringComparison.OrdinalIgnoreCase)) return e;
            return null;
        }

        public void Uygula(string skill, Transform hedef)
        {
            var e = Bul(skill); if (e == null) { Debug.LogWarning("[OLYMPOS] Efekt 7 yok: " + skill); return; }
            e.Oyna(hedef);
        }
    }
}

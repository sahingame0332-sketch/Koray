// OLYMPOS-KO · efekt 7 kutuphanesi: skill adina gore oynatir. Varsayilan adlar "kesik_aura", "yildiz"
// (videoda skill adlari gorunmuyordu; Inspector'dan oyundaki skill adlarini yazin).
using System.Collections.Generic;
using UnityEngine;

namespace Olympos.Efekt7Hasar
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 7 Hasar/Kutuphane")]
    public class OlymposEfekt7HasarKutuphanesi : MonoBehaviour
    {
        public List<OlymposEfekt7Hasar> efektler = new List<OlymposEfekt7Hasar>();

        public OlymposEfekt7Hasar Bul(string skill)
        {
            foreach (var e in efektler) if (e != null && string.Equals(e.skillAdi, skill, System.StringComparison.OrdinalIgnoreCase)) return e;
            return null;
        }

        public void Uygula(string skill, Transform hedef)
        {
            var e = Bul(skill); if (e == null) { Debug.LogWarning("[OLYMPOS] efekt 7 hasar yok: " + skill); return; }
            e.Oyna(hedef);
        }
    }
}

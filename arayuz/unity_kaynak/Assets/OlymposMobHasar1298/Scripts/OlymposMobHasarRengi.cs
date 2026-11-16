// OLYMPOS-KO · 1298 mob hasar rengi — vurulan mob kisa sure kirmiziya doner (isik degil, mobun rengi degisir).
// Olculen (kayit 14-01-51, 4 karede): tam gucte R = 0.60 L + 162, G = 0.95 L + 5, B = 0.75 L (L = zemin parlakligi).
// Mobun Renderer'larina sure boyunca "Olympos/Mob Hasar Kirmizi" malzemesi eklenir, guc egrisi kare kare (30 kare/sn) oynar, sonra kaldirilir.
// Kayittaki iki egri:
//   "kesik": 0.10 0.10 0.60 0.87 0.91 0.28 0.01            (kesik + aura skill'inin basinda, ~0.23 sn)
//   "yildiz": 0 0 0 0.34 0.59 0.95 0.54 0.01               (yildiz vurusunda, ~0.27 sn; ilk 3 kare bekleme)
// Kullanim: hasar.Oyna(mob.transform, "yildiz");  ya da hasar.Oyna(mob.transform, kendiEgrin);
using System.Collections.Generic;
using UnityEngine;

namespace Olympos.MobHasar
{
    [AddComponentMenu("OLYMPOS/1298/Mob Hasar/Mob Hasar Rengi")]
    public class OlymposMobHasarRengi : MonoBehaviour
    {
        public Material kirmiziMalzeme;
        public float fps = 30f;
        public float[] kesikEgrisi = { 0.097f, 0.097f, 0.599f, 0.866f, 0.91f, 0.279f, 0.007f };
        public float[] yildizEgrisi = { 0f, 0f, 0f, 0.336f, 0.586f, 0.946f, 0.538f, 0.01f };
        [Tooltip("Denemede surekli tekrar.")]
        public bool denemeDongusu = false;
        public Transform hedefDeneme;
        public string denemeEgrisi = "yildiz";

        readonly List<Renderer> takili = new List<Renderer>();
        Material kopya; float[] egri; float t; bool oynuyor;
        static readonly int GucId = Shader.PropertyToID("_Guc");

        void Start() { if (denemeDongusu && hedefDeneme != null) Oyna(hedefDeneme, denemeEgrisi); }

        public void Oyna(Transform hedef, string egriAdi) { Oyna(hedef, egriAdi == "kesik" ? kesikEgrisi : yildizEgrisi); }

        public void Oyna(Transform hedef, float[] guc)
        {
            Birak();
            if (hedef == null || kirmiziMalzeme == null || guc == null || guc.Length == 0) return;
            egri = guc; t = 0f; oynuyor = true;
            kopya = new Material(kirmiziMalzeme); kopya.SetFloat(GucId, egri[0]);
            foreach (var r in hedef.GetComponentsInChildren<Renderer>())
            {
                if (r is ParticleSystemRenderer) continue;
                var m = new List<Material>(r.sharedMaterials); m.Add(kopya); r.sharedMaterials = m.ToArray(); takili.Add(r);
            }
        }

        public void Birak()
        {
            foreach (var r in takili)
            {
                if (r == null) continue;
                var m = new List<Material>(r.sharedMaterials); m.Remove(kopya); r.sharedMaterials = m.ToArray();
            }
            takili.Clear(); oynuyor = false;
            if (kopya != null) { Destroy(kopya); kopya = null; }
        }

        void Update()
        {
            if (!oynuyor) return;
            t += Time.deltaTime; int k = Mathf.FloorToInt(t * fps);
            if (k >= egri.Length) { Birak(); if (denemeDongusu && hedefDeneme != null) Invoke("Tekrar", 0.8f); return; }
            kopya.SetFloat(GucId, egri[k]);
        }

        void Tekrar() { Oyna(hedefDeneme, denemeEgrisi); }
        void OnDisable() { Birak(); }
    }
}

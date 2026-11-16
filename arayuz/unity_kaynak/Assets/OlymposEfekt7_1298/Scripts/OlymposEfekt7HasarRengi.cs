// OLYMPOS-KO · efekt 7 hasar kirmizisi: mobun Renderer'larina sure boyunca ek malzeme (Olympos/Efekt7 Hasar Kirmizi) takar,
// guc egrisini (kare basina, 30 kare/sn, kayittan olculdu) oynatir, bitince malzemeyi kaldirir.
using System.Collections.Generic;
using UnityEngine;

namespace Olympos.Efekt7
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 7/Efekt 7 Hasar Rengi")]
    public class OlymposEfekt7HasarRengi : MonoBehaviour
    {
        public Material kirmiziMalzeme;
        public float fps = 30f;

        readonly List<Renderer> takili = new List<Renderer>();
        Material kopya; float[] egri; float t; bool oynuyor;
        static readonly int GucId = Shader.PropertyToID("_Guc");

        public void Oyna(Transform hedef, float[] guc)
        {
            Birak();
            if (hedef == null || kirmiziMalzeme == null || guc == null || guc.Length == 0) return;
            egri = guc; t = 0f; oynuyor = true;
            kopya = new Material(kirmiziMalzeme); kopya.SetFloat(GucId, egri[0]);
            foreach (var r in hedef.GetComponentsInChildren<Renderer>())
            {
                if (r is ParticleSystemRenderer || r.GetComponent<OlymposEfekt7Katman>() != null) continue;
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
            if (k >= egri.Length) { Birak(); return; }
            kopya.SetFloat(GucId, egri[k]);
        }

        void OnDisable() { Birak(); }
    }
}

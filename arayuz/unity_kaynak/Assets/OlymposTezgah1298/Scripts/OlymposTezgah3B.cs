// OLYMPOS-KO · 1298 yerdeki Merchant tezgahi — 3B (sandik + one egik teshir tahtasi), iki fotograftan dokulu.
// Olculer karakter boyuna gore (karakter 1.8 birim icin): genislik 0.78, derinlik 0.42, on yukseklik 0.59, arka yukseklik 0.99
//   (tahta ~44 derece one egik). Yuzler: UST (sancak + esyalar), ON (asili sancak), SOL/SAG yan (kirmizi perde; sag = ayna),
//   ARKA (fotograf yok -> yan doku). Pivot: taban merkezi; transform.forward = on yuz. Alt yuz yok (yerde durur).
// Mesh 5 alt-mesh (ust, on, sol, sag, arka) -> 3 malzeme (Ust, On, Yan). Kullanim: Kur(konum, onYonu); Kaldir().
using UnityEngine;

namespace Olympos.Tezgah
{
    [AddComponentMenu("OLYMPOS/1298/Merchant Tezgahi 3B")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposTezgah3B : MonoBehaviour
    {
        [Tooltip("Karakterinizin dunya birimindeki boyu.")]
        public float karakterBoyu = 1.8f;
        [Header("Olculer (karakter boyu 1.8 icin metre; karakterBoyu ile olceklenir)")]
        public float genislik = 0.78f;
        public float derinlik = 0.42f;
        public float onYukseklik = 0.59f;
        public float arkaYukseklik = 0.99f;

        void Awake() { Kur(); }
        void OnValidate() { if (GetComponent<MeshFilter>() != null) Kur(); }

        public void Kur()
        {
            float k = karakterBoyu / 1.8f, w = genislik * k * 0.5f, d = derinlik * k * 0.5f, hf = onYukseklik * k, hb = arkaYukseklik * k;
            var v = new System.Collections.Generic.List<Vector3>(); var uv = new System.Collections.Generic.List<Vector2>();
            var alt = new int[5][];
            // her yuz: sol-ust, sag-ust, sag-alt, sol-alt (doku yonunde), disa bakan sira
            Vector3[][] Y = {
                new[] { new Vector3(-w, hb, -d), new Vector3(w, hb, -d), new Vector3(w, hf, d), new Vector3(-w, hf, d) },   // ust (arka kenar dokunun ustu)
                new[] { new Vector3(-w, hf, d), new Vector3(w, hf, d), new Vector3(w, 0, d), new Vector3(-w, 0, d) },       // on
                new[] { new Vector3(-w, hb, -d), new Vector3(-w, hf, d), new Vector3(-w, 0, d), new Vector3(-w, 0, -d) },   // sol (arka solda, on sagda)
                new[] { new Vector3(w, hf, d), new Vector3(w, hb, -d), new Vector3(w, 0, -d), new Vector3(w, 0, d) },       // sag (ayna)
                new[] { new Vector3(w, hb, -d), new Vector3(-w, hb, -d), new Vector3(-w, 0, -d), new Vector3(w, 0, -d) } }; // arka
            for (int f = 0; f < 5; f++)
            {
                int b = v.Count; v.AddRange(Y[f]);
                bool ayna = f == 3;
                uv.Add(new Vector2(ayna ? 1 : 0, 1)); uv.Add(new Vector2(ayna ? 0 : 1, 1)); uv.Add(new Vector2(ayna ? 0 : 1, 0)); uv.Add(new Vector2(ayna ? 1 : 0, 0));
                alt[f] = new[] { b, b + 1, b + 2, b, b + 2, b + 3 };
            }
            var m = new Mesh(); m.name = "Tezgah3B";
            m.SetVertices(v); m.SetUVs(0, uv); m.subMeshCount = 5;
            for (int f = 0; f < 5; f++) m.SetTriangles(alt[f], f);
            m.RecalculateNormals(); m.RecalculateBounds();
            GetComponent<MeshFilter>().sharedMesh = m;
        }

        public void Kur(Vector3 konum, Vector3 onYonu)
        {
            transform.position = konum;
            onYonu.y = 0f; if (onYonu.sqrMagnitude > 1e-4f) transform.rotation = Quaternion.LookRotation(onYonu.normalized, Vector3.up);
            gameObject.SetActive(true);
        }
        public void Kaldir() { gameObject.SetActive(false); }
    }
}

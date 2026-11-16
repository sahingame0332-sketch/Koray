// OLYMPOS-KO · efekt 7 katmani — kare kare oynatici (dunya uzayi, kameraya donuk dortgen, eklemeli).
// Boyut hedef (mob) boyuna gore: genislik = hedefBoyu * genislikHedef; pivot = mobun zemin noktasinin kare icindeki yeri.
// derinlik: arka katman mobun arkasina (kameradan uzaga), on katman onune itilir -> mob arka katmani orter.
using UnityEngine;

namespace Olympos.Efekt7Hasar
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 7 Hasar/Katman")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposEfekt7HasarKatman : MonoBehaviour
    {
        public Texture2D[] kareler = new Texture2D[0];
        public float fps = 30f;
        [Header("Boyut (olculen)")]
        public float hedefBoyu = 1.8f;
        public float genislikHedef = 1f;
        public float enBoy = 1f;
        public Vector2 pivot = new Vector2(0.5f, 0f);
        [Tooltip("Kamera yonunde kaydirma (m): arka katman +, on katman -.")]
        public float derinlik = 0f;
        [Header("Gorunum")]
        public Color renk = Color.white;
        [Range(0f, 4f)] public float parlaklik = 1f;
        public Camera kamera;
        public Transform bagli;

        MeshRenderer mr; MaterialPropertyBlock mpb; float t; bool oynuyor;
        static readonly int TexId = Shader.PropertyToID("_MainTex");
        static readonly int RenkId = Shader.PropertyToID("_Renk");
        static readonly int ParlakId = Shader.PropertyToID("_Parlaklik");

        public float Sure { get { return kareler.Length / Mathf.Max(1f, fps); } }

        void Awake() { mr = GetComponent<MeshRenderer>(); mpb = new MaterialPropertyBlock(); MeshKur(); if (!oynuyor) mr.enabled = false; }
        void OnValidate() { if (!Application.isPlaying && GetComponent<MeshFilter>() != null) MeshKur(); }

        public void MeshKur()
        {
            float w = hedefBoyu * genislikHedef, h = w * enBoy, x0 = -pivot.x * w, y0 = -pivot.y * h;
            var m = new Mesh(); m.name = "Efekt7Dortgen";
            m.vertices = new[] { new Vector3(x0, y0, 0), new Vector3(x0 + w, y0, 0), new Vector3(x0, y0 + h, 0), new Vector3(x0 + w, y0 + h, 0) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds();
            GetComponent<MeshFilter>().sharedMesh = m;
        }

        public void Oyna(Transform nokta)
        {
            if (nokta != null) bagli = nokta;
            if (mr == null) mr = GetComponent<MeshRenderer>(); if (mpb == null) mpb = new MaterialPropertyBlock();
            t = 0f; oynuyor = true; mr.enabled = kareler.Length > 0; KareYaz(0); Konumla();
        }

        public void Durdur() { oynuyor = false; if (mr != null) mr.enabled = false; }

        void Update()
        {
            if (!oynuyor) return;
            t += Time.deltaTime;
            int k = Mathf.FloorToInt(t * fps);
            if (k >= kareler.Length) { Durdur(); return; }
            KareYaz(k);
        }

        void LateUpdate() { if (oynuyor) Konumla(); }

        void Konumla()
        {
            var k = kamera != null ? kamera : Camera.main;
            Vector3 p = bagli != null ? bagli.position : transform.position;
            if (k != null) { transform.rotation = k.transform.rotation; p += k.transform.forward * derinlik; }
            transform.position = p;
        }

        void KareYaz(int k)
        {
            if (mr == null || kareler.Length == 0) return;
            mr.GetPropertyBlock(mpb);
            if (kareler[k] != null) mpb.SetTexture(TexId, kareler[k]);
            mpb.SetColor(RenkId, renk); mpb.SetFloat(ParlakId, parlaklik);
            mr.SetPropertyBlock(mpb);
        }
    }
}

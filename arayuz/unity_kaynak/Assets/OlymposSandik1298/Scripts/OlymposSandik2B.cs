// OLYMPOS-KO · sandik 2B — kameraya donuk sprite (ekran goruntulerinden kesildi, yumusak kenarli alfa). 3B model yerine
// uzak/ucuz gosterim icin. Kapali: kilitli on yuz + kapak (gorunum 2), acik: altinlar + acik kapak (gorunum 1, ust kamera).
// Genislik karakter boyuna gore: kapali 0.33, acik 0.40 (3B modelin o kameradaki izdusumunden). Pivot: alt orta.
using UnityEngine;

namespace Olympos.Sandik
{
    [AddComponentMenu("OLYMPOS/1298/Sandik/Sandik 2B")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposSandik2B : MonoBehaviour
    {
        public Texture2D kapali, acik;
        public float karakterBoyu = 1.8f;
        public float kapaliGenislik = 0.33f, acikGenislik = 0.40f;
        public bool acikMi = false;
        public Camera kamera;
        MeshRenderer mr; MaterialPropertyBlock mpb;
        static readonly int TexId = Shader.PropertyToID("_MainTex");

        void Awake() { mr = GetComponent<MeshRenderer>(); mpb = new MaterialPropertyBlock(); Kur(); }
        void OnValidate() { if (GetComponent<MeshFilter>() != null) Kur(); }

        public void Ac() { acikMi = true; Kur(); }
        public void Kapat() { acikMi = false; Kur(); }

        void Kur()
        {
            var t = acikMi ? acik : kapali; if (t == null) return;
            float w = karakterBoyu * (acikMi ? acikGenislik : kapaliGenislik), h = w * t.height / Mathf.Max(1f, t.width), x0 = -w * 0.5f;
            var m = new Mesh(); m.name = "Sandik2B";
            m.vertices = new[] { new Vector3(x0, 0, 0), new Vector3(x0 + w, 0, 0), new Vector3(x0, h, 0), new Vector3(x0 + w, h, 0) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds(); GetComponent<MeshFilter>().sharedMesh = m;
            if (mr == null) mr = GetComponent<MeshRenderer>(); if (mpb == null) mpb = new MaterialPropertyBlock();
            if (mr != null) { mr.GetPropertyBlock(mpb); mpb.SetTexture(TexId, t); mr.SetPropertyBlock(mpb); }
        }

        void LateUpdate()
        {
            var k = kamera != null ? kamera : Camera.main;
            if (k != null) transform.rotation = k.transform.rotation;
        }
    }
}

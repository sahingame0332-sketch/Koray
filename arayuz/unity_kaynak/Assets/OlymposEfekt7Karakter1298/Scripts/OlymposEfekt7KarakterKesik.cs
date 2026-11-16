// OLYMPOS-KO · 1298 efekt 7 KARAKTER efekti: kilicin sari kesik yayi (skill kullanilirken karakterin onunde).
// Kayittan (14-01-51) 12 kare, 30 kare/sn (0.40 sn), eklemeli; renk/sicaklik degistirilmedi. Mobdaki vurus efekti ayri paket
// (OlymposEfekt7Hasar1298), mob kirmizisi ayri paket (OlymposMobHasar1298).
// Boyut karakter boyuna gore: genislik 1.166 x boy, yukseklik/genislik 1.026; pivot = karakterin ayagi (0.502, -0.272) —
// ayak kayitta alt cubugun altinda kaliyordu: oyuncu boyu (620 px) ve ayak TAHMIN, Inspector'dan rotus.
// Yon: kayitta hedef karakterin SOLUNDA; hedef ekranda saga dustugunde doku otomatik aynalanir (otomatikAyna).
// Kullanim: kesik.Oyna(karakter.transform, hedef.transform);
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.Efekt7Karakter
{
    [AddComponentMenu("OLYMPOS/1298/Efekt 7 Karakter/Kilic Kesigi")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposEfekt7KarakterKesik : MonoBehaviour
    {
        public Texture2D[] kareler = new Texture2D[0];
        public float fps = 30f;
        [Header("Boyut (olculen; oyuncu boyu tahmin)")]
        public float karakterBoyu = 1.8f;
        public float genislikKarakter = 1.1661f;
        public float enBoy = 1.0263f;
        public Vector2 pivot = new Vector2(0.5021f, -0.2722f);
        [Tooltip("Kamera yonunde kaydirma (m); negatif = karakterin onunde.")]
        public float derinlik = -0.3f;
        [Header("Yon")]
        public bool otomatikAyna = true;
        public bool ayna = false;
        [Header("Gorunum")]
        public Color renk = Color.white;
        [Range(0f, 4f)] public float parlaklik = 1f;
        public Camera kamera;
        public Transform karakter, hedef;
        [Header("Deneme")]
        public bool denemeDongusu = false;
        public float denemeAraligi = 0.8f;
        public UnityEvent onBitti = new UnityEvent();

        MeshRenderer mr; MeshFilter mf; MaterialPropertyBlock mpb; float t; bool oynuyor, sonAyna;
        static readonly int TexId = Shader.PropertyToID("_MainTex");
        static readonly int RenkId = Shader.PropertyToID("_Renk");
        static readonly int ParlakId = Shader.PropertyToID("_Parlaklik");

        public float Sure { get { return kareler.Length / Mathf.Max(1f, fps); } }

        void Awake() { mr = GetComponent<MeshRenderer>(); mf = GetComponent<MeshFilter>(); mpb = new MaterialPropertyBlock(); MeshKur(false); if (!oynuyor) mr.enabled = false; }
        void Start() { if (denemeDongusu) Oyna(karakter, hedef); }
        void OnValidate() { if (!Application.isPlaying && GetComponent<MeshFilter>() != null) { mf = GetComponent<MeshFilter>(); MeshKur(ayna); } }

        void MeshKur(bool aynali)
        {
            float w = karakterBoyu * genislikKarakter, h = w * enBoy;
            float px = aynali ? 1f - pivot.x : pivot.x, x0 = -px * w, y0 = -pivot.y * h;
            float u0 = aynali ? 1f : 0f, u1 = aynali ? 0f : 1f;
            var m = new Mesh(); m.name = "Efekt7KarakterDortgen";
            m.vertices = new[] { new Vector3(x0, y0, 0), new Vector3(x0 + w, y0, 0), new Vector3(x0, y0 + h, 0), new Vector3(x0 + w, y0 + h, 0) };
            m.uv = new[] { new Vector2(u0, 0), new Vector2(u1, 0), new Vector2(u0, 1), new Vector2(u1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds(); mf.sharedMesh = m; sonAyna = aynali;
        }

        public void Oyna(Transform kim, Transform neye)
        {
            if (kim != null) karakter = kim; hedef = neye;
            if (mr == null) mr = GetComponent<MeshRenderer>(); if (mf == null) mf = GetComponent<MeshFilter>(); if (mpb == null) mpb = new MaterialPropertyBlock();
            t = 0f; oynuyor = true; mr.enabled = kareler.Length > 0; Konumla(); KareYaz(0);
        }

        public void Durdur() { oynuyor = false; if (mr != null) mr.enabled = false; }

        void Update()
        {
            if (!oynuyor) return;
            t += Time.deltaTime; int k = Mathf.FloorToInt(t * fps);
            if (k >= kareler.Length) { Durdur(); onBitti.Invoke(); if (denemeDongusu) Invoke("Tekrar", denemeAraligi); return; }
            KareYaz(k);
        }

        void Tekrar() { Oyna(karakter, hedef); }
        void LateUpdate() { if (oynuyor) Konumla(); }

        void Konumla()
        {
            var k = kamera != null ? kamera : Camera.main;
            Vector3 p = karakter != null ? karakter.position : transform.position;
            bool aynali = ayna;
            if (k != null)
            {
                if (otomatikAyna && hedef != null && karakter != null)
                    aynali = k.WorldToScreenPoint(hedef.position).x > k.WorldToScreenPoint(karakter.position).x;   // kayitta hedef solda
                transform.rotation = k.transform.rotation; p += k.transform.forward * derinlik;
            }
            if (aynali != sonAyna) MeshKur(aynali);
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

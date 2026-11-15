// OLYMPOS-KO · 1298 karakterin kendine uyguladigi skill efektleri — kare kare oynatici (dunya uzayi, kameraya donuk dortgen).
// Kaynak: kullanicinin 9 telefon kaydi (2712x1220), 30 kare/sn. Her efektin karesi 720 x 860 px (ayni kesim kutusu);
// karakter kayitta ~265 px boyunda, ayagi kare icinde (370, 685) -> pivot (0.514, 0.203), genislik 2.717 karakter boyu.
// Efektler: Dokum yildizlari (cast sirasinda), Hide, Light Feet, Cat's/Lupine Eyes, Evade, Safety, Cure Disease/Curse, Magic Shield.
// Kullanim: efekt.Oyna(karakter.transform);  (dongu kapali, bitince gizlenir)
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.KendiSkill
{
    [AddComponentMenu("OLYMPOS/1298/Kendi Skill/Kendi Skill Efekti")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposKendiSkillEfekti : MonoBehaviour
    {
        public string skillAdi = "";
        public Texture2D[] kareler = new Texture2D[0];
        [Tooltip("Olculen: 30 kare/sn.")]
        public float fps = 30f;
        public bool dongu = false;
        public bool baslangictaOyna = false;
        public bool bitinceGizle = true;

        [Header("Boyut (olculen)")]
        public float karakterBoyu = 1.8f;
        [Tooltip("Kare genisligi / karakter boyu (720 / 265).")]
        public float genislikKarakter = 2.717f;
        [Tooltip("Yukseklik / genislik (860 / 720).")]
        public float enBoy = 1.194f;
        [Tooltip("Karakterin ayaginin kare icindeki yeri (x soldan, y alttan).")]
        public Vector2 pivot = new Vector2(0.514f, 0.203f);

        [Header("Gorunum")]
        public Color renk = Color.white;
        [Range(0f, 4f)] public float parlaklik = 1f;
        public Camera kamera;
        [Tooltip("Efekti bu karaktere bagla (ayaginda kalir).")]
        public Transform hedef;

        public UnityEvent onBitti = new UnityEvent();

        MeshRenderer mr; MaterialPropertyBlock mpb; float t; bool oynuyor;
        static readonly int TexId = Shader.PropertyToID("_MainTex");
        static readonly int RenkId = Shader.PropertyToID("_Renk");
        static readonly int ParlakId = Shader.PropertyToID("_Parlaklik");

        public float Sure { get { return kareler.Length / Mathf.Max(1f, fps); } }

        void Awake() { mr = GetComponent<MeshRenderer>(); mpb = new MaterialPropertyBlock(); MeshKur(); if (!baslangictaOyna && mr != null) mr.enabled = false; }
        void OnEnable() { if (baslangictaOyna) Oyna(hedef); }
        void OnValidate() { if (!Application.isPlaying && GetComponent<MeshFilter>() != null) MeshKur(); }

        void MeshKur()
        {
            float w = karakterBoyu * genislikKarakter, h = w * enBoy, x0 = -pivot.x * w, y0 = -pivot.y * h;
            var m = new Mesh(); m.name = "KendiSkillDortgen";
            m.vertices = new[] { new Vector3(x0, y0, 0), new Vector3(x0 + w, y0, 0), new Vector3(x0, y0 + h, 0), new Vector3(x0 + w, y0 + h, 0) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds();
            GetComponent<MeshFilter>().sharedMesh = m;
        }

        public void Oyna(Transform takip)
        {
            if (takip != null) hedef = takip;
            gameObject.SetActive(true); t = 0f; oynuyor = true;
            if (mr != null) mr.enabled = true;
            KareYaz(0);
        }

        public void Durdur() { oynuyor = false; if (mr != null) mr.enabled = false; }

        void Update()
        {
            if (!oynuyor || kareler.Length == 0) return;
            t += Time.deltaTime;
            int k = Mathf.FloorToInt(t * fps);
            if (k >= kareler.Length)
            {
                if (dongu) { t = 0f; k = 0; }
                else { Durdur(); onBitti.Invoke(); if (bitinceGizle) gameObject.SetActive(false); return; }
            }
            KareYaz(k);
        }

        void LateUpdate()
        {
            if (hedef != null) transform.position = hedef.position;
            var k = kamera != null ? kamera : Camera.main;
            if (k != null) transform.rotation = k.transform.rotation;
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

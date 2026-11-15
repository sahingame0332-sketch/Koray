// OLYMPOS-KO · yakin dovus skill efektinin bir katmani — kare kare oynatici (dunya uzayi, kameraya donuk dortgen, eklemeli).
// Iki tur katman: KARAKTER (kesik yaylari + kivilcimlar; karakterin ayagina bagli) ve HEDEF (gokten isin + vurus patlamasi; hedefin zeminine bagli).
// Boyut: dortgen genisligi = karakterBoyu * genislikKarakter; pivot = bagli noktanin (ayak / hedef zemini) kare icindeki yeri (x soldan, y alttan).
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.YakinSkill
{
    [AddComponentMenu("OLYMPOS/1298/Yakin Skill/Yakin Skill Katmani")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposYakinSkillKatmani : MonoBehaviour
    {
        public Texture2D[] kareler = new Texture2D[0];
        [Tooltip("Olculen: 30 kare/sn.")]
        public float fps = 30f;
        [Tooltip("Skill basladiktan kac kare sonra baslar (kayittaki zamanlama).")]
        public int gecikmeKare = 0;
        public bool dongu = false;

        [Header("Boyut (olculen)")]
        public float karakterBoyu = 1.8f;
        [Tooltip("Kare genisligi / karakter boyu (hedef katmaninda hedefin derinligindeki karakter boyu).")]
        public float genislikKarakter = 1f;
        [Tooltip("Yukseklik / genislik.")]
        public float enBoy = 1f;
        [Tooltip("Bagli noktanin kare icindeki yeri (x soldan, y alttan; 0-1).")]
        public Vector2 pivot = new Vector2(0.5f, 0f);

        [Header("Gorunum")]
        public Color renk = Color.white;
        [Range(0f, 4f)] public float parlaklik = 1f;
        public Camera kamera;
        [Tooltip("Katmani bu noktaya bagla (karakter ayagi ya da hedef).")]
        public Transform bagli;

        public UnityEvent onBitti = new UnityEvent();

        MeshRenderer mr; MaterialPropertyBlock mpb; float t; bool oynuyor;
        static readonly int TexId = Shader.PropertyToID("_MainTex");
        static readonly int RenkId = Shader.PropertyToID("_Renk");
        static readonly int ParlakId = Shader.PropertyToID("_Parlaklik");

        public float Sure { get { return (gecikmeKare + kareler.Length) / Mathf.Max(1f, fps); } }
        public bool Oynuyor { get { return oynuyor; } }

        void Awake() { mr = GetComponent<MeshRenderer>(); mpb = new MaterialPropertyBlock(); MeshKur(); if (mr != null && !oynuyor) mr.enabled = false; }
        void OnValidate() { if (!Application.isPlaying && GetComponent<MeshFilter>() != null) MeshKur(); }

        public void MeshKur()
        {
            float w = karakterBoyu * genislikKarakter, h = w * enBoy, x0 = -pivot.x * w, y0 = -pivot.y * h;
            var m = new Mesh(); m.name = "YakinSkillDortgen";
            m.vertices = new[] { new Vector3(x0, y0, 0), new Vector3(x0 + w, y0, 0), new Vector3(x0, y0 + h, 0), new Vector3(x0 + w, y0 + h, 0) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds();
            GetComponent<MeshFilter>().sharedMesh = m;
        }

        public void Oyna(Transform nokta)
        {
            if (nokta != null) bagli = nokta;
            gameObject.SetActive(true); t = 0f; oynuyor = true;
            if (mr == null) mr = GetComponent<MeshRenderer>();
            if (mpb == null) mpb = new MaterialPropertyBlock();
            mr.enabled = false;
            Konumla();
        }

        public void Durdur() { oynuyor = false; if (mr != null) mr.enabled = false; }

        void Update()
        {
            if (!oynuyor || kareler.Length == 0) return;
            t += Time.deltaTime;
            int k = Mathf.FloorToInt(t * fps) - gecikmeKare;
            if (k < 0) { mr.enabled = false; return; }
            if (k >= kareler.Length)
            {
                if (dongu) { t = 0f; k = 0; }
                else { Durdur(); onBitti.Invoke(); return; }
            }
            mr.enabled = true;
            KareYaz(k);
        }

        void LateUpdate() { Konumla(); }

        void Konumla()
        {
            if (bagli != null) transform.position = bagli.position;
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

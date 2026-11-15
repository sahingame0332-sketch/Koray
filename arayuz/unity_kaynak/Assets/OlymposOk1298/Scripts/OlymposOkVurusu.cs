// OLYMPOS-KO · ok vurusu: beyaz cizgi-roman patlamasi (0-0.2 sn) + gokten inen turuncu isin (0.2-1.2 sn) + pembe duman.
// 23 kare, 30 kare/sn, kare 520 x 260 px; on-carpimli ("Olympos/Ok Vurus"). Kayitta sol ustteki karakter paneli isinin
// ust kismini ortuyordu: isin karenin ust kenarinda kesik baslar.
// Boyut: kare genisligi 3.47 karakter boyu (hedefin uzakligindaki karakter boyu ~150 px, ufuk cizgisine gore olcek — tahmini olcu).
// Pivot: hedefin ayagi (secim halkasi merkezi) kare icinde (0.442, 0.277). Kameraya doner.
using UnityEngine;

namespace Olympos.Ok
{
    [AddComponentMenu("OLYMPOS/1298/Ok/Ok Vurusu")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposOkVurusu : MonoBehaviour
    {
        public Texture2D[] kareler = new Texture2D[0];
        public float fps = 30f;
        public float karakterBoyu = 1.8f;
        public float genislikKarakter = 3.47f;
        public float enBoy = 0.5f;
        public Vector2 pivot = new Vector2(0.442f, 0.277f);
        public bool dongu = false;
        public bool baslangictaOyna = false;
        public Camera kamera;
        [Tooltip("Hedef hareket ederse ayaginda kal.")]
        public Transform hedef;

        MeshRenderer mr; MaterialPropertyBlock mpb; float t; bool oynuyor;
        static readonly int TexId = Shader.PropertyToID("_MainTex");

        void Awake() { mr = GetComponent<MeshRenderer>(); mpb = new MaterialPropertyBlock(); MeshKur(); }
        void OnEnable() { if (baslangictaOyna) Oyna(); }
        void OnValidate() { if (!Application.isPlaying && GetComponent<MeshFilter>() != null) MeshKur(); }

        void MeshKur()
        {
            float w = karakterBoyu * genislikKarakter, h = w * enBoy, x0 = -pivot.x * w, y0 = -pivot.y * h;
            var m = new Mesh(); m.name = "OkVurusDortgen";
            m.vertices = new[] { new Vector3(x0, y0, 0), new Vector3(x0 + w, y0, 0), new Vector3(x0, y0 + h, 0), new Vector3(x0 + w, y0 + h, 0) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds();
            GetComponent<MeshFilter>().sharedMesh = m;
        }

        public void Oyna() { MeshKur(); t = 0f; oynuyor = true; if (mr != null) mr.enabled = true; Yaz(0); }

        void Update()
        {
            if (!oynuyor || kareler.Length == 0) return;
            t += Time.deltaTime; int k = Mathf.FloorToInt(t * fps);
            if (k >= kareler.Length) { if (dongu) { t = 0f; k = 0; } else { oynuyor = false; Destroy(gameObject); return; } }
            Yaz(k);
        }

        void LateUpdate()
        {
            if (hedef != null) transform.position = hedef.position;
            var c = kamera != null ? kamera : Camera.main; if (c != null) transform.rotation = c.transform.rotation;
        }

        void Yaz(int k)
        {
            if (mr == null || kareler.Length == 0) return;
            mr.GetPropertyBlock(mpb); if (kareler[k] != null) mpb.SetTexture(TexId, kareler[k]); mr.SetPropertyBlock(mpb);
        }
    }
}

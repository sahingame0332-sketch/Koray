// OLYMPOS-KO · 1298 yerdeki Merchant tezgahi (mavi ortulu alcak sandik + kirmizi sancak, parsomenler, kilic, yuzukler).
// Iki ekran goruntusunden kesildi (2712x1220): ON gorunus 251 x 330 px, YAN gorunus 193 x 246 px; opak, kenar yumusak, renk/isik degismedi.
// Kameraya donuk dortgen; kameranin tezgaha bakis acisina gore ON / YAN dokusu secilir (YAN'in ters tarafi yatay ayna).
// Boyut karakter boyuna gore olculdu: ON yukseklik 0.773 (karakter 427 px), YAN 0.741 (karakter 332 px) karakter boyu.
// transform.forward = tezgahin on yuzu (sancagin sarktigi taraf). Kullanim: tezgah.Kur(konum, yonu); tezgah.Kaldir();
using UnityEngine;

namespace Olympos.Tezgah
{
    [AddComponentMenu("OLYMPOS/1298/Merchant Tezgahi")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposTezgah : MonoBehaviour
    {
        [Header("Dokular")]
        public Texture2D onDoku;
        public Texture2D yanDoku;

        [Header("Boyut (olculen)")]
        [Tooltip("Karakterinizin dunya birimindeki boyu.")]
        public float karakterBoyu = 1.8f;
        public float onYukseklik = 0.773f;
        public float onEnBoy = 0.761f;
        public Vector2 onPivot = new Vector2(0.54f, 0f);
        public float yanYukseklik = 0.741f;
        public float yanEnBoy = 0.785f;
        public Vector2 yanPivot = new Vector2(0.55f, 0f);

        [Header("Gorunum secimi")]
        [Tooltip("Kamera tezgahin onune bu acidan (derece) daha dik bakarsa ON dokusu, degilse YAN.")]
        [Range(0f, 90f)] public float onAcisi = 50f;
        public Camera kamera;

        MeshRenderer mr; MeshFilter mf; MaterialPropertyBlock mpb;
        int secili = -1;   // 0 on, 1 yan, 2 yan (ayna)
        static readonly int TexId = Shader.PropertyToID("_MainTex");
        static readonly int AynaId = Shader.PropertyToID("_Ayna");

        void Awake() { mr = GetComponent<MeshRenderer>(); mf = GetComponent<MeshFilter>(); mpb = new MaterialPropertyBlock(); Sec(0); }
        void OnValidate() { if (GetComponent<MeshFilter>() != null) { mf = GetComponent<MeshFilter>(); MeshKur(secili < 0 ? 0 : secili); } }

        void MeshKur(int g)
        {
            float hk = g == 0 ? onYukseklik : yanYukseklik, eb = g == 0 ? onEnBoy : yanEnBoy; var pv = g == 0 ? onPivot : yanPivot;
            if (g == 2) pv.x = 1f - pv.x;
            float h = karakterBoyu * hk, w = h * eb, x0 = -pv.x * w, y0 = -pv.y * h;
            var m = new Mesh(); m.name = "TezgahDortgen";
            m.vertices = new[] { new Vector3(x0, y0, 0), new Vector3(x0 + w, y0, 0), new Vector3(x0, y0 + h, 0), new Vector3(x0 + w, y0 + h, 0) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds();
            mf.sharedMesh = m;
        }

        void Sec(int g)
        {
            if (g == secili || mr == null) return;
            secili = g; MeshKur(g);
            mr.GetPropertyBlock(mpb);
            var d = g == 0 ? onDoku : yanDoku; if (d != null) mpb.SetTexture(TexId, d);
            mpb.SetFloat(AynaId, g == 2 ? 1f : 0f);
            mr.SetPropertyBlock(mpb);
        }

        void LateUpdate()
        {
            var k = kamera != null ? kamera : Camera.main; if (k == null) return;
            // bakis: kameradan tezgaha, yatay duzlemde; tezgahin on yuzune gore aci
            Vector3 bak = transform.parent != null ? transform.parent.forward : yon;
            Vector3 kb = k.transform.forward; kb.y = 0f; bak.y = 0f;
            if (kb.sqrMagnitude > 1e-4f && bak.sqrMagnitude > 1e-4f)
            {
                float aci = Vector3.SignedAngle(-bak.normalized, kb.normalized, Vector3.up);
                Sec(Mathf.Abs(aci) <= onAcisi ? 0 : (aci > 0 ? 1 : 2));
            }
            transform.rotation = k.transform.rotation;          // kameraya donuk
        }

        [Tooltip("Tezgahin on yuzunun dunya yonu (ebeveyn yoksa).")]
        public Vector3 yon = Vector3.back;

        public void Kur(Vector3 dunyaKonumu, Vector3 onYonu) { transform.position = dunyaKonumu; yon = onYonu; gameObject.SetActive(true); }
        public void Kaldir() { gameObject.SetActive(false); }
    }
}

// OLYMPOS-KO · 1298 neon run halkasi (mor / mavi / yesil) — skill kullanirken karakterin altinda (OZGUN tasarim; stok gorsel kopyalanmadi).
// Iki parca: yerde run dairesi ("Olympos/Rune Neon Halkasi") + kenarindan yukselen alev duvari ("Olympos/Rune Neon Duvari").
// Boyut karakter boyuna gore: cap = karakterBoyu * capKarakter (1.6), alev duvari yuksekligi = cap * 0.12 (alevler yere yakin).
// Zarf: acilis (buyuyerek belirir) -> yanma -> sonus. Kullanim:  efekt.Oyna(karakter.transform, 2f);
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.RuneNeon
{
    [AddComponentMenu("OLYMPOS/1298/Rune Neon/Neon Run Halkasi")]
    public class OlymposRuneNeonEfekti : MonoBehaviour
    {
        [Header("Malzemeler")]
        public Material halkaMalzemesi;
        public Material duvarMalzemesi;

        [Header("Boyut")]
        public float karakterBoyu = 1.8f;
        [Tooltip("Daire capi, karakter boyu cinsinden.")]
        public float capKarakter = 1.6f;
        [Tooltip("Alev duvari yuksekligi / cap. 0 = duvar yok.")]
        public float duvarOrani = 0.12f;
        [Tooltip("Yerden yukseklik (z-fighting olmasin).")]
        public float yerdenYukseklik = 0.02f;

        [Header("Gorunum")]
        [Tooltip("Genel yogunluk (eklemeli efekt: dusuk = daha saydam). 0.5: karakterin onune gecmez.")]
        [Range(0f, 2f)] public float yogunluk = 0.5f;

        [Header("Zaman")]
        public float acilis = 0.25f;
        public float sure = 2.0f;
        public float sonus = 0.5f;
        public bool dongu = false;
        public bool baslangictaOyna = true;

        [Header("Takip")]
        [Tooltip("Bos degilse efekt bu karakterin ayaginda kalir.")]
        public Transform hedef;

        public UnityEvent onBitti = new UnityEvent();

        Transform halka, duvar;
        MeshRenderer hr, dr;
        MaterialPropertyBlock mpb;
        float t = -1f;
        static readonly int ZamanId = Shader.PropertyToID("_Zaman");
        static readonly int GucId = Shader.PropertyToID("_Guc");

        void Awake() { Kur(); }
        void OnEnable() { if (baslangictaOyna) Oyna(hedef, sure); }

        void Kur()
        {
            mpb = new MaterialPropertyBlock();
            if (halka == null)
            {
                var go = new GameObject("Halka", typeof(MeshFilter), typeof(MeshRenderer));
                go.transform.SetParent(transform, false);
                go.GetComponent<MeshFilter>().sharedMesh = Dortgen();
                hr = go.GetComponent<MeshRenderer>(); hr.sharedMaterial = halkaMalzemesi;
                hr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; hr.receiveShadows = false;
                halka = go.transform;
            }
            if (duvar == null)
            {
                var go = new GameObject("AlevDuvari", typeof(MeshFilter), typeof(MeshRenderer));
                go.transform.SetParent(transform, false);
                go.GetComponent<MeshFilter>().sharedMesh = Silindir(48);
                dr = go.GetComponent<MeshRenderer>(); dr.sharedMaterial = duvarMalzemesi;
                dr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; dr.receiveShadows = false;
                duvar = go.transform;
            }
            Olcekle(1f);
        }

        /// <summary>Yatay birim kare (XZ), merkez orijin, UV 0..1.</summary>
        static Mesh Dortgen()
        {
            var m = new Mesh(); m.name = "RuneHalka";
            m.vertices = new[] { new Vector3(-0.5f, 0, -0.5f), new Vector3(0.5f, 0, -0.5f), new Vector3(-0.5f, 0, 0.5f), new Vector3(0.5f, 0, 0.5f) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds(); return m;
        }

        /// <summary>Yaricap 0.5, yukseklik 1 acik silindir; u = cevre, v = yukseklik.</summary>
        static Mesh Silindir(int n)
        {
            var v = new Vector3[(n + 1) * 2]; var uv = new Vector2[(n + 1) * 2]; var tr = new int[n * 6];
            for (int i = 0; i <= n; i++)
            {
                float a = i / (float)n * Mathf.PI * 2f, x = Mathf.Cos(a) * 0.5f, z = Mathf.Sin(a) * 0.5f;
                v[i * 2] = new Vector3(x, 0, z); v[i * 2 + 1] = new Vector3(x, 1, z);
                uv[i * 2] = new Vector2(i / (float)n, 0); uv[i * 2 + 1] = new Vector2(i / (float)n, 1);
                if (i < n) { int k = i * 6, b = i * 2; tr[k] = b; tr[k + 1] = b + 1; tr[k + 2] = b + 2; tr[k + 3] = b + 2; tr[k + 4] = b + 1; tr[k + 5] = b + 3; }
            }
            var m = new Mesh(); m.name = "RuneDuvar"; m.vertices = v; m.uv = uv; m.triangles = tr; m.RecalculateBounds(); return m;
        }

        void Olcekle(float k)
        {
            float cap = karakterBoyu * capKarakter * k;
            if (halka != null) { halka.localScale = new Vector3(cap, 1f, cap); halka.localPosition = new Vector3(0, yerdenYukseklik, 0); }
            if (duvar != null)
            {
                duvar.gameObject.SetActive(duvarOrani > 0f);
                duvar.localScale = new Vector3(cap * 0.97f, Mathf.Max(0.001f, cap * duvarOrani * k), cap * 0.97f);
            }
        }

        public void Oyna(Transform takip, float yanmaSuresi)
        {
            if (takip != null) hedef = takip;
            sure = yanmaSuresi; t = 0f;
            gameObject.SetActive(true);
            if (hr != null) hr.enabled = true; if (dr != null) dr.enabled = true;
        }

        public void Durdur() { if (t >= 0f && t < acilis + sure) t = acilis + sure; }

        void Update()
        {
            if (t < 0f) return;
            t += Time.deltaTime;
            if (hedef != null) transform.position = hedef.position;
            float toplam = acilis + sure + sonus, guc, k;
            if (t < acilis) { float p = t / acilis; guc = p; k = Mathf.Lerp(0.6f, 1f, 1f - (1f - p) * (1f - p)); }
            else if (t < acilis + sure) { guc = 1f; k = 1f; }
            else if (t < toplam) { guc = 1f - (t - acilis - sure) / sonus; k = 1f; }
            else
            {
                if (dongu) { t = acilis; return; }
                t = -1f; if (hr != null) hr.enabled = false; if (dr != null) dr.enabled = false;
                onBitti.Invoke(); return;
            }
            Olcekle(k);
            Yaz(hr, guc); Yaz(dr, guc);
        }

        void Yaz(MeshRenderer r, float guc)
        {
            if (r == null) return;
            r.GetPropertyBlock(mpb); mpb.SetFloat(ZamanId, t); mpb.SetFloat(GucId, guc * yogunluk); r.SetPropertyBlock(mpb);
        }
    }
}

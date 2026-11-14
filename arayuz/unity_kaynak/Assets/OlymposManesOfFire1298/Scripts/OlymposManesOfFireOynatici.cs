// OLYMPOS-KO · 1298 "Manes Of Fire" (moba uygulanan skill) — kare kare oynatici (dunya uzayi, kameraya donuk dortgen)
// Kareler kullanicinin tablet kaydindan (2266x1488, 60 kare/sn) 2 karede bir: 49 kare, 30 kare/sn, 1.63 sn, 520 x 940 px.
// Gokten inen turuncu isin + dusen kirmizi prizma + mobun ustunde yanan ates + yerde donen sari run halkalari.
// Malzeme "Olympos/Manes Of Fire Eklemeli" (Blend One One): siyah = saydam, renk orijinalin isigi (orijinal - zemin).
// Boyut: kayitta mob ~140 px -> kare genisligi 3.71 mob/karakter boyu; pivot = mobun ayagi (0.365, 0.126).
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.ManesOfFire
{
    [AddComponentMenu("OLYMPOS/1298/Manes Of Fire/Manes Of Fire Oynatici")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposManesOfFireOynatici : MonoBehaviour
    {
        [Header("Kareler")]
        public Texture2D[] kareler = new Texture2D[0];
        [Tooltip("Kare hizi. Olculen: 30 (kayit ~67 kare/sn, 30 kare/sn.ye orneklendi).")]
        public float fps = 30f;
        public bool dongu = false;
        [Tooltip("Parlaklik 0'dan tama bu surede cikar. Kayit eksiksiz: 0.")]
        public float acilis = 0f;
        [Tooltip("Etkinlesince kendiliginden oynar.")]
        public bool baslangictaOyna = true;
        [Tooltip("Bitince nesneyi kapat.")]
        public bool bitinceGizle = true;

        [Header("Boyut")]
        [Tooltip("Karakterinizin dunya birimindeki boyu.")]
        public float karakterBoyu = 1.8f;
        [Tooltip("Efekt karesinin genisligi, karakter boyu cinsinden (olculen).")]
        public float genislikKarakter = 3.71f;
        [Tooltip("Kare en/boy orani (yukseklik / genislik, olculen).")]
        public float enBoy = 1.808f;
        [Tooltip("Hedef noktanin kare icindeki yeri (0..1; x soldan, y alttan).")]
        public Vector2 pivot = new Vector2(0.365f, 0.126f);

        [Header("Gorunum")]
        public Color renk = Color.white;
        [Range(0f, 4f)] public float parlaklik = 1f;
        [Tooltip("Kameraya don (kartal panosu). Bos ise Camera.main.")]
        public bool kameraya = true;
        public Camera kamera;

        public UnityEvent onBitti = new UnityEvent();

        MeshRenderer mr;
        MaterialPropertyBlock mpb;
        float t;
        bool oynuyor;
        static readonly int TexId = Shader.PropertyToID("_MainTex");
        static readonly int RenkId = Shader.PropertyToID("_Renk");
        static readonly int ParlakId = Shader.PropertyToID("_Parlaklik");

        public float Sure { get { return kareler.Length / Mathf.Max(1f, fps); } }

        void Awake()
        {
            mr = GetComponent<MeshRenderer>();
            mpb = new MaterialPropertyBlock();
            MeshKur();
        }

        void OnEnable() { if (baslangictaOyna) Oyna(); }

        void OnValidate()
        {
            if (Application.isPlaying) return;
            if (GetComponent<MeshFilter>() != null) MeshKur();
        }

        /// <summary>Pivot noktasi nesnenin konumunda olacak sekilde dortgeni kurar.</summary>
        void MeshKur()
        {
            float w = karakterBoyu * genislikKarakter, h = w * enBoy;
            float x0 = -pivot.x * w, y0 = -pivot.y * h;
            var m = new Mesh();
            m.name = "EfektDortgen";
            m.vertices = new[] { new Vector3(x0, y0, 0), new Vector3(x0 + w, y0, 0), new Vector3(x0, y0 + h, 0), new Vector3(x0 + w, y0 + h, 0) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds();
            GetComponent<MeshFilter>().sharedMesh = m;
        }

        public void Oyna()
        {
            t = 0f; oynuyor = true;
            if (mr != null) mr.enabled = true;
            KareYaz(0);
        }

        public void Durdur()
        {
            oynuyor = false;
            if (mr != null) mr.enabled = false;
        }

        void Update()
        {
            if (!oynuyor || kareler.Length == 0) return;
            t += Time.deltaTime;
            int k = Mathf.FloorToInt(t * fps);
            if (k >= kareler.Length)
            {
                if (dongu) { t = 0f; k = 0; }
                else
                {
                    oynuyor = false;
                    if (mr != null) mr.enabled = false;
                    onBitti.Invoke();
                    if (bitinceGizle) gameObject.SetActive(false);
                    return;
                }
            }
            KareYaz(k);
        }

        void LateUpdate()
        {
            if (!kameraya) return;
            var k = kamera != null ? kamera : Camera.main;
            if (k == null) return;
            transform.rotation = k.transform.rotation;      // kameraya paralel (ekran duzleminde)
        }

        void KareYaz(int k)
        {
            if (mr == null || kareler.Length == 0) return;
            mr.GetPropertyBlock(mpb);
            if (kareler[k] != null) mpb.SetTexture(TexId, kareler[k]);
            mpb.SetColor(RenkId, renk);
            mpb.SetFloat(ParlakId, parlaklik * (acilis > 0f ? Mathf.Clamp01(t / acilis) : 1f));
            mr.SetPropertyBlock(mpb);
        }

        /// <summary>Efekti bir hedefin uzerinde oynatir (konum + istege bagli karakter boyu).</summary>
        public void Hedefte(Vector3 dunyaKonumu)
        {
            transform.position = dunyaKonumu;
            gameObject.SetActive(true);
            Oyna();
        }
    }
}

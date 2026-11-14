// OLYMPOS-KO · 1298 karakter alti ates havuzu — kare kare oynatici (dunya uzayi, kameraya donuk dortgen)
// Kareler kullanicinin kaydindan (2712x1220, ~67 kare/sn) 30 kare/sn'ye orneklenerek cikarildi: 39 kare, 1.3 sn, 560 x 420 px.
// Malzeme "Olympos/Ates Havuzu Eklemeli" (Blend One One): siyah = saydam, renk orijinalin isigi (orijinal - zemin).
// Boyut: kayitta karakter ~150 px -> kare genisligi 3.73 karakter boyu; pivot = karakterin ayagi (kare icinde 0.464, 0.40).
// Kayitta efektin ilk ~0.2 sn'si kamera kayarken gectigi icin alinamadi: 'acilis' ile parlaklik 0'dan yukselir.
using UnityEngine;
using UnityEngine.Events;

namespace Olympos.AtesHavuzu
{
    [AddComponentMenu("OLYMPOS/1298/Ates Havuzu/Ates Havuzu Oynatici")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposAtesHavuzuOynatici : MonoBehaviour
    {
        [Header("Kareler")]
        public Texture2D[] kareler = new Texture2D[0];
        [Tooltip("Kare hizi. Olculen: 30 (kayit ~67 kare/sn, 30 kare/sn.ye orneklendi).")]
        public float fps = 30f;
        public bool dongu = false;
        [Tooltip("Parlaklik 0'dan tama bu surede cikar (kayitta kesilen baslangic). 0 = kapali.")]
        public float acilis = 0.15f;
        [Tooltip("Etkinlesince kendiliginden oynar.")]
        public bool baslangictaOyna = true;
        [Tooltip("Bitince nesneyi kapat.")]
        public bool bitinceGizle = true;

        [Header("Boyut")]
        [Tooltip("Karakterinizin dunya birimindeki boyu.")]
        public float karakterBoyu = 1.8f;
        [Tooltip("Efekt karesinin genisligi, karakter boyu cinsinden (olculen).")]
        public float genislikKarakter = 3.73f;
        [Tooltip("Kare en/boy orani (yukseklik / genislik, olculen).")]
        public float enBoy = 0.75f;
        [Tooltip("Hedef noktanin kare icindeki yeri (0..1; x soldan, y alttan).")]
        public Vector2 pivot = new Vector2(0.464f, 0.40f);

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

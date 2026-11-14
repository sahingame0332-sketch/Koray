// OLYMPOS-KO · 1298 yerdeki Merchant tezgahi (mavi ortulu alcak sandik + kirmizi sancak, parsomenler, kilic, yuzukler).
// Tek ekran goruntusunden kesildi (2712x1220): 251 x 330 px, opak nesne, kenar 1.2 px yumusak. Renk/isik degistirilmedi.
// Kameraya donuk dortgen (billboard). Boyut karakter boyuna gore olculdu: kayitta karakter 427 px ->
//   yukseklik 0.773, genislik 0.588 karakter boyu. Pivot: tezgahin yere degdigi alt orta nokta (0.54, 0.0).
// Kayitta tezgah satici karakterin yaninda, alicinin 1.2 karakter boyu sagindaydi; tezgah cubugu (OPEN/WHISPER) ustunde.
// Kullanim: Merchant acilinca tezgah.Kur(saticiKonumu + sag * 0.9f);  kapaninca tezgah.Kaldir();
using UnityEngine;

namespace Olympos.Tezgah
{
    [AddComponentMenu("OLYMPOS/1298/Merchant Tezgahi")]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposTezgah : MonoBehaviour
    {
        public Texture2D doku;
        [Tooltip("Karakterinizin dunya birimindeki boyu.")]
        public float karakterBoyu = 1.8f;
        [Tooltip("Tezgah yuksekligi, karakter boyu cinsinden (olculen 330/427).")]
        public float yukseklikKarakter = 0.773f;
        [Tooltip("En/boy (genislik / yukseklik, olculen 251/330).")]
        public float enBoy = 0.761f;
        public Vector2 pivot = new Vector2(0.54f, 0f);
        [Tooltip("Kameraya don (billboard). Kapatilirsa dunya yonunde sabit kalir.")]
        public bool kameraya = true;
        public Camera kamera;

        void Awake() { MeshKur(); }
        void OnValidate() { if (GetComponent<MeshFilter>() != null) MeshKur(); }

        void MeshKur()
        {
            float h = karakterBoyu * yukseklikKarakter, w = h * enBoy, x0 = -pivot.x * w, y0 = -pivot.y * h;
            var m = new Mesh(); m.name = "TezgahDortgen";
            m.vertices = new[] { new Vector3(x0, y0, 0), new Vector3(x0 + w, y0, 0), new Vector3(x0, y0 + h, 0), new Vector3(x0 + w, y0 + h, 0) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds();
            GetComponent<MeshFilter>().sharedMesh = m;
        }

        void LateUpdate()
        {
            if (!kameraya) return;
            var k = kamera != null ? kamera : Camera.main; if (k == null) return;
            transform.rotation = k.transform.rotation;
        }

        public void Kur(Vector3 dunyaKonumu) { transform.position = dunyaKonumu; gameObject.SetActive(true); }
        public void Kaldir() { gameObject.SetActive(false); }
    }
}

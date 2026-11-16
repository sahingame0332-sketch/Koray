// OLYMPOS-KO · 1298 mob olunce dusen sandik — 3B (govde + kubbe kapak), kapali / acik.
// Kullanicinin 5 ekran goruntusunden (2712x1220) olculdu: 3 kapali gorunumle kamera + sekil birlikte uyduruldu (siluet ortusmesi 0.92-0.93),
// acik gorunumde kapak acisi uyduruldu (115.5 derece, ortusme 0.87).
// Olculer (uzunluk = 1): derinlik 0.848, govde yuksekligi 0.389, kapak (yari elips) yuksekligi 0.414 -> toplam yukseklik 0.803.
// Uzunluk = 0.24 x karakter boyu (karakter 1.8 -> 0.43 m; tahmin, +-%15). Pivot: taban merkezi; transform.forward = kilitli on yuz.
// Dokular: on (kilit), arka, uc (kemerli yan, iki ucta ayni), kapak (kubbe; arka yamac on yamacin aynasi), acik: ust (cerceve + altinlar), kapak ici.
// Acik durumda yan yuzler ve kapak disi kayitta koyu: ton (0.41, 0.40, 0.45) — olculdu (acik goruntudeki golgeli yuzler).
// Kullanim: sandik.Dus(konum, yon) -> kapali;  sandik.Ac();  sandik.Kapat();  sandik.Kaldir();
using UnityEngine;

namespace Olympos.Sandik
{
    [AddComponentMenu("OLYMPOS/1298/Sandik/Sandik 3B")]
    public class OlymposSandik : MonoBehaviour
    {
        public enum Durum { Kapali, Acik }

        [Header("Boyut (olculen)")]
        public float karakterBoyu = 1.8f;
        [Tooltip("Sandik uzunlugu / karakter boyu (tahmin 0.24).")]
        public float uzunlukKarakter = 0.24f;
        public float derinlik = 0.848f;
        public float govdeYuksekligi = 0.389f;
        public float kapakYuksekligi = 0.414f;
        [Tooltip("Acik durumda kapagin acisi (derece, olculen 115.5).")]
        public float acikAci = 115.5f;
        [Range(8, 64)] public int kubbeDilim = 24;

        [Header("Malzemeler (kurucu doldurur)")]
        [Tooltip("0 on, 1 arka, 2 uc, 3 ust (acik)")]
        public Material[] govdeMalzemeleri = new Material[4];
        [Tooltip("0 kapak disi, 1 kapak ici, 2 uc")]
        public Material[] kapakMalzemeleri = new Material[3];

        [Header("Durum")]
        public Durum baslangic = Durum.Kapali;
        [Tooltip("Acilma suresi (sn) — kayitta acilis ani yok, varsayim.")]
        public float acilmaSuresi = 0.3f;
        public Color acikTon = new Color(0.41f, 0.40f, 0.45f, 1f);

        Transform kapak; MeshRenderer gR, kR; MaterialPropertyBlock mpb;
        float aci, hedefAci, ton = 1f, hedefTon = 1f;
        static readonly int RenkId = Shader.PropertyToID("_Renk");

        public Durum Simdi { get { return hedefAci > 0.5f ? Durum.Acik : Durum.Kapali; } }

        void Awake() { Kur(); Ayarla(baslangic, true); }

        public void Kur()
        {
            float L = karakterBoyu * uzunlukKarakter, D = derinlik * L, HB = govdeYuksekligi * L, HL = kapakYuksekligi * L, a = D * 0.5f;
            var g = Cocuk("Govde", transform); gR = Hazirla(g, govdeMalzemeleri);
            g.GetComponent<MeshFilter>().sharedMesh = GovdeMesh(L, D, HB, HL);
            var kk = Cocuk("Kapak Mentese", transform); kk.localPosition = new Vector3(0, HB, -a);   // arka ust kenar
            var km = Cocuk("Kapak", kk); kR = Hazirla(km, kapakMalzemeleri);
            km.GetComponent<MeshFilter>().sharedMesh = KapakMesh(L, D, HB, HL);
            kapak = kk;
            if (mpb == null) mpb = new MaterialPropertyBlock();
        }

        Transform Cocuk(string ad, Transform ust)
        {
            var t = ust.Find(ad);
            if (t == null) { t = new GameObject(ad).transform; t.SetParent(ust, false); }
            return t;
        }

        MeshRenderer Hazirla(Transform t, Material[] m)
        {
            var mf = t.GetComponent<MeshFilter>(); if (mf == null) mf = t.gameObject.AddComponent<MeshFilter>();
            var mr = t.GetComponent<MeshRenderer>(); if (mr == null) mr = t.gameObject.AddComponent<MeshRenderer>();
            mr.sharedMaterials = m; mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; mr.receiveShadows = false;
            return mr;
        }

        // olcum koordinati (x 0..L soldan, y yukari, z +on, sag-elli) -> Unity (sol-elli): x aynalanir, merkez tabanda
        static Vector3 U(float L, float x, float y, float z) { return new Vector3(-(x - L * 0.5f), y, z); }

        class Yapici
        {
            public System.Collections.Generic.List<Vector3> v = new System.Collections.Generic.List<Vector3>();
            public System.Collections.Generic.List<Vector2> uv = new System.Collections.Generic.List<Vector2>();
            public System.Collections.Generic.List<int>[] alt;
            public Yapici(int n) { alt = new System.Collections.Generic.List<int>[n]; for (int i = 0; i < n; i++) alt[i] = new System.Collections.Generic.List<int>(); }
            public void Dortgen(int s, Vector3 a, Vector3 b, Vector3 c, Vector3 d, Vector2 ua, Vector2 ub, Vector2 uc, Vector2 ud)
            {
                int k = v.Count; v.Add(a); v.Add(b); v.Add(c); v.Add(d); uv.Add(ua); uv.Add(ub); uv.Add(uc); uv.Add(ud);
                alt[s].AddRange(new[] { k, k + 1, k + 2, k, k + 2, k + 3 });
            }
            public void Ucgen(int s, Vector3 a, Vector3 b, Vector3 c, Vector2 ua, Vector2 ub, Vector2 uc)
            {
                int k = v.Count; v.Add(a); v.Add(b); v.Add(c); uv.Add(ua); uv.Add(ub); uv.Add(uc); alt[s].AddRange(new[] { k, k + 1, k + 2 });
            }
            public Mesh Mesh(string ad)
            {
                var m = new Mesh(); m.name = ad; m.SetVertices(v); m.SetUVs(0, uv); m.subMeshCount = alt.Length;
                for (int i = 0; i < alt.Length; i++) m.SetTriangles(alt[i], i);
                m.RecalculateNormals(); m.RecalculateBounds(); return m;
            }
        }

        Mesh GovdeMesh(float L, float D, float HB, float HL)
        {
            float a = D * 0.5f, vb = HB / (HB + HL); var y = new Yapici(4);
            Vector2 sU = new Vector2(0, 1), sgU = new Vector2(1, 1), sgA = new Vector2(1, 0), sA = new Vector2(0, 0);
            y.Dortgen(0, U(L, 0, HB, a), U(L, L, HB, a), U(L, L, 0, a), U(L, 0, 0, a), sU, sgU, sgA, sA);                 // on
            y.Dortgen(1, U(L, L, HB, -a), U(L, 0, HB, -a), U(L, 0, 0, -a), U(L, L, 0, -a), sU, sgU, sgA, sA);             // arka
            y.Dortgen(2, U(L, L, HB, a), U(L, L, HB, -a), U(L, L, 0, -a), U(L, L, 0, a), new Vector2(0, vb), new Vector2(1, vb), new Vector2(1, 0), new Vector2(0, 0));
            y.Dortgen(2, U(L, 0, HB, -a), U(L, 0, HB, a), U(L, 0, 0, a), U(L, 0, 0, -a), new Vector2(1, vb), new Vector2(0, vb), new Vector2(0, 0), new Vector2(1, 0));
            y.Dortgen(3, U(L, 0, HB, -a), U(L, L, HB, -a), U(L, L, HB, a), U(L, 0, HB, a), sU, sgU, sgA, sA);             // ust (acik: cerceve + altin)
            return y.Mesh("SandikGovde");
        }

        // kapak mentese noktasina gore (mentese = (y HB, z -a)) kurulur; donus mentese transform'unda
        Mesh KapakMesh(float L, float D, float HB, float HL)
        {
            float a = D * 0.5f, H = HB + HL; int N = Mathf.Max(8, kubbeDilim); var y = new Yapici(3);
            System.Func<float, float, float, Vector3> P = (x, yy, z) => U(L, x, yy - HB, z + a);
            float e = 0.012f * L;
            for (int k = 0; k < N; k++)
            {
                float p0 = Mathf.PI * k / N, p1 = Mathf.PI * (k + 1) / N, v0 = (float)k / N, v1 = (float)(k + 1) / N;
                for (int ic = 0; ic < 2; ic++)
                {
                    float hl = HL - (ic == 1 ? e : 0f), aa = a - (ic == 1 ? e : 0f);
                    Vector3 q0 = P(0, HB + hl * Mathf.Sin(p0), aa * Mathf.Cos(p0)), q1 = P(L, HB + hl * Mathf.Sin(p0), aa * Mathf.Cos(p0));
                    Vector3 q2 = P(L, HB + hl * Mathf.Sin(p1), aa * Mathf.Cos(p1)), q3 = P(0, HB + hl * Mathf.Sin(p1), aa * Mathf.Cos(p1));
                    y.Dortgen(ic, q0, q1, q2, q3, new Vector2(0, v0), new Vector2(1, v0), new Vector2(1, v1), new Vector2(0, v1));
                }
                for (int uc = 0; uc < 2; uc++)
                {
                    float x = uc == 0 ? L : 0f;
                    Vector3 c = P(x, HB, 0), A = P(x, HB + HL * Mathf.Sin(p0), a * Mathf.Cos(p0)), B = P(x, HB + HL * Mathf.Sin(p1), a * Mathf.Cos(p1));
                    System.Func<float, float, Vector2> f = (z, yy) => new Vector2(uc == 0 ? (a - z) / D : (z + a) / D, yy / H);
                    y.Ucgen(2, c, A, B, f(0, HB), f(a * Mathf.Cos(p0), HB + HL * Mathf.Sin(p0)), f(a * Mathf.Cos(p1), HB + HL * Mathf.Sin(p1)));
                }
            }
            return y.Mesh("SandikKapak");
        }

        public void Dus(Vector3 konum, Vector3 onYonu)
        {
            transform.position = konum;
            onYonu.y = 0f; if (onYonu.sqrMagnitude > 1e-4f) transform.rotation = Quaternion.LookRotation(onYonu.normalized, Vector3.up);
            gameObject.SetActive(true); Ayarla(Durum.Kapali, true);
        }
        public void Ac() { Ayarla(Durum.Acik, false); }
        public void Kapat() { Ayarla(Durum.Kapali, false); }
        public void Kaldir() { gameObject.SetActive(false); }

        public void Ayarla(Durum d, bool hemen)
        {
            hedefAci = d == Durum.Acik ? acikAci : 0f; hedefTon = d == Durum.Acik ? 0f : 1f;
            if (hemen || acilmaSuresi <= 0f) { aci = hedefAci; ton = hedefTon; Uygula(); }
        }

        void Update()
        {
            if (Mathf.Approximately(aci, hedefAci) && Mathf.Approximately(ton, hedefTon)) return;
            float h = Time.deltaTime / Mathf.Max(0.01f, acilmaSuresi);
            aci = Mathf.MoveTowards(aci, hedefAci, acikAci * h); ton = Mathf.MoveTowards(ton, hedefTon, h);
            Uygula();
        }

        void Uygula()
        {
            if (kapak == null) return;
            kapak.localRotation = Quaternion.Euler(-aci, 0f, 0f);       // ust -> arkaya (sol-elli: +x donusu yukariyi one goturur)
            if (mpb == null) mpb = new MaterialPropertyBlock();
            Color c = Color.Lerp(acikTon, Color.white, ton);
            // acikken golgeli yuzler: govde on/arka/uc ve kapak disi/uc
            Ton(gR, 0, c); Ton(gR, 1, c); Ton(gR, 2, c); Ton(gR, 3, Color.white);
            Ton(kR, 0, c); Ton(kR, 1, Color.white); Ton(kR, 2, c);
        }

        void Ton(MeshRenderer r, int i, Color c)
        {
            if (r == null) return;
            r.GetPropertyBlock(mpb, i); mpb.SetColor(RenkId, c); r.SetPropertyBlock(mpb, i);
        }
    }
}

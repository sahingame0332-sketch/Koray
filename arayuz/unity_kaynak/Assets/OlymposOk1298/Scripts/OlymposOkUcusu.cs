// OLYMPOS-KO · tek bir okun ucusu (OlymposOkAtisi olusturur). Uc = nesnenin konumu; dortgen geriye (-X) dogru uzanir.
using UnityEngine;

namespace Olympos.Ok
{
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public class OlymposOkUcusu : MonoBehaviour
    {
        OlymposOkAtisi atis; Transform hedef; Vector3 baslangic; float t, sure;

        public void Kur(OlymposOkAtisi a, Vector3 cikis, Transform h, float uzunluk, float kalinlik)
        {
            atis = a; hedef = h; baslangic = cikis; t = 0f; transform.position = cikis;
            float hy = kalinlik * 0.5f;
            var m = new Mesh(); m.name = "OkDortgen";
            m.vertices = new[] { new Vector3(-uzunluk, -hy, 0), new Vector3(0, -hy, 0), new Vector3(-uzunluk, hy, 0), new Vector3(0, hy, 0) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds();
            GetComponent<MeshFilter>().sharedMesh = m;
            float d = Vector3.Distance(cikis, Varis());
            sure = a.sabitSure ? a.ucusSuresi : d / Mathf.Max(0.01f, a.hiz);
            Yonelt((Varis() - cikis));
        }

        Vector3 Varis() { return hedef != null ? hedef.position + Vector3.up * atis.hedefYuksekligi : transform.position; }

        void Update()
        {
            if (atis == null) { Destroy(gameObject); return; }
            t += Time.deltaTime;
            float p = Mathf.Clamp01(t / Mathf.Max(0.01f, sure));
            Vector3 v = Varis(), onceki = transform.position;
            Vector3 konum = Vector3.Lerp(baslangic, v, p) + Vector3.up * (atis.yayOrani * Vector3.Distance(baslangic, v) * 4f * p * (1f - p));
            transform.position = konum;
            Yonelt(konum - onceki);
            if (p >= 1f) { atis.Vurdu(v, hedef); Destroy(gameObject); }
        }

        void Yonelt(Vector3 yon)
        {
            if (yon.sqrMagnitude < 1e-8f) return;
            var k = atis.kamera != null ? atis.kamera : Camera.main;
            Vector3 x = yon.normalized;
            Vector3 bak = k != null ? (k.transform.position - transform.position) : Vector3.up;
            Vector3 y = Vector3.Cross(bak, x); if (y.sqrMagnitude < 1e-6f) y = Vector3.up; y = y.normalized;
            Vector3 z = Vector3.Cross(x, y);
            transform.rotation = Quaternion.LookRotation(z, y);   // yerel X = ucus yonu, dortgen kameraya bakar
        }
    }
}

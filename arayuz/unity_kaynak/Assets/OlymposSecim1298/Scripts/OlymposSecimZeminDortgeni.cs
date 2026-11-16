// OLYMPOS-KO · yere yatik dortgen (secim halkasi / yon oku icin ortak): XZ duzleminde, pivot noktasi (u, v) dokuda.
// Zemine uydurma: istenirse asagi isin atilir, dortgen zeminin normaline yatirilir (egimli arazide halka yere yapisik kalir).
using UnityEngine;

namespace Olympos.Secim
{
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public abstract class OlymposSecimZeminDortgeni : MonoBehaviour
    {
        [Header("Zemin")]
        [Tooltip("Zemine isin atip normale yatir (Collider gerekir).")]
        public bool zemineUydur = true;
        public LayerMask zeminKatmani = ~0;
        [Tooltip("Z-catismasi olmasin diye zeminden yukseklik (m).")]
        public float zeminPayi = 0.02f;

        protected MeshRenderer mr;

        protected void MeshKur(float genislik, float uzunluk, Vector2 pivot)
        {
            float x0 = -pivot.x * genislik, z0 = -pivot.y * uzunluk;
            var m = new Mesh(); m.name = "SecimZeminDortgeni";
            m.vertices = new[] { new Vector3(x0, 0, z0), new Vector3(x0 + genislik, 0, z0), new Vector3(x0, 0, z0 + uzunluk), new Vector3(x0 + genislik, 0, z0 + uzunluk) };
            m.uv = new[] { new Vector2(0, 0), new Vector2(1, 0), new Vector2(0, 1), new Vector2(1, 1) };
            m.triangles = new[] { 0, 2, 1, 2, 3, 1 };
            m.RecalculateBounds();
            GetComponent<MeshFilter>().sharedMesh = m;
            if (mr == null) mr = GetComponent<MeshRenderer>();
        }

        /// <summary>Nokta ve ileri yonuyle dortgeni zemine yerlestirir.</summary>
        protected void Yerlestir(Vector3 nokta, Vector3 ileri)
        {
            Vector3 normal = Vector3.up, p = nokta;
            if (zemineUydur)
            {
                RaycastHit h;
                if (Physics.Raycast(nokta + Vector3.up * 2f, Vector3.down, out h, 6f, zeminKatmani, QueryTriggerInteraction.Ignore))
                { p = h.point; normal = h.normal; }
            }
            ileri = Vector3.ProjectOnPlane(ileri, normal);
            if (ileri.sqrMagnitude < 1e-6f) ileri = Vector3.ProjectOnPlane(Vector3.forward, normal);
            transform.SetPositionAndRotation(p + normal * zeminPayi, Quaternion.LookRotation(ileri.normalized, normal));
        }

        public void Gizle() { if (mr == null) mr = GetComponent<MeshRenderer>(); if (mr != null) mr.enabled = false; }
        public void Goster() { if (mr == null) mr = GetComponent<MeshRenderer>(); if (mr != null) mr.enabled = true; }
    }
}

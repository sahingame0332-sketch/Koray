// OLYMPOS-KO · legacy UI.Text icin harf araligi (SelectUpgrade paketi). Tek satirli yazilar: her harf sira * aralik kaydirilir.
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/SelectUpgrade/Harf Araligi")]
    [RequireComponent(typeof(Text))]
    public class OlymposSelectUpgradeHarfAraligi : BaseMeshEffect
    {
        public float aralik = 1f;
        void OnValidate() { var g = GetComponent<Text>(); if (g != null) g.SetVerticesDirty(); }
        public override void ModifyMesh(VertexHelper vh)
        {
            if (!IsActive() || aralik == 0f) return;
            var t = GetComponent<Text>(); if (t == null || string.IsNullOrEmpty(t.text)) return;
            string s = t.text; int dortgen = vh.currentVertCount / 4; bool boslukDahil = dortgen >= s.Length;
            float toplam = aralik * (s.Length - 1), hiza = 0f; var a = t.alignment;
            if (a == TextAnchor.UpperCenter || a == TextAnchor.MiddleCenter || a == TextAnchor.LowerCenter) hiza = -toplam * 0.5f;
            else if (a == TextAnchor.UpperRight || a == TextAnchor.MiddleRight || a == TextAnchor.LowerRight) hiza = -toplam;
            var v = new UIVertex(); int q = 0;
            for (int i = 0; i < s.Length && q < dortgen; i++)
            {
                if (!boslukDahil && char.IsWhiteSpace(s[i])) continue;
                float dx = hiza + aralik * i;
                for (int k = 0; k < 4; k++) { int idx = q * 4 + k; vh.PopulateUIVertex(ref v, idx); v.position = new Vector3(v.position.x + dx, v.position.y, v.position.z); vh.SetUIVertex(v, idx); }
                q++;
            }
        }
    }
}

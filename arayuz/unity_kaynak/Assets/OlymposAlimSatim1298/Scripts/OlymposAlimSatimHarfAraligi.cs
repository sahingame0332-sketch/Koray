// OLYMPOS-KO · legacy UI.Text icin harf araligi (orijinal pencerede yazilar ~2 px aralikli: Roboto Slab Bold 25 + 2 px, olculdu).
// Tek satirli, ortali yazilar icindir: her harfin dortgeni sira * aralik kadar kaydirilir, toplam genislik ortalanir.
// Unity 2019.1+ bosluklar icin dortgen uretmez: harf sirasi metinden sayilir, bosluklar atlanir (aralik yine eklenir).
using UnityEngine;
using UnityEngine.UI;

namespace Olympos.UI
{
    [AddComponentMenu("OLYMPOS/1298/Alim Satim/Harf Araligi")]
    [RequireComponent(typeof(Text))]
    public class OlymposAlimSatimHarfAraligi : BaseMeshEffect
    {
        [Tooltip("Harfler arasina eklenen piksel (2712x1220 duzeni). Olculen: 2.")]
        public float aralik = 2f;

        void OnValidate() { var g = GetComponent<Text>(); if (g != null) g.SetVerticesDirty(); }

        public override void ModifyMesh(VertexHelper vh)
        {
            if (!IsActive() || aralik == 0f) return;
            var t = GetComponent<Text>(); if (t == null || string.IsNullOrEmpty(t.text)) return;
            string s = t.text;
            int dortgen = vh.currentVertCount / 4;
            bool boslukDahil = dortgen >= s.Length;
            float toplam = aralik * (s.Length - 1);
            float hiza = 0f;                                      // ortali: -toplam/2, sola yasli: 0, saga yasli: -toplam
            var a = t.alignment;
            if (a == TextAnchor.UpperCenter || a == TextAnchor.MiddleCenter || a == TextAnchor.LowerCenter) hiza = -toplam * 0.5f;
            else if (a == TextAnchor.UpperRight || a == TextAnchor.MiddleRight || a == TextAnchor.LowerRight) hiza = -toplam;
            var v = new UIVertex();
            int q = 0;
            for (int i = 0; i < s.Length && q < dortgen; i++)
            {
                if (!boslukDahil && char.IsWhiteSpace(s[i])) continue;
                float dx = hiza + aralik * i;
                for (int k = 0; k < 4; k++)
                {
                    int idx = q * 4 + k;
                    vh.PopulateUIVertex(ref v, idx);
                    v.position = new Vector3(v.position.x + dx, v.position.y, v.position.z);
                    vh.SetUIVertex(v, idx);
                }
                q++;
            }
        }
    }
}

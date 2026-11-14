// OLYMPOS-KO · neon run halkasinin kenarindaki alcak isik alevleri (silindir) — EKLEMELI. u = cevre, v = yukseklik.
Shader "Olympos/Rune Neon Duvari"
{
    Properties
    {
        _Gurultu ("Gurultu", 2D) = "gray" {}
        _Renk1 ("Renk 1 (mor)", Color) = (0.62, 0.22, 1, 1)
        _Renk2 ("Renk 2 (mavi)", Color) = (0.22, 0.45, 1, 1)
        _Renk3 ("Renk 3 (yesil)", Color) = (0.25, 1, 0.45, 1)
        _Beyaz ("Cekirdek", Color) = (0.9, 0.95, 1, 1)
        _DuvarHiz ("Yukselme hizi", Float) = 1.4
        _TonHiz ("Renk donusu (tur/sn)", Float) = 0.05
        _Guc ("Guc", Range(0, 2)) = 1
        _Zaman ("Zaman", Float) = 0
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Transparent" "IgnoreProjector" = "True" }
        Blend One One
        ZWrite Off
        Cull Off
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            sampler2D _Gurultu; fixed4 _Renk1, _Renk2, _Renk3, _Beyaz; float _DuvarHiz, _TonHiz, _Guc, _Zaman;
            struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; };
            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
            v2f vert (appdata v) { v2f o; o.pos = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; }
            float3 ton(float u, float t)
            {
                float p = frac(u + t * _TonHiz) * 3.0; float f = frac(p); f = f * f * (3.0 - 2.0 * f);
                return p < 1.0 ? lerp(_Renk1.rgb, _Renk2.rgb, f) : (p < 2.0 ? lerp(_Renk2.rgb, _Renk3.rgb, f) : lerp(_Renk3.rgb, _Renk1.rgb, f));
            }
            fixed4 frag (v2f i) : SV_Target
            {
                float h = i.uv.y, t = _Zaman;
                float n  = tex2D(_Gurultu, float2(i.uv.x * 10.0 + 0.13 * sin(t), h * 1.2 - t * _DuvarHiz)).r;
                float n2 = tex2D(_Gurultu, float2(i.uv.x * 23.0, h * 2.5 - t * _DuvarHiz * 1.7)).r;
                float v = saturate(0.55 * n + 0.45 * n2 - h * 0.85 - 0.12) * 3.0 * pow(saturate(1.0 - h), 0.6);
                float3 c = v * ton(i.uv.x, t) + saturate(v - 0.5) * _Beyaz.rgb * 0.6;
                return fixed4(c * _Guc * 0.8, 1);
            }
            ENDCG
        }
    }
}

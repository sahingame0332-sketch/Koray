// OLYMPOS-KO · neon run halkasi (yer dairesi) — EKLEMELI (Blend One One), siyah = etkisiz.
// _Cizgi: R dis cizgi, G ic cizgi, B dis isilti, A ic isilti. Renk aciya gore _Renk1 -> _Renk2 -> _Renk3 (mor/mavi/yesil),
// _TonHiz ile yavasca doner. Formuller arayuz/araclar/rune/kur2.py benzetimiyle ayni.
Shader "Olympos/Rune Neon Halkasi"
{
    Properties
    {
        _Cizgi ("Cizgi (RGBA)", 2D) = "black" {}
        _Gurultu ("Gurultu", 2D) = "gray" {}
        _Renk1 ("Renk 1 (mor)", Color) = (0.62, 0.22, 1, 1)
        _Renk2 ("Renk 2 (mavi)", Color) = (0.22, 0.45, 1, 1)
        _Renk3 ("Renk 3 (yesil)", Color) = (0.25, 1, 0.45, 1)
        _Beyaz ("Cekirdek", Color) = (0.9, 0.95, 1, 1)
        _DisHiz ("Dis donus (tur/sn)", Float) = 0.04
        _IcHiz ("Ic donus (tur/sn)", Float) = -0.064
        _AlevHiz ("Alev hizi", Float) = 1.6
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
        Offset -1, -1
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            sampler2D _Cizgi; sampler2D _Gurultu;
            fixed4 _Renk1, _Renk2, _Renk3, _Beyaz;
            float _DisHiz, _IcHiz, _AlevHiz, _TonHiz, _Guc, _Zaman;
            struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; };
            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
            v2f vert (appdata v) { v2f o; o.pos = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; }
            float gur(float2 p) { return tex2D(_Gurultu, p).r; }
            float2 don(float2 x, float a) { float c = cos(a), s = sin(a); return 0.5 + float2(x.x * c - x.y * s, x.x * s + x.y * c); }
            float3 ton(float a, float t)
            {
                float p = frac(a / 6.2831853 + t * _TonHiz) * 3.0;
                float f = frac(p); f = f * f * (3.0 - 2.0 * f);
                float3 r = p < 1.0 ? lerp(_Renk1.rgb, _Renk2.rgb, f) : (p < 2.0 ? lerp(_Renk2.rgb, _Renk3.rgb, f) : lerp(_Renk3.rgb, _Renk1.rgb, f));
                return r;
            }
            fixed4 frag (v2f i) : SV_Target
            {
                const float TAU = 6.2831853;
                float2 x = i.uv - 0.5;
                float r = length(x) * 2.0, a = atan2(x.y, x.x), t = _Zaman;
                float n = gur(float2(a / TAU * 6.0, r * 1.5 - t * _AlevHiz));
                float buk = (n - 0.5) * 0.006;
                float4 Ld = tex2D(_Cizgi, don(x, t * _DisHiz * TAU) + buk);
                float4 Li = tex2D(_Cizgi, don(x, t * _IcHiz * TAU) + float2(-buk, buk));
                float cizgi = Ld.r + Li.g, isil = Ld.b + Li.a;
                float tit = 0.75 + 0.5 * gur(float2(a / TAU * 3.0 + t * 0.3, t * 0.7));
                float dil = gur(float2(a / TAU * 14.0, r * 2.2 - t * _AlevHiz * 1.3));
                float halka = exp(-pow((r - 0.94) / 0.05, 2)) + 0.6 * exp(-pow((r - 0.60) / 0.05, 2));
                float alev = saturate((dil - 0.40) * 3.4) * halka * tit * 1.3;
                float3 k = ton(a, t);
                float3 c = cizgi * (_Beyaz.rgb * 0.55 + k * 0.6) + isil * k * 0.65 * tit + alev * k + alev * alev * _Beyaz.rgb * 0.35;
                c *= step(r, 1.02) * _Guc;
                return fixed4(c, 1);
            }
            ENDCG
        }
    }
}

// OLYMPOS-KO · alevli run halkasi (yer dairesi) — EKLEMELI (Blend One One), siyah = etkisiz.
// _Cizgi: R dis katman cizgi, G ic katman cizgi, B dis isilti, A ic isilti (lineer doku). _Gurultu: dosenebilir fbm.
// Dis katman _DisHiz, ic katman _IcHiz (tur/sn) ile ters yonde doner; cizgiler kutupsal gurultuyle titrer; dis halkada ve
// heksagram cemberinde disa akan alev dilleri. Parametreler arayuz/araclar/rune/kur.py benzetimiyle ayni.
Shader "Olympos/Rune Ates Halkasi"
{
    Properties
    {
        _Cizgi ("Cizgi (RGBA)", 2D) = "black" {}
        _Gurultu ("Gurultu", 2D) = "gray" {}
        _Cekirdek ("Cekirdek rengi", Color) = (1, 0.78, 0.38, 1)
        _Alev ("Alev rengi", Color) = (1, 0.36, 0.04, 1)
        _Kor ("Kor rengi", Color) = (0.8, 0.08, 0, 1)
        _DisHiz ("Dis donus (tur/sn)", Float) = 0.04
        _IcHiz ("Ic donus (tur/sn)", Float) = -0.064
        _AlevHiz ("Alev hizi", Float) = 1.6
        _Guc ("Guc (0-1, betik surer)", Range(0, 2)) = 1
        _Zaman ("Zaman (betik surer)", Float) = 0
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
            fixed4 _Cekirdek, _Alev, _Kor;
            float _DisHiz, _IcHiz, _AlevHiz, _Guc, _Zaman;
            struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; };
            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
            v2f vert (appdata v) { v2f o; o.pos = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; }
            float gur(float2 p) { return tex2D(_Gurultu, p).r; }
            float2 don(float2 x, float a) { float c = cos(a), s = sin(a); return 0.5 + float2(x.x * c - x.y * s, x.x * s + x.y * c); }
            fixed4 frag (v2f i) : SV_Target
            {
                const float TAU = 6.2831853;
                float2 x = i.uv - 0.5;
                float r = length(x) * 2.0;
                float a = atan2(x.y, x.x);
                float t = _Zaman;
                float n = gur(float2(a / TAU * 6.0, r * 1.5 - t * _AlevHiz));
                float buk = (n - 0.5) * 0.006;
                float4 Ld = tex2D(_Cizgi, don(x, t * _DisHiz * TAU) + buk);
                float4 Li = tex2D(_Cizgi, don(x, t * _IcHiz * TAU) + float2(-buk, buk));
                float cizgi = Ld.r + Li.g;
                float isil = Ld.b + Li.a;
                float tit = 0.75 + 0.5 * gur(float2(a / TAU * 3.0 + t * 0.3, t * 0.7));
                float dil = gur(float2(a / TAU * 14.0, r * 2.2 - t * _AlevHiz * 1.3));
                float halka = exp(-pow((r - 0.93) / 0.05, 2)) + 0.6 * exp(-pow((r - 0.62) / 0.05, 2));
                float alev = saturate((dil - 0.45) * 3.0) * halka * tit;
                float3 c = cizgi * _Cekirdek.rgb * 0.95
                         + isil * _Alev.rgb * 0.55 * tit
                         + alev * (_Alev.rgb * 0.9 + _Kor.rgb * 0.4)
                         + alev * alev * _Cekirdek.rgb * 0.6;
                c *= step(r, 1.02) * _Guc;
                return fixed4(c, 1);
            }
            ENDCG
        }
    }
}

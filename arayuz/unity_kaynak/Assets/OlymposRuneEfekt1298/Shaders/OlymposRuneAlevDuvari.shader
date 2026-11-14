// OLYMPOS-KO · run halkasinin kenarindan yukselen alev duvari (silindir) — EKLEMELI.
// UV: u = cevre (0..1), v = yukseklik (0 taban .. 1 tepe). Iki katman gurultu yukari akar, yukari ciktikca incelir.
Shader "Olympos/Rune Alev Duvari"
{
    Properties
    {
        _Gurultu ("Gurultu", 2D) = "gray" {}
        _Cekirdek ("Cekirdek rengi", Color) = (1, 0.78, 0.38, 1)
        _Alev ("Alev rengi", Color) = (1, 0.36, 0.04, 1)
        _Kor ("Kor rengi", Color) = (0.8, 0.08, 0, 1)
        _DuvarHiz ("Yukselme hizi", Float) = 1.4
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
            sampler2D _Gurultu; fixed4 _Cekirdek, _Alev, _Kor; float _DuvarHiz, _Guc, _Zaman;
            struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; };
            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
            v2f vert (appdata v) { v2f o; o.pos = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; }
            fixed4 frag (v2f i) : SV_Target
            {
                float h = i.uv.y, t = _Zaman;
                float n  = tex2D(_Gurultu, float2(i.uv.x * 10.0 + 0.13 * sin(t), h * 1.2 - t * _DuvarHiz)).r;
                float n2 = tex2D(_Gurultu, float2(i.uv.x * 23.0, h * 2.5 - t * _DuvarHiz * 1.7)).r;
                float v = saturate(0.55 * n + 0.45 * n2 - h * 0.85 - 0.12) * 3.0 * pow(saturate(1.0 - h), 0.6);
                float3 c = v * _Alev.rgb + saturate(v - 0.5) * _Cekirdek.rgb + v * step(0.45, h) * _Kor.rgb * 0.4;
                return fixed4(c * _Guc * 0.8, 1);
            }
            ENDCG
        }
    }
}

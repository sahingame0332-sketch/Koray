// OLYMPOS-KO · 1298 skill efekt shader'i: EKLEMELI (Blend One One) — ates/isik efektleri zemine isik olarak eklenir.
// Efekt kareleri ekran goruntusunden "orijinal - zemin" olarak cikarildi; bu karisimla ayni zemine eklenince orijinal geri gelir.
// Siyah = etkisiz (saydam). _Renk ile ton/siddet, _Parlaklik ile genel guc ayarlanir. Built-in boru hatti; URP'de denenmedi.
Shader "Olympos/Skill Efekt Eklemeli"
{
    Properties
    {
        _MainTex ("Kare", 2D) = "black" {}
        _Renk ("Renk (ton)", Color) = (1, 1, 1, 1)
        _Parlaklik ("Parlaklik", Range(0, 4)) = 1
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Transparent" "IgnoreProjector" = "True" "PreviewType" = "Plane" }
        Blend One One
        ZWrite Off
        Cull Off
        Lighting Off
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _Renk;
            half _Parlaklik;
            struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; };
            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }
            fixed4 frag (v2f i) : SV_Target
            {
                fixed3 c = tex2D(_MainTex, i.uv).rgb * _Renk.rgb * _Parlaklik;
                return fixed4(c, 1);
            }
            ENDCG
        }
    }
}

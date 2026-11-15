// OLYMPOS-KO · karakterin kendine uyguladigi skill efektleri — EKLEMELI (Blend One One), siyah = etkisiz.
// Kareler kayittan "orijinal - efekt oncesi zemin" olarak cikarildi: ayni zemine eklenince orijinal geri gelir.
Shader "Olympos/Kendi Skill Eklemeli"
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
            sampler2D _MainTex; float4 _MainTex_ST; fixed4 _Renk; half _Parlaklik;
            struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; };
            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
            v2f vert (appdata v) { v2f o; o.pos = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _MainTex); return o; }
            fixed4 frag (v2f i) : SV_Target { return fixed4(tex2D(_MainTex, i.uv).rgb * _Renk.rgb * _Parlaklik, 1); }
            ENDCG
        }
    }
}

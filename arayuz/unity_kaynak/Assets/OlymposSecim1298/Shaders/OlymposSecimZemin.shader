// OLYMPOS-KO · secim halkasi / yon oku — yere yatik dortgen, ON-CARPIMLI alfa (Blend One OneMinusSrcAlpha).
// Doku rgb = renk x alfa (kayittan olculdu): halkanin ince mor isimasi alfa 0 ile eklemeli kalir.
// ZTest LEqual + Offset: zemine yapisir, mob ve karakter (opak) ustunde cizilir — kayittaki gibi solucan halkanin onunde.
Shader "Olympos/Secim Zemin"
{
    Properties
    {
        _MainTex ("Doku (on-carpimli)", 2D) = "black" {}
        _Renk ("Renk (ton)", Color) = (1, 1, 1, 1)
        _Parlaklik ("Parlaklik", Range(0, 4)) = 1
    }
    SubShader
    {
        Tags { "Queue" = "Transparent-50" "RenderType" = "Transparent" "IgnoreProjector" = "True" "PreviewType" = "Plane" }
        Blend One OneMinusSrcAlpha
        ZWrite Off
        Cull Off
        Lighting Off
        Offset -1, -1
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
            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 c = tex2D(_MainTex, i.uv);
                c.rgb *= _Renk.rgb * _Parlaklik; c.a *= _Renk.a; c.rgb *= _Renk.a;
                return c;
            }
            ENDCG
        }
    }
}

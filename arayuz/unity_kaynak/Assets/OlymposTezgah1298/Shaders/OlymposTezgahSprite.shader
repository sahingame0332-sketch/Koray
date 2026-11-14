// OLYMPOS-KO · yerdeki merchant tezgahi: alfa karisimli, isiksiz (renk ekran goruntusundeki gibi; sahne isigi tekrar uygulanmaz).
Shader "Olympos/Tezgah Sprite"
{
    Properties { _MainTex ("Tezgah", 2D) = "white" {} _Renk ("Ton", Color) = (1,1,1,1) _Ayna ("Yatay ayna (0/1)", Float) = 0 }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Transparent" "IgnoreProjector" = "True" }
        Blend SrcAlpha OneMinusSrcAlpha
        ZWrite Off
        Cull Off
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            sampler2D _MainTex; fixed4 _Renk; float _Ayna;
            struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; };
            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
            v2f vert (appdata v) { v2f o; o.pos = UnityObjectToClipPos(v.vertex); o.uv = float2(lerp(v.uv.x, 1.0 - v.uv.x, _Ayna), v.uv.y); return o; }
            fixed4 frag (v2f i) : SV_Target { return tex2D(_MainTex, i.uv) * _Renk; }
            ENDCG
        }
    }
}

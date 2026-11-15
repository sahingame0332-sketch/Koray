// OLYMPOS-KO · 3B merchant tezgahi: opak, isiksiz (doku fotograftan; isik ve renk zaten icinde). Yuz basina doku (_MainTex).
Shader "Olympos/Tezgah 3B"
{
    Properties { _MainTex ("Yuz", 2D) = "white" {} _Renk ("Ton", Color) = (1,1,1,1) }
    SubShader
    {
        Tags { "Queue" = "Geometry" "RenderType" = "Opaque" }
        Cull Back
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            sampler2D _MainTex; fixed4 _Renk;
            struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; };
            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
            v2f vert (appdata v) { v2f o; o.pos = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; }
            fixed4 frag (v2f i) : SV_Target { return fixed4(tex2D(_MainTex, i.uv).rgb * _Renk.rgb, 1); }
            ENDCG
        }
    }
}

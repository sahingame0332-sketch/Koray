// OLYMPOS-KO · ok vurusu: ON-CARPIMLI (Blend One OneMinusSrcAlpha). rgb = a*beyaz patlama + eklemeli isik (turuncu isin, pembe duman),
// alfa = beyaz patlamanin ortuculugu. Boylece hem ortucu beyaz patlama hem isik ayni karede, kayittaki gibi.
Shader "Olympos/Ok Vurus"
{
    Properties { _MainTex ("Kare", 2D) = "black" {} _Parlaklik ("Parlaklik", Range(0, 4)) = 1 }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Transparent" "IgnoreProjector" = "True" }
        Blend One OneMinusSrcAlpha
        ZWrite Off Cull Off Lighting Off
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            sampler2D _MainTex; half _Parlaklik;
            struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; };
            struct v2f { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
            v2f vert (appdata v) { v2f o; o.pos = UnityObjectToClipPos(v.vertex); o.uv = v.uv; return o; }
            fixed4 frag (v2f i) : SV_Target { fixed4 c = tex2D(_MainTex, i.uv); c.rgb *= _Parlaklik; return c; }
            ENDCG
        }
    }
}

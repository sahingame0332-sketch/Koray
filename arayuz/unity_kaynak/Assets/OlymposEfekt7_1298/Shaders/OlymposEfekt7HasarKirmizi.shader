// OLYMPOS-KO · efekt 7 hasar kirmizisi — mobun mesh'ine EK malzeme olarak cizilir (iki gecis):
//   olculen (4 karede): tam gucte R = 0.60 L + 162, G = 0.95 L + 5, B = 0.75 L   (L = zemin parlakligi, 0-255)
//   kanal basina yaklasim: hedef = c * dst + b, c = (0.60, 0.95, 0.75), b = (162, 5, 0)/255
//   sonuc = lerp(dst, hedef, s) = dst * (1 - s + s c) + s b      (s = _Guc, kare kare olculen egri)
//   1. gecis carpimsal (Blend DstColor Zero), 2. gecis eklemeli (Blend One One).
Shader "Olympos/Efekt7 Hasar Kirmizi"
{
    Properties
    {
        _Guc ("Guc (s)", Range(0, 1)) = 0
        _Carpan ("Carpan c", Color) = (0.60, 0.95, 0.75, 1)
        _Ekle ("Eklenen b", Color) = (0.635, 0.020, 0, 1)
    }
    SubShader
    {
        Tags { "Queue" = "Geometry+10" "RenderType" = "Opaque" }
        ZWrite Off
        ZTest LEqual
        Offset -1, -1
        CGINCLUDE
        #include "UnityCG.cginc"
        half _Guc; fixed4 _Carpan; fixed4 _Ekle;
        struct appdata { float4 vertex : POSITION; };
        struct v2f { float4 pos : SV_POSITION; };
        v2f vert (appdata v) { v2f o; o.pos = UnityObjectToClipPos(v.vertex); return o; }
        ENDCG
        Pass
        {
            Blend DstColor Zero
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            fixed4 frag (v2f i) : SV_Target { return fixed4(lerp(fixed3(1,1,1), _Carpan.rgb, _Guc), 1); }
            ENDCG
        }
        Pass
        {
            Blend One One
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            fixed4 frag (v2f i) : SV_Target { return fixed4(_Ekle.rgb * _Guc, 1); }
            ENDCG
        }
    }
}

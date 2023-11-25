#version 330 core

uniform vec2 res;
uniform float time;

in vec2 fragCoord;
out vec4 fragColor;

void main() {
    vec2 uv = fragCoord;
    uv -= 0.5;
    uv *= 2.0;
    uv.x *= res.x / res.y;
    
    float d = length(uv);
    time;
    d += time / 7.5;
    d = sin(d * 8.0)/8.0;
    d = abs(d);
        
    d = 0.02 / d;
        
    
    fragColor = vec4(d, d, d, 1.0);
}

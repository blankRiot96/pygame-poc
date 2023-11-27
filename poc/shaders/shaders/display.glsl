#version 330 core

uniform sampler2D tex;

in vec2 fragCoord;
out vec4 fragColor;

void main() {
    if (texture(tex, fragCoord).a == 0.0) { 
        fragColor = vec4(1.0, 1.0, 1.0, 0.0);
        return;
    }
    fragColor = vec4(texture(tex, fragCoord).rgba);
}

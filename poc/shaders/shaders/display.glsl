#version 330 core

uniform sampler2D tex;

in vec2 fragCoord;
out vec4 fragColor;

void main() {
    fragColor = texture(tex, fragCoord);
}

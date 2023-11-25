#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 fragCoord;


void main() {
    fragCoord = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}


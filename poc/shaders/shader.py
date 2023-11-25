import json
from array import array

import moderngl


def load_shader(name: str) -> str:
    with open(f"shaders/{name}.glsl") as f:
        shader = f.read()

    return shader


class Shader:
    """Handles the OpenGL Pipeline"""

    def __init__(self) -> None:
        self.ctx = moderngl.create_context()
        self.load_quad()
        self.load_program()
        self.load_render_obj()

    def load_quad(self):
        with open("shaders/quad.json") as f:
            quad = json.load(f)

        self.quad_buffer = self.ctx.buffer(data=array("f", quad))

    def load_program(self):
        self.program = self.ctx.program(
            vertex_shader=load_shader("vert_shader"),
            fragment_shader=load_shader("frag_shader"),
        )

    def load_render_obj(self):
        self.render_obj = self.ctx.vertex_array(
            self.program, [(self.quad_buffer, "2f 2f", "vert", "texcoord")]
        )

    def safe_assign(self, key: str, value):
        try:
            self.program[key] = value
        except KeyError:
            print(f"WARN: shader not using {key} currently")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.safe_assign(key, value)

    def render(self):
        self.render_obj.render(mode=moderngl.TRIANGLE_STRIP)

import json
import typing as t
from array import array

import moderngl
import pygame


def load_shader(name: str) -> str:
    with open(f"shaders/shaders/{name}.glsl") as f:
        shader = f.read()

    return shader


class Shader:
    """Handles the OpenGL Pipeline"""

    textures_formed = 0

    def __init__(
        self, vert_shader_name: str, frag_shader_name: str, surf_size: tuple[int, int]
    ) -> None:
        self.load_ctx()
        self.load_quad()
        self.load_program(vert_shader_name, frag_shader_name)
        self.load_render_obj()
        self.build_tex(surf_size)
        self.tex_pos: int = 0

    def load_ctx(self):
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)

        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

    def build_tex(self, surf_size: tuple[int, int]) -> moderngl.Texture:
        self.tex = self.ctx.texture(surf_size, 4)
        self.tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.tex.swizzle = "BGRA"
        self.tex_pos = Shader.textures_formed
        self.tex.build_mipmaps()
        Shader.textures_formed += 1

    def pass_surf_to_gl(self, surf: t.Optional[pygame.Surface]):
        if surf is None:
            return

        self.tex.write(surf.get_view("1"))
        self.tex.use(self.tex_pos)
        self.safe_assign("tex", self.tex_pos)

    def load_quad(self):
        with open("shaders/shaders/quad.json") as f:
            quad = json.load(f)

        self.quad_buffer = self.ctx.buffer(data=array("f", quad))

    def load_program(self, vert_shader_name: str, frag_shader_name: str):
        self.program = self.ctx.program(
            vertex_shader=load_shader(vert_shader_name),
            fragment_shader=load_shader(frag_shader_name),
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
        self.ctx.clear()
        self.render_obj.render(mode=moderngl.TRIANGLE_STRIP)
        # self.tex.release()

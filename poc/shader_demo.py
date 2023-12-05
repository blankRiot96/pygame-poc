import pygame
import shared
from shaders.shader import Shader
from shaders.square import Square


class Core:
    WIN_SIZE = (800, 450)

    def __init__(self):
        self.win_init()
        self.shader_init()
        self.square = Square()

    def win_init(self):
        pygame.init()
        pygame.display.set_mode(
            Core.WIN_SIZE, pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
        )
        shared.win = pygame.Surface(Core.WIN_SIZE, pygame.SRCALPHA)
        self.clock = pygame.Clock()

    def shader_init(self):
        self.shader = Shader(vert_shader_name="vert", frag_shader_name="frag")
        self.shader.safe_assign("res", Core.WIN_SIZE)

        self.display_shader = Shader(
            vert_shader_name="vert", frag_shader_name="display"
        )

    def traverse_events(self):
        for event in shared.events:
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.VIDEORESIZE:
                self.shader.safe_assign("res", Core.WIN_SIZE)

    def update(self):
        shared.win = pygame.Surface(Core.WIN_SIZE, pygame.SRCALPHA)
        shared.dt = self.clock.tick(60) / 1000
        shared.events = pygame.event.get()
        shared.keys = pygame.key.get_pressed()

        self.traverse_events()
        pygame.display.set_caption(f"{self.clock.get_fps():.0f}")
        self.shader.update(time=pygame.time.get_ticks() / 1000.0)
        self.display_shader.update()
        self.square.update()

    def render(self):
        self.square.render()
        self.display_shader.pass_surf_to_gl(shared.win)
        self.shader.render()
        self.display_shader.render()

        pygame.display.flip()

    def run(self):
        while True:
            self.update()
            self.render()


def main():
    core = Core()
    core.run()


if __name__ == "__main__":
    main()

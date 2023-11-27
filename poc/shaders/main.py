import pygame
import shared
from shader import Shader

WIN_SIZE = (800, 450)

pygame.init()
pygame.display.set_mode(WIN_SIZE, pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
shared.win = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
clock = pygame.Clock()
ring_shader = Shader(vert_shader_name="vert", frag_shader_name="ring")
ring_shader.safe_assign("res", WIN_SIZE)

# win_shader = Shader(vert_shader_name="vert", frag_shader_name="display")


surf = pygame.Surface((50, 50))
surf.fill("red")
# TODO: Add transparency (blending?)
surf.set_alpha(150)

while True:
    shared.win = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
    shared.dt = clock.tick(60) / 1000
    shared.events = pygame.event.get()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.VIDEORESIZE:
            ring_shader.safe_assign("res", WIN_SIZE)
    pygame.display.set_caption(f"{clock.get_fps():.0f}")

    ring_shader.update(time=pygame.time.get_ticks() / 1000.0)

    shared.win.blit(surf, (50, 50))
    ring_shader.pass_surf_to_gl(shared.win)

    # win_shader.pass_surf_to_gl(shared.win)
    # win_shader.update()

    ring_shader.render()
    # win_shader.render()

    pygame.display.flip()

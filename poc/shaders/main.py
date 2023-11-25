import pygame
import shared
from shader import Shader

WIN_SIZE = (800, 450)

pygame.init()
shared.win = pygame.display.set_mode(
    WIN_SIZE, pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
)
clock = pygame.Clock()
shader = Shader()

shader.safe_assign("res", WIN_SIZE)

while True:
    shared.dt = clock.tick(60) / 1000
    shared.events = pygame.event.get()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.VIDEORESIZE:
            shader.safe_assign("res", WIN_SIZE)

    pygame.display.set_caption(f"{clock.get_fps():.0f}")

    shader.update(time=pygame.time.get_ticks() / 1000.0)

    shared.win.fill("black")
    shader.render()

    pygame.display.flip()

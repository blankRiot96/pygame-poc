import pygame
import shared
from text_effects.manager import EffectManager

pygame.init()
shared.win = pygame.display.set_mode((800, 450))
shared.dt = 0.0
clock = pygame.Clock()


effect = EffectManager()

while True:
    shared.dt = clock.tick(60) / 1000
    shared.events = pygame.event.get()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit
    pygame.display.set_caption(f"{clock.get_fps():.0f}")
    effect.update()

    shared.win.fill("black")
    effect.render()
    pygame.display.update()

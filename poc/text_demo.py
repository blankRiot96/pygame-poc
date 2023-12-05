import pygame
from text_effects.manager import EffectManager

pygame.init()
win = pygame.display.set_mode((800, 450))
dt = 0.0
clock = pygame.Clock()


effect = EffectManager()

while True:
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            raise SystemExit
    pygame.display.set_caption(f"{clock.get_fps():.0f}")
    effect.update()

    win.fill("black")
    effect.render()
    pygame.display.update()

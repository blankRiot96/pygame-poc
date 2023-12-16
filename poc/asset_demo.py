import pygame
import shared
from asset_pipeline.entity import Entity

pygame.init()
shared.win = pygame.display.set_mode((800, 450))
shared.clock = pygame.Clock()

ent = Entity()


while True:
    shared.dt = shared.clock.tick(60) / 1000
    shared.events = pygame.event.get()
    shared.keys = pygame.key.get_pressed()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit

    ent.update()
    pygame.display.set_caption(f"{shared.clock.get_fps():.0f}")

    shared.win.fill("black")
    ent.render()
    pygame.display.update()

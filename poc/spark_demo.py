import pygame
from sparks.spark import SparkSpawner

pygame.init()
win = pygame.display.set_mode((800, 450))
clock = pygame.Clock()

sparks = SparkSpawner()


while True:
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            raise SystemExit

    sparks.update(events, dt)
    pygame.display.set_caption(f"{clock.get_fps():.0f}")

    win.fill("black")
    sparks.draw(win)
    pygame.display.update()

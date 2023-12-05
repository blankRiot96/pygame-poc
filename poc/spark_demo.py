import pygame
import shared
from sparks.spark import SparkSpawner

pygame.init()
shared.win = pygame.display.set_mode((800, 450))
clock = pygame.Clock()

sparks = SparkSpawner()


while True:
    shared.dt = clock.tick(60) / 1000
    shared.events = pygame.event.get()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit

    sparks.update()
    pygame.display.set_caption(f"{clock.get_fps():.0f}")

    shared.win.fill("black")
    sparks.draw()
    pygame.display.update()

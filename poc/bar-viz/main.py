from functools import partial

import pygame
from src import shared
from src.bars import BarVisualizer

pygame.init()
shared.win = pygame.display.set_mode((800, 450))
shared.WRECT = shared.win.get_rect()

shared.dt = 0.0

clock = pygame.Clock()


viz = BarVisualizer(
    size=(shared.WRECT.height, 150),
    bar_width=10,
    bar_space=5,
    update_cd=0.1,
)
viz.set_song(pygame.mixer.Sound("hiding-in-the-dark.mp3"), fade_ms=0)
viz.play()


while True:
    shared.dt = clock.tick(60) / 1000
    shared.events = pygame.event.get()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit

    pygame.display.set_caption(f"{clock.get_fps():.0f}")
    viz.update()

    shared.win.fill("black")
    viz.render(
        ["topleft", "topright"],
        [
            partial(pygame.transform.rotate, angle=-90),
            partial(pygame.transform.rotate, angle=90),
        ],
    )

    pygame.display.update()

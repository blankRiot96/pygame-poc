from functools import partial

import pygame
import shared
from bar_viz.bars import BarVisualizer

pygame.init()
shared.win = pygame.display.set_mode(
    pygame.display.get_desktop_sizes()[0], pygame.NOFRAME
)
shared.WRECT = shared.win.get_rect()

shared.dt = 0.0

shared.clock = pygame.Clock()


viz = BarVisualizer(
    size=(shared.WRECT.height, 150),
    bar_width=10,
    bar_space=5,
    update_cd=0.1,
)
viz.set_song(pygame.mixer.Sound("assets/hiding-in-the-dark.mp3"))
viz.play()


def bottom_left(surf):
    surf = pygame.transform.rotate(surf, angle=90)
    surf = pygame.transform.flip(surf, True, False)

    return surf


def top_right(surf):
    surf = pygame.transform.rotate(surf, angle=-90)
    surf = pygame.transform.flip(surf, True, False)

    return surf


while True:
    shared.dt = shared.clock.tick(60) / 1000
    shared.events = pygame.event.get()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit

    pygame.display.set_caption(f"{shared.clock.get_fps():.0f}")
    viz.update()

    shared.win.fill("black")
    # viz.render(
    #     ["topleft", "bottomleft", "topright", "bottomright"],
    #     [
    #         partial(pygame.transform.rotate, angle=-90),
    #         bottom_left,
    #         top_right,
    #         partial(pygame.transform.rotate, angle=90),
    #     ],
    # )

    viz.render(
        ["topleft", "topright"],
        [
            partial(pygame.transform.rotate, angle=-90),
            partial(pygame.transform.rotate, angle=90),
        ],
    )

    pygame.display.update()

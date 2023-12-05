from functools import partial

import pygame
from bar_viz.bars import BarVisualizer

pygame.init()
win = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0], pygame.NOFRAME)
WRECT = win.get_rect()

dt = 0.0

clock = pygame.Clock()


viz = BarVisualizer(
    size=(WRECT.height, 150),
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
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            raise SystemExit

    pygame.display.set_caption(f"{clock.get_fps():.0f}")
    viz.update()

    win.fill("black")
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

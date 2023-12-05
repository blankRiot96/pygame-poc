from functools import partial

import pygame
import shared
from bar_viz.bars import BarVisualizer
from text_effects.subtitles import Subtitles
from text_effects.text_effects import EffectChain, Open, Reveal, Rotate

pygame.init()
shared.win = pygame.display.set_mode((1100, 630))
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


amv_font_1 = pygame.Font("assets/neofont.ttf", 48)
amv_subs = {
    9.0: ([Reveal], "Have you ever fell apart", amv_font_1),
    10.0: ([Reveal], "Tell me you know what its like", amv_font_1),
}
amv_subtitles = Subtitles(amv_subs, final_sub_offset=1.0)


while True:
    shared.dt = shared.clock.tick(60) / 1000
    shared.events = pygame.event.get()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit

    pygame.display.set_caption(f"{shared.clock.get_fps():.0f}")
    viz.update()
    amv_subtitles.update()

    shared.win.fill("black")
    viz.render(
        ["topleft", "topright"],
        [
            partial(pygame.transform.rotate, angle=-90),
            partial(pygame.transform.rotate, angle=90),
        ],
    )
    amv_subtitles.render()

    pygame.display.update()

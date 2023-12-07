from functools import partial

import pygame
import shared
from bar_viz.bars import BarVisualizer
from text_effects.subtitles import Subtitles
from text_effects.text_effects import Expand, Open, Reveal, Rotate, Wiggle

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


amv_font_1 = pygame.Font("assets/neofont.ttf", 24)
amv_font_2 = pygame.Font("assets/neofont.ttf", 48)
amv_subs = {
    # Intro
    10.0: ([Reveal], "(Have you ever fell apart 💔)", amv_font_1),
    11.0: ([Reveal], "(Tell me you know what its like)", amv_font_1),
    16.0: ([Reveal], "(Hiding in the dark)", amv_font_1),
    17.0: ([Reveal], "(Always looking for the light)", amv_font_1),
    #
    # Starting
    21.4: ([Open, Rotate], "Have You Ever Fell Apart", amv_font_2),
    22.6: ([Expand], "Tell", amv_font_2),
    22.7: ([Expand], "Me", amv_font_2),
    22.8: ([Expand], "You", amv_font_2),
    22.9: ([Expand], "Know", amv_font_2, "yellow"),
    23.0: ([Expand], "What", amv_font_2),
    23.1: ([Expand], "Its", amv_font_2),
    23.2: ([Expand], "Like", amv_font_2),
    # Verse 2
    24.0: ([Wiggle], "Hiding In The Dark", amv_font_2),
    25.1: ([Expand], "Always", amv_font_2),
    25.2: ([Expand], "Looking", amv_font_2),
    25.3: ([Expand], "For", amv_font_2),
    25.4: ([Expand], "The", amv_font_2),
    25.5: ([Expand], "Light", amv_font_2, "yellow"),
    # Verse 3
    26.2: ([Reveal, Open], "I've Been Feeling So Alone", amv_font_2),
    28.0: ([Expand], "I've", amv_font_2),
    28.1: ([Expand], "Been", amv_font_2),
    28.2: ([Expand], "Trapped", amv_font_2, "red"),
    28.3: ([Expand], "In", amv_font_2),
    28.4: ([Expand], "My", amv_font_2),
    28.5: ([Expand], "Mind", amv_font_2),
    29.0: ([Open, Rotate], "And It's All I've Ever", amv_font_2),
    30.0: ([Expand], "Known", amv_font_2),
    30.5: ([Expand], "I've", amv_font_2),
    30.6: ([Expand], "Been", amv_font_2),
    30.7: ([Expand], "Dying", amv_font_2),
    30.8: ([Expand], "Inside", amv_font_2),
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

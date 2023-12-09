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


# viz = BarVisualizer(
#     size=(shared.WRECT.height, 150),
#     bar_width=10,
#     bar_space=5,
#     update_cd=0.1,
# )
# viz.set_song(pygame.mixer.Sound("assets/hiding-in-the-dark.mp3"))
# viz.play()


# def bottom_left(surf):
#     surf = pygame.transform.rotate(surf, angle=90)
#     surf = pygame.transform.flip(surf, True, False)

#     return surf


# def top_right(surf):
#     surf = pygame.transform.rotate(surf, angle=-90)
#     surf = pygame.transform.flip(surf, True, False)

#     return surf


DEBUG_START = 8

pygame.mixer.music.load("assets/hiding-in-the-dark.mp3")
pygame.mixer.music.play(start=DEBUG_START)

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
    24.0: ([Wiggle], "Hiding In The Dark[purple]", amv_font_2),
    25.1: ([Expand], "Always", amv_font_2),
    25.2: ([Expand], "Looking", amv_font_2),
    25.3: ([Expand], "For", amv_font_2),
    25.4: ([Expand], "The", amv_font_2),
    25.5: ([Expand], "Light", amv_font_2, "yellow"),
    # Verse 3
    26.2: ([Reveal, Open], "I've Been Feeling So Alone[red]", amv_font_2),
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
    # Verse 4
    32.0: ([Reveal, Open], "I Don't Know Where To Start", amv_font_2),
    33.4: ([Expand], "I", amv_font_2),
    33.6: ([Expand], "Got", amv_font_2),
    33.7: ([Expand], "Way", amv_font_2),
    33.8: ([Expand], "Too", amv_font_2),
    33.9: ([Expand], "Many", amv_font_2),
    34.0: ([Expand], "Questions", amv_font_2, "red"),
    35.0: ([Reveal, Expand], "Bleadin From My Heart", amv_font_2),
    36.4: ([Expand], "I", amv_font_2),
    36.5: ([Expand], "Can't", amv_font_2),
    36.6: ([Expand], "Handle", amv_font_2),
    36.7: ([Expand], "My", amv_font_2),
    36.8: ([Expand], "Reflection", amv_font_2),
    37.8: ([Reveal, Expand, Rotate], "Feel Like No[orange] One[red]", amv_font_2),
    38.4: ([Expand, Reveal], "T O L D", amv_font_2, "cyan"),
    38.8: ([Expand], "Me", amv_font_2),
    38.9: ([Expand], "To", amv_font_2),
    39.0: ([Expand], "Look", amv_font_2),
    39.1: ([Expand], "In", amv_font_2),
    39.2: ([Expand], "Myself", amv_font_2),
}
amv_subtitles = Subtitles(amv_subs, final_sub_offset=1.0, start_offset=DEBUG_START)


while True:
    shared.dt = shared.clock.tick(60) / 1000
    shared.events = pygame.event.get()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit

    pygame.display.set_caption(f"{shared.clock.get_fps():.0f}")
    # viz.update()
    amv_subtitles.update()

    shared.win.fill("black")
    # viz.render(
    #     ["topleft", "topright"],
    #     [
    #         partial(pygame.transform.rotate, angle=-90),
    #         partial(pygame.transform.rotate, angle=90),
    #     ],
    # )
    amv_subtitles.render()

    pygame.display.update()

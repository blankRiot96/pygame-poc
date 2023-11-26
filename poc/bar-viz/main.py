import numpy as np
import pygame

import shared
from utils import Time

pygame.init()
shared.win = pygame.display.set_mode((800, 450))
clock = pygame.Clock()


SAMPLE_RATE = 48_000

sound = pygame.mixer.Sound("hiding-in-the-dark.mp3")
arr = pygame.sndarray.array(sound)
size = len(arr)
sound.play()


SRECT = shared.win.get_rect()
BAR_WIDTH = 10
BAR_SPACING = 5
N_BARS = SRECT.width / (BAR_WIDTH + BAR_SPACING)
UPDATE_CD = 0.05
timer = Time(UPDATE_CD)


def draw_bars(data):
    if data is None:
        return

    if N_BARS < len(data):
        data = data[:: int(len(data) / N_BARS)]
    # data = data[: int(N_BARS)]
    for i, bar in enumerate(data):
        bar_height = bar[1] * 0.005
        r = pygame.Rect(0, SRECT.height - bar_height, BAR_WIDTH, bar_height)
        r.x = i * (BAR_WIDTH + BAR_SPACING)
        pygame.draw.rect(shared.win, "white", r)


def get_data():
    t = pygame.time.get_ticks() / 1000.0
    start_index = max(0, int(SAMPLE_RATE * (t - shared.dt)))
    end_index = min(
        size,
        int(SAMPLE_RATE * t),
    )

    data = np.abs(arr[start_index:end_index])
    return data


data = None
while True:
    shared.dt = clock.tick(60) / 1000
    shared.events = pygame.event.get()
    for event in shared.events:
        if event.type == pygame.QUIT:
            raise SystemExit

    pygame.display.set_caption(f"{clock.get_fps():.0f}")

    if timer.tick():
        data = get_data()

    shared.win.fill("black")

    draw_bars(data)

    pygame.display.update()

import numpy as np
import pygame
import shared

from .types_ import Size
from .utils import Time, render_at

SAMPLE_RATE = 48_000
pygame.mixer.pre_init(frequency=SAMPLE_RATE)


def tone_down_values(values, max_value):
    current_max = np.amax(values)

    if current_max != 0:
        scaling_factor = max_value / current_max
        toned_down_values = values * scaling_factor
    else:
        toned_down_values = values

    return toned_down_values


class BarVisualizer:
    def __init__(
        self, size: Size, bar_width: int, bar_space: int, update_cd: float
    ) -> None:
        self.size = size
        self.bar_width = bar_width
        self.bar_space = bar_space
        self.update_cd = update_cd

        self.meta_init()
        self.bars_init()

    def meta_init(self):
        self.width, self.height = self.size

        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)
        self.song = None
        self.fade_ms = None
        self.arr = None
        self.arr_size = None
        self.data = None
        self.steps = None

    def bars_init(self):
        self.n_bars = self.width / (self.bar_width + self.bar_space)
        self.timer = Time(self.update_cd)

    def set_song(self, song: pygame.mixer.Sound) -> None:
        self.song = song
        self.arr = tone_down_values(pygame.sndarray.array(self.song), self.height)
        self.arr_size = len(self.arr)

    def play(self, fade_ms: int = 0):
        self.song.play(fade_ms=fade_ms)

    def stop(self):
        self.song.stop()

    def get_data(self):
        t = pygame.time.get_ticks() / 1000.0
        start_index = max(0, int(SAMPLE_RATE * (t - 0.5)))
        end_index = min(
            self.arr_size,
            int(SAMPLE_RATE * (t + 0.5)),
        )

        self.data = np.abs(self.arr[start_index:end_index])
        self.steps = int(len(self.data) / self.n_bars)

        mean = lambda bar: (float(bar[0]) + float(bar[1])) / 2
        self.bar_heights = [mean(bar) for bar in self.data[:: self.steps]]
        self.bar_heights.sort(reverse=True)

    def get_bar_color(self, bar_height: float):
        ratio = bar_height / self.height
        color = (25, 255 * ratio, 150 * (1 - ratio))
        return color

    def create_surf(self):
        if self.data is None:
            return

        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)

        for i, bar_height in enumerate(self.bar_heights):
            bar_height = abs(bar_height)
            r = pygame.Rect(0, self.height - bar_height, self.bar_width, bar_height)
            r.x = i * (self.bar_width + self.bar_space)
            pygame.draw.rect(self.surf, self.get_bar_color(bar_height), r)

            if bar_height > 2:
                self.bar_heights[i] -= (bar_height / self.height) * 3.5
            else:
                self.bar_heights[i] = 2

    def update(self):
        if self.timer.tick():
            self.get_data()
        self.create_surf()

    def render(self, render_anchors: list[str], rotate_funcs: list[callable]):
        for render_anchor, rotate_func in zip(render_anchors, rotate_funcs):
            surf = rotate_func(self.surf)
            render_at(shared.win, surf, render_anchor)

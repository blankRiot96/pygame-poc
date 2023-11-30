import numpy as np
import pygame
from src import shared
from src.types_ import Size
from src.utils import Time, render_at

SAMPLE_RATE = 48_000


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

    def set_song(self, song: pygame.mixer.Sound, fade_ms: int) -> None:
        self.song = song
        self.fade_ms = fade_ms
        self.arr = tone_down_values(pygame.sndarray.array(self.song), self.height)
        self.arr_size = len(self.arr)

    def play(self):
        self.song.play(fade_ms=self.fade_ms)

    def stop(self):
        self.song.stop()

    def get_data(self):
        t = pygame.time.get_ticks() / 1000.0
        start_index = max(0, int(SAMPLE_RATE * (t - shared.dt)))
        end_index = min(
            self.arr_size,
            int(SAMPLE_RATE * t),
        )

        self.data = np.abs(self.arr[start_index:end_index])
        self.steps = int(len(self.data) / self.n_bars)

        mean = lambda bar: (float(bar[0]) + float(bar[1])) / 2
        self.bar_heights = [mean(bar) for bar in self.data[:: self.steps]]

    def create_surf(self):
        if self.data is None:
            return

        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)

        for i, bar_height in enumerate(self.bar_heights):
            r = pygame.Rect(0, self.height - bar_height, self.bar_width, bar_height)
            r.x = i * (self.bar_width + self.bar_space)
            pygame.draw.rect(self.surf, "white", r)

            if bar_height > 2:
                self.bar_heights[i] -= 10
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

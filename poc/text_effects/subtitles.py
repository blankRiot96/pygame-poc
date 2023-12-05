import time

import pygame

from .text_effects import EffectChain
from .utils import render_at


class Subtitles:
    def __init__(self, subs: dict[float, EffectChain]) -> None:
        self.subs = tuple(subs.items())
        self.start = time.perf_counter()
        self.current_index = 0
        self.current_sub = None
        self.get_next_subtitle()

    def get_next_subtitle(self):
        self.next_time = self.subs[self.current_index + 1][0]
        if self.is_over():
            self.current_time, self.current_sub = self.subs[self.current_index]
            effects_queue, text, font = self.current_sub
            self.current_sub = EffectChain(
                effect_queue=effects_queue,
                text=text,
                font=font,
                seconds=self.next_time - self.current_time,
                curve=3,
            )
            self.current_index += 1

    def is_over(self):
        return time.perf_counter() - self.start >= self.next_time

    def update(self):
        self.get_next_subtitle()
        if self.current_sub is None:
            return
        self.current_sub.update()

    def render(self, win: pygame.Surface):
        if self.current_sub is None:
            return
        render_at(win, self.current_sub.get_surf(), "center")

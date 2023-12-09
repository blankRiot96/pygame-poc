import time

import pygame
import shared

from .text_effects import EffectChain
from .utils import render_at


class Subtitles:
    def __init__(
        self,
        subs: dict[float, EffectChain],
        final_sub_offset: float,
        start_offset: float = 0.0,
    ) -> None:
        self.subs = tuple(subs.items())
        self.len_subs = len(self.subs)
        self.final_sub_offset = final_sub_offset
        self.start_offset = start_offset
        self.start = time.perf_counter()
        self.current_index = -1
        self.current_sub = None
        self.get_next_subtitle()

    def is_song_over(self) -> bool:
        return self.current_index >= self.len_subs - 1

    def get_duration(self) -> float:
        return min(self.get_pseudo_next_time() - self.current_time, 1.5)

    def create_next_sub(self) -> None:
        self.current_index += 1
        self.current_time, self.current_sub = self.subs[self.current_index]
        effects_queue, text, font, *color = self.current_sub
        self.current_sub = EffectChain(
            effect_queue=effects_queue,
            text=text,
            font=font,
            seconds=self.get_duration(),
            color=color[0] if color else "white",
        )

    def get_pseudo_next_time(self) -> float:
        try:
            return self.subs[self.current_index + 1][0]
        except IndexError:
            return self.subs[-1][0] + self.final_sub_offset

    def calc_next_time(self) -> None:
        self.next_time = self.get_pseudo_next_time()

    def get_next_subtitle(self):
        self.calc_next_time()
        if self.is_sub_over() and not self.is_song_over():
            self.create_next_sub()

    def is_sub_over(self):
        return (time.perf_counter() - self.start) + self.start_offset >= self.next_time

    def update(self):
        self.get_next_subtitle()
        if self.current_sub is None:
            return
        self.current_sub.update()

    def render(self):
        if self.current_sub is None:
            return
        render_at(shared.win, self.current_sub.get_surf(), "center")

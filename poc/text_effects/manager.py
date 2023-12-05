"""Handles the text effects for this specific PoC"""


import pygame
import shared

from .text_effects import EffectChain, Open, Reveal, Rotate
from .utils import render_at


class EffectManager:
    def __init__(self) -> None:
        self.get_effect()

    def get_effect(self) -> None:
        effects = [Open, Rotate]
        self.current_effect = EffectChain(
            effects,
            text="Hiding in the Dark",
            font=pygame.font.Font("assets/neofont.ttf", 48),
            seconds=2.0,
            curve=3,
        )

    def update(self):
        self.current_effect.update()
        if not self.current_effect.alive:
            self.get_effect()

    def render(self):
        render_at(shared.win, self.current_effect.get_surf(), "center")

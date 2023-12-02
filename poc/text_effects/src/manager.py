"""Handles the text effects for this specific PoC"""

import random

import pygame
from src import shared
from src.text_effects import RotateAndOpen, TextEffect
from src.utils import render_at


class EffectManager:
    EFFECTS: list[TextEffect] = [
        RotateAndOpen,
    ]

    def __init__(self) -> None:
        self.get_effect()

    def get_effect(self) -> None:
        self.current_effect: TextEffect = random.choice(EffectManager.EFFECTS)(
            text="Hiding in the Dark", font=pygame.Font("neofont.ttf", 48), seconds=2.0
        )

    def update(self):
        self.current_effect.update()
        if not self.current_effect.alive:
            self.get_effect()

    def render(self):
        render_at(shared.win, self.current_effect.get_surf(), "center")

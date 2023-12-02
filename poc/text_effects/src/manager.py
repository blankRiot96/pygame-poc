"""Handles the text effects for this specific PoC"""

import random

import pygame
from src.text_effects import RotateAndOpen


class EffectManager:
    EFFECTS = [
        RotateAndOpen,
    ]

    def __init__(self) -> None:
        self.current_effect = random.choice(EffectManager.EFFECTS)(
            text="Hiding in the Dark", font=pygame.Font()
        )

    def update(self):
        self.current_effect.update()

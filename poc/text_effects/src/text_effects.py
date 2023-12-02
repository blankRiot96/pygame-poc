import abc
import math

import pygame


class TextEffect(abc.ABC):
    def __init__(self, text: str, font: pygame.Font, seconds: float) -> None:
        self.text = text
        self.font = font
        self.seconds = seconds
        self.alive = True

    @abc.abstractmethod
    def update(self) -> None:
        if self.seconds <= 0.0:
            self.alive = False

    @abc.abstractmethod
    def get_surf(self) -> pygame.Surface:
        ...


class RotateAndOpen(TextEffect):
    def __init__(self, text: str, font: pygame.Font, seconds: float) -> None:
        super().__init__(text, font, seconds)
        self.original_surf = self.font.render(self.text, True, "white")

        self.max_seconds = self.seconds
        self.max_degrees = 180.0
        self.degrees = self.max_degrees

    def rotate_degrees(self) -> None:
        self.degrees = math.pow(self.seconds / self.max_seconds, 2) * self.max_degrees

    def update(self) -> None:
        super().update()
        self.rotate_degrees()

    def get_surf(self) -> pygame.Surface:
        return pygame.transform.rotate(self.original_surf, self.degrees)

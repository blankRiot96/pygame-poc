import abc

import pygame
from src import shared
from src.utils import render_at


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
        self.original_rect = self.original_surf.get_rect()

        self.max_seconds = self.seconds
        self.seconds_passed = 0.0
        self.max_degrees = 90.0
        self.degrees = self.max_degrees
        self.get_time_ratio()

    def get_time_ratio(self) -> None:
        self.seconds_passed += shared.dt
        self.time_ratio = (self.seconds / self.max_seconds) ** 3

    def rotate_degrees(self) -> None:
        self.seconds -= shared.dt
        self.degrees = self.time_ratio * self.max_degrees

    def update(self) -> None:
        super().update()
        self.get_time_ratio()
        self.rotate_degrees()

    def draw_bars(self, surf, rect) -> None:
        if self.degrees < 1:
            return
        bar = pygame.Surface((5, rect.height))
        bar.fill("white")
        render_at(surf, bar, "topleft")
        render_at(surf, bar, "topright")

    def get_surf(self) -> pygame.Surface:
        width = (1 - self.time_ratio) * self.original_rect.width
        rect = pygame.Rect(0, 0, width, self.original_rect.height)
        rect.center = self.original_rect.center
        surf = self.original_surf.subsurface(rect).copy()
        self.draw_bars(surf, rect)

        return pygame.transform.rotate(surf, self.degrees)

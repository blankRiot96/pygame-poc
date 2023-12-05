import abc
import typing as t

import pygame
import shared

from .utils import render_at


class TextEffect(abc.ABC):
    def __init__(
        self, text: str, font: pygame.Font, seconds: float, curve: int = 2
    ) -> None:
        self.text = text
        self.font = font
        self.seconds = seconds
        self.curve = curve

        self.original_surf = self.font.render(self.text, True, "white")
        self.original_rect = self.original_surf.get_rect()
        self.alive = True
        self.max_seconds = self.seconds
        self.get_time_ratio()

    def get_time_ratio(self) -> None:
        self.seconds -= shared.dt
        self.time_ratio = (self.seconds / self.max_seconds) ** self.curve

    def update(self) -> None:
        self.get_time_ratio()
        if self.seconds <= 0.0:
            self.alive = False

    def get_inst_surf(self) -> pygame.Surface:
        return self.get_surf(self.original_surf)

    @abc.abstractmethod
    def get_surf(self, surf):
        ...


class Reveal(TextEffect):
    def __init__(
        self, text: str, font: pygame.Font, seconds: float, curve: int = 2
    ) -> None:
        super().__init__(text, font, seconds, curve)
        self.alpha = 0

    def update(self) -> None:
        super().update()
        self.alpha = 255 * (1 - self.time_ratio)

    def get_surf(self, surf):
        surf.set_alpha(self.alpha)
        return surf


class Open(TextEffect):
    def draw_bars(self, surf, rect) -> None:
        if self.seconds < 0.2:
            return
        bar = pygame.Surface((5, rect.height))
        bar.fill("white")
        render_at(surf, bar, "topleft")
        render_at(surf, bar, "topright")

    def kyoto_sub(self, surf: pygame.Surface, rect: pygame.Rect) -> pygame.Surface:
        try:
            return surf.subsurface(rect).copy()
        except ValueError:
            return surf

    def get_surf(self, surf: pygame.Surface) -> pygame.Surface:
        width = (1 - self.time_ratio) * self.original_rect.width
        rect = pygame.Rect(0, 0, width, self.original_rect.height)
        rect.center = self.original_rect.center
        surf = self.kyoto_sub(surf, rect)
        self.draw_bars(surf, rect)

        return surf


class Rotate(TextEffect):
    def __init__(
        self, text: str, font: pygame.Font, seconds: float, curve: int = 2
    ) -> None:
        super().__init__(text, font, seconds, curve)
        self.max_degrees = 90.0
        self.degrees = self.max_degrees

    def rotate_degrees(self) -> None:
        self.degrees = self.time_ratio * self.max_degrees

    def update(self) -> None:
        super().update()
        self.rotate_degrees()

    def get_surf(self, surf: pygame.Surface) -> pygame.Surface:
        return pygame.transform.rotate(surf, self.degrees)


class EffectChain:
    """Chains effects

    PRECEDENCY:
    * Open, Reveal
    * Rotate

    Higher precendency effects MUST always come BEFORE Lower precendency effects
    Example:
    - [Open, Rotate] ✅
    - [Rotate, Open] ❌
    """

    def __init__(
        self,
        effect_queue: list[t.Type[TextEffect]],
        text: str,
        font: pygame.font.Font,
        seconds: float,
        curve: int = 2,
    ) -> None:
        self.effects = [Effect(text, font, seconds, curve) for Effect in effect_queue]
        self.alive = True

    def update(self):
        self.alive = all(effect.alive for effect in self.effects)
        for effect in self.effects:
            effect.update()

    def get_surf(self) -> pygame.Surface:
        surf = self.effects[0].get_inst_surf()
        for effect in self.effects[1:]:
            surf = effect.get_surf(surf)

        return surf

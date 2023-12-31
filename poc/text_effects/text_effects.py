import abc
import itertools
import typing as t

import pygame
import shared

from .utils import SinWave, render_at


class TextEffect(abc.ABC):
    def __init__(
        self,
        text: str,
        font: pygame.Font,
        seconds: float,
        color="white",
        curve: int = 2,
    ) -> None:
        self.font = font
        self.seconds = seconds
        self.curve = curve
        self.color = color

        self.parse_text_colors(text)  # Assigns self.text and self.original_surf
        self.original_rect = self.original_surf.get_rect()
        self.alive = True
        self.max_seconds = self.seconds
        self.get_time_ratio()

    def parse_text_colors(self, text: str) -> pygame.Surface:
        uni_colored = self.font.render(text, True, self.color)
        if text.find("[") == -1:
            self.text = text
            self.original_surf = uni_colored
            return
        final_surf = pygame.Surface(uni_colored.get_size(), pygame.SRCALPHA)
        final_text = ""
        acc_width = 0
        words = text.split()
        for i, word in enumerate(words):
            color = self.color
            filtered_text = word
            if word.endswith("]"):
                color = word[word.find("[") + 1 : word.find("]")]

                filtered_text = word[: word.find("[")]
            if i < len(words) - 1:
                filtered_text += " "

            final_text += filtered_text
            word_surf = self.font.render(filtered_text, True, color)
            final_surf.blit(word_surf, (acc_width, 0))
            acc_width += word_surf.get_width()

        self.text = final_text
        wotato = final_surf.get_bounding_rect()
        wotato.width = acc_width
        self.original_surf = final_surf.subsurface(wotato).copy()
        # self.original_surf = final_surf.copy()

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


class Shake(TextEffect):
    def __init__(
        self,
        text: str,
        font: pygame.Font,
        seconds: float,
        color: str = "white",
        curve: int = 2,
    ) -> None:
        ...


class Wiggle(TextEffect):
    def __init__(
        self,
        text: str,
        font: pygame.Font,
        seconds: float,
        color: str = "white",
        curve: int = 2,
    ) -> None:
        super().__init__(text, font, seconds, color, curve)

        self.offset_dir = True
        self.wave = SinWave(0.005)
        self.offset = 0
        self.split_into_letters(self.original_surf)

    def kyoto_sub(
        self, surf: pygame.Surface, rect_data: tuple[int | float, ...]
    ) -> pygame.Surface | None:
        try:
            return surf.subsurface(rect_data).copy()
        except (ValueError, pygame.error):
            return None

    def split_into_letters(self, surf: pygame.Surface) -> None:
        """Splits surf into tiny winy letters"""

        self.letters: list[tuple[float, pygame.Surface]] = []
        acc_width = 0
        for char in self.text:
            letter_width = self.font.render(char, True, "white").get_width()
            letter = self.kyoto_sub(
                surf, (acc_width, 0, letter_width, self.original_rect.height)
            )
            self.letters.append((acc_width, letter))
            acc_width += letter_width

    def get_surf(self, surf):  # noqa
        # surf will not be used because Wiggle is the highest precedency
        # and assumes it will always use `get_inst_surf` and hence
        # the result of `surf` is precalculated using the original surface
        scalene = self.font.get_height() / 16
        offset = self.wave.val() * scalene
        final_surf = pygame.Surface(
            (self.original_rect.width, self.original_rect.height + (2 * self.offset)),
            pygame.SRCALPHA,
        )

        self.offset_dir = abs(self.offset_dir)
        for x, letter in self.letters:
            if self.offset_dir:
                offset = (self.offset_dir - self.wave.val()) * scalene
            else:
                offset = self.wave.val() * scalene
            self.offset_dir = not self.offset_dir
            if letter is None:
                continue
            rect = pygame.FRect(x, 0, *letter.get_size())
            rect.centery = self.original_rect.centery + offset
            final_surf.blit(letter, rect)

        return final_surf


class Expand(TextEffect):
    def __init__(
        self,
        text: str,
        font: pygame.Font,
        seconds: float,
        color: str = "white",
        curve: int = 2,
    ) -> None:
        super().__init__(text, font, seconds, color, curve)
        self.width = 0
        self.height = 0

    def get_surf(self, surf):
        try:
            return pygame.transform.scale_by(surf, 1 - self.time_ratio)
        except ValueError:
            return pygame.transform.scale_by(surf, 0)


class Reveal(TextEffect):
    def __init__(
        self,
        text: str,
        font: pygame.Font,
        seconds: float,
        color: str = "white",
        curve: int = 2,
    ) -> None:
        super().__init__(text, font, seconds, color, curve)
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
        except (pygame.error, ValueError):
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
        self,
        text: str,
        font: pygame.Font,
        seconds: float,
        color: str = "white",
        curve: int = 2,
    ) -> None:
        super().__init__(text, font, seconds, color, curve)
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
    * Wiggle
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
        color: str = "white",
        curve: int = 2,
    ) -> None:
        self.text = text
        self.effects = [
            Effect(text, font, seconds, color, curve) for Effect in effect_queue
        ]
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

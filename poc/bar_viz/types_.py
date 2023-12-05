import typing as t

import pygame

Pos: t.TypeAlias = t.Sequence[float] | pygame.Vector2
Size: t.TypeAlias = t.Sequence[float]
Events: t.TypeAlias = list[pygame.Event]
ColorValue: t.TypeAlias = (
    pygame.Color | str | tuple[int, int, int] | tuple[int, int, int, int]
)

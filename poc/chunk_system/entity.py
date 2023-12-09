import pygame
import shared

from .common import TILE_SIDE, TILE_SIZE
from .types_ import Cell


class Entity:
    def __init__(self, cell: Cell) -> None:
        self.cell = cell
        self.pos = pygame.Vector2(self.cell) * TILE_SIDE
        self.surf = pygame.Surface(TILE_SIZE)
        self.surf.fill("red")
        self.rect = self.surf.get_rect(topleft=self.pos)

    def update(self) -> None:
        ...

    def render(self) -> None:
        shared.win.blit(self.surf, self.rect)

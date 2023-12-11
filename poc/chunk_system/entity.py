import pygame
import shared

from .common import CHUNK_SIZE, TILE_SIDE, TILE_SIZE
from .types_ import Cell


class Entity:
    def __init__(self, cell: Cell, chunk_pos: Cell) -> None:
        self.cell = cell
        self.chunk_pos = chunk_pos
        self.pos = pygame.Vector2(self.cell) * TILE_SIDE
        ## Setting it to its chunk
        self.pos += pygame.Vector2(self.chunk_pos) * CHUNK_SIZE
        self.surf = pygame.Surface(TILE_SIZE)
        self.surf.fill("white")
        self.rect = self.surf.get_rect(topleft=self.pos)

    def update(self) -> None:
        ...

    def render(self) -> None:
        shared.win.blit(self.surf, self.rect)

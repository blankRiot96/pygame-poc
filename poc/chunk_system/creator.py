"""File for creation of chunks. Sort of PoC specific"""
import pygame
import shared

from .chunks import Chunk
from .common import CHUNK_TILES, TILE_SIDE, TILE_SIZE
from .entity import Entity
from .file_handler import ChunkFilesHandler
from .types_ import Cell


class ChunkCreator:
    """Holds chunks in memory and creates them based on request"""

    def __init__(self) -> None:
        self.file_handler = ChunkFilesHandler()
        self.on_screen_chunks: dict[Cell, Chunk] = {}
        self.mx, self.my = 0, 0

    def _gen_center_chunk(self) -> None:
        """Assigns `self.center_chunk` based on some camera calculations."""

    def place_entity(self, entity: Entity):
        """Placing a entity to its respective chunk based on game coordinates"""

        chunk = self._get_chunk(entity)
        chunk.set_entity(entity)

    def remove_entity(self, entity: Entity) -> None:
        """Remove an entity from chunk system"""

        chunk = self._get_chunk(entity)
        chunk.remove_entity(entity)

    def _get_chunk(self, entity: Entity) -> Chunk:
        """Internal function for creating a chunk when an entity is placed to an
        empty chunk"""

        chunk = self.on_screen_chunks.get(entity.chunk_pos)
        if chunk is None:
            chunk = Chunk(entity.chunk_pos)
            self.on_screen_chunks[entity.chunk_pos] = chunk

        return chunk

    @staticmethod
    def check_clicked() -> bool:
        for event in shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

        return False

    def check_entity_exists(self, entity: Entity) -> bool:
        chunk = self._get_chunk(entity)

        return chunk.get_entity(entity.cell) is not None

    def update(self) -> None:
        """Runs every tick of pygame"""

        mx, my = shared.mouse_pos // TILE_SIDE
        self.mx, self.my = mx, my
        chunk_pos = (mx // CHUNK_TILES, my // CHUNK_TILES)
        entity_cell = (mx, my) - (pygame.Vector2(chunk_pos) * CHUNK_TILES)

        chunk_pos = (int(chunk_pos[0]), int(chunk_pos[1]))
        entity_cell = (int(entity_cell[0]), int(entity_cell[1]))

        if ChunkCreator.check_clicked():
            entity = Entity(entity_cell, chunk_pos)
            if self.check_entity_exists(entity):
                self.remove_entity(entity)
            else:
                self.place_entity(entity)

    def render(self) -> None:
        """Render chunks and entities"""

        for chunk in self.on_screen_chunks.values():
            pygame.draw.rect(shared.win, "red", chunk.rect, width=2)
            for entity in chunk.cells.values():
                entity.render()

        pygame.draw.rect(
            shared.win,
            "orange",
            (self.mx * TILE_SIDE, self.my * TILE_SIDE, *TILE_SIZE),
        )

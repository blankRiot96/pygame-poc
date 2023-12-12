"""File for creation of chunks. Sort of PoC specific"""
import math

import pygame
import shared

from .chunks import Chunk
from .common import CHUNK_SIZE, CHUNK_TILES, TILE_SIDE, TILE_SIZE
from .entity import Entity
from .file_handler import ChunkFilesHandler
from .types_ import Cell


class ChunkCreator:
    """Holds chunks in memory and creates them based on request"""

    def __init__(self) -> None:
        self.file_handler = ChunkFilesHandler()
        self.mx, self.my = 0, 0
        self.holding_to_create_entity = True
        self.on_screen_chunks: dict[Cell, Chunk] = {}
        self.prev_center_chunk = (-1, -1)
        self._calc_center_chunk()

    @staticmethod
    def negative_ceil(x: int | float) -> int:
        if x > 0:
            return math.ceil(x + 1)

        return -math.ceil(abs(x) + 1)

    def load_files(self):
        horizontal_limit = ChunkCreator.negative_ceil(
            (shared.WRECT.width / CHUNK_SIZE) / 2
        )
        vertical_limit = ChunkCreator.negative_ceil(
            (shared.WRECT.height / CHUNK_SIZE) / 2
        )

        # horizontal_limit, vertical_limit = self.center_chunk
        self.on_screen_chunks: dict[Cell, Chunk] = {
            chunk.chunk_pos: chunk
            for chunk in self.file_handler.get_surrounding_chunks(
                self.center_chunk,
                horizontal_limit=horizontal_limit,
                vertical_limit=vertical_limit,
            )
        }

    def dump_files(self):
        self.file_handler.write_chunks_to_disk(self.on_screen_chunks.values())

    def on_change_center(self):
        self.dump_files()
        self.load_files()

    def _calc_center_chunk(self) -> None:
        """Assigns `self.center_chunk` based on some camera calculations."""

        centerx = ((shared.WRECT.width / 2) + shared.camera.x) / CHUNK_SIZE
        centery = ((shared.WRECT.height / 2) + shared.camera.y) / CHUNK_SIZE

        self.center_chunk = (int(centerx), int(centery))
        if self.center_chunk != self.prev_center_chunk:
            self.on_change_center()

        self.prev_center_chunk = self.center_chunk

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
    def check_right_click() -> bool:
        for event in shared.events:
            # Check for right-click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                return True

        return False

    @staticmethod
    def check_holding() -> bool:
        # Check for left-click
        return pygame.mouse.get_pressed()[0]

    def check_entity_exists(self, entity: Entity) -> bool:
        chunk = self._get_chunk(entity)
        return chunk.get_entity(entity.cell) is not None

    def on_switch(self) -> None:
        if ChunkCreator.check_right_click():
            self.holding_to_create_entity = not self.holding_to_create_entity

    def on_hold(self, entity_cell: Cell, chunk_pos: Cell) -> None:
        if ChunkCreator.check_holding():
            entity = Entity(entity_cell, chunk_pos)
            if self.check_entity_exists(entity) and not self.holding_to_create_entity:
                self.remove_entity(entity)
            elif self.holding_to_create_entity:
                self.place_entity(entity)

    def update_chunks(self):
        for chunk in tuple(self.on_screen_chunks.values()):
            if chunk.is_empty():
                self.on_screen_chunks.pop(chunk.chunk_pos)

    def update(self) -> None:
        """Runs every tick of pygame"""

        self._calc_center_chunk()
        self.update_chunks()

        mx, my = (shared.mouse_pos + shared.camera) // TILE_SIDE
        self.mx, self.my = mx, my
        chunk_pos = (mx // CHUNK_TILES, my // CHUNK_TILES)
        entity_cell = (mx, my) - (pygame.Vector2(chunk_pos) * CHUNK_TILES)

        chunk_pos = (int(chunk_pos[0]), int(chunk_pos[1]))
        entity_cell = (int(entity_cell[0]), int(entity_cell[1]))

        self.on_switch()
        self.on_hold(entity_cell, chunk_pos)

    def render(self) -> None:
        """Render chunks and entities"""

        for chunk in self.on_screen_chunks.values():
            color = ("white", "yellow")[chunk.chunk_pos == self.center_chunk]
            width = (2, 5)[chunk.chunk_pos == self.center_chunk]
            pygame.draw.rect(
                shared.win, color, chunk.rect.move(*-shared.camera), width=width
            )
            for entity in chunk.cells.values():
                entity.render()

        pygame.draw.rect(
            shared.win,
            ("red", "green")[self.holding_to_create_entity],
            pygame.Rect(self.mx * TILE_SIDE, self.my * TILE_SIDE, *TILE_SIZE).move(
                *-shared.camera
            ),
        )

import os
from pathlib import Path

import pygame
import shared
from chunk_system import common
from chunk_system.entity import Entity
from chunk_system.file_handler import ChunkFilesHandler

pygame.init()
shared.win = pygame.display.set_mode((1100, 650))
shared.WRECT = shared.win.get_rect()
pygame.display.set_caption("Chunk Writer Demo")
clock = pygame.Clock()

# Clearing assets/chunks directory

for dir in Path("assets/chunks").iterdir():
    os.remove(dir)

chunk_handler = ChunkFilesHandler(common.CHUNK_SIZE)
camera_offset = pygame.Vector2()
current_center_cell = (0, 0)

# TODO: Work on writing to chunk system.
while True:
    shared.dt = clock.tick(65) / 1000.0
    shared.events = pygame.event.get()
    shared.mouse_pos = pygame.mouse.get_pos()
    for event in shared.events:
        if event.type == pygame.QUIT:
            chunk_handler.write_chunks_to_disk()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game_mouse_pos = shared.mouse_pos - camera_offset
            mx, my = map(int, game_mouse_pos // (common.CHUNK_SIZE * common.TILE_SIDE))
            hovered_chunk = chunk_handler.get_chunk((mx, my))

            cx, cy = map(int, game_mouse_pos // common.TILE_SIDE)
            cx //= mx
            cy //= my
            hovered_chunk.set_entity((mx, my), Entity((mx + cx, my + cy)))
            print(mx, my)
            print(cx, cy)
            chunk_handler.write_chunks_to_disk()
            chunk_handler.saved_chunky.clear()

    shared.win.fill("black")
    horizontal_limit = shared.WRECT.width // (common.CHUNK_SIZE * common.TILE_SIDE)
    vertical_limit = shared.WRECT.height // (common.CHUNK_SIZE * common.TILE_SIDE)
    # print(horizontal_limit, vertical_limit)

    for chunk in chunk_handler.get_surrounding_chunks(
        current_center_cell, horizontal_limit, vertical_limit
    ):
        if chunk.is_empty():
            continue
        # print(chunk.chunk_pos)
        rect = (
            pygame.Vector2(chunk.chunk_pos) * common.TILE_SIDE,
            pygame.Vector2(common.TILE_SIZE) * common.CHUNK_SIZE,
        )
        pygame.draw.rect(shared.win, "red", rect, width=1)
        for entity in chunk.cells.values():
            entity.render(camera_offset)
    pygame.display.update()

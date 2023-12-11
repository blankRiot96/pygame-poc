import os
from pathlib import Path

import pygame
import shared
from chunk_system.common import CHUNK_SIZE
from chunk_system.creator import ChunkCreator

## Clearing assets/chunks directory

for dir in Path("assets/chunks").iterdir():
    os.remove(dir)

pygame.init()
shared.win = pygame.display.set_mode((CHUNK_SIZE * 6, CHUNK_SIZE * 4))
shared.WRECT = shared.win.get_rect()

clock = pygame.Clock()


creator = ChunkCreator()


while True:
    clock.tick(60)

    shared.events = pygame.event.get()
    shared.mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

    for event in shared.events:
        if event.type == pygame.QUIT:
            creator.file_handler.write_chunks_to_disk(creator.on_screen_chunks.values())
            raise SystemExit

    creator.update()
    shared.win.fill("black")

    creator.render()

    pygame.display.update()

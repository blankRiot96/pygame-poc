import os
from pathlib import Path

import pygame
import shared
from chunk_system.common import CHUNK_SIZE
from chunk_system.creator import ChunkCreator

## Clearing assets/chunks directory
# for dir in Path("assets/chunks").iterdir():
#     os.remove(dir)

pygame.init()
shared.win = pygame.display.set_mode((CHUNK_SIZE * 6, CHUNK_SIZE * 4))
shared.WRECT = shared.win.get_rect()
true_cam = pygame.Vector2()
shared.camera = pygame.Vector2()
cam_speed = 400

clock = pygame.Clock()


creator = ChunkCreator()
scaling_factor = 0.65
font = pygame.Font(None, 32)


while True:
    shared.dt = clock.tick() / 1000.0

    shared.events = pygame.event.get()
    shared.mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) / scaling_factor
    shared.keys = pygame.key.get_pressed()

    for event in shared.events:
        if event.type == pygame.QUIT:
            creator.file_handler.write_chunks_to_disk(creator.on_screen_chunks.values())
            raise SystemExit

    if shared.keys[pygame.K_a]:
        true_cam.x -= cam_speed * shared.dt

    if shared.keys[pygame.K_w]:
        true_cam.y -= cam_speed * shared.dt

    if shared.keys[pygame.K_s]:
        true_cam.y += cam_speed * shared.dt

    if shared.keys[pygame.K_d]:
        true_cam.x += cam_speed * shared.dt

    shared.camera = true_cam / scaling_factor

    creator.update()
    shared.win.fill("black")

    creator.render()

    copium = pygame.transform.scale_by(shared.win, scaling_factor)

    shared.win.fill("black")
    pygame.draw.rect(shared.win, "red", copium.get_rect().inflate(10, 10), width=5)
    shared.win.blit(copium, (0, 0))
    shared.win.blit(
        font.render(
            f"No. of chunks LOADED: {len(creator.on_screen_chunks)}", True, "white"
        ),
        (copium.get_width() + 20, 100),
    )

    pygame.display.update()

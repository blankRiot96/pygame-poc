import pygame
import shared

from .loader import load_image


class Entity:
    def __init__(self) -> None:
        self.image = load_image("box.png")
        self.pos = pygame.Vector2()
        self.speed = 200

    def update(self):
        x, y = 0, 0
        if shared.keys[pygame.K_w]:
            y = -1
        if shared.keys[pygame.K_a]:
            x = -1
        if shared.keys[pygame.K_s]:
            y = 1
        if shared.keys[pygame.K_d]:
            x = 1

        self.pos += pygame.Vector2(x, y) * self.speed * shared.dt

    def render(self):
        shared.win.blit(self.image, self.pos)

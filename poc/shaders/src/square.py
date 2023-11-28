import pygame
from src import shared


class Square:
    def __init__(self) -> None:
        self.surf = pygame.Surface((50, 50))
        self.surf.fill("red")
        self.surf.set_alpha(50)
        self.pos = pygame.Vector2(250, 250)
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
        print(self.pos)

    def render(self):
        shared.win.blit(self.surf, self.pos)

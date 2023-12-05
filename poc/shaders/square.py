import pygame


class Square:
    def __init__(self) -> None:
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.surf.fill("red")
        self.surf.set_alpha(150)
        self.pos = pygame.Vector2(250, 250)
        self.speed = 200

    def update(self, keys, dt):
        x, y = 0, 0
        if keys[pygame.K_w]:
            y = -1
        if keys[pygame.K_a]:
            x = -1
        if keys[pygame.K_s]:
            y = 1
        if keys[pygame.K_d]:
            x = 1

        self.pos += pygame.Vector2(x, y) * self.speed * dt

    def render(self, win):
        win.blit(self.surf, self.pos)

import math
import random

import pygame
import shared
from types_ import ColorValue, Pos

RIGHT_ANGLE = math.pi / 2
COLOR = (200, 200, 170)


def entities_updater(entities: list) -> None:
    for entity in entities[:]:
        entity.update()
        if not entity.alive:
            entities.remove(entity)


def entities_renderer(entities: list) -> None:
    for entity in entities:
        entity.draw()


class Particle:
    def __init__(
        self, pos: Pos, speed: float, radians: float, size: int, color: ColorValue
    ) -> None:
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.radians = radians
        self.size = size
        self.color = color

        self.delta = pygame.Vector2()
        self.alive = True
        self.create_points()

    @classmethod
    def random(cls, pos: pygame.Vector2):
        speed = random.randint(30.0, 60.0)
        radians = random.uniform(0, 2 * math.pi)
        size = 0.5
        return cls(
            pos=pos,
            speed=speed,
            radians=radians,
            size=size,
            color=COLOR,
        )

    def create_points(self):
        self.points = [
            self.pos + self.delta,
            self.pos + self.get_delta(self.radians + RIGHT_ANGLE) * 0.3,
            self.pos - self.delta * 3.5,
            pygame.Vector2(
                self.pos.x + self.get_delta(self.radians - RIGHT_ANGLE).x * 0.3,
                self.pos.y - self.get_delta(self.radians + RIGHT_ANGLE).y * 0.3,
            ),
        ]

    def get_delta(self, radians: float):
        return pygame.Vector2(
            math.cos(radians) * self.speed * self.size,
            math.sin(radians) * self.speed * self.size,
        )

    def on_death(self):
        if self.speed > 0:
            return
        self.alive = False

    def update(self):
        self.delta = self.get_delta(self.radians)
        self.create_points()

        self.speed -= 300 * shared.dt
        self.pos += self.delta
        self.on_death()

    def draw(self):
        pygame.draw.polygon(shared.win, self.color, self.points)


class Spark:
    def __init__(self, center_pos: Pos, density: int) -> None:
        self.density = density
        self.particles: Particle = [Particle.random(center_pos) for _ in range(density)]
        self.alive = True

    def update(self):
        self.alive = all(particle.alive for particle in self.particles)
        entities_updater(self.particles)

    def draw(self):
        entities_renderer(self.particles)


class ShockWave:
    def __init__(
        self,
        pos: Pos,
        opening_speed: float,
        width: float,
        thinning_speed: float,
        color: ColorValue = COLOR,
    ) -> None:
        self.pos = pos
        self.opening_speed = opening_speed
        self.width = width
        self.thinning_speed = thinning_speed
        self.color = color
        self.radius = 0
        self.alive = True

    def update(self):
        self.alive = self.width > 0
        self.width -= self.thinning_speed
        self.radius += self.opening_speed

        denom_2 = 0.001
        if self.thinning_speed > denom_2:
            self.thinning_speed -= denom_2
        else:
            self.thinning_speed = denom_2

        denominator = 1
        if self.opening_speed > denominator:
            self.opening_speed -= denominator
        else:
            self.opening_speed = denominator

    def draw(self):
        if int(self.width) <= 0:
            return
        pygame.draw.circle(
            shared.win, self.color, self.pos, self.radius, int(self.width)
        )


class SparkSpawner:
    def __init__(self) -> None:
        self.sparks: list[Spark] = []
        self.shockwaves: list[ShockWave] = []

    def spawn(self):
        self.sparks.append(Spark(pygame.mouse.get_pos(), density=15))
        self.shockwaves.append(
            ShockWave(
                pygame.mouse.get_pos(),
                opening_speed=15,
                width=15,
                thinning_speed=0.9,
            )
        )

    def check_spawn(self):
        for event in shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.spawn()

    def update(self):
        self.check_spawn()
        entities_updater(self.shockwaves)
        entities_updater(self.sparks)

    def draw(self):
        entities_renderer(self.shockwaves)
        entities_renderer(self.sparks)

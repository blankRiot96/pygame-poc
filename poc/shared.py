import pygame

# Constants
WRECT: pygame.Rect

# Shared variables
win: pygame.Surface
events: list[pygame.Event]
keys: list[bool]
dt: float
camera: pygame.Vector2
mouse_pos: pygame.Vector2

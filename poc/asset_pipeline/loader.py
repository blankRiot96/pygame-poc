from functools import lru_cache
from pathlib import Path

import pygame

from .common import IMAGES_PATH, SOUND_PATH


def _find_file_path(file_name: str, directory: Path, pattern: str) -> Path:
    for file in directory.rglob(pattern):
        if file.name == file_name:
            return file

    raise FileNotFoundError(f"{file_name} does not exist in the {directory} directory")


@lru_cache
def load_image(file_name: str) -> pygame.Surface:
    """
    Loads an image from the disk and caches it.

    Attributes
    ----------
    file_name: Represents the name of the file. No need for the exact path. Searches
    that recursively.
    """

    file_path = _find_file_path(file_name, IMAGES_PATH, "*")
    raw_surface = pygame.image.load(file_path)
    alpha = raw_surface.get_alpha()

    if alpha is None:
        return raw_surface.convert()

    return raw_surface.convert_alpha()


@lru_cache
def load_sound(file_name: str) -> pygame.mixer.Sound:
    """
    Loads a sound file from the disk and caches it.

    Attributes
    ----------
    file_name: Represents the name of the file. No need for the exact path. Searches
    that recursively.
    """

    file_path = _find_file_path(file_name, SOUND_PATH, "*")
    return pygame.mixer.Sound(file_path)

from .chunks import Chunk


class Matrix:
    """Matrix object that goes well with chunk systems"""

    def __init__(self, chunk_size: int) -> None:
        self.chunk_size = chunk_size
        self.chunks: list[Chunk] = []

    def get_chunk(self, row: int, col: int) -> Chunk:
        ...

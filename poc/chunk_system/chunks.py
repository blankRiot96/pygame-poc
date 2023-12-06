from .types_ import Cell


class Chunk:
    """A chunk that contains cells"""

    def __init__(self, size: int, matrix_pos: Cell) -> None:
        self.size = size
        self.matrix_pos = matrix_pos
        self.cells: list[Cell] = []

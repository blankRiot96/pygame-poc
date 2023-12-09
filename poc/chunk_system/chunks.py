from .entity import Entity
from .types_ import Cell


class Chunk:
    """A chunk that contains cells"""

    def __init__(self, size: int, chunk_pos: Cell) -> None:
        """
        size: No. of rows and columns
        matrix_pos: The cell coordinate corressponding to this chunk's location in the
        matrix
        """
        self.size = size
        self.chunk_pos = chunk_pos
        self.cells: dict[Cell, Entity | None] = {}

    def get_entity(self, cell: Cell) -> Entity | None:
        return self.cells.get(cell)

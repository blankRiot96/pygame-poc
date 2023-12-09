import inspect
import pickle
import typing as t
from functools import partial

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
        self.cells: dict[Cell, Entity] = {}

    @classmethod
    def from_partial_data(
        cls, chunk_size, chunk_pos, cells: dict[Cell, Entity]
    ) -> t.Self:
        chunk = Chunk(chunk_size, chunk_pos)
        chunk.cells = {cell: PartialEntity() for cell, PartialEntity in cells.items()}

        return chunk

    def get_entity_args(self, entity: Entity) -> tuple:
        return tuple(getattr(entity, arg) for arg in inspect.getargs(entity.__init__))

    def write_to_disk(self) -> None:
        serializable_chunk_data = {
            cell: partial(Entity, self.get_entity_args(entity))
            for cell, entity in self.cells.items()
        }

        with open(f"assets/chunks/{self.chunk_pos}.dat", "wb") as f:
            pickle.dump(serializable_chunk_data, f)

    def is_empty(self) -> bool:
        """Checks if a chunk is empty"""

        return not self.cells

    def get_entity(self, cell: Cell) -> Entity | None:
        return self.cells.get(cell)

    def set_entity(self, cell: Cell, entity: Entity) -> None:
        self.cells[cell] = entity

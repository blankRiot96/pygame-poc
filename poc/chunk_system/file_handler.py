import pickle
import typing as t
from pathlib import Path

from .chunks import Chunk
from .common import CHUNK_TILES
from .types_ import Cell

# Arg types for the get_surrounding_chunks method
GetChunkArgs: t.TypeAlias = tuple[Cell, int, int]


class ChunkFilesHandler:
    """
    saved_chunk_group: A single group of chunks that are saved corressponding to the
    given chunk_pos, horiontal_limit and vertical_limit values
    """

    def __init__(self) -> None:
        self.saved_chunk_group: dict[GetChunkArgs, list[Chunk]] = {}

    def load_chunk_from_disk(self, path: Path) -> Chunk:
        """Loads a particular chunk from the disk"""

        with open(path, "rb") as f:
            return pickle.load(f)

    def write_chunks_to_disk(self, chunk_group: list[Chunk]) -> None:
        """Writes the saved chunkys to the disk"""

        for chunk in chunk_group:
            if chunk.is_empty():
                continue

            chunk.write_to_disk()

    def _get_chunk(self, chunk_pos: Cell) -> Chunk:
        """Internal function to get a particular chunk. Not meant to be used by user
        as it is quite the expensive operation"""
        possible_chunk_file_path = Path(f"assets/chunks/{chunk_pos}.dat")
        if possible_chunk_file_path.exists():
            return Chunk.from_partial_data(
                CHUNK_TILES,
                chunk_pos,
                self.load_chunk_from_disk(possible_chunk_file_path),
            )

        return Chunk(CHUNK_TILES, chunk_pos)

    def get_surrounding_chunks(
        self, chunk_pos: Cell, horizontal_limit: int, vertical_limit: int
    ) -> list[Chunk]:
        """
        horizontal_limit: The number of chunks to scan horizontally around the given
        chunk
        vertical_limit: The number of chunks to scan vertically around the given chunk

        returns: List of available/surrounding chunks. If there was no chunk
        surrounding the given chunk in a particular cell coordinate, then it returns
        an empty Chunk.
        """

        args = (chunk_pos, horizontal_limit, vertical_limit)
        if self.saved_chunk_group.get(args) is not None:
            return self.saved_chunk_group.get(args)
        else:
            self.saved_chunk_group.clear()

        chunks = []
        for x_offset in range(-horizontal_limit, horizontal_limit + 1):
            for y_offset in range(-vertical_limit, vertical_limit + 1):
                surrounding_chunk = (chunk_pos[0] + x_offset, chunk_pos[1] + y_offset)
                chunks.append(self._get_chunk(surrounding_chunk))

        self.saved_chunk_group[args] = chunks
        return chunks

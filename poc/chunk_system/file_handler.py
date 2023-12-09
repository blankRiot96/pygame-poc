import pickle
import typing as t
from pathlib import Path

from .chunks import Chunk
from .types_ import Cell

# Arg types for the get_surrounding_chunks method
GetChunkArgs: t.TypeAlias = tuple[Cell, int, int]


class ChunkFilesHandler:
    """
    saved_chunky: A single group of chunks that are saved corressponding to the given
    chunk_pos, horiontal_limit and vertical_limit values
    """

    def __init__(self, chunk_size: int) -> None:
        self.chunk_size = chunk_size
        self.saved_chunky: dict[GetChunkArgs, list[Chunk]] = {}

    def load_chunk_from_disk(self, path: Path) -> Chunk:
        """Loads a particular chunk from the disk"""

        return pickle.load(path)

    def get_chunk(self, chunk_pos: Cell) -> Chunk:
        possible_chunk_file_path = Path(f"assets/chunks/{chunk_pos}.dat")
        if possible_chunk_file_path.exists():
            return self.load_chunk_from_disk(possible_chunk_file_path)

        return Chunk(self.chunk_size, chunk_pos)

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
        if self.saved_chunky.get(args) is not None:
            print("LOADING SAME CHUNKS")
            return self.saved_chunky.get(args)

        chunks = []
        for x_offset in range(-horizontal_limit, horizontal_limit + 1):
            for y_offset in range(-vertical_limit, vertical_limit + 1):
                surrounding_chunk = (chunk_pos[0] + x_offset, chunk_pos[1] + y_offset)
                chunks.append(self.get_chunk(surrounding_chunk))

        self.saved_chunky[args] = chunks
        return chunks

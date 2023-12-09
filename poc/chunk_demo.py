from chunk_system.file_handler import ChunkFilesHandler

mat = ChunkFilesHandler(6)

chunks = mat.get_surrounding_chunks((0, 0), 1, 1)
chunks = mat.get_surrounding_chunks((0, 0), 1, 1)

for chunk in chunks:
    print(chunk.chunk_pos)

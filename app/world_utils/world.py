from app.settings import *
from app.meshes.chunks.chunk import Chunk
from app.graphics.voxel_handler import VoxelHandler

class World:
    """
    Represents the world containing chunks and manages their generation and rendering.

    Attributes:
        app: Main game instance
        chunks (list): List containing chunk instances representing the world
        voxels (numpy.ndarray): 2D array storing voxel data for each chunk
        voxel_handler (VoxelHandler): Instance of VoxelHandler for handling voxel interactions
    """

    def __init__(self, app):
        """
        Initializes the World instance.

        Args:
            app: The main game instance
        """

        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = numpy.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)

    def build_chunks(self):
        """
        Generates chunk instances and populates the world with them.
        """

        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                for z in range(WORLD_DEPTH):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_WIDTH * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # Put the chunk voxels into a separate array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # Get pointer to voxels
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        """
        Builds meshes for all chunks in the world.
        """
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        """
        Updates the voxel handler for interaction processing.
        """
        self.voxel_handler.update()

    def render(self):
        """
        Renders all chunks in the world.
        """
        for chunk in self.chunks:
            chunk.render()


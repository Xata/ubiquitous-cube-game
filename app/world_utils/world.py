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
        Renders all chunks using two-pass rendering for proper transparency.

        WHY TWO PASSES?
        - Transparent water needs depth testing but shouldn't write to depth buffer
        - This prevents water from blocking geometry behind it incorrectly
        - Solid blocks render first (with depth write), then water (depth test only)
        """
        # PASS 1: Render all solid blocks (writes to depth buffer)
        for chunk in self.chunks:
            chunk.render()

        # PASS 2: Render all transparent blocks (reads depth buffer, doesn't write to it)
        self.app.ctx.depth_mask = False  # Disable depth writes
        for chunk in self.chunks:
            chunk.render_transparent()
        self.app.ctx.depth_mask = True  # Re-enable depth writes

    def get_voxel_id(self, voxel_world_pos):
        """
        Gets the voxel ID at a given world position.

        Args:
            voxel_world_pos (tuple): World position (x, y, z)

        Returns:
            int: Voxel ID at the position, or 0 if out of bounds
        """
        cx, cy, cz = voxel_world_pos // CHUNK_SIZE

        if 0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH:
            chunk_index = cx + WORLD_WIDTH * cz + WORLD_AREA * cy
            lx, ly, lz = voxel_world_pos % CHUNK_SIZE
            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            return self.voxels[chunk_index][voxel_index]
        return 0

    def is_solid_voxel(self, position):
        """
        Checks if a voxel blocks player movement (for collision detection).

        Args:
            position (glm.vec3): World position to check

        Returns:
            bool: True if solid (blocks movement), False if passable

        IMPORTANT: Water (ID 16) is NOT solid - player can move through it!
        """
        voxel_pos = glm.ivec3(glm.floor(position))  # Use floor for negative coords
        voxel_id = self.get_voxel_id(voxel_pos)
        # Solid = any block except void (0) and water (16)
        return voxel_id != 0 and voxel_id != 16

    def is_water_voxel(self, position):
        """
        Checks if a voxel at a given position is water (voxel_id == 16).

        Args:
            position (glm.vec3): World position to check

        Returns:
            bool: True if voxel is water, False otherwise
        """
        voxel_pos = glm.ivec3(glm.floor(position))
        return self.get_voxel_id(voxel_pos) == 16


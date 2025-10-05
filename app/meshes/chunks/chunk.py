from app.settings import *
from .chunk_mesh import *
import app.world_utils.terrain_gen as terrain_gen

class Chunk:
    """
    Represents a chunk inside the world.

    Attributes:
        app: The game object
        world: World object that the chunk belongs to
        position: Position of the chunk in the world
        m_model: Model matrix of the chunk
        voxels: Array representing the voxels in the chunk
        mesh: Mesh associated with the chunk
        is_empty: Flag indicating if the chunk is empty
        center: Center position of the chunk
        is_on_frustum: A function to check if the chunk is within the camera frustum
    """

    def __init__(self, world, position):
        """
        Initializes a Chunk object within the given world and position.

        Args:
            world: World object
            position: Position of the chunk within the world
        """
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: numpy.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True

        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on__frustum = self.app.player.frustum.is_on_frustum

    def get_model_matrix(self):
        """
        Generates the model matrix for the chunk and returns it as m_model

        Returns:
            glm.mat4: Model matrix.
        """
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        """
        Sets the uniform values for rendering the chunk.
        """
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        """
        Builds the chunk mesh.
        """
        self.mesh = ChunkMesh(self)

    def render(self):
        """
        Render solid geometry of the chunk.
        """
        if not self.is_empty and self.is_on__frustum(self):
            self.set_uniform()
            self.mesh.render()

    def render_transparent(self):
        """
        Render transparent geometry (water) of the chunk.
        """
        if not self.is_empty and self.is_on__frustum(self):
            self.set_uniform()
            self.mesh.render_transparent()

    def build_voxels(self):
        """
        Builds the voxels for the chunk.

        Returns:
            numpy.array: A Numpy array representing the voxels in the chunk
        """

        # Empty Chunk
        # uint8 means the voxel ID can be from 0 to 255
        # 0 = empty space
        voxels = numpy.zeros(CHUNK_VOL, dtype='uint8')

        # Fill Chunk
        cx, cy, cz = glm.vec3(self.position) * CHUNK_SIZE
        self.generate_terrain(voxels, cx, cy, cz)

        if numpy.any(voxels):
            self.is_empty = False

        return voxels

    @staticmethod
    @njit  # Numba JIT compilation for performance (REQUIRED - don't remove!)
    def generate_terrain(voxels, cx, cy, cz):
        """
        Fills this chunk with terrain blocks using noise-based generation.

        Args:
            voxels: Flat uint8 array to fill (size CHUNK_VOL = 32*32*32)
            cx, cy, cz: Chunk position in world (chunk coords, not voxel coords)

        HOW IT WORKS:
        1. For each XZ column, calculate terrain height using noise
        2. Fill blocks below terrain height with stone/dirt/grass/etc
        3. Fill air gaps below WATER_LVL (32) with water blocks
        """

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                # Convert chunk-local coords to world coords
                wx = x + cx
                wz = z + cz

                # Get terrain height for this column (from noise function)
                world_height = terrain_gen.get_height(wx, wz)

                # Fill each Y level in this column
                for y in range(CHUNK_SIZE):
                    wy = y + cy  # World Y coordinate

                    if wy < world_height:
                        # Below terrain surface - place terrain blocks
                        # (stone, dirt, grass, etc based on height and noise)
                        terrain_gen.set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)
                    elif wy < WATER_LVL:
                        # Above terrain but below sea level - fill with water
                        terrain_gen.set_water(voxels, x, y, z)

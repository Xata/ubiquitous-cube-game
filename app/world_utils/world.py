from app.settings import *
from app.meshes.chunks.chunk import Chunk
from app.graphics.voxel_handler import VoxelHandler

class World:
    """
    Represents the world containing chunks and manages their generation and rendering.
    Supports infinite terrain generation by loading/unloading chunks based on player position.

    Attributes:
        app: Main game instance
        chunks (dict): Dictionary mapping chunk positions (x,y,z) to Chunk instances
        voxel_handler (VoxelHandler): Instance of VoxelHandler for handling voxel interactions
        render_distance: How many chunks to render around the player
    """

    def __init__(self, app):
        """
        Initializes the World instance.

        Args:
            app: The main game instance
        """

        self.app = app
        self.chunks = {}  # Dictionary for infinite world
        self.voxel_handler = VoxelHandler(self)
        self.render_distance = 8  # Load chunks within 8 chunks of player
        self.last_player_chunk = None

        # Build initial chunks around spawn
        self.build_initial_chunks()

    def build_initial_chunks(self):
        """
        Generates initial chunks around spawn position.
        """
        spawn_chunk_x = int(PLAYER_POS.x // CHUNK_SIZE)
        spawn_chunk_z = int(PLAYER_POS.z // CHUNK_SIZE)

        for x in range(spawn_chunk_x - self.render_distance, spawn_chunk_x + self.render_distance):
            for y in range(WORLD_HEIGHT):
                for z in range(spawn_chunk_z - self.render_distance, spawn_chunk_z + self.render_distance):
                    self.load_chunk(x, y, z)

    def load_chunk(self, cx, cy, cz):
        """
        Loads a single chunk at the given chunk coordinates.

        Args:
            cx, cy, cz: Chunk coordinates
        """
        chunk_pos = (cx, cy, cz)

        if chunk_pos not in self.chunks:
            chunk = Chunk(self, position=chunk_pos)
            chunk.voxels = chunk.build_voxels()
            chunk.build_mesh()
            self.chunks[chunk_pos] = chunk

    def unload_chunk(self, cx, cy, cz):
        """
        Unloads a chunk at the given chunk coordinates.

        Args:
            cx, cy, cz: Chunk coordinates
        """
        chunk_pos = (cx, cy, cz)
        if chunk_pos in self.chunks:
            del self.chunks[chunk_pos]

    def update(self):
        """
        Updates the voxel handler and manages chunk loading/unloading.
        """
        self.voxel_handler.update()
        self.update_chunks()

    def update_chunks(self):
        """
        Loads and unloads chunks based on player position.
        """
        player_pos = self.app.player.position
        player_chunk_x = int(player_pos.x // CHUNK_SIZE)
        player_chunk_z = int(player_pos.z // CHUNK_SIZE)
        player_chunk = (player_chunk_x, player_chunk_z)

        # Only update if player moved to a new chunk
        if player_chunk == self.last_player_chunk:
            return

        self.last_player_chunk = player_chunk

        # Load new chunks in render distance
        for x in range(player_chunk_x - self.render_distance, player_chunk_x + self.render_distance + 1):
            for y in range(WORLD_HEIGHT):
                for z in range(player_chunk_z - self.render_distance, player_chunk_z + self.render_distance + 1):
                    # Only load if within circular render distance
                    dist = ((x - player_chunk_x) ** 2 + (z - player_chunk_z) ** 2) ** 0.5
                    if dist <= self.render_distance:
                        self.load_chunk(x, y, z)

        # Unload distant chunks
        chunks_to_unload = []
        for chunk_pos in self.chunks.keys():
            cx, cy, cz = chunk_pos
            dist = ((cx - player_chunk_x) ** 2 + (cz - player_chunk_z) ** 2) ** 0.5
            if dist > self.render_distance + 2:  # Keep 2 extra chunks as buffer
                chunks_to_unload.append(chunk_pos)

        for chunk_pos in chunks_to_unload:
            self.unload_chunk(*chunk_pos)

    def render(self):
        """
        Renders all chunks using two-pass rendering for proper transparency.

        WHY TWO PASSES?
        - Transparent water needs depth testing but shouldn't write to depth buffer
        - This prevents water from blocking geometry behind it incorrectly
        - Solid blocks render first (with depth write), then water (depth test only)
        """
        # PASS 1: Render all solid blocks (writes to depth buffer)
        for chunk in self.chunks.values():
            chunk.render()

        # PASS 2: Render all transparent blocks (reads depth buffer, doesn't write to it)
        self.app.ctx.depth_mask = False  # Disable depth writes
        for chunk in self.chunks.values():
            chunk.render_transparent()
        self.app.ctx.depth_mask = True  # Re-enable depth writes

    def get_voxel_id(self, voxel_world_pos):
        """
        Gets the voxel ID at a given world position.

        Args:
            voxel_world_pos (tuple): World position (x, y, z)

        Returns:
            int: Voxel ID at the position, or 0 if out of bounds or chunk not loaded
        """
        cx, cy, cz = voxel_world_pos // CHUNK_SIZE

        # Check Y bounds only (infinite in X and Z)
        if not (0 <= cy < WORLD_HEIGHT):
            return 0

        chunk_pos = (int(cx), int(cy), int(cz))
        if chunk_pos in self.chunks:
            lx, ly, lz = voxel_world_pos % CHUNK_SIZE
            voxel_index = int(lx) + CHUNK_SIZE * int(lz) + CHUNK_AREA * int(ly)
            return self.chunks[chunk_pos].voxels[voxel_index]
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


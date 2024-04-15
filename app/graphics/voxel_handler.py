from app.settings import *
from app.meshes.chunks.chunk_mesh_builder import get_chunk_index
from app.blocks.block_type import BLOCK_DICT


class VoxelHandler:
    """
    Manages interactions with voxels in the world
    """

    def __init__(self, world):
        """
        Initializes a VoxelHandler object with the given world.

        Args:
            world: World object
        """

        self.app = world.app
        self.chunks = world.chunks

        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_position = None
        self.voxel_world_position = None
        self.voxel_normal = None

        # 0: Remove voxel
        # 1: Place voxel
        self.interaction_mode = 0

        # Default new voxel ID
        self.new_voxel_id = 1

    def add_voxel(self, player_new_voxel_id=1):
        """
        Adds a voxel to the world.
        """

        if self.voxel_id:
            result = self.get_voxel_id(self.voxel_world_position + self.voxel_normal)

            if not result[0]:
                _, voxel_index, _, chunk = result
                if player_new_voxel_id is None:
                    chunk.voxels[voxel_index] = self.new_voxel_id
                    chunk.mesh.rebuild()

                elif player_new_voxel_id is not None:
                    chunk.voxels[voxel_index] = player_new_voxel_id
                    print(BLOCK_DICT.get(player_new_voxel_id))
                    chunk.mesh.rebuild()

                if chunk.is_empty:
                    chunk.is_empty = False

    def rebuild_adj_chunk(self, adj_voxel_pos):
        """
        Rebuilds the mesh of an adjacent chunk.
        """

        index = get_chunk_index(adj_voxel_pos)
        if index != -1:
            self.chunks[index].mesh.rebuild()

    def rebuild_adjacent_chunks(self):
        """
        Rebuilds the meshes of all adjacent chunks.

        """
        lx, ly, lz = self.voxel_local_position
        wx, wy, wz = self.voxel_world_position

        if lx == 0:
            self.rebuild_adj_chunk((wx - 1, wy, wz))
        elif lx == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_adj_chunk((wx, wy - 1, wz))
        elif ly == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_adj_chunk((wx, wy, wz - 1))
        elif lz == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx, wy, wz + 1))

    def set_voxel(self, new_voxel_id=0):
        """
        Sets the interaction mode and performs voxel manipulation accordingly.
        """

        if self.interaction_mode == 1:
            self.add_voxel(new_voxel_id)
        elif self.interaction_mode == 0:
            if self.voxel_id:
                self.chunk.voxels[self.voxel_index] = 0

                self.chunk.mesh.rebuild()
                self.rebuild_adjacent_chunks()

    def switch_mode(self):
        """
        Switches between removal and placement modes.
        """

        self.interaction_mode = not self.interaction_mode
        if self.interaction_mode == 0:
            print("Delete blocks")
        else:
            print("Place blocks")


    def update(self):
        """
        Updates the voxel handler.
        """

        self.raycast()

    def raycast(self):
        """
        Performs ray casting to determine the voxel being interacted with.
        """

        # Start point
        x1, y1, z1 = self.app.player.position
        # End point
        x2, y2, z2 = self.app.player.position + self.app.player.forward * MAX_RAY_DIST

        current_voxel_position = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)
        step_dir = -1

        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):

            result = self.get_voxel_id(voxel_world_position=current_voxel_position)

            if result[0]:
                self.voxel_id, self.voxel_index, self.voxel_local_position, self.chunk = result
                self.voxel_world_position = current_voxel_position

                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True

            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_position.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_position.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_position.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_position.z += dz
                    max_z += delta_z
                    step_dir = 2
        return False

    def get_voxel_by_raycast(self):
        """
        Performs ray casting to determine the voxel being interacted with and returns it
        Warning: This function will return None if nothing is found
        """

        # Start point
        x1, y1, z1 = self.app.player.position

        # End point
        # Modify the max_distance variable to gauge distance
        max_distance = 2
        x2, y2, z2 = self.app.player.position + self.app.player.forward * max_distance

        current_voxel_position = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)
        step_dir = -1

        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):

            result = self.get_voxel_id(voxel_world_position=current_voxel_position)

            if result[0]:
                self.voxel_id, self.voxel_index, self.voxel_local_position, self.chunk = result
                self.voxel_world_position = current_voxel_position

                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return result

            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_position.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_position.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_position.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_position.z += dz
                    max_z += delta_z
                    step_dir = 2

        return None

    def get_voxel_id(self, voxel_world_position):
        """
        Retrieves the ID of the voxel at the given world position.

        Args:
            voxel_world_position: The world position of the voxel

        Returns:
            Tuple: A tuple containing the voxel ID, voxel index, voxel local position, and the chunk object
        """

        cx, cy, cz = chunk_pos = voxel_world_position / CHUNK_SIZE

        if 0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH:
            chunk_index = cx + WORLD_WIDTH * cz + WORLD_AREA * cy
            chunk = self.chunks[chunk_index]

            # Local coordinates
            lx, ly, lz = voxel_local_position = voxel_world_position - chunk_pos * CHUNK_SIZE

            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_position, chunk
        return 0, 0, 0, 0


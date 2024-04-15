from .noise import noise2, noise3
from random import random
from app.settings import *
from app.blocks import block_type


@njit
def get_height(x, z):
    """
    Generate height value for terrain generation at the given coordinates.

    Args:
        x (float): X-coordinate of the point
        z (float): Z-coordinate of the point

    Returns:
        int: Height value at the specified coordinates
    """

    # Amplitude
    a1 = CENTER_Y
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    # Frequency
    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    # Adjust amplitude based on noise
    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

    # Initialize height
    height = 0

    # Sum up noise contributions at different frequencies and amplitudes
    height += noise2(x * f1, z * f1) * a1 + a1
    height += noise2(x * f2, z * f2) * a2 - a2
    height += noise2(x * f4, z * f4) * a4 + a4
    height += noise2(x * f8, z * f8) * a8 - a8

    # Ensure minimum height and offset
    height = max(height,  int(noise2(x * f8, z * f8) + 2))
    height += 20  # Set the minimum height of the terrain

    return int(height)


@njit
def get_index(x, y, z):
    """
    Calculate the index of a voxel inside of a voxel array based on its local position.
    """

    return x + CHUNK_SIZE * z + CHUNK_AREA * y


@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
    """
    Set the voxel ID for terrain generation at the given local voxel coordinates.
    """

    # TODO: Change this to use dictionary from block_type.py
    voxel_id = block_type.VOID

    if wy < world_height - 1:
        # Create caves
        if (noise3(wx * 0.09, wy * 0.09, wz * 0.09) > 0 and
                noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10):
            voxel_id = 0

        # Generate coal ore
        elif (random.random() > 0.027 and random.random() < 0.03) and (wy < world_height - 1 and wy > world_height - 25):
            voxel_id = block_type.COAL_ORE

        # Generate tin ore
        elif (random.random() > 0.0090 and random.random() < 0.0091) and (wy < world_height - 10 and wy > world_height - 20):
            voxel_id = block_type.TIN_ORE

        # Generate copper ore
        elif (random.random() > 0.0091 and random.random() < 0.01) and (wy < world_height - 10 and wy > world_height - 20):
            voxel_id = block_type.COPPER_ORE

        else:
            voxel_id = block_type.STONE

    else:
        rng = int(7 * random.random())
        ry = wy - rng
        if SNOW_LVL <= ry < world_height:
            voxel_id = block_type.SNOW

        elif STONE_LVL <= ry < SNOW_LVL:
            voxel_id = block_type.STONE

        elif DIRT_LVL <= ry < STONE_LVL:
            voxel_id = block_type.DIRT

        elif GRASS_LVL <= ry < DIRT_LVL:
            voxel_id = block_type.GRASS

        else:
            voxel_id = block_type.SAND

    # Setting ID
    voxels[get_index(x, y, z)] = voxel_id

    # Place tree
    if wy < DIRT_LVL:
        place_tree(voxels, x, y, z, voxel_id)

@njit()
def place_tree(voxels, x, y, z, voxel_id):
    """
    Generates a tree at the given location
    """

    rnd = random.random()
    if voxel_id != block_type.GRASS or rnd > TREE_PROBABILITY:
        return None
    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None

    # Dirt under the tree
    voxels[get_index(x, y, z)] = block_type.DIRT

    # Leaves
    m = 0
    for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
        k = iy % 2
        rng = int(random.random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    voxels[get_index(x + ix + k, y + iy, z + iz + k)] = block_type.LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0

    # Tree trunk
    for iy in range(1, TREE_HEIGHT - 2):
        voxels[get_index(x, y + iy, z)] = block_type.WOOD

    # Top
    voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = block_type.LEAVES


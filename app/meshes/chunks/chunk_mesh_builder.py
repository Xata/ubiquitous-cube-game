from app.settings import *
from numba import uint8


@njit
def get_ambient_occlusion_value(local_pos, world_pos, world_voxels, plane):
    """
    Calculates the ambient occlusion value for a given voxel position.

    Args:
        local_pos (tuple): Local position of the voxel within the chunk
        world_pos (tuple): World position of the voxel
        world_voxels (numpy.array): Array containing voxel data for the entire world
        plane (str): Orientation plane of the voxel ('X', 'Y', or 'Z')

    Returns:
        tuple: Ambient occlusion values for adjacent voxels
    """

    x, y, z = local_pos
    wx, wy, wz = world_pos

    if plane == 'Y':
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)
        c = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels)
        g = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)

    elif plane == 'X':
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = a = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)

    # Z plane
    else:
        a = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_voxels)
        e = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)

    ambient_occlusion_value = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ambient_occlusion_value


@njit
def to_uint8(x, y, z, voxel_id, face_id, ao_id, flip_id):
    """
    Converts input values to uint8 data type.

    Args:
        x, y, z, voxel_id, face_id, ao_id, flip_id: Input values

    Returns:
        tuple: Values converted to uint8
    """

    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id), uint8(ao_id), uint8(flip_id)

@njit
def pack_data(x, y, z, voxel_id, face_id, ao_id, flip_id):
    """
    Packs voxel data into a single uint32 value. This increases performance.

    Args:
        x, y, z, voxel_id, face_id, ao_id, flip_id: Input voxel data

    Returns:
        uint32: Packed voxel data
    """

    # x: 6 bit, y: 6 bit, z: 6 bit, voxel_id: 8 bit, face_id: 3 bit, ao_id: 2 bit, flip_id: 1 bit
    a, b, c, d, e, f, g = x, y, z, voxel_id, face_id, ao_id, flip_id

    b_bit, c_bit, d_bit, e_bit, f_bit, g_bit = 6, 6, 8, 3, 2, 1

    # Calculate the length of the bits for the bitwise shift operation
    b_bit, c_bit, d_bit, e_bit, f_bit, g_bit = 6, 6, 8, 3, 2, 1
    fg_bit = f_bit + g_bit
    efg_bit = e_bit + fg_bit
    defg_bit = d_bit + efg_bit
    cdefg_bit = c_bit + defg_bit
    bcdefg_bit = b_bit + cdefg_bit

    packed_data = (
        a << bcdefg_bit |
        b << cdefg_bit |
        c << defg_bit |
        d << efg_bit |
        e << fg_bit |
        f << g_bit | g
    )

    return packed_data

@njit
def get_chunk_index(world_voxel_pos):
    """
    Calculates the index of the chunk containing a given world voxel position.

    Args:
        world_voxel_pos (tuple): World position of the voxel

    Returns:
        int: Index of the chunk containing the voxel
    """
    wx, wy, wz = world_voxel_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH):
        return -1

    index = cx + WORLD_WIDTH * cz + WORLD_AREA * cy
    return index


@njit
def get_voxel_id_at(local_voxel_pos, world_voxel_pos, world_voxels):
    """
    Gets the voxel ID at a given position.

    Args:
        local_voxel_pos (tuple): Local position of the voxel within its chunk
        world_voxel_pos (tuple): World position of the voxel
        world_voxels (numpy.array): Array containing voxel data for the entire world

    Returns:
        int: Voxel ID at the position, or 0 if out of bounds
    """

    chunk_index = get_chunk_index(world_voxel_pos)
    if chunk_index == -1:
        return 0
    chunk_voxels = world_voxels[chunk_index]

    x, y, z = local_voxel_pos
    voxel_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA

    return chunk_voxels[voxel_index]

@njit
def is_void(local_voxel_pos, world_voxel_pos, world_voxels):
    """
    Checks if a voxel position is empty (void) or transparent within the world.

    Args:
        local_voxel_pos (tuple): Local position of the voxel within its chunk
        world_voxel_pos (tuple): World position of the voxel
        world_voxels (numpy.array): Array containing voxel data for the entire world

    Returns:
        bool: True if the voxel position is empty or transparent, False otherwise
    """

    voxel_id = get_voxel_id_at(local_voxel_pos, world_voxel_pos, world_voxels)

    # Empty voxels are void
    if voxel_id == 0:
        return True
    else:
        return False

@njit
def should_render_face(current_voxel_id, neighbor_voxel_id):
    """
    Determines if a face should be rendered between two voxels.

    Args:
        current_voxel_id: ID of the current voxel
        neighbor_voxel_id: ID of the neighboring voxel

    Returns:
        bool: True if face should be rendered
    """

    # Don't render face if both are the same block type
    if current_voxel_id == neighbor_voxel_id:
        return False

    # Always render if neighbor is void (air)
    if neighbor_voxel_id == 0:
        return True

    # Water is transparent - always render faces adjacent to it
    # This includes: water->solid and solid->water
    if current_voxel_id == 16 or neighbor_voxel_id == 16:
        return True

    # Don't render between two different solid blocks
    return False


# @njit
# def add_data(vertex_data, index, *vertices):
#     for vertex in vertices:
#         for attr in vertex:
#             vertex_data[index] = attr
#             index += 1
#     return index

@njit
def add_data(vertex_data, index, *vertices):
    """
    Adds vertex data to a vertex array.

    Args:
        vertex_data (numpy.array): The vertex array
        index (int): Current index in the vertex array
        *vertices: Variable number of vertices to add

    Returns:
        int: Index after adding new vertices
    """

    for vertex in vertices:
        vertex_data[index] = vertex
        index += 1
    return index


@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels):
    """
    Builds the mesh data for a chunk based on its voxel data.
    Returns separate arrays for solid and transparent geometry.

    Args:
        chunk_voxels (numpy.array): Voxel data for the chunk
        format_size (int): Size of the format for vertex data
        chunk_pos (tuple): Position of the chunk
        world_voxels (numpy.array): Voxel data for the entire world

    Returns:
        tuple: (solid_mesh_data, transparent_mesh_data) - Two numpy arrays
    """

    # ARRAY_SIZE = CHUNK_VOL * NUM_VOXEL_VERTICES * VERTEX_ATTRS
    # Maximum number of visible vertices is 18 because each voxel is made up of two triangles
    # The 18 could be called NUMBER_VOXEL_VERTICES
    # Each vertex has at least 5 attributes (this is format_size)
    # 1) x position 2) y position 3) z position 4) voxel_id 5) face_id
    # Change dtype from uint32 to uint8 if using non-packed data!
    solid_data = numpy.empty(CHUNK_VOL * 18 * format_size, dtype='uint32')
    transparent_data = numpy.empty(CHUNK_VOL * 18 * format_size, dtype='uint32')
    solid_index = 0
    transparent_index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue

                # Voxel world position
                cx, cy, cz = chunk_pos
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # Top Face
                neighbor_id = get_voxel_id_at((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
                if should_render_face(voxel_id, neighbor_id):
                    # Get ambient occlusion values
                    ao_id = get_ambient_occlusion_value((x, y + 1, z), (wx, wy + 1, wz), world_voxels, plane='Y')

                    # Fix anisotropy by choosing a consistent orientation for vertices
                    flip_id = ao_id[1] + ao_id[3] > ao_id[0] + ao_id[2]

                    # Format: x, y, z, voxel_id, face_id, ao_id
                    v0 = pack_data(x, y + 1, z, voxel_id, 0, ao_id[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z, voxel_id, 0, ao_id[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 0, ao_id[2], flip_id)
                    v3 = pack_data(x, y + 1, z + 1, voxel_id, 0, ao_id[3], flip_id)

                    if voxel_id == 16:  # Water - transparent
                        if flip_id:
                            transparent_index = add_data(transparent_data, transparent_index, v1, v0, v3, v1, v3, v2)
                        else:
                            transparent_index = add_data(transparent_data, transparent_index, v0, v3, v2, v0, v2, v1)
                    else:  # Solid blocks
                        if flip_id:
                            solid_index = add_data(solid_data, solid_index, v1, v0, v3, v1, v3, v2)
                        else:
                            solid_index = add_data(solid_data, solid_index, v0, v3, v2, v0, v2, v1)

                # Bottom Face
                neighbor_id = get_voxel_id_at((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
                if should_render_face(voxel_id, neighbor_id):
                    # Get ambient occlusion values
                    ao_id = get_ambient_occlusion_value((x, y - 1, z), (wx, wy - 1, wz), world_voxels, plane='Y')

                    flip_id = ao_id[1] + ao_id[3] > ao_id[0] + ao_id[2]

                    v0 = pack_data(x, y, z, voxel_id, 1, ao_id[0], flip_id)
                    v1 = pack_data(x + 1, y, z, voxel_id, 1, ao_id[1], flip_id)
                    v2 = pack_data(x + 1, y, z + 1, voxel_id, 1, ao_id[2], flip_id)
                    v3 = pack_data(x, y, z + 1, voxel_id, 1, ao_id[3], flip_id)

                    if voxel_id == 16:  # Water - transparent
                        if flip_id:
                            transparent_index = add_data(transparent_data, transparent_index, v1, v3, v0, v1, v2, v3)
                        else:
                            transparent_index = add_data(transparent_data, transparent_index, v0, v2, v3, v0, v1, v2)
                    else:  # Solid blocks
                        if flip_id:
                            solid_index = add_data(solid_data, solid_index, v1, v3, v0, v1, v2, v3)
                        else:
                            solid_index = add_data(solid_data, solid_index, v0, v2, v3, v0, v1, v2)

                # Right Face
                neighbor_id = get_voxel_id_at((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
                if should_render_face(voxel_id, neighbor_id):
                    ao_id = get_ambient_occlusion_value((x + 1, y, z), (wx + 1, wy, wz), world_voxels, plane='X')

                    flip_id = ao_id[1] + ao_id[3] > ao_id[0] + ao_id[2]

                    v0 = pack_data(x + 1, y, z, voxel_id, 2, ao_id[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z, voxel_id, 2, ao_id[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 2, ao_id[2], flip_id)
                    v3 = pack_data(x + 1, y, z + 1, voxel_id, 2, ao_id[3], flip_id)

                    if voxel_id == 16:  # Water - transparent
                        if flip_id:
                            transparent_index = add_data(transparent_data, transparent_index, v3, v0, v1, v3, v1, v2)
                        else:
                            transparent_index = add_data(transparent_data, transparent_index, v0, v1, v2, v0, v2, v3)
                    else:  # Solid blocks
                        if flip_id:
                            solid_index = add_data(solid_data, solid_index, v3, v0, v1, v3, v1, v2)
                        else:
                            solid_index = add_data(solid_data, solid_index, v0, v1, v2, v0, v2, v3)

                # Left Face
                neighbor_id = get_voxel_id_at((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
                if should_render_face(voxel_id, neighbor_id):
                    ao_id = get_ambient_occlusion_value((x - 1, y, z), (wx - 1, wy, wz), world_voxels, plane='X')

                    flip_id = ao_id[1] + ao_id[3] > ao_id[0] + ao_id[2]

                    v0 = pack_data(x, y, z, voxel_id, 3, ao_id[0], flip_id)
                    v1 = pack_data(x, y + 1, z, voxel_id, 3, ao_id[1], flip_id)
                    v2 = pack_data(x, y + 1, z + 1, voxel_id, 3, ao_id[2], flip_id)
                    v3 = pack_data(x, y, z + 1, voxel_id, 3, ao_id[3], flip_id)

                    if voxel_id == 16:  # Water - transparent
                        if flip_id:
                            transparent_index = add_data(transparent_data, transparent_index, v3, v1, v0, v3, v2, v1)
                        else:
                            transparent_index = add_data(transparent_data, transparent_index, v0, v2, v1, v0, v3, v2)
                    else:  # Solid blocks
                        if flip_id:
                            solid_index = add_data(solid_data, solid_index, v3, v1, v0, v3, v2, v1)
                        else:
                            solid_index = add_data(solid_data, solid_index, v0, v2, v1, v0, v3, v2)

                # Back Face
                neighbor_id = get_voxel_id_at((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
                if should_render_face(voxel_id, neighbor_id):
                    ao_id = get_ambient_occlusion_value((x, y, z - 1), (wx, wy, wz - 1), world_voxels, plane='Z')

                    flip_id = ao_id[1] + ao_id[3] > ao_id[0] + ao_id[2]

                    v0 = pack_data(x, y, z, voxel_id, 4, ao_id[0], flip_id)
                    v1 = pack_data(x, y + 1, z, voxel_id, 4, ao_id[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z, voxel_id, 4, ao_id[2], flip_id)
                    v3 = pack_data(x + 1, y, z, voxel_id, 4, ao_id[3], flip_id)

                    if voxel_id == 16:  # Water - transparent
                        if flip_id:
                            transparent_index = add_data(transparent_data, transparent_index, v3, v0, v1, v3, v1, v2)
                        else:
                            transparent_index = add_data(transparent_data, transparent_index, v0, v1, v2, v0, v2, v3)
                    else:  # Solid blocks
                        if flip_id:
                            solid_index = add_data(solid_data, solid_index, v3, v0, v1, v3, v1, v2)
                        else:
                            solid_index = add_data(solid_data, solid_index, v0, v1, v2, v0, v2, v3)

                # Front Face
                neighbor_id = get_voxel_id_at((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
                if should_render_face(voxel_id, neighbor_id):
                    ao_id = get_ambient_occlusion_value((x, y, z + 1), (wx, wy, wz + 1), world_voxels, plane='Z')

                    flip_id = ao_id[1] + ao_id[3] > ao_id[0] + ao_id[2]

                    v0 = pack_data(x, y, z + 1, voxel_id, 5, ao_id[0], flip_id)
                    v1 = pack_data(x, y + 1, z + 1, voxel_id, 5, ao_id[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 5, ao_id[2], flip_id)
                    v3 = pack_data(x + 1, y, z + 1, voxel_id, 5, ao_id[3], flip_id)

                    if voxel_id == 16:  # Water - transparent
                        if flip_id:
                            transparent_index = add_data(transparent_data, transparent_index, v3, v1, v0, v3, v2, v1)
                        else:
                            transparent_index = add_data(transparent_data, transparent_index, v0, v2, v1, v0, v3, v2)
                    else:  # Solid blocks
                        if flip_id:
                            solid_index = add_data(solid_data, solid_index, v3, v1, v0, v3, v2, v1)
                        else:
                            solid_index = add_data(solid_data, solid_index, v0, v2, v1, v0, v3, v2)

    return solid_data[:solid_index + 1], transparent_data[:transparent_index + 1]


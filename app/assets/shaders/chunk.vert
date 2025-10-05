#version 330 core

// Input attributes (from a single uint for performance reasons)
layout (location = 0) in uint packed_data; // Packed vertex data containing position, voxel, face, AO, and flip information
int x, y, z;
int ao_id;
int flip_id;

// Uniform matrices
uniform mat4 m_proj; // Projection matrix
uniform mat4 m_view; // View matrix
uniform mat4 m_model; // Model matrix

// Output variables
flat out int voxel_id; // ID of the voxel
flat out int face_id; // ID of the voxel face

out vec3 voxel_color; // Color of the voxel
out vec2 uv; // UV coordinates of the fragment
out float shading; // Shading intensity
out vec3 frag_world_pos; // World position of fragment

// Ambient occlusion values
const float ao_values[4] = float[4](0.1, 0.25, 0.5, 1.0);

// Shading values for each face
const float face_shading[6] = float[6](
        1.0, 0.5, // Top: 1.0 Bottom: 0.5
        0.5, 0.8, // Right: 0.5 Left: 0.8
        0.5, 0.8 // Front: 0.5 Back: 0.8
);

// UV coordinates for vertices of a face
const vec2 uv_coords[4] = vec2[4](
        vec2(0, 0), vec2(0, 1),
        vec2(1, 0), vec2(1, 1)
);

// Indices of UV coordinates for vertices of a face
const int uv_indices[24] = int[24](
        1, 0, 2, 1, 2, 3, // Texture coords indices for vertices of an even face
        3, 0, 2, 3, 1, 0, // Odd faces
        3, 1, 0, 3, 0, 2, // Even flipped face
        1, 2, 3, 1, 0, 2
);

// Unpack packed_data function to extract vertex data
// Also this is really cool...
void unpack(uint packed_data) {
    // a, b, c, d, e, f, g = x, y, z, voxel_id, face_id, ao_id, flip_id
    uint b_bit = 6u, c_bit = 6u, d_bit = 8u, e_bit = 3u, f_bit = 2u, g_bit = 1u;
    uint b_mask = 63u, c_mask = 63u, d_mask = 255u, e_mask = 7u, f_mask = 3u, g_mask = 1u;

    // Set the bit masks
    uint fg_bit = f_bit + g_bit;
    uint efg_bit = e_bit + fg_bit;
    uint defg_bit = d_bit + efg_bit;
    uint cdefg_bit = c_bit + defg_bit;
    uint bcdefg_bit = b_bit + cdefg_bit;

    // Unpack the packed_data into individual components
    x = int(packed_data >> bcdefg_bit);
    y = int((packed_data >> cdefg_bit) & b_mask);
    z = int((packed_data >> defg_bit) & c_mask);
    voxel_id = int((packed_data >> efg_bit) & d_mask);
    face_id = int((packed_data >> fg_bit) & e_mask);
    ao_id = int((packed_data >> g_bit) & f_mask);
    flip_id = int(packed_data & g_mask);

}

void main() {
    // Unpack the packed_data to extract vertex data
    unpack(packed_data);

    vec3 in_position = vec3(x, y, z); // Vertex position
    int uv_index = gl_VertexID % 6 + ((face_id & 1) + flip_id * 2) * 6; // Calculate UV index

    // Calculate UV coordinates for the current vertex
    uv = uv_coords[uv_indices[uv_index]];

    // Calculate shading intensity by multiplying face shading and AO values
    shading = face_shading[face_id] * ao_values[ao_id];

    // Calculate world position
    frag_world_pos = (m_model * vec4(in_position, 1.0)).xyz;

    // Transform vertex position to clip space
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}// End of void main()
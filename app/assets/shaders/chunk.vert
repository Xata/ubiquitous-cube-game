#version 330 core

// --- Input: Packed vertex data for performance ---
// All vertex info is packed into a single uint32 to save memory bandwidth
layout (location = 0) in uint packed_data;

// Unpacked vertex data (local to this shader)
int x, y, z;        // Vertex position within chunk (0-31)
int ao_id;          // Ambient occlusion ID (0-3, darker to lighter)
int flip_id;        // Fix for anisotropic filtering artifacts

// --- Uniforms (set by CPU per chunk) ---
uniform mat4 m_proj;  // Camera projection matrix (perspective)
uniform mat4 m_view;  // Camera view matrix (position + rotation)
uniform mat4 m_model; // Chunk's world position matrix

// --- Outputs to fragment shader ---
flat out int voxel_id; // Block type ID (passed to fragment shader)
flat out int face_id;  // Which face: 0=top, 1=bottom, 2-5=sides

out vec3 voxel_color;   // Not used currently
out vec2 uv;            // Texture coordinates (0-1)
out float shading;      // Final lighting value (face direction * AO)
out vec3 frag_world_pos; // World position for water reflections

// --- Lighting constants ---
// Ambient occlusion: how much nearby blocks darken this vertex
const float ao_values[4] = float[4](0.1, 0.25, 0.5, 1.0); // darker -> lighter

// Directional shading: different brightness per face
const float face_shading[6] = float[6](
    1.0, 0.5,  // Top: bright (1.0), Bottom: dark (0.5)
    0.5, 0.8,  // Right: medium (0.5), Left: medium-bright (0.8)
    0.5, 0.8   // Front: medium (0.5), Back: medium-bright (0.8)
);

// --- UV coordinate lookup tables ---
// Maps vertex index to UV coords, handles quad orientation and flipping
const vec2 uv_coords[4] = vec2[4](
    vec2(0, 0), vec2(0, 1),
    vec2(1, 0), vec2(1, 1)
);

const int uv_indices[24] = int[24](
    1, 0, 2, 1, 2, 3,  // Normal even face
    3, 0, 2, 3, 1, 0,  // Normal odd face
    3, 1, 0, 3, 0, 2,  // Flipped even face (fixes anisotropic artifacts)
    1, 2, 3, 1, 0, 2   // Flipped odd face
);

// --- Unpacking function ---
// Extracts vertex data from packed uint32
// Format: [6 bits x][6 bits y][6 bits z][8 bits voxel_id][3 bits face_id][2 bits ao_id][1 bit flip_id]
void unpack(uint packed_data) {
    // Bit sizes for each field
    uint b_bit = 6u, c_bit = 6u, d_bit = 8u, e_bit = 3u, f_bit = 2u, g_bit = 1u;
    // Bit masks to extract values
    uint b_mask = 63u, c_mask = 63u, d_mask = 255u, e_mask = 7u, f_mask = 3u, g_mask = 1u;

    // Calculate bit offsets for each field
    uint fg_bit = f_bit + g_bit;
    uint efg_bit = e_bit + fg_bit;
    uint defg_bit = d_bit + efg_bit;
    uint cdefg_bit = c_bit + defg_bit;
    uint bcdefg_bit = b_bit + cdefg_bit;

    // Extract each field by shifting and masking
    x = int(packed_data >> bcdefg_bit);
    y = int((packed_data >> cdefg_bit) & b_mask);
    z = int((packed_data >> defg_bit) & c_mask);
    voxel_id = int((packed_data >> efg_bit) & d_mask);
    face_id = int((packed_data >> fg_bit) & e_mask);
    ao_id = int((packed_data >> g_bit) & f_mask);
    flip_id = int(packed_data & g_mask);
}

void main() {
    // --- Step 1: Unpack vertex data from compressed format ---
    unpack(packed_data);

    // --- Step 2: Build vertex position (local to chunk) ---
    vec3 in_position = vec3(x, y, z);

    // --- Step 3: Calculate UV coordinates ---
    // UV index selects correct coords based on vertex position in triangle,
    // face orientation (even/odd), and flip state (to fix texture artifacts)
    int uv_index = gl_VertexID % 6 + ((face_id & 1) + flip_id * 2) * 6;
    uv = uv_coords[uv_indices[uv_index]];

    // --- Step 4: Calculate lighting ---
    // Multiply face direction shading (which side of block) with ambient occlusion
    shading = face_shading[face_id] * ao_values[ao_id];

    // --- Step 5: Calculate world position (for water reflections) ---
    frag_world_pos = (m_model * vec4(in_position, 1.0)).xyz;

    // --- Step 6: Transform to clip space for rasterization ---
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}
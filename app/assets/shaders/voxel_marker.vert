#version 330 core

// Input variables
layout (location = 0) in vec2 in_tex_coord_0; // Texture coordinates
layout (location = 1) in vec3 in_position; // Vertex positions

// Uniform matrices
uniform mat4 m_proj; // Projection matrix
uniform mat4 m_view; // View matrix
uniform mat4 m_model; // Model matrix
uniform uint mode_id; // Mode identifier (used to select marker color)

// Marker colors based on mode_id
const vec3 marker_colors[2] = vec3[2](vec3(1, 0, 0), vec3(0, 0, 1));

// Output variables
out vec3 marker_color; // Color of the marker
out vec2 uv; // Output texture coordinates


void main() {
    // Pass texture coordinates to the fragment shader
    uv = in_tex_coord_0;

    // Select marker color based on mode_id
    marker_color = marker_colors[mode_id];

    // Transform vertex position into clip space
    gl_Position = m_proj * m_view * m_model * vec4((in_position - 0.5) * 1.01 + 0.5, 1.0);
}// End of void main()
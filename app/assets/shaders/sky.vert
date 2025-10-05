#version 330 core

layout (location = 0) in vec3 in_position;

out vec3 sky_position;

uniform mat4 m_proj;
uniform mat4 m_view;

void main() {
    // Remove translation from view matrix (only keep rotation)
    mat4 view_no_translation = mat4(mat3(m_view));

    vec4 pos = m_proj * view_no_translation * vec4(in_position, 1.0);

    // Set z to w so depth is always 1.0 (furthest possible)
    gl_Position = pos.xyww;

    sky_position = in_position;
}

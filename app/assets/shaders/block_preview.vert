#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec2 in_uv;
layout (location = 2) in float in_face_id;

uniform mat4 m_proj;
uniform mat4 m_model;

out vec2 uv;
flat out int face_id;

void main() {
    uv = in_uv;
    face_id = int(in_face_id);
    gl_Position = m_proj * m_model * vec4(in_position, 1.0);
}

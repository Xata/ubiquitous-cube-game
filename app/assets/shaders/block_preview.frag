#version 330 core

layout (location = 0) out vec4 fragColor;

uniform sampler2DArray u_texture_array_0;
uniform int voxel_id;

in vec2 uv;
flat in int face_id;

const vec3 gamma = vec3(2.0);
const vec3 inv_gamma = 1.0 / gamma;

// Simple directional lighting
const float face_shading[6] = float[6](
    1.0, 0.5,   // Top: 1.0, Bottom: 0.5
    0.7, 0.7,   // Right: 0.7, Left: 0.7
    0.8, 0.8    // Front: 0.8, Back: 0.8
);

void main() {
    // Adjust UV for texture atlas
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    // Sample texture
    vec4 tex_sample = texture(u_texture_array_0, vec3(face_uv, voxel_id));
    vec3 tex_col = tex_sample.rgb;

    // Apply gamma correction
    tex_col = pow(tex_col, gamma);

    // Apply face shading
    tex_col *= face_shading[face_id];

    // Inverse gamma correction
    tex_col = pow(tex_col, inv_gamma);

    fragColor = vec4(tex_col, 1.0);
}

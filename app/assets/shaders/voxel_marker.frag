#version 330 core

// Output color of the fragment
layout (location = 0) out vec4 fragColor;

// Input variables from vertex shader
in vec3 marker_color;
in vec2 uv;
flat in uint mode;
flat in int face_id;

// Uniform texture samplers
uniform sampler2D u_texture_0; // Old texture for delete mode
uniform sampler2DArray u_texture_array_0; // Texture array for place mode
uniform int selected_voxel_id; // Currently selected block

// Gamma correction
const vec3 gamma = vec3(2.0);
const vec3 inv_gamma = 1.0 / gamma;

void main() {
    if (mode == 0u) {
        // Delete mode: Red tint overlay
        vec4 tex_color = texture(u_texture_0, uv);
        fragColor.rgb = mix(tex_color.rgb, vec3(1.0, 0.0, 0.0), 0.4);  // 40% red tint
        fragColor.a = 0.8;  // Semi-transparent
    } else {
        // Place mode: Ghost preview of selected block
        // Adjust UV for texture atlas (same as chunk shader)
        vec2 face_uv = uv;
        face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

        // Sample from texture array
        vec4 tex_sample = texture(u_texture_array_0, vec3(face_uv, selected_voxel_id));
        vec3 tex_col = tex_sample.rgb;

        // Apply gamma correction
        tex_col = pow(tex_col, gamma);

        // Inverse gamma correction
        tex_col = pow(tex_col, inv_gamma);

        // Ghost effect - semi-transparent with slight brightness
        fragColor.rgb = tex_col * 1.2;  // Slight brightness boost
        fragColor.a = 0.5;  // Semi-transparent ghost
    }
}// End of void main()
#version 330 core

// Output variable for the final color with fog effect
layout (location = 0) out vec4 fogColor;

// Gamma correction constants
const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

// Uniforms
uniform sampler2DArray u_texture_array_0; // Texture array containing voxel textures
uniform vec3 bg_color; // Background color

// Vertex shader outputs
in vec3 voxel_color; // Color of the voxel
in vec2 uv; // UV coordinates of the fragment
in float shading; // Shading intensity

flat in int face_id; // ID of the voxel face
flat in int voxel_id; // ID of the voxel

void main() {
    // Adjust UV coordinates to map voxel texture
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    // Sample voxel texture from the texture array
    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, voxel_id)).rgb;
    tex_col = pow(tex_col, gamma); // Apply gamma correction

    // Apply shading to the texture color
    tex_col *= shading;

    // Fog effect calculation
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w; // Calculate distance from the camera
    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00001 * fog_dist * fog_dist))); // Apply fog

    // Inverse gamma correction for final color output
    tex_col = pow(tex_col, inv_gamma);

    // Set final color with fog effect
    fogColor = vec4(tex_col, 1);
}
#version 330 core

// Output variable for the final color with fog effect
layout (location = 0) out vec4 fogColor;

// Gamma correction constants
const vec3 gamma = vec3(2.0);
const vec3 inv_gamma = 1 / gamma;

// Uniforms
uniform sampler2DArray u_texture_array_0; // Texture array containing voxel textures
uniform vec3 bg_color; // Background color
uniform vec3 u_camera_pos; // Camera position

// Vertex shader outputs
in vec3 voxel_color; // Color of the voxel
in vec2 uv; // UV coordinates of the fragment
in float shading; // Shading intensity
in vec3 frag_world_pos; // World position of fragment

flat in int face_id; // ID of the voxel face
flat in int voxel_id; // ID of the voxel

void main() {
    // Adjust UV coordinates to map voxel texture
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    // Sample voxel texture from the texture array
    vec4 tex_sample = texture(u_texture_array_0, vec3(face_uv, voxel_id));
    vec3 tex_col = tex_sample.rgb;
    float alpha = tex_sample.a;

    tex_col = pow(tex_col, gamma); // Apply gamma correction

    // Apply shading to the texture color
    tex_col *= shading;

    // Fog effect calculation
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w; // Calculate distance from the camera

    // Check if this is a water block (voxel_id == 16)
    if (voxel_id == 16) {
        alpha = 0.65; // Semi-transparent water

        // Water color - murky blue
        vec3 water_color = vec3(0.1, 0.25, 0.45); // Murky blue

        // Water fog to obscure geometry behind water
        float water_fog = 1.0 - exp2(-0.15 * fog_dist);
        tex_col = mix(tex_col, water_color, water_fog * 0.85);

        // Apply blue tint for water appearance
        tex_col *= vec3(0.65, 0.8, 1.0);

        // Add reflection effect
        if (face_id == 0) { // Top face of water
            // Calculate view direction from fragment to camera
            vec3 view_dir = normalize(u_camera_pos - frag_world_pos);

            // Water surface normal (pointing up)
            vec3 water_normal = vec3(0.0, 1.0, 0.0);

            // Fresnel effect - stronger and more visible
            float fresnel = pow(1.0 - max(dot(view_dir, water_normal), 0.0), 2.0);
            fresnel = clamp(fresnel * 0.8 + 0.3, 0.3, 0.9); // Keep between 30-90%

            // Create animated ripple effect
            float wave = sin(frag_world_pos.x * 3.0) * cos(frag_world_pos.z * 3.0) * 0.1;
            fresnel += wave;

            // Blue sky reflection instead of grey background
            vec3 sky_reflection = vec3(0.5, 0.7, 1.0); // Nice blue sky color

            // Apply reflection
            tex_col = mix(tex_col, sky_reflection, fresnel);
        }
    }

    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00001 * fog_dist * fog_dist))); // Apply fog

    // Inverse gamma correction for final color output
    tex_col = pow(tex_col, inv_gamma);

    // Set final color with fog effect and alpha
    fogColor = vec4(tex_col, alpha);
}
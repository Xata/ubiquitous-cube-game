#version 330 core

// Final output color with fog and transparency effects applied
layout (location = 0) out vec4 fogColor;

// Gamma correction constants for proper color display
const vec3 gamma = vec3(2.0);
const vec3 inv_gamma = 1.0 / gamma;

// --- Uniforms (set by CPU) ---
uniform sampler2DArray u_texture_array_0; // Texture atlas containing all block textures
uniform vec3 bg_color; // Background/sky color for fog
uniform vec3 u_camera_pos; // Player camera position (for water reflections)

// --- Inputs from vertex shader ---
in vec3 voxel_color; // Base color of the voxel (not currently used)
in vec2 uv; // Texture coordinates (0-1 range)
in float shading; // Lighting intensity (combines face direction + ambient occlusion)
in vec3 frag_world_pos; // World-space position of this fragment (for reflections)

flat in int face_id; // Which face of the cube (0=top, 1=bottom, 2-5=sides)
flat in int voxel_id; // Block type ID (0=void, 1=sand, 2=grass, ..., 16=water)

void main() {
    // --- Step 1: Sample block texture from atlas ---
    // Adjust UV to select correct texture from 3-wide atlas (top/side/bottom in one row)
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    // Sample from 2D texture array (layer = voxel_id)
    vec4 tex_sample = texture(u_texture_array_0, vec3(face_uv, voxel_id));
    vec3 tex_col = tex_sample.rgb;
    float alpha = tex_sample.a;

    // Apply gamma correction (convert from sRGB to linear for lighting calculations)
    tex_col = pow(tex_col, gamma);

    // --- Step 2: Apply lighting (face direction + ambient occlusion) ---
    tex_col *= shading;

    // --- Step 3: Calculate fog distance ---
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w; // Distance from camera

    // --- Step 4: Special water rendering (voxel_id == 16) ---
    if (voxel_id == 16) {
        alpha = 0.65; // Make water semi-transparent

        // Apply underwater fog effect (murky blue depth fade)
        vec3 water_color = vec3(0.1, 0.25, 0.45); // Deep water color
        float water_fog = 1.0 - exp2(-0.15 * fog_dist);
        tex_col = mix(tex_col, water_color, water_fog * 0.85);

        // Add blue tint to water
        tex_col *= vec3(0.65, 0.8, 1.0);

        // --- Water surface reflections (only on top face) ---
        if (face_id == 0) {
            // Calculate view direction (camera to fragment)
            vec3 view_dir = normalize(u_camera_pos - frag_world_pos);

            // Water surface normal points straight up
            vec3 water_normal = vec3(0.0, 1.0, 0.0);

            // Fresnel effect: more reflection at grazing angles (30-90% reflection)
            float fresnel = pow(1.0 - max(dot(view_dir, water_normal), 0.0), 2.0);
            fresnel = clamp(fresnel * 0.8 + 0.3, 0.3, 0.9);

            // Add animated wave ripples for visual interest
            float wave = sin(frag_world_pos.x * 3.0) * cos(frag_world_pos.z * 3.0) * 0.1;
            fresnel += wave;

            // Reflect a nice blue sky (no actual skybox, so we fake it)
            vec3 sky_reflection = vec3(0.5, 0.7, 1.0);

            // Mix water color with sky reflection
            tex_col = mix(tex_col, sky_reflection, fresnel);
        }
    }

    // --- Step 5: Apply distance fog ---
    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00001 * fog_dist * fog_dist)));

    // --- Step 6: Convert back to sRGB for display ---
    tex_col = pow(tex_col, inv_gamma);

    // --- Step 7: Output final color with transparency ---
    fogColor = vec4(tex_col, alpha);
}
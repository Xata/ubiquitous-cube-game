#version 330 core

in vec3 sky_position;
out vec4 fragColor;

uniform float u_time;

// Simple 2D noise function
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);

    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));

    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

// Fractional Brownian Motion for cloud-like patterns
float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;

    for (int i = 0; i < 5; i++) {
        value += amplitude * noise(p * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
    }

    return value;
}

void main() {
    // Normalize the sky position to get direction
    vec3 direction = normalize(sky_position);

    // Calculate gradient based on vertical direction
    float height = direction.y;

    // Sky colors
    vec3 horizon_color = vec3(0.7, 0.85, 1.0);  // Light blue at horizon
    vec3 zenith_color = vec3(0.2, 0.5, 0.9);    // Deeper blue at top

    // Smooth interpolation from horizon to zenith
    float gradient = smoothstep(-0.1, 0.8, height);

    // Mix the colors based on height
    vec3 sky_color = mix(horizon_color, zenith_color, gradient);

    // Generate blocky clouds - only in upper sky
    if (height > 0.2) {
        // Simple planar projection (like Minecraft)
        // Just use X and Z directly, normalized by Y to keep consistent size
        vec2 cloud_uv = direction.xz / (direction.y + 0.5);

        // Slowly drift clouds over time
        cloud_uv += vec2(u_time * 0.01, u_time * 0.005);

        // PIXELATE for blocky effect
        float pixel_size = 0.1;  // Smaller = smaller cloud blocks
        cloud_uv = floor(cloud_uv / pixel_size) * pixel_size;

        // Simple noise-based clouds
        float cloud_noise = fbm(cloud_uv * 1.5);

        // Hard cutoff for blocky clouds
        float cloud_density = step(0.55, cloud_noise);

        // Fade near horizon
        cloud_density *= smoothstep(0.2, 0.4, height);

        // Cloud color
        vec3 cloud_color = vec3(1.0, 1.0, 1.0);

        // Mix clouds
        sky_color = mix(sky_color, cloud_color, cloud_density * 0.9);
    }

    // Subtle breathing effect
    float pulse = sin(u_time * 0.2) * 0.02 + 1.0;
    sky_color *= pulse;

    fragColor = vec4(sky_color, 1.0);
}

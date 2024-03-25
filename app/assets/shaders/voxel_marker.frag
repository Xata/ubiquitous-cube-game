#version 330 core

// Output color of the fragment
layout (location = 0) out vec4 fragColor;

// Input variables from vertex shader
in vec3 marker_color;
in vec2 uv;

// Uniform texture sampler
uniform sampler2D u_texture_0; // Texture sampler

void main() {
    // Sample texture using UV coordinates
    fragColor = texture(u_texture_0, uv);

    // Add marker color to the sampled texture color
    fragColor.rgb += marker_color;

    // Determine fragment alpha value
    // If the sum of red and blue components of the resulting color exceeds 1, set alpha to 0, otherwise set it to 1
    fragColor.a = (fragColor.r + fragColor.b > 1.0) ? 0.0 : 1.0;
}// End of void main()
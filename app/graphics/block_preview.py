from app.settings import *
import moderngl
import numpy as np


class BlockPreview:
    """
    Renders a rotating preview of the selected block in the corner of the screen.
    """

    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.player = app.player
        self.program = app.shader_program.block_preview

        # Create cube vertices
        self.vbo = self.get_vbo()
        self.vao = self.get_vao()

        # Rotation angle for animation
        self.rotation = 0

    def get_vbo(self):
        """Generate vertex buffer for a single cube."""
        # Cube vertices with UV coords and face IDs
        # Format: x, y, z, u, v, face_id
        vertices = [
            # Top face (face_id = 0)
            -0.5,  0.5, -0.5,  0, 0, 0,
            -0.5,  0.5,  0.5,  0, 1, 0,
             0.5,  0.5,  0.5,  1, 1, 0,
            -0.5,  0.5, -0.5,  0, 0, 0,
             0.5,  0.5,  0.5,  1, 1, 0,
             0.5,  0.5, -0.5,  1, 0, 0,

            # Bottom face (face_id = 1)
            -0.5, -0.5, -0.5,  0, 0, 1,
             0.5, -0.5, -0.5,  1, 0, 1,
             0.5, -0.5,  0.5,  1, 1, 1,
            -0.5, -0.5, -0.5,  0, 0, 1,
             0.5, -0.5,  0.5,  1, 1, 1,
            -0.5, -0.5,  0.5,  0, 1, 1,

            # Right face (face_id = 2)
             0.5, -0.5, -0.5,  0, 1, 2,
             0.5,  0.5, -0.5,  0, 0, 2,
             0.5,  0.5,  0.5,  1, 0, 2,
             0.5, -0.5, -0.5,  0, 1, 2,
             0.5,  0.5,  0.5,  1, 0, 2,
             0.5, -0.5,  0.5,  1, 1, 2,

            # Left face (face_id = 3)
            -0.5, -0.5, -0.5,  0, 1, 3,
            -0.5, -0.5,  0.5,  1, 1, 3,
            -0.5,  0.5,  0.5,  1, 0, 3,
            -0.5, -0.5, -0.5,  0, 1, 3,
            -0.5,  0.5,  0.5,  1, 0, 3,
            -0.5,  0.5, -0.5,  0, 0, 3,

            # Back face (face_id = 4)
            -0.5, -0.5, -0.5,  0, 1, 4,
            -0.5,  0.5, -0.5,  0, 0, 4,
             0.5,  0.5, -0.5,  1, 0, 4,
            -0.5, -0.5, -0.5,  0, 1, 4,
             0.5,  0.5, -0.5,  1, 0, 4,
             0.5, -0.5, -0.5,  1, 1, 4,

            # Front face (face_id = 5)
            -0.5, -0.5,  0.5,  0, 1, 5,
             0.5, -0.5,  0.5,  1, 1, 5,
             0.5,  0.5,  0.5,  1, 0, 5,
            -0.5, -0.5,  0.5,  0, 1, 5,
             0.5,  0.5,  0.5,  1, 0, 5,
            -0.5,  0.5,  0.5,  0, 0, 5,
        ]

        vertex_data = np.array(vertices, dtype='f4')
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_vao(self):
        """Create vertex array object."""
        vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '3f 2f 1f', 'in_position', 'in_uv', 'in_face_id')]
        )
        return vao

    def update(self):
        """Update rotation animation."""
        self.rotation += self.app.delta_time * 0.001  # Slow rotation

    def render(self):
        """Render the block preview in the top-right corner."""
        # Enable face culling for proper preview rendering
        self.ctx.enable(moderngl.CULL_FACE)

        # Create model matrix with rotation and positioning
        # Position in top-right corner
        m_model = glm.mat4()
        m_model = glm.translate(m_model, glm.vec3(0.7, 0.7, -2))  # Position in view space
        m_model = glm.rotate(m_model, self.rotation, glm.vec3(0, 1, 0))  # Rotate around Y
        m_model = glm.rotate(m_model, glm.radians(20), glm.vec3(1, 0, 0))  # Tilt slightly
        m_model = glm.scale(m_model, glm.vec3(0.15))  # Small scale

        # Orthographic projection for UI overlay
        ortho = glm.ortho(-1, 1, -1, 1, 0.1, 10)

        # Set uniforms
        self.program['m_proj'].write(ortho)
        self.program['m_model'].write(m_model)
        self.program['voxel_id'] = self.player.selected_voxel
        self.program['u_texture_array_0'] = 1

        # Render the cube
        self.vao.render()

        # Disable face culling again (since it's disabled for main world rendering)
        self.ctx.disable(moderngl.CULL_FACE)

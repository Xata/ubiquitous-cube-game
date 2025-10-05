"""
Sky rendering system.

Renders a gradient skybox that follows the camera.
"""

from app.settings import *
import numpy as np


class Sky:
    """
    Renders a sky gradient using a cube mesh.

    The sky follows the camera rotation but not position,
    creating the illusion of an infinite sky.
    """

    def __init__(self, app):
        """
        Initialize the sky renderer.

        Args:
            app: The main game instance
        """
        self.app = app
        self.ctx = app.ctx
        self.program = app.shader_program.sky

        # Create a large cube for the skybox
        self.vbo = self.get_vbo()
        self.vao = self.get_vao()

    def get_vertex_data(self):
        """
        Generate vertex data for a cube.

        Returns:
            numpy.ndarray: Vertex positions for the skybox cube
        """
        # Large cube vertices (no need for normals or UVs)
        vertices = [
            # Back face
            -1, -1, -1,
             1, -1, -1,
             1,  1, -1,
            -1, -1, -1,
             1,  1, -1,
            -1,  1, -1,

            # Front face
            -1, -1,  1,
             1,  1,  1,
             1, -1,  1,
            -1, -1,  1,
            -1,  1,  1,
             1,  1,  1,

            # Left face
            -1, -1, -1,
            -1,  1,  1,
            -1, -1,  1,
            -1, -1, -1,
            -1,  1, -1,
            -1,  1,  1,

            # Right face
             1, -1, -1,
             1, -1,  1,
             1,  1,  1,
             1, -1, -1,
             1,  1,  1,
             1,  1, -1,

            # Bottom face
            -1, -1, -1,
            -1, -1,  1,
             1, -1,  1,
            -1, -1, -1,
             1, -1,  1,
             1, -1, -1,

            # Top face
            -1,  1, -1,
             1,  1,  1,
             1,  1, -1,
            -1,  1, -1,
            -1,  1,  1,
             1,  1,  1,
        ]

        return np.array(vertices, dtype='f4')

    def get_vbo(self):
        """
        Create vertex buffer object.

        Returns:
            moderngl.Buffer: VBO containing vertex data
        """
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_vao(self):
        """
        Create vertex array object.

        Returns:
            moderngl.VertexArray: VAO for sky rendering
        """
        vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '3f', 'in_position')]
        )
        return vao

    def render(self):
        """
        Render the sky.

        Should be called before rendering the world.
        """
        # Disable depth writing for sky (but keep depth testing)
        self.ctx.depth_func = '<='

        # Write uniforms
        self.program['m_proj'].write(self.app.player.m_proj)
        self.program['m_view'].write(self.app.player.m_view)
        self.program['u_time'].value = self.app.time

        # Render the sky cube
        self.vao.render()

        # Reset depth function
        self.ctx.depth_func = '<'

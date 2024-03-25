from app.settings import *
from .mesh import Mesh


class CubeMesh(Mesh):
    """
    Represents a cube mesh for rendering voxel markers.

    Inherits from Mesh.

    Attributes:
        app: The game object
        ctx: The context associated with the game
        program: The shader program used for rendering
        vbo_format: The format string for vertex buffer objects
        attrs: The attributes of the mesh
        vao: The vertex array object for the mesh
    """

    def __init__(self, app):
        """
        Initializes a CubeMesh object

        Args:
            app: The game object
        """

        super().__init__()
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.voxel_marker

        self.vbo_format = '2f2 3f2'
        self.attrs = ('in_tex_coord_0', 'in_position',)
        self.vao = self.get_vao()

    @staticmethod
    def get_data(vertices, indices):
        """
        Generates data for the vertices of the cube.

        Args:
            vertices: List of vertices
            indices: List of indices

        Returns:
            numpy.array: The generated data in a numpy array
        """

        data = [vertices[ind] for triangle in indices for ind in triangle]
        return numpy.array(data, dtype='float16')

    def get_vertex_data(self):
        """
        Generates vertex data for the cube mesh

        Returns:
            numpy.array: The vertex data
        """

        vertices = [
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),
            (0, 1, 0), (0, 0, 0), (1, 0, 0), (1, 1, 0)
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]
        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3), (0, 1, 2),
            (0, 2, 3), (0, 1, 2),
            (0, 1, 2), (2, 3, 0),
            (2, 3, 0), (2, 0, 1),
            (0, 2, 3), (0, 1, 2),
            (3, 1, 2), (3, 0, 1),
        ]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)
        vertex_data = numpy.hstack([tex_coord_data, vertex_data])
        return vertex_data
    
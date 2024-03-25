from app.meshes.mesh import Mesh
from .chunk_mesh_builder import build_chunk_mesh


class ChunkMesh(Mesh):
    """
    Represents the chunk mesh for rendering a chunk in the world.

    Inherits from Mesh.

    Attributes:
        app: The game object.
        chunk: Chunk associated with the mesh
        ctx: OpenGL context associated with the game
        program: Shader program used for rendering
        vbo_format: Format string for the vertex buffer object
        format_size: Size of the format
        attrs: Attributes of the mesh
        vao: Vertex array object for the mesh
    """

    def __init__(self, chunk):
        """
        Initializes a ChunkMesh object with the given chunk.

        Args:
            chunk: The chunk object
        """

        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.chunk

        self.vbo_format = '1u4'
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())

        self.attrs = ('packed_data',)
        self.vao = self.get_vao()

    def rebuild(self):
        """
        Rebuilds the vertex array object (VAO) for the mesh.
        """

        self.vao = self.get_vao()

    def get_vertex_data(self):
        """
        Generates vertex data for the chunk mesh.

        Returns:
            numpy.array: Vertex data
        """

        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_pos=self.chunk.position,
            world_voxels=self.chunk.world.voxels
        )

        return mesh

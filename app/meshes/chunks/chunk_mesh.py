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
        vao_solid: Vertex array object for solid geometry
        vao_transparent: Vertex array object for transparent geometry
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
        self.vao_solid = None
        self.vao_transparent = None
        self.rebuild()

    def rebuild(self):
        """
        Rebuilds the vertex array objects (VAOs) for solid and transparent geometry.
        """
        solid_data, transparent_data = self.get_vertex_data()

        # Build solid VAO
        if len(solid_data) > 0:
            vbo_solid = self.ctx.buffer(solid_data)
            self.vao_solid = self.ctx.vertex_array(
                self.program, [(vbo_solid, self.vbo_format, *self.attrs)], skip_errors=True
            )
        else:
            self.vao_solid = None

        # Build transparent VAO
        if len(transparent_data) > 0:
            vbo_transparent = self.ctx.buffer(transparent_data)
            self.vao_transparent = self.ctx.vertex_array(
                self.program, [(vbo_transparent, self.vbo_format, *self.attrs)], skip_errors=True
            )
        else:
            self.vao_transparent = None

    def get_vertex_data(self):
        """
        Generates vertex data for the chunk mesh.

        Returns:
            tuple: (solid_mesh_data, transparent_mesh_data)
        """

        solid_mesh, transparent_mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_pos=self.chunk.position
        )

        return solid_mesh, transparent_mesh

    def render(self):
        """
        Renders the chunk mesh (solid geometry only - transparent is rendered separately).
        """
        if self.vao_solid:
            self.vao_solid.render()

    def render_transparent(self):
        """
        Renders transparent geometry (water blocks).
        """
        if self.vao_transparent:
            self.vao_transparent.render()

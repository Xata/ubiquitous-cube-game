import numpy


class Mesh:
    """
    A mesh for rendering in the OpenGL context.

    Attributes:
        ctx: OpenGL context used for rendering
        program: Shader program associated with the mesh
        vbo_format: Format of the vertex buffer object
        attrs: Attribute names for the mesh
        vao: Vertex array object (VAO) for the mesh
    """

    def __init__(self):
        """
        Initializes a Mesh object.
        """

        # Define OpenGL context
        self.ctx = None

        # Define the shader program
        self.program = None

        # Define the vertex buffer. Data type format should be: "3f 3f"
        self.vbo_format = None

        # Attribute names. Format should be: ("in_position", "in_color")
        self.attrs: tuple[str, ...] = None

        # Define vertex array object
        self.vao = None

    def get_vertex_data(self) -> numpy.array:
        """
        Abstract function to generate vertex data
        """
        ...

    def get_vao(self):
        """
        Generate and return a vertex array object (VAO) for the mesh

        Returns:
            moderngl.VertexArray: The vertex array object (VAO)
        """

        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors=True
        )

        return vao

    def render(self):
        """
        Renders the mesh.
        """

        self.vao.render()

from app.settings import *


class ShaderProgram:
    """
        Responsible for loading and managing shader programs.

        Attributes:
            app: The game object
            ctx: The context associated with the game
            player: The player object from the game
            chunk: The shader program for rendering chunks
            voxel_marker: The shader program for rendering voxel markers
        """
    def __init__(self, app):
        """
        Initializes a ShaderProgram object.

        Args:
            app: The game object
        """
        self.app = app
        self.ctx = app.ctx
        self.player = app.player

        # Load shader programs
        self.chunk = self.get_program(shader_name='chunk')
        self.voxel_marker = self.get_program(shader_name='voxel_marker')
        self.block_preview = self.get_program(shader_name='block_preview')

        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        """
        Sets the initial uniform values for the shader programs.
        """

        # Chunk uniforms
        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['m_model'].write(glm.mat4())
        self.chunk['u_texture_array_0'] = 1
        self.chunk['bg_color'].write(BG_COLOR)
        self.chunk['u_camera_pos'].write(self.player.position)

        # Voxel marker uniforms
        self.voxel_marker['m_proj'].write(self.player.m_proj)
        self.voxel_marker['m_model'].write(glm.mat4())
        self.voxel_marker['u_texture_0'] = 0
        self.voxel_marker['u_texture_array_0'] = 1  # Use same texture array as chunks

    def update(self):
        """
        Updates the shader programs with the player's view matrix.
        """
        self.chunk['m_view'].write(self.player.m_view)
        self.chunk['u_camera_pos'].write(self.player.position)
        self.voxel_marker['m_view'].write(self.player.m_view)

    def get_program(self, shader_name):
        """
         Loads and compiles a shader program from vertex and fragment shader files.

         Args:
             shader_name (str): The name of the shader program

         Returns:
             Program: Compiled shader program.
         """

        with open(f'app/assets/shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'app/assets/shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

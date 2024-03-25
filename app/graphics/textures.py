import pygame
import moderngl


class Textures:
    """
    Manages loading and handling of textures for the game.

    Attributes:
        app: The game object
        ctx: The OpenGL context associated with the game
        texture_0: The primary texture
        texture_array_0: The texture array used for multi-layered textures
    """

    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        # Load Textures
        self.texture_0 = self.load('frame.png')
        self.texture_array_0 = self.load('texture_array.png', is_texture_array=True)

        # Assign texture units
        self.texture_0.use(location=0)
        self.texture_array_0.use(location=1)

    def load(self, file_name, is_texture_array=False):
        """
        Loads a texture from the given file and returns a texture object.

        Args:
            file_name (str): The name of the texture file
            is_texture_array (bool): Indicates if the texture is a texture array. Defaults is False

        Returns:
            moderngl.Texture: The loaded texture object
        """

        texture = pygame.image.load(f'app/assets/textures/{file_name}')
        texture = pygame.transform.flip(texture, flip_x=True, flip_y=False)

        if is_texture_array:
            # Calculate number of layers for texture array
            num_layers = 3 * texture.get_height() // texture.get_width()
            texture = self.app.ctx.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers),
                components=4,
                data=pygame.image.tostring(texture, 'RGBA')
            )

        else:
            texture = self.ctx.texture(
                size=texture.get_size(),
                components=4,
                data=pygame.image.tostring(texture, 'RGBA', False)
            )

        # Set texture properties
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        return texture

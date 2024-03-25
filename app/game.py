from app.settings import *
import moderngl
import pygame
import sys

from app.graphics.shader_program import ShaderProgram
from app.graphics.scene import Scene
from app.graphics.textures import Textures

from app.players.player import Player


class Game:
    """
    Represents the main game engine.
    """
    def __init__(self):
        """
        Initializes the Game instance, setting up the OpenGL context, game window, and other stuff.
        """

        pygame.init()

        # Load the icon
        icon_img = pygame.image.load("app/assets/icon.png")

        # Set the OpenGL version to 3.3 and prevent use of deprecated features
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        # Set the depth buffer to 24 bits
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)

        # Set the window resolution and create OpenGL context
        pygame.display.set_mode(WINDOW_RESOLUTION, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        self.ctx = moderngl.create_context()

        # Activate fragment depth tests, culling of invisible faces, and color blending
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)

        # Turn on garbage collection of unused OpenGL objects
        self.ctx.gc_mode = "auto"

        # Create objects to keep track of time
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.time = 0

        # Grab the mouse
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        # Set the icon of the game
        pygame.display.set_icon(icon_img)

        # Set the title of the game window
        pygame.display.set_caption(GAME_TITLE)

        # This flag is to check to see if the game is running or not
        self.is_running = True

        # Init default font
        pygame.font.init()
        self.font = pygame.font.SysFont(name='arial', size=12)


        # Set pygame display surface
        self.display_surface = pygame.display.get_surface()

        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)
        self.player.init_voxel_handler()

    def update(self):
        """
        Updates the game logic and components.
        """

        self.player.update()
        self.shader_program.update()
        self.scene.update()

        # Update the time
        self.delta_time = self.clock.tick(MAX_FPS)
        self.time = pygame.time.get_ticks() * 0.001

        # Debug printing
        # Print the FPS to the console
        # print(f'{self.clock.get_fps() :.0f}')

        # Print player position to the console
        # print(f'{self.player.position}')

    def render(self):
        """
        Renders the main game scene.
        """

        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        pygame.display.flip()

    def handle_events(self):
        """
        Handles pygame events such as quitting the game or player events.
        """

        for event in pygame.event.get():
            # Check for exiting the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.is_running = False

            # Check for player events
            self.player.handle_event(event=event)

    def run(self):
        """
        Runs the main game loop.
        """

        # Main game loop
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        # Exit the game
        pygame.quit()
        sys.exit()

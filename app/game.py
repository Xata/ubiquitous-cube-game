from app.settings import *
import moderngl
import pygame
import sys
import math

from app.graphics.shader_program import ShaderProgram
from app.graphics.scene import Scene
from app.graphics.textures import Textures

from app.players.player import Player
from app.gui.gui_manager import GUIManager
from app.game_mode import GameMode, GameModeManager


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
        # Max OpenGL version on macOS is 4.1
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        # Set the depth buffer to 24 bits
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)

        # Set the window resolution and create OpenGL context
        pygame.display.set_mode(WINDOW_RESOLUTION, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        self.ctx = moderngl.create_context()

        # Activate fragment depth tests and color blending
        # Note: Face culling disabled to fix transparency rendering issues with water
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.BLEND)

        # Set blend function for proper transparency (src_alpha, one_minus_src_alpha)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        # Turn on garbage collection of unused OpenGL objects
        self.ctx.gc_mode = "auto"

        # Create objects to keep track of time
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.time = 0

        # Grab the mouse and enable relative mode (better for macOS)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        try:
            # Try to enable relative mouse mode (SDL2 feature, better mouse locking)
            pygame.mouse.set_relative_mode(True)
        except:
            # Fallback for older pygame versions
            pass
        pygame.mouse.get_rel()  # Clear any initial movement

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

        # Initialize game mode manager (start in DEBUG mode)
        self.game_mode = GameModeManager(starting_mode=GameMode.DEBUG)

        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)
        self.player.init_voxel_handler()

        # Initialize GUI system
        self.gui = GUIManager(self)
        # Register block preview as a GUI widget
        self.gui.add_widget('block_preview', self.scene.block_preview)

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

        # Render GUI elements (block preview, etc.)
        self.gui.render()

        # Render debug info
        self.render_debug_info()

        pygame.display.flip()

    def render_debug_info(self):
        """
        Renders debug information to console (simple approach for OpenGL).
        """
        yaw_degrees = math.degrees(self.player.yaw) % 360
        pitch_degrees = math.degrees(self.player.pitch)

        # Determine cardinal direction
        if 45 <= yaw_degrees < 135:
            direction = "East"
        elif 135 <= yaw_degrees < 225:
            direction = "South"
        elif 225 <= yaw_degrees < 315:
            direction = "West"
        else:
            direction = "North"

        # Print to console every 30 frames to avoid spam
        if not hasattr(self, '_debug_frame_count'):
            self._debug_frame_count = 0

        self._debug_frame_count += 1
        if self._debug_frame_count % 30 == 0:
            print(f"Pos: ({self.player.position.x:.1f}, {self.player.position.y:.1f}, {self.player.position.z:.1f}) | "
                  f"Facing: {direction} (Yaw: {yaw_degrees:.1f}°, Pitch: {pitch_degrees:.1f}°) | "
                  f"FPS: {self.clock.get_fps():.0f} | Ground: {self.player.on_ground}")

    def handle_events(self):
        """
        Handles pygame events such as quitting the game or player events.
        """

        for event in pygame.event.get():
            # Check for exiting the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.is_running = False

            # Handle GUI events (toggling windows, etc.)
            self.gui.handle_event(event)

            # Check for player events
            self.player.handle_event(event=event)

    def run(self):
        """
        Runs the main game loop.
        """
        # Print instructions
        print("CONTROLS:\n")
        print("Movement: WASD and QE")
        print("Place/delete a block: Left Mouse Button")
        print("Switch between placement and deletion modes: Right Mouse Button or p")
        print("Change your block: Middle Mouse Button or - or +")

        # Main game loop
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        # Exit the game
        pygame.quit()
        sys.exit()

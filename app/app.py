# Import libraries
import pygame
import moderngl
import sys

class App:
    def __init__(self, window_size=(1280, 720), fps=60, title="Ubiquitous Cube"):
        # Set window size
        self.WINDOW_SIZE = window_size

        # Set maximum FPS
        self.FPS = fps

        # Set window title
        self.TITLE = title

        # Initialize pygame modules
        pygame.init()
        pygame.display.set_caption(title)

        # Set OpenGL attributes
        pygame.display.gl_get_attribute(pygame.GL_CONTEXT_MAJOR_VERSION)
        pygame.display.gl_get_attribute(pygame.GL_CONTEXT_MINOR_VERSION)
        pygame.display.gl_get_attribute(pygame.GL_CONTEXT_PROFILE_MASK | pygame.GL_CONTEXT_PROFILE_CORE)

        # Create OpenGL context
        pygame.display.set_mode(self.WINDOW_SIZE, flags=pygame.OPENGL | pygame.DOUBLEBUF)

        # Detect and use existing OpenGL context
        self.ctx = moderngl.create_context()

        # Create object to track time
        self.clock = pygame.time.Clock()

    def check_events(self):
        for event in pygame.event.get():
            # Gracefully exit the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def render(self):
        # Clear the framebuffer (Fill the screen with a background color)
        self.ctx.clear(color=(0.05, 0.10, 0.15, 0.0))
        # Swap buffers
        pygame.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.render()
            self.clock.tick(self.FPS)
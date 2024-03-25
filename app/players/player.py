import pygame
from app.settings import *
from app.graphics.camera import Camera


class Player(Camera):
    """
    Represents a player object in the game.

    Inherits from Camera class for controlling the player's view.

    Attributes:
        app: The main application instance
        position: The initial position of the player
        yaw: The initial yaw angle of the player's view
        pitch: The initial pitch angle of the player's view
    """

    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        """
        Initializes a Player instance.

        Args:
            app: The main application instance.
            position (tuple): The initial position of the player. Default is PLAYER_POS
            yaw (float): The initial yaw angle of the player's view. Default is -90
            pitch (float): The initial pitch angle of the player's view. Default is 0
        """

        self.app = app
        super().__init__(position, yaw , pitch)

        # Init placement voxel
        self.selected_voxel = 0

    def init_voxel_handler(self):
        # Voxel handler
        self.player_voxel_handler = self.app.scene.world.voxel_handler

    def update(self):
        """
        Updates the player's state based on user input.
        """

        self.handle_keyboard()
        self.handle_mouse()
        # self.handle_collision()
        super().update()

    def set_player_position(self, new_position):
        """
        Updates the players position
        """
        self.position.x = new_position.x
        self.position.y = new_position.y
        self.position.z = new_position.z

    def handle_event(self, event):
        """
        Handles pygame events for player actions.

        Args:
            event: The pygame event to handle
        """

        # Add or remove voxel with mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            voxel_handler = self.app.scene.world.voxel_handler

            # Left mouse button
            if event.button == 1:
                voxel_handler.set_voxel(self.selected_voxel)
                print(self.selected_voxel)

            # Middle mouse button
            if event.button == 2:
                # Change the 15 when adding a block type to app.blocks.block_type.py:
                if self.selected_voxel < 15:
                    self.selected_voxel += 1
                else:
                    self.selected_voxel = 0

            # Right mouse button
            if event.button == 3:
                voxel_handler.switch_mode()

    def handle_mouse(self):
        """
        Handles mouse movement to adjust player's view.
        """

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def handle_keyboard(self):
        """
        Handles keyboard input to control player movement.
        """

        key_state = pygame.key.get_pressed()
        player_velocity = PLAYER_SPEED * self.app.delta_time
        if key_state[pygame.K_w]:
            self.move_forward(player_velocity)
        if key_state[pygame.K_s]:
            self.move_backward(player_velocity)
        if key_state[pygame.K_a]:
            self.move_left(player_velocity)
        if key_state[pygame.K_d]:
            self.move_right(player_velocity)
        if key_state[pygame.K_q]:
            self.move_up(player_velocity)
        if key_state[pygame.K_e]:
            self.move_down(player_velocity)

import pygame
from app.settings import *
from app.graphics.camera import Camera
from app.blocks.block_type import BLOCK_DICT


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

        # Player states
        self.is_jumping = False
        self.is_moving = 0
        self.turning = 0

        # Physics state
        self.velocity_y = 0.0
        self.on_ground = False
        self.in_water = False

    def init_voxel_handler(self):
        # Voxel handler
        self.player_voxel_handler = self.app.scene.world.voxel_handler

        # Find ground on spawn
        self.find_ground_on_spawn()

    def update(self):
        """
        Updates the player's state based on user input.
        """

        self.handle_keyboard()
        self.handle_mouse()
        self.apply_gravity()
        self.apply_vertical_movement()
        self.check_vertical_collision()  # Check vertical collision after vertical movement
        self.handle_collision()  # Handle horizontal collision
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
                if self.selected_voxel < TOTAL_BLOCKS:
                    self.selected_voxel += 1
                else:
                    self.selected_voxel = 0
                
                # Print the selected block to the console
                print(BLOCK_DICT.get(self.selected_voxel))

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

        voxel_handler = self.app.scene.world.voxel_handler

        key_state = pygame.key.get_pressed()
        player_velocity = PLAYER_SPEED * self.app.delta_time

        # Horizontal movement
        if key_state[pygame.K_w]:
            self.move_forward_horizontal(player_velocity)
        if key_state[pygame.K_s]:
            self.move_backward_horizontal(player_velocity)
        if key_state[pygame.K_a]:
            self.move_left(player_velocity)
        if key_state[pygame.K_d]:
            self.move_right(player_velocity)

        # Jump
        if key_state[pygame.K_SPACE] and self.on_ground:
            self.jump()

        # Block selection
        if key_state[pygame.K_MINUS]:
            if self.selected_voxel > 0:
                self.selected_voxel -= 1
            else:
                self.selected_voxel = TOTAL_BLOCKS
            print(BLOCK_DICT.get(self.selected_voxel))
        elif key_state[pygame.K_PLUS]:
            if self.selected_voxel < TOTAL_BLOCKS:
                self.selected_voxel += 1
            else:
                self.selected_voxel = 0
            print(BLOCK_DICT.get(self.selected_voxel))
        elif key_state[pygame.K_p]:
            voxel_handler.switch_mode()

    def move_forward_horizontal(self, velocity):
        """Move forward but only on horizontal plane (no vertical component)."""
        forward_horizontal = glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z))
        self.position += forward_horizontal * velocity

    def move_backward_horizontal(self, velocity):
        """Move backward but only on horizontal plane (no vertical component)."""
        forward_horizontal = glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z))
        self.position -= forward_horizontal * velocity

    def jump(self):
        """Makes the player jump."""
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def check_in_water(self):
        """Checks if the player is currently in water."""
        world = self.app.scene.world
        # Check at player's head position
        self.in_water = world.is_water_voxel(self.position)

    def find_ground_on_spawn(self):
        """Scans downward from spawn position to find and land on ground."""
        world = self.app.scene.world

        print(f"Scanning for ground from spawn position y={self.position.y}")

        # Scan downward from spawn position to find solid ground
        for y in range(int(self.position.y), -1, -1):
            check_pos = glm.vec3(self.position.x, y, self.position.z)
            if world.is_solid_voxel(check_pos):
                # Found solid block at y, place player's FEET on top at y+1
                ground_y = y + 1
                # Player position is at eye level, so add PLAYER_HEIGHT
                self.position.y = ground_y + PLAYER_HEIGHT
                self.on_ground = True
                print(f"Found ground block at y={y}, placing player eyes at y={self.position.y}, feet at y={ground_y}")

                # Make sure we're not inside a block
                head_check = glm.vec3(self.position.x, self.position.y + 0.5, self.position.z)
                if world.is_solid_voxel(head_check):
                    print(f"Warning: Player head is inside block, moving up")
                    self.position.y += 2

                return

        print("Warning: No ground found, player will fall!")

    def apply_gravity(self):
        """Applies gravity to the player's velocity."""
        if not self.on_ground:
            self.velocity_y -= GRAVITY * self.app.delta_time
            self.velocity_y = max(self.velocity_y, -TERMINAL_VELOCITY)

    def apply_vertical_movement(self):
        """Applies vertical velocity to player position."""
        if self.velocity_y == 0:
            return

        movement = self.velocity_y * self.app.delta_time

        # Apply movement
        self.position.y += movement

    def check_vertical_collision(self):
        """Checks and resolves vertical (Y-axis) collisions immediately after movement."""
        world = self.app.scene.world
        feet_y = self.position.y - PLAYER_HEIGHT

        # Check at multiple horizontal points around the player
        check_offsets = [
            (PLAYER_WIDTH/2, PLAYER_WIDTH/2),
            (-PLAYER_WIDTH/2, PLAYER_WIDTH/2),
            (PLAYER_WIDTH/2, -PLAYER_WIDTH/2),
            (-PLAYER_WIDTH/2, -PLAYER_WIDTH/2),
            (0, 0),  # Center
        ]

        ground_found = False

        for dx, dz in check_offsets:
            check_x = self.position.x + dx
            check_z = self.position.z + dz

            # Check just below feet
            check_pos = glm.vec3(check_x, feet_y - 0.1, check_z)

            if world.is_solid_voxel(check_pos):
                # Found ground - calculate proper landing position
                ground_y = int(glm.floor(check_pos.y)) + 1

                # Only snap if we're falling and penetrating the ground
                if self.velocity_y < 0 and feet_y < ground_y:
                    self.position.y = ground_y + PLAYER_HEIGHT
                    self.velocity_y = 0.0
                    self.on_ground = True
                    ground_found = True
                    break
                # If we're already on ground and not falling, stay grounded
                elif self.on_ground and abs(feet_y - ground_y) < 0.2:
                    self.on_ground = True
                    ground_found = True
                    break

        # If no ground found nearby, start falling
        if not ground_found:
            self.on_ground = False

        # Check for ceiling collision
        if self.velocity_y > 0:  # Moving upward
            head_pos = glm.vec3(self.position.x, self.position.y + 0.2, self.position.z)
            if world.is_solid_voxel(head_pos):
                self.velocity_y = 0.0

    def handle_collision(self):
        """Handles horizontal collision detection with the world."""
        world = self.app.scene.world

        # Store original position
        original_x = self.position.x
        original_z = self.position.z

        # Check horizontal collision at chest and feet level
        body_heights = [
            self.position.y - PLAYER_HEIGHT/2,
            self.position.y - PLAYER_HEIGHT + 0.5,
        ]

        x_collision = False
        z_collision = False

        for body_y in body_heights:
            # Check X-axis collision
            if not x_collision:
                # Check +X direction
                check_pos = glm.vec3(self.position.x + PLAYER_WIDTH/2 + 0.05, body_y, self.position.z)
                if world.is_solid_voxel(check_pos):
                    block_x = int(glm.floor(check_pos.x))
                    self.position.x = block_x - PLAYER_WIDTH/2 - 0.01
                    x_collision = True

                # Check -X direction
                check_pos = glm.vec3(self.position.x - PLAYER_WIDTH/2 - 0.05, body_y, self.position.z)
                if world.is_solid_voxel(check_pos):
                    block_x = int(glm.floor(check_pos.x))
                    self.position.x = block_x + 1 + PLAYER_WIDTH/2 + 0.01
                    x_collision = True

            # Check Z-axis collision
            if not z_collision:
                # Check +Z direction
                check_pos = glm.vec3(self.position.x, body_y, self.position.z + PLAYER_WIDTH/2 + 0.05)
                if world.is_solid_voxel(check_pos):
                    block_z = int(glm.floor(check_pos.z))
                    self.position.z = block_z - PLAYER_WIDTH/2 - 0.01
                    z_collision = True

                # Check -Z direction
                check_pos = glm.vec3(self.position.x, body_y, self.position.z - PLAYER_WIDTH/2 - 0.05)
                if world.is_solid_voxel(check_pos):
                    block_z = int(glm.floor(check_pos.z))
                    self.position.z = block_z + 1 + PLAYER_WIDTH/2 + 0.01
                    z_collision = True



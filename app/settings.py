import random

from numba import njit
import numpy
import glm
import math

# Window resolution
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
WINDOW_RESOLUTION = glm.vec2(WINDOW_WIDTH, WINDOW_HEIGHT)

# World generation
SEED = random.randrange(1, 10000)
print(SEED)

# FPS
MAX_FPS = 120

# Game title
GAME_TITLE = "Ubiquitous Cube Game"

# Ray casting settings
MAX_RAY_DIST = 6

# Colors
BG_COLOR = glm.vec3(0.58, 0.83, 0.99)

# Chunk
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)

# World
WORLD_WIDTH, WORLD_HEIGHT = 30, 3
WORLD_DEPTH = WORLD_WIDTH
WORLD_AREA = WORLD_WIDTH * WORLD_DEPTH
WORLD_VOL = WORLD_AREA * WORLD_HEIGHT

# World Center
CENTER_XZ = WORLD_WIDTH * H_CHUNK_SIZE
CENTER_Y = WORLD_HEIGHT * H_CHUNK_SIZE

# Camera
ASPECT_RATIO = WINDOW_RESOLUTION.x / WINDOW_RESOLUTION.y
FOV_DEG = 85
V_FOV = glm.radians(FOV_DEG)  # Vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # Horizontal FOV
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# Player
PLAYER_SPEED = 0.005
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, 75, CENTER_XZ)  # Spawn above typical terrain height
MOUSE_SENSITIVITY = 0.002

# Physics (tuned for delta_time in milliseconds, Minecraft-like)
GRAVITY = 0.00004  # Acceleration per millisecond (stronger gravity)
JUMP_STRENGTH = 0.009  # Initial upward velocity (lower jump)
TERMINAL_VELOCITY = 0.05  # Maximum fall speed
PLAYER_HEIGHT = 1.8
PLAYER_WIDTH = 0.6

# Water physics
WATER_DRAG = 0.5  # Movement speed multiplier in water (Minecraft-like resistance)
WATER_GRAVITY = 0.000005  # Very reduced gravity in water (strong buoyancy)
WATER_TERMINAL_VELOCITY = 0.015  # Slower fall speed in water
SWIM_SPEED = 0.006  # Vertical swim speed (spacebar in water)

# Terrain levels
SNOW_LVL = 55
STONE_LVL = 48
DIRT_LVL = 42
GRASS_LVL = 30
SAND_LVL = 20
WATER_LVL = 32  # Sea level - valleys below this fill with water

# Block settings
TOTAL_BLOCKS = 16

# Tree settings
TREE_PROBABILITY = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

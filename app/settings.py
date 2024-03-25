import random

from numba import njit
import numpy
import glm
import math

# Window resolution
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_RESOLUTION = glm.vec2(WINDOW_WIDTH, WINDOW_HEIGHT)

# World generation
SEED = random.randrange(1, 1000000)
print(SEED)

# FPS
MAX_FPS = 1000

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
FOV_DEG = 70
V_FOV = glm.radians(FOV_DEG)  # Vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # Horizontal FOV
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# Player
PLAYER_SPEED = 0.0085  # Set to 0.05 for fast flying
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, WORLD_HEIGHT * CHUNK_SIZE, CENTER_XZ)
MOUSE_SENSITIVITY = 0.002

# Terrain levels
SNOW_LVL = 55
STONE_LVL = 48
DIRT_LVL = 41
GRASS_LVL = 10
SAND_LVL = 6

# Tree settings
TREE_PROBABILITY = 0.018
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

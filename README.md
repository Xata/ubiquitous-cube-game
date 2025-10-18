# ubiquitous-cube-game

A Minecraft-inspired voxel engine tech demo built with Python and modern OpenGL.

<p align="center">

<img src="app/assets/icon.png" alt="Ubiquitous Cube Game icon" width="25%"/>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenGL](https://img.shields.io/badge/OpenGL-%23FFFFFF.svg?style=for-the-badge&logo=opengl)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

</p>

## Project Goal

The goal of this project is to create a 3D voxel engine tech demo reminiscent of Minecraft, written in Python, that runs on Windows 11 and macOS. Features include infinite world generation, procedural terrain with mountain valleys, cave systems, ore generation, and realistic water rendering.

## Installation

Requirements:

- 🐍 Python 3.13+ installed
- ⚙️ GPU capable of OpenGL 3.3+

Next, clone the repository to your local machine:

```zsh
git clone https://github.com/Xata/ubiquitous-cube-game.git
```

Navigate into the project directory:

```zsh
cd ubiquitous-cube-game
```

Create a virtual environment with venv:

```zsh
python -m venv .venv
```

⚠️ Be sure to activate the virtual environment before the next step!

⚠️ On Windows 10/11 you may need to change the execution policy of scripts by running:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Install the dependencies:

```zsh

pip install -r requirements.txt
```

## Running the game

Once installed run the game:

```zsh
python main.py
```

Logs are automatically saved to `logs/game_TIMESTAMP.log` for debugging and tracking game sessions.

## Features

### Infinite World Generation

Explore endlessly! The world generates infinitely as you move, with chunks loading and unloading dynamically (just like Minecraft). Configurable render distance of 8 chunks (256 blocks).

### Procedural Terrain

Colorado-style mountain valleys generated using multi-octave OpenSimplex noise with:

- Rolling hills and gentle valleys
- Dramatic cliff faces and mountain peaks
- Natural-looking ridges and slopes
- Seed-based generation (printed at startup for reproducibility)

### Cave Systems

3D noise-based cave generation creates natural underground networks throughout the world.

### Ore Generation

Random ore veins spawn at specific depth ranges:

- Coal ore (common, near surface)
- Copper ore (medium depth)
- Tin ore (medium depth)

### Water Rendering

Realistic water system with:

- Natural lakes and ocean basins in valleys (sea level: y=32)
- Transparent rendering with 65% alpha
- Blue tint and underwater fog effects
- Surface reflections with Fresnel effect
- Animated wave ripples on water surface
- Swimming mechanics with modified physics

### Trees

Procedural tree generation on grass blocks with randomized placement.

## Gameplay

Below you can find a picture of a house built with the current blocks:
![All current blocks](/resources/images/cube-game-screenshot-03.jpg)

The current controls are:

| Key | Action |
|------|--------|
| W | Move forward |
| S | Move backward |
| A | Move left |
| D | Move right |
| SPACE | Jump |
| G | Toggle game mode (DEBUG ↔ GAME) |
| Left Mouse Btn | Place/remove block (depends on mode) |
| Right Mouse Btn | Switch mode (place/delete) |
| Middle Mouse Btn | Pick block |
| Scroll / - / + | Change selected block |
| P | Switch mode (place/delete) |
| ESC | Exit |

**Game Modes:**

- **DEBUG mode**: Creative mode with flight, no restrictions (default)
- **GAME mode**: Survival mode (coming soon - will have inventory, health, hunger)

**Block Interaction Modes:**

- **Delete mode**: Left-click removes blocks (red highlight)
- **Place mode**: Left-click places selected block (ghost preview)

Note: The selected block and current mode are printed to the console and logged to the log file.

### Available blocks

The blocks below are defined in app.blocks.block_type.py!

![All current blocks](/resources/images/cube-game-screenshot-01.jpg)

The current blocks that are placeable are:

| Block name           | Block ID |
|----------------------|----------|
| VOID                 | 0        |
| SAND                 | 1        |
| GRASS                | 2        |
| DIRT                 | 3        |
| STONE                | 4        |
| SNOW                 | 5        |
| LEAVES               | 6        |
| WOOD                 | 7        |
| COAL_ORE             | 8        |
| RAW_COAL_BLOCK       | 9        |
| COPPER_ORE           | 10       |
| RAW_COPPER_BLOCK     | 11       |
| TIN_ORE              | 12       |
| RAW_TIN_BLOCK        | 13       |
| WOOD_BLOCK           | 14       |
| BASIC_CRAFTING_TABLE | 15       |
| WATER                | 16       |

![Example of ore being generated within the caves](/resources/images/cube-game-screenshot-02.jpg)

## Technical Details

### Performance Optimizations

- **Numba JIT compilation** on terrain generation and mesh building (critical hot paths)
- **Greedy meshing** with face culling - only renders faces adjacent to air/transparent blocks
- **Frustum culling** - only visible chunks are rendered
- **Vertex packing** - 1 uint32 per vertex (position, voxel_id, face_id, ambient occlusion, flip_id)
- **Chunk-based rendering** with dynamic load/unload
- **Two-pass rendering** for proper water transparency

### Architecture

- **Chunk system**: 32×32×32 voxel regions with individual meshes
- **World system**: Dictionary-based infinite chunk storage
- **Player physics**: Gravity, jumping, collision detection, swimming
- **Camera**: First-person view with frustum culling
- **Voxel interaction**: Raycasting for block placement/removal

### Rendering

- Modern OpenGL 3.3+ core profile
- GLSL shaders for chunk and voxel marker rendering
- Texture atlas for all block types
- Ambient occlusion for lighting
- Alpha blending for water transparency

## Credits

Built with:

- [ModernGL](https://moderngl.readthedocs.io/en/5.8.2/) - Modern OpenGL wrapper
- [OpenSimplex](https://github.com/lmas/opensimplex) - Noise generation
- [Numba](https://numba.pydata.org/) - JIT compilation for performance
- [Pygame](https://www.pygame.org/) - Window management and input
- [PyGLM](https://github.com/Zuzu-Typ/PyGLM) - OpenGL mathematics

## License

MIT License - See LICENSE file for details

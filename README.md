# ubiquitous-cube-game
A Minecraft clone implementation in Python using modern OpenGL.

<p align="center">
<img src="app/assets/icon.png" alt="Ubiquitous Cube Game icon" width="25%"/>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenGL](https://img.shields.io/badge/OpenGL-%23FFFFFF.svg?style=for-the-badge&logo=opengl)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

</p>

## Project Goal

The goal of this project is to create a simple Minecraft clone written in Python that can run on Windows 11 and macOS.

## Installation

Requirements:
- 🐍 Python 3.13+ installed (As of May 2025)
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

## Gameplay

Below you can find a picture of a house built with the current blocks:
![All current blocks](/resources/images/cube-game-screenshot-03.jpg)

The current controls are:

| Key | Action |
|------|--------|
| W | Move Forward |
| S | Move Backward |
| A | Move Left |
| D | Move Right |
| Q | Move Up |
| E | Move Down |
| Left Mouse Btn | Block Action |
| Right Mouse Btn | Change block Action |
| Middle Mouse Btn | Change active block to place |
| ESC | Exit |

Note: To change the block you need to place press the middle mouse button. The selected block will be printed in the console.

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

Generates a random world each time using ![OpenSimplex](https://github.com/lmas/opensimplex)

There is also ore generation within the cave systems:

![Example of ore being generated within the caves](/resources/images/cube-game-screenshot-02.jpg)

## Credits

The following was used to create the base game:

- ![ModernGL](https://moderngl.readthedocs.io/en/5.8.2/)
- ![OpenSimplex](https://github.com/lmas/opensimplex)
- ![Numba](https://numba.pydata.org/)
- ![David Wolff's OpenGL 4 Shading Language Cookbook](https://www.amazon.com/OpenGL-Shading-Language-Cookbook-high-quality/dp/1789342252)
- ![Coder Space's Creating a Voxel Engine Tutorial](https://www.youtube.com/watch?v=Ab8TOSFfNp4)
- ![Alan Zucconi's How Minecraft ACTUALLY Works](https://www.youtube.com/watch?v=YyVAaJqYAfE&t=973s)

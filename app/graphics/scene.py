import moderngl
from app.world_utils.world import World
from .voxel_marker import VoxelMarker
from .block_preview import BlockPreview
from .sky import Sky


class Scene:
    """
    Represents a scene in the game, managing the world and voxel marker.

    Attributes:
        app: The application object
        sky: The sky renderer
        world: The world object containing the environment
        voxel_marker: The voxel marker object used for marking voxels
    """

    def __init__(self, app):
        """
        Initializes a Scene object .

        Args:
            app: The game object
        """
        self.app = app
        self.sky = Sky(self.app)
        self.world = World(self.app)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)
        self.block_preview = BlockPreview(self.app)

    def update(self):
        """
        Updates the scene by updating the world and voxel marker.
        """
        self.world.update()
        self.voxel_marker.update()
        self.block_preview.update()

    def render(self):
        """
        Renders the scene by rendering the sky, world, and voxel marker.
        """
        self.sky.render()  # Render sky first (background)
        self.world.render()
        self.voxel_marker.render()

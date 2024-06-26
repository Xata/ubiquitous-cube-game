from app.world_utils.world import World
from .voxel_marker import VoxelMarker


class Scene:
    """
    Represents a scene in the game, managing the world and voxel marker.

    Attributes:
        app: The application object
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
        self.world = World(self.app)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)

    def update(self):
        """
        Updates the scene by updating the world and voxel marker.
        """
        self.world.update()
        self.voxel_marker.update()

    def render(self):
        """
        Renders the scene by rendering the world and voxel marker.
        """
        self.world.render()
        self.voxel_marker.render()

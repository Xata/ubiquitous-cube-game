from app.settings import *
from app.meshes.cube_mesh import CubeMesh


class VoxelMarker:
    """
    Represents a marker indicating the selected voxel in the world.

    Attributes:
        app: The application object
        handler: The voxel handler object
        position: The position of the marker in 3D space
        m_model: The model matrix of the marker
        mesh: The mesh representing the marker
    """

    def __init__(self, voxel_handler):
        """
        Initializes a VoxelMarker object with the given voxel handler.

        Args:
            voxel_handler: The voxel handler object
        """

        self.app = voxel_handler.app
        self.handler = voxel_handler
        self.position = glm.vec3(0)
        self.m_model = self.get_model_matrix()
        self.mesh = CubeMesh(self.app)

    def update(self):
        """
        Updates the position of the marker based on the voxel handler's state.
        """

        if self.handler.voxel_id:
            if self.handler.interaction_mode:
                self.position = self.handler.voxel_world_position + self.handler.voxel_normal
            else:
                self.position = self.handler.voxel_world_position

    def set_uniform(self):
        """
         Sets the uniform values for rendering the marker.
         """

        self.mesh.program['mode_id'] = self.handler.interaction_mode
        self.mesh.program['m_model'].write(self.get_model_matrix())

    def get_model_matrix(self):
        """
        Calculates the model matrix of the marker.

        Returns:
            glm.mat4: The model matrix
        """

        m_model = glm.translate(glm.mat4(), glm.vec3(self.position))
        return m_model

    def render(self):
        """
        Renders the marker if a voxel is selected.
        """

        if self.handler.voxel_id:
            self.set_uniform()
            self.mesh.render()

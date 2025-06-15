from app.settings import *

class Camera:
    """
    Represents a camera in the game's 3D environment.

    Attributes:
        position (glm.vec3): The position of the camera in 3D space
        yaw (float): The yaw angle of the camera in radians
        pitch (float): The pitch angle of the camera in radians
        up (glm.vec3): The upward direction vector relative to the camera
        right (glm.vec3): The rightward direction vector relative to the camera
        forward (glm.vec3): The forward direction vector relative to the camera
        m_proj (glm.mat4): The projection matrix of the camera
        m_view (glm.mat4): The view matrix of the camera
        frustum (Frustum): The frustum object representing the camera's view volume
    """
    def __init__(self, position, yaw, pitch):
        """
        Inits the Camera object with a given position, yaw, and pitch angles.

        Args:
            position (tuple): The x, y, z coordinates of the camera
            yaw (float): The yaw angle of the camera in degrees
            pitch (float): The pitch angle of the camera in degrees
        """
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        # Define direction vectors
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        # Initialize projection and view matrices
        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

        # Create frustum object
        self.frustum = Frustum(self)

    def update(self):
        """
        Updates the camera
        """
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        """
        Updates the view matrix of the camera based on its position and orientation using lookAt()
        """
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        """
         Updates the camera's direction vectors based on its yaw and pitch angles.
        """
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    # Below are functions to move the camera around
    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def move_left(self, velocity):
        self.position -= self.right * velocity

    def move_right(self, velocity):
        self.position += self.right * velocity

    def move_up(self, velocity):
        self.position += self.up * velocity

    def move_down(self, velocity):
        self.position -= self.up * velocity

    def move_forward(self, velocity):
        self.position += self.forward * velocity

    def move_backward(self, velocity):
        self.position -= self.forward * velocity

class Frustum:
    """
    Represents a frustum for culling objects in the camera's view volume.

    Attributes:
        cam (Camera): The camera associated with this frustum
        factor_y (float): The reciprocal of the cosine of half the vertical field of view angle
        tan_y (float): The tangent of half the vertical field of view angle
        factor_x (float): The reciprocal of the cosine of half the horizontal field of view angle
        tan_x (float): The tangent of half the horizontal field of view angle
    """

    def __init__(self, cam):
        """
        Initializes a Frustum object with the given camera.

        Args:
            cam (Camera): The camera associated with this frustum
        """
        self.cam: Camera = cam

        # Calculate factors and tangents for field of view angles
        self.factor_y = 1.0 / math.cos(half_y := V_FOV * 0.5)
        self.tan_y = math.tan(half_y)

        self.factor_x = 1.0 / math.cos(half_x := H_FOV * 0.5)
        self.tan_x = math.tan(half_x)

    def is_on_frustum(self, chunk):
        """
        Checks if a chunk is inside the frustum.

        Args:
            chunk: The chunk to be checked

        Returns:
            bool: True if the chunk is inside the frustum
        """

        # Calculate vector to the center of the chunk from the camera position
        sphere_vec = chunk.center - self.cam.position

        # Check if the chunk is outside the NEAR and FAR planes
        sz = glm.dot(sphere_vec, self.cam.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS):
            return False

        # Check if the chunk is outside the TOP and BOTTOM planes
        sy = glm.dot(sphere_vec, self.cam.up)
        dist = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y
        if not (-dist <= sy <= dist):
            return False

        # Check if the chunk is outside the LEFT and RIGHT planes
        sx = glm.dot(sphere_vec, self.cam.right)
        dist = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x
        if not (-dist <= sx <= dist):
            return False

        return True

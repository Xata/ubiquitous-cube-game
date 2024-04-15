from app.settings import SEED
from numba import njit

# Import protected internals because of numba
# Ignore the warning from IDEs
from opensimplex.internals import _noise2, _noise3, _init
import opensimplex

# Initialize permutation tables for noise generation using the seed
perm, perm_grad_index3 = _init(seed=SEED)

#perm, perm_grad_index3 = opensimplex.seed(SEED)

@njit(cache=True)
def noise2(x, y):
    """
    Generate 2D simplex noise value at the given coordinates.

    Args:
        x (float): X-coordinate of the point
        y (float): Y-coordinate of the point

    Returns:
        float: Simplex noise value at the specified coordinates
    """

    return _noise2(x, y, perm)


@njit(cache=True)
def noise3(x, y, z):
    """
    Generate 3D simplex noise value at the given coordinates.

    Args:
        x (float): X-coordinate of the point
        y (float): Y-coordinate of the point
        z (float): Z-coordinate of the point

    Returns:
        float: Simplex noise value at the specified coordinates
    """
    return _noise3(x, y, z, perm, perm_grad_index3)

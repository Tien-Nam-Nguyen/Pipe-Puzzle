from pygame.math import Vector2


def quadratic_bezier(
    start: Vector2,
    mid: Vector2,
    end: Vector2,
    t: float,
):
    """Generate the positions of a quadratic bezier curve.

    Args:
        start (tuple[float, float]): The starting point.
        mid (tuple[float, float]): The middle handle.
        end (tuple[float, float]): The ending point.
        t (float): Offset. Range [0, 1]. 0 returns the starting point, 1 returns the ending point.

    Returns:
        tuple[float, float]: The position of the point on the curve.
    """
    x = (1 - t) ** 2 * start.x + 2 * (1 - t) * t * mid.x + t**2 * end.x
    y = (1 - t) ** 2 * start.y + 2 * (1 - t) * t * mid.y + t**2 * end.y
    return x, y

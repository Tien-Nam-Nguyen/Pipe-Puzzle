from ..GameState import Coordinate


def on_segment(p: Coordinate, q: Coordinate, r: Coordinate) -> bool:
    """Given three collinear points `p`, `q`, `r`, the function checks if
    point `q` lies on line segment (`p`, `r`).

    Args:
        p (Coordinate): The starting point of the line segment.
        q (Coordinate): The point to check if it lies on the line segment.
        r (Coordinate): The ending point of the line segment.

    Returns:
        bool: True if `q` lies on the line segment (`p`, `r`), False otherwise.
    """
    if (
        (q.x <= max(p.x, r.x))
        and (q.x >= min(p.x, r.x))
        and (q.y <= max(p.y, r.y))
        and (q.y >= min(p.y, r.y))
    ):
        return True
    return False


def orientation(p: Coordinate, q: Coordinate, r: Coordinate) -> int:
    """Find the orientation of an ordered triplet (`p`, `q`, `r`).
    See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    for details of below formula.

    Args:
        p (Coordinate): _description_
        q (Coordinate): _description_
        r (Coordinate): _description_

    Returns:
        int: 0 : Collinear points, 1 : Clockwise points, 2 : Counterclockwise
    """

    val = ((q.y - p.y) * (r.x - q.x)) - ((q.x - p.x) * (r.y - q.y))
    if val > 0:
        return 1
    elif val < 0:
        return 2
    else:
        return 0


def is_intersecting(
    line_a: tuple[Coordinate, Coordinate], line_b: tuple[Coordinate, Coordinate]
) -> bool:
    """Given two line segments `line_a` and `line_b`, the function checks if
    the two line segments intersect.

    Args:
        line_a (tuple[Coordinate, Coordinate]): Line segment 1.
        line_b (tuple[Coordinate, Coordinate]): Line segment 2.

    Returns:
        bool: True if the two line segments intersect, False otherwise.
    """
    p1, q1 = line_a
    p2, q2 = line_b

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2) and (o3 != o4):
        return True

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if (o1 == 0) and on_segment(p1, p2, q1):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if (o2 == 0) and on_segment(p1, q2, q1):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if (o3 == 0) and on_segment(p2, p1, q2):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if (o4 == 0) and on_segment(p2, q1, q2):
        return True

    return False

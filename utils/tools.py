from pygame.math import Vector2
from random import uniform
import math


PI = math.pi
TAU = math.tau
    
    
def get_angle_direction(
        angle: float, 
        degrees: bool=False, 
        error: float=0, 
        offset: float=0, 
        return_angle: bool=False
        ) -> Vector2 | dict[float, Vector2]:
    """
    Returns the normalized vector from a given angle, radian by default.
    Specify an error to introduce randomized spread.\n
    Specify an offset to offset the direction.
    It can also return the result angle.
    """
    radian = math.radians(angle) if degrees else angle
    radian = get_offset(radian, offset) if offset else radian
    radian = get_error(radian, error) if error else radian
    direction = Vector2(math.cos(radian), -math.sin(radian))
    angle = math.degrees(radian) if degrees else radian 
    if return_angle:
        return {"angle": angle, "direction": direction}
    return direction


def get_scaled_vector(origin_pos: Vector2, end_pos: Vector2, magnitude: float, error: float=0) -> Vector2:
    """
    Returns a position with the same direction as origin to end position, but scaled by a magnitude.\n
    Specify an error to introduce randomized spread.
    """
    radian = get_angle(origin_pos, end_pos, error=error)
    scaled_vector = origin_pos + Vector2(math.cos(radian), -math.sin(radian)) * magnitude
    return scaled_vector


def get_distance(origin_pos: Vector2, end_pos: Vector2) -> float:
    """
    Returns the absolute distance between origin and end position. 
    """
    side_lengths = get_side_lengths(origin_pos, end_pos)
    distance = math.hypot(side_lengths['adjacent'], side_lengths['opposite'])
    return distance


def get_angle(origin_pos: Vector2, end_pos: Vector2, error: float=0, offset: float=0, degrees: bool=False) -> float:
    """
    Returns the angle in radians in default from origin to end position.\n
    Specify if degrees to return degrees instead.
    Specify an error to introduce randomized spread.
    Specify an offset to offset the calculated radian.
    """
    try:
        side_lengths = get_side_lengths(origin_pos, end_pos)
        radian = math.atan(side_lengths['opposite'] / side_lengths['adjacent'])
    except ZeroDivisionError:
        radian = math.pi / 2

    # top left (Q2)
    if end_pos.y <= origin_pos.y and end_pos.x <= origin_pos.x:
        radian = PI - radian
    # bottom left (Q3)
    elif end_pos.y >= origin_pos.y and end_pos.x <= origin_pos.x:
        radian = PI + radian
    # bottom right (Q4)
    elif end_pos.y >= origin_pos.y and end_pos.x >= origin_pos.x:
        radian = TAU - radian

    radian = get_offset(radian, offset) if offset else radian
    radian = get_error(radian, error) if error else radian
    radian = math.degrees(radian) % 360 if degrees else radian
    return radian
    

def get_side_lengths(origin_pos: Vector2, end_pos: Vector2) -> dict:
    """
    Returns the adjacent and opposite lengths based on the given positions.
    """
    adjacent = abs(end_pos.x - origin_pos.x)
    opposite = abs(end_pos.y - origin_pos.y)
    side_lengths = {'adjacent': adjacent, 'opposite': opposite}
    return side_lengths


def get_error(radian: float, error: float) -> float:
    error *= PI 
    radian = uniform(radian - error, radian + error) % TAU 
    return radian


def get_offset(radian: float, offset: float) -> float:
    offset *= PI
    radian = (radian + offset) % TAU
    return radian


def clamp(value: float| int, min_value: float | int, max_value: float | int) -> int | float:
    result = min(max(value, min_value), max_value)
    return result


def lerp(a: float, b: float, t: float) -> float:
    result = (1 - t) * a + t * b
    return result


def invlerp(a: float, b: float, v: float) -> float:
    result = (v - a) / (b - a) if b != v else 1.0
    return result


def remap(a1: float, b1: float, v: float, a2: float, b2: float, is_clamped: bool=True) -> float:
    lerp_val = invlerp(a1, b1, v)
    lerp_val = clamp(lerp_val, 0, 1) if is_clamped else lerp_val
    result = lerp(a2, b2, lerp_val)
    return result


def snap(value: float | int, multiple: float | int) -> float | int:
    result = multiple * round(value / multiple) if multiple else value
    return result

from constants import TILE_SIZE, HUD_HEIGHT, GRID_W, GRID_H


def grid_to_pixel(gx, gy):
    """Convert grid position (col, row) to top-left pixel on screen."""
    return (gx * TILE_SIZE, gy * TILE_SIZE + HUD_HEIGHT)


def pixel_to_grid(px, py):
    """Convert pixel position to grid position."""
    return (px // TILE_SIZE, (py - HUD_HEIGHT) // TILE_SIZE)


def is_in_bounds(gx, gy, grid_w=GRID_W, grid_h=GRID_H):
    """Check if a grid coordinate is within bounds."""
    return 0 <= gx < grid_w and 0 <= gy < grid_h


def manhattan_distance(pos1, pos2):
    """Manhattan distance between two (x,y) grid positions."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def direction_toward(from_pos, to_pos):
    """Returns (dx, dy) that moves from_pos one step closer to to_pos.
    Picks the axis with the largest gap. Used by Bat AI."""
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]
    if dx == 0 and dy == 0:
        return (0, 0)
    if abs(dx) >= abs(dy):
        return (1 if dx > 0 else -1, 0)
    else:
        return (0, 1 if dy > 0 else -1)

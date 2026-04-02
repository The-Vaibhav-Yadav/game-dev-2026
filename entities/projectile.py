from constants import PROJECTILE_SPEED
from utils import is_in_bounds


class Projectile:
    def __init__(self, gx, gy, dx, dy):
        self.gx = gx
        self.gy = gy
        self.dx = dx
        self.dy = dy
        self.alive = True
        self.move_accumulator = 0.0

    def update(self, dt, walls):
        """Move the projectile. Sets alive=False on wall hit or out of bounds."""
        self.move_accumulator += PROJECTILE_SPEED * dt
        while self.move_accumulator >= 1.0 and self.alive:
            self.move_accumulator -= 1.0
            self.gx += self.dx
            self.gy += self.dy
            if not is_in_bounds(self.gx, self.gy) or (self.gx, self.gy) in walls:
                self.alive = False

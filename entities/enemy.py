import random
from constants import (
    SLIME_MOVE_INTERVAL, BAT_MOVE_INTERVAL, TURRET_FIRE_INTERVAL
)
from utils import is_in_bounds, direction_toward
from entities.projectile import Projectile


class Enemy:
    def __init__(self, gx, gy, enemy_type, hp=1):
        self.gx = gx
        self.gy = gy
        self.enemy_type = enemy_type
        self.hp = hp
        self.alive = True
        self.move_timer = 0.0

    def take_damage(self, amount=1):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

    def ai_update(self, dt, player, walls, room_enemies):
        """Override in subclasses. Returns a Projectile or None."""
        raise NotImplementedError


class Slime(Enemy):
    def __init__(self, gx, gy):
        super().__init__(gx, gy, "slime", hp=1)
        self.move_timer = SLIME_MOVE_INTERVAL

    def ai_update(self, dt, player, walls, room_enemies):
        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_timer = SLIME_MOVE_INTERVAL
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = self.gx + dx, self.gy + dy
                if (nx, ny) not in walls and is_in_bounds(nx, ny):
                    occupied = any(
                        e.gx == nx and e.gy == ny
                        for e in room_enemies if e.alive and e is not self
                    )
                    if not occupied:
                        self.gx, self.gy = nx, ny
                        break
        return None


class Bat(Enemy):
    def __init__(self, gx, gy):
        super().__init__(gx, gy, "bat", hp=1)
        self.move_timer = BAT_MOVE_INTERVAL

    def ai_update(self, dt, player, walls, room_enemies):
        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_timer = BAT_MOVE_INTERVAL
            dx, dy = direction_toward((self.gx, self.gy), (player.gx, player.gy))
            nx, ny = self.gx + dx, self.gy + dy
            if (nx, ny) not in walls and is_in_bounds(nx, ny):
                self.gx, self.gy = nx, ny
        return None


class Turret(Enemy):
    def __init__(self, gx, gy):
        super().__init__(gx, gy, "turret", hp=2)
        self.move_timer = TURRET_FIRE_INTERVAL

    def ai_update(self, dt, player, walls, room_enemies):
        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_timer = TURRET_FIRE_INTERVAL
            dx, dy = direction_toward((self.gx, self.gy), (player.gx, player.gy))
            spawn_x, spawn_y = self.gx + dx, self.gy + dy
            # Don't spawn projectile inside a wall
            if is_in_bounds(spawn_x, spawn_y) and (spawn_x, spawn_y) not in walls:
                return Projectile(spawn_x, spawn_y, dx, dy)
        return None

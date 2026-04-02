import pygame
from constants import ATTACK_COOLDOWN, KNOCKBACK_STUN
from utils import is_in_bounds


class Player:
    def __init__(self, grid_x, grid_y):
        self.gx = grid_x
        self.gy = grid_y
        self.facing = (0, 1)       # default: facing down
        self.move_timer = 0.0
        self.attack_timer = 0.0
        self.stun_timer = 0.0
        self.has_key = False
        self.is_attacking = False
        self.attack_visual_timer = 0.0
        self.damage_cooldown = 0.0  # prevents per-frame collision damage

    def get_speed(self, game_state):
        return game_state.get_player_speed()

    def update(self, dt, keys_pressed, walls, game_state):
        """Called every frame by playing_state.
        walls = set of (gx, gy) that are impassable.
        """
        self.attack_timer = max(0, self.attack_timer - dt)
        self.stun_timer = max(0, self.stun_timer - dt)
        self.attack_visual_timer = max(0, self.attack_visual_timer - dt)
        self.damage_cooldown = max(0, self.damage_cooldown - dt)

        if self.attack_visual_timer <= 0:
            self.is_attacking = False

        if self.stun_timer > 0:
            return None

        # --- Movement ---
        speed = self.get_speed(game_state)
        move_delay = 1.0 / speed
        self.move_timer -= dt

        dx, dy = 0, 0
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            dx, dy = 0, -1
        elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            dx, dy = 0, 1
        elif keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            dx, dy = -1, 0
        elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            dx, dy = 1, 0

        if (dx, dy) != (0, 0):
            self.facing = (dx, dy)
            if self.move_timer <= 0:
                new_x = self.gx + dx
                new_y = self.gy + dy
                if (new_x, new_y) not in walls and is_in_bounds(new_x, new_y):
                    self.gx = new_x
                    self.gy = new_y
                    self.move_timer = move_delay

        return None

    def try_attack(self, game_state):
        """Called by playing_state when spacebar is pressed.
        Returns the grid position being attacked, or None."""
        if not game_state.has("combat"):
            return None
        if self.attack_timer > 0:
            return None
        self.attack_timer = ATTACK_COOLDOWN
        self.is_attacking = True
        self.attack_visual_timer = 0.15
        target_x = self.gx + self.facing[0]
        target_y = self.gy + self.facing[1]
        return (target_x, target_y)

    def apply_knockback(self, from_gx, from_gy, walls):
        """Push player 1 tile away from (from_gx, from_gy). Apply stun."""
        dx = self.gx - from_gx
        dy = self.gy - from_gy
        if dx == 0 and dy == 0:
            dx = 1
        push_x = self.gx + (1 if dx > 0 else -1 if dx < 0 else 0)
        push_y = self.gy + (1 if dy > 0 else -1 if dy < 0 else 0)
        if (push_x, push_y) not in walls and is_in_bounds(push_x, push_y):
            self.gx = push_x
            self.gy = push_y
        self.stun_timer = KNOCKBACK_STUN

import pygame
from constants import (
    SCREEN_W, HUD_HEIGHT, GRID_W, GRID_H, TILE_SIZE,
    COLOR_HUD_BG, COLOR_HUD_TEXT, COLOR_COIN
)
from utils import grid_to_pixel


class HUD:
    def __init__(self, assets):
        self.assets = assets
        self.font = pygame.font.SysFont("Courier", 20)
        self.font_large = pygame.font.SysFont("Courier", 28)

    def draw(self, screen, run_gold, tax_rate, room_number, game_state,
             enemies=None, player=None, walls=None):
        # --- HUD Background ---
        pygame.draw.rect(screen, COLOR_HUD_BG, (0, 0, SCREEN_W, HUD_HEIGHT))

        # --- Gold counter ---
        gold_text = self.font_large.render(f"GOLD: {int(run_gold)}", True, COLOR_COIN)
        screen.blit(gold_text, (10, 10))

        # --- Tax rate ---
        tax_text = self.font.render(f"TAX: {tax_rate:.1f}g/s", True, (200, 80, 80))
        screen.blit(tax_text, (10, 45))

        # --- Room number ---
        room_text = self.font.render(f"ROOM {room_number}", True, COLOR_HUD_TEXT)
        screen.blit(room_text, (SCREEN_W - 120, 10))

        # --- Persistent gold ---
        pgold_text = self.font.render(f"BANK: {int(game_state.gold)}g", True, (120, 200, 120))
        screen.blit(pgold_text, (SCREEN_W - 160, 45))

        # --- HUD Upgrade extras ---
        if game_state.has("hud_upgrade"):
            self._draw_minimap(screen, player, enemies, walls)

    def _draw_minimap(self, screen, player, enemies, walls):
        """Small 100x100 minimap in top-right corner area, shifted left."""
        map_x, map_y = SCREEN_W - 270, 5
        map_size = 70
        cell = map_size // GRID_W

        # Background
        pygame.draw.rect(screen, (15, 15, 15), (map_x - 2, map_y - 2, map_size + 4, map_size + 4))
        pygame.draw.rect(screen, (30, 30, 30), (map_x, map_y, map_size, map_size))

        # Walls
        if walls:
            for (wx, wy) in walls:
                pygame.draw.rect(screen, (80, 80, 80),
                    (map_x + wx * cell, map_y + wy * cell, cell, cell))

        # Player dot
        if player:
            pygame.draw.rect(screen, (0, 255, 0),
                (map_x + player.gx * cell, map_y + player.gy * cell, cell, cell))

        # Enemy dots
        if enemies:
            for e in enemies:
                if e.alive:
                    pygame.draw.rect(screen, (255, 0, 0),
                        (map_x + e.gx * cell, map_y + e.gy * cell, cell, cell))

    def draw_enemy_hp_bar(self, screen, enemy):
        """Draw a small HP bar above an enemy."""
        px, py = grid_to_pixel(enemy.gx, enemy.gy)
        bar_w = 40
        bar_h = 4
        bar_x = px + (TILE_SIZE - bar_w) // 2
        bar_y = py - 6
        # background
        pygame.draw.rect(screen, (80, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        # fill
        max_hp = 2 if enemy.enemy_type == "turret" else 1
        fill_w = int(bar_w * (enemy.hp / max_hp))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, fill_w, bar_h))

import pygame
from states.base_state import BaseState
from constants import SCREEN_W, SCREEN_H, COLOR_BG, STATE_SHOP


class DeadState(BaseState):
    def __init__(self, game_state, assets, audio):
        super().__init__(game_state, assets, audio)
        self.timer = 0.0
        self.font_large = None
        self.font_small = None
        self.gold_earned = 0

    def enter(self):
        self.timer = 1.5
        self.font_large = pygame.font.SysFont("Courier", 64, bold=True)
        self.font_small = pygame.font.SysFont("Courier", 20)
        self.gold_earned = 0  # Set by playing_state before transition if needed
        self.audio.play_sfx("player_death")

    def update(self, dt, events):
        self.timer -= dt
        if self.timer <= 0:
            return STATE_SHOP
        return None

    def draw(self, screen):
        screen.fill(COLOR_BG)

        # BANKRUPT text with slight red pulse
        import math
        pulse = int(200 + 55 * math.sin(pygame.time.get_ticks() / 100.0))
        color = (pulse, 30, 30)

        bankrupt_surf = self.font_large.render("BANKRUPT", True, color)
        bankrupt_rect = bankrupt_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 30))
        screen.blit(bankrupt_surf, bankrupt_rect)

        # Stats
        deaths_text = f"Total Deaths: {self.game_state.total_deaths}"
        deaths_surf = self.font_small.render(deaths_text, True, (150, 150, 150))
        deaths_rect = deaths_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 40))
        screen.blit(deaths_surf, deaths_rect)

        gold_text = f"Bank: {self.game_state.gold}g"
        gold_surf = self.font_small.render(gold_text, True, (200, 180, 50))
        gold_rect = gold_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 70))
        screen.blit(gold_surf, gold_rect)

        # Redirect hint
        hint_surf = self.font_small.render("Redirecting to shop...", True, (80, 80, 80))
        hint_rect = hint_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H - 40))
        screen.blit(hint_surf, hint_rect)

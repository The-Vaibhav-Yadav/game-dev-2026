import pygame
from states.base_state import BaseState
from constants import SCREEN_W, SCREEN_H, COLOR_BG, STATE_TITLE


class VictoryState(BaseState):
    def __init__(self, game_state, assets, audio):
        super().__init__(game_state, assets, audio)
        self.font_title = None
        self.font_large = None
        self.font_small = None

    def enter(self):
        self.font_title = pygame.font.SysFont("Courier", 48, bold=True)
        self.font_large = pygame.font.SysFont("Courier", 28)
        self.font_small = pygame.font.SysFont("Courier", 20)
        self.audio.stop_music()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                return STATE_TITLE
        return None

    def draw(self, screen):
        screen.fill(COLOR_BG)

        # Title
        title_surf = self.font_title.render("DEBT: PAID", True, (50, 255, 100))
        title_rect = title_surf.get_rect(center=(SCREEN_W // 2, 120))
        screen.blit(title_surf, title_rect)

        subtitle_surf = self.font_large.render("YOU OWN THE GAME", True, (200, 200, 200))
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_W // 2, 180))
        screen.blit(subtitle_surf, subtitle_rect)

        # Stats
        stats = [
            f"Total Runs: {self.game_state.run_count}",
            f"Total Deaths: {self.game_state.total_deaths}",
            f"Total Gold Earned: {self.game_state.total_gold_earned}g",
            f"Items Purchased: {sum(1 for v in self.game_state.purchased.values() if v)}/10",
        ]

        y = 260
        for stat in stats:
            stat_surf = self.font_small.render(stat, True, (180, 180, 180))
            stat_rect = stat_surf.get_rect(center=(SCREEN_W // 2, y))
            screen.blit(stat_surf, stat_rect)
            y += 35

        # Prompt
        prompt_surf = self.font_small.render("> Press Any Key <", True, (120, 120, 120))
        prompt_rect = prompt_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H - 60))
        screen.blit(prompt_surf, prompt_rect)

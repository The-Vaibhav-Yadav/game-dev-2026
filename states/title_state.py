import pygame
from states.base_state import BaseState
from constants import SCREEN_W, SCREEN_H, COLOR_BG, STATE_SHOP


class TitleState(BaseState):
    def __init__(self, game_state, assets, audio):
        super().__init__(game_state, assets, audio)
        self.blink_timer = 0.0
        self.show_prompt = True
        self.font_title = None
        self.font_prompt = None
        self.font_sub = None

    def enter(self):
        self.blink_timer = 0.0
        self.show_prompt = True
        self.font_title = pygame.font.SysFont("Courier", 52, bold=True)
        self.font_prompt = pygame.font.SysFont("Courier", 22)
        self.font_sub = pygame.font.SysFont("Courier", 16)

    def update(self, dt, events):
        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.blink_timer = 0.0
            self.show_prompt = not self.show_prompt

        for event in events:
            if event.type == pygame.KEYDOWN:
                return STATE_SHOP

        return None

    def draw(self, screen):
        screen.fill(COLOR_BG)

        # Title
        title_surf = self.font_title.render("DEBT DUNGEON", True, (200, 50, 50))
        title_rect = title_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3))
        screen.blit(title_surf, title_rect)

        # Subtitle
        sub_surf = self.font_sub.render("[ YOU OWE EVERYTHING ]", True, (120, 120, 120))
        sub_rect = sub_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3 + 50))
        screen.blit(sub_surf, sub_rect)

        # Blinking prompt
        if self.show_prompt:
            prompt_surf = self.font_prompt.render("> Press Any Key <", True, (180, 180, 180))
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H * 2 // 3))
            screen.blit(prompt_surf, prompt_rect)

        # Version / flavor
        ver_surf = self.font_sub.render("v0.1 - NO FEATURES INSTALLED", True, (60, 60, 60))
        ver_rect = ver_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H - 30))
        screen.blit(ver_surf, ver_rect)

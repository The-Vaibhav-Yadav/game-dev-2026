import pygame
from states.base_state import BaseState
from constants import SCREEN_W, SCREEN_H, COLOR_BG, STATE_PLAYING
from data.shop_items import SHOP_ITEMS


class ShopState(BaseState):
    def __init__(self, game_state, assets, audio):
        super().__init__(game_state, assets, audio)
        self.font_title = None
        self.font_item = None
        self.font_small = None
        self.font_flavor = None
        self.font_btn = None
        self.scroll_offset = 0
        self.max_scroll = 0
        self.cards = []
        self.start_button_rect = None
        self.flash_timer = 0.0
        self.flash_item = None

    def enter(self):
        self.font_title = pygame.font.SysFont("Courier", 32, bold=True)
        self.font_item = pygame.font.SysFont("Courier", 18, bold=True)
        self.font_small = pygame.font.SysFont("Courier", 14)
        self.font_flavor = pygame.font.SysFont("Courier", 12)
        self.font_btn = pygame.font.SysFont("Courier", 22, bold=True)
        self.scroll_offset = 0
        self.flash_timer = 0.0
        self.flash_item = None
        self._build_cards()
        self.audio.play_music("bgm_shop")

    def exit(self):
        self.audio.stop_music()

    def _build_cards(self):
        """Build card rectangles for each item."""
        self.cards = []
        card_w = SCREEN_W - 60
        card_h = 80
        x = 30
        y_start = 90
        gap = 8

        for i, item in enumerate(SHOP_ITEMS):
            y = y_start + i * (card_h + gap)
            rect = pygame.Rect(x, y, card_w, card_h)
            self.cards.append({"item": item, "rect": rect, "index": i})

        total_height = y_start + len(SHOP_ITEMS) * (card_h + gap) + 80
        self.max_scroll = max(0, total_height - SCREEN_H + 30)

        # Start run button
        btn_w, btn_h = 200, 50
        btn_y = y_start + len(SHOP_ITEMS) * (card_h + gap) + 10
        self.start_button_rect = pygame.Rect(
            (SCREEN_W - btn_w) // 2, btn_y, btn_w, btn_h
        )

    def update(self, dt, events):
        self.flash_timer = max(0, self.flash_timer - dt)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                my_adjusted = my + self.scroll_offset

                # Check start button
                btn = self.start_button_rect.copy()
                btn.y -= self.scroll_offset
                if btn.collidepoint(mx, my):
                    self.game_state.start_new_run()
                    return STATE_PLAYING

                # Check item cards
                for card_data in self.cards:
                    card_rect = card_data["rect"].copy()
                    card_rect.y -= self.scroll_offset
                    if card_rect.collidepoint(mx, my):
                        item = card_data["item"]
                        self._try_buy(item)

            # Scroll
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= event.y * 30
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

            # Keyboard scroll
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state.start_new_run()
                    return STATE_PLAYING

        # Arrow key scrolling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.scroll_offset = max(0, self.scroll_offset - 5)
        if keys[pygame.K_DOWN]:
            self.scroll_offset = min(self.max_scroll, self.scroll_offset + 5)

        return None

    def _try_buy(self, item):
        key = item["key"]
        if self.game_state.has(key):
            return  # already owned
        prereq = item["requires"]
        if prereq is not None and not self.game_state.has(prereq):
            return  # prereq not met
        if self.game_state.gold < item["cost"]:
            return  # can't afford
        # Purchase!
        self.game_state.gold -= item["cost"]
        self.game_state.purchased[key] = True
        self.audio.play_sfx_always("purchase")
        self.flash_item = key
        self.flash_timer = 0.3

    def draw(self, screen):
        # Background — fake OS desktop feel
        screen.fill((25, 25, 35))

        # Draw "desktop" pattern
        for x in range(0, SCREEN_W, 40):
            for y in range(0, SCREEN_H, 40):
                pygame.draw.rect(screen, (28, 28, 38), (x, y, 39, 39))

        # Window chrome
        pygame.draw.rect(screen, (40, 40, 55), (10, 10, SCREEN_W - 20, SCREEN_H - 20), border_radius=8)
        pygame.draw.rect(screen, (60, 60, 80), (10, 10, SCREEN_W - 20, SCREEN_H - 20), 2, border_radius=8)

        # Title bar
        pygame.draw.rect(screen, (50, 50, 70), (10, 10, SCREEN_W - 20, 40), border_radius=8)
        pygame.draw.rect(screen, (50, 50, 70), (10, 40, SCREEN_W - 20, 15))

        title_surf = self.font_title.render("SYSTEM SHOP", True, (220, 220, 220))
        screen.blit(title_surf, (25, 15))

        # Gold display
        gold_surf = self.font_item.render(f"GOLD: {self.game_state.gold}g", True, (255, 215, 0))
        screen.blit(gold_surf, (SCREEN_W - 180, 20))

        # Window buttons (decorative)
        for i, color in enumerate([(200, 60, 60), (200, 200, 60), (60, 200, 60)]):
            pygame.draw.circle(screen, color, (SCREEN_W - 45 + i * 20, 30), 6)

        # Clip drawing area
        clip_rect = pygame.Rect(15, 60, SCREEN_W - 30, SCREEN_H - 75)
        screen.set_clip(clip_rect)

        # Draw item cards
        for card_data in self.cards:
            item = card_data["item"]
            rect = card_data["rect"].copy()
            rect.y -= self.scroll_offset

            owned = self.game_state.has(item["key"])
            prereq_met = item["requires"] is None or self.game_state.has(item["requires"])
            can_afford = self.game_state.gold >= item["cost"]

            if owned:
                self._draw_card_owned(screen, rect, item)
            elif prereq_met and can_afford:
                self._draw_card_buyable(screen, rect, item)
            elif prereq_met:
                self._draw_card_expensive(screen, rect, item)
            else:
                self._draw_card_locked(screen, rect, item)

        # Start Run button
        btn = self.start_button_rect.copy()
        btn.y -= self.scroll_offset

        # Button hover effect
        mx, my = pygame.mouse.get_pos()
        btn_check = btn.copy()
        hovering = btn_check.collidepoint(mx, my)

        btn_color = (40, 180, 80) if hovering else (30, 140, 60)
        pygame.draw.rect(screen, btn_color, btn, border_radius=6)
        pygame.draw.rect(screen, (50, 220, 100), btn, 2, border_radius=6)

        btn_text = self.font_btn.render("START RUN", True, (255, 255, 255))
        btn_text_rect = btn_text.get_rect(center=btn.center)
        screen.blit(btn_text, btn_text_rect)

        # Run count
        run_surf = self.font_small.render(f"Run #{self.game_state.run_count + 1}", True, (120, 120, 120))
        run_rect = run_surf.get_rect(center=(btn.centerx, btn.bottom + 15))
        screen.blit(run_surf, run_rect)

        screen.set_clip(None)

    def _draw_card_owned(self, screen, rect, item):
        """Already purchased — stamped green."""
        pygame.draw.rect(screen, (25, 50, 30), rect, border_radius=6)
        pygame.draw.rect(screen, (40, 120, 50), rect, 2, border_radius=6)

        # Flash on recent purchase
        if self.flash_item == item["key"] and self.flash_timer > 0:
            flash_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            alpha = int(200 * (self.flash_timer / 0.3))
            flash_surf.fill((100, 255, 100, alpha))
            screen.blit(flash_surf, rect.topleft)

        name_surf = self.font_item.render(item["name"], True, (80, 200, 80))
        screen.blit(name_surf, (rect.x + 12, rect.y + 8))

        status_surf = self.font_small.render("[INSTALLED]", True, (60, 160, 60))
        screen.blit(status_surf, (rect.right - 110, rect.y + 10))

        desc_surf = self.font_small.render(item["description"], True, (80, 120, 80))
        screen.blit(desc_surf, (rect.x + 12, rect.y + 32))

        flavor_surf = self.font_flavor.render(item["flavor"], True, (50, 100, 50))
        screen.blit(flavor_surf, (rect.x + 12, rect.y + 55))

    def _draw_card_buyable(self, screen, rect, item):
        """Available for purchase — highlighted."""
        mx, my = pygame.mouse.get_pos()
        hovering = rect.collidepoint(mx, my)

        bg_color = (50, 50, 70) if hovering else (40, 40, 55)
        border_color = (100, 180, 255) if hovering else (80, 80, 120)

        pygame.draw.rect(screen, bg_color, rect, border_radius=6)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=6)

        name_surf = self.font_item.render(item["name"], True, (220, 220, 255))
        screen.blit(name_surf, (rect.x + 12, rect.y + 8))

        cost_color = (100, 255, 100)
        cost_surf = self.font_item.render(f"{item['cost']}g", True, cost_color)
        screen.blit(cost_surf, (rect.right - 70, rect.y + 10))

        desc_surf = self.font_small.render(item["description"], True, (180, 180, 200))
        screen.blit(desc_surf, (rect.x + 12, rect.y + 32))

        flavor_surf = self.font_flavor.render(item["flavor"], True, (100, 100, 140))
        screen.blit(flavor_surf, (rect.x + 12, rect.y + 55))

        if hovering:
            buy_surf = self.font_small.render("[ CLICK TO BUY ]", True, (150, 220, 255))
            screen.blit(buy_surf, (rect.right - 140, rect.y + 55))

    def _draw_card_expensive(self, screen, rect, item):
        """Prereqs met but can't afford — dimmed."""
        pygame.draw.rect(screen, (35, 30, 30), rect, border_radius=6)
        pygame.draw.rect(screen, (80, 60, 60), rect, 2, border_radius=6)

        name_surf = self.font_item.render(item["name"], True, (180, 120, 120))
        screen.blit(name_surf, (rect.x + 12, rect.y + 8))

        cost_surf = self.font_item.render(f"{item['cost']}g", True, (200, 80, 80))
        screen.blit(cost_surf, (rect.right - 70, rect.y + 10))

        desc_surf = self.font_small.render(item["description"], True, (140, 100, 100))
        screen.blit(desc_surf, (rect.x + 12, rect.y + 32))

        need_surf = self.font_small.render(f"Need {item['cost'] - self.game_state.gold}g more", True, (200, 80, 80))
        screen.blit(need_surf, (rect.x + 12, rect.y + 55))

    def _draw_card_locked(self, screen, rect, item):
        """Prerequisites not met — greyed out."""
        pygame.draw.rect(screen, (25, 25, 25), rect, border_radius=6)
        pygame.draw.rect(screen, (50, 50, 50), rect, 1, border_radius=6)

        name_surf = self.font_item.render(item["name"], True, (80, 80, 80))
        screen.blit(name_surf, (rect.x + 12, rect.y + 8))

        cost_surf = self.font_item.render(f"{item['cost']}g", True, (60, 60, 60))
        screen.blit(cost_surf, (rect.right - 70, rect.y + 10))

        # Find prereq name
        prereq_key = item["requires"]
        prereq_name = prereq_key
        for si in SHOP_ITEMS:
            if si["key"] == prereq_key:
                prereq_name = si["name"]
                break

        lock_surf = self.font_small.render(f"LOCKED - Requires: {prereq_name}", True, (100, 60, 60))
        screen.blit(lock_surf, (rect.x + 12, rect.y + 35))

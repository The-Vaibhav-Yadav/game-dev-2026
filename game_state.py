from constants import PLAYER_SPEED_BASE, PLAYER_SPEED_V1, PLAYER_SPEED_V2, TAX_RATES, TAX_SHELTER_MULTIPLIER


class GameState:
    def __init__(self):
        self.gold = 0                  # persistent gold across runs
        self.current_room = 1          # which room to load on next run
        self.run_count = 0             # total runs attempted
        self.total_deaths = 0
        self.total_gold_earned = 0     # lifetime stat for victory screen

        # --- Upgrade flags (all start False) ---
        self.purchased = {
            "speed_v1": False,
            "sprite_basic": False,
            "combat": False,
            "audio_sfx": False,
            "speed_v2": False,
            "sprite_deluxe": False,
            "audio_music": False,
            "room_expansion": False,
            "hud_upgrade": False,
            "tax_shelter": False,
        }

    def has(self, upgrade_name):
        """Shortcut: game_state.has('combat') -> True/False"""
        return self.purchased.get(upgrade_name, False)

    def get_player_speed(self):
        if self.has("speed_v2"):
            return PLAYER_SPEED_V2
        elif self.has("speed_v1"):
            return PLAYER_SPEED_V1
        return PLAYER_SPEED_BASE

    def get_tax_rate(self, room_number):
        """Returns gold/sec drain for a given room."""
        base = TAX_RATES.get(room_number, 2)
        if self.has("tax_shelter"):
            base *= TAX_SHELTER_MULTIPLIER
        return base

    def get_max_room(self):
        """Rooms 1-2 always available. 3-5 need Room Expansion."""
        return 5 if self.has("room_expansion") else 2

    def start_new_run(self):
        """Called when player leaves the shop to start a run."""
        self.run_count += 1
        self.current_room = 1
        # gold is NOT reset — it persists

    def on_death(self):
        self.total_deaths += 1

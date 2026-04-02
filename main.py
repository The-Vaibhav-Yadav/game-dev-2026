import pygame
import sys
from constants import SCREEN_W, SCREEN_H, FPS, STATE_TITLE
from game_state import GameState
from systems.asset_manager import AssetManager
from systems.audio_manager import AudioManager
from states.title_state import TitleState
from states.playing_state import PlayingState
from states.dead_state import DeadState
from states.shop_state import ShopState
from states.victory_state import VictoryState


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Debt Dungeon")
    clock = pygame.time.Clock()

    # --- Shared singletons ---
    game_state = GameState()
    assets = AssetManager()
    audio = AudioManager(game_state)

    # --- Create all states, pass shared objects ---
    states = {
        "title":   TitleState(game_state, assets, audio),
        "playing": PlayingState(game_state, assets, audio),
        "dead":    DeadState(game_state, assets, audio),
        "shop":    ShopState(game_state, assets, audio),
        "victory": VictoryState(game_state, assets, audio),
    }

    current_state_name = STATE_TITLE
    states[current_state_name].enter()

    # --- Main loop ---
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Update returns None (stay) or a state name string (transition)
        next_state = states[current_state_name].update(dt, events)

        if next_state and next_state != current_state_name:
            states[current_state_name].exit()
            current_state_name = next_state
            states[current_state_name].enter()

        states[current_state_name].draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

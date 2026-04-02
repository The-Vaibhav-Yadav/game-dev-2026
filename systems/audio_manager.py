import pygame
import os
from constants import AUDIO_DIR


class AudioManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.sfx = {}
        self._load_all()

    def _load_all(self):
        sfx_dir = os.path.join(AUDIO_DIR, "sfx")
        if os.path.exists(sfx_dir):
            for f in os.listdir(sfx_dir):
                if f.endswith(".wav"):
                    key = os.path.splitext(f)[0]
                    try:
                        self.sfx[key] = pygame.mixer.Sound(os.path.join(sfx_dir, f))
                    except pygame.error:
                        print(f"WARNING: Could not load sfx: {f}")

    def play_sfx(self, name):
        """Play a sound effect — but ONLY if audio_sfx is purchased."""
        if not self.game_state.has("audio_sfx"):
            return
        sound = self.sfx.get(name)
        if sound:
            sound.play()

    def play_music(self, track_name):
        """Play background music — but ONLY if audio_music is purchased."""
        if not self.game_state.has("audio_music"):
            return
        path = os.path.join(AUDIO_DIR, "music", f"{track_name}.ogg")
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass

    def play_sfx_always(self, name):
        """For sounds that should play even without the upgrade."""
        sound = self.sfx.get(name)
        if sound:
            sound.play()

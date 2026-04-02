import pygame
import os
from constants import SPRITE_DIR, TILE_SIZE, FONT_DIR


class AssetManager:
    def __init__(self):
        self.sprites = {}
        self._fonts = {}
        self._load_all()

    def _load_all(self):
        """Walk the sprites directory and load everything.
        File: assets/sprites/player/player_down.png -> key: 'player_down'
        """
        if not os.path.exists(SPRITE_DIR):
            return
        for root, dirs, files in os.walk(SPRITE_DIR):
            for filename in files:
                if filename.endswith(".png"):
                    key = os.path.splitext(filename)[0]
                    path = os.path.join(root, filename)
                    try:
                        img = pygame.image.load(path).convert_alpha()
                        # Scale to tile size if needed
                        if img.get_width() != TILE_SIZE or img.get_height() != TILE_SIZE:
                            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.sprites[key] = img
                    except pygame.error:
                        print(f"WARNING: Could not load sprite: {path}")

    def get_sprite(self, key):
        """Returns the Surface or None."""
        return self.sprites.get(key, None)

    def has_sprite(self, key):
        return key in self.sprites

    def get_font(self, name, size):
        """Load a font. Caches internally."""
        cache_key = (name, size)
        if cache_key not in self._fonts:
            font_path = os.path.join(FONT_DIR, name)
            if os.path.exists(font_path):
                self._fonts[cache_key] = pygame.font.Font(font_path, size)
            else:
                self._fonts[cache_key] = pygame.font.SysFont("Courier", size)
        return self._fonts[cache_key]

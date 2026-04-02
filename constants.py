import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITE_DIR = os.path.join(ASSETS_DIR, "sprites")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
UI_DIR = os.path.join(ASSETS_DIR, "ui")
FONT_DIR = os.path.join(UI_DIR, "fonts")

# --- Display ---
TILE_SIZE = 64
GRID_W = 10
GRID_H = 10
HUD_HEIGHT = 80
SCREEN_W = GRID_W * TILE_SIZE             # 640
SCREEN_H = GRID_H * TILE_SIZE + HUD_HEIGHT  # 720
FPS = 60

# --- Colors (used BEFORE sprite packs are bought) ---
COLOR_BG           = (10, 10, 10)
COLOR_PLAYER       = (255, 255, 255)
COLOR_WALL         = (40, 40, 40)
COLOR_FLOOR        = (20, 20, 20)
COLOR_COIN         = (255, 215, 0)
COLOR_KEY          = (0, 255, 255)
COLOR_DOOR_LOCKED  = (100, 100, 100)
COLOR_DOOR_OPEN    = (0, 255, 100)
COLOR_SLIME        = (0, 200, 0)
COLOR_BAT          = (200, 0, 0)
COLOR_TURRET       = (200, 200, 0)
COLOR_PROJECTILE   = (255, 100, 0)
COLOR_SPIKE        = (150, 0, 0)
COLOR_TAX_ZONE     = (200, 170, 0)
COLOR_HUD_BG       = (30, 30, 30)
COLOR_HUD_TEXT     = (255, 255, 255)
COLOR_ATTACK_FLASH = (255, 255, 100)

# --- Player ---
PLAYER_SPEED_BASE = 1.0      # tiles per second
PLAYER_SPEED_V1   = 3.0
PLAYER_SPEED_V2   = 5.0
PLAYER_START_GOLD = 50
ATTACK_COOLDOWN   = 0.4      # seconds
KNOCKBACK_STUN    = 0.5      # seconds
ATTACK_RANGE      = 1        # tiles

# --- Economy ---
COIN_VALUE          = 3
KILL_BONUS_NORMAL   = 5
KILL_BONUS_TURRET   = 8
ROOM_CLEAR_BONUS    = 10
KEY_BONUS           = 5
TRAP_DAMAGE         = 8
ENEMY_COLLISION_DMG = 10
PROJECTILE_DAMAGE   = 8

# --- Tax ---
TAX_RATES = {1: 2, 2: 2, 3: 3, 4: 3, 5: 4}
TAX_SHELTER_MULTIPLIER = 0.5

# --- Enemies ---
SLIME_MOVE_INTERVAL   = 1.5
BAT_MOVE_INTERVAL     = 1.0
TURRET_FIRE_INTERVAL  = 2.0
PROJECTILE_SPEED      = 3.33

# --- Traps ---
SPIKE_CYCLE_TIME = 2.0

# --- Tile type characters ---
TILE_FLOOR   = '.'
TILE_WALL    = '#'
TILE_PLAYER  = 'P'
TILE_KEY     = 'K'
TILE_DOOR    = 'D'
TILE_COIN    = '$'
TILE_SLIME   = 'S'
TILE_BAT     = 'B'
TILE_TURRET  = 'T'
TILE_SPIKE   = '^'
TILE_TAX     = 'X'

# --- Directions ---
DIR_UP    = (0, -1)
DIR_DOWN  = (0, 1)
DIR_LEFT  = (-1, 0)
DIR_RIGHT = (1, 0)

# --- State IDs ---
STATE_TITLE   = "title"
STATE_PLAYING = "playing"
STATE_DEAD    = "dead"
STATE_SHOP    = "shop"
STATE_VICTORY = "victory"

# --- Damage cooldown ---
DAMAGE_COOLDOWN = 0.5  # seconds between enemy collision damage ticks

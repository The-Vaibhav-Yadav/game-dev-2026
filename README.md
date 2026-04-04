# Debt Dungeon

A roguelike dungeon crawler where **you start with nothing** — no graphics, no sound, no combat. Every game feature must be purchased from the in-game shop using gold earned from dungeon runs. Die, earn gold, buy upgrades, repeat.

## Request to Judges
We request the judges to play the game at each and every level , upgrade to every level from starting to end and also 
at last see the audio in in each phase of bankrupt , victory , collecting coins , initial shoppingphase and playing state.
We hope the that our hardwork will be loved by the judges.

## Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** — fast Python package manager

### Installing uv

If you don't have `uv` installed:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

## Getting Started

```bash
# Clone / navigate to the project
cd debt_dungeon

# Install dependencies and run (uv handles the virtual environment automatically)
uv run python main.py
```

That's it — `uv` will create a `.venv`, install `pygame-ce`, and launch the game.

### Manual Setup (if needed)

```bash
uv sync          # install dependencies from pyproject.toml
uv run python main.py   # run the game
```

## How to Play

### The Loop

1. **Title Screen** → Press any key
2. **Shop** → Browse upgrades, click **START RUN** (or press Enter)
3. **Dungeon** → Collect coins, collect the key, reach the door
4. **BANKRUPT** → Your gold drains constantly. Hit 0 and you die.
5. **Back to Shop** → Gold earned carries over. Buy upgrades. Try again.

### Controls

| Key | Action |
|-----|--------|
| **Arrow Keys / WASD** | Move |
| **Space** | Attack (requires Combat Module upgrade) |
| **Mouse Click** | Buy items in shop |
| **Mouse Scroll / Arrow Keys** | Scroll shop list |
| **Enter** | Start a run from shop |

### The Upgrades (in purchase order)

| # | Upgrade | Cost | What It Does |
|---|---------|------|-------------|
| 1 | Speed Module v1 | 30g | Faster movement (1 → 3 tiles/sec) |
| 2 | Sprite Pack: Basic | 50g | Colored rects → actual sprites |
| 3 | Combat Module | 75g | Press Space to attack enemies |
| 4 | Audio Card: SFX | 40g | Sound effects enabled |
| 5 | Speed Module v2 | 60g | Max movement speed (5 tiles/sec) |
| 6 | Sprite Pack: Deluxe | 80g | HD enemy & trap art |
| 7 | Audio Card: Music | 60g | Background music enabled |
| 8 | Room Expansion | 100g | Unlocks Rooms 3, 4, and 5 |
| 9 | HUD Upgrade | 45g | Minimap + enemy HP bars |
| 10 | Tax Shelter | 150g | Halves the existence tax |

Each upgrade requires the previous one to be purchased first.

### Tips

- **Gold drains every second** (Existence Tax). Move fast, collect coins, get out.
- Enemies cost gold on contact — avoid them until you buy Combat Module.
- Tax Zones (pulsing gold tiles) **double** your tax rate while standing on them.
- Spike traps cycle on/off — time your movement.
- The **key** must be collected before the **door** opens.

## Debug Keys

For testing — enabled by default (`DEBUG = True` in `playing_state.py`):

| Key | Effect |
|-----|--------|
| **F1** | +500 run gold |
| **F2** | Skip to victory screen |
| **F3** | Skip to next room |
| **F4** | Unlock all upgrades |
| **F5** | Print debug info to terminal |

Set `DEBUG = False` in `states/playing_state.py` to disable.

## Adding Custom Assets (Optional)

The game works fully with animated characters and backgrounds. To add sprites and audio, you need to upgrade to that level.

### Sprites (64×64 PNG)

```
assets/sprites/player/   → player_up.png, player_down.png, player_left.png, player_right.png ,player_attack_up.png, player_attack_down.png,
                           player_attack_left.png, player_attack_right.png
assets/sprites/pickups/    → key.png
assets/sprites/fire_png.png/  
assets/sprites/enemies/  → slime_1.png, bat_1.png, turret_1.png , enemies_sprite.png
assets/sprites/traps/    → spike_up.png, spike_down.png, tax_zone_1.png
                         ├── tiles
                                    →floor_1.png , wall.png

```

### Audio

```
assets/audio/music/   → shop_music.mp3 
debt_dungeon/dd_cursor
├── buy.mpeg
├── click.mpeg
├── click2.mpeg
├── coin2.mp3
├── click2.mp3
├── counting_stars.mpeg
├── faah.mpeg
├── fien.mp3
├── fien2.mp3
├── keys.mpeg
├── keys2.mp3
├── slash.mpeg
├── sunflower.mpeg
├── this_is_the_end.mpeg
├── victory.mpeg
 
```



## Project Structure

```
debt_dungeon/dd_cursor(Excluding the )
├── main.py              # Entry point — game loop
├── constants.py         # All magic numbers and paths
├── game_state.py        # Persistent state (gold, upgrades)
├── utils.py             # Grid/pixel helpers
├── states/              # Game screens (title, playing, shop, dead, victory)
├── entities/            # Player, enemies, projectiles, pickups, traps
├── systems/             # Room loader, asset/audio managers, HUD, camera
├── data/                # Room layouts and shop item definitions
└── assets/              # Sprites, audio, UI (optional)
```

## License

MIT

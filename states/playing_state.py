import pygame
from states.base_state import BaseState
from constants import (
    SCREEN_W, SCREEN_H, HUD_HEIGHT, TILE_SIZE, GRID_W, GRID_H,
    COLOR_BG, COLOR_FLOOR, COLOR_WALL, COLOR_PLAYER, COLOR_COIN, COLOR_KEY,
    COLOR_DOOR_LOCKED, COLOR_DOOR_OPEN, COLOR_SLIME, COLOR_BAT, COLOR_TURRET,
    COLOR_PROJECTILE, COLOR_SPIKE, COLOR_TAX_ZONE, COLOR_ATTACK_FLASH,
    PLAYER_START_GOLD, COIN_VALUE, KEY_BONUS, KILL_BONUS_NORMAL,
    KILL_BONUS_TURRET, ROOM_CLEAR_BONUS, TRAP_DAMAGE, ENEMY_COLLISION_DMG,
    PROJECTILE_DAMAGE, DAMAGE_COOLDOWN,
    STATE_DEAD, STATE_VICTORY, STATE_SHOP
)
from utils import grid_to_pixel, is_in_bounds
from entities.player import Player
from systems.room_manager import RoomManager
from systems.hud import HUD
from systems.camera import Camera

DEBUG = True


class PlayingState(BaseState):
    def __init__(self, game_state, assets, audio):
        super().__init__(game_state, assets, audio)
        self.room_manager = RoomManager()
        self.hud = HUD(assets)
        self.camera = Camera()

        # Per-run state (initialized in enter())
        self.player = None
        self.enemies = []
        self.pickups = []
        self.traps = []
        self.projectiles = []
        self.walls = set()
        self.door_pos = (9, 9)
        self.run_gold = 0
        self.gold_earned_this_run = 0
        self.tax_multiplier = 1.0
        self.spikes_hit_this_cycle = set()

    def enter(self):
        """Set up the room for a new run or new room."""
        room_number = self.game_state.current_room
        room_data = self.room_manager.load_room(room_number)

        spawn = room_data["player_spawn"]
        self.player = Player(spawn[0], spawn[1])
        self.walls = room_data["walls"]
        self.enemies = room_data["enemies"]
        self.pickups = room_data["pickups"]
        self.traps = room_data["traps"]
        self.door_pos = room_data["door_pos"]
        self.projectiles = []
        self.spikes_hit_this_cycle = set()

        # Only reset run gold on a fresh run (room 1)
        if self.game_state.current_room == 1:
            self.run_gold = PLAYER_START_GOLD
            self.gold_earned_this_run = 0

        self.audio.play_music("bgm_dungeon")

    def exit(self):
        self.audio.stop_music()

    def _load_current_room(self):
        """Reload the current room (used when advancing rooms mid-run)."""
        room_number = self.game_state.current_room
        room_data = self.room_manager.load_room(room_number)

        spawn = room_data["player_spawn"]
        self.player = Player(spawn[0], spawn[1])
        # Carry over key status = False for new room
        self.walls = room_data["walls"]
        self.enemies = room_data["enemies"]
        self.pickups = room_data["pickups"]
        self.traps = room_data["traps"]
        self.door_pos = room_data["door_pos"]
        self.projectiles = []
        self.spikes_hit_this_cycle = set()

    def update(self, dt, events):
        # --- Debug keys ---
        if DEBUG:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.run_gold += 500
                    elif event.key == pygame.K_F2:
                        return STATE_VICTORY
                    elif event.key == pygame.K_F3:
                        self.game_state.current_room += 1
                        if self.game_state.current_room > 5:
                            self.game_state.current_room = 1
                        self._load_current_room()
                    elif event.key == pygame.K_F4:
                        for key in self.game_state.purchased:
                            self.game_state.purchased[key] = True
                    elif event.key == pygame.K_F5:
                        print(f"Gold: {self.run_gold}, Room: {self.game_state.current_room}")
                        print(f"Persistent gold: {self.game_state.gold}")
                        print(f"Upgrades: {self.game_state.purchased}")

        # 1. Read keyboard input
        keys = pygame.key.get_pressed()

        # 2. Player movement
        self.player.update(dt, keys, self.walls, self.game_state)

        # 3. Attack (spacebar)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                attack_pos = self.player.try_attack(self.game_state)
                if attack_pos:
                    self.audio.play_sfx("attack")
                    self.camera.trigger_shake(2, 0.1)
                    for enemy in self.enemies:
                        if enemy.alive and enemy.gx == attack_pos[0] and enemy.gy == attack_pos[1]:
                            enemy.take_damage(1)
                            self.audio.play_sfx("hit")
                            if not enemy.alive:
                                bonus = KILL_BONUS_TURRET if enemy.enemy_type == "turret" else KILL_BONUS_NORMAL
                                self.run_gold += bonus
                                self.gold_earned_this_run += bonus
                                self.audio.play_sfx("enemy_death")
                                self.camera.trigger_shake(4, 0.15)

        # 4. Enemy AI
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            proj = enemy.ai_update(dt, self.player, self.walls, self.enemies)
            if proj is not None:
                self.projectiles.append(proj)
                self.audio.play_sfx("turret_fire")

        # 5. Projectiles
        for proj in self.projectiles:
            if not proj.alive:
                continue
            proj.update(dt, self.walls)
            if proj.alive and proj.gx == self.player.gx and proj.gy == self.player.gy:
                self.run_gold -= PROJECTILE_DAMAGE
                proj.alive = False
                self.audio.play_sfx("hit")
                self.camera.trigger_shake(3, 0.12)
        self.projectiles = [p for p in self.projectiles if p.alive]

        # 6. Enemy-player collisions
        if self.player.damage_cooldown <= 0:
            for enemy in self.enemies:
                if enemy.alive and enemy.gx == self.player.gx and enemy.gy == self.player.gy:
                    self.run_gold -= ENEMY_COLLISION_DMG
                    self.player.apply_knockback(enemy.gx, enemy.gy, self.walls)
                    self.player.damage_cooldown = DAMAGE_COOLDOWN
                    self.camera.trigger_shake(5, 0.2)
                    self.audio.play_sfx("hit")
                    break  # only one collision per frame

        # 7. Traps
        self.tax_multiplier = 1.0
        for trap in self.traps:
            trap.update(dt)
            if self.player.gx == trap.gx and self.player.gy == trap.gy:
                if trap.trap_type == "spike" and trap.active:
                    if trap not in self.spikes_hit_this_cycle:
                        self.run_gold -= TRAP_DAMAGE
                        self.spikes_hit_this_cycle.add(trap)
                        self.audio.play_sfx("spike_trap")
                        self.camera.trigger_shake(3, 0.1)
                elif trap.trap_type == "tax_zone":
                    self.tax_multiplier = 2.0
            # Reset spike hit tracking when spike retracts
            if trap.trap_type == "spike" and not trap.active:
                self.spikes_hit_this_cycle.discard(trap)

        # 8. Pickups
        for pickup in self.pickups:
            pickup.update(dt)
            if pickup.collected:
                continue
            if self.player.gx == pickup.gx and self.player.gy == pickup.gy:
                pickup.collected = True
                if pickup.pickup_type == "coin":
                    self.run_gold += COIN_VALUE
                    self.gold_earned_this_run += COIN_VALUE
                    self.audio.play_sfx("coin")
                elif pickup.pickup_type == "key":
                    self.player.has_key = True
                    self.run_gold += KEY_BONUS
                    self.gold_earned_this_run += KEY_BONUS
                    self.audio.play_sfx("key")

        # 9. Door check
        if (self.player.gx == self.door_pos[0] and
                self.player.gy == self.door_pos[1] and
                self.player.has_key):
            self.run_gold += ROOM_CLEAR_BONUS
            self.gold_earned_this_run += ROOM_CLEAR_BONUS
            self.audio.play_sfx("door_open")
            self.game_state.current_room += 1

            if self.game_state.current_room > self.game_state.get_max_room():
                # Victory! Save earned gold
                self.game_state.gold += self.gold_earned_this_run
                self.game_state.total_gold_earned += self.gold_earned_this_run
                return STATE_VICTORY
            else:
                # Advance to next room
                self._load_current_room()

        # 10. Existence Tax
        room_number = self.game_state.current_room
        tax_rate = self.game_state.get_tax_rate(room_number)
        tax = tax_rate * self.tax_multiplier * dt
        self.run_gold -= tax

        # 11. Death check
        if self.run_gold <= 0:
            self.run_gold = 0
            self.game_state.gold += self.gold_earned_this_run
            self.game_state.total_gold_earned += self.gold_earned_this_run
            self.game_state.on_death()
            return STATE_DEAD

        # 12. Camera
        self.camera.update(dt)

        return None

    def draw(self, screen):
        screen.fill(COLOR_BG)

        shake_x = self.camera.shake_offset_x
        shake_y = self.camera.shake_offset_y

        # --- Draw HUD ---
        room_number = self.game_state.current_room
        tax_rate = self.game_state.get_tax_rate(room_number) * self.tax_multiplier
        self.hud.draw(screen, self.run_gold, tax_rate, room_number,
                      self.game_state, self.enemies, self.player, self.walls)

        # --- Draw grid ---
        for gy in range(GRID_H):
            for gx in range(GRID_W):
                px, py = grid_to_pixel(gx, gy)
                px += shake_x
                py += shake_y

                if (gx, gy) in self.walls:
                    self._draw_tile(screen, px, py, "wall", COLOR_WALL)
                else:
                    self._draw_tile(screen, px, py, "floor_1", COLOR_FLOOR)

        # --- Draw door ---
        dpx, dpy = grid_to_pixel(self.door_pos[0], self.door_pos[1])
        dpx += shake_x
        dpy += shake_y
        if self.player.has_key:
            self._draw_tile(screen, dpx, dpy, "door_open", COLOR_DOOR_OPEN)
        else:
            self._draw_tile(screen, dpx, dpy, "door_locked", COLOR_DOOR_LOCKED)

        # --- Draw traps ---
        for trap in self.traps:
            tpx, tpy = grid_to_pixel(trap.gx, trap.gy)
            tpx += shake_x
            tpy += shake_y
            if trap.trap_type == "spike":
                if trap.active:
                    self._draw_tile(screen, tpx, tpy, "spike_up", COLOR_SPIKE)
                else:
                    # Draw dimmer when retracted
                    color = (80, 0, 0)
                    self._draw_tile(screen, tpx, tpy, "spike_down", color)
            elif trap.trap_type == "tax_zone":
                # Pulsing effect
                import math
                pulse = int(170 + 30 * math.sin(pygame.time.get_ticks() / 200.0))
                color = (pulse, int(pulse * 0.8), 0)
                self._draw_tile(screen, tpx, tpy, "tax_zone_1", color)

        # --- Draw pickups ---
        for pickup in self.pickups:
            if pickup.collected:
                continue
            ppx, ppy = grid_to_pixel(pickup.gx, pickup.gy)
            ppx += shake_x
            ppy += shake_y
            if pickup.pickup_type == "coin":
                # Coin bob animation
                import math
                bob = int(3 * math.sin(pickup.anim_timer * 4))
                self._draw_entity(screen, ppx, ppy + bob, "coin_1", COLOR_COIN)
            elif pickup.pickup_type == "key":
                self._draw_entity(screen, ppx, ppy, "key", COLOR_KEY)

        # --- Draw enemies ---
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            epx, epy = grid_to_pixel(enemy.gx, enemy.gy)
            epx += shake_x
            epy += shake_y

            if enemy.enemy_type == "slime":
                self._draw_entity(screen, epx, epy, "slime_1", COLOR_SLIME)
            elif enemy.enemy_type == "bat":
                self._draw_entity(screen, epx, epy, "bat_1", COLOR_BAT)
            elif enemy.enemy_type == "turret":
                self._draw_entity(screen, epx, epy, "turret_1", COLOR_TURRET)

            # HP bars (if HUD upgrade)
            if self.game_state.has("hud_upgrade"):
                self.hud.draw_enemy_hp_bar(screen, enemy)

        # --- Draw player ---
        plx, ply = grid_to_pixel(self.player.gx, self.player.gy)
        plx += shake_x
        ply += shake_y

        # Determine player sprite key based on facing
        facing = self.player.facing
        if facing == (0, -1):
            sprite_key = "player_up"
        elif facing == (0, 1):
            sprite_key = "player_down"
        elif facing == (-1, 0):
            sprite_key = "player_left"
        else:
            sprite_key = "player_right"

        self._draw_entity(screen, plx, ply, sprite_key, COLOR_PLAYER)

        # --- Draw attack flash ---
        if self.player.attack_visual_timer > 0:
            atk_gx = self.player.gx + self.player.facing[0]
            atk_gy = self.player.gy + self.player.facing[1]
            if is_in_bounds(atk_gx, atk_gy):
                apx, apy = grid_to_pixel(atk_gx, atk_gy)
                apx += shake_x
                apy += shake_y
                # Semi-transparent flash
                flash_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                flash_surf.fill((*COLOR_ATTACK_FLASH, 150))
                screen.blit(flash_surf, (apx, apy))

        # --- Draw projectiles ---
        for proj in self.projectiles:
            prpx, prpy = grid_to_pixel(proj.gx, proj.gy)
            prpx += shake_x
            prpy += shake_y
            self._draw_entity(screen, prpx, prpy, "projectile", COLOR_PROJECTILE, size=24)

        # --- Stun indicator ---
        if self.player.stun_timer > 0:
            stun_text = pygame.font.SysFont("Courier", 14).render("STUNNED", True, (255, 100, 100))
            screen.blit(stun_text, (plx - 5, ply - 16))

    def _draw_tile(self, screen, px, py, sprite_key, fallback_color):
        """Draw a tile-sized element using sprite if available, else colored rect."""
        if self.game_state.has("sprite_basic") and self.assets.has_sprite(sprite_key):
            screen.blit(self.assets.get_sprite(sprite_key), (px, py))
        else:
            pygame.draw.rect(screen, fallback_color, (px, py, TILE_SIZE, TILE_SIZE))

    def _draw_entity(self, screen, px, py, sprite_key, fallback_color, size=56):
        """Draw an entity using sprite if available, else centered colored rect."""
        use_sprites = self.game_state.has("sprite_basic") and self.assets.has_sprite(sprite_key)
        # For enemies, also check sprite_deluxe
        if sprite_key in ("slime_1", "slime_2", "bat_1", "bat_2", "turret_1"):
            use_sprites = self.game_state.has("sprite_deluxe") and self.assets.has_sprite(sprite_key)

        if use_sprites:
            screen.blit(self.assets.get_sprite(sprite_key), (px, py))
        else:
            offset = (TILE_SIZE - size) // 2
            pygame.draw.rect(screen, fallback_color, (px + offset, py + offset, size, size))

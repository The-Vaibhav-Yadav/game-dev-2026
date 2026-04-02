from data.rooms import ROOMS
from constants import (
    TILE_WALL, TILE_PLAYER, TILE_DOOR, TILE_KEY, TILE_COIN,
    TILE_SLIME, TILE_BAT, TILE_TURRET, TILE_SPIKE, TILE_TAX
)
from entities.enemy import Slime, Bat, Turret
from entities.pickup import Pickup
from entities.trap import Trap


class RoomManager:
    def load_room(self, room_number):
        """Parse a room layout string and return all entities + wall set.

        Returns a dict:
        {
            "player_spawn": (gx, gy),
            "walls": set of (gx, gy),
            "enemies": [Enemy, ...],
            "pickups": [Pickup, ...],
            "traps": [Trap, ...],
            "door_pos": (gx, gy),
        }
        """
        layout = ROOMS[room_number]
        result = {
            "player_spawn": (1, 1),
            "walls": set(),
            "enemies": [],
            "pickups": [],
            "traps": [],
            "door_pos": (9, 9),
        }

        for gy, row in enumerate(layout):
            for gx, char in enumerate(row):
                if char == TILE_WALL:
                    result["walls"].add((gx, gy))
                elif char == TILE_PLAYER:
                    result["player_spawn"] = (gx, gy)
                elif char == TILE_DOOR:
                    result["door_pos"] = (gx, gy)
                elif char == TILE_KEY:
                    result["pickups"].append(Pickup(gx, gy, "key"))
                elif char == TILE_COIN:
                    result["pickups"].append(Pickup(gx, gy, "coin"))
                elif char == TILE_SLIME:
                    result["enemies"].append(Slime(gx, gy))
                elif char == TILE_BAT:
                    result["enemies"].append(Bat(gx, gy))
                elif char == TILE_TURRET:
                    result["enemies"].append(Turret(gx, gy))
                elif char == TILE_SPIKE:
                    result["traps"].append(Trap(gx, gy, "spike"))
                elif char == TILE_TAX:
                    result["traps"].append(Trap(gx, gy, "tax_zone"))

        return result

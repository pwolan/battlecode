from enum import Enum
from battlecode25.stubs import *

directions = [
    Direction.NORTH,
    Direction.NORTHEAST,
    Direction.EAST,
    Direction.SOUTHEAST,
    Direction.SOUTH,
    Direction.SOUTHWEST,
    Direction.WEST,
    Direction.NORTHWEST,
]


class MessageType(Enum):
    RUIN_LOCATION = 0
    BUILD_TOWER = 1

def has_tower(loc):
    # Possible todo: tile.has_ruin()
    return can_sense_location(loc) and sense_robot_at_location(loc) != None

def has_ruin_without_tower(tile):
    return can_sense_location(tile.get_map_location()) and tile.has_ruin() and sense_robot_at_location(tile.get_map_location()) is None

def is_tower_pattern_complete(unit_type, loc):
    # sprawdzamy czy wszystkie kafelki są poprawnie pomalowane (wzorzec gotowy)
    for pattern_tile in sense_nearby_map_infos(loc, 8):
        if pattern_tile.get_mark() != PaintType.EMPTY and pattern_tile.get_mark() != pattern_tile.get_paint():
            return False
    return True

def is_enemy_visible(loc):
    # Sprawdza, czy w danej lokacji jest widoczny wróg
    enemies = sense_nearby_robots(team=get_team().opponent())
    if enemies:
        return True
    return False

def my_max(seq, key=lambda x: x):
    if len(seq) == 0:
        raise ValueError("my_max() arg is an empty sequence")

    best_item = seq[0]
    best_value = key(best_item)

    i = 1
    while i < len(seq):
        item = seq[i]
        val = key(item)
        if val > best_value:
            best_value = val
            best_item = item
        i += 1

    return best_item

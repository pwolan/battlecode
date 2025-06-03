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
    return can_sense_location(loc) and sense_robot_at_location(loc) != None

def has_ruin_without_tower(tile):
    return can_sense_location(tile.get_map_location()) and tile.has_ruin() and sense_robot_at_location(tile.get_map_location()) is None

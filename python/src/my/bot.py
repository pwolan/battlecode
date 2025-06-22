from battlecode25.stubs import *
from run_tower import run_tower
from run_soldier import run_soldier
from run_splasher import run_splasher
from run_mopper import run_mopper
from game_state import increment_turn


def turn():
    increment_turn()

    unit_type = get_type()
    if unit_type == UnitType.SOLDIER:
        run_soldier()
    elif unit_type == UnitType.MOPPER:
        run_mopper()
    elif unit_type == UnitType.SPLASHER:
        run_splasher()
    elif unit_type.is_tower_type():
        run_tower()

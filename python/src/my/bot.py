from battlecode25.stubs import *
from roles import run_mopper, run_tower
from run_soldier import run_soldier
from game_state import increment_turn


def turn():
    increment_turn()

    unit_type = get_type()
    if unit_type == UnitType.SOLDIER:
        run_soldier()
    elif unit_type == UnitType.MOPPER:
        run_mopper()
    elif unit_type == UnitType.SPLASHER:
        pass  # TODO
    elif unit_type.is_tower_type():
        run_tower()

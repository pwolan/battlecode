# roles.py

from battlecode25.stubs import *
import random
from utils import MessageType, directions
import game_state

def run_tower():
    dir = random.choice(directions)
    next_loc = get_location().add(dir)


    if game_state.should_save():
        game_state.decrement_save_turns()
    else:
        if can_build_robot(UnitType.SOLDIER, next_loc):
            build_robot(UnitType.SOLDIER, next_loc)
            log("BUILT A SOLDIER")

    read_msgs()
    broadcast_ruin_locations()

def read_msgs():
    messages = read_messages()
    for m in messages:
        log(f"Tower received message: '#{m.get_sender_id()}: {m.get_bytes()}'")
        # broadcast_message(m.get_bytes())
        if m.get_bytes() == MessageType.BUILD_TOWER.value: # Build a tower request
            if not game_state.should_save():
                game_state.set_save_turns(200)


def broadcast_ruin_locations():
    for tile in sense_nearby_map_infos():
        if tile.has_ruin():
            loc = tile.get_map_location()
            for ally in sense_nearby_robots(team=get_team()):
                if can_send_message(ally.location):
                    encoded = (MessageType.RUIN_LOCATION.value << 16) | (loc.x << 8) | loc.y
                    send_message(ally.location, encoded)


def run_mopper():
    dir = random.choice(directions)
    next_loc = get_location().add(dir)
    if can_move(dir):
        move(dir)
    if can_mop_swing(dir):
        mop_swing(dir)
    elif can_attack(next_loc):
        attack(next_loc)

    update_enemy_robots()

def update_enemy_robots():
    enemies = sense_nearby_robots(team=get_team().opponent())
    if enemies:
        set_indicator_string("There are nearby enemy robots! Scary!")
        if get_round_num() % 20 == 0:
            for ally in sense_nearby_robots(team=get_team()):
                if can_send_message(ally.location):
                    send_message(ally.location, len(enemies))

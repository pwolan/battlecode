from battlecode25.stubs import *
import random
from utils import MessageType, directions
import game_state

what_build_next = None

def run_tower():
    dir = random.choice(directions)
    next_loc = get_location().add(dir)


    if game_state.should_save():
        game_state.decrement_save_turns()
    else:
        spawn(next_loc)

    read_msgs()
    broadcast_ruin_locations()

def decide_what_next():
    global what_build_next
    if what_build_next is None:
        if get_round_num() < 300:
            what_build_next = UnitType.SOLDIER
        else:
            what_build_next = random.choice([UnitType.SOLDIER, UnitType.MOPPER])
    return what_build_next

def spawn(next_loc):
    global what_build_next
    if what_build_next is None:
        what_build_next = decide_what_next()

    if can_build_robot(what_build_next, next_loc):
        build_robot(what_build_next, next_loc)
        log(f"BUILT A {what_build_next}")
        what_build_next = None

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

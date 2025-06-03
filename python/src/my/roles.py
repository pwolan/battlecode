# roles.py

from battlecode25.stubs import *
import random
from utils import directions
import game_state

def run_tower():
    dir = random.choice(directions)
    next_loc = get_location().add(dir)

    if can_build_robot(UnitType.SOLDIER, next_loc):
        build_robot(UnitType.SOLDIER, next_loc)
        log("BUILT A SOLDIER")

    messages = read_messages()
    for m in messages:
        log(f"Tower received message: '#{m.get_sender_id()}: {m.get_bytes()}'")

    for tile in sense_nearby_map_infos():
        if tile.has_ruin():
            loc = tile.get_map_location()
            for ally in sense_nearby_robots(team=get_team()):
                if can_send_message(ally.location):
                    encoded = (0 << 16) | (loc.x << 8) | loc.y
                    send_message(ally.location, encoded)

def run_soldier():
    for m in read_messages():
        m = m.get_bytes()
        tag = (m >> 16) & 0xF
        x = (m >> 8) & 0xFF
        y = m & 0xFF
        if tag == 0:
            loc = MapLocation(x, y)
            game_state.add_known_ruin(loc)

    nearby_tiles = sense_nearby_map_infos()
    cur_ruin = None
    for tile in nearby_tiles:
        if tile.has_ruin():
            loc = tile.get_map_location()
            game_state.add_known_ruin(loc)
            cur_ruin = tile

    known_ruins = game_state.get_known_ruins()
    if cur_ruin is None:
        for loc in known_ruins:
            if can_sense_location(loc) and not sense_map_info(loc).has_ruin():
                game_state.remove_known_ruin(loc)

    robot_id = get_id()
    if cur_ruin:
        painting_turns = game_state.get_painting_turns(robot_id)
        if painting_turns % 3 == 0:
            to_ruin = get_location().direction_to(cur_ruin.get_map_location())
            tangent = to_ruin.rotate_right().rotate_right()
            if get_location().distance_squared_to(cur_ruin.get_map_location()) > 4:
                tangent = tangent.rotate_left()
            if can_move(tangent):
                move(tangent)

        game_state.increment_painting_turn(robot_id)

        target_loc = cur_ruin.get_map_location()
        should_mark = target_loc.subtract(get_location().direction_to(target_loc))

        if sense_map_info(should_mark).get_mark() == PaintType.EMPTY and can_mark_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc):
            mark_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc)
            log("Trying to build a tower at " + str(target_loc))

        for tile in sense_nearby_map_infos(target_loc, 8):
            if tile.get_mark() != tile.get_paint() and tile.get_mark() != PaintType.EMPTY:
                use_secondary = tile.get_mark() == PaintType.ALLY_SECONDARY
                if can_attack(tile.get_map_location()):
                    attack(tile.get_map_location(), use_secondary)

        if can_complete_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc):
            complete_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc)
            set_timeline_marker("Tower built", 0, 255, 0)
            log("Built a tower at " + str(target_loc) + "!")

    if known_ruins:
        target_loc = known_ruins[get_id() % len(known_ruins)]
        dir = get_location().direction_to(target_loc)
        if can_move(dir):
            move(dir)

    dir = random.choice(directions)
    if can_move(dir):
        move(dir)

    if not sense_map_info(get_location()).get_paint().is_ally() and can_attack(get_location()):
        attack(get_location())

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

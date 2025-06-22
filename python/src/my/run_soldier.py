from battlecode25.stubs import *
import random
from utils import MessageType, directions, has_ruin_without_tower, is_tower_pattern_complete
import game_state
from utils import has_tower, enemy_or_empty_tiles_in_range

def run_soldier():
    # read messages and update knowledge
    read_msgs()

    # remove any known ruins that are no longer ruins
    known_ruins = game_state.get_known_ruins()
    for loc in known_ruins:
        # if robot is at location it means it is no longer a ruin
        if has_tower(loc):
            log("Removing known ruin at " + str(loc))
            game_state.remove_known_ruin(loc)

    # if we have a known ruin, try to move towards it
    nearby_tiles = sense_nearby_map_infos()
    cur_ruin = None
    for tile in nearby_tiles:
        if has_ruin_without_tower(tile):
            loc = tile.get_map_location()
            game_state.add_known_ruin(loc)
            cur_ruin = tile

    if cur_ruin:
        # painting_turns = game_state.get_painting_turns(robot_id)
        # if painting_turns % 3 == 0:
        #     to_ruin = get_location().direction_to(cur_ruin.get_map_location())
        #     tangent = to_ruin.rotate_right().rotate_right()
        #     if get_location().distance_squared_to(cur_ruin.get_map_location()) > 4:
        #         tangent = tangent.rotate_left()
        #     if can_move(tangent):
        #         move(tangent)

        # game_state.increment_painting_turn(robot_id)

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
        elif is_tower_pattern_complete(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc):
            # log("Tower pattern is complete at " + str(target_loc) + ", but we cannot complete it yet.")
            if not game_state.should_save():
                game_state.set_save_turns(200)
                # set message to save money to adjacent towers
                ally_robots = sense_nearby_robots(team=get_team())
                for ally in ally_robots:
                    # Only consider tower type
                    if not ally.get_type().is_tower_type():
                        continue
                    ally_loc = ally.location
                    # Send a message to the nearby tower
                    if can_send_message(ally_loc):
                        log(f"Sending message to tower at {ally_loc} to save money")
                        send_message(ally_loc, int(MessageType.BUILD_TOWER.value))

    # log([str(r) for r in known_ruins])
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

    # try to get paint from tower
    nearby_tiles = sense_nearby_map_infos()
    for tile in nearby_tiles:
        loc = tile.get_map_location()
        if has_tower(loc):
            needs = 200 - get_paint()
            if can_transfer_paint(loc,-needs):
                transfer_paint(loc, -needs)
                # log(f"Got paint from tower at {loc}")
                break

def read_msgs():
    for m in read_messages():
        # log(f"Soldier received message: '#{m.get_sender_id()}: {m.get_bytes()}'")
        m = m.get_bytes()
        tag = (m >> 16) & 0xF
        x = (m >> 8) & 0xFF
        y = m & 0xFF
        if tag == MessageType.RUIN_LOCATION.value: # Ruin location
            loc = MapLocation(x, y)
            if not can_sense_location(loc):
                continue
            tile = sense_map_info(loc)
            if has_ruin_without_tower(tile):
                game_state.add_known_ruin(loc)
        # broadcast_message(m.get_bytes())
        elif tag == MessageType.BUILD_TOWER.value: # Build a tower request
            pass
            # game_state.set_save_turns(200)
            # log("Received a request to build a tower, saving money for 200 turns")
        else:
            log(f"Unknown message type: {tag}")

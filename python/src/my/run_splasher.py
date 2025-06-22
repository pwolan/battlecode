import random
from battlecode25.stubs import *
from utils import MessageType, directions, has_ruin_without_tower, enemy_or_empty_tiles_in_range, my_max, has_tower
import game_state


def run_splasher():
    read_msgs()
    loc = get_location()


    # try to get paint from tower
    if get_paint() < 120:
        nearby_tiles = sense_nearby_map_infos()
        for tile in nearby_tiles:
            loc = tile.get_map_location()
            if has_tower(loc):
                needs = 300 - get_paint()
                if can_transfer_paint(loc,-needs):
                    transfer_paint(loc, -needs)
                    # log(f"Got paint from tower at {loc}")
                    break

    best_target = None
    greates_tiles = 0
    for dir in directions:
        target = loc.add(dir)
        if can_attack(target) and enemy_or_empty_tiles_in_range(target) > greates_tiles:
            best_target = target
            greates_tiles = enemy_or_empty_tiles_in_range(target)
            break
    if best_target is not None:
        attack(target)
        log(f"SPLASHING!! {enemy_or_empty_tiles_in_range(target)} tiles to paint")


    # chodzenie
    # 300 - max paint for splasher
    found_tower = False
    if get_paint() < 100:
        # log("Not enough paint, going to tower")

        # go to the nearest tower
        nearby_tiles = sense_nearby_map_infos()
        for tile in nearby_tiles:
            loc = tile.get_map_location()
            if has_tower(loc):
                dir = get_location().direction_to(loc)
                if can_move(dir):
                    move(dir)
                    found_tower = True
                    break
    if get_paint() >= 100 or not found_tower:
        best_dir = None
        for dir in directions:
            target = loc.add(dir)
            if can_move(dir) and enemy_or_empty_tiles_in_range(target, 9) > 0:
                move(dir)
                best_dir = dir
                break
        # best_dir = None
        # greates_tiles = 1
        # for dir in directions:
        #     target = loc.add(dir)
        #     if can_move(dir) and enemy_or_empty_tiles_in_range(target) > greates_tiles:
        #         best_dir = dir
        #         greates_tiles = enemy_or_empty_tiles_in_range(target)
        # if best_dir is not None:
        #     move(best_dir)

        if best_dir is None:
            if not game_state.reached_center:
                # go to center of map
                center = MapLocation(get_map_width() // 2, get_map_height() // 2)
                dir = get_location().direction_to(center)
                if can_move(dir):
                    move(dir)

                # check if in center
                if get_location().is_within_distance_squared(center, 10):
                    game_state.set_reached_center()
                    log("Reached center of the map")
            # if already was in center, just move randomly
            dir = random.choice(directions)
            if can_move(dir):
                move(dir)




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


#[A: #13707@812] Reached center of the map

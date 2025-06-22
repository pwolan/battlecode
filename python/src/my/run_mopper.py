from battlecode25.stubs import *
import random
from utils import directions, my_min, MessageType, directions, has_ruin_without_tower, has_tower
import game_state


def run_mopper():
    read_msgs()
    my_id = get_id()
    my_loc = get_location()
    my_team = get_team()

    # Pobierz info o polach w zasięgu czujników
    enemy_fields = game_state.get_enemy_fields()

    all_seen_tiles = sense_nearby_map_infos()
    # Sprawdzamy pola pod kątem farby przeciwnika
    for tile in all_seen_tiles:
        paint = tile.get_paint()
        if paint is not None and paint.is_enemy():
            if tile.get_map_location() not in enemy_fields:
                game_state.add_enemy_field(tile.get_map_location())
        else:
            if tile.get_map_location() in enemy_fields:
                game_state.remove_enemy_field(tile.get_map_location())
    enemy_fields = game_state.get_enemy_fields()
    # Jeśli aktualna pozycja jest na liście brudnych, to usuwamy ją po mopowaniu
    # print(enemy_fields)
    if my_loc in enemy_fields and can_mop_swing(Direction.CENTER):
        mop_swing(Direction.CENTER)


    if enemy_fields:
        # Idziemy do najbliższego brudnego pola
        nearest_dirty = my_min(enemy_fields, key=lambda loc: loc.distance_squared_to(my_loc))
        d = my_loc.direction_to(nearest_dirty)
        if can_move(d):
            move(d)
    else:
        # Brak znanych brudnych pól - zachowanie standardowe
        visible = sense_nearby_robots()
        enemies = [r for r in visible if r.team != my_team]

        if enemies:
            nearest = my_min(enemies, key=lambda r: r.location.distance_squared_to(my_loc))
            d = my_loc.direction_to(nearest.location)
            if can_move(d):
                move(d)
        else:
            dir = random.choice(directions)
            if can_move(dir):
                move(dir)
        # try to get paint from tower
    nearby_tiles = sense_nearby_map_infos()
    for tile in nearby_tiles:
        loc = tile.get_map_location()
        if has_tower(loc):
            needs = 100 - get_paint()
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

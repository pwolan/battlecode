from battlecode25.stubs import *
import random
from utils import directions, is_enemy_visible, my_max

def run_mopper():
    best_dir = my_max(directions, key=evaluate_direction)
    if can_attack(get_location().add(best_dir)):
        attack(get_location().add(best_dir))
    elif can_mop_swing(best_dir):
        mop_swing(best_dir)
    elif can_move(best_dir):
        move(best_dir)

def evaluate_direction(dir):
    score = 0
    loc = get_location().add(dir)

    if not can_move(dir):
        return -1  # zablokowane

    if can_mop_swing(dir):
        score += 5

    if can_attack(loc):
        score += 10

    if is_enemy_visible(loc):
        score += 15

    # if is closer to center of map, prefer it
    center = MapLocation(get_map_width() // 2, get_map_height() // 2)
    distance_to_center = loc.distance_squared_to(center)
    score += (1 + distance_to_center)//100  # preferuj pola bliżej środka

    # # np. preferuj nieodwiedzone pola
    # if not has_been_there(loc):
    #     score += 3

    return score

# def update_enemy_robots():
#     enemies = sense_nearby_robots(team=get_team().opponent())
#     if enemies:
#         set_indicator_string("There are nearby enemy robots! Scary!")
#         if get_round_num() % 20 == 0:
#             for ally in sense_nearby_robots(team=get_team()):
#                 if can_send_message(ally.location):
#                     send_message(ally.location, len(enemies))

import random

from battlecode25.stubs import *
from globals import directions

def run_mopper():
    # Move and attack randomly.
    dir = directions[random.randint(0, len(directions) - 1)]
    next_loc = get_location().add(dir)
    if can_move(dir):
        move(dir)
    if can_mop_swing(dir):
        mop_swing(dir)
        log("Mop Swing! Booyah!")
    elif can_attack(next_loc):
        attack(next_loc)

    # We can also move our code into different methods or classes to better organize it!
    update_enemy_robots()

def update_enemy_robots():
    # Sensing methods can be passed in a radius of -1 to automatically 
    # use the largest possible value.
    enemy_robots = sense_nearby_robots(team=get_team().opponent())
    if len(enemy_robots) == 0:
        return

    set_indicator_string("There are nearby enemy robots! Scary!");

    # Save an array of locations with enemy robots in them for possible future use.
    enemy_locations = [None] * len(enemy_robots)
    for i in range(len(enemy_robots)):
        enemy_locations[i] = enemy_robots[i].get_location()

    # Occasionally try to tell nearby allies how many enemy robots we see.
    ally_robots = sense_nearby_robots(team=get_team())
    if get_round_num() % 20 == 0:
        for ally in ally_robots:
            if can_send_message(ally.location):
                send_message(ally.location, len(enemy_robots))

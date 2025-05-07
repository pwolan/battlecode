import random

from battlecode25.stubs import *
from globals import directions
from mopper import run_mopper
from soldier import run_soldier



# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!
turn_count = 0

def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    global turn_count
    turn_count += 1

    if get_type() == UnitType.SOLDIER:
        run_soldier()
    # if get_type() == UnitType.MOPPER:
    #     run_mopper()
    # elif get_type() == UnitType.SPLASHER:
    #     pass  # TODO
    elif get_type().is_tower_type():
        run_tower()
    else:
        pass  # Other robot types?

def run_tower():
    # Pick a direction to build in.
    dir = directions[random.randint(0, len(directions) - 1)]
    next_loc = get_location().add(dir)

    # Pick a random robot type to build.
    robot_type = random.randint(0, 2)
    if robot_type == 0 and can_build_robot(UnitType.SOLDIER, next_loc):
        build_robot(UnitType.SOLDIER, next_loc)
        log("BUILT A SOLDIER")
    if robot_type == 1 and can_build_robot(UnitType.MOPPER, next_loc):
        build_robot(UnitType.MOPPER, next_loc)
        log("BUILT A MOPPER")
    if robot_type == 2 and can_build_robot(UnitType.SPLASHER, next_loc):
        set_indicator_string("SPLASHER NOT IMPLEMENTED YET");
        #build_robot(RobotType.SPLASHER, next_loc)
        #log("BUILT A SPLASHER")

    # Read incoming messages
    messages = read_messages()
    for m in messages:
        log(f"Tower received message: '#{m.get_sender_id()}: {m.get_bytes()}'")

    # TODO: can we attack other bots?


# def run_soldier():
#     # Sense information about all visible nearby tiles.
#     nearby_tiles = sense_nearby_map_infos()

#     # Search for a nearby ruin to complete.
#     cur_ruin = None
#     for tile in nearby_tiles:
#         if tile.has_ruin():
#             cur_ruin = tile

#     if cur_ruin is not None:
#         target_loc = cur_ruin.get_map_location()
#         dir = get_location().direction_to(target_loc)
#         if can_move(dir):
#             move(dir)

#         # Mark the pattern we need to draw to build a tower here if we haven't already.
#         should_mark = cur_ruin.get_map_location().subtract(dir)
#         if sense_map_info(should_mark).get_mark() == PaintType.EMPTY and can_mark_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc):
#             mark_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc)
#             log("Trying to build a tower at " + str(target_loc))

#         # Fill in any spots in the pattern with the appropriate paint.
#         for pattern_tile in sense_nearby_map_infos(target_loc, 8):
#             if pattern_tile.get_mark() != pattern_tile.get_paint() and pattern_tile.get_mark() != PaintType.EMPTY:
#                 use_secondary = pattern_tile.get_mark() == PaintType.ALLY_SECONDARY
#                 if can_attack(pattern_tile.get_map_location()):
#                     attack(pattern_tile.get_map_location(), use_secondary)

#         # Complete the ruin if we can.
#         if can_complete_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc):
#             complete_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc)
#             set_timeline_marker("Tower built", 0, 255, 0)
#             log("Built a tower at " + str(target_loc) + "!")

#     # Move and attack randomly if no objective.
#     dir = directions[random.randint(0, len(directions) - 1)]
#     next_loc = get_location().add(dir)
#     if can_move(dir):
#         move(dir)

#     # Try to paint beneath us as we walk to avoid paint penalties.
#     # Avoiding wasting paint by re-painting our own tiles.
#     current_tile = sense_map_info(get_location())
#     if not current_tile.get_paint().is_ally() and can_attack(get_location()):
#         attack(get_location())

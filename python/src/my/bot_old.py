import random

from battlecode25.stubs import *
# from battlecode25.engine.game.robot_controller import RobotError



# Globals
turn_count = 0
directions = [
    Direction.NORTH,
    Direction.NORTHEAST,
    Direction.EAST,
    Direction.SOUTHEAST,
    Direction.SOUTH,
    Direction.SOUTHWEST,
    Direction.WEST,
    Direction.NORTHWEST,
]
known_ruins = []
painting_turns = 0

def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    global turn_count
    turn_count += 1

    if get_type() == UnitType.SOLDIER:
        run_soldier()
    elif get_type() == UnitType.MOPPER:
        run_mopper()
    elif get_type() == UnitType.SPLASHER:
        pass  # TODO
    elif get_type().is_tower_type():
        run_tower()
    else:
        pass  # Other robot types?




def run_tower():
    # Pick a direction to build in.
    dir = directions[random.randint(0, len(directions) - 1)]
    next_loc = get_location().add(dir)

    # Pick a random robot type to build.
    robot_type = random.randint(0,0)
    # if robot_type == 0 and not can_build_robot(UnitType.SOLDIER, next_loc):
    #     log("Trying to build a soldier at " + str(next_loc))

    if robot_type == 0 and can_build_robot(UnitType.SOLDIER, next_loc):
        build_robot(UnitType.SOLDIER, next_loc)
        log("BUILT A SOLDIER")
    # if robot_type == 1 and can_build_robot(UnitType.MOPPER, next_loc):
    #     build_robot(UnitType.MOPPER, next_loc)
    #     log("BUILT A MOPPER")
    # if robot_type == 2 and can_build_robot(UnitType.SPLASHER, next_loc):
    #     set_indicator_string("SPLASHER NOT IMPLEMENTED YET");
    #     build_robot(UnitType.SPLASHER, next_loc)
    #     log("BUILT A SPLASHER")

    # Read incoming messages
    messages = read_messages()
    for m in messages:
        log(f"Tower received message: '#{m.get_sender_id()}: {m.get_bytes()}'")

    # Broadcast seen ruins
    nearby_tiles = sense_nearby_map_infos()
    for tile in nearby_tiles:
        if tile.has_ruin():
            loc = tile.get_map_location()
            for ally in sense_nearby_robots(team=get_team()):
                if can_send_message(ally.location):
                    encoded = (0 << 16) | (loc.x << 8) | loc.y
                    send_message(ally.location, encoded)

def run_soldier():

    # Read shared ruin locations
    messages = read_messages()
    for m in messages:
        m = m.get_bytes()
        tag = (m >> 16) & 0xF
        x = (m >> 8) & 0xFF
        y = m & 0xFF
        if tag == 0:  # 0 = RUIN message
            loc = MapLocation(x, y)
            if loc not in known_ruins:
                known_ruins.append(loc)

    # Sense information about all visible nearby tiles.
    nearby_tiles = sense_nearby_map_infos()

    # Check for visible ruins first
    cur_ruin = None
    for tile in nearby_tiles:
        if tile.has_ruin():
            cur_ruin = tile
            loc = tile.get_map_location()
            if loc not in known_ruins:
                known_ruins.append(loc)

    # If no visible ruins, go to remembered ones
    if cur_ruin is None and known_ruins:
        # Clean up ruins that no longer exist
        for loc in known_ruins:
            if can_sense_location(loc) and not sense_map_info(loc).has_ruin():
                known_ruins.remove(loc)



    if cur_ruin is not None:
        global painting_turns
        distance = 0
        tangent = None
        if painting_turns % 3 == 0:
            to_ruin = get_location().direction_to(cur_ruin.get_map_location())
            tangent = to_ruin.rotate_right().rotate_right()
            distance = get_location().distance_squared_to(cur_ruin.get_map_location())

        if distance > 4:
            tangent = tangent.rotate_left()

        if can_move(tangent):
            move(tangent)
        painting_turns += 1
        target_loc = cur_ruin.get_map_location()
        dir = get_location().direction_to(target_loc)

        # if can_move(dir):
        #     move(dir)

        # Mark the pattern we need to draw to build a tower here if we haven't already.
        should_mark = cur_ruin.get_map_location().subtract(dir)
        if sense_map_info(should_mark).get_mark() == PaintType.EMPTY and can_mark_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc):
            mark_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc)
            log("Trying to build a tower at " + str(target_loc))

        # Fill in any spots in the pattern with the appropriate paint.
        for pattern_tile in sense_nearby_map_infos(target_loc, 8):
            if pattern_tile.get_mark() != pattern_tile.get_paint() and pattern_tile.get_mark() != PaintType.EMPTY:
                use_secondary = pattern_tile.get_mark() == PaintType.ALLY_SECONDARY
                if can_attack(pattern_tile.get_map_location()):
                    attack(pattern_tile.get_map_location(), use_secondary)

        # Complete the ruin if we can.
        if can_complete_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc):
            complete_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, target_loc)
            set_timeline_marker("Tower built", 0, 255, 0)
            log("Built a tower at " + str(target_loc) + "!")

    if known_ruins:
        index = get_id() % len(known_ruins)
        target_loc = known_ruins[index if random.random() > 0.6 else -1]
        dir = get_location().direction_to(target_loc)
        if can_move(dir):
            move(dir)

    # Move and attack randomly if no objective.
    dir = directions[random.randint(0, len(directions) - 1)]
    next_loc = get_location().add(dir)
    if can_move(dir):
        move(dir)

    # Try to paint beneath us as we walk to avoid paint penalties.
    # Avoiding wasting paint by re-painting our own tiles.
    current_tile = sense_map_info(get_location())
    if not current_tile.get_paint().is_ally() and can_attack(get_location()):
        attack(get_location())




def run_mopper():
    # Move and attack randomly.
    dir = directions[random.randint(0, len(directions) - 1)]
    next_loc = get_location().add(dir)
    if can_move(dir):
        move(dir)
    if can_mop_swing(dir):
        mop_swing(dir)
        # log("Mop Swing! Booyah!");
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

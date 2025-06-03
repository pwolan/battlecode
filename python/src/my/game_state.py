# game_state.py

turn_count = 0
known_ruins = []
painting_turns = {}
save_turns = 0

def increment_turn():
    global turn_count
    turn_count += 1

def get_turn_count():
    return turn_count

def get_known_ruins():
    return known_ruins

def add_known_ruin(loc):
    if loc not in known_ruins:
        known_ruins.append(loc)

def remove_known_ruin(loc):
    if loc in known_ruins:
        known_ruins.remove(loc)

def get_painting_turns(robot_id):
    return painting_turns.get(robot_id, 0)

def increment_painting_turn(robot_id):
    painting_turns[robot_id] = get_painting_turns(robot_id) + 1

def set_save_turns(turns):
    global save_turns
    save_turns = turns

def decrement_save_turns():
    global save_turns
    if save_turns > 0:
        save_turns -= 1

def should_save():
    return save_turns > 0

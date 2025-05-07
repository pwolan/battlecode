import random

from battlecode25.stubs import *
from globals import directions

from qtable import Q_TABLE

# Q-learning parameters
epsilon = 0.1    # exploration rate
alpha = 0.1      # learning rate
gamma = 0.9      # discount factor

# Q-table: maps (state, action) -> value
Q = Q_TABLE
last_state = None
last_action = None

# Reward shaping parameters
time_penalty = -0.01
tower_reward = 10
paint_reward = 0.1


def get_state():
    """
    Build a discrete state representation for the soldier.
    Here: (has_visible_ruin, current_tile_paint)
    """
    # Detect any visible ruin
    nearby = sense_nearby_map_infos()
    has_ruin = 0
    ruin_dir = None
    for tile in nearby:
        if tile.has_ruin():
            has_ruin = 1
            ruin_dir = get_location().direction_to(tile.get_map_location())
            break

    # Encode current paint under soldier
    cur = sense_map_info(get_location())
    if cur:
        print("wa")
        paint_code = cur.get_paint().to_int()

    # State tuple
        return (has_ruin, paint_code)
    return (has_ruin, None)


def choose_action(state):
    """
    Epsilon-greedy action selection over movement directions.
    """
    # Exploration
    if random.random() < epsilon:
        return random.choice(directions)

    # Greedy: pick action with highest Q
    values = [Q.get((state, d), 0) for d in directions]
    max_val = max(values)
    # break ties randomly
    best = [d for d, v in zip(directions, values) if v == max_val]
    return random.choice(best)


def compute_reward(completed_tower=False):
    """
    Reward function: shape behavior toward tower building and efficient movement.
    """
    r = time_penalty
    if completed_tower:
        r += tower_reward
    # reward for moving onto enemy or ally paint
    cur = sense_map_info(get_location())
    if cur.get_paint().is_ally():
        r += paint_reward
    return r


def update_q(prev_state, prev_action, reward, curr_state):
    """
    Q-learning update rule.
    """
    prev_q = Q.get((prev_state, prev_action), 0)
    # estimate of optimal future value
    future_q = max(Q.get((curr_state, a), 0) for a in directions)
    # Q-learning Bellman update
    Q[(prev_state, prev_action)] = prev_q + alpha * (reward + gamma * future_q - prev_q)


def run_soldier():
    global last_state, last_action

    # Get current state
    state = get_state()
    # Choose direction via Q-learning policy
    action_dir = choose_action(state)

    # Try to move
    moved = False
    if can_move(action_dir):
        move(action_dir)
        moved = True

    # Handle marking or building if near ruin
    completed = False
    nearby = sense_nearby_map_infos()
    for tile in nearby:
        if tile.has_ruin():
            loc = tile.get_map_location()
            if can_complete_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, loc):
                complete_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER, loc)
                completed = True
            break

    # Compute reward after action
    reward = compute_reward(completed)

    # Q-update from last step
    if last_state is not None and last_action is not None:
        update_q(last_state, last_action, reward, state)

    # Save for next turn
    last_state = state
    last_action = action_dir
    # Optional: log action for debugging
    set_indicator_string(f"Q-act: {action_dir}, r={reward:.2f}")
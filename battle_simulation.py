from config import DEBUG, IDEAL_TURNS, IDEAL_TURNS_TOLERANCE
from battle_state import BattleState
from collections import Counter

import numpy

if DEBUG:
    battle_log = open('battle_log.log', 'w')
    def log_battle_data(string):
        battle_log.write(string + "\n")
        
battle_id = 0
def battle_simulation(moves, player_1, player_2):
    """
    Performs a battle simulation, where player1 and player2 take turns using
    moves until someone dies.
    """
    global battle_id
    p1_name, p2_name = player_1.__name__, player_2.__name__
    
    battle_state = BattleState(players = (player_1, player_2))
    turns = 0
    move_usage= Counter(dict([(id(move), 0) for move in moves]))
    absolute_value_record = [battle_state.absolute_value()]
    
    if DEBUG:
        log_battle_data("Battle %d" % (1+battle_id, ))
        log_battle_data("\tTurn 0: %s" % (str(battle_state),))
    
    while battle_state.players_alive() and turns < 30:
        move = player_1.get_move(battle_state)
        battle_state = move.apply(battle_state)
        move_usage[id(move)]+= 1
        turns += 1
        if DEBUG:
            log_battle_data("\t\tMove: %s" % (str(move),))
            log_battle_data("\tTurn %d: %s" % (turns, str(battle_state)))
        
        absolute_value_record.append(battle_state.absolute_value())
        
    if DEBUG:
        log_battle_data("\t" + battle_state.get_winner())
    
    # Calculate Metrics of success
    
    # Was the length good?
    length_good = abs(IDEAL_TURNS - turns) <= IDEAL_TURNS_TOLERANCE
    if not length_good:
        length_success = -50 
    else:
        length_success = 50. * abs(turns - IDEAL_TURNS) / float(IDEAL_TURNS)
    
    # Did someone win?
    if length_good and battle_state.is_one_winner():
        victory_success = 50
    else:
        victory_success = -50
        
    # Were attacks used evenly?
    move_usage = [usage / float(turns) for usage in move_usage.values()]
    #print sum(normalize_move_usage) , MAXIMUM_MOVE_USAGE
    move_usage_success = -50 * numpy.std(move_usage)
    
    # Did the battle progress linearly?
    if abs(IDEAL_TURNS - turns) < IDEAL_TURNS_TOLERANCE:
        def ideal_decay(time):
            return 200 - time * 200. / turns
        distance_from_ideal = sum([abs(ideal_decay(i) - actual) for i, actual in enumerate(absolute_value_record)])
        maximum = 100. * (turns + 1)
        linearity_success = -50 * distance_from_ideal / maximum
    else:
        linearity_success = -50
    
    # Summate the sucesses
    total_success = sum((length_success, victory_success, move_usage_success, linearity_success))
    if DEBUG:
        log_battle_data("\t%d, %d, %d, %d, %d" % (length_success, victory_success, move_usage_success, linearity_success, total_success))
        
    battle_id+= 1
    return total_success, battle_id
import random
#random.seed(33)
from config import CONFIG, update_attributes
import argparse

if __name__ == "__main__":

    # Get Command Line Arguments
    parser = argparse.ArgumentParser(description='Setup configuration for the Attribute Learning System')
    parser.add_argument('-p1', "--player1", type=str, help="Player 1's type", default='minimax')
    parser.add_argument('-p2', "--player2", type=str, help="Player 2's type", default='minimax')
    parser.add_argument('-f', "--function_type", type=str, help='type of function for learning', default='vector')
    parser.add_argument('-ap', "--primary_attributes", type=int, help='number of primary attributes per player', default=1)
    parser.add_argument('-as', "--secondary_attributes", type=int, help='number of secondary attributes per player', default=2)
    parser.add_argument('-re', "--retain_percent", type=float, help='percentage of population to retain, given as a decimal', default=CONFIG['retain_percent'])
    parser.add_argument('-mu', "--mutation_rate", type=float, help='percentage of population to mutate, given as a decimal', default=CONFIG['mutation_rate'])
    parser.add_argument('-ra', "--radiation_amount", type=int, help='level of mutation undergone during mutate phase', default=CONFIG['radiation_amount'])
    parser.add_argument('-n', '--name', type=str, help="The name of the resulting .data file", default="untitled")

    # Put CL args into the config dict
    CONFIG.update(vars(parser.parse_args()))

    update_attributes()

    # Update the Function Type
    if CONFIG['function_type'] == "vector":
        from function_vector import FunctionVector
        CONFIG['function_type'] = FunctionVector
    elif CONFIG['function_type'] == "tree":
        from function_tree import FunctionTree
        CONFIG['function_type'] = FunctionTree

    # Update the Players
    from players import GreedyPlayer, RandomPlayer, MinimaxPlayer
    player_type_map = {"minimax": MinimaxPlayer, "greedy": GreedyPlayer, "random": RandomPlayer}
    CONFIG['player1'] = player_type_map[CONFIG['player1']]
    CONFIG['player2'] = player_type_map[CONFIG['player2']]

    # Run the system
    from genetic import genetic
    best_result = genetic((CONFIG['player1'], CONFIG['player2']),
                          CONFIG['population_size'],
                          CONFIG['iterations_limit'],
                          CONFIG['retain_percent'],
                          CONFIG['mutation_rate'],
                          CONFIG['radiation_amount'])

    from movelist_validation import test_movelist
    test_movelist(best_result)
    # for index, move in enumerate(best_result):
        # print "Move", 1+index
        # print "\t",move.feature, "=", move
        
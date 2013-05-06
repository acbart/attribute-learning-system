import random
random.seed(33)
import config
from genetic import genetic
import argparse
from config import CMDLINE
from players import PLAYERS, GreedyPlayer, RandomPlayer, MinimaxPlayer

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Setup configuration for the Attribute Learning System')
    parser.add_argument('population', type=int, help='total move list population used')
    parser.add_argument('iterations', type=int, help='number of iterations to use for simulation')
    parser.add_argument('retain percent', type=float, help='percentage of population to retain, given as a decimal')
    parser.add_argument('mutation rate', type=float, help='percentage of population to mutate, given as a decimal')
    parser.add_argument('radiation amount', type=int, help='level of mutation undergone during mutate phase')

    if CMDLINE:
        args = vars(parser.parse_args())
        best_result = genetic((MinimaxPlayer,MinimaxPlayer),
                          args['population'],
                          args['iterations'],
                          args['retain percent'],
                          args['mutation rate'],
                          args['radiation amount'])
    else:
        best_result = genetic((MinimaxPlayer,MinimaxPlayer),
                          config.POPULATION_SIZE,
                          config.ITERATIONS_LIMIT,
                          config.RETAIN_PARENTS,
                          config.MUTATION_RATE,
                          config.RADIATION_AMOUNT)

    for index, move in enumerate(best_result):
        print "Move", 1+index
        print "\t",move.feature, "=", move

import random
random.seed(33)
import config
from genetic import genetic
import argparse
from players import PLAYERS, GreedyPlayer, RandomPlayer, MinimaxPlayer

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Setup configuration for the Attribute Learning System')
    parser.add_argument('-population', "--population", type=int, help='total move list population used', default=config.POPULATION_SIZE)
    parser.add_argument('-iterations', "--iterations", type=int, help='number of iterations to use for simulation', default=config.ITERATIONS_LIMIT)
    parser.add_argument('-retain_percent', "--retain_percent", type=float, help='percentage of population to retain, given as a decimal', default=config.RETAIN_PARENTS)
    parser.add_argument('-mutation_rate', "--mutation_rate", type=float, help='percentage of population to mutate, given as a decimal', default=config.MUTATION_RATE)
    parser.add_argument('-radiation_amount', "--radiation_amount", type=int, help='level of mutation undergone during mutate phase', default=config.RADIATION_AMOUNT)

    args = vars(parser.parse_args())
    best_result = genetic((MinimaxPlayer,MinimaxPlayer),
                          args['population'],
                          args['iterations'],
                          args['retain_percent'],
                          args['mutation_rate'],
                          args['radiation_amount'])

    for index, move in enumerate(best_result):
        print "Move", 1+index
        print "\t",move.feature, "=", move

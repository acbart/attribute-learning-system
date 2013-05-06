import random
random.seed(33)
import config

from genetic import genetic
from players import PLAYERS, GreedyPlayer, RandomPlayer, MinimaxPlayer


if __name__ == "__main__":
    best_result = genetic((MinimaxPlayer,MinimaxPlayer),
                          config.POPULATION_SIZE, 
                          config.ITERATIONS_LIMIT, 
                          config.RETAIN_PARENTS, 
                          config.MUTATION_RATE, 
                          config.RADIATION_AMOUNT)
    
    for index, move in enumerate(best_result):
        print "Move", 1+index
        print "\t",move.feature, "=", move
    print CONFIG
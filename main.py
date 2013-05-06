import random
random.seed(33)
import config
from function_vector import FunctionVector
from function_tree import FunctionTree
from move_list import FUNCTION_TYPE
from config import ATTRIBUTE_TYPES, ATTRIBUTES, PRIMARIES, SECONDARIES, ATTRIBUTE_AFFECTS, FUNC_TYPE
from genetic import genetic
import argparse
from players import PLAYERS, GreedyPlayer, RandomPlayer, MinimaxPlayer


# this is an ugly hack for the minute
def reset_attributes(primary_attribute, secondary_attributes):
    ATTRIBUTES = []
    ATTRIBUTE_TYPES = {"primary": primary_attribute, "secondary": secondary_attributes}
    for person in ["self", "other"]:
        for attribute_type, occurrence in ATTRIBUTE_TYPES.items():
            for i in xrange(1, 1+occurrence):
                ATTRIBUTES.append( "_".join((person, attribute_type, str(i))) )
    ATTRIBUTES = tuple(ATTRIBUTES)

    PRIMARIES = [str(i) for i in range(1, 1+ATTRIBUTE_TYPES["primary"])]
    SECONDARIES = [str(i) for i in range(1, 1+ATTRIBUTE_TYPES["secondary"])]
    ATTRIBUTE_AFFECTS = {}
    for index in PRIMARIES:
        ATTRIBUTE_AFFECTS["self_primary_"+index] = tuple(["self_secondary_"+i for i in SECONDARIES])
        ATTRIBUTE_AFFECTS["other_primary_"+index] = tuple(["self_secondary_"+i for i in SECONDARIES]+
                                                         ["other_secondary_"+i for i in SECONDARIES])
    for index in SECONDARIES:
        ATTRIBUTE_AFFECTS["self_secondary_"+index] = tuple(["self_secondary_"+i for i in SECONDARIES]+
                                                           ["self_primary_"+i for i in PRIMARIES])
        ATTRIBUTE_AFFECTS["other_secondary_"+index] = tuple(["self_secondary_"+i for i in SECONDARIES]+
                                                         ["other_secondary_"+i for i in SECONDARIES]+
                                                         ["self_primary_"+i for i in PRIMARIES]+
                                                         ["other_primary_"+i for i in PRIMARIES])

    return (ATTRIBUTE_TYPES, ATTRIBUTES, PRIMARIES, SECONDARIES, ATTRIBUTE_AFFECTS)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Setup configuration for the Attribute Learning System')
    parser.add_argument('-function_type', "--function_type", type=str, help='type of function for learning')
    parser.add_argument('-primary_attributes', "--primary_attributes", type=int, help='number of primary attributes per player', default=3)
    parser.add_argument('-secondary_attributes', "--secondary_attributes", type=int, help='number of secondary attributes per player', default=2)
    parser.add_argument('-retain_percent', "--retain_percent", type=float, help='percentage of population to retain, given as a decimal', default=config.RETAIN_PARENTS)
    parser.add_argument('-mutation_rate', "--mutation_rate", type=float, help='percentage of population to mutate, given as a decimal', default=config.MUTATION_RATE)
    parser.add_argument('-radiation_amount', "--radiation_amount", type=int, help='level of mutation undergone during mutate phase', default=config.RADIATION_AMOUNT)

    args = vars(parser.parse_args())
    ATTRIBUTE_TYPES, ATTRIBUTES, PRIMARIES, SECONDARIES, ATTRIBUTE_AFFECTS = reset_attributes(args['primary_attributes'], args['secondary_attributes'])

    FUNC_TYPE = args['function_type']

    best_result = genetic((MinimaxPlayer,MinimaxPlayer),
                          config.POPULATION_SIZE,
                          config.ITERATIONS_LIMIT,
                          args['retain_percent'],
                          args['mutation_rate'],
                          args['radiation_amount'])

    for index, move in enumerate(best_result):
        print "Move", 1+index
        print "\t",move.feature, "=", move

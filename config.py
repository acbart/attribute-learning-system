
ATTRIBUTES = []
ATTRIBUTE_TYPES = {"primary": 1, "secondary": 2}
for person in ["self", "other"]:
    for attribute_type, occurrence in ATTRIBUTE_TYPES.items():
        for i in xrange(1, 1+occurrence):
            ATTRIBUTES.append( "_".join((person, attribute_type, str(i))) )
ATTRIBUTES = tuple(ATTRIBUTES)

ATTRIBUTE_AFFECTS = {"self_primary_1" : ("other_secondary_1", "self_secondary_2"),
                     "self_secondary_1" : ("other_secondary_1", "self_secondary_2"),
                     "self_secondary_2": ("other_secondary_1", "other_primary_1"),
                     "other_primary_1" : ("self_secondary_1", "other_secondary_2"),
                     "other_secondary_1" : ("self_secondary_1", "other_secondary_2"),
                     "other_secondary_2": ("self_secondary_1", "self_primary_1")}
            
NUMBER_OF_MOVES_PER_MOVE_LIST = 6   # 
DEBUG = True                       # Whether to log data

MOVE_FEATURE_CHANGE_RATE = 1000 # 1 in MOVE_FEATURE_CHANGE_RATE of changing

FEATURE_VECTOR_RANGE = (1,2)
FEATURE_COEFFECIENTS_DOMAIN = (-5, 5)
FEATURE_MUTATION_FLUCTATION_RANGE = (-5, 5)

IDEAL_TURNS = 10            # The ideal turns of a battle simulation (each player takes a turn)
IDEAL_TURNS_TOLERANCE = 5   # How far you can be from the IDEAL_TURNS before it's no longer acceptable

HEIGHT_MAX = 2              # The maximum height of a Function Tree
RANDOM_VARIABLES = False    # Whether to use ConstantNodes (I don't know if this still works)

BOOLEANS = (True, False)        # Simple convenience constant

MOVE_COMBINATIONS = ["none", "single", "all"][0]

# genetic.py parameters
POPULATION_SIZE = 100
ITERATIONS_LIMIT = 4
RETAIN_PARENTS = .1
MUTATION_RATE = .4
RADIATION_AMOUNT = 1

from function_tree import FunctionTree
FUNCTION_TYPE = FunctionTree
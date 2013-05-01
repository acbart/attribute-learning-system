
ATTRIBUTES = {"primary": 1, "secondary": 2}

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
POPULATION_SIZE = 500
ITERATIONS_LIMIT = 10
RETAIN_PARENTS = .1
MUTATION_RATE = .4
RADIATION_AMOUNT = 1

from function_vector import FunctionVector
FUNCTION_TYPE = FunctionVector
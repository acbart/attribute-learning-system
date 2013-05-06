ATTRIBUTES = []
ATTRIBUTE_TYPES = {"primary": 1, "secondary": 2}
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
ITERATIONS_LIMIT = 25
RETAIN_PARENTS = .3
MUTATION_RATE = .5
RADIATION_AMOUNT = 5

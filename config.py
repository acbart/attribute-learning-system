CONFIG = {}
CONFIG['population_size'] = 500
CONFIG['iterations_limit'] = 25
CONFIG['retain_percent'] = .3 
CONFIG['mutation_rate'] =  .5
CONFIG['radiation_amount'] = 5
CONFIG['function_type'] = 'vector'
CONFIG['primary_attributes'] = 1
CONFIG['secondary_attributes'] = 2
CONFIG['name'] = 'untitled'
CONFIG['number_of_moves_per_move_list'] = 6   #
CONFIG['player1'] = 'minimax'
CONFIG['player2'] = 'minimax'
DEBUG = False                       # Whether to log data

CONFIG['feature_vector_range'] = (1,2)
CONFIG['feature_coeffecients_domain'] = (-5, 5)
CONFIG['feature_mutation_fluctation_range'] = (-5, 5)

CONFIG['height_max'] = 2              # The maximum height of a Function Tree

CONFIG['move_combinations'] = ["none", "single", "all"][0]

def update_attributes():
    # Update the attributes
    ATTRIBUTE_TYPES = {"primary": CONFIG['primary_attributes'], "secondary": CONFIG['secondary_attributes']}
    ATTRIBUTES = []
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
    CONFIG['attribute_types'] = ATTRIBUTE_TYPES
    CONFIG['attributes'] = ATTRIBUTES
    CONFIG['primaries'] = PRIMARIES
    CONFIG['secondaries'] = SECONDARIES
    CONFIG['attribute_affects'] = ATTRIBUTE_AFFECTS
    
update_attributes()
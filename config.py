CONFIG = {}
CONFIG['population_size'] = 500
CONFIG['iterations_limit'] = 2 #25
CONFIG['retain_percent'] = .3 
CONFIG['mutation_rate'] =  .5
CONFIG['radiation_amount'] = 5
CONFIG['number_of_moves_per_move_list'] = 6   #
DEBUG = True                       # Whether to log data

CONFIG['feature_vector_range'] = (1,2)
CONFIG['feature_coeffecients_domain'] = (-5, 5)
CONFIG['feature_mutation_fluctation_range'] = (-5, 5)

CONFIG['height_max'] = 2              # The maximum height of a Function Tree

CONFIG['move_combinations'] = ["none", "single", "all"][0]
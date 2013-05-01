import random
from orderedset import OrderedSet
from move_list import MoveList
from function_vector import FunctionVector
from move import Move
<<<<<<< HEAD
from players import PLAYERS, GreedyPlayer, RandomPlayer
from config import DEBUG, MOVE_COMBINATIONS
=======
from players import PLAYERS, GreedyPlayer, RandomPlayer, MinimaxPlayer
from config import DEBUG
>>>>>>> 026166d717ddded6c770367c79c85847768d036a
from battle_simulation import battle_simulation
import time

from itertools import permutations

def avg(values):
    return sum(values) / float(len(values))

def genetic(players = None,
            population_size = 100, 
            iterations_limit = 10,
            retain_parents = .1,
            mutation_rate = .4,
            radiation_amount = 1):

    # Logging for debug purposes
    if DEBUG:
        genetic_log = open('genetic.log', 'w')
        def log_genetic_data(string):
            genetic_log.write(string + "\n")

    # If needed, generate random players
    if players is None:
        first_player = MinimaxPlayer#random.choice(PLAYERS)
        second_player = MinimaxPlayer#random.choice(PLAYERS)
    else:
        first_player, second_player = players

    # Create the evaluation function
    simulation_results_cache = {}
    prior = time.time()
    def evaluate_population(population):
        """
        Given a list of move lists (the population),
        Returns a list of (move list, value of move list, corresponding battle_id)
        that is sorted by the values.
        """
        population_values = []
        duplicates = 0
        for move_list in population:
            if move_list.short_string() in simulation_results_cache:
                value, battle_ids = simulation_results_cache[move_list.short_string()]
                duplicates += 1
            else:
                values = []
                battle_ids = []
                
                # Determine what variants on this MoveList we'll test
                if MOVE_COMBINATIONS == "all":
                    move_lists = [(MoveList(list(permutation) + move_list.subtract(permutation)))
                                        for permutation in permutations(move_list, len(move_list)/2)]
                elif MOVE_COMBINATIONS == "single":
                    move_lists = (move_list, MoveList(reversed(move_list)))
                elif MOVE_COMBINATIONS == "none":
                    move_lists = (move_list,)
                
                # Run each variant in a simulation
                for permutation in move_lists:
                    player_movelists = permutation[:3], permutation[3:]
                    value, battle_id = battle_simulation(move_list, 
                                                         first_player(*player_movelists),
                                                         second_player(*player_movelists))
                    values.append(value)
                    battle_ids.append(battle_id)
                value = avg(values)
                
                # Store the result in case we reuse this MoveList
                simulation_results_cache[move_list.short_string()] = (value, battle_ids)
            
            population_values.append( (move_list, value, battle_ids) )
            
        population_values.sort(key = lambda item: -item[1]) # sort by value

        if DEBUG:
            log_genetic_data("\tDuplicates: %d" % (duplicates,))

        return population_values

    # Generate the new population
    population = [MoveList() for x in xrange(population_size)]

    # Iterate through the Genetic Algorithm
    for iteration in xrange(iterations_limit):

        # Log this iteration
        if DEBUG: log_genetic_data("Iteration: %d" % (1+iteration,))

        # Calculate the size of the segments of our new population
        parents_retained = int(round(retain_parents * population_size))
        mutants_generated = int(round(mutation_rate * population_size))

        # Run the simulation on each move_list, and sort by best
        population_values = evaluate_population(population)

        # Log the values and battle ids
        if DEBUG:
            for move_list, value, battle_id in population_values:
                log_genetic_data("\tValue: %d, Battle: %s, Move List: %s" % 
                                 (value, str(battle_id), move_list.short_string()))

        # create our new population
        population = OrderedSet()
        top_perfomers = population_values[:parents_retained]

        # Retain the top performers of the old generation
        for move_list, value, battle_id in top_perfomers:
            population.add(move_list)

        # Add in the mutants!
        while len(population) - parents_retained  < mutants_generated:
            mutant, value, battle_id = random.choice(top_perfomers)
            for r in xrange(radiation_amount):
                mutant = mutant.mutate()
            population.add(mutant)

        # Add in the children!
        while len(population) < population_size:
            dad, mom = random.sample(population, 2)
            child = dad.cross_over(mom).mutate()
            population.add(child)

        # Report to the user that we've finished an iteration!
        print "Iteration", str(iteration+1), "Time:", round(time.time() - prior, 3)
        prior = time.time()

    # Calculate the final resulting population
    results = evaluate_population(population)

    # Close up the log
    if DEBUG:
        log_genetic_data("Final Results")
        for move_list, value, battle_id in population_values:
            log_genetic_data("\tValue: %d, Battle: %d, Move List: %s" %
                             (value, battle_id, move_list.short_string()))
    if DEBUG: genetic_log.close()

    # Return the best state
    return results[0][0]

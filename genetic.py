import random
from orderedset import OrderedSet
from move_list import MoveList
from config import DEBUG, CONFIG
from battle_simulation import battle_simulation
import time
import numpy

from itertools import permutations

def avg(values):
    return sum(values) / float(len(values))

def genetic(players, population_size, iterations_limit, retain_parents, mutation_rate, radiation_amount):

    # Iteration log
    results_log = open('data/results-%s.data' % CONFIG['name'], 'w')
    results_log.write('Name | Player 1 Type | Player 2 Type | Function Type | Primary Attributes | Secondary Attributes | Parents Retained | Mutation Rate' + "\n")
    results_log.write('' + CONFIG['name'])
    results_log.write(' | ' + players[0].__name__)
    results_log.write(' | ' + players[1].__name__)
    results_log.write(' | ' + CONFIG['function_type'].__name__)
    results_log.write(' | ' + str(CONFIG['primary_attributes']))
    results_log.write(' | ' + str(CONFIG['secondary_attributes']))
    results_log.write(' | ' + str(retain_parents))
    results_log.write(' | ' + str(mutation_rate) + "\n\n")

    results_log.write('Iteration | Time Taken | Maximum Utility | Average Utility | Stddev of Utility | Battle ID | MoveList')

    # Logging for debug purposes
    if DEBUG:
        genetic_log = open('genetic.log', 'w')
        def log_genetic_data(string):
            genetic_log.write(string + "\n")

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
                value, battle_ids, winners = simulation_results_cache[move_list.short_string()]
                duplicates += 1
            else:
                values = []
                battle_ids = []
                winners = []

                # Determine what variants on this MoveList we'll test
                if CONFIG['move_combinations'] == "all":
                    move_lists = [(MoveList(list(permutation) + move_list.subtract(permutation)))
                                        for permutation in permutations(move_list, len(move_list)/2)]
                elif CONFIG['move_combinations'] == "single":
                    move_lists = (move_list, MoveList(reversed(move_list)))
                elif CONFIG['move_combinations'] == "none":
                    move_lists = (move_list,)

                # Run each variant in a simulation
                for permutation in move_lists:
                    player_1 = first_player(MoveList(permutation[:3]))
                    player_2 = second_player(MoveList(permutation[3:]))
                    player_1.opponent, player_2.opponent = player_2, player_1
                    value, battle_id, winner = battle_simulation(permutation, player_1, player_2)
                    values.append(value)
                    battle_ids.append(battle_id)
                    winners.append(winner)
                value = avg(values)

                # Store the result in case we reuse this MoveList
                simulation_results_cache[move_list.short_string()] = (value, battle_ids, winners)

            population_values.append( (move_list, value, battle_ids, winners) )

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
            for move_list, value, battle_id, winner in population_values:
                log_genetic_data("\tValue: %d, Battle: %s, Move List: %s" %
                                 (value, str(battle_id), move_list.short_string()))

        # create our new population
        population = OrderedSet()
        top_perfomers = population_values[:parents_retained]

        # Retain the top performers of the old generation
        for move_list, value, battle_id, winner in top_perfomers:
            population.add(move_list)

        # Add in the mutants!
        while len(population) - parents_retained  < mutants_generated:
            mutant, value, battle_id, winner = random.choice(top_perfomers)
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

        # Log details of this iteration
        move_list, moveset_value, battle_id, winner = population_values[0]
        all_utilities = [population_value[1] for population_value in population_values]
        results_log.write("\n" + str(iteration+1))
        results_log.write(" | " + str(round(time.time() - prior, 3)))
        results_log.write(" | " + str(moveset_value))
        results_log.write(" | " + str(numpy.mean(all_utilities)))
        results_log.write(" | " + str(numpy.std(all_utilities)))
        results_log.write(" | " + str(battle_id[0]))
        results_log.write(" | " + str(move_list))

        # Set timer for next iteration
        prior = time.time()

    # Calculate the final resulting population
    results = evaluate_population(population)

    # Close up the log
    if DEBUG:
        log_genetic_data("Final Results")
        for move_list, value, battle_id, winner in population_values:
            log_genetic_data("\tValue: %d, Battle: %s, Move List: %s" %
                             (value, str(battle_id), move_list.short_string()))
    if DEBUG: genetic_log.close()

    # Close the results log
    results_log.close()

    # Return the best state
    return results[0][0]

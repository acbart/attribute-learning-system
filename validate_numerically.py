import itertools
import time
from move import Move
import random
import numpy as np
import scipy.stats.stats as sp
from zss.compare import distance
random.seed(13)

class state(object):
    __slots__ = ["self_health", "self_attack", "self_defense",
                "other_health", "other_attack", "other_defense"]
    def __init__(self, row):
        self.self_health, self.self_attack, self.self_defense, self.other_health, self.other_attack, self.other_defense = row
    def get_value(self, attr):
        return getattr(self, attr)
   
if __name__ == "__main__":
    log = open("validation.log", "w")
    distance_to_numerical_log = open("dtn.log", "w")
    TRIALS = 100
    for radiation in xrange(1000):
        print "Radiation", radiation
        distance_to_numerical_log.write(str(radiation))
        log.write("Radiation Strength: %d\n" % radiation)
        trial_results = np.zeros(TRIALS, dtype=np.float64)
        trial_distances = np.zeros(TRIALS, dtype=np.float64)
        print "Trial", 
        for trial in xrange(TRIALS):
            #log.write("\tTrial: %d\n" % trial)
            original = Move.generate_random_move()
            mutant = original.copy()
            for x in xrange(radiation): mutant = mutant.mutate()
            prior_time = time.time()
            #results = np.zeros(10 ** 6, dtype=np.float64)
            #for i, row in enumerate(itertools.product(xrange(0, 100, 10), repeat=6)):
            #    s = state(row)
            #    results[i] = original.evaluate(s) - mutant.evaluate(s)
            #print sp.pearsonr(original_values, mutant_values)
            d = distance(original, mutant)
            #deviation = np.std(results,dtype=np.float64)
            #log.write("\t\tOriginal: %s\n" % (original,))
            #log.write("\t\tMutant: %s\n" % (mutant,))
            #log.write("\t\tDistance: %d\n" % (d,))
            #log.write("\t\tNumerical Deviation %f\n" % (deviation,))
            #log.write("\t\tTime: %f\n" % round(time.time() - prior_time, 2))
            #distance_to_numerical_log.write("%d, %f\n" % (d, deviation))
            trial_distances[trial] = d
            #trial_results[trial] = deviation
            print trial, 
        print ""
        distance_to_numerical_log.write(", %f, %f\n" % (np.mean(trial_distances), np.std(trial_distances)))
        log.write("\tDistance Mean: %f\n" % np.mean(trial_distances))
        log.write("\tDistance Stdev: %f\n" % np.std(trial_distances))
        #log.write("\tDeviation Mean: %f\n" % np.mean(trial_results))
        #log.write("\tDeviation Stdev: %f\n" % np.std(trial_results))
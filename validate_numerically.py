import random
random.seed(13)
import itertools
import time
from function_tree import FunctionTree
from function_vector import FunctionVector
from battle_state import BattleState
import numpy as np
import scipy
import scipy.stats.stats as sp
from config import ATTRIBUTES
from zss.compare import distance
import sys
import math

class State(dict):
    def get_value(self, feature):
        return self[feature]

# INPUTS = 100
# t1 = np.zeros(INPUTS, dtype=np.float64)
# t2 = np.zeros(INPUTS, dtype=np.float64)
# for i, input in enumerate(xrange(INPUTS)):
    # t1[i] = input * input * 5 + input * -3 + 10
    # t2[i] = input * input * 0 + input * -3 + 10
# print scipy.stats.ks_2samp(t1, t2)
   
# sys.exit()
   
if __name__ == "__main__":
    log = open("validation.log", "w")
    distance_to_numerical_log = open("dtn.csv", "w")
    TRIALS = 30
    check = "mutation_numerical"
    
    prior_time = time.time()
    if check == "cross_over":
        cros_log = open("col.log", "w")
        distances1 = np.zeros(TRIALS, dtype=np.float64)
        distances2 = np.zeros(TRIALS, dtype=np.float64)
        dads, moms = 0 , 0
        for trial in xrange(TRIALS):
            dad = FunctionTree()
            mom = FunctionTree()
            child = dad.cross_over(mom)
            d1 = distance(dad, mom)
            if float(d1) < 1:
                d2, d3 = 1, 1
            else:
                d2 = distance(child, dad) / float(d1)
                d3 = distance(child, mom) / float(d1)
            distances1[trial] = d2
            print "%.2f, %.2f" % (d2, d3)
            cros_log.write("%d, %f, %d, %d\n" % (d1, d2, len(dad), len(mom)))
        print np.mean(distances1), np.std(distances1), dads, moms
        cros_log.close()
    elif check == "vector_mutation_numerical":
        cros_log = open("vect_mut_num.csv", "w")
        for radiation in xrange(1, 100):
            print radiation
            for trial in xrange(TRIALS):
                original = FunctionVector()
                mutant = original.copy()                
                for x in xrange(radiation): mutant = mutant.mutate()
                STRIDE = 25
                POWER = 6
                o_values = np.zeros( math.ceil(201 / float(STRIDE)) ** POWER)
                m_values = np.zeros( math.ceil(201 / float(STRIDE)) ** POWER)
                for i, input in enumerate(itertools.product(xrange(-100, 100, STRIDE), repeat=POWER)):
                    state = State(dict(zip(ATTRIBUTES, input)))
                    o_values[i] = original.evaluate(state)
                    m_values[i] = mutant.evaluate(state)
                res = scipy.stats.ks_2samp(o_values, m_values)
                print "\t", trial, "(%.2f)" % (time.time() - prior_time,), res[0], res[1], radiation
                prior_time = time.time()
                cros_log.write("%d, %f, %f\n" % (radiation, res[0], res[1]))
    elif check == "mutation_numerical":
        mut_log = open("func_mut_num.csv", "w")
        for radiation in xrange(1, 100):
            for trial in xrange(TRIALS):
                original = FunctionTree()
                mutant = original.copy()
                for x in xrange(radiation): mutant = mutant.mutate()
                d = distance(original, mutant)
                STRIDE = 25
                POWER = 6
                o_values = np.zeros( math.ceil(201 / float(STRIDE)) ** POWER)
                m_values = np.zeros( math.ceil(201 / float(STRIDE)) ** POWER)
                for i, input in enumerate(itertools.product(xrange(-100, 100, STRIDE), repeat=POWER)):
                    state = State(dict(zip(ATTRIBUTES, input)))
                    o_values[i] = original.evaluate(state)
                    m_values[i] = mutant.evaluate(state)
                res = scipy.stats.ks_2samp(o_values, m_values)
                print "\t", trial, "(%.2f)" % (time.time() - prior_time,), res[0], res[1], d, radiation
                prior_time = time.time()
                mut_log.write("%d, %f, %f\n" % (radiation, res[0], res[1]))
    elif check == "mutation":
        for radiation in xrange(1, 20):
            print "Radiation", radiation
            distance_to_numerical_log.write(str(radiation))
            trial_distances = np.zeros(TRIALS, dtype=np.float64)
            for trial in xrange(TRIALS):
                original = FunctionTree()
                mutant = original.copy()
                for x in xrange(radiation): mutant = mutant.mutate()
                d = distance(original, mutant)
                trial_distances[trial] = d
                print "\t", trial, "("+ str(time.time() - prior_time) + ")", radiation, d
                prior_time = time.time()
               
            distance_to_numerical_log.write(", %f, %f\n" % (np.mean(trial_distances), np.std(trial_distances)))
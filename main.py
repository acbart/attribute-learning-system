import random
random.seed(42)

from genetic import genetic

if __name__ == "__main__":
    best_result = genetic()
    for index, move in enumerate(best_result):
        print "Move", 1+index
        for feature, function in move.iteritems():
            print "\t",feature, "=", function
            
import random
random.seed(33)

from genetic import genetic

if __name__ == "__main__":
    best_result = genetic()
    
    for index, move in enumerate(best_result):
        print "Move", 1+index
        for function in move:
            print "\t",function.feature, "=", function
            
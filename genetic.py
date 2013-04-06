import random
#random.seed(42)

from function_tree import FunctionTree

from simpleai.search.local import genetic
from simpleai.search import SearchProblem

class BattleState(object):
    __slots__ = ["health_1", "attack_1", "defense_1",
                 "health_2", "attack_2", "defense_2",
                 "turn"]
    def __init__(self, h1, a1, d1, h2, a2, d2):
        self.health_1 = h1
        self.attack_1 = a1
        self.defense_1 = d1 
        self.health_2 = h2 
        self.attack_2 = a2 
        self.defense_2 = d2
        self.turn = True

class FunProblem(SearchProblem):
    def generate_random_state(self):
        return FunctionTree()
        
    def crossover(self, state1, state2):
        return state1.cross_over(state2)
        
    def mutate(self, state):
        return state.mutate()
        
    def value(self, state):
        b = BattleState(100, 10, 10, 100, 10, 10)
        return - abs(42 - state.value(b)) * (4. / float(len(state)))

print "I'll try 10 times to find a cool equation"
for x in xrange(10):
    n = genetic(FunProblem(FunctionTree()), population_size=300)
    print "Attempt", x, "was",n.state, n.state.value(BattleState(100, 10, 10, 100, 10, 10))
import random
random.seed(42)

from function_tree import FunctionTree, AttributeNode

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
        
def battle_simulation(moveset, player1, player2):
    return sum([len(move) for move in moveset.moves])

def random_subset(list):
    return random.sample(list, random.randint(1, 1))#len(list)))
    
class Move(dict):
    all_features = ["health_1", "attack_1", "defense_1", "health_2", "attack_2", "defense_2"]
    
    def fill_randomly(self):
        for feature in random_subset(self.all_features):
            self[feature] = FunctionTree(AttributeNode(feature))
            for x in xrange(100): # RADIATION
                self[feature] = self[feature].mutate()
        return self
            
    def copy(self):
        new_move = Move()
        for k, v in self.iteritems():
            new_move[k] = v.copy()
        return new_move
    
    def mutate(self):
        #new_moveset = self.copy()
        #feature = random.choice(self.keys())
        #new_moveset[feature] = self[feature].mutate()
        #return new_moveset
        new_move = Move()
        for k, v in self.iteritems():
            new_move[k] = v.mutate()
        return new_move
        
    def cross_over(self, other):
        new_move = self.copy()
        for feature in self.all_features:
            if feature in self and feature in other:
                new_move[feature] = self[feature].cross_over(other[feature])
            elif feature in self:
                if random.choice((True, False)) and len(new_move) > 1:
                    del new_move[feature]
            elif feature in other:
                if random.choice((True, False)):
                    new_move[feature] = other[feature].copy()
        return new_move
        
    def __str__(self):
        return "{%s}" % (", ".join("%s <= %s" % (k, v) for k,v in self.iteritems()),)
    
    def value(self, battle_state):
        worth = 0
        for positive_feature in ("health_1", "attack_1", "defense_1"):
            if positive_feature in self:
                worth += self[positive_feature].value(battle_state)
        for negative_feature in ("health_2", "attack_2", "defense_2"):
            if negative_feature in self:
                worth -= self[negative_feature].value(battle_state)
        return worth
        
class MoveList(object):
    def __init__(self, moves = None):
        if moves is None:
            moves = [Move().fill_randomly() for i in xrange(3)]
        self.moves = list(moves)
    
    def cross_over(self, other):
        return MoveList([move1.cross_over(move2) for move1, move2 in zip(self.moves, other.moves)])
    
    def mutate(self):
        return MoveList([move.mutate() for move in self.moves])
        
    def __str__(self):
        return "[%s]" % (", ".join(map(str, self.moves)),)

class FunProblem(SearchProblem):
    def __init__(self, player1, player2):
        SearchProblem.__init__(self, MoveList())
        self.player1 = player1
        self.player2 = player2
        
    def generate_random_state(self):
        return MoveList()
        
    def crossover(self, state1, state2):
        return state1.cross_over(state2)
        
    def mutate(self, state):
        return state.mutate()
        
    def value(self, state):
        return battle_simulation(state, self.player1, self.player2)
        
    def pprint(self, state):
        return "\n".join(["Move %d:\n\t%s" % (i, "\n\t".join([k+": "+str(v) for k, v in s.iteritems()])) for i, s in enumerate(state)])
        

for x in xrange(1):
    n = genetic(FunProblem(None, None), population_size=500, iterations_limit=10, mutation_chance = .1)
    for i, move in enumerate(n.state.moves):
        print "Move", 1+i
        for k, v in move.iteritems():
            print "\t",k, "=", v
            #print "\t\t", getattr(b, k), "=>", v.value(b)
    #print "Attempt", x, "was", n.state
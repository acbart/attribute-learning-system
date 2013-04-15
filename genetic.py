import random
from random import choice
random.seed(42)
import time
import math

from orderedset import OrderedSet

from collections import Counter
from operator import itemgetter
from itertools import cycle

from function_tree import FunctionTree, AttributeNode
from players import PLAYERS

#from simpleai.search.local import genetic
from simpleai.search import SearchProblem

"""
BattleState is a simple representation of a battle, with the two players three
attributes being slots (for efficiency).

battle_simulation will actually run a battle and calculate its value. It
consumes a MoveList and a pair of Player instances. It will log all the battles
that it generates.

Move is a class that holds one or more FunctionTrees, mapping each one to and
attribute that they modify. In other words, this would be a "Move" in Pokemon:
if it affected "opponent's health" (health_2) than it would be a damaging move.
A Move can possibly affect more than one Attribute!

MoveList is basically a list of Move instances. In fact, it has a single useful
property ("moves") that is simple the list of Move instances. Otherwise, it
simply abstracts out some code from FunProblem.

FunProblem is the interface between SimpleAI's genetic search and a MoveList.
You can pass in specific Players to a FunProblem if you wish to see the game
played with different players.
"""

class BattleState(object):
    __slots__ = ["health_1", "attack_1", "defense_1",
                 "health_2", "attack_2", "defense_2"]
    def __init__(self, player_1=None, player_2=None, other = None):
        if other is not None:
            self.health_1 = other.health_1
            self.attack_1 = other.attack_1
            self.defense_1 = other.defense_1
            self.health_2 = other.health_2
            self.attack_2 = other.attack_2
            self.defense_2 = other.defense_2
        else:
            self.health_1, self.attack_1, self.defense_1 = player_1.get_initial_stats()
            self.health_2, self.attack_2, self.defense_2 = player_2.get_initial_stats()
    
    def flip(self):
        self.health_1, self.health_2 = self.health_2, self.health_1
        self.attack_1, self.attack_2 = self.attack_2, self.attack_1
        self.defense_1, self.defense_2 = self.defense_2, self.defense_1

    def players_alive(self):
        return self.health_1 > 0 and self.health_2 > 0
    
    def value(self):
        return self.health_1 - self.health_2
        
    def __str__(self):
        return "(H: %d, A: %d, D: %d), (H: %d, A: %d, D: %d)" % (self.health_1, self.attack_1, self.defense_1,self.health_2, self.attack_2, self.defense_2)
        
battle_log = open('battle_log.log', 'w')
battle_log.write("LET MORTAL COMBAT COMMENCE!\n")
battle_log.close()
battle_log = open('battle_log.log', 'a')
battle_id = 0
def battle_simulation(moves, player_1, player_2):
    """
    Performs a battle simulation, where player1 and player2 take turns using
    moves until someone dies.
    """
    global battle_id
    battle_state = BattleState(player_1, player_2)
    p1, p2 = player_1.__name__, player_2.__name__
    battle_log.write("Battle %d!\n" % (1+battle_id, ))
    turns = 0
    battle_log.write("Initial: %s" % (str(battle_state),))
    move_usage= Counter()
    life_record = [battle_state.health_1 + battle_state.health_2]
    while battle_state.players_alive() and turns < 20:
        battle_log.write("\tTurn %d\n" % (turns+1,))
        battle_state, move1 = player_1.move(battle_state)
        battle_log.write("\t\tPlayer 1's move: %s\n" % (str(move1),))
        move_usage[id(move1)]+= 1
        #battle_log.write("\t\t\t%s\n" % (str(battle_state),))
        if battle_state.health_2 > 0:
            battle_state, move2 = player_2.move(battle_state)
            battle_log.write("\t\tPlayer 2's move: %s\n" % (str(move2),))
            move_usage[id(move2)]+= 1
        battle_log.write("\t\t\t%s\n" % (str(battle_state),))
        turns += 1
        life_record.append(battle_state.health_1 + battle_state.health_2)
    if battle_state.health_1 <= 0 and battle_state.health_2 <= 0:
        battle_log.write("It was a tie after %d rounds (P12V)!\n" % (turns,))
    elif battle_state.health_1 <= 0:
        battle_log.write("Player 2 (%s) won in %d rounds (P2V))!\n" % (p2, turns))
    elif battle_state.health_2 <= 0:
        battle_log.write("Player 1 (%s) won in %d rounds (P1V)!\n" % (p1, turns))
    else:
        battle_log.write("No one won. That battle sucked (BOR)!\n")
    IDEAL_TURNS = 10
    total_moves = float(len(moves.moves))
    ideal = 100. / total_moves
    used_moves = [100. * v/(turns*2.) for v in move_usage.values()]
    unused_moves = [0 for x in xrange(int(total_moves - len(move_usage)))]
    ideal_usages = ((sum([abs(ideal - value)/2. for value in used_moves + unused_moves])))
    #print (sum([abs(ideal - value)/2. for value in used_moves + unused_moves]))
    #print ideal_usages
    ideal_turns = abs(IDEAL_TURNS - turns)*10
    ideal_life = ((battle_state.health_1 + battle_state.health_2)/20.) ** 2
    if IDEAL_TURNS -5 < turns < IDEAL_TURNS + 5:
        def ideal_life_decay(turn, total):
            maximum = (life_record[0] - 0)
            return maximum - maximum * turn/float(total)
        ideal_life_change = (sum([abs(r - ideal_life_decay(i, turns)) for i,r in enumerate(life_record)])) / 10.
    else:
        ideal_life_change = 100
    #print ideal_life
    #print ideal_life_change
    #print "*" * 5
    #print -ideal_turns - ideal_usages - ideal_life - ideal_life_change, -ideal_usages, -ideal_turns, -ideal_life, - ideal_life_change
    #print -ideal_life_change, - ideal_life
    battle_id+= 1
    return - ideal_life_change - ideal_life- ideal_usages, battle_id#-ideal_turns - ideal_usages - ideal_life - ideal_life_change

def random_subset(list):
    """
    Return a subset of length 1-3 of the list.
    """
    return random.sample(list, random.randint(1, 3))#len(list)))

feature_occurrences = {"health_1" : 1, "attack_1" : 3, 
                       "defense_1" : 3, "health_2" : 4, 
                       "attack_2" : 3, "defense_2" : 3}
def add_feature_if_new(feature, current):
    if feature not in current:
        return [feature] * feature_occurrences[feature]
    else:
        return []
    
class Move(dict):
    all_features = ["health_1", "attack_1", "defense_1", "health_2", "attack_2", "defense_2"]
    short_name = {"health_1" : "H", "attack_1": "A", "defense_1": "D",
                  "health_2" : "h", "attack_2": "a", "defense_2": "d"}
    def fill_randomly(self):
        #for feature in random_subset(self.all_features):
        #    self[feature] = FunctionTree(AttributeNode(feature))
        #    for x in xrange(100): # RADIATION
        #        self[feature] = self[feature].mutate()
        #return self
        # Alternate method where damaging attacks are much more likely
        features = []
        # random.choice((1, 1, 1, 1, 2, 2))
        for x in xrange(1):
            possibilities = []
            for feature in self.all_features:
                possibilities.extend(add_feature_if_new(feature, features))
            features.append(random.choice(possibilities))
        for feature in features:
            self[feature] = FunctionTree(AttributeNode(feature, lock=True))
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
        if random.randint(0, 3) == 1:
            return Move().fill_randomly()
        else:
            new_move = Move()
            for k, v in self.iteritems():
                new_move[k] = v.mutate()
            return new_move
        #if len(self) > 1 and random.randint(0, 1) == 1:
        #    del new_move[random.choice(self.keys())]
        #if len(self) < 2 and random.randint(0, 1) == 1:
        #    feature = random.choice(list(set(self.all_features) - set(self.iterkeys())))
        #    self[feature] = FunctionTree(AttributeNode(feature, lock=True))
        #    for x in xrange(100): # RADIATION
        #        new_move[feature] = self[feature].mutate()
        #return new_move
        
    def cross_over(self, other):
        new_move = self.copy()
        for feature in self.all_features:
            if feature in self and feature in other:
                new_move[feature] = self[feature].cross_over(other[feature])
            #elif feature in self:
            #    if random.choice((True, False)) and len(new_move) > 1:
            #        del new_move[feature]
            #elif feature in other:
            #    if random.choice((True, False)) and len(self) < 2:
            #        new_move[feature] = other[feature].copy()
        return new_move
        
    def apply(self, state):
        new_battle_state = BattleState(other = state)
        for feature, function in self.iteritems():
            setattr(new_battle_state, feature, function.value(state))
        new_battle_state.flip()
        return new_battle_state
        
    def __str__(self):
        return "{%s}" % (", ".join("%s <= %s" % (k, v) for k,v in self.iteritems()),)
    
    def short_str(self):
        return "{%s}" % (", ".join("%s <= %s" % (self.short_name[k], v.short_str()) for k,v in self.iteritems()),)
    
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
    def short_str(self):
        return "[%s]" % (", ".join([move.short_str() for move in self.moves]),)
    def __hash__(self):
        return hash(self.short_str())
        
        
genetic_log = open('genetic.log', 'w')
genetic_log.write("There's gonna be an Evolution!\n")
genetic_log.close()
genetic_log = open('genetic.log', 'a')
def genetic(problem, population_size = 100, 
                     iterations_limit = 2,
                     retain_parents = .25,
                     mutation_rate = .4,
                     radiation_amount = 10):
    population = [problem.generate_random_state() for x in xrange(population_size)]
       
    from function_operators import multiply, subtract, fmod, div, double, decrement
    from function_tree import FunctionTree, BinaryNode, UnaryNode, AttributeNode
    a, b, c = Move(), Move(), Move()
    a["health_1"] = FunctionTree(BinaryNode(BinaryNode(AttributeNode("health_1", lock=True),
                                                       AttributeNode("health_2"), subtract),
                                            BinaryNode(AttributeNode("attack_1"),
                                                       AttributeNode("attack_2"), fmod), multiply))
    b["attack_1"] = FunctionTree(UnaryNode(BinaryNode(AttributeNode("attack_1", lock=True),
                                                                   AttributeNode("defense_2"), div), double))
    c["health_1"] = FunctionTree(UnaryNode(AttributeNode("health_1", lock=True), decrement))
    population[0].moves = [a, b, c]
    
    genetic_log.write("Initial\n")
    for dna in population:
        genetic_log.write("\t" + dna.short_str() + "\n")
    for iteration in xrange(iterations_limit):
        genetic_log.write(str(1+iteration)+ "\n")
        parents_retained = int(round(retain_parents * population_size))
        mutants_generated = int(round(mutation_rate * population_size))
        children_generated = population_size - parents_retained - mutants_generated
        dna_values = sorted([(problem.value(dna), dna) for dna in population], key=lambda x: -x[0][0])
        for (value, battle_id), dna in dna_values:
            genetic_log.write("\t" + str(value) + "("+ str(battle_id)+"): " +dna.short_str() + "\n")
        population = OrderedSet()
        for dna_value in dna_values[:parents_retained]:
            population.add(dna_value[1])
        for survivor in zip(xrange(mutants_generated), cycle(population)):
            force_add = True
            while force_add:
                mutant = survivor[1]
                for r in xrange(radiation_amount):
                    mutant = problem.mutate(mutant)
                force_add = not population.add(mutant)
        for couple in xrange(children_generated):
            force_add = True
            while force_add:
                dad, mom = random.sample(population, 2)
                child = problem.crossover(dad, mom).mutate()
                force_add = not population.add(child)
        print "Iteration", str(iteration+1)
        
    dna_values = sorted([(problem.value(dna), dna) for dna in population], key=lambda x: -x[0][0])
    return dna_values[0][1]
        
class FunProblem(SearchProblem):
    def __init__(self, player1 = None, player2 = None):
        SearchProblem.__init__(self, MoveList())
        if player1 is None:
            player1 = random.choice(PLAYERS)
        if player2 is None:
            player2 = random.choice(PLAYERS)
        self.player1 = player1
        self.player2 = player2
        
    def generate_random_state(self):
        return MoveList()
        
    def crossover(self, state1, state2):
        return state1.cross_over(state2)
        
    def mutate(self, state):
        return state.mutate()
        
    def value(self, state):
        return battle_simulation(state, self.player1(state), self.player2(state))
        
    def pprint(self, state):
        return "\n".join(["Move %d:\n\t%s" % (i, "\n\t".join([k+": "+str(v) for k, v in s.iteritems()])) for i, s in enumerate(state)])
        
if __name__ == "__main__":
    for x in xrange(1):
        n = genetic(FunProblem()) #, population_size=5, iterations_limit=1, mutation_chance = .1)
        for i, move in enumerate(n.moves):
            print "Move", 1+i
            for k, v in move.iteritems():
                print "\t",k, "=", v
                #print "\t\t", getattr(b, k), "=>", v.value(b)
        #print "Attempt", x, "was", n.state
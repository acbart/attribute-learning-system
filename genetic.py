import random
from random import choice
random.seed(42)

from collections import Counter

from function_tree import FunctionTree, AttributeNode
from players import PLAYERS

from simpleai.search.local import genetic
from simpleai.search import SearchProblem

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
def battle_simulation(moves, player_1, player_2):
    """
    Performs a battle simulation, where player1 and player2 take turns using
    moves until someone dies.
    """
    battle_state = BattleState(player_1, player_2)
    p1, p2 = player_1.__name__, player_2.__name__
    battle_log.write("New battle between %s and %s!\n" % (p1, p2))
    turns = 0
    battle_log.write("Initial: %s" % (str(battle_state),))
    move_usage= Counter()
    while battle_state.players_alive() and turns < 15:
        battle_log.write("\tTurn %d\n" % (turns+1,))
        battle_state, move1 = player_1.move(battle_state)
        battle_log.write("\t\tPlayer 1's move: %s\n" % (str(move1),))
        #battle_log.write("\t\t\t%s\n" % (str(battle_state),))
        battle_state, move2 = player_2.move(battle_state)
        battle_log.write("\t\tPlayer 2's move: %s\n" % (str(move2),))
        battle_log.write("\t\t\t%s\n" % (str(battle_state),))
        move_usage[id(move1)]+= 1
        move_usage[id(move2)]+= 1
        turns += 1
    if battle_state.health_1 <= 0 and battle_state.health_2 <= 0:
        battle_log.write("It was a tie after %d rounds!\n" % (turns,))
    elif battle_state.health_1 <= 0:
        battle_log.write("Player 2 (%s) won in %d rounds!\n" % (p2, turns))
    elif battle_state.health_2 <= 0:
        battle_log.write("Player 1 (%s) won in %d rounds!\n" % (p1, turns))
    else:
        battle_log.write("No one won. That battle sucked!\n")
    total_moves = float(len(moves.moves))
    ideal = 100. / total_moves
    values = [100. * v/(turns*2.) for v in move_usage.values()]
    values += [0 for x in xrange(int(total_moves - len(move_usage)))]
    ideal_usages = sum([abs(ideal - value) for value in values])
    ideal_turns = abs(10 - turns)*10
    ideal_life = battle_state.health_1 + battle_state.health_2
    return -ideal_turns - ideal_usages - ideal_life

def random_subset(list):
    return random.sample(list, random.randint(1, 3))#len(list)))

feature_occurrences = {"health_1" : 1, "attack_1" : 2, 
                       "defense_1" : 2, "health_2" : 8, 
                       "attack_2" : 2, "defense_2" : 2}
def add_feature_if_new(feature, current):
    if feature not in current:
        return [feature] * feature_occurrences[feature]
    else:
        return []
    
class Move(dict):
    all_features = ["health_1", "attack_1", "defense_1", "health_2", "attack_2", "defense_2"]
    
    def fill_randomly(self):
        #for feature in random_subset(self.all_features):
        #    self[feature] = FunctionTree(AttributeNode(feature))
        #    for x in xrange(100): # RADIATION
        #        self[feature] = self[feature].mutate()
        #return self
        # Alternate method where damaging attacks are much more likely
        features = []
        for x in xrange(random.choice((1, 1, 1, 1, 2, 2, 3))):
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
        
    def apply(self, state):
        new_battle_state = BattleState(other = state)
        for feature, function in self.iteritems():
            setattr(new_battle_state, feature, function.value(state))
        new_battle_state.flip()
        return new_battle_state
        
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
        
for x in xrange(1):
    n = genetic(FunProblem(), population_size=5, iterations_limit=1, mutation_chance = .1)
    for i, move in enumerate(n.state.moves):
        print "Move", 1+i
        for k, v in move.iteritems():
            print "\t",k, "=", v
            #print "\t\t", getattr(b, k), "=>", v.value(b)
    #print "Attempt", x, "was", n.state
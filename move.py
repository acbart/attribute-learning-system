import random
from battle_state import BattleState
from function_tree import FunctionTree
from function_vector import FunctionVector
from function_operators import get_feature_operator
from config import NUMBER_OF_FEATURES_PER_MOVE, RADIATION_STRENGTH, MOVE_FEATURE_CHANGE_RATE

def random_weighted_subset(weights, max_length):
    features = []
    for x in xrange(random.randint(1, max_length)):
        possibilities = []
        for feature, occurrences in weights.items():
            if feature not in features:
                possibilities += [feature] * occurrences
        features.append(random.choice(possibilities))
    return features

class Move(list):
    feature_occurrences = {"self_health" : 1, "self_attack" : 3, 
                           "self_defense" : 3, "other_health" : 4, 
                           "other_attack" : 3, "other_defense" : 3}
    
    @classmethod
    def generate_random_move(cls):
        new_move = Move()
        
        # Choose a set of features for this move to modify
        features = random_weighted_subset(Move.feature_occurrences, NUMBER_OF_FEATURES_PER_MOVE)
        
        # For each feature, create it's function
        for feature in features:
            new_move.append(FunctionVector())
        
        return new_move
        
    def copy(self):
        new_move = Move()
        for function in self:
            new_move.append(function.copy())
        return new_move
    
    def mutate(self):
        new_move = Move()
        for function in self:
            new_move.append(function.mutate())
        return new_move
        
    def cross_over(self, other):
        new_move = Move()
        for self_f, other_f in zip(self, other):
            new_move.append(self_f.cross_over(other_f))
        return new_move
        
    def apply(self, state):
        new_battle_state = BattleState(state)
        new_battle_state.apply(self)
        return new_battle_state
    
    def evaluate(self, state):
        # Realistically, this shouldn't happen the way it does; it should return a vector of numbers.
        return sum(function_tree.evaluate(state) for function_tree in self)
        
    def __str__(self):
        return "{%s}" % (", ".join("%s <= %s" % (ft.feature, str(ft)) for ft in self),)
    
    def short_string(self):
        return "{%s}" % (", ".join("%s <= %s" % (ft.feature, ft.short_string()) for ft in self),)

    def _label(self):
        return ""
    
    label = property(_label)
    
    def _children(self):
        return self
    
    children = property(_children)
import random
from battle_state import BattleState
from function_tree import FunctionTree
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

class Move(dict):
    feature_occurrences = {"self_health" : 1, "self_attack" : 3, 
                           "self_defense" : 3, "other_health" : 4, 
                           "other_attack" : 3, "other_defense" : 3}
    short_name = {"self_health" : "H", "self_attack": "A", "self_defense": "D",
                  "other_health" : "h", "other_attack": "a", "other_defense": "d"}
    
    @classmethod
    def generate_random_move(cls):
        new_move = Move()
        
        # Choose a set of features for this move to modify
        features = random_weighted_subset(Move.feature_occurrences, NUMBER_OF_FEATURES_PER_MOVE)
        
        # For each feature, create it's function
        for feature in features:
            new_move[feature] = FunctionTree(feature=feature)
            
            #Mutate the function a little
            for x in xrange(RADIATION_STRENGTH):
                new_move[feature] = new_move[feature].mutate()
        
        return new_move
        
    def copy(self):
        new_move = Move()
        for feature, function in self.iteritems():
            new_move[feature] = function.copy()
        return new_move
    
    def mutate(self):
        # With some probability, completely change this Move
        if random.randint(1, MOVE_FEATURE_CHANGE_RATE) == 1:
            return Move.generate_random_move()
        # Otherwise, just mutate it's function trees a little
        else:
            new_move = Move()
            for feature, function in self.iteritems():
                new_move[feature] = function.mutate()
            return new_move
        
    def cross_over(self, other):
        common_features = set(self.keys()) & set(other.keys())
        # If they have features in common, merge them
        if common_features:
            child_move = Move()
            # Merge each feature individually
            for feature in common_features:
                self_function, other_function = self[feature], other[feature]
                child_move[feature] = self_function.cross_over(other_function)
            return child_move
        # Otherwise, just pick one to copy, slightly mutated
        else:
            if random.choice((True, False)):
                return self.mutate()
            else:
                return other.mutate()
        
    def apply(self, state):
        new_battle_state = BattleState(state)
        new_battle_state.apply(self)
        return new_battle_state
        
    def __str__(self):
        return "{%s}" % (", ".join("%s <= %s" % (k, v) for k,v in self.iteritems()),)
    
    def short_string(self):
        return "{%s}" % (", ".join("%s <= %s" % (self.short_name[k], v.short_string()) for k,v in self.iteritems()),)

import random
from node import Node
from config import FEATURE_VECTOR_RANGE
from function_operators import clamp, NULLARY_OPERATORS, get_feature_operator

class FunctionVector:
    
    feature_choices = [op.formatted_name for op in NULLARY_OPERATORS]
    feature_affects = {"self_attack" : ("other_attack", "self_defense"),
                       "self_health" : ("other_attack", "self_defense"),
                       "self_defense": ("other_attack", "other_health"),
                       "other_attack" : ("self_attack", "other_defense"),
                       "other_health" : ("self_attack", "other_defense"),
                       "other_defense": ("self_attack", "self_health"),
    
    def __init__(self, source= None):
        # If not given a node, create a new random tree
        if source is None:
            self.output_feature = random.choice(self.feature_affects.keys())
            affects = self.feature_affects[self.output_feature]
            self.input_features = random.sample(affects, random.randint(*FEATURE_VECTOR_RANGE))
            self.coeffecients = [random.randint(*FEATURE_COEFFECIENTS_DOMAIN)
                                        for x in self.input_features + [1]]
        else:
            self.output_feature = source.output_feature
            self.input_features = source.input_features[:]
            self.coeffecients = source.coeffecients[:]
    
    def copy(self):
        """
        copy(self): return a new FunctionTree based on the old one. Nothing changes.
        """
        return FunctionVector(self)
    
    def mutate(self):
        """
        mutate(self): return a new FunctionTree, based on the old one, with only one
                  change, e.g. a different terminal node, or changing a binary
                  node into a unary node.
        """
        new_function = FunctionVector(self)
        mutant_index = random.randint(0, len(new_function.coeffecients)-1)
        new_function.coeffecients[mutant_index] += random.randint(-10, 10)
        return new_function
    
    def cross_over(self, other):
        new_function = FunctionVector(self)
        for self_coeffecient, other_coeffecient in zip(self.coeffecients, other.coeffecients):
            sum(self_coeffecient, other_coeffecient) / 2.
        return FunctionTree(new_root)
    
    def evaluate(self, state):
        """
        state (BattleState)
        
        return an integer by plugging in the values from the state into this 
        function.
        """
        return None
    
    def __len__(self):
        return len(self.coeffecients)
    
    def __str__(self):
        return str(self.coeffecients)
    
    def short_string(self):
        return self.coeffecients
        
import random
from node import Node
from config import FEATURE_VECTOR_RANGE, FEATURE_MUTATION_FLUCTATION_RANGE, FEATURE_COEFFECIENTS_DOMAIN, ATTRIBUTE_AFFECTS
from function_operators import clamp, NULLARY_OPERATORS, get_feature_operator
from auxiliary import abbreviate

class FunctionVector(object):
    
    def __init__(self, source= None):
        # If not given a node, create a new random tree
        if source is None:
            self.feature = random.choice(ATTRIBUTE_AFFECTS.keys())
            affects = ATTRIBUTE_AFFECTS[self.feature]
            self.coeffecients = {}
            for input_feature in random.sample(affects, random.randint(*FEATURE_VECTOR_RANGE)):
                self.coeffecients[input_feature] = random.randint(*FEATURE_COEFFECIENTS_DOMAIN)
            self.constant = random.randint(*FEATURE_COEFFECIENTS_DOMAIN)
        else:
            self.feature = source.feature
            self.coeffecients = dict(source.coeffecients)
            self.constant = source.constant
    
    def copy(self):
        """
        copy(self): return a new FunctionTree based on the old one. Nothing changes.
        """
        return FunctionVector(self)
    
    def mutate(self):
        new_function = FunctionVector(self)
        if random.randint(0, 3) == 0:
            new_function.constant += random.randint(*FEATURE_MUTATION_FLUCTATION_RANGE)
        else:
            mutant_feature = random.choice(new_function.coeffecients.keys())
            new_function.coeffecients[mutant_feature] += random.randint(-10, 10)
        return new_function
    
    def cross_over(self, other):
        if self.feature != other.feature:
            return (random.choice((self, other))).copy()
        else:
            new_function = FunctionVector(self)
            for input_feature, coeffecient in other.coeffecients.iteritems():
                if input_feature in new_function.coeffecients:
                    new_function.coeffecients[input_feature] += coeffecient
                    new_function.coeffecients[input_feature] /= 2.
                else:
                    new_function.coeffecients[input_feature] = coeffecient
            new_function.constant = (new_function.constant + other.constant) /2.
            return new_function
    
    def evaluate(self, state):
        """
        state (BattleState)
        
        return an integer by plugging in the values from the state into this 
        function.
        """
        result = state.get_value(self.feature)
        for input_feature, coeffecient in self.coeffecients.iteritems():
            result += state.get_value(input_feature) * coeffecient
        result += self.constant
        return clamp(result)
    
    def __len__(self):
        return len(self.coeffecients)
    
    def __str__(self):
        return str(self.coeffecients) + " + " + str(self.constant)
    
    def short_string(self):
        return "(" + abbreviate(self.feature) + "=" + "{:.2f}".format(self.constant) + "".join([("%+.1f*%s" % (value, abbreviate(key))) for key, value in self.coeffecients.iteritems()]) + ")"
        
    def __hash__(self):
        return hash(self.short_string())
        
import random
from node import Node
from config import HEIGHT_MAX, BOOLEANS
from function_operators import clamp, NULLARY_OPERATORS, get_feature_operator

class FunctionTree(object):
    """    
    A FunctionTree has:
        A root (a Node)
    """
    
    feature_choices = [op.formatted_name for op in NULLARY_OPERATORS]
    
    def __init__(self, root=None):
        # If not given a node, create a new random tree
        if root is None:
            root = Node.random_tree()#random_tree()
        self.root = root
        self.feature = self.choose_random_attribute_leaf()
        if self.feature is None:
            self.feature = random.choice(self.feature_choices)
        else:
            self.feature = self.feature.operator.formatted_name
        
    def choose_random_attribute_leaf(self):
        return self.root.choose_random_attribute_leaf()
    
    def copy(self):
        """
        copy(self): return a new FunctionTree based on the old one. Nothing changes.
        """
        new_root = self.root.copy()
        return FunctionTree(new_root)
    
    def mutate(self):
        """
        mutate(self): return a new FunctionTree, based on the old one, with only one
                  change, e.g. a different terminal node, or changing a binary
                  node into a unary node.
        """
        #mutant_node_index = random.randrange(len(self.root))
        leaf_node_indexes, length_traversed = self.root.find_leave_indexes()
        mutant_node_index = random.choice(leaf_node_indexes)
        new_root, length_traversed = self.root.mutate_index(0, mutant_node_index, HEIGHT_MAX)
        return FunctionTree(new_root)
    
    def cross_over(self, other):
        """
        other (FunctionTree)
        
        cross_over(self, other): merge two trees by walking through them
                             simultaneously and randomly choosing either the
                             first or the second's nodes. Creates a new tree.
         
        The behavior of crossing over two nodes with different locked attribute 
        types is undefined.
        """
        new_root = self.root.cross_over(other.root)
        return FunctionTree(new_root)
    
    def evaluate(self, state):
        """
        state (BattleState)
        
        return an integer by plugging in the values from the state into this 
        function.
        """
        return clamp(self.root.evaluate(state))
    
    def __len__(self):
        return len(self.root)
    
    def __str__(self):
        return str(self.root)
    
    def short_string(self):
        return self.root.short_string()
        
    def _label(self):
        return ""
    
    label = property(_label)
    
    def _children(self):
        return [self.root]
    
    children = property(_children)
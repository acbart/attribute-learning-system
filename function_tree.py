import random
from node import Node
from config import HEIGHT_MAX, BOOLEANS
from function_operators import clamp, NULLARY_OPERATORS, get_feature_operator

class FunctionTree(object):
    """    
    A FunctionTree has:
        A root (a Node)
    """
    
    def __init__(self, root=None, feature = None):
        # If not given a node, create a new random tree
        if root is None and feature is None:
            root = Node.random_tree()#random_tree()
        # If given a feature (string), create a simple f(x)=x fucntion
        if feature is not None:
            root = Node(operator = get_feature_operator[feature],
                           lock = True) #AttributeNode(feature, lock=True)
        self.root = root
    
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
        p = self.root.get_protected().operator
        mutant_node_index = random.randrange(len(self.root))
        new_root, length_traversed = self.root.mutate_index(0, mutant_node_index, HEIGHT_MAX)
        #print self, new_root
        assert new_root.count_protected() == 1
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
        new_root = self.root.cross_over(other.root, keeping=random.choice(("self", "other")))
        assert new_root.count_protected() == 1
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
        
import random
from node import Node
from config import HEIGHT_MAX, BOOLEANS
from function_operators import clamp, NULLARY_OPERATORS, get_feature_operator

class SFunctionTree(object):
    """
    A FunctionTree has:
        A root (a Node)
    """

    def __init__(self, root=None, mod_features=None, specific_binary_operator=None, changed_feature=None):
        # If not given a node or features, throw error
        if root is None and (mod_features is None or changed_feature is None):
            raise Exception("FunctionTree needs a node, or features list and changed feature specified")

        # If given features (list), create a simple f(x)=x function
        if mod_features is not None:

            children_feature_nodes = []
            for feature in mod_features:
                children_feature_nodes.append(SNode(operator=get_feature_operator[feature]))

            if specific_binary_operator is not None:
                root = SNode(operator=specific_binary_operator, children=children_feature_nodes)
            else:
                root = SNode(arity=2, children=children_feature_nodes)

        if changed_feature is not None:
            self.changed_feature = changed_feature

        self.root = root

    def copy(self):
        """
        copy(self): return a new FunctionTree based on the old one. Nothing changes.
        """
        new_root = self.root.copy()
        return SFunctionTree(new_root)

    def mutate(self):
        """
        mutate(self): return a new FunctionTree, based on the old one, with only one
                  change, e.g. a different terminal node, or changing a binary
                  node into a unary node.
        """
        mutant_node_index = random.randrange(len(self.root))
        new_root, length_traversed = self.root.mutate_index(0, mutant_node_index, HEIGHT_MAX)
        print "After Mutate: " + self + " new root: " + new_root
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

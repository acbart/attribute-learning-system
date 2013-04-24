import random
from config import RANDOM_VARIABLES, BOOLEANS, HEIGHT_MAX
from function_operators import BINARY_OPERATORS, UNARY_OPERATORS, NULLARY_OPERATORS, CONSTANT_OPERATORS
        
class Node(object):
    """
    A Node is basically an operator and its arguments. If a node has a nullary
    operator (i.e. has no arguments), then it's an attribute (e.g. other_health).
    
    Important properties:
        operator (function): check out function_operators.py for examples
        children (listof Node): an immutable list of the arguments of this node
        lock (Boolean): whether this particular node is a nullary operator that MUST be kept during mutations.
    """
    
    operators_from_arity = {0 : NULLARY_OPERATORS,
                            1 : UNARY_OPERATORS,
                            2 : BINARY_OPERATORS}
                            
    def __init__(self, operator = None, arity=None, children = None):
        """
        If an operator is NOT specified, then a random operator will be chosen. If
            an arity IS specified, an operator of the that arity will be randomly
            chosen.
            
        If no children are specified, then new random nullary nodes will be created
            as children.
        """
        if operator is None:
            if arity is None:
                operator = random.choice(NULLARY_OPERATORS + 
                                         UNARY_OPERATORS + 
                                         BINARY_OPERATORS + random.sample(CONSTANT_OPERATORS, 3))
            else:
                if not random.randint(0, 5) and not arity:
                    operator = random.choice(CONSTANT_OPERATORS)
                else:
                    operator = random.choice(Node.operators_from_arity[arity])
        self.operator = operator
        if children is None:
            children = []
            for child in xrange(operator.arity):
                children.append(Node(arity=0))
        self.children = children

    @staticmethod
    def random_tree(height_left=HEIGHT_MAX):
        """
        Utility function for creating random trees of a maximal height.
        
        Only used in tests, not by the genetic algorithm.
        """
        if height_left == 0:
            return Node(arity=0)
        arity = random.randint(0, 2)
        children = [Node.random_tree(height_left-1) for child in xrange(arity)]
        new_tree = Node(arity=arity, children=children)
        return new_tree
        
    def choose_random_attribute_leaf(self):
        def get_attribute_leaves(node):
            """
            Get a specific leaf, which is *index* away from this *node*.
            """
            if node.children:
                result = list()
                for child in node.children:
                    result += get_attribute_leaves(child)
                return result
            else:
                return [node] if node.operator.is_attribute else []
        attribute_leaves = get_attribute_leaves(self)
        if attribute_leaves:
            return random.choice(attribute_leaves)
        else:
            return None
    
    def copy(self):
        """
        Returns a complete copy of this node and its children.
        
        If lock is True, then also copy any lock status in the nullary nodes. 
            Otherwise, turn off any locking encountered.
        """
        children_copies = [child.copy() for child in self.children]
        return Node(operator = self.operator, 
                    children = children_copies)
    
    def evaluate(self, state):
        """
        Given the values specified in the *state* (a BattleState), perform the
        operation of this node on its children.
        """
        arguments = [child.evaluate(state) for child in self.children]
        return self.operator(state, *arguments)
        
    def __len__(self):
        """
        Count how many subnodes are in this node.
        """
        return 1 + sum(len(child) for child in self.children)
        
    def count_leaves(self):
        """
        Count how many terminal nodes (leaves, or in this case, nodes that have
        a nullary operator) are in this node.
        """
        if self.children:
            return sum(child.count_leaves() for child in self.children)
        else:
            return 1
            
    def count_attribute_leaves(self):
        """
        Count how many terminal nodes (leaves, or in this case, nodes that have
        a nullary operator) are in this node.
        """
        if self.children:
            return sum(child.count_attribute_leaves() for child in self.children)
        else:
            return 1 if self.operator.is_attribute else 0
    
    def __str__(self):
        """
        Return a long string represention of this node, with full names and
        operators.
        """
        return self.operator.formatted_name % tuple([str(child) for child in self.children])
    
    def short_string(self):
        """
        Return a concise string representation of this node. Any locked nodes
        will be surronded with sigils ($).
        """
        this = self.operator.short_name
        children = ",".join([child.short_string() for child in self.children])
        return this + "("+children+")"
    
    def _label(self):
        return self.operator.short_name
    
    label = property(_label)
            
    def mutate(self, height_left):
        """
        Return a mutated version of this node.
        """
        
        # If we're out of room, just return a Nullary node
        if height_left == 0:
            return Node(arity = 0)
        
        # 50% chance of promoting a child to replace this node. (50% is arbitrarly chosen)
        if self.operator.arity > 0 and random.choice((True, False)):
            promoted_child = random.choice(self.children)
            return promoted_child.copy()
        else:
            # Otherwise, just choose a completely new type of node to change this to.
            new_arity = random.randint(0, 2)
            children_copies = [child.copy() for child in self.children]
            # Add nodes until we reach proper arity
            while len(children_copies) < new_arity:
                children_copies.append(Node(arity=0))
            # Remove nodes until we reach proper arity, ensuring that we never kill a protected node.
            while len(children_copies) > new_arity:
                node_to_kill = random.choice(children_copies)
                children_copies.remove(node_to_kill)
            return Node(arity = new_arity, children = children_copies)
            
    def mutate_index(self, current_index, mutant_index, height_left):
        """
        Find a specific node and mutate it.
        """
        # If we've found the mutant, return a mutated version of it!
        if current_index == mutant_index:
            return self.mutate(height_left), len(self)
        else:
            # Otherwise, continue recursively searching for it.
            nodes_traversed = 1
            new_children = []
            for child in self.children:
                new_child, new_nodes_traversed = child.mutate_index(current_index+nodes_traversed,
                                                                    mutant_index,
                                                                    height_left-1)
                new_children.append(new_child)
                nodes_traversed += new_nodes_traversed
            return Node(operator = self.operator, children = new_children), nodes_traversed
            
    def cross_over(self, other):
        """
        The following Description is from:
        http://ieeexplore.ieee.org.ezproxy.lib.vt.edu:8080/stamp/stamp.jsp?tp=&arnumber=6256587
        
        "According to [12], the GP uniform crossover process starts 
        at the tree's root node and works its way down each tree along 
        some path until finding function nodes of differing arity at the 
        similar location. Furthermore it can swap every node up to this 
        point with its counterpart in the other tree without altering the 
        structure of either. Any node in one tree having a 
        corresponding node at the same location in the other is said to 
        be located within the common region. Those pairs of nodes 
        within the common region that have the same arity are referred 
        to as interior. The common region necessarily includes all 
        interior nodes. Once the interior nodes have been identified, the 
        parent trees are copied. Interior nodes are selected for crossover 
        with some probability which is generally set to 0.5. Crossover 
        involves exchanging the selected nodes between the trees, 
        while those nodes not selected for crossover remain unaffected. 
        Non-interior nodes within the common region can also be 
        crossed, but in this case the nodes and their subtrees are 
        swapped."
        
        [12] Poli R., Langdon W.B. On the search properties of different crossover 
        operators in genetic programming. In J. R. Koza, et al., editors, Genetic 
        Programming 1998:Proceedings of the Third Annual Conference, pages 
        293-301, University of Wisconsin, Madison, Wisconsin, USA, 22-25 
        July 1998.
        """
        
        # Are we in an interior node?
        if self.operator.arity == other.operator.arity and self.operator.arity:
            new_operator = random.choice((self.operator, other.operator))
            new_children = []
            for self_child, other_child in zip(self.children, other.children):
                new_child = self_child.cross_over(other_child)
                new_children.append(new_child)
            return Node(operator=new_operator, children=new_children)
        # Then just choose a subtree and use it
        else:
            return (random.choice((self, other))).copy()
        
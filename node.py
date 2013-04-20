import random
from config import RANDOM_VARIABLES, BOOLEANS, HEIGHT_MAX
from function_operators import BINARY_OPERATORS, UNARY_OPERATORS, NULLARY_OPERATORS

import itertools
        
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
                            
    def __init__(self, operator = None, arity=None, children = None, lock=False):
        """
        If an operator is NOT specified, then a random operator will be chosen. If
            an arity IS specified, an operator of the that arity will be randomly
            chosen.
            
        If no children are specified, then new random nullary nodes will be created
            as children.
        """
        self.lock = lock
        if operator is None:
            if arity is None:
                operator = random.choice(NULLARY_OPERATORS + 
                                         UNARY_OPERATORS + 
                                         BINARY_OPERATORS)
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
        
    def lock_random(self):
        """
        Lock a random nullary node of this tree.
        
        Only used in tests, not by the genetic algorithms.
        """
        def get_leaf(node, index, current_index = 0):
            if node.children:
                leaves_visited = 0
                for child in node.children:
                    result = get_leaf(child, index, current_index+leaves_visited)
                    if isinstance(result, Node):
                        return result
                    leaves_visited += result
                return leaves_visited
            elif index == current_index:
                return node
            else:
                return 1
        leaf = random.randint(0, self.count_leaves()-1)
        get_leaf(self, leaf).lock = True
    
    def copy(self, lock=True):
        """
        Returns a complete copy of this node and its children.
        
        If lock is True, then also copy any lock status in the nullary nodes. 
            Otherwise, turn off any locking encountered.
        """
        children_copies = [child.copy(lock) for child in self.children]
        return Node(operator = self.operator, 
                       children = children_copies,
                       lock = self.lock if lock else False)
    
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
        this = ("$%s$" if self.lock else "%s") % (self.operator.short_name,)
        children = ",".join([child.short_string() for child in self.children])
        return this + "("+children+")"
    
    def is_protected(self):
        """
        Return whether this node or any of its children is locked.
        """
        return self.lock or any(child.is_protected() for child in self.children)
        
    def get_protected(self):
        """
        If this node or any of its children are locked, return that locked node.
        
        Otherwise return None.
        """
        if self.lock: 
            return self
        for child in self.children:
            possible_protected = child.get_protected()
            if possible_protected is not None:
                return possible_protected
        return None
        
    def count_protected(self):
        """
        Count how many subnodes in this node are locked.
        """
        if self.lock:
            return 1
        else:
            return sum(child.count_protected() for child in self.children)
            
    def mutate(self, height_left):
        """
        Return a mutated version of this node.
        """
        
        # If we're out of room, just return a Nullary node
        if height_left == 0:
            if self.lock:
                # Keep the attribute if it's locked
                return Node(operator = self.operator, lock = self.lock)
            else:
                return Node(arity = 0, lock = self.lock)
        
        # If it's a locked attribute, make sure you keep it.
        if self.lock:
            new_arity = random.randint(0, 2)
            if new_arity == 0:
                # Copy it wholesale
                return self.copy()
            else:
                # Make it a child of a new parent
                new_children = [self.copy()] + [Node(arity=0) for x in xrange(new_arity-1)]
                random.shuffle(new_children)
                new_node = Node(arity=new_arity, children= new_children)
                return new_node
        
        # 50% chance of promoting a child to replace this node. (50% is arbitrarly chosen)
        if self.operator.arity > 0 and random.choice((True, False)):
            # If one of the children is locked, we must keep it!
            promoted_child = self.get_protected()
            if promoted_child is None:
                promoted_child = random.choice(self.children)
            return promoted_child.copy()
        else:
            # Otherwise, just choose a completely new type of node to change this to.
            if self.is_protected():
                new_arity = random.randint(1, 2)            
            else:
                new_arity = random.randint(0, 2)
            children_copies = [child.copy() for child in self.children]
            # Add nodes until we reach proper arity
            while len(children_copies) < new_arity:
                children_copies.append(Node(arity=0))
            # Remove nodes until we reach proper arity, ensuring that we never kill a protected node.
            while len(children_copies) > new_arity:
                node_to_kill = random.choice(children_copies)
                if node_to_kill.is_protected():
                    # Very dangerous, but I'm pretty sure we should never get stuck in an infinite loop...
                    continue
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
            return Node(operator = self.operator, children = new_children, lock = self.lock), nodes_traversed
            
    def cross_over(self, other, keeping):
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
                new_child = self_child.cross_over(other_child, keeping)
                new_children.append(new_child)
            return Node(operator=new_operator, children=new_children)
        # Are we dealing with a protected boundary node?
        elif self.is_protected() and keeping == "self":
            return self.copy()
        elif other.is_protected() and keeping == "other":
            return other.copy()
        # Then just choose a subtree and use it
        else:
            return (random.choice((self, other))).copy(False)
        
   
if __name__ == "__main__":
    random.seed(5)
    a = Node.random_tree()
    print "A", a, a.get_protected()
    a.lock_random()
    b = Node.random_tree()
    print "B", b
    b.lock_random()
    print "Cross-over: Notice how the first node of B is used with the rest of A's nodes!"
    print "A+B", a.cross_over(b, "self")
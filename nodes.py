import random
from config import RANDOM_VARIABLES, BOOLEANS, HEIGHT_MAX
from function_operators import BINARY_OPERATORS, UNARY_OPERATORS, NULLARY_OPERATORS

import itertools
        
class Node(object):
    operators_from_arity = {0 : NULLARY_OPERATORS,
                            1 : UNARY_OPERATORS,
                            2 : BINARY_OPERATORS}
    def __init__(self, operator = None, arity=None, children = None, lock=False):
        """
        children (list) must be ownable by this new Node, so don't rely on it.
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
        print "TEST"
        if height_left == 0:
            return Node(arity=0)
        arity = random.randint(0, 2)
        children = [random_tree(height_left-1) for child in xrange(arity)]
        new_tree = Node(arity=arity, children=children)
        return new_tree
    
    def copy(self):
        children_copies = [child.copy() for child in self.children]
        return Node(operator = self.operator, 
                       children = children_copies,
                       lock = self.lock)
    
    def evaluate(self, state):
        arguments = [child.evaluate(state) for child in self.children]
        return self.operator(state, *arguments)
        
    def __len__(self):
        return 1 + sum(len(child) for child in self.children)
    
    def __str__(self):
        return self.operator.formatted_name % tuple([str(child) for child in self.children])
    
    def short_string(self):
        return self.operator.short_name % [child.short_string() for child in self.children]
    
    def is_protected(self):
        return self.lock or any(child.is_protected() for child in self.children)
        
    def get_protected(self):
        if self.lock: return self
        for child in self.children:
            possible_protected = child.get_protected()
            if possible_protected is not None: return possible_protected
        return None
        
    def mutate(self, height_left):
        # If we're out of room, just return a Nullary node
        if height_left == 0:
            if self.lock:
                return Node(operator = self.operator, lock = self.lock)
            else:
                return Node(arity = 0, lock = self.lock)
        
        if self.lock:
            new_arity = random.randint(1, 2)
            new_children = [self.copy()] + [Node(arity=0) for x in xrange(new_arity-1)]
            random.shuffle(new_children)
            new_node = Node(arity=new_arity, children= new_children)
            return new_node
        
        if self.operator.arity > 0 and random.choice((True, False)):
            promoted_child = self.get_protected()
            if promoted_child is None:
                promoted_child = random.choice(self.children)
            return promoted_child.copy()
        else:
            if self.is_protected():
                new_arity = random.randint(1, 2)            
            else:
                new_arity = random.randint(0, 2)
            children_copies = [child.copy() for child in self.children]
            # Add nodes until we reach proper arity
            while len(children_copies) < new_arity:
                children_copies.append(Node(arity=0))
            # Remove nodes until we reach proper arity
            while len(children_copies) > new_arity:
                node_to_kill = random.choice(children_copies)
                if node_to_kill.is_protected():
                    continue
                children_copies.remove(node_to_kill)
            return Node(arity = new_arity, children = children_copies)
            
    def mutate_index(self, current_index, mutant_index, height_left):
        # If we've found the mutant, mutate it!
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
        # If one of the nodes is lock and we're keeping it, then keep it!
        if self.lock and keeping == "self":
            child_node = Node(operator = self.operator, lock = True)
            return child_node
        elif other.lock and keeping == "other":
            child_node = Node(operator = other.operator, lock = True)
            return child_node
        
        # We cannot use an operator if it would ensure that we kill a lock node
        if keeping == "self" and self.is_protected() and other.operator.arity == 0:
            new_operator = self.operator
        elif keeping == "other" and other.is_protected() and self.operator.arity == 0:
            new_operator = other.operator
        else:
            new_operator = random.choice((self.operator, other.operator))
        
        # Create a new list of children by crossing over the two lists of children.
        new_children = []
        # lock_status is used to keep track of whether a node's lock status must be kept
        lock_status = {}
        for self_child, other_child in itertools.izip_longest(self.children, other.children):
            if self_child is None:
                new_child = other_child.copy()
                lock_status[new_child] = keeping == "other" and other_child.is_protected()
            elif other_child is None:
                new_child = self_child.copy()
                lock_status[new_child] = keeping == "self" and self_child.is_protected()
            else:
                new_child = self_child.cross_over(other_child, keeping)
                if self_child.is_protected() and keeping == "self":
                    lock_status[new_child] = True
                elif other_child.is_protected() and keeping == "other":
                    lock_status[new_child] = True
                else:
                    lock_status[new_child] = False
            new_children.append(new_child)

        # We might have too many children. Kill non-lock ones at random
        while len(new_children) > new_operator.arity:
            potential_victim = random.choice(new_children)
            if potential_victim.is_protected() and lock_status[potential_victim]:
                continue
            new_children.remove(potential_victim)
            
        return Node(operator = new_operator, children = new_children)
   
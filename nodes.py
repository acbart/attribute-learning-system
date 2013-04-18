import random
from config import RANDOM_VARIABLES, BOOLEANS, HEIGHT_MAX
from function_operators import BINARY_OPERATORS, UNARY_OPERATORS, NULLARY_OPERATORS

import itertools


"""

A Node is either:
    TerminalNode
    BinaryNode
    UnaryNode

A TerminalNode is either:
    AttributeNode (which holds an attribute, e.g. "opponent's health")
    ConstantNode (Removed, but held a random value in 0..100)

A BinaryNode has:
    A left child (a Node)
    A right child (a Node)
    A binary operator (e.g. +, -, //)
    
A UnaryNode has:
    A child (a Node)
    A unary operator (e.g. *2, log, sqr)
    
"""

# Interfaces are pointless in Python. Why did I do this.
class Node(object): pass

class TerminalNode(Node):
    def mutate(self, height_left):
        """
        Mutate this node by returning a new one based on this one.
        
        height_left (int): how much farther we can go down the tree before we run out of space
        """
        # If we've reached the bottom level, then we can only copy this node or
        #   randomly change to another type of terminal node
        if height_left <= 0:
            # We always keep a locked node the same!
            if self.is_locked:
                return self.copy()
            else:
                return random_terminal()
                
        # Choose a type of mutation
        if self.is_locked():
            # A locked node cannot change its attribute, only its parents
            mutation = random.choice(("single_parent", "binary_left", "binary_right"))
        else:
            mutation = random.choice(("change", "single_parent", "binary_left", "binary_right"))
            
        # Change this node's attribute
        if mutation == "change":
            return random_terminal()
        # Return a new UnaryNode with this as the child
        elif mutation == "single_parent":
            return UnaryNode(self.copy())
        # Return a new BinaryNode with this as the left child
        elif mutation == "binary_left":
            return BinaryNode(left=self.copy())
        # Return a new BinaryNode with this as the right child
        elif mutation == "binary_right":
            return BinaryNode(right=self.copy())
    
    def __len__(self):
        return 1
        
    def mutate_index(self, mutant, current_index, height_left):
        """
        We're only going to mutate one specific node, but it might not be this
        one!
        
        mutant (int): the node we want to change 
        current_index (int): the current node
        height_left (int)
        
        returns mutant_node (Node), nodes_traversed (int)
        """
        if current_index == mutant:
            return self.mutate(height_left), len(self)
        else:
            return self.copy(), len(self)
           
    def cross_over(self, other, use_selfs_locked_node):
        """
        Create a new Node by combining this and another one. 
        
        The "use_selfs_locked_mode" is to identify whether we should use this
        node's locked node (True) or the other node's locked node (False).
        Remember that we have no idea what node is locked.
        """
        if use_selfs_locked_node and self.is_locked:
            # If this node is locked, and we're using self's lockedness, return
            #   a copy of this node
            return self.copy()
        elif not use_selfs_locked_node and other.is_locked:
            # If the other node is locked and we're using it's lockedness,
            #   return a copy of that node crossed with this one.
            return other.cross_over(self, not use_selfs_locked_node)
        dominant = random.choice(BOOLEANS)
        if dominant:
            # If this node is dominant, then use it
            return self.copy()
        else:
            if isinstance(other, UnaryNode):
                # Keep the binary node, but maybe change a child
                return self.cross_over_with_unary_node(other, use_selfs_locked_node)
            if isinstance(other, BinaryNode):
                # Keep the unary node, but maybe change the child
                return self.cross_over_with_binary_node(other, use_selfs_locked_node)
            else:
                # Keep the other node (it's terminal)
                return other.copy()
    
    def cross_over_with_binary_node(self, other, use_selfs_locked_node):
        # Cross this node with either the left or right child.
        if random.choice(BOOLEANS):
            return BinaryNode(other.left.cross_over(self, use_selfs_locked_node), 
                              other.right.copy(),
                              other.operator)
        else:
            return BinaryNode(other.left.copy(), 
                              other.right.cross_over(self, use_selfs_locked_node),
                              other.operator)
      
    def cross_over_with_unary_node(self, other, use_selfs_locked_node):
        # Cross this node with the child
        return UnaryNode(other.child.cross_over(self, use_selfs_locked_node), 
                                 other.operator)
                                 
class AttributeNode(TerminalNode):
    short_name = {"self_health" : "H", "self_attack": "A", "self_defense": "D",
                  "other_health" : "h", "other_attack": "a", "other_defense": "d"}
                  
    def __init__(self, attribute = None, lock=False):
        """
        attribute (string): the attribute that this represents (default to random)
        lock (boolean): whether this node's attribute cannot be changed
        """
        if attribute is None:
            attribute = random.choice(AttributeNode.short_name.keys())
        self.attribute = attribute
        self.locked = lock
        
    def is_locked(self):
        return self.locked
        
    def evaluate(self, state):
        return state.get_value(self.attribute)
        
    def copy(self):
        return AttributeNode(self.attribute, self.locked)
        
    def __str__(self):
        return self.attribute
        
    def short_string(self):
        return self.short_name[self.attribute]
        
class ConstantNode(TerminalNode):
    """
    I turned this off, and haven't tested if it still works recently.
    """
    def __init__(self, value = None):
        if value is None:
            value = float(random.randint(1, 100))
        self.value = value
        
    def is_locked(self):
        return False
        
    def evaluate(self, state):
        return self.value
        
    def copy(self):
        return ConstantNode(self.value)
        
    def __str__(self):
        return str(self.value)
    
    def short_string(self):
        return str(self.value)
        

def random_terminal():
    """
    Return a random terminal node, unless RANDOM_VARIABLE is off, in which case
    always return a random AttributeNode.
    """
    if not RANDOM_VARIABLES or random.choice(BOOLEANS):
        return AttributeNode()
    else:
        return ConstantNode()
        
class AryNode(Node):
    operators_from_arity = {0 : NULLARY_OPERATORS,
                            1 : UNARY_OPERATORS,
                            2 : BINARY_OPERATORS}
    def __init__(self, operator = None, arity=None, children = None, lock=False):
        """
        children (list) must be ownable by this new AryNode, so don't rely on it.
        """
        self.lock = lock
        if operator is None:
            if arity is None:
                operator = random.choice(NULLARY_OPERATORS + 
                                         UNARY_OPERATORS + 
                                         BINARY_OPERATORS)
            else:
                operator = random.choice(AryNode.operators_from_arity[arity])
        self.operator = operator
        if children is None:
            children = []
            for child in xrange(operator.arity):
                children.append(AryNode(arity=0))
        self.children = children

    @staticmethod
    def random_tree(height_left=HEIGHT_MAX):
        if height_left == 0:
            return AryNode(arity=0)
        arity = random.randint(0, 2)
        children = [random_tree(height_left-1) for child in xrange(arity)]
        new_tree = AryNode(arity=arity, children=children)
        return new_tree
    
    def copy(self):
        children_copies = [child.copy() for child in self.children]
        return AryNode(operator = self.operator, 
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
                return AryNode(operator = self.operator, lock = self.lock)
            else:
                return AryNode(arity = 0, lock = self.lock)
        
        if self.lock:
            new_arity = random.randint(1, 2)
            new_children = [self.copy()] + [AryNode(arity=0) for x in xrange(new_arity-1)]
            random.shuffle(new_children)
            new_node = AryNode(arity=new_arity, children= new_children)
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
                children_copies.append(AryNode(arity=0))
            # Remove nodes until we reach proper arity
            while len(children_copies) > new_arity:
                node_to_kill = random.choice(children_copies)
                if node_to_kill.is_protected():
                    continue
                children_copies.remove(node_to_kill)
            return AryNode(arity = new_arity, children = children_copies)
            
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
            return AryNode(operator = self.operator, children = new_children, lock = self.lock), nodes_traversed
            
    def cross_over(self, other, keeping):
        # If one of the nodes is lock and we're keeping it, then keep it!
        if self.lock and keeping == "self":
            child_node = AryNode(operator = self.operator, lock = True)
            return child_node
        elif other.lock and keeping == "other":
            child_node = AryNode(operator = other.operator, lock = True)
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
            
        return AryNode(operator = new_operator, children = new_children)
        
        
class UnaryNode(Node):
    def __init__(self, child = None, operator= None):
        if operator is None:
            operator = random.choice(UNARY_OPERATORS)
        if child is None:
            child = random_terminal()
        self.operator = operator
        self.child = child
        
    def is_locked(self):
        return self.child.is_locked()
        
    def evaluate(self, state):
        return self.operator(self.child.evaluate(state))
        
    def __len__(self):
        return 1+len(self.child)
        
    def copy(self):
        return UnaryNode(self.child.copy(), self.operator)
    
    def mutate(self, height_left):
        mutation = random.choice(("orphan", "change", "add_right", "add_right"))
        if mutation == "orphan":
            return self.child.copy()
        elif mutation == "change":
            return UnaryNode(self.child.copy())
        elif mutation == "add_right":
            return BinaryNode(left = self.child.copy())
        elif mutation == "add_left":
            return BinaryNode(right = self.child.copy())
            
    def mutate_index(self, mutant, index, height_left):
        if index == mutant:
            return self.mutate(height_left), len(self)
        else:
            child, child_size = self.child.mutate_index(mutant, index+1, height_left-1)
            return UnaryNode(child, self.operator), 1+child_size
            
    def __str__(self):
        return self.operator.formatted_name % (str(self.child),)
        
    def short_string(self):
        return (self.operator.short_name + "(%s)") % (self.child.short_string(),)
    
    def cross_over(self, other, use_selfs_locked_node):
        must_keep_self = use_selfs_locked_node and self.is_locked()
        must_keep_other = not use_selfs_locked_node and other.is_locked()
        dominant = random.choice(BOOLEANS)
        chance = random.choice(BOOLEANS)
        if isinstance(other, UnaryNode):
            return UnaryNode(self.child.cross_over(other.child, use_selfs_locked_node),
                             self.operator if dominant else other.operator)
        elif isinstance(other, BinaryNode):
            if dominant:
                if chance or (not use_selfs_locked_node and other.left.is_locked()):
                    return UnaryNode(self.child.cross_over(other.left, use_selfs_locked_node), 
                                     self.operator)
                else:
                    return UnaryNode(self.child.cross_over(other.right, use_selfs_locked_node), 
                                     self.operator)
            else:
                if chance:
                    return BinaryNode(other.left.cross_over(self.child, use_selfs_locked_node),
                                      other.right.copy(),
                                      other.operator)
                else:
                    return BinaryNode(other.left.copy(),
                                      other.right.cross_over(self.child, use_selfs_locked_node),
                                      other.operator)
        elif isinstance(other, TerminalNode):
            if must_keep_self or (dominant and not must_keep_other):
                return self.copy()
            else:
                return other.copy()            
                
                
        
class BinaryNode(Node):
    def __init__(self, left=None, right=None, operator=None):
        if operator is None:
            operator = random.choice(BINARY_OPERATORS)
        if left is None:
            left = random_terminal()
        if right is None:
            right = random_terminal()
        self.operator = operator
        self.left = left
        self.right = right
    
    def is_locked(self):
        return self.left.is_locked() or self.right.is_locked()
        
    def __len__(self):
        return 1+len(self.left)+len(self.right)
        
    def evaluate(self, state):
        return self.operator(self.left.evaluate(state), self.right.evaluate(state))
        
    def copy(self):
        return BinaryNode(self.left.copy(), self.right.copy(), self.operator)
    
    def __str__(self):
        return self.operator.formatted_name % (str(self.left), str(self.right))
        
    def short_string(self):
        return (self.operator.short_name + "(%s, %s)") % (self.left.short_string(), self.right.short_string())
        
    def mutate_index(self, mutant, current_index, height_left):
        if current_index == mutant:
            return self.mutate(height_left), len(self)
        else:
            left, left_subtree_size = self.left.mutate_index(mutant, current_index+1, height_left-1)
            right, right_subtree_size = self.right.mutate_index(mutant, current_index+1+left_subtree_size, height_left-1)
            return BinaryNode(left, right, self.operator), 1+left_subtree_size+right_subtree_size
        
    def mutate(self, height_left):
        if self.left.is_locked():
            mutation = random.choice(("orphan_left", "change", "remove_right"))
        elif self.right.is_locked():
            mutation = random.choice(("orphan_right", "change", "remove_left"))
        else:
            mutation = random.choice(("orphan_left", "orphan_right", "change", "remove_right", "remove_left"))
        if mutation == "orphan_left":
            return self.left.copy()
        elif mutation == "orphan_right":
            return self.right.copy()
        elif mutation == "change":
            return BinaryNode(self.left.copy(), self.right.copy())
        elif mutation == "remove_right":
            return UnaryNode(self.left.copy())
        elif mutation == "remove_left":
            return UnaryNode(self.right.copy())
    
    def cross_over(self, other, use_selfs_locked_node):
        must_keep_self = use_selfs_locked_node and self.is_locked()
        must_keep_other = not use_selfs_locked_node and other.is_locked()
        dominant = random.choice(BOOLEANS)
        chance = random.choice(BOOLEANS)
        if isinstance(other, BinaryNode):
            return BinaryNode(self.left.cross_over(other.left, use_selfs_locked_node),
                              self.right.cross_over(other.right, use_selfs_locked_node),
                              self.operator if dominant else other.operator)
        elif isinstance(other, UnaryNode):
            if dominant:
                if chance:
                    return BinaryNode(self.left.cross_over(other.child, use_selfs_locked_node),
                                      self.right.copy(),
                                      self.operator)
                else:
                    return BinaryNode(self.left.copy(),
                                      self.right.cross_over(other.child, use_selfs_locked_node),
                                      self.operator)
            else:
                if chance or (not use_selfs_locked_node and self.left.is_locked()):
                    return UnaryNode(other.child.cross_over(self.left, use_selfs_locked_node), 
                                     other.operator)
                else:
                    return UnaryNode(other.child.cross_over(self.right, use_selfs_locked_node), 
                                     other.operator)
        elif isinstance(other, TerminalNode):
            if must_keep_self or (dominant and not must_keep_other):
                return self.copy()
            else:
                return other.copy()
            
def random_tree(height=HEIGHT_MAX):
    if height == 0:
        return random_terminal()
    node = random.choice(("terminal", "binary", "unary"))
    if node == "terminal":
        return random_terminal()
    elif node == "binary":
        return BinaryNode(random_tree(height-1), random_tree(height-1))
    elif node == "unary":
        return UnaryNode(random_tree(height-1))
import random

from random import choice
BOOLEANS = (True, False)

from function_operators import BINARY_OPERATORS, UNARY_OPERATORS, clamp

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
    
A FunctionTree has:
    A root (a Node)
    
Key functions for the FunctionTree (and Nodes):
    copy(self): return a new FunctionTree based on the old one. Nothing changes.
    mutate(self): return a new FunctionTree, based on the old one, with only one
                  change, e.g. a different terminal node, or changing a binary
                  node into a unary node.
    cross_over(self, other): merge two trees by walking through them
                             simultaneously and randomly choosing either the
                             first or the second's nodes. Creates a new tree.
    
The behavior of crossing over two nodes with different locked attribute types is
undefined.
    
"""

HEIGHT_MAX = 2              # The maximum height of a Function Tree
RANDOM_VARIABLES = False    # Whether to use ConstantNodes

class Node(object): pass

class TerminalNode(Node):
    def mutate(self, height_left):
        if height_left <= 0:
            if self.is_locked:
                return self.copy()
            else:
                return random_terminal()
        if self.is_locked():
            mutation = choice(("single_parent", "binary_left", "binary_right"))
        else:
            mutation = choice(("change", "single_parent", "binary_left", "binary_right"))
        if mutation == "change":
            return random_terminal()
        elif mutation == "single_parent":
            return UnaryNode(self.copy())
        elif mutation == "binary_left":
            return BinaryNode(left=self.copy())
        elif mutation == "binary_right":
            return BinaryNode(right=self.copy())
    
    def __len__(self):
        return 1
        
    def inorder(self):
        yield self
        
    def mutate_randomly(self, mutant, index, height_left):
        if index == mutant:
            return self.mutate(height_left), len(self)
        else:
            return self.copy(), len(self)
            
    def cross_over(self, other, sl):
        if sl and self.is_locked:
            return self.copy()
        elif not sl and other.is_locked:
            return other.cross_over(self, not sl)
        dominant = choice(BOOLEANS)
        chance = choice(BOOLEANS)
        if dominant:
            return self.copy()
        else:
            if isinstance(other, UnaryNode):
                return UnaryNode(other.child.cross_over(self, sl), 
                                 other.operator)
            if isinstance(other, BinaryNode):
                if chance:
                    return BinaryNode(other.left.cross_over(self, sl), 
                                      other.right.copy(),
                                      other.operator)
                else:
                    return BinaryNode(other.left.copy(), 
                                      other.right.cross_over(self, sl),
                                      other.operator)
            else:
                return other.copy()

class AttributeNode(TerminalNode):
    short_name = {"self_health" : "H", "self_attack": "A", "self_defense": "D",
                  "other_health" : "h", "other_attack": "a", "other_defense": "d"}
    def __init__(self, index = None, lock=False):
        if index is None:
            index = choice(AttributeNode.short_name.keys())
        self.index = index
        self.locked = lock
        
    def is_locked(self):
        return self.locked
        
    def value(self, state):
        return state.get_value(self.index)
        
    def copy(self):
        return AttributeNode(self.index, self.locked)
        
    def __str__(self):
        return self.index
    def short_string(self):
        return self.short_name[self.index]
        
    def label(self):
        return self.index
    def children(self):
        return []
    label = property(label)
    children = property(children)
        
class ConstantNode(TerminalNode):
    def __init__(self, value = None):
        if value is None:
            value = float(random.randint(1, 100))
        self._value = value
        
    def is_locked(self):
        return False
        
    def value(self, state):
        return self._value
        
    def copy(self):
        return ConstantNode(self._value)
        
    def __str__(self):
        return str(self._value)

    def label(self):
        return self._value
    def children(self):
        return []
    label = property(label)
    children = property(children)
        
def random_terminal():
    if not RANDOM_VARIABLES or choice(BOOLEANS):
        return AttributeNode()
    else:
        return ConstantNode()
        
class UnaryNode(Node):
    def __init__(self, child = None, operator= None):
        if operator is None:
            operator = choice(UNARY_OPERATORS)
        if child is None:
            child = random_terminal()
        self.operator = operator
        self.child = child
        
    def is_locked(self):
        return self.child.is_locked()
        
    def value(self, state):
        return self.operator(self.child.value(state))
    
    def label(self):
        return self.operator.short_name
    def children(self):
        return [self.child]
    label = property(label)
    children = property(children)
        
    def __len__(self):
        return 1+len(self.child)
        
    def copy(self):
        return UnaryNode(self.child.copy(), self.operator)
    
    def mutate(self, height_left):
        mutation = choice(("orphan", "change", "add_right", "add_right"))
        if mutation == "orphan":
            return self.child.copy()
        elif mutation == "change":
            return UnaryNode(self.child.copy())
        elif mutation == "add_right":
            return BinaryNode(left = self.child.copy())
        elif mutation == "add_left":
            return BinaryNode(right = self.child.copy())
            
    def mutate_randomly(self, mutant, index, height_left):
        if index == mutant:
            return self.mutate(height_left), len(self)
        else:
            child, child_size = self.child.mutate_randomly(mutant, index+1, height_left-1)
            return UnaryNode(child, self.operator), 1+child_size
            
    def inorder(self):
        yield self
        for x in self.child.inorder():
            yield x
            
    def __str__(self):
        return self.operator.formatted_name % (str(self.child),)
        
    def short_string(self):
        return (self.operator.short_name + "(%s)") % (self.child.short_string(),)
    
    def cross_over(self, other, sl):
        must_keep_self = sl and self.is_locked()
        must_keep_other = not sl and other.is_locked()
        dominant = choice(BOOLEANS)
        chance = choice(BOOLEANS)
        if isinstance(other, UnaryNode):
            return UnaryNode(self.child.cross_over(other.child, sl),
                             self.operator if dominant else other.operator)
        elif isinstance(other, BinaryNode):
            if dominant:
                if chance or (not sl and other.left.is_locked()):
                    return UnaryNode(self.child.cross_over(other.left, sl), 
                                     self.operator)
                else:
                    return UnaryNode(self.child.cross_over(other.right, sl), 
                                     self.operator)
            else:
                if chance:
                    return BinaryNode(other.left.cross_over(self.child, sl),
                                      other.right.copy(),
                                      other.operator)
                else:
                    return BinaryNode(other.left.copy(),
                                      other.right.cross_over(self.child, sl),
                                      other.operator)
        elif isinstance(other, TerminalNode):
            if must_keep_self or (dominant and not must_keep_other):
                return self.copy()
            else:
                return other.copy()            
                
                
        
class BinaryNode(Node):
    def __init__(self, left=None, right=None, operator=None):
        if operator is None:
            operator = choice(BINARY_OPERATORS)
        if left is None:
            left = random_terminal()
        if right is None:
            right = random_terminal()
        self.operator = operator
        self.left = left
        self.right = right
    
    def is_locked(self):
        return self.left.is_locked() or self.right.is_locked()
        
    def inorder(self):
        for x in self.left.inorder():
            yield x
        yield self
        for x in self.right.inorder():
            yield x
            
    def label(self):
        return self.operator.short_name
    def children(self):
        return [self.left, self.right]
    label = property(label)
    children = property(children)
        
    def __len__(self):
        return 1+len(self.left)+len(self.right)
        
    def value(self, state):
        return self.operator(self.left.value(state), self.right.value(state))
        
    def copy(self):
        return BinaryNode(self.left.copy(), self.right.copy(), self.operator)
    
    def __str__(self):
        return self.operator.formatted_name % (str(self.left), str(self.right))
        
    def short_string(self):
        return (self.operator.short_name + "(%s, %s)") % (self.left.short_string(), self.right.short_string())
        
    def mutate_randomly(self, mutant, index, height_left):
        if index == mutant:
            return self.mutate(height_left), len(self)
        else:
            left, left_subtree_size = self.left.mutate_randomly(mutant, index+1, height_left-1)
            right, right_subtree_size = self.right.mutate_randomly(mutant, index+1+left_subtree_size, height_left-1)
            return BinaryNode(left, right, self.operator), 1+left_subtree_size+right_subtree_size
        
    def mutate(self, height_left):
        if self.left.is_locked():
            mutation = choice(("orphan_left", "change", "remove_right"))
        elif self.right.is_locked():
            mutation = choice(("orphan_right", "change", "remove_left"))
        else:
            mutation = choice(("orphan_left", "orphan_right", "change", "remove_right", "remove_left"))
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
    
    def cross_over(self, other, sl):
        must_keep_self = sl and self.is_locked()
        must_keep_other = not sl and other.is_locked()
        dominant = choice(BOOLEANS)
        chance = choice(BOOLEANS)
        if isinstance(other, BinaryNode):
            return BinaryNode(self.left.cross_over(other.left, sl),
                              self.right.cross_over(other.right, sl),
                              self.operator if dominant else other.operator)
        elif isinstance(other, UnaryNode):
            if dominant:
                if chance:
                    return BinaryNode(self.left.cross_over(other.child, sl),
                                      self.right.copy(),
                                      self.operator)
                else:
                    return BinaryNode(self.left.copy(),
                                      self.right.cross_over(other.child, sl),
                                      self.operator)
            else:
                if chance or (not sl and self.left.is_locked()):
                    return UnaryNode(other.child.cross_over(self.left, sl), 
                                     other.operator)
                else:
                    return UnaryNode(other.child.cross_over(self.right, sl), 
                                     other.operator)
        elif isinstance(other, TerminalNode):
            if must_keep_self or (dominant and not must_keep_other):
                return self.copy()
            else:
                return other.copy()
            
def random_tree(height=HEIGHT_MAX):
    if height == 0:
        return random_terminal()
    node = choice(("terminal", "binary", "unary"))
    if node == "terminal":
        return random_terminal()
    elif node == "binary":
        return BinaryNode(random_tree(height-1), random_tree(height-1))
    elif node == "unary":
        return UnaryNode(random_tree(height-1))

class FunctionTree(object):
    def __init__(self, root=None, feature = None):
        if root is None:
            root = random_tree()
        if feature is not None:
            root = AttributeNode(feature, lock=True)
        self.root = root
    
    def copy(self):
        return FunctionTree(self.root.copy())
    
    def mutate(self):
        mutant = random.randrange(len(self.root))
        return FunctionTree(self.root.mutate_randomly(mutant, 0, HEIGHT_MAX)[0])
    
    def cross_over(self, other):
        return FunctionTree(self.root.cross_over(other.root, choice(BOOLEANS)))
    
    def inorder(self):
        return self.root.inorder()
    
    def __len__(self):
        return len(self.root)
    
    def __str__(self):
        return str(self.root)
    
    def short_string(self):
        return self.root.short_string()
    
    def value(self, state):
        return clamp(self.root.value(state))
        
import random
random.seed(42)

import math
import operator

def div(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 0
        
def floordiv(left, right):
    try:
        return left // right
    except ZeroDivisionError:
        return 0
        
def sqr(value):
    return value ** 2
        
UNARY_OPERATORS = [sqr, math.sqrt, math.ceil, 
                   math.floor, math.log]
BINARY_OPERATORS = [operator.add, operator.mul, operator.sub, 
                    math.fmod, div, floordiv]

# given a vector of variables A, we want to define a random function
#   F such that F: A -> A'. The function F can use any combination of 
#   variables from A, favoring smaller combinations. It can use any of
#   the following binary operations: addition, subtraction, division, 
#   multiplication, and exponentiation. It can also use a random
#   variable X (that'll change every run of the function)
    
# a -> a'                   : a
# g(a) -> a'                : ua
# h(a,b) -> a'              : baa
# h(g(a),b) -> a'           : buaa
# h(a,g(b)) -> a'           : baua
# h(g(a),g(b)) -> a'        : 
# h(h(a,b),g(c)) -> a'
# h(g(a),h(b,c)) -> a'
# h(h(a,b),h(c,d)) -> a'
# A terminal node 

# binary operator
# a
# ua
# baa

# For each terminal node

# +, -, /, *, **, // : a, b -> a'
# +X, -X, /X, *X, **X, //X : a -> a'
# a : -> a'

class Node(object): pass

class TerminalNode(Node):
    def mutate(self):
        mutation = random.choice(("change", "single_parent", "binary_left", "binary_right"))
        if mutation == "change":
            return random_terminal()
        elif mutation == "single_parent":
            return UnaryNode(self.copy())
        elif mutation == "binary_left":
            return BinaryNode(left=self.copy())
        elif mutation == "binary_right":
            return BinaryNode(right =self.copy())
    
    def __len__(self):
        return 1
        
    def inorder(self):
        yield self
        
    def mutate_randomly(self, mutant, index):
        if index == mutant:
            return self.mutate(), len(self)
        else:
            return self.copy(), len(self)
            
    def cross_over(self, other):
        dominant = random.choice((True, False))
        chance = random.choice((True, False))
        if dominant:
            return self.copy()
        else:
            if isinstance(other, UnaryNode):
                return UnaryNode(other.child.cross_over(self), other.operator)
            if isinstance(other, BinaryNode):
                if chance:
                    return BinaryNode(other.left.cross_over(self), 
                                      other.right.copy(),
                                      other.operator)
                else:
                    return BinaryNode(other.left.copy(), 
                                      other.right.cross_over(self),
                                      other.operator)
            else:
                return other.copy()

class AttributeNode(TerminalNode):
    def __init__(self, index = None):
        if index is None:
            index = random.choice(("health_1", "attack_1", "defense_1",
                                   "health_2", "attack_2", "defense_2"))
        self.index = index
        
    def value(self, state):
        return getattr(state, self.index)
        
    def copy(self):
        return AttributeNode(self.index)
        
    def __str__(self):
        return self.index
        
class ConstantNode(TerminalNode):
    def __init__(self, value = None):
        if value is None:
            value = float(random.randint(1, 100))
        self._value = value
        
    def value(self, state):
        return self._value
        
    def copy(self):
        return ConstantNode(self._value)
        
    def __str__(self):
        return str(self._value)

def random_terminal():
    if random.choice((True, False)):
        return AttributeNode()
    else:
        return ConstantNode()
        
class UnaryNode(Node):
    def __init__(self, child = None, operator= None):
        if operator is None:
            operator = random.choice(UNARY_OPERATORS)
        if child is None:
            child = random_terminal()
        self.operator = operator
        self.child = child
        
    def value(self, state):
        return self.operator(self.child.value(state))
        
    def __len__(self):
        return 1+len(self.child)
        
    def copy(self):
        return UnaryNode(self.child.copy(), self.operator)
    
    def mutate(self):
        mutation = random.choice(("orphan", "change", "add_right", "add_right"))
        if mutation == "orphan":
            return self.child.copy()
        elif mutation == "change":
            return UnaryNode(self.child.copy())
        elif mutation == "add_right":
            return BinaryNode(left = self.child.copy())
        elif mutation == "add_left":
            return BinaryNode(right = self.child.copy())
            
    def mutate_randomly(self, mutant, index):
        if index == mutant:
            return self.mutate(), len(self)
        else:
            child, child_size = self.child.mutate_randomly(mutant, index+1)
            return UnaryNode(child, self.operator), 1+child_size
            
    def inorder(self):
        yield self
        for x in self.child.inorder():
            yield x
            
    def __str__(self):
        return "%s(%s)" % (self.operator.__name__, str(self.child))
    
    def cross_over(self, other):
        dominant = random.choice((True, False))
        chance = random.choice((True, False))
        if isinstance(other, UnaryNode):
            return UnaryNode(self.child.cross_over(other.child),
                             self.operator if dominant else other.operator)
        elif isinstance(other, BinaryNode):
            if dominant:
                if chance:
                    return UnaryNode(self.child.cross_over(other.left), self.operator)
                else:
                    return UnaryNode(self.child.cross_over(other.right), self.operator)
            else:
                if chance:
                    return BinaryNode(other.left.cross_over(self.child),
                                      other.right.copy(),
                                      other.operator)
                else:
                    return BinaryNode(other.left.copy(),
                                      other.right.cross_over(self.child),
                                      other.operator)
        elif isinstance(other, TerminalNode):
            if dominant:
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
        
    def inorder(self):
        for x in self.left.inorder():
            yield x
        yield self
        for x in self.right.inorder():
            yield x
        
    def __len__(self):
        return 1+len(self.left)+len(self.right)
        
    def value(self, state):
        return self.operator(self.left.value(state), self.right.value(state))
        
    def copy(self):
        return BinaryNode(self.left.copy(), self.right.copy(), self.operator)
    
    def __str__(self):
        return "%s(%s, %s)" % (self.operator.__name__, str(self.left), str(self.right))
        
    def mutate_randomly(self, mutant, index):
        if index == mutant:
            return self.mutate(), len(self)
        else:
            left, left_subtree_size = self.left.mutate_randomly(mutant, index+1)
            right, right_subtree_size = self.right.mutate_randomly(mutant, index+1+left_subtree_size)
            return BinaryNode(left, right, self.operator), 1+left_subtree_size+right_subtree_size
        
    def mutate(self):
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
    
    def cross_over(self, other):
        dominant = random.choice((True, False))
        chance = random.choice((True, False))
        if isinstance(other, BinaryNode):
            return BinaryNode(self.left.cross_over(other.left),
                              self.right.cross_over(other.right),
                              self.operator if dominant else other.operator)
        elif isinstance(other, UnaryNode):
            if dominant:
                if chance:
                    return BinaryNode(self.left.cross_over(other.child),
                                      self.right.copy(),
                                      self.operator)
                else:
                    return BinaryNode(self.left.copy(),
                                      self.right.cross_over(other.child),
                                      self.operator)
            else:
                if chance:
                    return UnaryNode(other.child.cross_over(self.left), other.operator)
                else:
                    return UnaryNode(other.child.cross_over(self.right), other.operator)
        elif isinstance(other, TerminalNode):
            if dominant:
                return self.copy()
            else:
                return other.copy()
            
def random_tree(height=3):
    if height == 0:
        return random_terminal()
    node = random.choice(("terminal", "binary", "unary"))
    if node == "terminal":
        return random_terminal()
    elif node == "binary":
        return BinaryNode(random_tree(height-1), random_tree(height-1))
    elif node == "unary":
        return UnaryNode(random_tree(height-1))

class FunctionTree(object):
    def __init__(self, root=None):
        if root is None:
            root = random_tree()
        self.root = root
    
    def copy(self):
        return self.root.copy()
    
    def mutate(self):
        mutant = random.randrange(len(self.root))
        return FunctionTree(self.root.mutate_randomly(mutant, 0)[0])
    
    def cross_over(self, other):
        return FunctionTree(self.root.cross_over(other.root))
    
    def inorder(self):
        return self.root.inorder()
    
    def __len__(self):
        return len(self.root)
    
    def __str__(self):
        return str(self.root)
    
    def value(self, state):
        return self.root.value(state)
        
# for x in xrange(5):
    # ft = FunctionTree()
    # print x, "Orgnal:", ft
    # m =ft.mutate()
    # print x, "Mutant:", m
    
# print ""

# for x in xrange(5):
    # dad, mom = FunctionTree(), FunctionTree()
    # print x, "Dad:", dad
    # print x, "Mom:", mom
    # kid = mom.cross_over(dad)
    # print x, "Kid:", kid

import math
import operator

def clamp(value, minimum = 0, maximum = 100):
    return min(maximum, max(minimum, value))

def bound_check(minimum = 0, maximum = 100):
    """
    Decorator for clamping a functions output to be between 0 and 100, or within
    a specified range.
    """
    def wrap(f):
        def new_f(*args):
            return min(maximum, max(minimum, f(*args)))
        return new_f
    return wrap
    
def log(value):
    try:
        return math.log(value)
    except ValueError:
        return 0

def sqrt(value):
    try:
        return math.sqrt(value)
    except ValueError:
        return 0
        
def sqr(value):
    return value ** 2

def ceil(value):
    return math.ceil(value)
   
def floor(value):
    return math.floor(value)
    
def double(value): return value * 2.
def halve(value): return value / 2.    
def triple(value): return value * 3.
def third(value): return value / 3.
def increment(value): return value + 1.
def decrement(value): return value - 1.
    
log.string_template = "log(%s)"
log.op = "log"
sqrt.string_template = "sqrt(%s)"
sqrt.op = "sqrt"
sqr.string_template = "sqr(%s)"
sqr.op = "sqr"
ceil.string_template = "ceil(%s)"
ceil.op = "v"
floor.string_template = "floor(%s)"
floor.op = "^"
double.string_template = "(2 * %s)"
double.op = "*2"
halve.string_template = "(%s / 2)"
halve.op = "/2"
triple.string_template = "(3 * %s)"
triple.op = "*3"
third.string_template = "(%s / 3)"
third.op = "/3"
increment.string_template = "(%s + 1)"
increment.op = "+1"
decrement.string_template = "(%s - 1)"
decrement.op = "-1"
        
UNARY_OPERATORS = [sqrt, ceil, floor, log, double, halve, triple, third, increment, decrement]
   
def fmod(left, right):
    try:
        return math.fmod(left, right)
    except ValueError:
        return 0        
    
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

def add(left, right):
    return left + right

def multipy(left, right):
    return left * right

def subtract(left, right):
    return left - right
    
fmod.string_template = "mod(%s, %s)"
fmod.op = "%"
div.string_template = "(%s / %s)"
div.op = "/"
floordiv.string_template = "(%s // %s)"
floordiv.op = "//"
add.string_template = "(%s + %s)"
add.op = "+"
multipy.string_template = "(%s * %s)"
multipy.op = "*"
subtract.string_template = "(%s - %s)"
subtract.op = "-"

BINARY_OPERATORS = [add, multipy, subtract, fmod, div, floordiv]
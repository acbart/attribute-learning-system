
import math
import operator

"""
This file defines a bunch of operators for a FunctionTree. They are either
Unary operators (with one argument) or Binary operators (with two arguments).

Every function has a "short_name" property to concisely describe it's name, and
a "formatted_name" that can be interpolated to look like the actual function
call.

There is also the "clamp" function, which is used to force results to stay
between 0 and 100.
"""

def clamp(value, minimum = 0, maximum = 100):
    # This function is called a bajillion times, possibly optimize it?
    return min(maximum, max(minimum, value))

def bound_check(minimum = 0, maximum = 100):
    """
    Decorator for clamping a functions output to be between 0 and 100, or within
    a specified range.
    
    I don't actually use it.
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
    
log.formatted_name = "log(%s)"
log.short_name = "log"
sqrt.formatted_name = "sqrt(%s)"
sqrt.short_name = "sqrt"
sqr.formatted_name = "sqr(%s)"
sqr.short_name = "sqr"
ceil.formatted_name = "ceil(%s)"
ceil.short_name = "v"
floor.formatted_name = "floor(%s)"
floor.short_name = "^"
double.formatted_name = "(2 * %s)"
double.short_name = "*2"
halve.formatted_name = "(%s / 2)"
halve.short_name = "/2"
triple.formatted_name = "(3 * %s)"
triple.short_name = "*3"
third.formatted_name = "(%s / 3)"
third.short_name = "/3"
increment.formatted_name = "(%s + 1)"
increment.short_name = "+1"
decrement.formatted_name = "(%s - 1)"
decrement.short_name = "-1"
        
UNARY_OPERATORS = [double, halve, triple, third, increment, decrement] #ceil, floor, log, sqrt, 
   
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

def multiply(left, right):
    return left * right

def subtract(left, right):
    return left - right
    
fmod.formatted_name = "mod(%s, %s)"
fmod.short_name = "mod"
div.formatted_name = "(%s / %s)"
div.short_name = "/"
floordiv.formatted_name = "(%s // %s)"
floordiv.short_name = "//"
add.formatted_name = "(%s + %s)"
add.short_name = "+"
multiply.formatted_name = "(%s * %s)"
multiply.short_name = "*"
subtract.formatted_name = "(%s - %s)"
subtract.short_name = "-"

BINARY_OPERATORS = [add, multiply, subtract, fmod, div] #floordiv
# from itertools import chain, repeat

# def ncycles(iterable, n):
    # "Returns the sequence elements n times"
    # return chain.from_iterable(repeat(tuple(iterable), n))
    
# print [x for x in ncycles([1,2,3], 5)]

import timeit

setup1 = """
import random
def clamp(value):
    return max(0, min(100, value))
"""

setup2 = """
import random
def clamp(value):
    if value < 0:
        return 0
    elif value > 100:
        return 100
    return value
"""

print timeit.timeit('clamp(random.randint(-100, 200))', setup=setup1, number = 10000000)
print timeit.timeit('clamp(random.randint(-100, 200))', setup=setup2, number = 10000000)
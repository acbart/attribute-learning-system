# from itertools import chain, repeat

# def ncycles(iterable, n):
    # "Returns the sequence elements n times"
    # return chain.from_iterable(repeat(tuple(iterable), n))
    
# print [x for x in ncycles([1,2,3], 5)]

import timeit

setup1 = """
class A(dict):
    def __init__(self):
        dict.__init__(self)
        self["a"] = 100
        self["b"] = 50
        
c = A()
"""

setup2 = """
c = {"a" : 100, "b" : 50}
"""

print timeit.timeit('c["a"]', setup=setup1, number = 10000000)
print timeit.timeit('c["a"]', setup=setup2, number = 10000000)
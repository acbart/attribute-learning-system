# from itertools import chain, repeat

# def ncycles(iterable, n):
    # "Returns the sequence elements n times"
    # return chain.from_iterable(repeat(tuple(iterable), n))
    
# print [x for x in ncycles([1,2,3], 5)]

def filter(self, player, attribute):
    return [value for key, value in self.iteritems() if key.startswith(player) and attribute in key]

import timeit

setup1 = """
k = (1,2,3,4,5,6)
"""

setup2 = """
k = dict([(1+x, "banana") for x in xrange(5)])
"""


print timeit.timeit('j(3)', setup=setup1, number = 10000000)
print timeit.timeit('j(3)', setup=setup2, number = 10000000)
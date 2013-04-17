from itertools import chain, repeat

def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(tuple(iterable), n))
    
print [x for x in ncycles([1,2,3], 5)]
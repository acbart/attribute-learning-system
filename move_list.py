import random
from config import ATTRIBUTE_TYPES, NUMBER_OF_MOVES_PER_MOVE_LIST

from function_vector import FunctionVector
from function_tree import FunctionTree

FUNCTION_TYPE = FunctionVector

class MoveList(list):
    def __init__(self, moves = None):
        if moves is None:
            moves = [FUNCTION_TYPE() for i in xrange(NUMBER_OF_MOVES_PER_MOVE_LIST)]
            self.force_damagers(moves)

        list.__init__(self, moves)

    def cross_over(self, other):
        child_move_list = MoveList([])
        # Possible improvement: match up children with the same features
        for self_move, other_move in zip(self, other):
            child_move_list.append(self_move.cross_over(other_move))
        self.force_damagers(child_move_list)
        return child_move_list

    def force_damagers(self, l):
        mid = len(l) / 2
        if not any(m.feature.startswith("other_primary_") for m in l[:mid]):
            l[0] = FUNCTION_TYPE(feature = "other_primary_"+str(random.randint(1,ATTRIBUTE_TYPES["primary"])))
        if not any(m.feature.startswith("other_primary_") for m in l[mid+1:]):
            l[mid] = FUNCTION_TYPE(feature = "other_primary_"+str(random.randint(1,ATTRIBUTE_TYPES["primary"])))

    def mutate(self):
        new_list = [move.mutate() for move in self]
        if not random.randint(0,5):
            mid = len(new_list) / 2
            frozen = (new_list[0], new_list[mid]) if random.choice((True, False)) else (new_list[mid], new_list[0])
            new_list = new_list[1:mid] + new_list[mid+1:]
            random.shuffle(new_list)
            new_list.insert(0, frozen[0])
            new_list.insert(mid, frozen[1])
        self.force_damagers(new_list)
        return MoveList(new_list)

    def __str__(self):
        return "[%s]" % (", ".join(map(str, self)),)

    def short_string(self):
        return "[%s]" % (", ".join([move.short_string() for move in self]),)

    def __hash__(self):
        return hash(self.short_string())

    def subtract(self, other):
        result = []
        for item in self:
            if item not in other:
                result.append(item)
        return result

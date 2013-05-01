from move import Move
from config import NUMBER_OF_MOVES_PER_MOVE_LIST

class MoveList(list):
    def __init__(self, moves = None):
        if moves is None:
            moves = [Move.generate_random_move() 
                        for i in xrange(NUMBER_OF_MOVES_PER_MOVE_LIST)]
        list.__init__(self, moves)
    
    def cross_over(self, other):
        child_move_list = MoveList([])
        # Possible improvement: match up children with the same features
        for self_move, other_move in zip(self, other):
            child_move_list.append(self_move.cross_over(other_move))
        return child_move_list
    
    def mutate(self):
        return MoveList([move.mutate() for move in self])
        
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
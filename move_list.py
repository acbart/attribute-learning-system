from config import NUMBER_OF_MOVES_PER_MOVE_LIST, FUNCTION_TYPE

class MoveList(list):
    def __init__(self, moves = None):
        if moves is None:
            moves = [FUNCTION_TYPE()
                        for i in xrange(NUMBER_OF_MOVES_PER_MOVE_LIST)]
                        
            found_1 = False
            for move in moves[:3]:
                if move.feature == "other_primary_1":
                    found_1 = True
                    
            found_2 = False
            for move in moves[:3]:
                if move.feature == "other_primary_1":
                    found_2 = True
            
            f = FUNCTION_TYPE()
            f.feature = "other_primary_1"
            f.coeffecients = {"self_secondary_1":0, "other_secondary_2":0}
            f.constant = -10
            
            if not found_1:
                moves[0] = FUNCTION_TYPE(f)
            
            if not found_2:
                moves.append(FUNCTION_TYPE(f))
            
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

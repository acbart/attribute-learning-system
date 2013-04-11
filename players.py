import random
from aima.minimax import alphabeta_search, Game

class Player(object):
    __name__ = "Abstract Player"
    def __init__(self, movelist):
        self.movelist = movelist
        
    def get_initial_stats(self):
        return 100, 10, 10
    
class RandomPlayer(Player):
    __name__ = "Random Player"
    def __init__(self, movelist):
        Player.__init__(self, movelist)
    
    def move(self, battle_state):
        using_move = random.choice(self.movelist.moves)
        return using_move.apply(battle_state), using_move
        
class EagerPlayer(Player):
    __name__ = "Eager Player"
    def __init__(self, movelist):
        Player.__init__(self, movelist)
    
    def move(self, battle_state):
        using_move = self.movelist.moves[0]
        return using_move.apply(battle_state), using_move
        
class MinimaxState(object):
    __slots__ = ["health_1", "attack_1", "defense_1",
                 "health_2", "attack_2", "defense_2",
                 "turn"]
    def __init__(self, other, turn):
        self.health_1 = other.health_1
        self.attack_1 = other.attack_1
        self.defense_1 = other.defense_1
        self.health_2 = other.health_2
        self.attack_2 = other.attack_2
        self.defense_2 = other.defense_2
        self.turn = turn
        
    def flip(self):
        self.health_1, self.health_2 = self.health_2, self.health_1
        self.attack_1, self.attack_2 = self.attack_2, self.attack_1
        self.defense_1, self.defense_2 = self.defense_2, self.defense_1
        
class MinimaxGame(Game):
    # True means it's player 1's turn
    def __init__(self, moves):
        self.moves = moves
    
    def actions(self, state):
        return self.moves
    
    def result(self, state, action):
        new_state = MinimaxState(state, not state.turn)
        if state.turn:
            new_state.flip()
        for feature, function in action.iteritems():
            setattr(new_state, feature, function.value(state))
        if state.turn:
            new_state.flip()
        return new_state
    
    def utility(self, state, player):
        # worth = 0
        # p1, p2 = ("1", "2") if state.turn else ("2", "1")
        # for positive_feature in ("health_"+p1, "attack_"+p1, "defense_"+p1):
            # worth += getattr(state, positive_feature)
        # for negative_feature in ("health_"+p2, "attack_"+p2, "defense_"+p2):
            # worth -= getattr(state, negative_feature)
        # return worth
        # Alternate battle calculation where only health matters
        if state.turn:
            return state.health_1 - state.health_2
        else:
            return state.health_2 - state.health_1
            
    def to_move(self, state):
        return state.turn
    
    def terminal_test(self, state):
        return state.health_1 <= 0 or state.health_2 <= 0

class MinimaxPlayer(Player):
    __name__ = "Minimax Player"
    def move(self, battle_state):
        battle = MinimaxGame(self.movelist.moves)
        initial = MinimaxState(battle_state, True)
        move = alphabeta_search(initial, battle, d= 5)
        return move.apply(battle_state), move
        
PLAYERS = [MinimaxPlayer]
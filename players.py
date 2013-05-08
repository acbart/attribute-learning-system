import random
from aima.minimax import alphabeta_search as minimax_decision
from aima.minimax import Game

"""
Player is a class that makes decision in a battle_simulation. When they are
defined, they should be given a movelist, which they can use to make decisions.
For instance, a RandomPlayer will choose a move randomly, but a MiniMax player
will actually attempt to find an ideal move to play.

A Player should also define "get_initial_stats", this way we can have players
in the future with initial buffs like a higher defense or something.
"""

# TODO:
#   add Greedy player, who always takes the currently optimal attack

class Player(object):
    __name__ = "Abstract Player"
    def __init__(self, moves):
        self.moves = moves
        self.opponent = None

    def get_initial_stats(self):
        return {"primary_1": 100, "secondary_1": 10, "secondary_2": 10}

class RandomPlayer(Player):
    """
    A random player always chooses a random attack.
    """
    __name__ = "Random Player"

    def get_move(self, battle_state):
        return random.choice(self.moves)

class EagerPlayer(Player):
    """
    An eager player always chooses the first attack.
    """
    __name__ = "Eager Player"

    def get_move(self, battle_state):
        return self.moves[0]

class MinimaxGame(Game):

    # True means it's player 1's turn
    def __init__(self, moves, opponent, initial_turn):
        self.moves = moves
        self.opponent = opponent
        self.initial_turn = initial_turn

    def actions(self, state):
        if state.turn == self.initial_turn:
            return self.moves
        else:
            return self.opponent.moves

    def result(self, state, action):
        return state.apply(action)

    def utility(self, state):
        if self.initial_turn:
            if state.is_player_dead("player_1"): return 0
            return sum(state.get_primary_values("player_1")) - sum(state.get_primary_values("player_2"))
        else:
            if state.is_player_dead("player_2"): return 0
            return sum(state.get_primary_values("player_2")) - sum(state.get_primary_values("player_1"))

    def terminal_test(self, state):
        return not state.players_alive()

class MinimaxPlayer(Player):
    """
    A minimax player will use the Minimax algorithm to calculate the optimal
    move at a limited depth.
    """
    __name__ = "Minimax Player"
    def __init__(self, moves, level = 4):
        self.level = level
        Player.__init__(self, moves)
        
    def get_move(self, battle_state):
        battle = MinimaxGame(self.moves, self.opponent, battle_state.turn)
        move = minimax_decision(battle_state, battle, d= self.level)
        return move

class GreedyPlayer(Player):
    """
    A greedy player simply decides what the best move to take this turn is,
    without looking ahead at all.
    """
    __name__ = "Greedy Player"
    def get_move(self, battle_state):
        battle = MinimaxGame(self.moves, self.opponent, battle_state.turn)
        move = minimax_decision(battle_state, battle, d=0)
        return move

PLAYERS = [MinimaxPlayer]
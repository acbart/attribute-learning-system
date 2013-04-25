import random
from aima.minimax import alphabeta_search, Game
from battle_state import BattleState

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
    def __init__(self, movelist):
        self.movelist = movelist

    def get_initial_stats(self):
        return 100, 10, 10

class RandomPlayer(Player):
    """
    A random player always chooses a random attack.
    """
    __name__ = "Random Player"
    def __init__(self, movelist):
        Player.__init__(self, movelist)

    def get_move(self, battle_state):
        return random.choice(self.movelist)

class EagerPlayer(Player):
    """
    An eager player always chooses the first attack.
    """
    __name__ = "Eager Player"
    def __init__(self, movelist):
        Player.__init__(self, movelist)

    def get_move(self, battle_state):
        return self.movelist.moves[0]

class MinimaxGame(Game):

    # True means it's player 1's turn
    def __init__(self, moves):
        self.moves = moves

    def actions(self, state):
        return self.moves

    def result(self, state, action):
        new_state= action.apply(state)
        return new_state

    def utility(self, state, player):
        return state.value()

    def to_move(self, state):
        return state.turn

    def terminal_test(self, state):
        return not state.players_alive()

class MinimaxPlayer(Player):
    """
    A minimax player will use the Minimax algorithm to calculate the optimal
    move at a limited depth.
    """
    __name__ = "Minimax Player"
    def get_move(self, battle_state):
        battle = MinimaxGame(self.movelist)
        initial = BattleState(source = battle_state)
        move = alphabeta_search(initial, battle, d= 4)
        return move

class GreedyPlayer(Player):
    """
    A greedy player simply decides what the best move to take this turn is,
    without looking ahead at all.
    """
    __name__ = "Greedy Player"
    def get_move(self, battle_state):
        battle = MinimaxGame(self.movelist)
        initial = BattleState(source = battle_state)
        move = alphabeta_search(initial, battle, d= 1)
        return move

PLAYERS = [GreedyPlayer]
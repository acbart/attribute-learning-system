"""Games, or Adversarial Search. (Chapter 5)
"""

from aima.utils import *
import random

#______________________________________________________________________________
# Minimax Search

def minimax_decision(state, game, d=4):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Fig. 5.3]"""

    player = game.to_move(state)

    def max_value(state, depth):
        print "\t" * depth, "N", state.turn, hash(",".join([m.short_string() for m in game.actions(state)]))
        #print "MAX", state.turn
        if game.terminal_test(state) or depth > d:
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), depth+1))
        return v

    def min_value(state, depth):
        if game.terminal_test(state) or depth > d:
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), depth+1))
        return v

    # Body of minimax_decision:
    v, best_a = -infinity, None
    for a in game.actions(state):
        new_v = min_value(game.result(state, a), 1)
        if v < new_v:
            v = new_v
            best_a = a
    return best_a

#______________________________________________________________________________

def alphabeta_full_search(state, game, d=4):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Fig. 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if game.terminal_test(state) or depth > d:
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if game.terminal_test(state) or depth > d:
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a),
                                      -infinity, infinity, 1))

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for i, a in enumerate(game.actions(state)):
            new_v = min_value(game.result(state, a), alpha, beta, depth+1)
            v = max(v, new_v)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth, name=None):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for i, a in enumerate(game.actions(state)):
            new_v = max_value(game.result(state, a), alpha, beta, depth+1)
            v = min(v, new_v)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state))
    act = argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a),
                                      -infinity, infinity, 0, a))
    return act
    
debug = False
if debug: minimax_log = open("minimax.log", "w")
def alphabeta_search_debug(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    global debug
    
    if debug: minimax_log.write("New testrun!\n")

    def max_value(state, alpha, beta, depth):
        if debug: minimax_log.write("\t" * depth + str(depth) + " " + str(state) + "\n")
        if cutoff_test(state, depth):
            if debug: minimax_log.write("\t" * (depth) + "Cutoff!\n")
            return eval_fn(state)
        v = -infinity
        if debug and len(game.actions(state)) == 0:
            minimax_log.write("\t" * (depth) + "No more actions!\n")
        for i, a in enumerate(game.actions(state)):
            if debug: minimax_log.write("\t" * (1+depth) + "Exploring " + str(i) + "\n")
            new_v = min_value(game.result(state, a), alpha, beta, depth+1)
            if debug: minimax_log.write("\t" * (1+depth) + "... " + str(new_v) + " [" + str(v) + "] maximize\n")
            v = max(v, new_v)
            if v >= beta:
                if debug: minimax_log.write("\t" * (depth) + "Beta told me to stop!\n")
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth, name=None):
        if debug: minimax_log.write("\t" * depth + str(depth) + " " + str(state) + "\n")
        if debug and name is not None: minimax_log.write("\t" * (depth) + str(name) + "\n")
        if cutoff_test(state, depth):
            if debug: minimax_log.write("\t" * (depth) + "Cutoff!\n")
            return eval_fn(state)
        v = infinity
        if debug and len(game.actions(state)) == 0:
            minimax_log.write("\t" * (depth) + "No more actions!\n")
        for i, a in enumerate(game.actions(state)):
            if debug: minimax_log.write("\t" * (1+depth) + "Exploring " + str(i) + "\n")
            new_v = max_value(game.result(state, a), alpha, beta, depth+1)
            if debug: minimax_log.write("\t" * (1+depth) + "... " + str(new_v) + " [" + str(v) + "] minimize\n")
            v = min(v, new_v)
            if v <= alpha:
                if debug: minimax_log.write("\t" * (depth) + "Alpha told me to stop!\n")
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state))
    act = argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a),
                                      -infinity, infinity, 0, a))
    if debug: minimax_log.write(str(game.actions(state).index(act)) + " won!\n")
    return act

#______________________________________________________________________________
# Players for Games

def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    return num_or_str(raw_input('Your move? '))

def random_player(game, state):
    "A player that chooses a legal move at random."
    return random.choice(game.actions(state))

def alphabeta_player(game, state):
    return alphabeta_search(state, game)

def play_game(game, *players):
    """Play an n-person, move-alternating game.
    >>> play_game(Fig52Game(), alphabeta_player, alphabeta_player)
    3
    """
    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            state = game.result(state, move)
            if game.terminal_test(state):
                return game.utility(state, game.to_move(game.initial))

#______________________________________________________________________________
# Some Sample Games

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        "Return a list of the allowable moves at this point."
        abstract

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        abstract

    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

class Fig52Game(Game):
    """The game represented in [Fig. 5.2]. Serves as a simple test case.
    >>> g = Fig52Game()
    >>> minimax_decision('A', g)
    'a1'
    >>> alphabeta_full_search('A', g)
    'a1'
    >>> alphabeta_search('A', g)
    'a1'
    """
    succs = dict(A=dict(a1='B', a2='C', a3='D'),
                 B=dict(b1='B1', b2='B2', b3='B3'),
                 C=dict(c1='C1', c2='C2', c3='C3'),
                 D=dict(d1='D1', d2='D2', d3='D3'))
    utils = Dict(B1=3, B2=12, B3=8, C1=2, C2=4, C3=6, D1=14, D2=5, D3=2)
    initial = 'A'

    def actions(self, state):
        return self.succs.get(state, {}).keys()

    def result(self, state, move):
        return self.succs[state][move]

    def utility(self, state, player):
        if player == 'MAX':
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state):
        return state not in ('A', 'B', 'C', 'D')

    def to_move(self, state):
        return if_(state in 'BCD', 'MIN', 'MAX')

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    def __init__(self, h=3, v=3, k=3):
        update(self, h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state # Illegal move has no effect
        board = state.board.copy(); board[move] = state.to_move
        moves = list(state.moves); moves.remove(move)
        return Struct(to_move=if_(state.to_move == 'X', 'O', 'X'),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        return if_(player == 'X', state.utility, -state.utility)

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print board.get((x, y), '.'),
            print

    def compute_utility(self, board, move, player):
        "If X wins with this move, return 1; if O return -1; else return 0."
        if (self.k_in_row(board, move, player, (0, 1)) or
            self.k_in_row(board, move, player, (1, 0)) or
            self.k_in_row(board, move, player, (1, -1)) or
            self.k_in_row(board, move, player, (1, 1))):
            return if_(player == 'X', +1, -1)
        else:
            return 0

    def k_in_row(self, board, move, player, (delta_x, delta_y)):
        "Return true if there is a line through move on board for player."
        x, y = move
        n = 0 # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1 # Because we counted move itself twice
        return n >= self.k

class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if y == 0 or (x, y-1) in state.board]


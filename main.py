import mdp
import pprint
import random
import itertools
from collections import Counter
import minimax

GOOD_GAME_LENGTH = 8

from state import State, Entity, boost_attack, boost_defense, weaken_attack, \
    weaken_defense, attack_opponent, ATTRIBUTE_MIN, ATTRIBUTE_MAX
moves = [boost_attack, boost_defense, weaken_attack, weaken_defense]
    
class BattleSimulation(minimax.Game):
    BATTLE_COUNTER = 0
    def __init__(self, moveset_values):
        self.moveset_values = moveset_values
    
    def legal_moves(self, state):
        if state.turn == "player":
            return state.player.moveset
        else:
            return state.opponent.moveset
    
    def make_move(self, move, state):
        if state.turn == "player":
            new_player, new_opponent = self.moveset_values[move](state.player, state.opponent)
        else:
            new_opponent, new_player = self.moveset_values[move](state.opponent, state.player)
        new_turn = "opponent" if state.turn == "player" else "player"
        #if BattleSimulation.BATTLE_COUNTER % 100000 == 0:
        #    print BattleSimulation.BATTLE_COUNTER
        #    print "\t",new_player
        #    print "\t",new_opponent
        #    print "\t",new_turn
        #BattleSimulation.BATTLE_COUNTER += 1
        return State(new_player, new_opponent, new_turn)
    
    def utility(self, state, player):
        if state.player == "player":
            return state.player.hp - state.opponent.hp
        else:
            return state.opponent.hp - state.player.hp
            
    def to_move(self, state):
        return state.turn
    
    def terminal_test(self, state):
        return state.player.hp <= 0 or state.opponent.hp <= 0

# Returns a sequence of moves that the first player should take to win after
#   GOOD_GAME_LENGTH steps
# first_player needs info about attributes and moves
# second_player needs info about attributes and moves
# more_values should be a mapping to a move to its values
def choose_best_moves(first_player, second_player, move_values):
    battle = BattleSimulation(move_values)
    initial = State(first_player, second_player, "player")
    action, solution = minimax.alphabeta_search_policy(initial, battle, d= GOOD_GAME_LENGTH)
    solution = [s[1] for s in solution]
    pprint.PrettyPrinter(indent=4).pprint([s.__name__ for s in solution])
    return solution

def run_trial(move_values):
    best_moves = []
    opponents = [generate_opponent() for x in xrange(1)]
    for player_moves in itertools.combinations(moves, 3):
        player = generate_player(list(player_moves))
        these_moves = []
        for opponent in opponents:
            these_moves.append(choose_best_moves(player, opponent, move_values))
        print player
        pretty_print_utilities(Counter(itertools.chain.from_iterable(these_moves)))
        best_moves += these_moves
    move_count = Counter(itertools.chain.from_iterable(best_moves))
    return move_count
    
def generate_player(moveset):
    return Entity(5, 5, 5, moveset + [attack_opponent])
    
def generate_opponent(attributes_distribution = random.randint):
    return Entity(5, attributes_distribution(ATTRIBUTE_MIN, ATTRIBUTE_MAX), 
                      attributes_distribution(ATTRIBUTE_MIN, ATTRIBUTE_MAX), 
                      random.sample(moves, 3) + [attack_opponent])

def pretty_print_utilities(utilities):
    total_utilities = sum(utilities.values())
    utilities_percents = {}
    for utility, value in utilities.iteritems():
        utilities_percents[utility.__name__] = str(int(value / float(total_utilities) * 1000) / 10.0) + "%"
    pprint.PrettyPrinter(indent=4).pprint(utilities_percents)
                           
initial_values = [1,2,2,2,2]
move_values = {}
for move, initial_value in zip([attack_opponent] + moves, initial_values):
    move_values[move] = move(initial_value)
utilities = run_trial(move_values)
pretty_print_utilities(utilities)

class MovesetMDP(mdp.MDP):
    def __init__(self, grid, terminals, init=(0, 0), gamma=.9):
        grid.reverse() ## because we want row 0 on bottom, not on top
        MDP.__init__(self, init, actlist=orientations,
                     terminals=terminals, gamma=gamma)
        update(self, grid=grid, rows=len(grid), cols=len(grid[0]))
        for x in range(self.cols):
            for y in range(self.rows):
                self.reward[x, y] = grid[y][x]
                if grid[y][x] is not None:
                    self.states.add((x, y))

    def T(self, state, action):
        if action == None:
            return [(0.0, state)]
        else:
            return [(0.8, self.go(state, action)),
                    (0.1, self.go(state, turn_right(action))),
                    (0.1, self.go(state, turn_left(action)))]

    def go(self, state, direction):
        "Return the state that results from going in this direction."
        state1 = vector_add(state, direction)
        return if_(state1 in self.states, state1, state)

    def to_grid(self, mapping):
        """Convert a mapping from (x, y) to v into a [[..., v, ...]] grid."""
        return list(reversed([[mapping.get((x,y), None)
                               for x in range(self.cols)]
                              for y in range(self.rows)]))

    def to_arrows(self, policy):
        chars = {(1, 0):'>', (0, 1):'^', (-1, 0):'<', (0, -1):'v', None: '.'}
        return self.to_grid(dict([(s, chars[a]) for (s, a) in policy.items()]))


#solution = mdp.policy_iteration(m)
#pprint.PrettyPrinter(indent=4).pprint(solution)
import mdp
import pprint
import random
import itertools
from collections import Counter
import minimax

import cProfile

GOOD_GAME_LENGTH = 8

from mdp_state import State, Entity, boost_attack, boost_defense, weaken_attack, \
    weaken_defense, attack_opponent, ATTRIBUTE_MIN, ATTRIBUTE_MAX
moves = [boost_attack, boost_defense, weaken_attack, weaken_defense]

class BattleSimulation(object):
    def __init__(self, moveset_values, initial, gamma=.9):
        """A Markov Decision Process, defined by an initial state, transition model,
    and reward function. We also keep track of a gamma value, for use by
    algorithms. The transition model is represented somewhat differently from
    the text.  Instead of T(s, a, s') being  probability number for each
    state/action/state triplet, we instead have T(s, a) return a list of (p, s')
    pairs.  We also keep track of the possible states, terminal states, and
    actions for each state. [page 615]"""
        self.init = initial
        self.moveset_values = moveset_values
        self.states = set()
        self.gamma = gamma
        attr_domain = ["low", "medium", "high"]
        for state in itertools.product(xrange(1,1+ATTRIBUTE_MAX), repeat = 4):
            for self_hp in itertools.product(xrange(0,1+ATTRIBUTE_MAX), repeat = 2):
                self.states.add(State(Entity(self_hp[0], state[0], state[1],
                                             initial.player.moveset),
                          Entity(self_hp[1], state[2], state[3],
                                 initial.opponent.moveset)))
        
    def R(self, state):
        "Return a numeric reward for this state."
        return state.player.hp - state.opponent.hp

    def actions(self, state):
        """Set of actions that can be performed in this state.  By default, a
        fixed list of actions, except for terminal states. Override this
        method if you need to specialize by state."""
        if "dead" in (state.player.classify_hp(), state.opponent.classify_hp()):
            return [None]
        else:
            return state.player.moveset

    def T(self, state, action):
        if action == None:
            return [(0.0, state)]
        else:
            p = 1. / len(state.opponent.moveset)
            your_action = action(self.moveset_values[action])(state)
            v =  [(p, counter_attack(self.moveset_values[counter_attack])(your_action))
                            for counter_attack in state.opponent.moveset]
            return v

initial_state = State(Entity(5, 1, 1, [attack_opponent, weaken_defense, boost_attack]),
                      Entity(5, 1, 1, [attack_opponent, weaken_attack, boost_defense]))
initial_moveset_values = {boost_attack: 1, 
                          boost_defense: 1, 
                          weaken_attack: 1, 
                          weaken_defense: 1,
                          attack_opponent: 1}
m = BattleSimulation(initial_moveset_values, initial_state)
solution = mdp.policy_iteration(m)
pprint.PrettyPrinter(indent=4).pprint(solution)
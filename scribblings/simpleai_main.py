from timeit import timeit

from simpleai.search import SearchProblem, astar
from simpleai.search.local import hill_climbing

import sys
import os

class BattleState(object):
    __slots__ = ["health_1", "attack_1", "defense_1",
                 "health_2", "attack_2", "defense_2",
                 "turn"]
    def __init__(self, h1, a1, d1, h2, a2, d2):
        self.health_1 = h1
        self.attack_1 = a1
        self.defense_1 = d1 
        self.health_2 = h2 
        self.attack_2 = a2 
        self.defense_2 = d2
        self.turn = True
    
    def __str__(self):
        return "First {Health: %d, Attack: %d, Defense: %d}, " +\
               "Second {Health: %d, Attack: %d, Defense: %d}, %s turn" %\
               (self.health_1, self.attack_1, self.defense_1, 
                self.health_2, self.attack_2, self.defense_2, "First" if self.turn else "Second")
                
    def copy(self):
        return State(self.health_1, self.attack_1, self.defense_1, self.health_2, self.attack_2, self.defense_2, not self.turn)

class Player(object):
    pass
    
# All the moves will consume and produce a state

def BattleSimulation(moves, player_1, player_2):
    initial = BattleState(100., 10., 10., 100., 10., 10.)
    return random.randint(5)

class FunSearch(SearchProblem):
    def __init__(self, initial_problem, player_1, player_2):
        SearchProblem.__init__(self, initial_state)
        self.player_1 = player_1
        self.player_2 = player_2
        
    def actions(self, state):
        return state.variations()

    def result(self, state, action):
        return action(state)

    def value(self, state):
        return BattleSimulation(state.moves, self.player_1, self.player_2)
   
    def generate_random_state(self):
        return FunState()

    #def heuristic(self, state):


problem = FunProblem(initial_state='')
result = hill_climbing(problem, iterations_limit=None)

print result.state
print result.path()
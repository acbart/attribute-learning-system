import battle_simulation
import time
import numpy
import random

from players import GreedyPlayer, RandomPlayer, MinimaxPlayer

def test_movelist(movelist):
    
    player_1.opponent, player_2.opponent = player_2, player_1
    value, battle_id, winner = battle_simulation(permutation, player_1, player_2)
from battle_simulation import battle_simulation
import numpy
import collections
from config import CONFIG
from time import time

from players import GreedyPlayer, RandomPlayer, MinimaxPlayer

def test_movelist(movelist):
    #Results log
    results_log = open('data/valid-%s.data' % CONFIG['name'], 'w')
    
    p1_moves, p2_moves = movelist[:3], movelist[3:]
    
    TRIALS = 400
    prior_time = time()    
    
    print "Player 1 as random..."
    results_log.write("Player 1 is random\n")
    p1 = RandomPlayer(p1_moves)
    for p2_intelligence in [-1, 0, 3, 6]:
        p2 = MinimaxPlayer(p2_moves, p2_intelligence)
        if p2_intelligence == -1:
            p2 = RandomPlayer(p2_moves)
        p1.opponent, p2.opponent = p2, p1
        winners = []
        for trial in xrange(TRIALS):
            winners.append(battle_simulation(movelist, p1, p2)[2])
        results = collections.Counter(winners)
        results_log.write("%d, %f, %s\n" % (p2_intelligence, (results[0] + results[1])/float(TRIALS), str(results)))
    
    print "Player 2 as random..."
    results_log.write("\nPlayer 2 is random\n")
    p2 = RandomPlayer(p2_moves)
    for p1_intelligence in [-1, 0, 3, 6]:
        p1 = MinimaxPlayer(p1_moves, p1_intelligence)
        if p1_intelligence == -1:
            p1 = RandomPlayer(p1_moves)
        p1.opponent, p2.opponent = p2, p1
        winners = []
        for trial in xrange(TRIALS):
            winners.append(battle_simulation(movelist, p1, p2)[2])
        results = collections.Counter(winners)
        results_log.write("%d, %f, %s\n" % (p1_intelligence, (results[0] + results[2])/float(TRIALS), str(results)))
        
    print "Deterministic validations..."
    results_log.write("\nP1 Intelligence, P2 Intelligence, Correct\n")
    t = 0
    for p1_intelligence in [0,3,6]: 
        for p2_intelligence in [0,3,6]:
            # Generate the players
            p1 = MinimaxPlayer(p1_moves, p1_intelligence)
            p2 = MinimaxPlayer(p2_moves, p2_intelligence)
            p1.opponent, p2.opponent = p2, p1
            
            # Run the battle
            winner = battle_simulation(movelist, p1, p2)[2]
            if p1_intelligence == p2_intelligence:
                w = int(winner in (0, 1))
                results_log.write("%d, %d, %d\n" % (p1_intelligence, p2_intelligence, w))
            elif p1_intelligence < p2_intelligence:
                w = int(winner==2)
                results_log.write("%d, %d, %d\n" % (p1_intelligence, p2_intelligence, w))
            else:
                w = int(winner==1)
                results_log.write("%d, %d, %d\n" % (p1_intelligence, p2_intelligence, w))
            t += w
            prior_time = time()
    results_log.write("Final Result: %d\n" % (t,))

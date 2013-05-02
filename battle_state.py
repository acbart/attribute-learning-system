from config import ATTRIBUTES, ATTRIBUTE_TYPES
from auxiliary import abbreviate

feature_to_attribute_1 = {}
feature_to_attribute_2 = {}
abbreviations = {}
for attribute in ATTRIBUTES:
    left = attribute.replace("self", "player_1").replace("other", "player_2")
    right = attribute.replace("self", "player_2").replace("other", "player_1")
    feature_to_attribute_1[attribute] = left
    feature_to_attribute_2[attribute] = right
    abbreviations[left] = abbreviate(left)

class BattleState(object):
    def __init__(self, source= None, players=None):
        if players is not None:
            self.v = {}
            for feature, stat in players[0].get_initial_stats().iteritems():
                self.v["player_1_"+feature] = stat
            for feature, stat in players[1].get_initial_stats().iteritems():
                self.v["player_2_"+feature] = stat
            self.turn = True
        else:
            self.v = source.v.copy()
            self.turn = not source.turn
        
    # Maps the features to the attacker and defender attributes, depending on turn
    def get_value(self, feature):
        if self.turn:
            return self.v[feature_to_attribute_1[feature]]
        else:
            return self.v[feature_to_attribute_2[feature]]
    
    def apply(self, move):
        new_state = BattleState(self)
        if new_state.turn:
            attribute_name= feature_to_attribute_1[move.feature]
        else:
            attribute_name= feature_to_attribute_2[move.feature]
        new_state.v[attribute_name] = move.evaluate(new_state)
        return new_state
    
    def get_primary_values(self, player):
        return [int(self.v[player+"_primary_"+str(i+1)]) for i in xrange(ATTRIBUTE_TYPES["primary"])]
    
    def is_player_dead(self, player):
        return any(value <= 0 for value in self.get_primary_values(player))
        
    def get_winner(self):
        p1_death = self.is_player_dead("player_1")
        p2_death = self.is_player_dead("player_2")
        if p1_death and p2_death:
            return "Tie"
        elif p1_death:
            return "Player 2 won"
        elif p2_death:
            return "Player 1 won"
        else:
            return "Stalemate"
        
    def players_alive(self):
        return not (self.is_player_dead("player_1") or self.is_player_dead("player_2"))
        
    def is_one_winner(self):
        return self.is_player_dead("player_1") != self.is_player_dead("player_2")
        
    def __str__(self):
        return ", ".join(["%s:%d" % (abbreviations[attribute], value) 
                            for attribute, value in sorted(self.v.iteritems())] 
                        + ["P1" if self.turn else "P2"])
                        
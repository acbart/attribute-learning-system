class BattleState(object):
    __slots__ = ["player_1_health", "player_1_attack", "player_1_defense",
                 "player_2_health", "player_2_attack", "player_2_defense",
                 "turn"]
    move_features = ["self_health", "self_attack", "self_defense",
                    "other_health", "other_attack", "other_defense"]
    def __init__(self, source= None, players=None):
        if players is not None:
            self.player_1_health, self.player_1_attack, self.player_1_defense = players[0].get_initial_stats()
            self.player_2_health, self.player_2_attack, self.player_2_defense = players[1].get_initial_stats()
            self.turn = True
        else:
            self.player_1_health = source.player_1_health
            self.player_1_attack = source.player_1_attack
            self.player_1_defense = source.player_1_defense
            self.player_2_health = source.player_2_health
            self.player_2_attack = source.player_2_attack
            self.player_2_defense = source.player_2_defense
            self.turn = not source.turn
    
    # Maps the features to the attacker and defender attributes, depending on turn
    feature_to_attribute = {"self_health" : ("player_1_health", "player_2_health"),
                            "self_attack" : ("player_1_attack", "player_2_attack"),
                            "self_defense" : ("player_1_defense", "player_2_defense"),
                            "other_health" : ("player_2_health", "player_1_health"),
                            "other_attack" : ("player_2_attack", "player_1_attack"),
                            "other_defense" : ("player_2_defense", "player_1_defense")}
    def get_value(self, feature):
        return getattr(self, BattleState.feature_to_attribute[feature][int(self.turn)])
            
    def apply(self, move):
        for feature, function in move.iteritems():
            attribute_name = BattleState.feature_to_attribute[feature][int(self.turn)]
            setattr(self, attribute_name, function.evaluate(self))
        
    def players_alive(self):
        return int(self.player_1_health) > 0 and int(self.player_2_health) > 0
    
    def absolute_value(self):
        return self.player_1_health + self.player_2_health
    
    def value(self):
        if self.turn:
            return self.player_1_health - self.player_2_health
        else:
            return -(self.player_1_health - self.player_2_health)
        
    def __str__(self):
        return "(H: %d, A: %d, D: %d), (H: %d, A: %d, D: %d), %s" % (self.player_1_health, self.player_1_attack, self.player_1_defense,self.player_2_health, self.player_2_attack, self.player_2_defense, "Att" if self.turn else "Def")
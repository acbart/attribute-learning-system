class BattleState(object):
    __slots__ = ["attacker_health", "attacker_attack", "attacker_defense",
                 "defender_health", "defender_attack", "defender_defense",
                 "turn"]
    move_features = ["self_health", "self_attack", "self_defense",
                    "other_health", "other_attack", "other_defense"]
    def __init__(self, source= None, players=None):
        if players is not None:
            self.attacker_health, self.attacker_attack, self.attacker_defense = players[0].get_initial_stats()
            self.defender_health, self.defender_attack, self.defender_defense = players[1].get_initial_stats()
            self.turn = True
        else:
            self.attacker_health = source.attacker_health
            self.attacker_attack = source.attacker_attack
            self.attacker_defense = source.attacker_defense
            self.defender_health = source.defender_health
            self.defender_attack = source.defender_attack
            self.defender_defense = source.defender_defense
            self.turn = not source.turn
    
    feature_to_attribute = {"self_health" : ("attacker_health", "defender_health"),
                            "self_attack" : ("attacker_attack", "defender_attack"),
                            "self_defense" : ("attacker_defense", "defender_defense"),
                            "other_health" : ("defender_health", "attacker_health"),
                            "other_attack" : ("defender_attack", "attacker_attack"),
                            "other_defense" : ("defender_defense", "attacker_defense")}
    def get_value(self, feature):
        return getattr(self, BattleState.feature_to_attribute[feature][int(self.turn)])
            
    def apply(self, move):
        for feature, function in move.iteritems():
            setattr(self, BattleState.feature_to_attribute[feature][int(self.turn)], function.value(self))
        
    def players_alive(self):
        return int(self.attacker_health) > 0 and int(self.defender_health) > 0
    
    def absolute_value(self):
        return self.attacker_health + self.defender_health
    
    def value(self):
        if self.turn:
            return self.attacker_health - self.defender_health
        else:
            return -(self.attacker_health - self.defender_health)
        
    def __str__(self):
        return "(H: %d, A: %d, D: %d), (H: %d, A: %d, D: %d), %s" % (self.attacker_health, self.attacker_attack, self.attacker_defense,self.defender_health, self.defender_attack, self.defender_defense, "Att" if self.turn else "Def")
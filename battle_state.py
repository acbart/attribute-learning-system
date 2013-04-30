class BattleState(dict):
    move_features = ["self_health", "self_attack", "self_defense",
                    "other_health", "other_attack", "other_defense"]
    def __init__(self, source= None, players=None):
        dict.__init__(self)
        if players is not None:
            self["player_1_health"], self["player_1_attack"], self["player_1_defense"] = players[0].get_initial_stats()
            self["player_2_health"], self["player_2_attack"], self["player_2_defense"] = players[1].get_initial_stats()
            self.turn = True
        else:
            self.update(source)
            self.turn = not source.turn
        
    # Maps the features to the attacker and defender attributes, depending on turn
    feature_to_attribute = {"self_health" : ("player_1_health", "player_2_health"),
                            "self_attack" : ("player_1_attack", "player_2_attack"),
                            "self_defense" : ("player_1_defense", "player_2_defense"),
                            "other_health" : ("player_2_health", "player_1_health"),
                            "other_attack" : ("player_2_attack", "player_1_attack"),
                            "other_defense" : ("player_2_defense", "player_1_defense")}
    def get_value(self, feature):
        return self[BattleState.feature_to_attribute[feature][int(self.turn)]]
        
    def get_winner(self):
        if int(self["player_1_health"]) <= 0 and int(self["player_2_health"]) <= 0:
            return "Tie"
        elif int(self["player_1_health"]) <= 0:
            return "Player 2 won"
        elif int(self["player_2_health"]) <= 0:
            return "Player 1 won"
        else:
            return "Stalemate"
            
    def apply(self, move):
        for function_tree in move:
            feature = function_tree.feature
            attribute_name = BattleState.feature_to_attribute[feature][int(self.turn)]
            self[attribute_name] = function_tree.evaluate(self)
        
    def players_alive(self):
        return int(self["player_1_health"]) > 0 and int(self["player_2_health"]) > 0
        
    def is_one_winner(self):
        return (self["player_2_health"] <= 0) != (self["player_1_health"] <= 0)
    
    def absolute_value(self):
        return self["player_1_health"] + self["player_2_health"]
    
    def value(self):
        return self["player_1_health"] - self["player_2_health"]
        
    def __str__(self):
        return "(H: %d, A: %d, D: %d), (H: %d, A: %d, D: %d), %s" % (self["player_1_health"], self["player_1_attack"], self["player_1_defense"], self["player_2_health"], self["player_2_attack"], self["player_2_defense"], ["Att" if self.turn else "Def"])
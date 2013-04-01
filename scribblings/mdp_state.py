
ATTRIBUTE_MIN, ATTRIBUTE_MAX = 1, 5

class State(object):
    __slots__ = ["player", "opponent"]
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
        
    def __str__(self):
        return "%s\t%s" % (str(self.player), str(self.opponent))
    
    def __repr__(self):
        return "%s\t%s" % (str(self.player), str(self.opponent))
        
    def copy(self):
        return State(self.player.copy(), self.opponent.copy())
        
    def __hash__(self):
        return hash((self.player.classify_hp(), self.player.classify_attack(), self.player.classify_defense(),
                     self.opponent.classify_hp(), self.opponent.classify_attack(), self.opponent.classify_defense()))
    
    def __eq__(self, other):
        return self.player == other.player and self.opponent == other.opponent
        
class Entity(object):
    __slots__ = ["hp", "attack", "defense", "moveset"]
    def __init__(self, hp, attack, defense, moveset):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.moveset = moveset
    
    def __str__(self):
        moves = ", ".join([move.__name__ for move in self.moveset])
        return "Entity(%d, %d, %d, [%s])" % (self.hp, self.attack, self.defense, moves)
        
    def classify_attribute(self, attribute):
        third = (ATTRIBUTE_MAX - ATTRIBUTE_MIN) / 3.
        if getattr(self, attribute) < ATTRIBUTE_MIN + third:
            return "low"
        if getattr(self, attribute) < ATTRIBUTE_MIN + 2 * third:
            return "medium"
        else:
            return "high"
    
    def classify_hp(self): 
        if self.hp <= 0:
            return "dead"
        else:
            return self.classify_attribute("hp")
    def classify_attack(self): return self.classify_attribute("attack")
    def classify_defense(self): return self.classify_attribute("defense")
    
    @classmethod
    def from_entity(cls, other):
        return Entity(other.hp, other.attack, other.defense, 
                      list(other.moveset))
    
    def copy(self):
        return Entity(self.hp, self.attack, self.defense, list(self.moveset))
        
    def __hash__(self):
        return hash((self.hp, self.attack, self.defense))
    
    def __eq__(self, other):
        return self.classify_hp() == other.classify_hp() and self.classify_attack() == other.classify_attack() and self.classify_defense() == other.classify_defense()

def attack_opponent(value):
    def attack_opponent_move(state):
        n = state.copy()
        n.opponent.hp = max(0, int(n.opponent.hp -value * n.player.attack / float(n.opponent.defense)))
        return n
    return attack_opponent_move
    
def boost_attack(value):
    def boost_attack_move(state):
        n = state.copy()
        n.player.attack = min(n.player.attack + value, ATTRIBUTE_MAX)
        return n
    return boost_attack_move
    
def boost_defense(value):
    def boost_defense_move(state):
        n = state.copy()
        n.player.defense = min(n.player.defense + value, ATTRIBUTE_MAX)
        return n
    return boost_defense_move

def weaken_attack(value):
    def weaken_attack_move(state):
        n = state.copy()
        n.opponent.attack = max(n.opponent.attack - value, ATTRIBUTE_MIN)
        return n
    return weaken_attack_move

def weaken_defense(value):
    def weaken_defense_move(state):
        n = state.copy()
        n.opponent.defense = max(n.opponent.defense - value, ATTRIBUTE_MIN)
        return n
    return weaken_defense_move
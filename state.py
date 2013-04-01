
ATTRIBUTE_MIN, ATTRIBUTE_MAX = 1, 10

class State(object):
    __slots__ = ["player", "opponent", "turn"]
    def __init__(self, player, opponent, turn):
        self.player = player
        self.opponent = opponent
        self.turn = turn
        
    def __str__(self):
        return "\t%s\n\t%s\n\t(%s)" % (str(self.player), str(self.opponent), self.turn)
        
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
            return classify_attribute("hp")
    def classify_attack(self): return classify_attribute("attack")
    def classify_defense(self): return classify_attribute("defense")
    
    @classmethod
    def from_entity(cls, other):
        return Entity(other.hp, other.attack, other.defense, 
                      list(other.moveset))

def attack_opponent(value):
    def attack_opponent_move(self, other):
        new_self = Entity.from_entity(self)
        new_other = Entity.from_entity(other)
        new_self.hp -= value * (self.attack / float(self.defense))
        return new_self, new_other
    return attack_opponent_move
    
def boost_attack(value):
    def boost_attack_move(self, other):
        new_self = Entity.from_entity(self)
        new_other = Entity.from_entity(other)
        new_self.attack = min(new_other.attack + value, ATTRIBUTE_MAX)
        if new_self.attack == ATTRIBUTE_MAX: 
            try:
                new_self.moveset.remove(boost_attack)
            except ValueError: pass
        return new_self, new_other
    return boost_attack_move
    
def boost_defense(value):
    def boost_defense_move(self, other):
        new_self = Entity.from_entity(self)
        new_other = Entity.from_entity(other)
        new_self.defense = min(new_other.defense + value, ATTRIBUTE_MAX)
        if new_self.defense == ATTRIBUTE_MAX: 
            try:
                new_self.moveset.remove(boost_defense)
            except ValueError: pass
        return new_self, new_other
    return boost_defense_move

def weaken_attack(value):
    def weaken_attack_move(self, other):
        new_self = Entity.from_entity(self)
        new_other = Entity.from_entity(other)
        new_other.attack = max(new_other.attack - value, ATTRIBUTE_MIN)
        if new_other.attack == ATTRIBUTE_MIN: 
            try:
                new_other.moveset.remove(weaken_attack)
            except ValueError: pass
        return new_self, new_other
    return weaken_attack_move

def weaken_defense(value):
    def weaken_defense_move(self, other):
        new_self = Entity.from_entity(self)
        new_other = Entity.from_entity(other)
        new_other.defense = max(new_other.defense - value, ATTRIBUTE_MIN)
        if new_other.defense == ATTRIBUTE_MIN: 
            try:
                new_other.moveset.remove(weaken_defense)
            except ValueError: pass
        return new_self, new_other
    return weaken_defense_move
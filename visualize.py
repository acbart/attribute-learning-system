import random
import sys
import os
import spyral
from operator import itemgetter

from zss import compare
diff = compare.distance

from function_tree import FunctionTree, AttributeNode, UnaryNode, BinaryNode
from genetic import MoveList, Move, battle_simulation
from players import PLAYERS

os.environ['SDL_VIDEO_CENTERED'] = '1'
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (25, -75)


SIZE = (1250, 650)
S = 30
FONT = None

class FooterTitle(spyral.Sprite):
    def __init__(self, scene, text, pos = None):
        spyral.Sprite.__init__(self, scene)
        self.image = FONT.render(text, color=(255, 255, 255))
        self.anchor = 'midtop'
        if pos is not None:
            self.pos = pos

def draw_node(letter, color, lock = False):
    image = spyral.Image(size=(S, S))
    image.fill((0,0,0,255))
    if lock:
        image.draw_rect(color, (0,0), (S, S), anchor= 'center')
        image.draw_rect((255,255,255), (0,0), (S, S), 1,anchor= 'center')
    else:
        image.draw_circle(color, (0,0), S/2, anchor= 'center')
        image.draw_circle((255,255,255), (0,0), S/2, 1,anchor= 'center')
    image.draw_image(FONT.render(letter), anchor= 'center')
    return image
    
def make_v(s, p0, p1, p2, p3):
    s = spyral.Sprite(s)
    w = abs(p1[0] - p3[0]) + 4
    h = abs(p1[1] - p2[1]) + 4
    s.image = spyral.Image(size=(w,h))
    s.image.fill((0,0,0,255))
    ps = (p1 + spyral.Vec2D(w/2 + 2, 0), p2+ spyral.Vec2D(w/2 + 2, 0), p3+ spyral.Vec2D(w/2 + 2, 0))
    s.image.draw_lines((255, 255, 255), ps, width = 4)
    s.anchor = "midtop"
    s.pos = p0
    s.layer = "bottom"
    return s
    
def make_line(s, p0, p1, p2):
    s = spyral.Sprite(s)
    w = abs(p1[0] - p2[0]) + 4
    h = abs(p1[1] - p2[1]) + 4
    s.image = spyral.Image(size=(w,h))
    s.image.fill((0,0,0,255))
    s.image.draw_lines((255, 255, 255), (p1 + spyral.Vec2D(w/2 + 2, 0), p2+ spyral.Vec2D(w/2 + 2, 0)), width = 4)
    s.anchor = "midtop"
    s.pos = p0
    s.layer = "bottom"
    return s
    

class AttributeNodeSprite(spyral.Sprite):
    value_map = {"health_1" : ("H", (128, 128, 255)),
                 "health_2" : ("H", (255, 128, 128)),
                 "attack_1" : ("A", (128, 128, 255)),
                 "attack_2" : ("A", (255, 128, 128)),
                 "defense_1" : ("D", (128, 128, 255)),
                 "defense_2" : ("D", (255, 128, 128))}
    def __init__(self, scene, node, pos = (50, 50)):
        spyral.Sprite.__init__(self, scene)
        self.image = draw_node(*AttributeNodeSprite.value_map[node.index], lock=node.is_locked())
        self.pos = pos
        self.layer = "top"
        self.anchor = "center"

class NodeSprite(spyral.Sprite):
    def __init__(self, scene, node, pos = (50, 50)):
        spyral.Sprite.__init__(self, scene)
        self.image = draw_node(node.operator.short_name, (128, 128, 128))
        self.pos = pos
        self.layer = "top"
        self.anchor = "center"
        
import objgraph;
def checkBackrefs(something, filename='', ignores=[]):
	objgraph.show_backrefs(something, max_depth=4, too_many= 20, filename= r'C:\Users\acbart\Projects\attribute-learning-system\graph.png', extra_ignore=ignores)
        
class FunctionTreeDrawer(object):
    def __init__(self, scene, movelist, position):
        self.scene = scene
        self.sprites = []
        for i, move in enumerate(movelist.moves):
            if len(move) == 2:
                feature, root = move.items()[0]
                self.sprites += self.make_sprite(root.root, (position - 100., 50 + 200 *i), 0)
                self.sprites += [FooterTitle(scene, str(root.root), (position - 100., 180 + 200 *i))]
                
                feature, root = move.items()[1]
                self.sprites += self.make_sprite(root.root, (position + 100., 50 + 200 *i), 0)
                self.sprites += [FooterTitle(scene, str(root.root), (position + 100., 180 + 200 *i))]
            else:
                feature, root = move.items()[0]
                self.sprites += self.make_sprite(root.root, (position, 50 + 200 *i), 0)
                self.sprites += [FooterTitle(scene, str(root.root), (position, 180 + 200 *i))]
        #for sprite in self.sprites:
            #print sprite.pos
        
    def kill(self):
        for x in self.sprites:
            x.kill()
            #checkBackrefs(x)
            #sys.exit()
        self.sprites = []
        
    def make_sprite(self, node, pos, depth):
        if depth < 1:
            w = S * 1.5
        else:
            w = S
        h = S * 1.5
        if isinstance(node, AttributeNode):
            return [AttributeNodeSprite(self.scene, node, pos)]
        elif isinstance(node, UnaryNode):
            return ([NodeSprite(self.scene, node, pos),
                     make_line(self.scene, pos, spyral.Vec2D(0,0), spyral.Vec2D(0, h))] +
                    self.make_sprite(node.child, pos + spyral.Vec2D(0, h), depth+1))
        elif isinstance(node, BinaryNode):
            return ([NodeSprite(self.scene, node, pos),
                     make_v(self.scene, pos, spyral.Vec2D(-w, h), spyral.Vec2D(0,0), spyral.Vec2D(w, h))] +
                     self.make_sprite(node.left, pos + spyral.Vec2D(-w, h), depth+1) +
                     self.make_sprite(node.right, pos + spyral.Vec2D(w, h), depth+1))
        else:
            return []

class Visualization(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE)
        self.background.fill((0, 0, 0))
        self.set_layers(["bottom", "top"])
        self.register("system.quit", sys.exit)
        self.register("input.keyboard.down.esc", sys.exit)
        
        self.player1 = random.choice(PLAYERS)
        self.player2 = random.choice(PLAYERS)
            
        self.r = MoveList()
        self.l = MoveList()
        self.c = None
        self.drawers = []
        def make_new():
            for drawer in self.drawers:
                drawer.kill()
            self.drawers = [FunctionTreeDrawer(self, self.r, SIZE[0] / 7),
                            FunctionTreeDrawer(self, self.l, SIZE[0] * 6 / 7)]
            movelists = [self.r, self.l, self.r.mutate(), self.l.mutate()]
            if self.c is not None:
                self.drawers += [FunctionTreeDrawer(self, self.c, SIZE[0] / 2)]
                movelists += [self.c]
                print diff(self.c.moves[0].values()[0].root, self.r.moves[0].values()[0].root), diff(self.c.moves[0].values()[0].root, self.l.moves[0].values()[0].root)
            values = {}
            for movelist in movelists:
                values[movelist] = battle_simulation(movelist, self.player1(movelist), self.player2(movelist))
            winners = sorted(values.iteritems(), key=itemgetter(1))
            self.l, self.r = winners[0][0], winners[1][0]
            self.c = self.l.cross_over(self.r)
            
        make_new()
        self.register("input.mouse.up", make_new)
        self.register("input.keyboard.down.space", make_new)
        FooterTitle(self, "Dad").pos = (SIZE[0] / 5, 0)
        FooterTitle(self, "Mom").pos = (SIZE[0] * 4/ 5, 0)
        FooterTitle(self, "Child").pos = (SIZE[0] / 2, 0)
        
spyral.director.init(SIZE)
FONT = spyral.font.Font("spyral/resources/fonts/DejaVuSans.ttf", 12, (0, 0, 0))
spyral.director.run(scene=Visualization())
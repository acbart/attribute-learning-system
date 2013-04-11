import random
import sys
import os
#sys.path.insert(0, os.path.abspath(r"C:\Users\acbart\Projects\Platipy\spyral\\"))
import spyral

from function_tree import FunctionTree, AttributeNode, UnaryNode, BinaryNode
from genetic import MoveList, Move


SIZE = (600, 500)
S = 50
FONT = None

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
    value_map = {"health_1" : ("S.H", (128, 128, 255)),
                 "health_2" : ("O.H", (128, 255, 255)),
                 "attack_1" : ("S.A", (255, 128, 255)),
                 "attack_2" : ("O.A", (255, 255, 128)),
                 "defense_1" : ("S.D", (128, 255, 128)),
                 "defense_2" : ("O.D", (255, 128, 128))}
    def __init__(self, scene, node, pos = (50, 50)):
        spyral.Sprite.__init__(self, scene)
        self.image = draw_node(*AttributeNodeSprite.value_map[node.index], lock=node.is_locked())
        self.pos = pos
        self.layer = "top"
        self.anchor = "center"

class NodeSprite(spyral.Sprite):
    def __init__(self, scene, node, pos = (50, 50)):
        spyral.Sprite.__init__(self, scene)
        self.image = draw_node(node.operator.op, (128, 128, 128))
        self.pos = pos
        self.layer = "top"
        self.anchor = "center"
        
import objgraph;
def checkBackrefs(something, filename='', ignores=[]):
	objgraph.show_backrefs(something, max_depth=4, too_many= 20, filename= r'C:\Users\acbart\Projects\attribute-learning-system\graph.png', extra_ignore=ignores);
        
class FunctionTreeDrawer(object):
    def __init__(self, scene, root, position):
        self.scene = scene
        self.sprites = self.make_sprite(root.root, position)
        #for sprite in self.sprites:
            #print sprite.pos
        
    def kill(self):
        for x in self.sprites:
            x.kill()
            #checkBackrefs(x)
            #sys.exit()
        self.sprites = []
        
    def make_sprite(self, node, pos):
        if isinstance(node, AttributeNode):
            return [AttributeNodeSprite(self.scene, node, pos)]
        elif isinstance(node, UnaryNode):
            return ([NodeSprite(self.scene, node, pos),
                     make_line(self.scene, pos, spyral.Vec2D(0,0), spyral.Vec2D(0, S*2))] +
                    self.make_sprite(node.child, pos + spyral.Vec2D(0, S*2)))
        elif isinstance(node, BinaryNode):
            return ([NodeSprite(self.scene, node, pos),
                     make_v(self.scene, pos, spyral.Vec2D(-S, S*2), spyral.Vec2D(0,0), spyral.Vec2D(S, S*2))] +
                     self.make_sprite(node.left, pos + spyral.Vec2D(-S, S*2)) +
                     self.make_sprite(node.right, pos + spyral.Vec2D(S, S*2)))
        else:
            return []

class Visualization(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self, SIZE)
        self.set_layers(["bottom", "top"])
        self.register("system.quit", sys.exit)
        
        self.r = FunctionTree(AttributeNode("health_1", lock=True))
        self.f = None
        def make_new():
            if self.f is not None: 
                self.f.kill()
            self.r= self.r.mutate()
            self.f = FunctionTreeDrawer(self, self.r, (SIZE[0] / 2, 50))
        self.register("input.mouse.up", make_new)
        
spyral.director.init(SIZE)
FONT = spyral.font.Font("spyral/resources/fonts/DejaVuSans.ttf", 18, (0, 0, 0))
spyral.director.run(scene=Visualization())
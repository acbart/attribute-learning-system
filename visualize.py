import sys
import os
#sys.path.insert(0, os.path.abspath(r"C:\Users\acbart\Projects\Platipy\spyral\\"))
import spyral

SIZE = (600, 500)

class Visualization(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self, SIZE)
        self.register("system.quit", sys.exit)
        
spyral.director.init(SIZE)
spyral.director.run(scene=Visualization())
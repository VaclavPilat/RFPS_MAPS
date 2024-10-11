## \file
# Classes for generating a Babel map

if __name__ == "__main__":
    import os, sys, bpy, math
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from MAIN import *

CENTRAL_PILLAR_RADIUS = 1
CENTRAL_PILLAR_SEGMENTS = 16

class Babel(Map):
    """Tower of Babel
    """

    def __init__(self):
        """Generating map
        """
        super().__init__()
        self.face(self.circle(CENTRAL_PILLAR_RADIUS, CENTRAL_PILLAR_SEGMENTS))
    
    def sin(self, degrees: int|float, radius: int|float) -> float:
        return math.sin(math.radians(degrees)) * radius
    
    def cos(self, degrees: int|float, radius: int|float) -> float:
        return math.cos(math.radians(degrees)) * radius
    
    def circle(self, radius: int|float, count: int) -> list:
        return [V3(self.sin(d, radius), self.cos(d, radius)) for d in (360*i/count for i in range(count))]

if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    Babel().create("Tower of Babel")
    #Scene.forceDepthMaterial()
    #Scene.topIsoRender()
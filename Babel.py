## \file
# Classes for generating a Babel map

if __name__ == "__main__":
    import os, sys, bpy, math
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from MAIN import *

TOWER_FLOOR_HEIGHT = 5
CENTRAL_PILLAR_RADIUS = 0.5
CENTRAL_PILLAR_SEGMENTS = 32
CENTRAL_STAIRCASE_WIDTH = 1.5
CENTRAL_STAIRCASE_FLOOR = 2

class Babel(Map):
    """Tower of Babel
    """

    def __init__(self):
        """Generating map
        """
        super().__init__()
        self.central_staircase()
    
    def central_staircase(self) -> None:
        # Pillar
        pillar_floor = self.circle(CENTRAL_PILLAR_RADIUS, CENTRAL_PILLAR_SEGMENTS)
        pillar_ceiling = [i + V3.UP * TOWER_FLOOR_HEIGHT for i in pillar_floor]
        for a, b in [(i, (i+1)%CENTRAL_PILLAR_SEGMENTS) for i in range(CENTRAL_PILLAR_SEGMENTS)]:
            self.face([pillar_ceiling[a], pillar_ceiling[b], pillar_floor[b], pillar_floor[a]])
        # Steps
        wall_inner = self.circle(CENTRAL_PILLAR_RADIUS + CENTRAL_STAIRCASE_WIDTH, CENTRAL_PILLAR_SEGMENTS)
        #for a, b in [(i, (i+1)%CENTRAL_PILLAR_SEGMENTS) for i in range(CENTRAL_STAIRCASE_FLOOR, CENTRAL_PILLAR_SEGMENTS-CENTRAL_STAIRCASE_FLOOR)]:
        #    self.face([pillar_floor[a], pillar_floor[b], wall_inner[b], wall_inner[a]])
        self.face(
            pillar_floor[-CENTRAL_STAIRCASE_FLOOR:] + pillar_floor[:CENTRAL_STAIRCASE_FLOOR+1]
            + wall_inner[:CENTRAL_STAIRCASE_FLOOR+1][::-1] + wall_inner[-CENTRAL_STAIRCASE_FLOOR:][::-1]
        )
        self.face(
            pillar_floor[int(CENTRAL_PILLAR_SEGMENTS/2-CENTRAL_STAIRCASE_FLOOR):int(CENTRAL_PILLAR_SEGMENTS/2+CENTRAL_STAIRCASE_FLOOR)+1]
            + wall_inner[int(CENTRAL_PILLAR_SEGMENTS/2-CENTRAL_STAIRCASE_FLOOR):int(CENTRAL_PILLAR_SEGMENTS/2+CENTRAL_STAIRCASE_FLOOR)+1][::-1]
        )
    
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
## \file
# Classes for generating a Babel map

if __name__ == "__main__":
    import os, sys, bpy, math
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from MAIN import *

TOWER_FLOOR_HEIGHT = 5
TOWER_FLOOR_THICKNESS = 0.5
CENTER_PILLAR_RADIUS = 0.5
CENTER_PILLAR_SEGMENTS = 32
CENTER_STAIRCASE_WIDTH = 1.5
CENTER_ISLE_SEGMENTS = 2

class Babel(Map):
    """Tower of Babel
    """

    def __init__(self, origin: V3 = V3.ZERO):
        """Generating map
        """
        super().__init__()
        self.ORIGIN = origin
        self.central_staircase()
    
    def central_staircase(self) -> None:
        # Pillar
        pillar_floor = self.circle(CENTER_PILLAR_RADIUS, CENTER_PILLAR_SEGMENTS)
        pillar_ceiling = [i + V3.UP * TOWER_FLOOR_HEIGHT for i in pillar_floor]
        for a, b in [(i, (i+1)%CENTER_PILLAR_SEGMENTS) for i in range(CENTER_PILLAR_SEGMENTS)]:
            self.face([pillar_ceiling[a], pillar_ceiling[b], pillar_floor[b], pillar_floor[a]])
        # Steps
        wall_inner = self.circle(CENTER_PILLAR_RADIUS + CENTER_STAIRCASE_WIDTH, CENTER_PILLAR_SEGMENTS)
        for i in range(2):
            self.central_steps(pillar_floor, wall_inner, i*CENTER_PILLAR_SEGMENTS//2 + CENTER_ISLE_SEGMENTS, i*TOWER_FLOOR_HEIGHT/2)
        # Stair cover walls
    
    def central_steps(self, inner: list|tuple, outer: list|tuple, start: int, offset: int|float = 0) -> None:
        steps = CENTER_PILLAR_SEGMENTS//2 - CENTER_ISLE_SEGMENTS*2 + 1
        heights = [TOWER_FLOOR_HEIGHT/2 * a/(steps) + offset for a in range(steps + 1)]
        for (index, (a, b)) in enumerate([(i%CENTER_PILLAR_SEGMENTS, (i+1)%CENTER_PILLAR_SEGMENTS) for i in range(start, start+steps)]):
            self.face(
                [x + V3.UP * heights[index+1] for x in [inner[a], outer[a]]]
                + [x + V3.UP * heights[index] for x in [outer[a], inner[a]]]
            )
            self.face([y + V3.DOWN * TOWER_FLOOR_THICKNESS for y in
                [x + V3.UP * heights[index+1] for x in [outer[b], inner[b]]]
                + [x + V3.UP * heights[index] for x in [inner[a], outer[a]]]
            ])
            if index >= steps -1:
                break
            self.face([x + V3.UP * heights[index+1] for x in [inner[a], inner[b], outer[b], outer[a]]])
        self.face([x + V3.UP * offset for x in
            [inner[i%CENTER_PILLAR_SEGMENTS] for i in range(start-CENTER_ISLE_SEGMENTS*2, start+1)]
            + [outer[i%CENTER_PILLAR_SEGMENTS] for i in range(start-CENTER_ISLE_SEGMENTS*2, start+1)][::-1]
        ])
        self.face([x(z=self.ORIGIN.z + (+offset-TOWER_FLOOR_THICKNESS)%TOWER_FLOOR_HEIGHT) for x in
            [outer[i%CENTER_PILLAR_SEGMENTS] for i in range(start-CENTER_ISLE_SEGMENTS*2+1, start+1)]
            + [inner[i%CENTER_PILLAR_SEGMENTS] for i in range(start-CENTER_ISLE_SEGMENTS*2+1, start+1)][::-1]
        ])
    
    def sin(self, degrees: int|float, radius: int|float) -> float:
        return math.sin(math.radians(degrees)) * radius
    
    def cos(self, degrees: int|float, radius: int|float) -> float:
        return math.cos(math.radians(degrees)) * radius
    
    def circle(self, radius: int|float, count: int) -> list:
        return [self.ORIGIN+V3.FORWARD*self.sin(d, radius)+V3.LEFT*self.cos(d, radius) for d in (360*i/count for i in range(count))]

if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    Babel(V3.ZERO).create("Tower of Babel")
    Babel(V3.DOWN * TOWER_FLOOR_HEIGHT).create("Tower of Babel")
    Scene.forceDepthMaterial()
    Scene.topIsoRender()
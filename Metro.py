## \file
# Classes for generating a Metro map



if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from MAIN import *



class Metro(Map):
    """Metro station map
    """

    HALLWAY_DEPTH = 1
    HALLWAY_HEIGHT = 3
    HALLWAY_WIDTH = 4

    CONCRETE = (Material.color, "Smooth concrete", (0.2, 0.2, 0.2, 1))
    WALL = (Material.color, "White plaster", (0.9, 0.9, 0.9, 1))
    TILES = (Material.color, "Floor tiles", (0.4, 0.35, 0.25, 1))

    def __init__(self):
        """Generating map
        """
        super().__init__()
        self.load(UnderpassSlopeEntrance, V3.LEFT*30, (3, 30))
        self.load(UnderpassStairsEntrance, V3.RIGHT*self.HALLWAY_WIDTH, (3, 10), rotation=2)



class UnderpassEntrance(Tile):
    """Common structure for an underpass entrance
    """

    CURB_HEIGHT = 0.1
    CURB_WIDTH = 0.25

    def __init__(self, *args):
        """Generating tile
        """
        super().__init__(*args)
        # Upper walls without inner vertices
        TL1, BL1, TR1, BR1 = (a+self.CURB_HEIGHT*V3.UP for a in (self.TL, self.BL, self.TR, self.BR))
        self.face([self.TL, TL1, TR1, self.TR], Metro.CONCRETE)
        self.face([self.TR, TR1, BR1, self.BR], Metro.CONCRETE)
        self.face([self.BR, BR1, BL1, self.BL], Metro.CONCRETE)
        # Upper walls with inner vertices
        self.TLI = self.TL + self.CURB_WIDTH*V3.BACKWARD
        self.BLI = self.BL + self.CURB_WIDTH*V3.FORWARD
        self.TRI = self.TR + self.CURB_WIDTH*V3.BACKWARD + self.CURB_WIDTH*V3.LEFT
        self.BRI = self.BR + self.CURB_WIDTH*V3.FORWARD + self.CURB_WIDTH*V3.LEFT
        TLI1, BLI1, TRI1, BRI1 = (a+self.CURB_HEIGHT*V3.UP for a in (self.TLI, self.BLI, self.TRI, self.BRI))
        self.face([TL1, self.TL, self.TLI, TLI1], Metro.CONCRETE)
        self.face([BLI1, self.BLI, self.BL, BL1], Metro.CONCRETE)
        self.face([TL1, TLI1, TRI1, BRI1, BLI1, BL1, BR1, TR1], Metro.CONCRETE)
        self.face([TLI1, self.TLI, self.TRI, TRI1], Metro.CONCRETE)
        self.face([TRI1, self.TRI, self.BRI, BRI1], Metro.CONCRETE)
        self.face([BRI1, self.BRI, self.BLI, BLI1], Metro.CONCRETE)
        # Lower walls
        self.TRIC, self.BRIC = (a+Metro.HALLWAY_DEPTH*V3.DOWN for a in (self.TRI, self.BRI))
        self.face([self.TRI, self.TRIC, self.BRIC, self.BRI], Metro.WALL)
        self.TRC = self.TR+Metro.HALLWAY_DEPTH*V3.DOWN + self.CURB_WIDTH*V3.BACKWARD
        self.BRC = self.BR+Metro.HALLWAY_DEPTH*V3.DOWN + self.CURB_WIDTH*V3.FORWARD
        self.face([self.TRIC, self.TRC, self.BRC, self.BRIC], Metro.WALL)
        self.TRIF, self.BRIF, self.TRF, self.BRF = (a+Metro.HALLWAY_HEIGHT*V3.DOWN for a in (self.TRIC, self.BRIC, self.TRC, self.BRC))
        self.face([self.TRC, self.TRIC, self.TRIF, self.TRF], Metro.WALL)
        self.face([self.BRIC, self.BRC, self.BRF, self.BRIF], Metro.WALL)
        self.face([self.TRIF, self.BRIF, self.BRF, self.TRF], Metro.TILES)



class UnderpassSlopeEntrance(Tile):
    """Outdoor slope entrance to an underpass hall
    """

    def __init__(self, *args):
        """Generating tile
        """
        super().__init__(*args)
        t = self.load(UnderpassEntrance)
        self.face([t.TLI, t.TRIF, t.TRIC, t.TRI], Metro.WALL)
        self.face([t.BRI, t.BRIC, t.BRIF, t.BLI], Metro.WALL)
        self.face([t.TLI, t.BLI, t.BRIF, t.TRIF], Metro.TILES)



class UnderpassStairsEntrance(Tile):
    """Outdoor stairs entrance to an underpass hall
    """

    STEP_LENGTH = 0.3
    STEP_HEIGHT = 0.15
    STEP_GROUPS = 3

    def __init__(self, *args):
        """Generating tile
        """
        super().__init__(*args)
        t = self.load(UnderpassEntrance)
        height = Metro.HALLWAY_DEPTH + Metro.HALLWAY_HEIGHT
        steps = round(height/self.STEP_HEIGHT)
        depths = list(height*a/steps for a in range(1, steps+1))
        # Generating stairs
        TW = [t.TRIF, t.TRIC, t.TRI]
        BW = [t.BRI, t.BRIC, t.BRIF]
        TL = t.TLI
        BL = t.BLI
        group = 1
        for i in range(steps):
            # Horizontal face
            if i/steps >= group/self.STEP_GROUPS:
                TL1, BL1 = (V3(a.x, (t.TLI+V3.RIGHT*(self.size[1]*group/self.STEP_GROUPS+self.STEP_LENGTH)).y, a.z) for a in (TL, BL))
                group += 1
            else:
                TL1, BL1 = (a + V3.RIGHT*self.STEP_LENGTH for a in (TL, BL))
            self.face([TL, BL, BL1, TL1], Metro.TILES)
            TL = TL1
            BL = BL1
            TW.append(TL)
            BW.insert(0, BL)
            # Vertical face
            TL1, BL1 = (V3(a.x, a.y, (t.TLI+V3.DOWN*depths[i]).z) for a in (TL, BL))
            self.face([TL, BL, BL1, TL1], Metro.TILES)
            TL = TL1
            BL = BL1
            TW.append(TL)
            BW.insert(0, BL)
        self.face([TL, BL, t.BRIF, t.TRIF], Metro.TILES)
        # Adding walls
        self.face(TW, Metro.WALL)
        self.face(BW, Metro.WALL)



if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    Metro().create("Metro station")
    Scene.topIsoRender()
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
        self.load(UnderpassStairsEntrance, V3.RIGHT*self.HALLWAY_WIDTH, (3, 11), rotation=2)

def UnderpassEntrance(self):
    """Common structure for an underpass entrance
    """
    CURB_HEIGHT = 0.1
    CURB_WIDTH = 0.25
    # Upper horizontal faces
    TL1, BL1, TR1, BR1 = (a+CURB_HEIGHT*V3.UP for a in (self.TL, self.BL, self.TR, self.BR))
    self.face([self.TL, TL1, TR1, self.TR], Metro.CONCRETE)
    self.face([self.TR, TR1, BR1, self.BR], Metro.CONCRETE)
    self.face([self.BR, BR1, BL1, self.BL], Metro.CONCRETE)
    # Upper walls with inner vertices
    self.TLI = self.TL + CURB_WIDTH*V3.BACKWARD
    self.BLI = self.BL + CURB_WIDTH*V3.FORWARD
    self.TRI = self.TR + CURB_WIDTH*V3.BACKWARD + CURB_WIDTH*V3.LEFT
    self.BRI = self.BR + CURB_WIDTH*V3.FORWARD + CURB_WIDTH*V3.LEFT
    TLI1, BLI1, TRI1, BRI1 = (a+CURB_HEIGHT*V3.UP for a in (self.TLI, self.BLI, self.TRI, self.BRI))
    self.face([TL1, self.TL, self.TLI, TLI1], Metro.CONCRETE)
    self.face([BLI1, self.BLI, self.BL, BL1], Metro.CONCRETE)
    self.face([TL1, TLI1, TRI1, BRI1, BLI1, BL1, BR1, TR1], Metro.CONCRETE)
    self.face([TLI1, self.TLI, self.TRI, TRI1], Metro.CONCRETE)
    self.face([TRI1, self.TRI, self.BRI, BRI1], Metro.CONCRETE)
    self.face([BRI1, self.BRI, self.BLI, BLI1], Metro.CONCRETE)
    # Lower walls
    self.TRIC, self.BRIC = (a+Metro.HALLWAY_DEPTH*V3.DOWN for a in (self.TRI, self.BRI))
    self.face([self.TRI, self.TRIC, self.BRIC, self.BRI], Metro.WALL)
    self.TRC = self.TR+Metro.HALLWAY_DEPTH*V3.DOWN + CURB_WIDTH*V3.BACKWARD
    self.BRC = self.BR+Metro.HALLWAY_DEPTH*V3.DOWN + CURB_WIDTH*V3.FORWARD
    self.face([self.TRIC, self.TRC, self.BRC, self.BRIC], Metro.WALL)
    self.TRIF, self.BRIF, self.TRF, self.BRF = (a+Metro.HALLWAY_HEIGHT*V3.DOWN for a in (self.TRIC, self.BRIC, self.TRC, self.BRC))
    self.face([self.TRIF, self.BRIF, self.BRF, self.TRF], Metro.TILES)

def UnderpassSlopeEntrance(self):
    """Outdoor slope entrance to an underpass hall
    """
    t = self.load(UnderpassEntrance)
    # Variables
    SLOPE_COUNT = 4
    SLOPE_GAP = 1.5
    SLOPE_LENGTH = (abs(t.TLI.y - t.TRIF.y) - (SLOPE_COUNT-1)*SLOPE_GAP) / SLOPE_COUNT
    SLOPE_HEIGHT = (Metro.HALLWAY_DEPTH + Metro.HALLWAY_HEIGHT) / SLOPE_COUNT
    # Generating mesh
    TL, BL = (t.TLI, t.BLI)
    TW = [t.TRIF, t.TRF, t.TRC, t.TRIC, t.TRI, t.TLI]
    BW = [t.BLI, t.BRI, t.BRIC, t.BRC, t.BRF, t.BRIF]
    for i in range((SLOPE_COUNT-1)*2):
        if i % 2 == 0:
            TL1, BL1 = (a + SLOPE_LENGTH*V3.RIGHT + SLOPE_HEIGHT*V3.DOWN for a in (TL, BL))
        else:
            TL1, BL1 = (a + SLOPE_GAP*V3.RIGHT for a in (TL, BL))
        self.face([TL, BL, BL1, TL1], Metro.TILES)
        TL, BL = (TL1, BL1)
        TW.append(TL1)
        BW.insert(0, BL1)
    self.face([TL, BL, t.BRIF, t.TRIF], Metro.TILES)
    # Creating side walls
    self.face(TW, Metro.WALL)
    self.face(BW, Metro.WALL)

def UnderpassStairsEntrance(self):
    """Outdoor stairs entrance to an underpass hall
    """
    t = self.load(UnderpassEntrance)
    # Variables
    STEP_GROUPS = 3
    STEP_LENGTH = 0.3
    STEP_HEIGHT = 0.15
    STEP_COUNT = round((Metro.HALLWAY_DEPTH + Metro.HALLWAY_HEIGHT) / STEP_HEIGHT)
    STEP_GAP = (abs(t.TLI.y - t.TRI.y) - STEP_COUNT * STEP_LENGTH) / (STEP_GROUPS-1)
    # Generating mesh
    TL, BL = (t.TLI, t.BLI)
    TW = [t.TRF, t.TRC, t.TRIC, t.TRI]
    BW = [t.BRI, t.BRIC, t.BRC, t.BRF]
    for i in range(STEP_GROUPS):
        for j in range(round(i/STEP_GROUPS*STEP_COUNT), round((i+1)/STEP_GROUPS*STEP_COUNT)):
            if i > 0 and j == round(i/STEP_GROUPS*STEP_COUNT):
                TL1, BL1 = (a + V3.RIGHT*(STEP_LENGTH+STEP_GAP) for a in (TL, BL))
            elif j == STEP_COUNT - 1:
                TL1 = V3(TL.x, t.TRIC.y, TL.z)
                BL1 = V3(BL.x, t.BRIC.y, BL.z)
            else:
                TL1, BL1 = (a + V3.RIGHT*STEP_LENGTH for a in (TL, BL))
            self.face([TL, BL, BL1, TL1], Metro.TILES)
            TL, BL = (TL1, BL1)
            TW.append(TL1)
            BW.insert(0, BL1)
            TL1, BL1 = (V3(a.x, a.y, (t.TLI+V3.DOWN*(j+1)/STEP_COUNT*(Metro.HALLWAY_DEPTH+Metro.HALLWAY_HEIGHT)).z) for a in (TL, BL))
            self.face([TL, BL, BL1, TL1], Metro.TILES)
            TL, BL = (TL1, BL1)
            TW.append(TL1)
            BW.insert(0, BL1)
    # Creating side walls
    self.face(TW, Metro.WALL)
    self.face(BW, Metro.WALL)



if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    Metro().create("Metro station")
    Scene.topIsoRender()
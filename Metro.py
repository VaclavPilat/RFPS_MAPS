## \file
# Classes for generating a Metro map

if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from MAIN import *

UNDERPASS_ENTRANCE_WIDTH = 3
UNDERPASS_CURB_HEIGHT = 0.2
UNDERPASS_CURB_WIDTH = 0.25
UNDERPASS_STAIRS_LENGTH = 11
UNDERPASS_STEP_GROUPS = 3
UNDERPASS_STEP_LENGTH = 0.3
UNDERPASS_STEP_HEIGHT = 0.15
UNDERPASS_SLOPE_LENGTH = 30
UNDERPASS_SLOPE_COUNT = 4
UNDERPASS_SLOPE_GAP = 1.5
UNDERPASS_HALLWAY_DEPTH = 1
UNDERPASS_HALLWAY_HEIGHT = 3
UNDERPASS_HALLWAY_WIDTH = 4
STREET_SIDEWALK_WIDTH = 3
STREET_LANE_WIDTH = 3.5
STREET_LANE_COUNT = 2
STREET_CURB_WIDTH = 0.3
STREET_CURB_HEIGHT = 0.2

CONCRETE = (Material.color, "Smooth concrete", (0.2, 0.2, 0.2, 1))
WALL = (Material.color, "White plaster", (0.9, 0.9, 0.9, 1))
TILES = (Material.color, "Floor tiles", (0.4, 0.35, 0.25, 1))
ASPHALT = (Material.color, "Road asphalt", (0, 0, 0, 1))

class Metro(Map):
    """Metro station map
    """

    def __init__(self):
        """Generating map
        """
        super().__init__()
        self.load(UnderpassEntranceSidewalk, V3.ZERO, (STREET_SIDEWALK_WIDTH+STREET_LANE_WIDTH, UNDERPASS_SLOPE_LENGTH+UNDERPASS_HALLWAY_WIDTH+UNDERPASS_STAIRS_LENGTH))
        self.load(UnderpassStairsEntrance, V3.BACKWARD*STREET_SIDEWALK_WIDTH, (UNDERPASS_ENTRANCE_WIDTH, UNDERPASS_STAIRS_LENGTH))
        self.load(UnderpassSlopeEntrance, V3.BACKWARD*STREET_SIDEWALK_WIDTH+V3.RIGHT*(UNDERPASS_HALLWAY_WIDTH+UNDERPASS_STAIRS_LENGTH), (UNDERPASS_ENTRANCE_WIDTH, UNDERPASS_SLOPE_LENGTH), rotation=2)
        self.load(StreetRoad, V3.BACKWARD*(STREET_SIDEWALK_WIDTH+STREET_LANE_WIDTH)+V3.DOWN*STREET_CURB_HEIGHT, (STREET_LANE_WIDTH*STREET_LANE_COUNT, UNDERPASS_SLOPE_LENGTH+UNDERPASS_HALLWAY_WIDTH+UNDERPASS_STAIRS_LENGTH))
        self.load(UnderpassStairsEntrance, V3.BACKWARD*(STREET_SIDEWALK_WIDTH+STREET_LANE_WIDTH*(STREET_LANE_COUNT+2)-UNDERPASS_ENTRANCE_WIDTH), (UNDERPASS_ENTRANCE_WIDTH, UNDERPASS_STAIRS_LENGTH))
        self.load(UnderpassSlopeEntrance, V3.BACKWARD*(STREET_SIDEWALK_WIDTH+STREET_LANE_WIDTH*(STREET_LANE_COUNT+2)-UNDERPASS_ENTRANCE_WIDTH)+V3.RIGHT*(UNDERPASS_HALLWAY_WIDTH+UNDERPASS_STAIRS_LENGTH), (UNDERPASS_ENTRANCE_WIDTH, UNDERPASS_SLOPE_LENGTH), rotation=2)

def UnderpassEntrance(self):
    """Common structure for an underpass entrance
    """
    # Upper horizontal faces
    TL1, BL1, TR1, BR1 = (a+UNDERPASS_CURB_HEIGHT*V3.UP for a in (self.TL, self.BL, self.TR, self.BR))
    self.face([self.TL, TL1, TR1, self.TR], CONCRETE)
    self.face([self.TR, TR1, BR1, self.BR], CONCRETE)
    self.face([self.BR, BR1, BL1, self.BL], CONCRETE)
    # Upper walls with inner vertices
    self.TLI = self.TL + UNDERPASS_CURB_WIDTH*V3.BACKWARD
    self.BLI = self.BL + UNDERPASS_CURB_WIDTH*V3.FORWARD
    self.TRI = self.TR + UNDERPASS_CURB_WIDTH*V3.BACKWARD + UNDERPASS_CURB_WIDTH*V3.LEFT
    self.BRI = self.BR + UNDERPASS_CURB_WIDTH*V3.FORWARD + UNDERPASS_CURB_WIDTH*V3.LEFT
    TLI1, BLI1, TRI1, BRI1 = (a+UNDERPASS_CURB_HEIGHT*V3.UP for a in (self.TLI, self.BLI, self.TRI, self.BRI))
    self.face([TL1, self.TL, self.TLI, TLI1], CONCRETE)
    self.face([BLI1, self.BLI, self.BL, BL1], CONCRETE)
    self.face([TL1, TLI1, TRI1, BRI1, BLI1, BL1, BR1, TR1], CONCRETE)
    self.face([TLI1, self.TLI, self.TRI, TRI1], CONCRETE)
    self.face([TRI1, self.TRI, self.BRI, BRI1], CONCRETE)
    self.face([BRI1, self.BRI, self.BLI, BLI1], CONCRETE)
    # Lower walls
    self.TRIC, self.BRIC = (a+UNDERPASS_HALLWAY_DEPTH*V3.DOWN for a in (self.TRI, self.BRI))
    self.face([self.TRI, self.TRIC, self.BRIC, self.BRI], WALL)
    self.TRC = self.TR+UNDERPASS_HALLWAY_DEPTH*V3.DOWN + UNDERPASS_CURB_WIDTH*V3.BACKWARD
    self.BRC = self.BR+UNDERPASS_HALLWAY_DEPTH*V3.DOWN + UNDERPASS_CURB_WIDTH*V3.FORWARD
    #self.face([self.TRIC, self.TRC, self.BRC, self.BRIC], WALL)
    self.TRIF, self.BRIF, self.TRF, self.BRF = (a+UNDERPASS_HALLWAY_HEIGHT*V3.DOWN for a in (self.TRIC, self.BRIC, self.TRC, self.BRC))
    #self.face([self.TRIF, self.BRIF, self.BRF, self.TRF], TILES)

def UnderpassSlopeEntrance(self):
    """Outdoor slope entrance to an underpass hall
    """
    t = self.load(UnderpassEntrance)
    # Variables
    SLOPE_LENGTH = (abs(t.TLI.y - t.TRIF.y) - (UNDERPASS_SLOPE_COUNT-1)*UNDERPASS_SLOPE_GAP) / UNDERPASS_SLOPE_COUNT
    SLOPE_HEIGHT = (UNDERPASS_HALLWAY_DEPTH + UNDERPASS_HALLWAY_HEIGHT) / UNDERPASS_SLOPE_COUNT
    # Generating mesh
    TL, BL = (t.TLI, t.BLI)
    TW = [t.TRIF, t.TRF, t.TRC, t.TRIC, t.TRI, t.TLI]
    BW = [t.BLI, t.BRI, t.BRIC, t.BRC, t.BRF, t.BRIF]
    for i in range((UNDERPASS_SLOPE_COUNT-1)*2):
        if i % 2 == 0:
            TL1, BL1 = (a + SLOPE_LENGTH*V3.RIGHT + SLOPE_HEIGHT*V3.DOWN for a in (TL, BL))
        else:
            TL1, BL1 = (a + UNDERPASS_SLOPE_GAP*V3.RIGHT for a in (TL, BL))
        self.face([TL, BL, BL1, TL1], TILES)
        TL, BL = (TL1, BL1)
        TW.append(TL1)
        BW.insert(0, BL1)
    self.face([TL, BL, t.BRIF, t.TRIF], TILES)
    # Creating side walls
    self.face(TW, WALL)
    self.face(BW, WALL)

def UnderpassStairsEntrance(self):
    """Outdoor stairs entrance to an underpass hall
    """
    t = self.load(UnderpassEntrance)
    # Variables
    STEP_COUNT = round((UNDERPASS_HALLWAY_DEPTH + UNDERPASS_HALLWAY_HEIGHT) / UNDERPASS_STEP_HEIGHT)
    STEP_GAP = (abs(t.TLI.y - t.TRI.y) - STEP_COUNT * UNDERPASS_STEP_LENGTH) / (UNDERPASS_STEP_GROUPS-1)
    # Generating mesh
    TL, BL = (t.TLI, t.BLI)
    TW = [t.TRF, t.TRC, t.TRIC, t.TRI]
    BW = [t.BRI, t.BRIC, t.BRC, t.BRF]
    for i in range(UNDERPASS_STEP_GROUPS):
        for j in range(round(i/UNDERPASS_STEP_GROUPS*STEP_COUNT), round((i+1)/UNDERPASS_STEP_GROUPS*STEP_COUNT)):
            if i > 0 and j == round(i/UNDERPASS_STEP_GROUPS*STEP_COUNT):
                TL1, BL1 = (a + V3.RIGHT*(UNDERPASS_STEP_LENGTH+STEP_GAP) for a in (TL, BL))
            elif j == STEP_COUNT - 1:
                TL1 = TL(y=t.TRIC.y)
                BL1 = BL(y=t.BRIC.y)
            else:
                TL1, BL1 = (a + V3.RIGHT*UNDERPASS_STEP_LENGTH for a in (TL, BL))
            self.face([TL, BL, BL1, TL1], TILES)
            TL, BL = (TL1, BL1)
            TW.append(TL1)
            BW.insert(0, BL1)
            TL1, BL1 = (a(z=(t.TLI+V3.DOWN*(j+1)/STEP_COUNT*(UNDERPASS_HALLWAY_DEPTH+UNDERPASS_HALLWAY_HEIGHT)).z) for a in (TL, BL))
            self.face([TL, BL, BL1, TL1], TILES)
            TL, BL = (TL1, BL1)
            TW.append(TL1)
            BW.insert(0, BL1)
    # Creating side walls
    self.face(TW, WALL)
    self.face(BW, WALL)

def UnderpassEntranceSidewalk(self):
    """Sidewalk between and around underpass entrances
    """
    # Sidewalk
    TLI1, TRI1 = (a + V3.BACKWARD * STREET_SIDEWALK_WIDTH for a in (self.TL, self.TR))
    TLI2 = TLI1 + V3.RIGHT * UNDERPASS_STAIRS_LENGTH
    TRI2 = TRI1 + V3.LEFT * UNDERPASS_SLOPE_LENGTH
    BLI2, BRI2 = (a + V3.BACKWARD * UNDERPASS_ENTRANCE_WIDTH for a in (TLI2, TRI2))
    BLI1, BRI1 = (a + V3.BACKWARD * UNDERPASS_ENTRANCE_WIDTH for a in (TLI1, TRI1))
    BL, BR = (a + V3.FORWARD * STREET_CURB_WIDTH for a in (self.BL, self.BR))
    self.face([self.TL, TLI1, TLI2, BLI2, BLI1, BL, BR, BRI1, BRI2, TRI2, TRI1, self.TR], TILES) ########
    # Curb
    self.face([BR, BL, self.BL, self.BR], CONCRETE) #####
    BLU, BRU = (a + V3.DOWN * STREET_CURB_HEIGHT for a in (self.BL, self.BR))
    self.face([self.BR, self.BL, BLU, BRU], CONCRETE) #####

def StreetRoad(self):
    """Asphalt road between sidewalks, above underpass
    """
    self.face([self.TR, self.TL, self.BL, self.BR], ASPHALT)

if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    Metro().create("Metro station")
    #Scene.topIsoRender()
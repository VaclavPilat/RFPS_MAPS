if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from MAIN import *



class Metro(Map):
    def __init__(self):
        super().__init__()
        self.load(UnderpassSlopeEntrance, V3.ZERO, (3, 5))



class UnderpassSlopeEntrance(Tile):
    """Outdoor slope entrance to an underpass hall
    """

    CURB_HEIGHT = 0.1
    CURB_WIDTH = 0.25
    HALLWAY_DEPTH = 2
    HALLWAY_HEIGHT = 3

    CONCRETE = (Material.color, "Smooth concrete", (0.2, 0.2, 0.2, 1))
    WALL = (Material.color, "White plaster", (0.9, 0.9, 0.9, 1))
    TILES = (Material.color, "Floor tiles", (0.4, 0.35, 0.25, 1))

    def __init__(self, *args):
        """Generating tile
        """
        super().__init__(*args)
        # Upper walls without inner vertices
        TL1, BL1, TR1, BR1 = (a+self.CURB_HEIGHT*V3.UP for a in (self.TL, self.BL, self.TR, self.BR))
        self.face([self.TL, TL1, TR1, self.TR], self.CONCRETE)
        self.face([self.TR, TR1, BR1, self.BR], self.CONCRETE)
        self.face([self.BR, BR1, BL1, self.BL], self.CONCRETE)
        # Upper walls with inner vertices
        TLI = self.TL + self.CURB_WIDTH*V3.BACKWARD
        BLI = self.BL + self.CURB_WIDTH*V3.FORWARD
        TRI = self.TR + self.CURB_WIDTH*V3.BACKWARD + self.CURB_WIDTH*V3.LEFT
        BRI = self.BR + self.CURB_WIDTH*V3.FORWARD + self.CURB_WIDTH*V3.LEFT
        TLI1, BLI1, TRI1, BRI1 = (a+self.CURB_HEIGHT*V3.UP for a in (TLI, BLI, TRI, BRI))
        self.face([TL1, self.TL, TLI, TLI1], self.CONCRETE)
        self.face([BLI1, BLI, self.BL, BL1], self.CONCRETE)
        self.face([TL1, TLI1, TRI1, BRI1, BLI1, BL1, BR1, TR1], self.CONCRETE)
        self.face([TLI1, TLI, TRI, TRI1], self.CONCRETE)
        self.face([TRI1, TRI, BRI, BRI1], self.CONCRETE)
        self.face([BRI1, BRI, BLI, BLI1], self.CONCRETE)
        # Lower walls
        TRIC, BRIC = (a+self.HALLWAY_DEPTH*V3.DOWN for a in (TRI, BRI))
        self.face([TRI, TRIC, BRIC, BRI], self.WALL)
        TRC = self.TR+self.HALLWAY_DEPTH*V3.DOWN + self.CURB_WIDTH*V3.BACKWARD
        BRC = self.BR+self.HALLWAY_DEPTH*V3.DOWN + self.CURB_WIDTH*V3.FORWARD
        self.face([TRIC, TRC, BRC, BRIC], self.WALL)
        TRIF, BRIF, TRF, BRF = (a+self.HALLWAY_HEIGHT*V3.DOWN for a in (TRIC, BRIC, TRC, BRC))
        self.face([TLI, TRIF, TRF, TRC, TRIC, TRI], self.WALL)
        self.face([BRI, BRIC, BRC, BRF, BRIF, BLI], self.WALL)
        self.face([TLI, BLI, BRIF, TRIF], self.TILES)
        self.face([TRIF, BRIF, BRF, TRF], self.TILES)



if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    Metro().create("Metro station")
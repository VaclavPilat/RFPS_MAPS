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

    def __init__(self, *args):
        """Generating tile
        """
        super().__init__(*args)
        # Upper walls without inner vertices
        TL1, BL1, TR1, BR1 = (a+self.CURB_HEIGHT*V3.UP for a in (self.TL, self.BL, self.TR, self.BR))
        self.face([self.TL, TL1, TR1, self.TR])
        self.face([self.TR, TR1, BR1, self.BR])
        self.face([self.BR, BR1, BL1, self.BL])
        # Upper walls with inner vertices
        TLI = self.TL + self.CURB_WIDTH*V3.BACKWARD
        BLI = self.BL + self.CURB_WIDTH*V3.FORWARD
        TRI = self.TR + self.CURB_WIDTH*V3.BACKWARD + self.CURB_WIDTH*V3.LEFT
        BRI = self.BR + self.CURB_WIDTH*V3.FORWARD + self.CURB_WIDTH*V3.LEFT
        TLI1, BLI1, TRI1, BRI1 = (a+self.CURB_HEIGHT*V3.UP for a in (TLI, BLI, TRI, BRI))
        self.face([TL1, self.TL, TLI, TLI1])
        self.face([BLI1, BLI, self.BL, BL1])
        self.face([TL1, TLI1, TRI1, BRI1, BLI1, BL1, BR1, TR1])
        self.face([TLI1, TLI, TRI, TRI1])
        self.face([TRI1, TRI, BRI, BRI1])
        self.face([BRI1, BRI, BLI, BLI1])
        # Lower walls
        TRIC, BRIC = (a+self.HALLWAY_DEPTH*V3.DOWN for a in (TRI, BRI))
        self.face([TRI, TRIC, BRIC, BRI])
        TRC = self.TR+self.HALLWAY_DEPTH*V3.DOWN + self.CURB_WIDTH*V3.BACKWARD
        BRC = self.BR+self.HALLWAY_DEPTH*V3.DOWN + self.CURB_WIDTH*V3.FORWARD
        self.face([TRIC, TRC, BRC, BRIC])
        TRIF, BRIF, TRF, BRF = (a+self.HALLWAY_HEIGHT*V3.DOWN for a in (TRIC, BRIC, TRC, BRC))
        self.face([TLI, TRIF, TRF, TRC, TRIC, TRI])
        self.face([BRI, BRIC, BRC, BRF, BRIF, BLI])
        self.face([TLI, BLI, BRIF, TRIF])
        self.face([TRIF, BRIF, BRF, TRF])



if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    Metro().create("Metro station")
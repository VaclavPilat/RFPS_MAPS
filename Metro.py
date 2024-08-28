import os, sys, bpy, math
directory = os.path.dirname(bpy.data.filepath)
if not directory in sys.path:
    sys.path.append(directory)
from MAIN import *
from V import *
##############################################

UNDERPASS_HALLWAY_WIDTH = 5
UNDERPASS_HALLWAY_HEIGHT = 3
UNDERPASS_HALLWAY_DEPTH = 1

UNDERPASS_ENTRANCE_TOP = 0.2
UNDERPASS_ENTRANCE_BORDER = 0.3
UNDERPASS_ENTRANCE_WIDTH = 3
UNDERPASS_ENTRANCE_SLOPE = 10
UNDERPASS_ENTRANCE_STAIRS = 5

class Metro(Map):
    def __init__(self) -> None:
        super().__init__()
        Scene.clear()
        self.UNDERPASS_SLOPE()
        self.create("Metro")
    def UNDERPASS_SLOPE(self, S: V = V(0, 0, 0)):
        # Outer points
        TRO = S
        TLO = TRO + UNDERPASS_ENTRANCE_SLOPE * V.LEFT
        BRO = TRO + UNDERPASS_ENTRANCE_WIDTH * V.BACKWARD
        BLO = BRO + UNDERPASS_ENTRANCE_SLOPE * V.LEFT
        # Inner points
        TRI = TRO + UNDERPASS_ENTRANCE_BORDER * (V.LEFT + V.BACKWARD)
        TLI = TLO + UNDERPASS_ENTRANCE_BORDER * V.BACKWARD
        BRI = BRO + UNDERPASS_ENTRANCE_BORDER * (V.LEFT + V.FORWARD)
        BLI = BLO + UNDERPASS_ENTRANCE_BORDER * V.FORWARD
        # Upper points
        TRO1, TLO1, BRO1, BLO1, TRI1, TLI1, BRI1, BLI1 = (x + UNDERPASS_ENTRANCE_TOP * V.UP for x in (TRO, TLO, BRO, BLO, TRI, TLI, BRI, BLI))
        self.face([TLO1, TRO1, BRO1, BLO1, BLI1, BRI1, TRI1, TLI1][::-1])
        # Outer walls
        self.face([TLO, TLI, TLI1, TLO1])
        self.face([TLO, TRO, TRO1, TLO1][::-1])
        self.face([TRO, BRO, BRO1, TRO1][::-1])
        self.face([BLO, BRO, BRO1, BLO1])
        self.face([BLO, BLI, BLI1, BLO1][::-1])
        # Lower points
        TRIC = TRI + UNDERPASS_HALLWAY_DEPTH * V.DOWN
        TRIF = TRIC + UNDERPASS_HALLWAY_HEIGHT * V.DOWN
        BRIC = BRI + UNDERPASS_HALLWAY_DEPTH * V.DOWN
        BRIF = BRIC + UNDERPASS_HALLWAY_HEIGHT * V.DOWN
        self.face([BLI, TLI, TRIF, BRIF][::-1])
        self.face([TRI1, BRI1, BRIC, TRIC][::-1])
        TROC = TRO + UNDERPASS_ENTRANCE_BORDER * V.BACKWARD + UNDERPASS_HALLWAY_DEPTH * V.DOWN
        TROF = TROC + UNDERPASS_HALLWAY_HEIGHT * V.DOWN
        BROC = BRO + UNDERPASS_ENTRANCE_BORDER * V.FORWARD + UNDERPASS_HALLWAY_DEPTH * V.DOWN
        BROF = BROC + UNDERPASS_HALLWAY_HEIGHT * V.DOWN
        self.face([TLI1, TLI, TRIF, TROF, TROC, TRIC, TRI1])
        self.face([BLI, BLI1, BRI1, BRIC, BROC, BROF, BRIF])
        self.face([TRIF, TROF, BROF, BRIF][::-1])
        self.face([TRIC, TROC, BROC, BRIC])

Metro()
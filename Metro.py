import os, sys, bpy, math
directory = os.path.dirname(bpy.data.filepath)
if not directory in sys.path:
    sys.path.append(directory)
from MAIN import *
from V import *
##############################################

UNDERPASS_HALLWAY_WIDTH = 5

UNDERPASS_ENTRANCE_TOP = 0.2
UNDERPASS_ENTRANCE_BORDER = 0.3
UNDERPASS_ENTRANCE_WIDTH = 3
UNDERPASS_ENTRANCE_SLOPE = 10
UNDERPASS_ENTRANCE_STAIRS = 5

def underpass(S: V = V(0, 0, 0)):
    global metro
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
    metro.face([TLO1, TRO1, BRO1, BLO1, BLI1, BRI1, TRI1, TLI1])
    # Outer walls
    metro.face([TLO, TLI, TLI1, TLO1])
    metro.face([TLO, TRO, TRO1, TLO1])
    metro.face([TRO, BRO, BRO1, TRO1])
    metro.face([BLO, BRO, BRO1, BLO1])
    metro.face([BLO, BLI, BLI1, BLO1])

Scene.clear()
metro = Model()
underpass()
metro.create("Metro")
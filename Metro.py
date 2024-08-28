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
    TRO = S
    TRI = TRO + UNDERPASS_ENTRANCE_BORDER * (V.LEFT + V.BACKWARD)
    TLO = TRO + UNDERPASS_ENTRANCE_SLOPE * V.LEFT
    TLI = TLO + UNDERPASS_ENTRANCE_BORDER * V.BACKWARD
    BRO = TRO + UNDERPASS_ENTRANCE_WIDTH * V.BACKWARD
    BRI = BRO + UNDERPASS_ENTRANCE_BORDER * (V.LEFT + V.FORWARD)
    BLO = BRO + UNDERPASS_ENTRANCE_SLOPE * V.LEFT
    BLI = BLO + UNDERPASS_ENTRANCE_BORDER * V.FORWARD
    metro.face([TLO, TRO, BRO, BLO, BLI, BRI, TRI, TLI])


Scene.clear()
metro = Model()
underpass()
metro.create("Metro")
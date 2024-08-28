import os, sys, bpy
directory = os.path.dirname(bpy.data.filepath)
if not directory in sys.path:
    sys.path.append(directory)
from MAIN import *
##############################################

Scene.clear()
model = Model()

model.face([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])

model.create("Warehouse")
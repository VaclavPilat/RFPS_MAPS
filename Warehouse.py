import os, sys, bpy
directory = os.path.dirname(bpy.data.filepath)
if not directory in sys.path:
    sys.path.append(directory)
from MAIN import *
##############################################

Scene.clear()
model = Model()



model.create("test")
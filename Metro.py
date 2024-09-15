if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from MAIN import *



class Metro(Map):
    def __init__(self):
        super().__init__()
        self.face([V3.ZERO, V3.RIGHT, V3.RIGHT+V3.FORWARD, V3.FORWARD])



if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    Metro().create("Metro station")
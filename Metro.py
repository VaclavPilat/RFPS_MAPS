if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from MAIN import *



class Metro(Map):
    def __init__(self):
        super().__init__()
        self.load(Arrow, V3.ZERO, (2, 2))



class Arrow(Tile):
    def __init__(self, *args):
        super().__init__(*args)
        self.face([self.BL, self.C, self.BR, self.C+(self.TL-self.BL)/2])



if __name__ == "__main__":
    Scene.setup()
    Scene.clear()
    Metro().create("Metro station")
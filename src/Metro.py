## \file
# Implementation of the Metro station map
if __name__ == "__main__":
    try:
        import os, sys, bpy
        BLENDER = True
        directory = os.path.dirname(bpy.data.filepath)
        if not directory in sys.path:
            sys.path.append(directory)
    except ImportError:
        BLENDER = False
from Math.Vector import V3
from Mesh.Object import Object, createObjectSubclass
from Mesh.Tile import Tile, Bounds, Box, Anchor
from Utils.Decorators import makeImmutable
if BLENDER:
    from Blender.Object import Blender
    Object.__bases__ = (Blender,) + Object.__bases__



@makeImmutable
class Settings:
    """Class for containing readonly object settings
    """

    def __init__(self, **kwargs) -> None:
        """Initialising a Settings instance with kwarg values
        """
        for key, value in kwargs.items():
            setattr(self, key, value)



SETTINGS = Settings(
    UECH = 0.1, # Underpass entrance curb height (in meters)
    UECW = 0.3, # Underpass entrance curb width (in meters)
    UEWD = 3, # Underpass entrance width (in meters)
    UHDP = 1, # Underpass hallway depth (in meters)
    UHHG = 3, # Underpass hallway height (in meters)
    UHWD = 4, # Underpass hallway width (in meters)
    USCL = 10, # Underpass staircase length (in meters)
    USLC = 3, # Underpass slope count
    USLL = 40, # Underpass slope length (in meters)
    USLR = 8, # Underpass slope ratio
    USTG = 3, # Underpass step group count
    USTH = 0.2, # Underpass step height (in meters)
    USTL = 0.3, # Underpass step length (in meters)
)



@createObjectSubclass(Tile)
def Stairs(self, D: float, G: int, H: float, L: float) -> None:
    """Generating multiple flights of stairs with resting places in between

    Args:
        D (float): Total staircase depth (in meters)
        G (int): Number of step groups
        H (float): Step height (in meters, will be adjusted)
        L (float): Step length (in meters)
    """
    assert G >= 1, "At least 1 step group required"
    VF = round(D / H) # Vertical face count
    HF = VF + 1 # Horizontal face count
    assert HF * L < self.bounds.W, "Steps will not fit horizontally"
    TL, BL = (self.bounds.TL, self.bounds.BL)
    if G >= 2:
        R = (self.bounds.W - (HF - G + 1) * L) / (G - 1) # Resting place length
    I = set(int(i / G * HF) for i in range(1, G)) # Resting place indices
    for i in range(HF):
        if i == HF - 1: # Final horizontal face
            self.face(self.bounds.TR(z=TL.z), TL, BL, self.bounds.BR(z=BL.z))
            break
        # Making a horizontal face
        TL1, BL1 = map(lambda v: v + V3.RIGHT * (R if i in I else L), (TL, BL))
        self.face(TL1, TL, BL, BL1)
        # Making a vertical face
        z = (self.bounds.TL + V3.DOWN * D * (i + 1) / VF).z
        TL2, BL2 = map(lambda v: v(z=z), (TL1, BL1))
        self.face(TL2, TL1, BL1, BL2)
        TL, BL = (TL2, BL2)



@createObjectSubclass(Tile)
def Slopes(self, D: float, S: int, R: float) -> None:
    """Generating multiple (wheelchair accessible) slopes with resting places in between

    Args:
        D (float): Total depth (in meters)
        S (int): Slope count
        R (float): Slope ratio (slope length per meter of descent)
    """
    assert S >= 1, "At least 1 slope is required"
    assert D * R < self.bounds.W, "Slopes would not fit horizontally"
    if S > 1:
        G = (self.bounds.W - D * R) / (S - 1) # Resting place (gap) length
    TL, BL = (self.bounds.TL, self.bounds.BL)
    C = 1 if S == 1 else S - 1 # Resting place count
    for i in range(S + C):
        if i > 0 and i == S + C - 1: # Final face, whatever it might be
            self.face(TL, BL, *map(lambda v: v + V3.DOWN * D, (self.bounds.BR, self.bounds.TR)))
            break
        if i % 2 == 0: # Making a slope face
            z = (self.bounds.TL + V3.DOWN * D * (i // 2 + 1) / S).z
            TL1, BL1 = map(lambda v: (v + V3.RIGHT * (TL.z - z) * R)(z=z), (TL, BL))
        else: # Making a horizontal face
            TL1, BL1 = map(lambda v: v + V3.RIGHT * G, (TL, BL))
        self.face(TL1, TL, BL, BL1)
        TL, BL = (TL1, BL1)



@createObjectSubclass(Tile)
def UnderpassEntrance(self, C: type = None, **kwargs) -> None:
    """Generating an underpass entrance

    Args:
        C (type, optional): Class for generating descent. Defaults to None.
    """
    TLI, TRI = map(lambda v: v + V3.BACKWARD * SETTINGS.UECW, (self.bounds.TL, self.bounds.TR))
    BLI, BRI = map(lambda v: v + V3.FORWARD * SETTINGS.UECW, (self.bounds.BL, self.bounds.BR))
    TRI, BRI = map(lambda v: v + V3.LEFT * SETTINGS.UECW, (TRI, BRI))
    TL1, TR1, BL1, BR1 = map(lambda v: v + V3.UP * SETTINGS.UECH, (self.bounds.TL, self.bounds.TR, self.bounds.BL, self.bounds.BR))
    TLI1, TRI1, BLI1, BRI1 = map(lambda v: v + V3.UP * SETTINGS.UECH, (TLI, TRI, BLI, BRI))
    self.face(TR1, TL1, TLI1, TRI1, BRI1, BLI1, BL1, BR1) # Top face
    # Outer faces
    self.face(TR1, BR1, self.bounds.BR, self.bounds.TR)
    self.face(TL1, TR1, self.bounds.TR, self.bounds.TL)
    self.face(BR1, BL1, self.bounds.BL, self.bounds.BR)
    self.face(TLI1, TL1, self.bounds.TL, TLI)
    self.face(BL1, BLI1, BLI, self.bounds.BL)
    # Inner faces
    self.face(BLI1, BRI1, BRI, BLI)
    self.face(BRI1, TRI1, TRI, BRI)
    self.face(TRI1, TLI1, TLI, TRI)
    # Generating descenting mesh
    if C is not None:
        self.load(C, f"Underpass {str(C).lower()}", Anchor(TLI, BRI), D=SETTINGS.UHDP+SETTINGS.UHHG, **kwargs)



@createObjectSubclass(Object)
def Metro(self) -> None:
    """Generating the Metro station
    """
    self.load(UnderpassEntrance, "Underpass stair entrance", Box(V3.ZERO, 10, 3), C=Stairs, G=SETTINGS.USTG, H=SETTINGS.USTH, L=SETTINGS.USTL)
    self.load(UnderpassEntrance, "Underpass slope entrance", Box(V3.BACKWARD * 3, 40, 3), C=Slopes, S=SETTINGS.USLC, R=SETTINGS.USLR)



if __name__ == "__main__":
    if BLENDER:
        from Blender.Functions import setupForDevelopment, purgeExistingObjects
        setupForDevelopment()
        purgeExistingObjects()
    metro = Metro("Metro station")
    metro.printHierarchy()
    if BLENDER:
        metro.build()
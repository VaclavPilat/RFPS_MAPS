## \file
# Implementation of the Babel map
# \todo Refactor & add docs
if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from Math.Vector import V3
from Math.Interval import I360
from Math.Shape import Circle
from Blender.Object import createObjectSubclass, Object
from Utils.Decorators import defaultKwargsValues, makeImmutable



@makeImmutable
class BabelSettings:
    """Class for storing common Babel map settings
    """

    def __init__(self, floorHeight: float = 5, floorThickness: float = 0.5, wallWidth: float = 0.5, archWidth: float = 2.5,
    archHeight: float = 3, teamCount: int = 2, atriumSegments: int = 8, atriumRadius: float = 10, pillarHeight: float = 3.5,
    pillarRadius: float = 0.5) -> None:
        """Initialising Babel settings

        Args:
            floorHeight (float, optional): Floor height. Defaults to 5.
            floorThickness (float, optional): Floor thickness. Defaults to 0.5.
            wallWidth (float, optional): Wall width. Defaults to 0.5.
            archWidth (float, optional): Arch width. Defaults to 2.5.
            archHeight (float, optional): Arch height. Defaults to 3.
            teamCount (int, optional): Number of team areas. Defaults to 2.
            atriumSegments (int, optional): Number of atrium segments. Defaults to 8.
            atriumRadius (float, optional): Atrium radius. Defaults to 10.
            pillarHeight (float, optional): Pillar height. Defaults to 3.5.
            pillarRadius (float, optional): Pillar radius. Defaults to 0.5.
        """
        ## Babel floor height
        self.floorHeight = floorHeight
        ## Floor thickness
        self.floorThickness = floorThickness
        ## Wall width
        self.wallWidth = wallWidth
        ## Arch width
        self.archWidth = archWidth
        ## Arch height
        assert archHeight < pillarHeight, "Arch height has to be lesser than pillar height"
        self.archHeight = archHeight
        ## Number of team areas
        assert teamCount >= 2, "At least two team areas are required"
        self.teamCount = teamCount
        ## Number of atrium segments
        assert atriumSegments >= 3, "At least 3 atrium segments are required"
        assert atriumSegments % teamCount == 0, "Atrium segment count has to be divisible by team count"
        self.atriumSegments = atriumSegments
        ## Atrium radius
        self.atriumRadius = atriumRadius
        ## Pillar height. Anything above is a part of the ceiling.
        self.pillarHeight = pillarHeight
        ## Pillar radius
        self.pillarRadius = pillarRadius



class BabelObject(Object):
    """Object subclass used for all Babel objects
    """

    def __init__(self, *args, settings: BabelSettings = BabelSettings(), **kwargs) -> None:
        """Initialising a Babel object.

        Args:
            settings (BabelSettings, optional): Babel map settings. Defaults to BabelSettings().
        """
        ## Common map settings
        self.settings = settings
        super().__init__(*args, **kwargs)
    
    @defaultKwargsValues("settings")
    def load(self, *args, **kwargs) -> None:
        """Loading a new object with preset values
        """
        super().load(*args, **kwargs)



@createObjectSubclass(BabelObject)
def Pillar(self) -> None:
    """Generating a pillar
    """
    for face in Circle(self.settings.pillarRadius, self.pivot, I360(points=16)).cylinder(self.settings.pillarHeight):
        self.face(face)



@createObjectSubclass(BabelObject)
def Babel(self) -> None:
    """Generating a floor of a tower of Babel
    """
    for point in Circle(self.settings.atriumRadius, bounds=I360(points=self.settings.atriumSegments)):
        self.load(Pillar, "Atrium wall pillar", point)



if __name__ == "__main__":
    from Blender.Functions import setupForDevelopment, purgeExistingObjects
    setupForDevelopment()
    purgeExistingObjects()
    Babel("Tower of Babel").print().build()
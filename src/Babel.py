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
from Blender.Object import createObjectSubclass, ModuloObject



@createObjectSubclass(ModuloObject)
def Column(self, circle: Circle) -> None:
    """Generating a column

    Args:
        circle (Circle): Column radius.
    """
    for face in circle.cylinder(self.height):
        self.face(face)



@createObjectSubclass(ModuloObject)
def AtriumFloor(self, outer: Circle, inner: Circle) -> None:
    """Generating atrium floor, split into two halves

    Args:
        outer (Circle): Outer circle
        inner (Circle): Inner circle
    """
    for bounds in (I360.HALF1, I360.HALF2):
        self.face(outer(bounds=bounds).face(cutout=inner(bounds=bounds)))



@createObjectSubclass(ModuloObject)
def CenterWall(self, outer: Circle, inner: Circle) -> None:
    """Generating walls around spiral staircase in the middle of the map

    Args:
        outer (Circle): Outer wall circle
        inner (Circle): Inner wall circle
    """
    # Outer wall
    for face in outer.cylinder(self.height, closed=False):
        self.face(face)
    # Inner wall
    for face in inner.cylinder(self.height, closed=False):
        self.face(face, inverted=True)
    # Entrance floor
    """outerPoints, innerPoints = ([x for x in circle(bounds=I360(openEnd=True)) if x not in tuple(circle)[1:-1]] for circle in (outer, inner))
    outerPoints, innerPoints = ([x for x in points if x.x < 0] + [x for x in points if x.x >= 0] for points in (outerPoints, innerPoints))
    self.face(outerPoints + innerPoints[::-1])"""



@createObjectSubclass(ModuloObject)
def SpiralStairs(self, outer: Circle, inner: Circle) -> None:
    """Generating a spiral staircase

    Args:
        outer (Circle): Outer circle
        inner (Circle): inner circle
    """
    # Getting step points
    innerIntersect, outerIntersect = (x(bounds=x.bounds & x.bounds + 180) for x in (inner, outer))
    innerPoints, outerPoints = (tuple(x) for x in (innerIntersect, outerIntersect))
    leftInnerPoints, leftOuterPoints = ([x for x in points if x.x < 0] for points in (innerPoints, outerPoints))
    rightInnerPoints, rightOuterPoints = ([x for x in points if x.x > 0] for points in (innerPoints, outerPoints))
    # Adding step faces
    stepCount = (len(leftInnerPoints) - 1) * 2
    for i in range(stepCount // 2):
        self.face([x(z=(i + stepCount // 2) / stepCount * self.height) for x in leftOuterPoints[i:i+2] + leftInnerPoints[i:i+2][::-1]])
        stepBound = [leftInnerPoints[i+1], leftOuterPoints[i+1]]
        self.face([x(z=(i+stepCount//2) / stepCount * self.height) for x in stepBound] + [x(z=(i+1+stepCount//2) / stepCount * self.height) for x in stepBound[::-1]])
    for i in range(stepCount // 2):
        self.face([x(z=i / stepCount * self.height) for x in rightOuterPoints[i:i+2] + rightInnerPoints[i:i+2][::-1]])
        stepBound = [rightInnerPoints[i+1], rightOuterPoints[i+1]]
        self.face([x(z=i / stepCount * self.height) for x in stepBound] + [x(z=(i+1) / stepCount * self.height) for x in stepBound[::-1]])
    # Adding the middle floor
    middleInnerPoints = [x for x in inner(bounds=I360(openEnd=True)) if x not in leftInnerPoints[1:-1] and x not in rightInnerPoints[1:-1]]
    middleOuterPoints = [x for x in outer(bounds=I360(openEnd=True)) if x not in leftOuterPoints[1:-1] and x not in rightOuterPoints[1:-1]]
    forwardInnerPoints, forwardOuterPoints = ([x for x in points if x.y > 0] for points in (middleInnerPoints, middleOuterPoints))
    self.face([x(z=self.height / 2) for x in forwardOuterPoints + forwardInnerPoints[::-1]])
    # Adding the entrance floor
    backwardInnerPoints = [x for x in middleInnerPoints if x.y < 0 and x.x < 0] + [x for x in middleInnerPoints if x.y < 0 and x.x >= 0]
    backwardOuterPoints = [x for x in middleOuterPoints if x.y < 0 and x.x < 0] + [x for x in middleOuterPoints if x.y < 0 and x.x >= 0]
    self.face(backwardOuterPoints + backwardInnerPoints[::-1])



@createObjectSubclass(ModuloObject)
def Center(self, outer: Circle) -> None:
    """Generating a central column with a spiral staircase inside

    Args:
        outer (Circle): Outer circle
    """
    inner = outer(radius=outer.radius - 0.5)
    column = Circle(radius=1, points=outer.points//4)
    self.load(Column, "Central pillar", circle=column)
    self.load(CenterWall, "Central wall", outer=outer, inner=inner)
    #self.load(SpiralStairs, "Spiral stairs", outer=inner, inner=column(bounds=inner.bounds))



@createObjectSubclass(ModuloObject)
def Atrium(self, outer: Circle) -> None:
    """Generating the atrium in the center of the map

    Args:
        outer (Circle): Outer circle
    """
    ## \todo Calculate the correct Circle instance based on gap size by using arc-goniometric functions
    center = Circle(radius=4, points=outer.points//2, bounds=I360(30, -30%360))
    self.load(AtriumFloor, "Atrium floor", outer=outer, inner=center)
    self.load(Center, "Central staircase", outer=center)
    #for position in Circle(radius=Math.average(outer.radius, center.radius), points=8.vertices():
    #    self.load(Column, "Atrium pillar", height=3, circle=Circle(0.5, 8, position))



@createObjectSubclass(ModuloObject)
def Babel(self) -> None:
    """Generating a floor of a tower of Babel
    """
    atrium = Circle(10, 512)
    self.load(Atrium, "Atrium", outer=atrium)



if __name__ == "__main__":
    from Blender.Functions import setupForDevelopment, purgeExistingObjects
    setupForDevelopment()
    purgeExistingObjects()
    Babel("Tower of Babel", height=5).print().build()
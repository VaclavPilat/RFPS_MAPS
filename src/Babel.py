## \file
# Implementation of the Babel map
if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from Math.Vector import V3
from Math.Interval import I360
from Math.Shape import Circle
from Blender.Object import Object
from Blender.Blender import Blender



def createObject(func: "func") -> "cls":
    """Creating an Object subclass from a generator function

    Args:
        func (func): Generator function

    Returns:
        cls: Object subclass containing the generator function
    """
    class Wrapped(Object):
        pass
    Wrapped.generate = func
    Wrapped.__name__ = func.__name__
    return Wrapped



@createObject
def Column(self, height: int|float, circle: Circle) -> None:
    """Generating a column

    Args:
        height (int | float): Column height.
        circle (Circle): Column radius.
    """
    for face in circle.cylinder(height):
        self.face(face)



@createObject
def CenterWall(self, height: int|float, outer: Circle, inner: Circle) -> None:
    """Generating walls around spiral

    Args:
        height (int | float): Object height
        outer (Circle): Outer wall circle
        inner (Circle): Inner wall circle
    """
    # Outer wall
    for face in outer.cylinder(height, closed=False):
        self.face(face)
    # Inner wall
    for face in inner.cylinder(height, closed=False):
        self.face(face, inverted=True)
    # Entrance floor
    outerPoints, innerPoints = ([x for x in circle(bounds=I360(openEnd=True)) if x not in tuple(circle)[1:-1]] for circle in (outer, inner))
    outerPoints, innerPoints = ([x for x in points if x.x < 0] + [x for x in points if x.x >= 0] for points in (outerPoints, innerPoints))
    self.face(outerPoints + innerPoints[::-1])



@createObject
def SpiralStairs(self, height: int|float, outer: Circle, inner: Circle) -> None:
    """Generating a spiral staircase

    Args:
        height (int|float): Floor height
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
        self.face([x(z=(i + stepCount // 2) / stepCount * height) for x in leftOuterPoints[i:i+2] + leftInnerPoints[i:i+2][::-1]])
        stepBound = [leftInnerPoints[i+1], leftOuterPoints[i+1]]
        self.face([x(z=(i+stepCount//2) / stepCount * height) for x in stepBound] + [x(z=(i+1+stepCount//2) / stepCount * height) for x in stepBound[::-1]])
    for i in range(stepCount // 2):
        self.face([x(z=i / stepCount * height) for x in rightOuterPoints[i:i+2] + rightInnerPoints[i:i+2][::-1]])
        stepBound = [rightInnerPoints[i+1], rightOuterPoints[i+1]]
        self.face([x(z=i / stepCount * height) for x in stepBound] + [x(z=(i+1) / stepCount * height) for x in stepBound[::-1]])
    # Adding the middle floor
    middleInnerPoints = [x for x in inner(bounds=I360(openEnd=True)) if x not in leftInnerPoints[1:-1] and x not in rightInnerPoints[1:-1]]
    middleOuterPoints = [x for x in outer(bounds=I360(openEnd=True)) if x not in leftOuterPoints[1:-1] and x not in rightOuterPoints[1:-1]]
    forwardInnerPoints, forwardOuterPoints = ([x for x in points if x.y > 0] for points in (middleInnerPoints, middleOuterPoints))
    self.face([x(z=height / 2) for x in forwardOuterPoints + forwardInnerPoints[::-1]])
    # Adding the entrance floor
    backwardInnerPoints = [x for x in middleInnerPoints if x.y < 0 and x.x < 0] + [x for x in middleInnerPoints if x.y < 0 and x.x >= 0]
    backwardOuterPoints = [x for x in middleOuterPoints if x.y < 0 and x.x < 0] + [x for x in middleOuterPoints if x.y < 0 and x.x >= 0]
    self.face(backwardOuterPoints + backwardInnerPoints[::-1])



@createObject
def Center(self, height: int|float, outer: Circle) -> None:
    """Generating a central column with a spiral staircase inside

    Args:
        height (int | float): Object height
        outer (Circle): Outer circle
    """
    inner = outer(radius=outer.radius - 0.5)
    column = Circle(radius=1, points=outer.points)
    self.load(Column, "Central pillar", height=height, circle=column)
    self.load(CenterWall, "Central wall", height=height, outer=outer, inner=inner)
    self.load(SpiralStairs, "Spiral stairs", height=height, outer=inner, inner=column(bounds=inner.bounds))



@createObject
def AtriumFloor(self, height: int|float, outer: Circle, inner: Circle) -> None:
    """Generating atrium floor

    Args:
        height (int | float): Floor height
        outer (Circle): Outer circle
        inner (Circle): Inner circle
    """
    self.face(outer.face(cutout=inner))



@createObject
def Atrium(self, height: int|float, outer: Circle) -> None:
    """Generating the atrium in the center of the map

    Args:
        height (int | float): Floor height
        outer (Circle): Outer circle
    """
    center = Circle(radius=4, points=32, bounds=I360(30, -30%360))
    self.load(Center, "Central staircase", height=height, outer=center)
    for bounds in (I360(0, 180), I360(180, 360)):
        self.load(AtriumFloor, "Atrium floor", height=height, outer=outer(bounds=bounds), inner=center(bounds=bounds))
    #for position in Circle(radius=Math.average(outer.radius, center.radius), points=8.vertices():
    #    self.load(Column, "Atrium pillar", height=3, circle=Circle(0.5, 8, position))



@createObject
def Babel(self, height: int|float = 5) -> None:
    """Generating a floor of a tower of Babel

    Args:
        height (int | float, optional): Floor height. Defaults to 5.
    """
    atrium = Circle(10, 64)
    self.load(Atrium, "Atrium", height=height, outer=atrium)



if __name__ == "__main__":
    Blender.setup()
    Blender.purge()
    Babel("Tower of Babel").print().build()
    #Babel("Tower of Babel (above copy)", V3.UP * 5).build()
    #Babel("Tower of Babel (below copy)", V3.DOWN * 5).build()
# RFPS_MAPS v0.2

This repository is a part of the *RFPS* project. It is used for generating meshes of 3D models that are then used in the *RFPS* repository. Instead of *modelling them by hand*, they are created using parametrized scripts. There are a few pros of doing it this way:

- Meshes tend to be more optimized, since what you don't code, you won't have.
- The risk of leaving in misaligned/duplicated vertices is smaller due to builtin checks.
- Scripts are easier to modify with when size changes are required.

This project consists of Python scripts that are meant to be run within the Blender program to generate Blender files. They can also be run outside the Blender context, in order to create simple 2D renders in console.

I would like to improve this project by adding support for applying materials (while not restricting the ability to run scripts outside of Blender) in order to generate quick renders.

## How to run

Make sure that you have Python3 (version 3.10 was used in development) and Blender (3.0) installed.
This project does not have any other dependencies.

Run all tests:
```shell
make test
```

To create 2D model renders in console, do this (you can use the `FILE=Babel.py` argument to only run a specific script):
```shell
make run
```

To show generated models in Blender, run:
```shell
make show
```

## Usage examples

If you want to create your own models, start by creating a new Python script. Declare a function decorated by `createObjectSubclass` from the `Objects` module. Then create faces inside the function, like this:

```python
from src.Mesh import *
from src.Objects import createObjectSubclass
from src.Grids import Grid

@createObjectSubclass()
def Cube(self):
    self += Face(ZERO, RIGHT, UP+RIGHT, UP)
    self += Face(UP, UP+RIGHT, UP+RIGHT+FORWARD, UP+FORWARD)
    self += Face(RIGHT, RIGHT+FORWARD, UP+RIGHT+FORWARD, UP+RIGHT)
    self += Face(FORWARD, ZERO, UP, UP+FORWARD)
    self += Face(RIGHT+FORWARD, FORWARD, UP+FORWARD, UP+RIGHT+FORWARD)
    self += Face(ZERO, FORWARD, RIGHT+FORWARD, RIGHT)

cube = Cube()
print(Grid(cube))
```

Run the script. It will create a simple cube and render its top view to console.
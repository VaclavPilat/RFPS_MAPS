# About RFPS MAPS

This repository is used for generating the static parts of 3D scene maps used in the *RFPS* project.
Instead of creating the map scenes by hand, they are created using parametrized scripts.

There are a few pros of programming meshes instead of *modelling* them by hand:
- The mesh is usually optimalized, since what you don't code, you won't have.
- The risk of leaving in misaligned vertices is smaller because of builtin checks.
- Parametrized scripts are easier to work with when some size change is required.

Blender version 3.0.1 and Python 3.10 were used in development.
I did not use venv because this project does use any depencencies
(except for `bpy`, which is provided by the Blender program itself).

## How to run
Make sure you have Blender installed.
- **Run tests**: `make test`
- **Render model(s) in console**: `make run FILE=Metro.py`
- **Show model(s) in Blender**: `make show FILE=Metro.py`

## Documentation
- **Create documentation**: `make doc`
- **Count lines of code**: `make cloc`
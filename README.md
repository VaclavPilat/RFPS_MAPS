# About RFPS Maps

This project contains scripts for creating maps and other 3D models for the **RFPS** project using Blender's Python support.

Blender version **3.0.1** was used.

## How to run
- **Run tests** : `python3 -m unittest discover -s Tests -p "*Test.py"`
- **To view models** : `blender --python-exit-code 2 --disable-abort-handler --python Babel.py` (replace `Babel.py` with the desired script file name)

## Documentation
- **Create documentation** : `doxygen Doxyfile`
- **Count lines of code** : `cloc . --include-lang=Python`
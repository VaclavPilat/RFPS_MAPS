## \file
# Script for testing usage examples from the source code
import os, importlib, doctest, sys


code = 0

for name in os.listdir("src"):
    path = os.path.join("src", name)

    if os.path.isfile(path) and name.endswith(".py") and name not in ("Blender.py",):

        # Testing doctests in modules
        module = path.replace("/", ".").replace(".py", "")
        results = doctest.testmod(importlib.import_module(module))
        if results.failed > 0:
            code = 1

        # Comparing expected doctest count
        count = open(path).read().count(">>>")
        if results.attempted != count:
            print(f"Testing of {path} skipped {count-results.attempted} doctests.")
            code = 1

sys.exit(code)
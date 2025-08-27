## \file
# Script for testing usage examples from the source code
import os, importlib, doctest


for name in os.listdir("src"):
    path = os.path.join("src", name)

    if os.path.isfile(path) and name.endswith(".py") and name not in ("Blender.py",):

        # Testing doctests in modules
        module = path.replace("/", ".").replace(".py", "")
        results = doctest.testmod(importlib.import_module(module), raise_on_error=True)

        # Comparing expected doctest count
        count = open(path).read().count(">>>")
        assert results.attempted == count, f"Testing of {path} skipped {count-results.attempted} doctests."
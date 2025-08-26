## \file
# Script for testing usage examples from the source code
import os, importlib, doctest


for name in os.listdir("src"):
    path = os.path.join("src", name)
    if os.path.isfile(path) and name.endswith(".py") and name not in ("Blender.py",):
        module = path.replace("/", ".").replace(".py", "")
        results = doctest.testmod(importlib.import_module(module))
        print(f"{path} - {results.attempted - results.failed}/{results.attempted}")